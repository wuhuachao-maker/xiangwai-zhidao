"""使用标准库运行：python3 -m unittest discover -s tests -v"""
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from validate_skill import validate
from match_cases import search_cases


class SkillTests(unittest.TestCase):
    def test_skill_structure(self):
        self.assertEqual(validate(ROOT),[])

    def test_no_fictional_case_in_default_search(self):
        self.assertEqual(search_cases('AI 视频流量 客户'),[])

    def test_demo_flag(self):
        results=search_cases('AI 视频流量 客户',include_demo=True)
        self.assertTrue(results)
        self.assertEqual(results[0][1]['evidence_status'],'fictional')


if __name__=='__main__':
    unittest.main()
