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
- 已归档任务卡：[`archive/task-cards/`](archive/task-cards/)

F-001 与 F-002 的完整任务卡均已归档并关闭，PR #3 与收口 PR #4 均已合并。D-001 Step 6 独立 QA 与用户 UAT 均已完成，Step 7 Git/PR 交付已获准。

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
| `implementation-plan.md` | 当前活动任务的 Step 计划；无活动任务时记录门禁 | Step 状态或验证方式变化 | 否 |
| `progress.md` | 当前 Step、最近结果、阻塞和下一动作 | Step 收口 | 仅最近摘要 |
| `evidence.md` | 可复现验证证据索引 | 门禁或验收完成 | 是，保留摘要 |
| `archive/task-cards/` | 已关闭任务卡原文 | 任务完成并获准归档 | 是 |

## 权威顺序

```text
当前代码、测试和 Git 事实
→ 用户已批准的范围与任务卡
→ architecture / testing-strategy / release-plan
→ roadmap / current-task
→ 聊天记录和历史材料
```

## 当前状态

- 活动任务：D-001 发布候选与发布前审查；Step 6 独立 QA 与用户 UAT 已完成，当前进入 Step 7 Git/PR 交付。
- roadmap：已批准；F-001、F-002 已关闭，D-001 已由用户选择并按 Step 门禁推进。
- Git：private `origin` 为 `wcnm8888/mcp1-weather-query`；PR #3、PR #4 均已合并；D-001 基线为 `a3ef73c`，当前本地分支为 `chore/d-001-release-candidate`。
- 实现/测试：唯一 `get_current_weather` MCP Tool、可安装包、固定候选 wheel/sdist 和双干净安装闭环均已完成；当前默认门禁为 `76 passed, 1 skipped`，唯一 skip 是显式 live contract。
- 构建/发布：独立 QA 修复发布文档陈旧状态后生成新的 QA wheel/sdist，并分别完成项目外离线安装和 installed-package stdio 复验；未上传或发布。
- 唯一下一步：完成已获准的 D-001 Step 7 Git/PR 交付并停在用户 PR 审查门禁；不得自动合并、登录或发布。
