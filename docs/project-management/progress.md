# Project Progress

## 当前状态

- F-001、F-002、D-001 与 R-001 均已完成并关闭；`R-002` 已批准并进入活动状态。
- 当前 Step：R-002 Step 5 Draft readiness PR #11 已创建，等待最终 CI。
- 本地分支：`release/r-002-mcp-registry-0.1.0`；首个交付提交为 `4d262c3`。
- 起始基线：`main == origin/main == 2fae2579517ebb5f7154f9646b54b4f174be6ffa`；
  `v0.1.0` 解引用到 `bb24624dcc8eb2efce5f4c49c80c850542c4d2b3`。
- `mcp-weather-query==0.1.0` 仍已公开并完成外部安装复验；Official MCP Registry 仍未登记。

## 最近完成：R-002 Step 4

- 已审查 11 个已跟踪差异和 2 个未跟踪文件；所有文件均属于 R-002，没有来源不明文件。
- 修复 README/docs 的两处旧测试计数和 current-task 的一处 validate 陈旧描述；未发现其他
  高、中优先级范围内缺陷。
- 冻结 `server.json` 原始 SHA-256 `e0ad8ae8...c6709`；规范化语义 SHA-256
  `7363235e...e39f0d` 已由静态契约固定，避免行尾/缩进差异造成假漂移。
- 生产 PyPI 官方 0.1.0 JSON 返回 HTTP 200；唯一 ownership marker、两个未 yank 制品、
  wheel/sdist SHA-256、Python 范围和 MIT metadata 均匹配既有发布证据。
- 官方 Terms 源文件返回 HTTP 200，有效日期仍为 2025-09-02；preview/data reset、CC0、公开
  metadata/GitHub 用户名和仅 Registry Data 适用的边界均存在。
- 完整离线 QA 为 `95 passed, 1 skipped`；Registry 定向契约 `10 passed`；lock、Ruff、严格
  mypy、diff、唯一 Tool、无 HTTP/SSE 和无 Registry CI 路径均通过。
- 用户明确回复 `R-002 Step 4 UAT 通过`，确认冻结身份、preview/CC0/公开 metadata、不可变
  版本恢复及 UAT 不授权外部写入。
- 未执行 login、publish、Terms 接受或 Registry 写入；未修改 manifest、源码、workflow、
  依赖、锁文件或系统环境。

## 当前交付：R-002 Step 5

- 精确提交并推送 13 个已审查的 readiness 文件，提交为 `4d262c3`。
- Draft PR #11：`https://github.com/wcnm8888/mcp1-weather-query/pull/11`，目标为 `main`。
- PR 创建时 GitHub Actions `release / Validate and build distributions` 已启动；等待最终结果。
- 本 Step 不执行 Terms、OAuth、login、publish、Registry 写入或 PR 合并。
