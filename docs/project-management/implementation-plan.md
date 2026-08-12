# 实施计划门禁

## 当前状态

- 活动任务：R-001 PyPI 首次外部发布
- 等级：L
- 状态：`step_7_metadata_remediation / awaiting_pr_merge`
- 当前基线：`main == origin/main == fb986bdda4fdba41327165f2f569fdd8c7d9d6a7`
- 本地分支：`agent/r-001-step7-release-metadata`
- 外部发布：Step 7 已授权；tag/上传尚未执行

## R-001 Step 地图

- [x] Step 0：持久化任务卡、L 级治理基线、创建本地发布分支、运行离线基线。
- [x] Step 1：建立先失败的发布/workflow 安全契约。
- [x] Step 2：实现最终发布元数据和安全 CI workflow。
- [x] Step 3：本地重建、制品审查和双干净安装。
- [x] Step 4：独立 QA、新 live contract 和用户 UAT。
- [x] Step 5：Git/PR 交付；PR CI 只能检查，不能发布。
- [x] Step 6：合并后同步、公开名称复核和 Pending Publisher 配置；单独授权并完成。
- [ ] Step 7：最终发布门禁与精确 `v0.1.0` tag；再次明确授权。
- [ ] Step 8：公开 PyPI 文件、attestation、安装和 stdio 验证。
- [ ] Step 9：发布后文档、Git 收口；停止在 R-002 前。

## R-001 Step 0 结果

- [x] 确认工作树干净，本地 `main` 与 `origin/main` 一致。
- [x] 从已同步基线创建仅本地 `release/r-001-pypi-0.1.0`。
- [x] 持久化已批准 R-001 任务卡和 L 级 QA 清单。
- [x] 同步 roadmap、progress、文档地图、项目规则和 evidence。
- [x] 默认离线门禁通过：46 packages、43 个文件格式、Ruff、严格 mypy、
  `76 passed, 1 skipped`；唯一 skip 为显式 live contract。
- [x] 未创建 workflow、未改发布元数据、未构建制品、未访问 live API。
- [x] 未登录 PyPI、未配置 Pending Publisher、未创建 tag、未提交、推送或上传。

## R-001 Step 1 结果

- [x] 核验 PyPI/PyPA/GitHub 官方 Trusted Publishing、OIDC、environment 和 attestation 边界。
- [x] 新增 `tests/release/test_pypi_publish_contract.py`，只静态读取本地文件，不联网、不构建、不发布。
- [x] 两个绿色守卫固定 package/import/console/version 身份，并保持 `0.1.0` 诚实标记为 `Unreleased`。
- [x] 七个预期红灯准确暴露：缺少 `release.yml` 的五类安全契约、发布方案未记录已批准
  Publisher tuple/恢复边界、README 未公开 Open-Meteo 非商业和三档限额。
- [x] 定向契约为 `7 failed, 2 passed`；完整套件为 `7 failed, 78 passed, 1 skipped`。
- [x] 排除故意红灯后既有回归为 `76 passed, 1 skipped`，唯一 skip 为显式 live contract。
- [x] lock、Ruff format/lint、严格 mypy 和 diff 检查通过；仍恰好一个 Tool。
- [x] 未创建 `.github/`、workflow 或 tag，未修改 README/release plan/CHANGELOG/pyproject/源码。
- [x] 未访问 Open-Meteo live API，未登录/配置/上传 PyPI，未提交、推送或创建 PR。

## R-001 Step 2 结果

- [x] 新增专用 `.github/workflows/release.yml`，PR 执行 build，publish 只响应精确
  `v0.1.0` tag，并同时使用事件/ref 双重 guard。
- [x] workflow 顶层仅 `contents: read`；只有 publish job 额外拥有 `id-token: write`，
  且绑定 `pypi` environment。
- [x] build job 固定 Python 版本文件和 uv 0.6.14，运行 lock、Ruff、mypy、默认离线
  pytest、`uv build --no-sources`，再上传唯一 distribution artifact。
- [x] publish job 不构建、不测试、不读取 secrets，只下载 build artifact 并调用官方 PyPA
  action；未配置 TestPyPI、password、token、`skip-existing` 或关闭 attestations。
- [x] 六个外部 action 全部固定完整 SHA；复核后把 setup-uv 从旧 v7 pin 更正为当前官方
  不可变 v9.0.0 commit，同时 CI 安装的 uv 版本仍固定为 0.6.14。
- [x] README 补充 Open-Meteo 非商业免费层、600/分钟、5,000/小时、10,000/日、无 SLA
  和 CC BY 边界；release plan 固化 Publisher tuple、双授权与 yank 策略。
- [x] Step 1 契约从 `7 failed, 2 passed` 转为 `9 passed`，未删除或放宽断言。
- [x] 完整离线门禁为 `85 passed, 1 skipped`；lock、Ruff、严格 mypy 和 diff 通过。
- [x] 未构建本地最终制品、未访问 live API、未触发 Actions、未登录/配置/上传 PyPI，
  未创建 tag、commit、push 或 PR。

## R-001 Step 3 结果

- [x] 在项目外新建唯一候选根
  `E:\mcp-weather-query-release-candidate\0.1.0\r001-step3-20260812T003655`，未覆盖历史目录。
- [x] 使用现有 uv 0.6.14、项目内 Python 3.12.10 和
  `uv build --no-sources --offline` 从当前工作树构建 wheel/sdist。
- [x] wheel：15 files、16,523 bytes、SHA-256 `e95429d4...d225b6e`；sdist：14 files、
  12,107 bytes、SHA-256 `e824aa4c...15b63`；均为 Core Metadata 2.4。
- [x] 两个制品通过精确文件白名单、Metadata/entry point/RECORD、源码、当前 README、
  LICENSE/NOTICE、发布边界和敏感信息检查；安装后复审哈希不变。
- [x] 新建独立 `wheel-env`/`sdist-env`，在清空 `PYTHONPATH`、`PYTHONHOME`、
  `VIRTUAL_ENV` 且 `UV_OFFLINE=1` 下分别安装对应制品，各安装 34 packages。
- [x] provenance 精确匹配对应 artifact，模块来自各环境 `Lib\site-packages`，console 来自
  各环境 `Scripts\mcp-weather-query.exe`，不是 editable 或源码目录安装。
- [x] 两套生产 console 均完成 Legacy 2025-11-25 握手/唯一 Tool/退出码 0；官方 SDK v2
  均以 MCP 2026-07-28 完成 modern discovery，确定性调用返回合法 `structuredContent`。
- [x] stdout 仅协议消息；production-modern stderr 均为 0 bytes，测试诊断仅进入 stderr；
  完成后无候选目录关联的运行时残留进程。
- [x] 完整门禁：`85 passed, 1 skipped`；lock、Ruff、严格 mypy、制品复审和 diff 通过。
- [x] 未访问 live API、未触发 Actions、未登录/配置/上传 PyPI，未创建 tag、commit、push 或 PR。

## R-001 Step 4 QA/live 结果

- [x] 独立审查全部 10 个已跟踪变更和 3 个未跟踪文件；没有 `src/`、`pyproject.toml`、
  `uv.lock`、`server.json`、`CHANGELOG.md`、LICENSE 或 NOTICE 变更。
- [x] 发现并最小修复一个中优先级供应链缺口：build job 原先构建后直接上传，现改为上传前
  运行 `git diff --check` 和 `tests/packaging/inspect_artifacts.py dist`，发布契约同时校验执行顺序。
- [x] Step 3 固定 wheel/sdist 复审通过，文件数、大小和 SHA-256 不变；两套项目外安装的
  provenance、Legacy/现代协议、唯一 Tool、`structuredContent`、stdout/stderr 和退出再次通过。
- [x] 2026-08-12 显式运行新的 Open-Meteo live contract：`1 passed in 2.73s`；只访问固定
  官方端点，没有保存完整响应或位置数据。
- [x] 发布契约定向结果为 `9 passed`；完整离线门禁为 `85 passed, 1 skipped`，唯一 skip
  为默认关闭的 live contract；lock、Ruff、严格 mypy、diff 和范围扫描通过。
- [x] 用户在固定 wheel 环境完成 UAT 并明确确认通过；截图中的 provenance、唯一 Tool、
  `structuredContent`、stdout/stderr 和退出码均符合验收。
- [x] 未触发 Actions、未登录/配置/上传 PyPI，未创建 tag、commit、push 或 PR。

## R-001 Step 5 结果

- [x] 精确提交并推送 13 个 R-001 文件，创建以 `main` 为目标的 Draft PR #7。
- [x] 首次 PR run 发现 artifact actions 的 Node.js 20 弃用告警；以官方最新不可变 SHA
  更新 upload v7.0.1 和 download v8.0.1，二者均使用 Node.js 24。
- [x] 最新功能提交 `b5b1ff3430bd6ea15be735ec0e925e664bceb9d3` 的 run
  `31516139712` 成功：build/QA、wheel/sdist、制品检查和 artifact 上传全部通过。
- [x] `Publish distributions to production PyPI` 明确 skipped，annotations 为空；没有 tag、
  OIDC 发布、PyPI 登录、Publisher 配置或制品上传到 PyPI。
- [x] Draft PR #7 保持 Draft、merge state clean，等待用户审查/合并。

## Step 7 发布元数据修复

- [x] 用户明确授权进入 Step 7，并确认 PyPI 邮箱已验证。
- [x] PR #8 已合并，本地 `main == origin/main == fb986bd`；本地/远程均无 `v0.1.0`。
- [x] 公开 PyPI JSON 查询仍为 404；Pending Publisher tuple 与 `pypi` environment 已就绪。
- [x] 最终门禁发现 README、CHANGELOG 和契约仍固化“尚未发布 / Unreleased”，会使首发
  PyPI 页面立即陈旧，因此在 tag 前停止。
- [x] 用户授权独立修复 PR；README 改为由 PyPI 官方项目页核验公开状态，CHANGELOG 日期
  固定为 `2026-08-12`，相关制品/发布契约同步更新，Registry 仍明确未登记。
- [x] 项目外重建候选到
  `E:\mcp-weather-query-release-candidate\0.1.0\r001-step7-metadata-20260812T132608`；
  wheel 为 15 files / 16,485 bytes / SHA-256 `48909c4c...3e4387`，sdist 为
  14 files / 12,066 bytes / SHA-256 `ea8fa9cb...77b0c`，静态制品审查通过。
- [x] 完整离线门禁通过：lock、Ruff format/lint、严格 mypy、`85 passed, 1 skipped`、
  diff、唯一 Tool、无 HTTP/SSE、制品复审；唯一 skip 为显式 live contract。
- [x] 创建 Draft PR #9；run `31566777632` 的 build/QA 成功，生产 PyPI publish job 明确
  skipped，没有 OIDC 上传或公开制品。

## 当前门禁

等待用户审查并合并 Draft PR #9。合并前不得创建或推送 `v0.1.0`；合并后
必须同步 `main`、复核包名/Pending Publisher/tag 唯一性并重跑最终门禁，才能执行已授权 tag。

## 历史计划

以下内容是最近完成的 D-001 摘要；D-001 完整任务卡已归档到
`docs/archive/task-cards/D-001-发布候选与发布前审查.md`，不属于当前执行授权。

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
- [x] 收口文档已通过独立 Draft PR #6 交付；该 PR 仍由用户审查并合并。

## 下一门禁

等待用户明确授权 Step 7。不得读取或记录密码、2FA、Cookie；不得创建/推送 tag、上传制品
或进入 R-002。

## 当前验证

```powershell
$env:MCP_WEATHER_RUN_LIVE = $null
uv lock --check
uv run ruff format --check .
uv run ruff check .
uv run mypy
uv run pytest -q --tb=short
git diff --check
git status --short
git diff --name-status
git ls-files --others --exclude-standard
```

## 停止条件

发现合并事实不一致、来源不明变更、敏感信息、需要修改源码/依赖/系统环境、publisher login/publish、Registry/PyPI 写入、tag/Release 或需要自动进入后续任务时立即停止并报告。
