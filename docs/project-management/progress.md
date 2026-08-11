# Project Progress

## 当前状态

- F-001：已完成、合并、归档并关闭。
- F-002：已完成、合并、归档并关闭；PR #3 与收口 PR #4 均已合并。
- D-001：Step 6 独立 QA 与用户 UAT 已完成；Step 7 Git/PR 交付已获准。
- 当前分支：`chore/d-001-release-candidate`（Step 7 开始时尚未 push）。
- 基线：`main == origin/main == a3ef73c185084ae0a0e3374d78779f7618f0a16b`。
- 外部发布：未授权、未执行。

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

## 当前门禁

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

## 当前门禁

用户于 2026-08-11 提供 QA wheel 环境复验结果，并要求验收通过后进入 Step 7；截图显示 provenance、Legacy/现代协议、唯一 Tool、`structuredContent`、stdout/stderr 和退出码均通过。因此 Step 6 UAT 已通过，当前只执行 Step 7 Git/PR 交付；不得自动合并、登录或发布。
