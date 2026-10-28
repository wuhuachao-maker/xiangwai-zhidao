# 【老吴】象外之道 · ChatGPT Plugin / Agent Skill

以《象外之道》固定认知体系为内核，唯一决策路径为：**定果 → 观局 → 寻根 → 定策**。人物思想、案例与公开资料只作辅助验证，不能替换内核。

- 技能入口：`skills/xiangwai-zhidao/SKILL.md`
- 核心定义、生态法则、探岸法及数据寻岸：`skills/xiangwai-zhidao/references/`
- 图文回复模板：`skills/xiangwai-zhidao/references/visual-response-template.md`
- [知识库读取及证据分层](skills/xiangwai-zhidao/data/README.md)
- [当前数量与文件校验值](skills/xiangwai-zhidao/data/index.json)
- [本批质量报告与旧8条审核](reports/2026-10-28-batch02-quality.md)

截至2026-10-28，知识库有**20条真实案例及政策记录（18条来源核读、2条待核）、8张思想卡（6张核读、2张待核）、4组候选对照、28条来源登记**。另有2条虚构演示与6条候选规律种子，均不计入真实证据。数量不可跨类别相加为独立样本。长期建设目标尚未完成。

`verified`只表示限定主张得到本轮直接核读来源支持，不等于独立人工审核或因果验证。默认检索排除待核与虚构记录。详细限制、偏差和下一批方向见质量报告。

校验：从 `skills/xiangwai-zhidao/` 运行：

```bash
python3 scripts/validate_skill.py
python3 scripts/validate_knowledge.py
python3 -m unittest discover -s tests -v
```

**Skill/插件框架版本**仍为v0.1.2；**数据批次**为2026-10-28-batch02。此次不改内核或插件配置。

本仓库包含插件描述文件，可作为插件源码。无内建MCP服务、采集服务器或GitHub与已安装插件的自动同步。网络检索依赖安装环境提供的工具。

**版权**：未附加对外开源授权。公开可读不意味着获得复制、修改或商用许可。
