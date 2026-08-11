# 任务卡：F-002 可安装与可构建闭环

## 任务状态

- 状态：`approved / step_6_completed / draft_pr_open / awaiting_user_review`
- 项目整体等级：M
- 当前任务等级：S
- 用户选择：已选择 F-002
- 任务卡批准：已批准（2026-08-11）
- 当前分支：`feat/f-002-installable-package`
- 基线：`main` 与 `origin/main` 均为 `4d84ad0`
- 环境：local build / clean install / synthetic offline
- 外部发布：不在本任务范围，未授权

本文件是当前唯一活动任务卡。F-001 已归档到
`docs/archive/task-cards/F-001-一个-Tool-的本地天气闭环.md`。本任务只关闭“源码可运行但不能作为标准 Python 包安装”的缺口，不进入外部发布。

## 用户目标

Python/MCP 学习者希望把现有只能依赖源码路径启动的天气 MCP Server 构建成标准 wheel 和 sdist，并在项目外的干净 Python 环境安装后，通过稳定的 console command 启动同一个 stdio Server。

## 业务价值

完成后形成可复现的本地制品闭环：

```text
项目源码
→ uv 构建 wheel/sdist
→ 审查真实制品
→ 项目外双干净环境安装
→ console command 启动 stdio
→ MCP discovery 与唯一 Tool
→ 安装包的确定性离线 Tool 调用
```

这为 D-001 发布候选准备提供可信制品基础，但不等于已经发布。

## 当前能力与缺口

当前已有：

- 标准 `src/mcp_weather_query/` import package；
- `mcp_weather_query.__main__:main` 生产 stdio 入口；
- 唯一 `get_current_weather` Tool；
- 官方 SDK v2 in-memory、现代/Legacy stdio 和真实子进程测试；
- `pyproject.toml` 中的显式 `uv_build`、版本 `0.1.0`、console entry point、
  Python 范围、运行依赖和 MIT/License-File 元数据；
- 根目录 MIT `LICENSE` 与单独的 Open-Meteo `NOTICE`；
- 项目环境中的 `mcp-weather-query` console script；
- 一个经审查的 pure-Python wheel 和一个 sdist；
- 可重复执行的真实制品清单、元数据、RECORD 和敏感信息审查脚本；
- 项目外两个独立环境的 wheel/sdist 安装来源、console stdio、现代 discovery 和
  确定性 structuredContent 证据；
- `.gitignore` 已排除 `build/`、`dist/` 和 `*.egg-info/`。

当前仍缺少：

- 用户审查 Draft PR #3；Step 6 Git/PR 交付已完成；
- 后续经独立授权的 Git/PR 交付和合并后收口。

当前已使用 `uv build` 先生成 sdist、再从 sdist 生成 wheel，并完成静态制品审查；
两个制品已分别在项目外独立环境安装，并在非源码工作目录、无 `PYTHONPATH` 下
完成 installed-package stdio 验证。

## 已批准命名与构建决策

| 决策 | 已批准值 |
| --- | --- |
| Python distribution | `mcp-weather-query` |
| import package | `mcp_weather_query` |
| console command | `mcp-weather-query` |
| console target | `mcp_weather_query.__main__:main` |
| MCP Server name | 保持 `mcp-weather-query` |
| 初始包版本 | `0.1.0` |
| 代码 License | MIT |
| 署名 | 根目录 `NOTICE` + README + 现有 Tool 输出元数据 |
| build backend | 优先 `uv_build`；先验证与现有 uv 0.6.14 的兼容性 |
| 制品 | wheel 和 sdist 均为强制验收制品 |
| 干净安装 | wheel 与 sdist 分别使用独立环境 |
| 临时环境 | 项目外 E 盘独立目录 |
| GitHub CI | F-002 不新增；使用本地门禁和 PR 人工审查 |
| sdist 测试 | 允许有意保留的测试源码；wheel 禁止包含测试 |
| 依赖获取 | 允许从官方 Python 包索引读取已声明依赖；Tool 调用必须离线 |

项目代码的 MIT License 与 Open-Meteo 数据的 CC BY 4.0 署名必须分开表达，不能把数据许可写成本项目代码许可证。

## 范围

- 配置显式 Python build backend 和 `src` layout 包发现。
- 移除 `tool.uv.package = false` 的 source-only 边界。
- 配置稳定 console entry point，默认启动现有 stdio Server。
- 将本地初始版本设为 `0.1.0`。
- 新增 MIT `LICENSE` 和 Open-Meteo `NOTICE`，并纳入制品元数据/文件。
- 使用现有 uv 构建真实 wheel 和 sdist。
- 检查 wheel/sdist 文件清单、METADATA、entry point、Python 范围、依赖、License 和 NOTICE。
- 在项目外分别安装 wheel 和 sdist，不依赖 editable install 或 `PYTHONPATH`。
- 验证安装后的 console command、MCP discovery、唯一 Tool、stdout/stderr 和退出。
- 通过只存在于测试中的 fixed handler 验证已安装包的确定性离线 Tool 调用。
- 执行独立 QA、用户 UAT、Git PR 和合并后收口。

## 非目标

- 不上传 TestPyPI 或 PyPI，不执行 `uv publish`。
- 不登记 MCP Registry，不创建 `server.json`、Release 或发布标签。
- 不把本地构建或安装写成外部已发布。
- 不增加第二个 Tool，不修改 Tool 名称、input/output Schema、annotations 或稳定错误语义。
- 不增加 Streamable HTTP、SSE、远程部署、Agent、RAG、数据库或 UI。
- 不访问 Open-Meteo live API，不运行 MCP Inspector。
- 不更新或覆盖 Cherry Studio 管理的 uv，不修改系统 Python、Node、注册表或全局环境变量。
- 不新增 GitHub Actions；如需 CI，必须另行调整范围。
- 不进入 D-001、R-001 或 R-002。
- 不提交 `dist/`、`build/`、干净环境、缓存、日志、Token 或本机私有配置。

## 前置条件与环境边界

- 项目：`E:\Agent\开发实践\MCP1-天气查询`
- 当前分支：`feat/f-002-installable-package`
- Python：项目内 CPython 3.12.10
- uv：复用现有 0.6.14，不原地更新
- 默认测试：synthetic/offline；live contract 保持显式跳过
- 构建和首次依赖解析可能访问官方 Python 包索引，但不得执行任何上传
- 干净环境建议位于：
  `E:\Agent\.tmp\mcp1-weather-query\f-002\<run-id>\wheel-env` 和 `sdist-env`
- 临时环境不自动批量删除；清理前需精确列出路径并遵守用户确认

## 输入、输出与状态变化

输入：

- 当前干净源码树、`pyproject.toml`、`uv.lock`；
- 现有 `mcp_weather_query.__main__:main`；
- 已验证的 stdio 测试和 synthetic fixture。

输出：

- 一个 sdist 和一个 pure-Python wheel；
- 可审查的包元数据、License 和 NOTICE；
- 安装后的 `mcp-weather-query` command；
- wheel 和 sdist 各自的干净安装证据；
- 安装后 stdio 与离线 Tool call 证据；
- 不包含实际制品的 Git PR。

状态变化：

```text
source-only / package=false
→ packageable
→ wheel + sdist
→ clean-install verified
→ PR merged
→ F-002 closed
```

## 数据、安全与权限边界

- 不新增或修改业务数据、数据库、用户账户或持久状态。
- 构建后端在隔离环境执行；只允许声明的构建依赖和运行依赖。
- console command 不读取新增 secrets，不需要 API Key。
- 默认验收不得发起天气查询；确定性 Tool 调用必须注入 synthetic handler。
- stdout 只允许 MCP 协议消息；诊断只能进入 stderr。
- 制品和证据不得包含绝对个人路径、环境变量值、Token、Cookie、完整上游响应或临时环境内容。
- 用户输入仍不能改变 Open-Meteo 固定 endpoint；F-002 不修改这一边界。

## 制品契约

Wheel 必须包含：

- `mcp_weather_query` 生产包；
- `.dist-info/METADATA`、`entry_points.txt` 和 `RECORD`；
- License/NOTICE；
- 正确的名称、版本、运行依赖和 Python 范围。

Wheel 禁止包含：

- `tests/`、synthetic fixture、项目管理文档；
- `.runtime/`、`.venv/`、缓存、日志、Git 数据；
- `dist/`、`build/`、凭证、本机私有配置或源码绝对路径。

Sdist 必须包含生产源码、`pyproject.toml`、README、License/NOTICE 和从 sdist 重建 wheel 所需内容；允许有意保留的测试源码，但禁止测试缓存、运行日志和临时制品。

## 安装后协议验证边界

生产 console command 只验证：启动、现代 MCP discovery、`tools/list`、唯一 Tool、stdin 关闭、退出码、stdout/stderr；不执行天气 Tool，因此不访问 live API。

确定性 Tool call 使用测试专用 runner：

- runner 从项目外工作目录启动，使用干净环境的已安装包；
- 不设置 `PYTHONPATH`；
- 通过 `create_server(fixed_handler)` 注入 synthetic 结果；
- runner 不成为 console entry point，不进入 wheel；
- 返回结果通过 `CurrentWeatherResult` 和 outputSchema 校验；
- 该证据不代表 Open-Meteo live 可用性。

## UI 与交互状态

本任务没有图形 UI。命令/stdio 状态为：

| 状态 | 预期 |
| --- | --- |
| 启动 | command 阻塞等待 Host 输入，不打印普通文本 |
| 正常协议 | stdout 仅包含 MCP 消息 |
| 诊断 | 仅进入 stderr |
| stdin 关闭 | 有限时间内退出码 0 |
| 安装缺失 | command/import 明确失败且测试可观察 |
| Tool 调用 | synthetic handler 返回合法 structuredContent |

## 验收标准

1. `uv build` 生成一个 wheel 和一个 sdist。
2. 制品不含缓存、日志、凭据、本机私有路径和未授权内容。
3. wheel 和 sdist 分别在项目外独立环境安装成功。
4. 安装验证不使用 editable install、项目源码目录或 `PYTHONPATH`。
5. 任一干净环境导入的 `mcp_weather_query` 来自该环境安装位置。
6. `mcp-weather-query` command 启动现有生产 stdio Server。
7. 官方 SDK Client 完成现代 discovery，`tools/list` 只发现 `get_current_weather`。
8. 已安装包通过测试专用 runner 完成确定性离线 Tool 调用并返回合法 structuredContent。
9. stdout 无协议外文本，诊断仅在 stderr，关闭后无遗留子进程。
10. wheel 元数据中的名称、`0.1.0`、Python 范围、依赖、entry point、MIT 和 License-File 可检查。
11. sdist 能独立提供重建 wheel 所需文件。
12. 默认离线门禁全部通过，live contract 仍是唯一显式 skip。
13. 没有 HTTP/SSE、第二 Tool、敏感信息、发布配置或已提交制品。
14. 独立 QA、用户 UAT、PR 和合并后文档收口完成后才关闭任务。

## 测试矩阵

| 风险/行为 | 层级 | 核心验证 | 失败证明 |
| --- | --- | --- | --- |
| package 未启用 | 配置测试 | build-system/package 状态 | 当前 `package=false` 先失败 |
| console script 缺失 | 元数据测试 | `[project.scripts]`/wheel entry point | 当前安装后无 command |
| wheel 内容污染 | 制品测试 | `zipfile` 白/黑名单 | 禁止路径进入时失败 |
| sdist 不完整 | 制品测试 | `tarfile` 必要文件 | 缺源码/metadata 时失败 |
| 元数据错误 | 制品测试 | `importlib.metadata` | 名称/版本/依赖漂移时失败 |
| wheel 安装 | clean-install smoke | 安装具体 `.whl` | 不得回退源码 import |
| sdist 安装 | clean-install smoke | 安装具体 `.tar.gz` | 缺 build 文件时失败 |
| `PYTHONPATH` 假阳性 | 隔离测试 | 清除变量、项目外 cwd、模块路径 | 模块来自项目 `src` 时失败 |
| console stdio | 子进程 smoke | discovery、唯一 Tool、退出 | command/协议污染时失败 |
| 离线 Tool call | 协议 smoke | installed package + fixed runner | 网络访问/Schema 漂移时失败 |
| License/NOTICE | 制品测试 | wheel/sdist/metadata 检查 | 文件或字段缺失时失败 |
| 回归 | 全量门禁 | Ruff、mypy、pytest、lock | 现有行为回归时失败 |
| 敏感信息 | 范围扫描 | 源码、元数据、制品 | 凭据或本机私有路径命中时失败 |

## 文件影响范围

预计允许修改：

- `pyproject.toml`、`uv.lock`；
- `LICENSE`、`NOTICE`、`README.md`；
- `src/mcp_weather_query/__main__.py`，仅当 entry point 兼容性需要最小调整；
- `tests/` 中与 packaging、artifact、clean-install 和 installed-stdio 直接相关的文件；
- `.gitignore`，仅当出现遗漏；
- `docs/README.md`、`docs/architecture.md`、`docs/testing-strategy.md`、`docs/release-plan.md`、`docs/evidence.md`；
- `docs/project-management/` 当前任务、计划、进度和 roadmap；
- `docs/archive/task-cards/` 已关闭任务卡。

明确不修改：

- Tool 契约、天气领域模型、服务和适配器；
- HTTP/SSE、live API 或 Inspector 配置；
- GitHub Actions；
- `server.json`、CHANGELOG、Release、PyPI/Registry 配置；
- 系统、Cherry Studio、全局 uv/Python/Node。

## 文档更新契约

- 当前任务入口：本文件。
- 当前计划：`docs/project-management/implementation-plan.md`。
- 短状态：`docs/project-management/progress.md`。
- 路线：`docs/project-management/roadmap.md`。
- 验收证据：`docs/evidence.md`。
- F-001 归档：`docs/archive/task-cards/F-001-一个-Tool-的本地天气闭环.md`。
- F-002 完成并合并后归档到 `docs/archive/task-cards/F-002-可安装与可构建闭环.md`，再把 current-task 重置为无活动任务。
- README 不得把本地构建写成 PyPI 或 Registry 已发布。

## 风险与回滚

- uv 0.6.14 已成功调用 `uv_build` 完成项目环境安装和真实 wheel/sdist 构建；
  Step 4 又完成两个项目外环境安装，无需升级或覆盖 Cherry Studio 管理的 uv。
- sdist 可能能生成但不能重建 wheel：必须从 sdist 构建和单独安装。
- 测试可能误用源码目录：项目外 cwd、清除 `PYTHONPATH` 并检查模块实际路径。
- console command 可能污染 stdout：真实子进程捕获每条协议消息。
- License 与数据署名可能混写：MIT 与 CC BY 4.0 NOTICE 分离检查。
- 临时环境和制品可能误提交：保持 ignore，并在 Git 交付前审查。
- 回滚通过功能分支精确提交或 PR revert；不重置 `main`，不删除源码。

## 上下文与预算

- 任务级别：S，仍服从项目 M 级任务卡/分支/PR 流程。
- 每个 Step 只读取任务卡、当前计划、短进度和直接相关文件。
- 不设置显式 Token 预算；如范围扩展到 CI、发布、Registry 或 Tool 契约，立即停止重切。

## Step 地图

### Step 0：任务与构建基线

- 状态：`completed`（2026-08-11）。
- [x] 用户批准 F-002 和 14 项决策。
- [x] 核对 `main`/`origin/main`/工作树并创建功能分支。
- [x] 归档 F-001，建立 F-002 当前任务和计划入口。
- [x] 只读核验现有 uv 0.6.14 的 build frontend 能力与候选 `uv_build` 的兼容边界。
- [x] 运行默认离线基线门禁：`52 passed, 1 skipped`，其余门禁通过。
- 不修改 packaging 配置，不构建制品，不提交或推送。

兼容性结论：现有 uv 0.6.14 的命令帮助明确支持 PEP 517、wheel 和 sdist
构建前端能力；由于 Step 0 禁止构建，尚未实际调用候选 `uv_build` 后端，不能把
具体后端版本的运行兼容性写成已验证。该验证留在获准的后续构建 Step；若必须
更新 uv，立即停止并提交 E 盘独立 uv 方案，不覆盖 Cherry Studio 管理的 uv。

### Step 1：先失败的 packaging 契约测试

- 状态：`completed`（2026-08-11）。
- [x] 建立 package/build-system、版本、entry point、License/NOTICE 契约测试。
- [x] 建立 wheel/sdist 制品矩阵和双干净安装隔离矩阵骨架。
- [x] 证明当前 source-only 状态的六个预期失败：`package=false`、无显式
  build system、版本仍为 `0.0.0`、无 console script、无许可证元数据、无
  LICENSE/NOTICE。
- [x] 新测试通过 Ruff 和严格 mypy；既有离线回归保持 `52 passed, 1 skipped`。
- 完整 pytest 的真实红灯为 `6 failed, 56 passed, 1 skipped`；这是 Step 2 的输入，
  不得写成全量门禁通过。
- 本 Step 未修改生产 packaging 配置，未构建或安装制品。

### Step 2：最小可安装包配置

- 状态：`completed`（2026-08-11）。
- [x] 使用 `uv_build>=0.11.32,<0.12` 和默认 `src` layout。
- [x] 移除 `tool.uv.package=false`，版本更新为 `0.1.0`。
- [x] 注册 `mcp-weather-query = "mcp_weather_query.__main__:main"`。
- [x] 新增 MIT LICENSE、Open-Meteo NOTICE 和 SPDX/License-File 元数据。
- [x] `uv lock` 仅把根项目从 `0.0.0 / virtual` 更新为 `0.1.0 / editable`。
- [x] Step 1 契约从 `6 failed, 4 passed` 转为 `10 passed`；完整默认测试为
  `62 passed, 1 skipped`。
- [x] uv 0.6.14 成功调用后端并在项目环境安装 console script，无需更新 uv。
- 本 Step 没有执行 `uv build`，没有生成 wheel/sdist、`dist/` 或项目外环境。

### Step 3：真实构建与制品审查

- 状态：`completed`（2026-08-11）。
- [x] `uv build` 先构建 `mcp_weather_query-0.1.0.tar.gz`，再从 sdist 构建
  `mcp_weather_query-0.1.0-py3-none-any.whl`。
- [x] wheel 精确包含 15 个文件：9 个生产源码文件及 6 个 `.dist-info` 文件；
  不含 tests、docs、fixture、缓存、日志或本机配置。
- [x] sdist 精确包含 14 个文件：生产源码、PKG-INFO、pyproject、README、
  LICENSE 和 NOTICE；足以在 Step 4 验证重建/安装。
- [x] METADATA/PKG-INFO 为 2.4，名称/版本/Python/依赖/MIT/License-File 正确。
- [x] console entry point、purelib 和 `py3-none-any` 正确；wheel RECORD 的文件、
  SHA-256 和大小逐项校验通过。
- [x] wheel/sdist 中生产源码及法律文件与工作树逐字节一致，无绝对本机路径或
  明显凭据赋值。
- [x] README 状态更新后重新构建，最终制品不再嵌入构建前状态。
- 没有安装制品、创建项目外环境、上传或发布。

### Step 4：双干净环境安装与 stdio smoke

- 状态：`completed`（2026-08-11）。
- [x] 在项目外 E 盘目录创建互相独立的 wheel-env/sdist-env 和工作目录。
- [x] wheel/sdist 分别从精确制品安装；`direct_url.json` 证明来源，且不是 editable。
- [x] 两套 package import/console 均来自各自环境，不依赖源码目录或 `PYTHONPATH`。
- [x] 生产 console 完成 raw stdio handshake/tools-list，只发现 `get_current_weather`，
  stdout 仅协议消息、stderr 无 traceback、退出码 0。
- [x] 官方 v2 Client 对两套生产 console 协商 MCP 2026-07-28。
- [x] 未进入制品的测试 runner 使用已安装包完成确定性离线 Tool 调用，返回通过
  outputSchema 模型校验的 `structuredContent`，诊断只进入 stderr。
- [x] 没有 live API、Inspector、第二 Tool、HTTP/SSE、遗留子进程或发布行为。

### Step 5：独立 QA 与用户 UAT

- 状态：`completed`（2026-08-11）。
- [x] 独立审查完整 tracked/untracked diff、任务卡、制品、双安装证据和安全范围。
- [x] 发现旧 `dist` 的 README/长描述已落后于当前 README；增强制品门禁后，旧
  制品得到预期失败。
- [x] 在项目外 `step5-20260811-a` 构建新的 QA wheel/sdist；精确清单、元数据、
  RECORD、法律文件、敏感路径和当前 README 一致性均通过。
- [x] 新 QA wheel/sdist 分别安装到两个新环境，并重复通过安装来源、console
  stdio、唯一 Tool、MCP 2026-07-28、structuredContent、stdout/stderr 和退出验证。
- [x] lock、Ruff、严格 mypy、完整默认 pytest 和 diff 门禁通过；没有 live API、
  Inspector、HTTP/SSE、第二 Tool、发布或 Git 交付。
- [x] 用户从 QA wheel 干净环境执行验证命令，并于 2026-08-11 明确确认 UAT 通过。

### Step 6：Git/PR 交付

- 状态：`completed / draft_pr_open / awaiting_user_review`（2026-08-11）。
- [x] 精确审查并按意图拆分提交：
  - `af1f4af build(package): make weather server installable`；
  - `64e0328 test(packaging): verify build and clean installs`；
  - `docs(project): record F-002 draft PR delivery`（本次文档交付）。
- [x] 推送 `feat/f-002-installable-package` 到 `origin`，未推送 `main`。
- [x] 创建 Draft PR #3：`feat/f-002-installable-package → main`。
- [x] PR 正文记录范围、非目标、验证、回滚和“F-002 不新增 GitHub Actions”的
  local-only 门禁例外；没有把缺少远程 CI 写成 CI 通过。
- [x] 没有提交 `dist`、QA 环境、日志、运行时或敏感信息。
- [ ] 用户审查 PR 并决定标记 Ready 或合并；本 Step 不自动执行。

### Step 7：合并后收口

- 同步 `main`、归档 F-002、重置 current-task、更新 roadmap/progress/evidence；不自动进入 D-001。

## 停止条件

- `main`、`origin/main` 或工作树出现无法解释的不一致。
- 需要修改 Tool 契约、数据源、业务错误或增加 transport。
- 现有 uv 无法安全调用候选 build backend，或继续必须更新系统/Cherry Studio 环境。
- 需要 live API、Inspector、外部上传、Registry、Release 或 GitHub Actions。
- 干净安装只能通过 editable install 或 `PYTHONPATH`。
- 测试 runner 必须进入生产 wheel。
- 发现敏感信息、来源不明文件、用户无关改动或需要删除/覆盖文件。
- 范围扩大到不能通过一次构建/安装/UAT 闭环验收。

## 完成定义

- [ ] F-002 各验收标准通过，负向与隔离测试覆盖。
- [x] wheel 和 sdist 真实构建并完成制品审查。
- [x] wheel/sdist 分别在项目外干净安装。
- [x] console command 和已安装包的离线 MCP 验证通过。
- [x] License/NOTICE 和包元数据正确。
- [x] 默认离线门禁和独立 QA 完成。
- [x] 用户 UAT 完成。
- [ ] diff、提交和 Draft PR 证据已齐全；用户 PR 审查与合并尚未完成。
- [ ] F-002 已归档，current-task 重置，文档与 Git 事实一致。
- [ ] 未进入 D-001、PyPI、Registry 或其他发布。
- [ ] 没有无关修改、敏感信息或已提交构建/临时制品。

## 审批记录与下一门禁

用户于 2026-08-11 批准本任务卡的目标、范围、非目标、命名、版本、MIT License、构建方案、测试矩阵、Step 地图和完成定义，并确认 14 项推荐决策。Step 6 已按授权完成精确提交、功能分支推送和 Draft PR #3 创建；当前等待用户审查 PR，并决定标记 Ready 或合并。不得自动进入 Step 7。
