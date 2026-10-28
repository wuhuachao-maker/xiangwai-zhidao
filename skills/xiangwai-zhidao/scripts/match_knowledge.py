#!/usr/bin/env python3
"""跨案例、思想、对照的关键词粗筛。分数只表示关键词重合，不能表示因果或成功率。"""
import argparse
import json
from pathlib import Path
from match_cases import tokens

ROOT = Path(__file__).resolve().parents[1]


def search(query, include_provisional=False, root=ROOT):
    wanted = tokens(query)
    found = []
    for kind in ('cases', 'thoughts', 'comparisons'):
        for path in sorted((Path(root) / 'data' / kind).glob('*.jsonl')):
            for line in path.read_text(encoding='utf-8').splitlines():
                if not line.strip():
                    continue
                item = json.loads(line)
                status = item.get('evidence_status')
                if status == 'fictional' or status == 'provisional' and not include_provisional:
                    continue
                if status not in {'verified', 'provisional'}:
                    continue
                fields = ['title', 'domain', 'scenario', 'goal', 'hidden_side', 'summary', 'candidate_relation', 'similarity', 'differences']
                haystack = ' '.join(str(item.get(f, '')) for f in fields) + ' '.join(item.get('tags', []))
                score = len(wanted & tokens(haystack))
                if score:
                    found.append(dict(score=score, kind=kind, record=item))
    return sorted(found, key=lambda row: (-row['score'], row['record']['id']))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('query')
    parser.add_argument('--include-provisional', action='store_true')
    args = parser.parse_args()
    rows = search(args.query, args.include_provisional)
    if not rows:
        print('无匹配的已核验资料；可另查待核线索。')
    for row in rows[:8]:
        item = row['record']
        print(json.dumps(dict(kind=row['kind'], id=item['id'], title=item['title'], evidence_status=item['evidence_status'], keyword_overlap=row['score'], note='仅关键词线索，按目标、生态、资源、阶段与条件再次筛选'), ensure_ascii=False))
