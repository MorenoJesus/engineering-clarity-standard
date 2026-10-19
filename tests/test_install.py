"""Exercise the installer CLI in disposable target directories."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def snapshot(root):
    return {str(p.relative_to(root)): p.read_bytes()
            for p in root.rglob('*') if p.is_file()}


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.target = Path(self.temp.name) / 'target repo'
        self.target.mkdir()

    def install(self, *extra):
        return subprocess.run(
            [sys.executable, str(ROOT / 'scripts/install.py'),
             '--scope', 'repo', '--repo', str(self.target), *extra],
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
            [sys.executable, str(ROOT / 'scripts/install.py'), '--scope', 'repo',
             '--repo', str(missing)], capture_output=True, text=True)
        self.assertEqual(2, result.returncode)
        self.assertFalse(missing.exists())
