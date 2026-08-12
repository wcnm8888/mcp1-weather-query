# R-002 实施计划

## 当前状态

- 活动任务：`R-002` Official MCP Registry 登记，L 级。
- 当前 Step：Step 10 已完成；Draft closure PR #12 等待用户审查并合并。
- 分支：`agent/r-002-step10-registry-closure`，起点为 PR #11 merge commit
  `900f71133ad9525ff65965d0822a1e92d06faead`；`origin/main` 仍为该提交。
- Step 0 离线基线：lock、Ruff format/lint、严格 mypy、`85 passed, 1 skipped` 和 diff 检查通过；
  唯一 skip 是显式 live contract。
- 外部事实：PyPI 0.1.0 已公开；Official MCP Registry 0.1.0 已登记，官方 API 与公开
  PyPI 安装/stdio 复验通过。

## Step 计划

| Step | 目标 | 状态 | 进入门禁 |
| --- | --- | --- | --- |
| 0 | 文档治理、R-001 QA 归档、任务基线、本地分支和离线门禁 | **完成** | 已获批准 |
| 1 | 建立先失败的 Registry 身份、安全与生命周期契约 | **完成：6 failed, 4 passed** | 已获批准 |
| 2 | 最小实现使 Step 1 红灯转绿 | **完成：10 passed** | 已获批准 |
| 3 | 固定 publisher/schema 核验和联网 `validate` | **完成** | 已获批准；退出码 0，无写入 |
| 4 | 独立 QA、元数据冻结、PyPI marker 复核与 UAT | **完成** | QA/UAT 均通过 |
| 5 | readiness Git/PR 交付 | **完成：Draft PR #11，CI 通过** | QA/UAT 通过；用户已授权；不登录/发布 |
| 6 | 合并后同步、Registry 空状态与 Terms/认证边界 | **完成** | 用户已合并 readiness PR |
| 7 | 官方 GitHub OAuth login | **完成** | 用户单独授权；完成后停止 |
| 8 | 单次 Registry publish | **完成** | 用户单独授权；仅一次且退出码 0 |
| 9 | 官方 API、PyPI 安装与 stdio 公开复验 | **完成** | 唯一 active 条目与公开安装复验通过 |
| 10 | 凭据处置、发布后文档/测试与 closure PR | **完成：Draft PR #12** | 用户已授权凭据处置和 Git 交付 |
| 11 | 合并后同步、归档并关闭 | 未开始 | 用户合并 closure PR |

## 当前门禁

- Step 10 已获授权；固定 `mcp-publisher v1.8.1 logout` 退出码 0，认证文件已由官方工具移除，
  发布后定向契约 `30 passed`、完整离线门禁 `96 passed, 1 skipped` 和项目外制品检查均通过；
  Draft closure PR #12 已创建；当前只剩用户审查/合并门禁。
- Step 8 仅一次 publish 已成功；不得再次发布同名同版本。Step 9 只执行官方 API 与公开 PyPI
  安装/stdio 只读复验，没有 Registry/PyPI 写入。
- 不手工删除未知认证文件，不重复 publish，不自行合并 closure PR，也不进入 Step 11。
- 任何需要修改业务代码、Tool 契约、传输、PyPI 版本、仓库可见性或工具版本的情况立即停止。
