# 项目文档地图

本目录是项目唯一长期文档目录，不另建 `memory-bank/`。当前事实优先覆盖更新，历史过程不追加到权威文档。

## 当前工作入口

- 项目规则：[`../AGENTS.md`](../AGENTS.md)
- 项目入口：[`../README.md`](../README.md)
- 产品简述：[`product-brief.md`](product-brief.md)
- 架构说明：[`architecture.md`](architecture.md)
- 测试策略：[`testing-strategy.md`](testing-strategy.md)
- 发布方案：[`release-plan.md`](release-plan.md)
- 项目路线：[`project-management/roadmap.md`](project-management/roadmap.md)
- 当前状态：[`project-management/current-task.md`](project-management/current-task.md)
- 当前计划：[`project-management/implementation-plan.md`](project-management/implementation-plan.md)
- 最近进度：[`project-management/progress.md`](project-management/progress.md)
- 验收证据：[`evidence.md`](evidence.md)

F-001 是唯一活动任务卡，Step 0 已完成执行基线。后续只能从 `implementation-plan.md` 中紧邻的已批准 Step 推进。

## 权威文档映射

| 文档 | 唯一职责 | 更新触发条件 | 保存历史 |
| --- | --- | --- | --- |
| `README.md` | 项目入口、当前能力与交付边界 | 运行或交付事实变化 | 否 |
| `docs/README.md` | 文档地图和权威关系 | 文档结构变化 | 否 |
| `product-brief.md` | 用户、目标、范围、非目标与成功标准 | 产品方向经用户确认后变化 | 否 |
| `architecture.md` | 当前候选架构、数据流和依赖边界 | 架构决策变化 | 否；决策历史以后进入 ADR |
| `testing-strategy.md` | 测试分层、失败路径和质量门禁 | 测试策略变化 | 否 |
| `release-plan.md` | 本地闭环、打包与外部发布边界 | 发布渠道或流程变化 | 否 |
| `roadmap.md` | 未批准/已批准候选任务、顺序和依赖 | 用户调整优先级 | 仅完成项短摘要 |
| `current-task.md` | 唯一生命周期状态和活动任务入口 | 任务选择或 Step 状态变化 | 否 |
| `implementation-plan.md` | F-001 当前 Step 计划 | Step 状态或验证方式变化 | 否 |
| `progress.md` | 当前 Step、最近结果、阻塞和下一动作 | Step 收口 | 仅最近摘要 |
| `evidence.md` | 可复现验证证据索引 | 门禁或验收完成 | 是，保留摘要 |

## 权威顺序

```text
当前代码、测试和 Git 事实
→ 用户已批准的范围与任务卡
→ architecture / testing-strategy / release-plan
→ roadmap / current-task
→ 聊天记录和历史材料
```

## 当前状态

- 活动任务：F-001 已批准，Step 0 已完成。
- roadmap：已批准，F-001 已选择。
- Git：本地 `main` 基线和 `feat/f-001-local-weather-tool`；无远程、未推送。
- 实现/测试/构建/发布：均未开始。
- 唯一下一步：等待用户允许进入 F-001 Step 1。
