#!/usr/bin/env python3
"""零依赖的 Agent Skill 结构和 JSONL 初步校验。"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / 'data' / 'cases'
MODELS = ROOT / 'data' / 'models'
REQUIRED_CASE_FIELDS = {'id','title','domain','scenario','goal','visible_side','hidden_side','action','outcome','tags','source_urls','evidence_status','source_type','as_of'}
ALLOWED_CASE_STATUSES = {'verified','provisional','fictional'}
ALLOWED_SOURCE_TYPES = {'primary','secondary','illustrative'}


def validate(root=ROOT):
    root = Path(root)
    errors = []
    skill = root / 'SKILL.md'
    if not skill.is_file():
        return ['缺少 SKILL.md']
    data = skill.read_text(encoding='utf-8')
    match = re.match(r'\A---\s*\n(.*?)\n---\s*\n', data, re.S)
    if not match:
        errors.append('SKILL.md 缺少 YAML frontmatter')
    else:
        head = match.group(1)
        name = re.search(r'^name:\s*([a-z0-9-]+)\s*$', head, re.M)
        desc = re.search(r'^description:\s*(.+)$', head, re.M)
        if not name or name.group(1) != root.name or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', root.name):
            errors.append('name 不符合规范或不等于目录名')
        if not desc or not 1 <= len(desc.group(1).strip()) <= 1024:
            errors.append('description 缺失或超长')
        if not re.search(r'定果\s*[→、,，]\s*观局\s*[→、,，]\s*寻根\s*[→、,，]\s*定策', data):
            errors.append('未找到固定核心决策顺序')

    ids = set()
    for folder in [root/'data'/'cases', root/'data'/'models']:
        if not folder.is_dir():
            errors.append(f'缺少目录 {folder.relative_to(root)}')
            continue
        for file in folder.glob('*.jsonl'):
            for lineno, line in enumerate(file.read_text(encoding='utf-8').splitlines(), 1):
                if not line.strip():
                    continue
                try:
                    item = json.loads(line)
                except json.JSONDecodeError as exc:
                    errors.append(f'{file.name}:{lineno} JSON 无效: {exc}')
                    continue
                if not isinstance(item,dict):
                    errors.append(f'{file.name}:{lineno} 必须是对象')
                    continue
                iid = item.get('id')
                if not iid or iid in ids:
                    errors.append(f'{file.name}:{lineno} id 缺失或重复: {iid}')
                ids.add(iid)
                if folder.name == 'cases':
                    missing = REQUIRED_CASE_FIELDS - item.keys()
                    if missing:
                        errors.append(f'{file.name}:{lineno} 字段缺失: {sorted(missing)}')
                    if item.get('evidence_status') not in ALLOWED_CASE_STATUSES:
                        errors.append(f'{file.name}:{lineno} 不支持的证据状态')
                    if item.get('source_type') not in ALLOWED_SOURCE_TYPES:
                        errors.append(f'{file.name}:{lineno} 不支持的来源类型')
                    if not isinstance(item.get('tags'),list) or not isinstance(item.get('source_urls'),list):
                        errors.append(f'{file.name}:{lineno} tags/source_urls 必须是数组')
                    if item.get('evidence_status') == 'verified' and not item.get('source_urls'):
                        errors.append(f'{file.name}:{lineno} 已核实案例必须有来源')
                    if item.get('evidence_status') == 'fictional' and item.get('source_type') != 'illustrative':
                        errors.append(f'{file.name}:{lineno} 虚构示例必须是 illustrative')
    for ref in ['core.md','research.md','decision-template.md','knowledge-architecture.md','cases-schema.md','model-catalog.md']:
        if not (root/'references'/ref).is_file():
            errors.append(f'缺少 references/{ref}')
    return errors


if __name__ == '__main__':
    problems = validate()
    if problems:
        print('FAILED')
        for problem in problems:
            print(' -', problem)
        sys.exit(1)
    print('PASS: SKILL.md、核心参考资料及 JSONL 结构检查通过')
