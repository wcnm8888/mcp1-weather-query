# Project Progress

## 当前状态

- F-001：已完成、合并、归档并关闭。
- F-002：已完成、合并、归档并关闭；PR #3 与收口 PR #4 均已合并。
- D-001：已完成、合并、归档并关闭；PR #5 已合并。
- R-001：任务卡已批准，Step 5 Git/PR 交付已获授权并进行中。
- 当前分支：`release/r-001-pypi-0.1.0`（仅本地，尚未提交或推送）。
- 起点基线：`main == origin/main == 0d5d7be9271b71143cdbcdf768bfbde5ed4393d0`。
- 外部发布：未授权、未执行。

## R-001 Step 0 结果

- 复核起点工作树干净、`main` 与 `origin/main` 一致，并创建本地发布分支。
- 持久化 R-001 L 级任务卡、Step 地图和独立 QA 清单。
- 默认离线门禁通过：`uv lock --check`、Ruff format/lint、严格 mypy、
  `76 passed, 1 skipped`、`git diff --check`；唯一 skip 为显式 live contract。
- 没有创建 `.github/workflows/`、修改包配置、构建制品或访问 Open-Meteo live API。
- 没有登录 PyPI、配置 Pending Publisher、创建/推送 tag、commit、push 或上传制品。

## R-001 Step 1 结果

- 新增 9 项 R-001 静态离线契约：2 项绿色身份/未发布守卫，7 项预期红灯。
- 五项 workflow 红灯均因 `.github/workflows/release.yml` 尚不存在；另外两项分别对应
  release plan 未记录批准的 Publisher tuple/恢复契约，以及 README 未公开非商业和限额。
- 契约文件：`7 failed, 2 passed`；完整套件：`7 failed, 78 passed, 1 skipped`。
- 排除故意红灯后既有回归：`76 passed, 1 skipped`；lock、Ruff、严格 mypy 和 diff 通过。
- 未创建 workflow/tag，未修改发布元数据或业务代码，未构建、登录、配置或上传。

## R-001 当前门禁

R-001 Step 4 的独立 QA、新 live contract 和用户 UAT 已完成。用户已允许 Step 5 的精确
commit、push、Draft PR 和 PR 检查；仍不授权发布 job、PyPI 登录/配置/上传或 tag。

## R-001 Step 2 结果

- 新增安全 `release.yml`，固定精确 tag、build/publish 隔离、最小 OIDC、`pypi`
  environment、artifact 传递和六个完整 action SHA。
- CI uv 固定为 0.6.14；setup-uv action 使用当前不可变 v9.0.0 commit，未改变本机 uv。
- README 和 release plan 补齐公开数据源限制、Publisher tuple、双授权与 yank 边界；
  CHANGELOG 继续诚实保持 `Unreleased`。
- R-001 契约由 `7 failed, 2 passed` 转为 `9 passed`；完整门禁为
  `85 passed, 1 skipped`，唯一 skip 为显式 live contract。
- 未实际构建、触发 CI、访问 live API、登录/配置/上传、创建 tag 或执行 Git 交付。

## R-001 Step 3 结果

- 在新的项目外目录以 `--no-sources --offline` 构建并审查 wheel/sdist；哈希分别为
  `e95429d4...d225b6e` 与 `e824aa4c...15b63`。
- 两个新的 Python 3.12.10 环境离线安装各自制品；provenance、无源码路径、生产 stdio、
  现代 discovery、唯一 Tool、确定性 `structuredContent`、stdout/stderr 和退出全部通过。
- 两套 production-modern stderr 为 0 bytes，测试诊断各自只写 stderr；无遗留运行时进程。
- 制品复审哈希不变；默认门禁保持 `85 passed, 1 skipped`，唯一 skip 为 live contract。
- 未访问 live、触发 Actions、登录/配置/上传、创建 tag 或执行 Git 交付。

## R-001 Step 4 QA/live 结果

- 独立审查所有已跟踪和未跟踪变更，确认业务源码、包元数据、锁文件、Registry 草案和
  CHANGELOG 均未改变；仍只有一个只读 `get_current_weather` Tool。
- 修复 CI 构建后未在上传前执行制品检查的供应链缺口，并用发布契约固定
  build -> artifact inspection -> upload 的顺序；定向契约 `9 passed`。
- 固定 wheel/sdist 哈希不变，两套 installed-package stdio 复验再次通过。
- 新的显式 Open-Meteo live contract 为 `1 passed in 2.73s`。
- 完整离线门禁为 `85 passed, 1 skipped`；唯一 skip 是默认关闭的 live contract。
- 用户 UAT 已确认通过：固定 wheel 的来源、唯一 Tool、现代/Legacy 协议、
  `structuredContent`、stdout/stderr 和退出码均符合验收。
- 未触发 Actions、登录/配置/上传 PyPI、创建 tag、commit、push 或 PR；等待 Step 5 授权。

## D-001 历史摘要

## Step 0 进展

- 已确认起点工作树干净，本地/远程 `main` 无分叉。
- 已确认 PR #4 于 2026-08-11 合并，merge commit 为 `a3ef73c`。
- 已从该基线创建 D-001 本地功能分支。
- 已修正 F-002 历史状态，并建立 D-001 唯一活动任务、实施计划和 roadmap 基线。
- 默认离线门禁通过：38 个文件格式检查通过，Ruff lint 通过，严格 mypy 24 个源文件通过，pytest `62 passed, 1 skipped`；唯一 skip 为显式 live contract。
- 未创建 `CHANGELOG.md`、`server.json` 或构建制品；未安装 publisher，未访问发布平台。

## Step 1 结果

- 新增一个 release contract 测试文件，共 10 项：6 项准确暴露 Step 2 文档缺口，4 项固定现有 identity 和后续 Step 3–5 验证矩阵。
- 契约文件：`6 failed, 4 passed`；完整默认套件：`6 failed, 66 passed, 1 skipped`。
- 排除故意红灯后，既有套件仍为 `62 passed, 1 skipped`，唯一 skip 为显式 live contract。
- lock、Ruff format/lint、严格 mypy、diff 检查通过。
- 未创建 `CHANGELOG.md`、`server.json` 或制品；未修改 README、release plan、包配置、源码或运行时。

## Step 2 结果

- 新建 `CHANGELOG.md`；README 增加本地/未来 PyPI 使用说明、stdio Host 配置、Registry ownership marker 和明确未发布状态。
- release plan 增加项目外候选构建与本地 Registry 校验命令边界，并明确禁止 login/publish。
- release contract 已从 6 个红灯转为 `10 passed`；完整默认测试为 `72 passed, 1 skipped`。
- lock、Ruff format/lint、严格 mypy 和 diff 检查通过。
- 未修改包版本、`pyproject.toml`、依赖、源码、Tool 或 transport；未创建 `server.json`、构建制品或执行发布。

## Step 3 结果

- 新建根 `server.json` 和 4 项静态 Registry contract；唯一包为固定版本 PyPI distribution，唯一 transport 为 stdio。
- 固定版 `mcp-publisher v1.8.1` 位于项目外 E 盘，官方归档 SHA-256 核验通过，未加入 PATH。
- 官方 validate 返回 `server.json is valid`；该命令调用未认证 `/v0/validate`，不是纯离线，但没有认证、发布或持久化条目。
- 完整默认测试为 `76 passed, 1 skipped`；lock、Ruff、严格 mypy 和 diff 检查通过。
- 未构建制品、未修改源码/依赖/Tool/transport，未执行 login/publish。

## Step 4 结果

- 在项目外 E 盘以 `uv build --no-sources --offline` 生成唯一 wheel/sdist；未访问包索引。
- wheel：16,376 bytes，SHA-256 `3e526b64...6da438a`；sdist：11,946 bytes，SHA-256 `eff5f30a...090f4f`。
- 文件白名单、Metadata 2.4、entry point、RECORD、源码/法律文件、嵌入 README、Registry marker、未发布状态和敏感信息扫描通过。
- 完整默认测试为 `76 passed, 1 skipped`；lock、Ruff、严格 mypy 和 diff 检查通过。
- 未安装或运行候选，未执行 live、Inspector、publisher、登录或发布。

## D-001 Step 8 历史门禁

## Step 5 结果

- 在项目外新建独立 `wheel-env` 与 `sdist-env`，以 `UV_OFFLINE=1` 分别安装 Step 4 固定 wheel/sdist；安装来源与对应制品一一匹配，不使用 editable、源码目录或 `PYTHONPATH`。
- 两个环境均从各自 `site-packages` 导入、从各自 `Scripts\mcp-weather-query.exe` 启动；生产 Legacy 握手/发现、现代 MCP 2026-07-28 discovery 和确定性结构化调用均通过，且只发现 `get_current_weather`。
- 两个生产进程 stdout 仅含协议消息、stderr 无 traceback、退出码 0；测试诊断仅进入 stderr，检查后无 Step 5 运行时残留进程。
- 固定制品哈希未变化；完整默认门禁为 `76 passed, 1 skipped`，lock、Ruff、严格 mypy 和 diff 检查通过。
- 未访问 live API，未运行 Inspector/publisher，未重建、登录、发布、提交、push 或创建 PR。

## Step 6 独立 QA 结果

- 完整审查 14 个已跟踪变更和 4 个未跟踪文件；没有生产源码、包配置、锁文件或法律文件变更。
- 修复 README、测试策略、架构、发布方案和 release contract 说明中的陈旧阶段状态；旧 Step 4 制品因此被 README 一致性门禁拒绝。
- 在新的项目外 Step 6 QA 目录离线重建并审查 wheel/sdist；两者又分别完成独立安装和 installed-package stdio 复验。
- QA wheel/sdist 的安装 provenance、Legacy/现代协议、唯一 Tool、结构化输出、stdout/stderr、退出和无残留进程均通过。
- 最终完整门禁为 `76 passed, 1 skipped`；lock、Ruff、严格 mypy、制品复审和 diff 检查通过。
- 未访问 live API，未运行 Inspector/publisher，未登录、发布、提交、push 或创建 PR。

## D-001 Step 8 历史门禁

当时 PR #5 已由用户合并，本地 `main` 已同步，合并后完整离线门禁通过；随后通过
PR #6 完成 D-001 收口。这是历史状态，不覆盖本文顶部的 R-001 当前门禁。

## Step 8 合并后收口

- PR #5 状态：`MERGED`；合并时间 `2026-08-11T15:46:20Z`；merge commit `2e691c351b78a0281a4a1fcdb21eca90c8e2f580`。
- 本地 `main` 通过 fast-forward 与 `origin/main` 对齐，工作树在创建收口分支前干净。
- 合并后门禁：lock、Ruff format/lint、严格 mypy、`76 passed, 1 skipped` 和 diff 检查均通过。
- D-001 完整任务卡已归档到 `docs/archive/task-cards/D-001-发布候选与发布前审查.md`。
- 收口文档已通过 Draft PR #6 交付，来源分支为 `docs/d-001-post-merge`，目标为 `main`。
- 未访问 live API，未运行 Inspector/publisher，未上传、登记、创建 tag 或 Release。
