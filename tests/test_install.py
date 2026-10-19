"""Exercise the installer CLI in disposable target directories."""
from pathlib import Path
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def snapshot(root):
    return {str(p.relative_to(root)): p.read_bytes()
            for p in root.rglob('*') if p.is_file()}


class InstallerTests(unittest.TestCase):
    def command(self, *args):
        return [sys.executable, str(ROOT / 'scripts/install.py'), *args]

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.target = Path(self.temp.name) / 'target repo'
        self.target.mkdir()

    def install(self, *extra):
        return subprocess.run(
            self.command('--scope', 'repo', '--repo', str(self.target), *extra),
            capture_output=True, text=True, check=True)

    def test_dry_run_writes_nothing(self):
        existing = self.target / 'AGENTS.md'
        existing.write_text('Existing project instructions.', encoding='utf-8')
        before = sorted(self.target.rglob('*'))
        content = snapshot(self.target)
        result = self.install('--dry-run')
        self.assertIn('WOULD INSTALL', result.stdout)
        self.assertIn('SKIP', result.stdout)
        self.assertEqual(before, sorted(self.target.rglob('*')))
        self.assertEqual(content, snapshot(self.target))

    def test_install_copies_expected_files_and_is_repeatable(self):
        self.install()
        canonical = ROOT / '.agents/skills/engineering-clarity'
        for base in ('.agents/skills', '.claude/skills'):
            self.assertEqual(snapshot(canonical),
                             snapshot(self.target / base / 'engineering-clarity'))
        for rel in ('AGENTS.md', 'CLAUDE.md', 'GEMINI.md',
                    '.github/copilot-instructions.md',
                    '.github/PULL_REQUEST_TEMPLATE.md',
                    '.github/ISSUE_TEMPLATE/user-story.md',
                    '.azuredevops/pull_request_template.md'):
            self.assertEqual((ROOT / rel).read_bytes(), (self.target / rel).read_bytes())
        before = snapshot(self.target)
        times = {p: p.stat().st_mtime_ns for p in self.target.rglob('*') if p.is_file()}
        result = self.install()
        self.assertIn('SAME:', result.stdout)
        self.assertNotIn('INSTALLED:', result.stdout)
        self.assertEqual(before, snapshot(self.target))
        self.assertEqual(times, {p: p.stat().st_mtime_ns for p in times})

    def test_conflicting_files_and_skills_are_preserved(self):
        (self.target / 'AGENTS.md').write_text('Local rules', encoding='utf-8')
        skill = self.target / '.agents/skills/engineering-clarity'
        skill.mkdir(parents=True)
        (skill / 'SKILL.md').write_text('Customized skill', encoding='utf-8')
        (skill / 'local.txt').write_text('Local extension', encoding='utf-8')
        before = snapshot(self.target)
        result = self.install()
        self.assertIn('SKIP (merge manually)', result.stdout)
        self.assertIn('SKIP (existing skill differs', result.stdout)
        for rel, content in before.items():
            self.assertEqual(content, (self.target / rel).read_bytes())
        self.assertEqual({'SKILL.md', 'local.txt'}, set(snapshot(skill)))
        self.assertTrue((self.target / 'CLAUDE.md').is_file())

    def test_missing_target_fails_without_creating_it(self):
        missing = self.target / 'missing'
        result = subprocess.run(
            self.command('--scope', 'repo', '--repo', str(missing)),
            capture_output=True, text=True)
        self.assertEqual(2, result.returncode)
        self.assertFalse(missing.exists())

    def test_invalid_argument_combinations_write_nothing(self):
        for args in [('--scope', 'repo'),
                     ('--scope', 'user', '--repo', str(self.target)),
                     ('--scope', 'invalid')]:
            with self.subTest(args=args):
                result = subprocess.run(self.command(*args), capture_output=True, text=True)
                self.assertNotEqual(0, result.returncode)
                self.assertEqual([], list(self.target.iterdir()))


class PowerShellInstallerTests(InstallerTests):
    shell = shutil.which('pwsh')

    def setUp(self):
        if not self.shell:
            self.skipTest('PowerShell 7 is not installed')
        super().setUp()

    def command(self, *args):
        mapping = {'--scope': '-Scope', '--repo': '-Repo', '--dry-run': '-DryRun'}
        return [self.shell, '-NoProfile', '-NonInteractive', '-ExecutionPolicy', 'RemoteSigned', '-File',
                str(ROOT / 'scripts/install.ps1'), *[mapping.get(a, a) for a in args]]


class WindowsPowerShellInstallerTests(PowerShellInstallerTests):
    shell = shutil.which('powershell') if os.name == 'nt' else None

    def setUp(self):
        if not self.shell:
            self.skipTest('Windows PowerShell 5.1 is not installed')
        super().setUp()


class InstallerParityTests(unittest.TestCase):
    def test_both_installers_produce_the_same_files_and_statuses(self):
        shells = [s for s in (shutil.which('pwsh'),
                  shutil.which('powershell') if os.name == 'nt' else None) if s]
        if not shells:
            self.skipTest('PowerShell is not installed')
        with tempfile.TemporaryDirectory() as directory:
            # Every process receives an isolated home, including user-scope tests.
            for scope in ('repo', 'user'):
                expected_files = expected_statuses = None
                commands = [[sys.executable, str(ROOT / 'scripts/install.py')]]
                commands += [[s, '-NoProfile', '-NonInteractive', '-ExecutionPolicy', 'RemoteSigned', '-File',
                              str(ROOT / 'scripts/install.ps1')] for s in shells]
                for i, command in enumerate(commands):
                    with self.subTest(scope=scope, command=command[0]):
                        target = Path(directory) / f"{scope} {i} team's [repo]"
                        target.mkdir()
                        env = dict(os.environ)
                        ps = i > 0
                        args = ['-Scope' if ps else '--scope', scope]
                        if scope == 'repo':
                            args += ['-Repo' if ps else '--repo', str(target)]
                        statuses = []
                        for preview in (True, False, False):
                            flags = (['-DryRun' if ps else '--dry-run'] if preview else [])
                            if ps:
                                # Set the test home after shell startup so runtime caches
                                # cannot be mistaken for installer writes.
                                quote = lambda value: "'" + value.replace("'", "''") + "'"
                                invocation = "& " + quote(command[-1]) + " " + " ".join(
                                    a if a.startswith('-') else quote(a) for a in args + flags)
                                setup = "$env:USERPROFILE=" + quote(str(target)) + "; "
                                setup += "$env:HOME=" + quote(str(target)) + "; "
                                run = command[:-2] + ['-Command', setup + invocation]
                            else:
                                env.update(HOME=str(target), USERPROFILE=str(target))
                                run = command + args + flags
                            result = subprocess.run(run, env=env, capture_output=True,
                                                    text=True, check=True)
                            statuses.append([line.split(':', 1)[0] for line in result.stdout.splitlines()
                                             if ':' in line])
                            if preview:
                                self.assertEqual([], list(target.iterdir()))
                        files = snapshot(target)
                        if expected_files is None:
                            expected_files, expected_statuses = files, statuses
                        else:
                            self.assertEqual(expected_files, files)
                            self.assertEqual(expected_statuses, statuses)
