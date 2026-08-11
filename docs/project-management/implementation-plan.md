# 实施计划门禁

## 当前状态

- 活动任务：无
- 最近完成任务：D-001 发布候选与发布前审查
- 状态：`no_active_task / awaiting_user_selection`
- 功能合并：PR #5，merge commit `2e691c351b78a0281a4a1fcdb21eca90c8e2f580`
- 当前收口分支：`docs/d-001-post-merge`

以下 Step 0–7 内容保留为最近完成计划的摘要；D-001 完整任务卡已归档到 `docs/archive/task-cards/D-001-发布候选与发布前审查.md`。

## Step 0 唯一目标

纠正 F-002/PR #4 的最终合并事实，持久化已批准 D-001 任务卡及阶段地图，建立可复核的本地 Git 和离线质量基线。不得提前实现发布材料、构建制品或访问发布平台。

## Step 0 检查表

- [x] 核验起点工作树干净、`main` 与 `origin/main` 一致。
- [x] 核验 PR #4 已合并，merge commit 为 `a3ef73c`。
- [x] 从同步后的 `main` 创建本地 `chore/d-001-release-candidate`。
- [x] 修正 F-002 归档和长期文档中的旧 PR #4 状态。
- [x] 将 D-001 持久化为唯一活动任务并同步 roadmap/progress。
- [x] 运行默认离线质量门禁和 Git 范围检查。
- [x] 记录真实证据并停在 Step 1 用户门禁。

## Step 1 唯一目标

在不实现发布材料、不构建制品、不创建 `server.json` 和不访问发布平台的前提下，把 D-001 已批准的发布候选边界固化为可执行契约，并证明失败只来自当前真实缺口。

## Step 1 结果

- [x] 新增 `tests/release/test_release_candidate_contract.py`。
- [x] 固定 distribution/import/console/version/License/Registry 名称，现有 identity 守卫通过。
- [x] 建立 6 个预期红灯：CHANGELOG、候选 wheel 安装说明、未来 PyPI 命令及未发布标签、Host stdio 配置、Registry ownership marker/未发布边界、可复现候选与安全 publisher 命令。
- [x] 定义 Step 3 Registry、Step 4 wheel/sdist、Step 5 双干净安装矩阵；本 Step 未执行这些动作。
- [x] 契约文件结果：`6 failed, 4 passed`；完整套件：`6 failed, 66 passed, 1 skipped`。
- [x] 排除故意红灯后，既有回归：`62 passed, 1 skipped`；lock、format、lint、mypy 和 diff 检查通过。
- [x] 未修改 README、release plan、`pyproject.toml`、源码、Tool 契约或运行时。
- [x] 停在 Step 2 用户门禁。

## Step 2 唯一目标

仅通过最小发布文档和包 README 元数据实现，使 Step 1 的 6 个预期红灯转绿，同时保持版本、入口、Tool、依赖、运行时和未发布状态不变。

## Step 2 结果

- [x] 新建根 `CHANGELOG.md`，记录 `0.1.0` 的真实能力、限制和 `Unreleased` 状态。
- [x] README 增加官方 Registry PyPI ownership marker、本地候选 wheel 安装、未来 PyPI `uvx` 命令、stdio Host JSON 和明确未发布边界。
- [x] release plan 增加 `uv build --no-sources`、项目外 E 盘候选目录、本地 `mcp-publisher validate` 以及禁止 `login`/`publish` 的阶段命令契约。
- [x] release contract 从 `6 failed, 4 passed` 转为 `10 passed`，未放宽或删除断言。
- [x] 完整离线门禁通过：`72 passed, 1 skipped`；唯一 skip 为显式 live contract。
- [x] lock、Ruff format/lint、严格 mypy 和 diff 检查通过。
- [x] 未修改 `pyproject.toml`、`uv.lock`、`src/`、Tool/transport/依赖或系统环境。
- [x] 未创建 `server.json`、构建制品或外部发布记录；停在 Step 3 用户门禁。

## Step 3 唯一目标

创建与已批准 Python 包/stdio 边界一致的根 `server.json` 草案，并使用项目外固定版本官方 publisher 完成 Schema/语义校验，不认证、不发布。

## Step 3 结果

- [x] 创建 605-byte 根 `server.json`，使用当前 `2025-12-11` Schema。
- [x] 固定名称 `io.github.wcnm8888/mcp1-weather-query`、版本 `0.1.0`、单一 PyPI package `mcp-weather-query`、`runtimeHint=uvx` 和 stdio。
- [x] 未配置 remote、environment variables、package/runtime arguments、HTTP/SSE 或秘密。
- [x] 新增 4 项静态 Registry contract；两组 release 测试合计 `14 passed`。
- [x] 从官方 v1.8.1 release 下载 Windows amd64 publisher 到项目外 E 盘，归档 SHA-256 与官方 digest 一致；未加入 PATH。
- [x] 官方 `mcp-publisher v1.8.1 validate` 返回 `✅ server.json is valid`、exit code 0。
- [x] 核验源码确认 validate 使用未认证 POST `/v0/validate`，不是纯离线；未调用 login/publish 或创建条目。
- [x] 完整离线门禁为 `76 passed, 1 skipped`；lock、Ruff、mypy 和 diff 检查通过。
- [x] 未构建 wheel/sdist、未修改源码/依赖/Tool/transport；停在 Step 4 用户门禁。

## Step 4 唯一目标

使用锁定的现有项目环境在项目外离线构建唯一 wheel/sdist 候选，并完成文件、元数据、完整性、来源一致性和敏感信息审查；不安装或运行制品。

## Step 4 结果

- [x] 使用 `uv build --no-sources --offline`，没有包索引访问或 source override。
- [x] 项目外候选目录：`E:\mcp-weather-query-release-candidate\0.1.0\step4-20260811T205328\dist`。
- [x] uv 先构建 sdist，再从 sdist 构建 pure-Python `py3-none-any` wheel。
- [x] wheel：16,376 bytes，15 个文件，SHA-256 `3e526b64...6da438a`。
- [x] sdist：11,946 bytes，14 个文件，SHA-256 `eff5f30a...090f4f`。
- [x] 候选目录除两个制品外只有 uv 自动生成的 1-byte `*` 型 `.gitignore`。
- [x] Core Metadata 2.4、名称/版本、Python 范围、依赖、MIT、LICENSE/NOTICE、console entry point 和 wheel RECORD 通过。
- [x] 源码/法律文本与当前工作树一致；嵌入 README 与根 README 一致并含 Registry marker、attribution 和明确未发布状态。
- [x] 精确文件白名单和全 payload 扫描未发现测试、缓存、日志、凭据、本机路径或无关配置。
- [x] 增强既有制品检查器，增加外层目录白名单和 D-001 README 发布边界；未放宽 F-002 完整性检查。
- [x] 完整离线门禁：`76 passed, 1 skipped`；lock、Ruff、严格 mypy 和 diff 检查通过。
- [x] 未安装、导入或运行候选；未执行 live、Inspector、publisher 或外部发布；停在 Step 5 用户门禁。

## Step 5 唯一目标

从 Step 4 固定 wheel/sdist 分别安装到两个新的项目外干净环境，证明安装来源、无源码目录/`PYTHONPATH` 依赖、生产 console stdio、现代协议发现、唯一 Tool、确定性结构化调用、stdout/stderr 和有限时间退出行为。

## Step 5 结果

- [x] 在 `E:\mcp-weather-query-release-candidate\0.1.0\step5-20260811T210410` 新建独立 `wheel-env` 与 `sdist-env`，均使用 Python 3.12.10。
- [x] 在 `UV_OFFLINE=1` 且清空 `PYTHONPATH`、`PYTHONHOME`、`VIRTUAL_ENV`、live 开关后，分别安装 Step 4 固定 wheel 和 sdist；两套环境均安装 `mcp-weather-query==0.1.0` 及共 34 个包。
- [x] `direct_url.json`、模块路径和 console 路径分别指向对应本地制品、环境 `site-packages` 与 `Scripts`；不是 editable 或源码目录安装。
- [x] 两个生产 console 均完成 Legacy 2025-11-25 initialize/tools-list，且仅发现 `get_current_weather`；stdout 只有 JSON-RPC，stderr 无 traceback，关闭 stdin 后退出码 0。
- [x] 官方 SDK v2 Client 对两套生产 console 均通过 MCP 2026-07-28 modern discovery；确定性测试专用子进程在同一现代协议下返回合法 `structuredContent`，诊断仅在 stderr。
- [x] 10 秒单步超时和 finally 清理生效；复验后没有来自 Step 5 环境的 Python/uv/Node 残留进程。
- [x] 固定制品复审保持原文件数、大小和 SHA-256；没有重建或替换制品。
- [x] 初次离线门禁发现复验脚本混合换行，仅格式化该测试脚本后全部通过：`76 passed, 1 skipped`；lock、Ruff、严格 mypy 和 diff 检查通过。
- [x] 未访问 live API，未运行 Inspector/publisher，未修改源码、依赖、锁文件或系统环境，未登录、发布、提交或 push；停在 Step 6 用户门禁。

## Step 6 唯一目标

独立审查 D-001 全部已跟踪和未跟踪变更，修复发布候选范围内的真实缺陷，重新验证最终 README 对应的候选制品、双安装和 stdio，并把可复核候选交给用户 UAT；用户确认前不进入 Git/PR。

## Step 6 QA 结果

- [x] 审查 14 个已跟踪变更和 4 个未跟踪文件；没有 `src/`、`pyproject.toml`、`uv.lock`、LICENSE 或 NOTICE 变更。
- [x] 修复根 README 中“后续生成候选”“拟交付能力”和旧测试计数，以及测试策略/架构/发布方案中的陈旧阶段文字。
- [x] 旧 Step 4 制品被当前 README 一致性门禁按预期拒绝；未删除、覆盖或冒充为 QA 候选。
- [x] 在 `E:\mcp-weather-query-release-candidate\0.1.0\step6-qa-20260811T213511` 离线重建唯一 QA wheel/sdist 并完成严格制品审查。
- [x] QA wheel 为 16,340 bytes、15 个文件、SHA-256 `c93ab545...01b661b6`；sdist 为 11,904 bytes、14 个文件、SHA-256 `f9d68065...1b4d18f2`。
- [x] 新建 wheel/sdist 两个 Python 3.12.10 环境离线安装；provenance、无源码路径、生产 stdio、现代 discovery、唯一 Tool、确定性 `structuredContent`、stdout/stderr 和退出均通过。
- [x] 完整默认门禁：`76 passed, 1 skipped`；lock、Ruff、严格 mypy、制品复审和 diff 检查通过；没有 Step 6 遗留运行时进程。
- [x] 未访问 live API，未运行 Inspector/publisher，未更新依赖或系统环境，未登录、发布、commit、push 或创建 PR。
- [x] 用户 UAT 已确认通过：QA wheel 环境的 provenance、Legacy/现代协议、唯一 Tool、`structuredContent`、stdout/stderr 和退出码均符合验收。

## Step 7 唯一目标

把全部 D-001 范围内变更精确提交并推送到 `chore/d-001-release-candidate`，创建以 `main` 为目标的 Draft PR，然后停在用户审查/合并门禁；不执行任何外部发布或自动合并。

## Step 7 检查表

- [x] 用户 UAT 通过并明确允许进入 Step 7。
- [x] 刷新并确认 `main == origin/main == a3ef73c185084ae0a0e3374d78779f7618f0a16b`。
- [x] 重新运行提交前离线门禁并精确审查暂存范围。
- [x] 创建提交 `f44e8b6a4df63016a639df4b7e2d5337c6fbf28d` 并推送 `chore/d-001-release-candidate`。
- [x] 创建以 `main` 为目标的 Draft PR #5：`https://github.com/wcnm8888/mcp1-weather-query/pull/5`。
- [x] 停在用户 PR 审查/合并门禁。

## Step 8 合并后收口

- [x] 核验 PR #5 已合并，merge commit 为 `2e691c351b78a0281a4a1fcdb21eca90c8e2f580`。
- [x] 本地 `main` 以 fast-forward 同步到 `origin/main`。
- [x] 合并后完整离线门禁通过：`76 passed, 1 skipped`。
- [x] D-001 完整任务卡归档，活动任务重置为无。
- [x] roadmap、progress、文档地图、架构和证据同步到最终状态。
- [ ] 收口文档通过独立 PR 合入 `main`；该 PR 由用户审查并合并。

## 下一门禁

等待用户选择是否起草 R-001 候选任务卡。不得自动进入 R-001/R-002。

## 当前验证

```powershell
$env:MCP_WEATHER_RUN_LIVE = $null
uv lock --check
uv run ruff format --check .
uv run ruff check .
uv run mypy
uv run pytest -q --tb=short
uv run pytest -q --tb=short --ignore=tests/release/test_release_candidate_contract.py
git diff --check
git status --short
git diff --name-status
git ls-files --others --exclude-standard
```

## 停止条件

发现合并事实不一致、来源不明变更、敏感信息、需要修改源码/依赖/系统环境、publisher login/publish、Registry/PyPI 写入、tag/Release 或需要自动进入后续任务时立即停止并报告。
