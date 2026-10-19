#!/usr/bin/env python3
"""Heuristic warning checker for finished ECS technical Markdown prose.

Not an ASD-STE100 compliance checker. Does not interpret code or verify claims.
"""
import argparse
from pathlib import Path
import re
import sys

VAGUE = re.compile(r'\b(?:properly|seamlessly|robustly|quickly|efficiently|as needed|user[- ]friendly|and/or)\b|\betc\.', re.I)
PLACEHOLDER = re.compile(r'\b(?:TBD|TODO|FIXME)\b|\[(?:describe|add|insert|role|capability|value|precondition|trigger|observable|outcome|failure|unknown)[^\]]*\]', re.I)
SENTENCE = re.compile(r'[^.!?]+[.!?](?=\s|$)')


def inspect(text):
    findings=[]
    in_code=False
    for line_no, raw in enumerate(text.splitlines(),1):
        line = raw.strip()
        if line.startswith('```') or line.startswith('~~~'):
            in_code = not in_code
            continue
        if in_code or not line or line.startswith(('<!--','|','>','---')):
            continue
        # Ignore inline code, URLs, and headings. This is a conservative warning pass.
        line = re.sub(r'`[^`]*`', '', line)
        line = re.sub(r'https?://\S+', '', line)
        if line.startswith('#'): continue
        for match in VAGUE.finditer(line):
            findings.append((line_no,'vague term',match.group(0)))
        for match in PLACEHOLDER.finditer(line):
            findings.append((line_no,'unresolved placeholder',match.group(0)))
        for sent in SENTENCE.finditer(line):
            count = len(re.findall(r"\b[\w'-]+\b",sent.group(0)))
            if count > 32:
                findings.append((line_no,f'long sentence ({count} words)',sent.group(0).strip()[:70]))
    return findings


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('files',nargs='+',type=Path)
    parser.add_argument('--strict',action='store_true',help='Exit nonzero if warnings are present')
    args=parser.parse_args()
    warnings=0
    for p in args.files:
        if not p.is_file():
            print(f'ERROR: cannot read {p}',file=sys.stderr)
            return 2
        findings=inspect(p.read_text(encoding='utf-8'))
        warnings+=len(findings)
        for ln,category,detail in findings:
            print(f'{p}:{ln}: {category}: {detail}')
    if warnings:
        print(f'{warnings} possible writing issue(s). Human review is required.')
    else:
        print('No heuristic issues found. This does not prove technical correctness or STE compliance.')
    return 1 if args.strict and warnings else 0

if __name__ == '__main__':
    sys.exit(main())
