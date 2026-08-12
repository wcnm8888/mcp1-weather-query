# R-002 实施计划

## 当前状态

- 活动任务：`R-002` Official MCP Registry 登记，L 级。
- 当前 Step：Step 5 Draft readiness PR #11 已创建，等待最终 CI。
- 分支：本地 `release/r-002-mcp-registry-0.1.0`，从同步后的
  `2fae2579517ebb5f7154f9646b54b4f174be6ffa` 创建；尚未提交或推送。
- Step 0 离线基线：lock、Ruff format/lint、严格 mypy、`85 passed, 1 skipped` 和 diff 检查通过；
  唯一 skip 是显式 live contract。
- 外部事实未改变：PyPI 0.1.0 已公开，Official MCP Registry 尚未登记。

## Step 计划

| Step | 目标 | 状态 | 进入门禁 |
| --- | --- | --- | --- |
| 0 | 文档治理、R-001 QA 归档、任务基线、本地分支和离线门禁 | **完成** | 已获批准 |
| 1 | 建立先失败的 Registry 身份、安全与生命周期契约 | **完成：6 failed, 4 passed** | 已获批准 |
| 2 | 最小实现使 Step 1 红灯转绿 | **完成：10 passed** | 已获批准 |
| 3 | 固定 publisher/schema 核验和联网 `validate` | **完成** | 已获批准；退出码 0，无写入 |
| 4 | 独立 QA、元数据冻结、PyPI marker 复核与 UAT | **完成** | QA/UAT 均通过 |
| 5 | readiness Git/PR 交付 | **进行中：Draft PR #11，CI 待完成** | QA/UAT 通过；用户已授权；不登录/发布 |
| 6 | 合并后同步、Registry 空状态与 Terms/认证边界 | 未开始 | 用户已合并 readiness PR |
| 7 | 官方 GitHub OAuth login | 未开始 | 用户单独授权；完成后停止 |
| 8 | 单次 Registry publish | 未开始 | 用户单独授权冻结元数据 |
| 9 | 官方 API、PyPI 安装与 stdio 公开复验 | 未开始 | publish 结果明确 |
| 10 | 凭据处置、发布后文档/测试与 closure PR | 未开始 | 用户授权凭据处置和 Git 交付 |
| 11 | 合并后同步、归档并关闭 | 未开始 | 用户合并 closure PR |

## 当前门禁

- Step 5 已获用户明确授权；只允许精确提交当前 readiness 变更、推送既定分支并创建 Draft PR。
- Step 5 只能交付当前冻结的 readiness 变更；CI 不得 Registry login/publish，PR 合并也不授权
  Terms、OAuth 或 Registry 写入。
- Step 7、8、9 必须分别授权并分别停止。
- 任何需要修改业务代码、Tool 契约、传输、PyPI 版本、仓库可见性或工具版本的情况立即停止。
