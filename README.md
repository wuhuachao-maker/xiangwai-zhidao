# 【老吴】象外之道 · ChatGPT Plugin / Agent Skill

以《象外之道》四大认知模块为决策内核：定果、观局、寻根、定策。人物哲学、案例与公开资料均为辅助事实验证材料。

- 跨平台技能入口：`skills/xiangwai-zhidao/SKILL.md`
- 四大模块及研究规范：`skills/xiangwai-zhidao/references/`
- 图文决策统一回复模板：`skills/xiangwai-zhidao/references/visual-response-template.md`
- 数据示例：`skills/xiangwai-zhidao/data/`（仅演示，非真实案例库）
- 校验：从 `skills/xiangwai-zhidao/` 运行 `python3 scripts/validate_skill.py` 与 `python3 -m unittest discover -s tests -v`

本仓库包含插件描述文件 `plugin.json`，可作为插件源码使用。没有内建 MCP 服务，网络检索依赖安装环境提供的工具，不会自动获得或持续同步 GitHub 更新。

**版本**：v0.1.2，为功能性初版。预期的大型人物、思想卡、真实案例库尚未构建；不可将演示数据作为证据。

**版权**：未附加对外开源授权。公开可读不意味着获得复制、修改或商用许可。
