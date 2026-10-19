#!/usr/bin/env python3
"""Install ECS skill and repository adapters without overwriting conflicts."""
import argparse
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / '.agents/skills/engineering-clarity'
FILES = [
    'AGENTS.md',
    'CLAUDE.md',
    'GEMINI.md',
    '.github/copilot-instructions.md',
    '.github/PULL_REQUEST_TEMPLATE.md',
    '.github/ISSUE_TEMPLATE/user-story.md',
    '.azuredevops/pull_request_template.md',
]

def copy_file(src, dst, dry_run):
    if dst.is_file() and src.read_bytes() == dst.read_bytes():
        print('SAME: ', dst)
        return
    if dst.exists():
        print('SKIP (merge manually):', dst)
        return
    print(('WOULD INSTALL: ' if dry_run else 'INSTALLED: '), dst)
    if not dry_run:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)

def copy_skill(destination, dry_run):
    if destination.exists():
        def snapshot(d):
            return {str(p.relative_to(d)): p.read_bytes() for p in d.rglob('*') if p.is_file()}
        if snapshot(destination) == snapshot(SKILL):
            print('SAME: ', destination)
        else:
            print('SKIP (existing skill differs; review and update manually):', destination)
        return
    print(('WOULD INSTALL SKILL: ' if dry_run else 'INSTALLED SKILL: '), destination)
    if not dry_run:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(SKILL, destination)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scope', required=True, choices=('repo', 'user'))
    parser.add_argument('--repo', help='Target repository directory; required for --scope repo')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    if args.scope == 'repo':
        if not args.repo:
            parser.error('--repo is required for --scope repo')
        target = Path(args.repo).expanduser().resolve()
        if not target.is_dir():
            parser.error(f'Repository directory does not exist: {target}')
        for base in ('.agents/skills', '.claude/skills'):
            copy_skill(target / base / 'engineering-clarity', args.dry_run)
        for rel in FILES:
            copy_file(ROOT / rel, target / rel, args.dry_run)
        print('Review all SKIP entries; then commit approved changes for team and cloud-agent use.')
    else:
        if args.repo:
            parser.error('--repo is only valid for --scope repo')
        home = Path.home()
        copy_skill(home / '.agents/skills/engineering-clarity', args.dry_run)
        copy_skill(home / '.claude/skills/engineering-clarity', args.dry_run)
        print('Personal skills installed for supported local clients. Global always-on instruction files are not modified.')
    print('Done. Skill selection depends on the agent and task; review results.')

if __name__ == '__main__':
    main()
