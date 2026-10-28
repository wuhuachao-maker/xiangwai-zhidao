#!/usr/bin/env python3
"""案例关键词粗筛；不作概率预测，不调用网络。"""
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data' / 'cases'


def tokens(text):
    # 保留英文词，并用中文二字片段帮助无需第三方依赖的简易匹配。
    normalized = re.sub(r'[^\u4e00-\u9fffA-Za-z0-9]+', ' ', text.lower())
    result = set()
    for section in normalized.split():
        if re.search(r'[\u4e00-\u9fff]', section):
            result.add(section)
            result.update(section[i:i+2] for i in range(len(section)-1))
        else:
            result.add(section)
    return result


def search_cases(query, include_demo=False, include_provisional=False):
    query_tokens = tokens(query)
    results = []
    for path in DATA.glob('*.jsonl'):
        for row in path.read_text(encoding='utf-8').splitlines():
            if not row.strip():
                continue
            item = json.loads(row)
            if item['evidence_status'] == 'fictional' and not include_demo:
                continue
            if item['evidence_status'] == 'provisional' and not include_provisional:
                continue
            haystack = ' '.join([item.get('title',''),item.get('domain',''),item.get('scenario',''),item.get('goal',''),item.get('visible_side',''),item.get('hidden_side','')] + item.get('tags',[]))
            overlap = query_tokens & tokens(haystack)
            score = len(overlap)
            if score:
                results.append((score,item))
    return sorted(results,key=lambda r:r[0],reverse=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='象外之道案例粗筛（仅线索，不代表概率）')
    parser.add_argument('query',help='描述问题，例如：AI 视频流量差')
    parser.add_argument('--include-demo',action='store_true',help='包括虚构演示案例；不可当作事实证据')
    parser.add_argument('--include-provisional',action='store_true',help='包括待核线索；不得作为已核验证据')
    args = parser.parse_args()
    matches = search_cases(args.query,include_demo=args.include_demo,include_provisional=args.include_provisional)
    if not matches:
        print('当前没有可用于真实证据匹配的案例。请先录入经过来源核验的真实案例；若仅测试格式可加 --include-demo。')
    for score,case in matches[:5]:
        label = '【虚构演示，不能作为证据】' if case['evidence_status']=='fictional' else '【待核实】' if case['evidence_status']=='provisional' else '【已核实来源】'
        print(f"{label} {case['id']} {case['title']} (关键词命中 {score})\n  可能对岸：{case['hidden_side']}\n  行动：{case['action']}\n")
