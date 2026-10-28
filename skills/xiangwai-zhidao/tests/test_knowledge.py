import json
import tempfile
import unittest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from validate_knowledge import validate
from match_knowledge import search


class KnowledgeTests(unittest.TestCase):
    def test_repository_is_valid(self):
        self.assertEqual(validate(), [])

    def test_default_search_never_returns_candidates_or_demo(self):
        rows = search('青蒿 科学 失败 定策')
        self.assertTrue(rows)
        self.assertTrue(all(r['record']['evidence_status'] == 'verified' for r in rows))
        self.assertTrue(any(r['record']['id'] == 'XW-RC-0019' for r in search('青蒿', True)))
        self.assertFalse(any(r['record']['id'] == 'XW-RC-0019' for r in search('青蒿')))

    def test_dangling_source_and_duplicate_key_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            p = root / 'data' / 'thoughts' / 'test.jsonl'
            p.parent.mkdir(parents=True)
            base = dict(id='a',canonical_key='same',evidence_status='verified',source_ids=['missing'])
            p.write_text(json.dumps(base)+'\n'+json.dumps(dict(base,id='b'))+'\n')
            errors = validate(root)
            self.assertTrue(any('无效来源引用' in e for e in errors))
            self.assertTrue(any('canonical_key缺失或重复' in e for e in errors))

    def test_comparison_cannot_be_promoted_to_proven_rule(self):
        with tempfile.TemporaryDirectory() as temp:
            p = Path(temp) / 'data' / 'comparisons' / 'test.jsonl'
            p.parent.mkdir(parents=True)
            p.write_text(json.dumps(dict(id='c', canonical_key='c', claim_type='fact', evidence_status='verified',case_ids=[]))+'\n')
            self.assertTrue(any('不能伪装' in e for e in validate(temp)))


if __name__ == '__main__':
    unittest.main()
