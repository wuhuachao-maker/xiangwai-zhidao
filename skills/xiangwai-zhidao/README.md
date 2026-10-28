# 【老吴】象外之道 | Xiangwai Zhi Dao Agent Skill

一个以老吴原创《象外之道》为统一认知框架的 AI 决策 Skill：**定果 → 观局 → 寻根 → 定策**。

**状态：v0.1.2 技能基础包，已包含工作流、知识库标准、演示数据、检索辅助脚本及自动校验；尚未完成大规模真实人物/案例采集，也未发布成 ChatGPT 插件。**

## 设计原则
- **内核主导，万家为证**：对话结论采用象外之道；马斯克、毛泽东、巴菲特、芒格等外部思想只是案例和证据。
- **先决策后解释**：优先给一个行动判断，而不是输出名言合集。
- **以数寻岸**：有工具就检索、核对、筛选相似案例；没有联网工具不得宣称已经查过最新资料。
- **探岸只在必要时启动**：证据不足导致无法决定时，再搜集新信息或设计最小对照。
- **保护隐私与版权**：不得把用户未授权的真实案例放到公开 GitHub。

## 目录

```text
xiangwai-zhidao/
├── SKILL.md                 # 跨平台入口与执行指令
├── references/
│   ├── core.md              # 固定四大模块
│   ├── research.md          # 数据寻岸研究规范
│   ├── knowledge-architecture.md # 人物/案例库规划
│   ├── decision-template.md # 决策输出模板
│   ├── visual-response-template.md # 一图一表＋行动卡
│   ├── cases-schema.md      # 案例字段规范
│   └── model-catalog.md     # 候选规律模型
├── data/
│   ├── cases/demo.jsonl     # 虚构示例，仅作格式测试
│   └── models/seed.jsonl    # 候选关系模型，不是概率数据库
├── scripts/
│   ├── validate_skill.py    # 校验 Skill 和数据
│   └── match_cases.py       # 案例粗筛（非统计预测）
├── examples/video-decision.md
└── tests/test_skill.py
```

## 如何安装

### Codex（项目级）
将整个 `xiangwai-zhidao` 文件夹放在项目的 `.agents/skills/` 下，形成 `.agents/skills/xiangwai-zhidao/SKILL.md`。随后在支持的环境使用 `$xiangwai-zhidao` 或在任务中提出匹配的问题。

### Claude Code（项目级）
将整个文件夹放在 `.claude/skills/` 下，形成 `.claude/skills/xiangwai-zhidao/SKILL.md`。

### ChatGPT
当前文档格式符合通用 Agent Skills 基础结构。**Skill 与可安装的 ChatGPT 插件不是同一个分发包**：在支持 standalone skills 的客户端按产品说明安装；若面向 ChatGPT Chat/Work 发布，需要另行按照该平台当时的插件规范打包与配置。

GitHub 只是代码与知识库的版本仓库，**不会自动使 Skill 在所有客户端可用**，也不会自动运行数据更新。

## 本地运行与数据校验
```bash
python3 scripts/validate_skill.py
python3 -m unittest discover -s tests -v
python3 scripts/match_cases.py "企业 AI 视频 流量 低 没有客户"
```

检索脚本只在已有 JSONL 的候选案例中做关键词匹配。若数据全是虚构演示，仅会返回示范线索，不可引用为真实证据。新案例写入时，请遵守 `references/cases-schema.md`。

## GitHub 发布路线
1. 由项目所有者确定仓库名称、可见性（public/private）和授权许可。
2. 把本目录提交到仓库；先使用私有仓库更易控制研究材料和未完成稿。
3. 建立 `main` 稳定分支与内容审核流程；大规模案例采集进入独立分支。
4. 验证 Skill 在目标客户端能被识别、输出逻辑符合核心公理。
5. 单独制作 ChatGPT 插件分发包，并视需要配置搜索与连接器。

## 知识库规模规划
长期目标可设计为 1000+ 人物、15000+ 思想卡、30000+ 真实案例、3000+ 规律对照，但这是**规划，不是已收集的数据库**。不按名气替代可比性，不拿数量替代核验。

## 来源规范参考
- https://agentskills.io/specification
- https://learn.chatgpt.com/docs/build-skills
- https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview

## 权利说明
初版尚未添加对外授权许可文件。创建公开仓库前由项目所有者决定许可证、商标和版权方案；不应直接上传未经授权的书籍、课程和客户信息。
