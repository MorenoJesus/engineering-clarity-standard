#!/usr/bin/env python3
"""Synchronize vendor mirrors from one canonical ECS skill source."""
import argparse
import filecmp
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / '.agents/skills/engineering-clarity'
MIRROR = ROOT / '.claude/skills/engineering-clarity'
PR_SOURCE = ROOT / '.github/PULL_REQUEST_TEMPLATE.md'
PR_MIRROR = ROOT / '.azuredevops/pull_request_template.md'

def snapshot(path):
    return {str(f.relative_to(path)): f.read_bytes() for f in path.rglob('*') if f.is_file()} if path.is_dir() else {}

def check():
    issues = []
    if snapshot(CANONICAL) != snapshot(MIRROR):
        issues.append('Claude skill mirror differs from .agents canonical source.')
    if not PR_MIRROR.exists() or PR_SOURCE.read_bytes() != PR_MIRROR.read_bytes():
        issues.append('Azure Repos PR template differs from GitHub PR template.')
    if issues:
        for issue in issues: print('ERROR:', issue)
        return 1
    print('OK: skill mirrors and PR templates are synchronized.')
    return 0

def sync():
    if not CANONICAL.is_dir():
        raise SystemExit(f'Missing skill source: {CANONICAL}')
    if MIRROR.exists(): shutil.rmtree(MIRROR)
    MIRROR.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(CANONICAL, MIRROR)
    PR_MIRROR.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(PR_SOURCE, PR_MIRROR)
    print('Mirrors regenerated from canonical files.')
    return check()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Check for drift without changing files')
    args = parser.parse_args()
    sys.exit(check() if args.check else sync())
