# 知识库读取与证据分层

截至2026-10-28，库存以 `index.json` 为准。数据批次与Skill版本分开管理，本次内核、四大模块及SKILL.md不变。

| 目录 | 内容 | 默认使用 |
|---|---|---|
| cases/ | 具体事件、公开战略与政策记录；按一次决策或政策建卡 | 仅verified |
| thoughts/ | 有出处的自撰人物思想释义，非名言集 | 仅verified |
| comparisons/ | 跨案例候选关系，不能当成独立样本或已证实规律 | 仅显式包含待核资料时 |
| sources/ | 来源类型、正文定位、读取方式及限制 | 用于回查主张 |
| models/ | 原有6条候选规律种子 | 非经验验证结论 |

读取顺序：按问题查案例→核对来源与未知项→按目标、生态、资源、阶段、条件排除不可比资料→仅用“定果、观局、寻根、定策”形成判断。思想和跨案例卡只作补充。

`verified`表示本轮直接核读的来源足以支持卡片限定的事实或本人观点，不表示独立人工审核、双源交叉证实、未来有效或因果关系成立。`provisional`为待核线索；原站403而仅有索引文本的两项科学研究及对应思想卡保留此状态。

`source_type`为主证据类型，混合来源逐项见source_ids；官方历史摘要也可能是secondary。相同出版方的多个URL不算多个独立来源。多个记录使用同一信件不会增加独立样本数。

`claims`逐项区分事实、人物观点、研究者解释；`hidden_side`、`why_it_might_work`、`transfer_conditions`、`xiangwai`是候选迁移解释，不是原作者原话。`counterevidence`多数是边界与潜在反驳，不冒充已采集的经验反例。无反事实识别时不输出因果成功率。

`decision_date_precision`只允许year/month/day。仅知年份不补写1月1日；政策归属年与实际出台日分开。`as_of`是本批资料截至日，非决策发生日。

来源只存自撰摘要、定位与链接，不镜像原书或网页全文。不包含客户私密材料。来源可能改版、重定向或失效；已观察的访问限制写在access_note及质量报告中。

运行（在技能目录下）：

```bash
python3 scripts/validate_skill.py
python3 scripts/validate_knowledge.py
python3 -m unittest discover -s tests -v
python3 scripts/match_knowledge.py '产品创新 失败 客户需求'
python3 scripts/match_knowledge.py '青蒿' --include-provisional
```

关键词粗筛不代表语义或因果匹配，不具备向量检索、图数据库或自动联网更新功能。已安装插件不会自动获得本仓库新数据。
