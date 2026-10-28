# 案例结构与证据字段

一条 JSONL 记录是一个 JSON 对象，不是以人物为基本单位，而是以**一次具体决策**为单位。

必填：
- `id` 唯一标识，稳定不变；`title` 案例名；`domain` 问题领域。
- `scenario` 当时生态与资源条件；`goal` 决策目标；`visible_side` 已有做法/已知面。
- `hidden_side` 候选对岸/隐藏条件；`action` 具体行动；`outcome` 实际结果。
- `tags` 关键词数组；`source_urls` 可检索的原始出处列表。
- `evidence_status`：`verified` / `provisional` / `fictional`。
- `source_type`：`primary` / `secondary` / `illustrative`。
- `as_of`：数据或资料时间（YYYY-MM-DD；演示可使用固定日期）。

建议补充：`constraints`、`alternatives`、`why_it_might_work`、`counterevidence`、`transfer_conditions`、`privacy_status`、`reviewer`。

约束：
- `fictional` 的案例必须显式标注“虚构演示”，且不能作为真实证据。
- 真实案例应尽量使用当时可获得的资料、不同结果的可比样本和独立来源。
- 使用了未获明确授权的客户真实信息，应**不入库**，不得通过简单改名规避隐私要求。
- 审核不充分的资料不得标 `verified`。
