#!/usr/bin/env python3
"""检查知识记录、来源和跨记录关系；结构通过不等于事实或因果被证明。"""
import json
import re
from collections import Counter
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FOLDERS = ('cases', 'thoughts', 'comparisons', 'sources')


def records(root=ROOT):
    for folder in FOLDERS:
        for path in sorted((Path(root) / 'data' / folder).glob('*.jsonl')):
            for n, line in enumerate(path.read_text(encoding='utf-8').splitlines(), 1):
                if line.strip():
                    yield folder, path, n, json.loads(line)


def validate(root=ROOT):
    errors = []
    try:
        rows = list(records(root))
    except (ValueError, OSError) as exc:
        return [str(exc)]
    ids = set()
    keys = set()
    lookup = {r['id']: r for _, _, _, r in rows if isinstance(r, dict) and 'id' in r}
    kinds = {r['id']: k for k, _, _, r in rows if isinstance(r, dict) and 'id' in r}
    for kind, path, n, item in rows:
        prefix = f'{path.name}:{n}'
        if not isinstance(item, dict):
            errors.append(f'{prefix} 记录必须为对象')
            continue
        iid = item.get('id')
        if not iid or iid in ids:
            errors.append(f'{prefix} id缺失或重复: {iid}')
        ids.add(iid)
        if kind == 'sources':
            if not re.match(r'^https://', item.get('url', '')) or not item.get('locator'):
                errors.append(f'{prefix} 来源缺少HTTPS链接或正文定位')
            if not item.get('access_method') or not item.get('checked_at'):
                errors.append(f'{prefix} 来源缺少读取方法或核对日期')
            continue
        if item.get('evidence_status') == 'fictional':
            continue
        key = item.get('canonical_key')
        if not key or key in keys:
            errors.append(f'{prefix} canonical_key缺失或重复')
        keys.add(key)
        if kind == 'comparisons':
            if item.get('claim_type') != 'xiangwai_inference' or item.get('evidence_status') != 'provisional':
                errors.append(f'{prefix} 对照不能伪装为已验证规律')
            if len(set(item.get('case_ids', []))) < 2:
                errors.append(f'{prefix} 对照至少需要两条不同案例')
            for rid in item.get('case_ids', []):
                if kinds.get(rid) != 'cases' or lookup[rid].get('evidence_status') == 'fictional':
                    errors.append(f'{prefix} 无效案例引用: {rid}')
            continue
        if item.get('evidence_status') not in {'verified', 'provisional'}:
            errors.append(f'{prefix} 无效证据状态')
        refs = item.get('source_ids', [])
        if not refs:
            errors.append(f'{prefix} 缺少来源ID')
        for rid in refs:
            if kinds.get(rid) != 'sources':
                errors.append(f'{prefix} 无效来源引用: {rid}')
        valid_sources = [lookup[rid] for rid in refs if kinds.get(rid) == 'sources']
        if set(item.get('source_urls', [])) != {s['url'] for s in valid_sources}:
            errors.append(f'{prefix} source_urls与来源登记不一致')
        if item.get('evidence_status') == 'verified' and not any(s.get('access_method') in {'direct_text', 'direct_pdf_text'} for s in valid_sources):
            errors.append(f'{prefix} verified至少需一个可直接核读来源')
        if not item.get('reviewer') or not item.get('review_level'):
            errors.append(f'{prefix} 缺少审核范围')
        if kind == 'cases':
            precision = item.get('decision_date_precision')
            value = item.get('decision_date', '')
            formats = {'year': r'\d{4}', 'month': r'\d{4}-\d{2}', 'day': r'\d{4}-\d{2}-\d{2}'}
            if precision not in formats or not re.fullmatch(formats[precision], value):
                errors.append(f'{prefix} 日期与精度不一致')
            else:
                try:
                    date.fromisoformat(value + {'year': '-01-01', 'month': '-01', 'day': ''}[precision])
                except ValueError:
                    errors.append(f'{prefix} 日期无效')
            if not item.get('claims') or not item.get('unknowns') or not item.get('interpretation_label'):
                errors.append(f'{prefix} 缺少主张、未知或推断标签')
            for claim in item.get('claims', []):
                if claim.get('type') not in {'fact', 'person_view', 'researcher_interpretation'}:
                    errors.append(f'{prefix} 主张类型无效')
                if not claim.get('source_ids') or not set(claim['source_ids']).issubset(refs):
                    errors.append(f'{prefix} 主张的来源未登记于案例')
    return errors


def counts(root=ROOT):
    result = {}
    for kind in FOLDERS:
        items = [r for k, _, _, r in records(root) if k == kind]
        result[kind] = dict(Counter(r.get('evidence_status', 'source_record') for r in items))
    return result


if __name__ == '__main__':
    problems = validate()
    if problems:
        print('\n'.join(problems))
        raise SystemExit(1)
    print('PASS: 唯一性、来源关系、日期精度、证据分层与对照引用')
    print(json.dumps(counts(), ensure_ascii=False))
