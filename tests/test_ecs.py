import importlib.util
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / '.agents/skills/engineering-clarity'

class EcsTests(unittest.TestCase):
    def test_frontmatter(self):
        text = (SKILL / 'SKILL.md').read_text(encoding='utf-8')
        self.assertTrue(text.startswith('---\n'))
        self.assertRegex(text, r'(?m)^name: engineering-clarity$')
        self.assertRegex(text, r'(?m)^description: .{20,1024}$')
        self.assertEqual('engineering-clarity', SKILL.name)

    def test_skill_mirror(self):
        source = {str(p.relative_to(SKILL)):p.read_bytes() for p in SKILL.rglob('*') if p.is_file()}
        dst = ROOT / '.claude/skills/engineering-clarity'
        mirror = {str(p.relative_to(dst)):p.read_bytes() for p in dst.rglob('*') if p.is_file()}
        self.assertEqual(source, mirror)

    def test_pr_template_mirror(self):
        self.assertEqual((ROOT / '.github/PULL_REQUEST_TEMPLATE.md').read_bytes(),
                         (ROOT / '.azuredevops/pull_request_template.md').read_bytes())

    def test_skill_local_references(self):
        text=(SKILL/'SKILL.md').read_text(encoding='utf-8')
        for rel in re.findall(r'`((?:references|assets|examples)/[^`]+\.md)`',text):
            self.assertTrue((SKILL / rel).is_file(), rel)

    def test_checker_finds_vague_word(self):
        spec=importlib.util.spec_from_file_location('clarity_checker',ROOT/'scripts/check_clarity.py')
        mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
        issues=mod.inspect('The system should work properly.\n')
        self.assertTrue(any(item[1]=='vague term' for item in issues))
        clean=mod.inspect('If the token is invalid, return HTTP 401.\n')
        self.assertFalse(clean)

if __name__ == '__main__': unittest.main()
