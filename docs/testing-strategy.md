# 测试策略

## 目标

测试从用户行为和风险推导，覆盖 Tool schema、地点解析、上游错误、结构化输出和 stdio 协议边界。Mock 测试只证明确定性逻辑；外部 API 的真实可用性必须单独标记为 live contract 证据，不能由 fixture 冒充。

## 分层

| 层级 | 主要内容 | 是否默认联网 |
| --- | --- | --- |
| 领域/服务单元测试 | 输入规范化、WMO code 映射、两步编排、错误分类、单位和模型组装 | 否 |
| HTTP 适配器测试 | query params、固定域名、超时、429、4xx/5xx、坏 JSON、缺字段 | 否，使用 MockTransport/fixture |
| MCP 协议集成测试 | `tools/list`、inputSchema/outputSchema、annotations、`tools/call`、Tool error | 否，优先 SDK in-memory session |
| stdio 冒烟测试 | 子进程启动、Tool 发现、一次调用、退出、stdout 无协议外文本 | 否，可注入固定适配器或测试模式；不得把测试模式用于发布运行 |
| live contract 测试 | Open-Meteo 地理编码和当前天气最小响应契约 | 是，显式 opt-in，失败需区分网络/上游/代码 |
| Inspector 人工验收 | 连接、Tool 描述/Schema、成功与错误显示 | 查询天气时联网 |
| 构建/安装测试 | wheel/sdist 内容、双干净环境安装、console entry point、官方 SDK Client 从包启动 | 构建可离线；首次依赖解析可能联网 |

## 最低行为矩阵

- 有效中文城市、有效英文城市、带 `country_code` 的地点。
- 输入前后空白、过短/过长地点、非法国家代码。
- 地理编码无结果。
- 同名地点：返回解析后地点，使调用方能识别实际选择；限制写入文档。
- 地理编码超时、天气请求超时。
- 429、5xx、连接失败、无效 JSON、必填字段缺失。
- 成功结果通过输出 Schema，所有数值带明确单位和有效时间。
- Tool 列表只有首期授权的 `get_current_weather`。
- annotations 与只读/开放世界边界一致。
- 日志进入 `stderr`；`stdout` 不出现普通 `print`、调试文本或堆栈。
- 用户输入无法改变 scheme、host 或 path 基址。

## 当前门禁

项目继续复用以下默认离线门禁：

```text
uv lock --check
uv run ruff format --check .
uv run ruff check .
uv run mypy
清除 MCP_WEATHER_RUN_LIVE 后运行 uv run pytest -q --tb=short
git diff --check
```

R-001 Step 2 已使发布契约全部转绿：完整 pytest 为 `85 passed, 1 skipped`，唯一 skip
仍是显式 live contract。Step 1 的历史红灯为 `7 failed, 78 passed, 1 skipped`，对应
尚未实现的发布 workflow 和最终公开发布说明。

`uv build`、wheel/sdist 审查属于 F-002 Step 3，双干净安装与 installed-package
stdio 验证属于 Step 4，两者均已通过。Inspector 是人工协议调试工具，不替代自动化协议集成测试；live API 测试
不应成为每次离线单元测试的硬依赖。

## F-002 packaging 测试分层

- Step 1 配置契约：静态读取 `pyproject.toml`，验证 package 状态、显式
  `uv_build`、`0.1.0`、console entry point、SPDX MIT 和 LICENSE/NOTICE。
- Step 1 制品骨架：明确 wheel/sdist 都是 Step 3 强制制品，不在红灯阶段调用构建。
- Step 1 安装骨架：明确 wheel-env/sdist-env 分离，并禁止 editable install 和
  `PYTHONPATH`；真实创建环境留在 Step 4。
- Step 2 已通过最小配置使 `10` 项 packaging 契约全部转绿，没有用生成空制品、
  跳过测试或放宽断言规避契约。
- Step 3 已执行真实构建，并使用 `tests/packaging/inspect_artifacts.py` 检查精确
  文件白名单、Core Metadata、entry point、wheel RECORD、源码一致性和敏感路径。
- Step 4 已在项目外 `wheel-env`/`sdist-env` 分别安装约定制品；安装 provenance、
  无 `PYTHONPATH` 的 console stdio、唯一 Tool、现代 discovery、确定性
  `structuredContent`、stdout/stderr、退出码和无遗留进程均通过。
- `tests/packaging/verify_installed_package.py` 不进入制品；它从安装环境自身导入
  包并读取 `direct_url.json` 区分 wheel/sdist 来源，固定 Tool handler 不访问网络。
- Step 5 独立 QA 将内嵌 README 检查从临时 Step 文字升级为与当前根 README
  UTF-8 内容一致；旧 `dist` 得到预期失败，新 QA 候选通过并重新完成两套安装验证。
- 用户随后从 Step 5 QA wheel 干净环境运行同一 installed-package 验证命令，并明确
  确认 UAT 通过；该确认不替代自动门禁，也不代表外部发布。
- F-002 按已批准决策不新增 GitHub Actions；PR #3 明确记录 local-only 门禁例外，
  因此 PR 页面没有新增远程 CI 不能被误写成“CI 通过”或“未测试”。
- Step 7 合并后复验补充跨平台文本规则：源文件、README 和法律文件比较先统一
  CRLF/LF；wheel `RECORD` 的原始字节大小、哈希和覆盖范围仍必须严格复算。

截至 F-002 Step 7，MCP 协议集成层已通过官方 SDK in-memory client 验证；真实子进程层分别验证生产入口的 Legacy 原始协议握手/discovery/退出、官方 v2 Client 的现代 discovery，以及测试专用固定 Server 的结构化 Tool call。默认测试仍全部离线；`tests/integration/test_open_meteo_live.py` 只有在显式设置 `MCP_WEATHER_RUN_LIVE=1` 时才执行真实 Open-Meteo 两步契约。最近一次默认结果为 `62 passed, 1 skipped`，唯一 skip 是 live contract。

子进程测试使用 10 秒单步超时；原始进程测试在 `finally` 中终止未退出进程，SDK client 则使用其上下文管理器执行关闭 stdin、限时等待和进程树清理。测试专用 Server 的诊断标记必须出现在 `stderr`，所有生产入口 `stdout` 行必须能解析为 JSON-RPC。

live contract 只断言固定 endpoint、响应模型、解析地点和来源/许可证元数据，不保存完整响应。Inspector 使用精确 v2.1.0、项目虚拟环境 Python、显式源码 `PYTHONPATH` 与工作目录；人工验证唯一 Tool、输入字段、annotations、结构化成功结果和稳定错误语义，结束后关闭进程并使临时认证令牌失效。

兼容性复验使用项目独立 Node 24.19.0 消除 Inspector engine warning。协议证据区分两条路径：stdio Inspector 的 Legacy `initialize`/2025-11-25 只证明向后兼容；官方 SDK v2 `Client(mode="auto")` 对生产 stdio 入口执行 `server/discover`，以 `protocol_version=2026-07-28`、存在 `discover_result` 且不存在 `initialize_result` 证明现代路径。测试专用 stdio Server 在同一现代协议下完成离线 Tool call。不得要求一个 2026 会话展示 `initialize=2026-07-28`，也不得把 Legacy Inspector 会话冒充现代协议证据。

## D-001 发布候选测试分层

- Step 1 新增 `tests/release/test_release_candidate_contract.py`，只静态读取现有文件，
  不构建、不安装、不启动子进程、不联网。
- 6 个预期红灯分别对应：缺少 CHANGELOG、候选 wheel 安装说明、未来 PyPI 命令及
  未发布标签、Host stdio 配置、PyPI Registry ownership marker/明确未发布边界、
  `uv build --no-sources` 与安全 publisher 命令契约。
- 现有 distribution/import/console/version/License identity 继续通过，防止 D-001 借发布
  准备改名、升级版本或替换入口。
- Step 3 Registry 矩阵只允许 `server.json`、当前固定 Schema、PyPI 引用和 stdio；
  `login`/`publish` 明确禁止。本 Step 不创建或校验 manifest。
- Step 4 强制 wheel/sdist 两种候选制品且不提交 Git；Step 5 强制两个独立安装环境，
  禁止 editable、`PYTHONPATH` 和 live 天气请求。本 Step 只定义矩阵。
- Step 1 完整测试故意为 `6 failed, 66 passed, 1 skipped`；排除 release contract 后，
  既有回归仍为 `62 passed, 1 skipped`。
- Step 2 只新增/更新 README、CHANGELOG 和 release plan，使 release contract 达到
  `10 passed`；完整离线测试为 `72 passed, 1 skipped`，没有放宽断言或执行后续矩阵。
- Step 3 新增 `server.json` 与 4 项静态契约，检查 Schema、名称/版本、PyPI package、
  `runtimeHint=uvx`、stdio、README marker/repository 一致性，并拒绝 remote、HTTP/SSE、
  环境变量、参数和敏感字段。release 测试合计 `14 passed`。
- 官方 `mcp-publisher v1.8.1 validate` 额外完成 Schema/语义验证。该命令会把 manifest
  POST 到未认证 `/v0/validate`，因此与默认离线 pytest 分开记录，不能写成纯离线
  证据；它不调用 publish 或创建 Registry 条目。
- Step 3 完整默认离线测试为 `76 passed, 1 skipped`，唯一 skip 仍是 live contract。
- Step 4 以 `uv build --no-sources --offline` 在项目外生成候选，并复用/增强
  `tests/packaging/inspect_artifacts.py`。外层目录必须恰有 uv 的 `*` 型 `.gitignore`、
  一个 wheel 和一个 sdist；归档内部继续使用精确白名单。
- wheel 检查 15 个文件、Core Metadata 2.4、pure-Python tag、console entry point、
  RECORD 全覆盖/大小/SHA-256；sdist 检查 14 个可重建文件和当前 pyproject/README。
- 两个制品还必须与当前源码、LICENSE/NOTICE、README 一致；README 直接检查 Registry
  marker、Open-Meteo/CC BY 4.0 和 PyPI/Registry 未发布状态。所有 payload 扫描本机
  路径、运行时目录和秘密赋值。
- Step 4 只做静态审查，明确没有安装、import 或 stdio；这些属于 Step 5。
- Step 5 在项目外新建 `wheel-env`/`sdist-env`，以 `UV_OFFLINE=1` 从 Step 4 固定制品
  分别安装。验证器必须由各自环境 Python 运行，并检查 `direct_url.json`、模块和 console
  来源，拒绝 editable、源码目录、`PYTHONPATH` 与 `VIRTUAL_ENV` 泄漏。
- 每套 installed-package 复验包含三条证据：原始生产 console 的 Legacy
  initialize/tools-list/stdout/exit；官方 SDK v2 Client 的 MCP 2026-07-28 modern
  discovery；未发布的测试专用入口对已安装生产包执行确定性结构化 Tool 调用。三条均只
  允许唯一 `get_current_weather`，且不访问天气 API。
- 子进程单步超时为 10 秒；生产 stderr 不得含 traceback，测试诊断只进入 stderr，关闭后
  不得残留来自 Step 5 环境的 Python/uv/Node 进程。Step 5 实际结果为 wheel 与 sdist
  两条验证均通过；默认回归保持 `76 passed, 1 skipped`。
- Step 6 独立 QA 把发布候选 README 的阶段文字改为当前事实后，先确认旧 Step 4 制品因
  嵌入 README 过期而失败，再在新的项目外 QA 目录离线重建。QA wheel/sdist 均重新通过
  精确白名单、元数据、源码/法律文件/README 一致性、双安装 provenance 和三条 stdio
  证据；用户 UAT 只使用该 QA 候选。

## R-001 PyPI 发布契约分层

- Step 1 新增 `tests/release/test_pypi_publish_contract.py`，只静态读取本地 workflow、
  package identity、README、CHANGELOG 和 release plan；不构建、不联网、不请求 OIDC。
- 两个绿色守卫固定 `mcp-weather-query`/`mcp_weather_query`/console/`0.1.0` 身份，并确保
  在真实发布完成前 CHANGELOG 继续写 `Unreleased` 和“尚未发布”。
- 五个 workflow 红灯要求专用 `release.yml`、PR 与精确 `v0.1.0` tag 入口、build/publish
  隔离、publish job 的 `pypi` environment 与最小 OIDC 权限，以及所有 action 的完整 SHA。
- publish job 只允许下载 build job 的制品并调用官方 PyPA action；禁止 build/test、
  password/username、`secrets.*`、TestPyPI、`skip-existing` 和关闭 attestations。
- 其余两个红灯要求 release plan 记录 Pending Trusted Publisher 精确 tuple、双授权和
  yank 边界，并要求公共 README 披露 Open-Meteo 非商业层、三档限额、无 SLA 和 CC BY。
- Step 1 定向结果为 `7 failed, 2 passed`；完整结果为 `7 failed, 78 passed, 1 skipped`；
  排除故意红灯后既有回归仍为 `76 passed, 1 skipped`。
- Step 2 新增 `release.yml`、公开 Open-Meteo 限制和 Trusted Publisher/recovery 文档，
  使 9 项契约全部通过；没有删除或放宽 Step 1 断言。真实 workflow 运行留到 Git/PR Step。
- Step 3 在项目外离线重建 wheel/sdist，并复用严格 artifact/installed-package 验证器。
  两个制品分别在新的环境离线安装，均通过 provenance、Legacy/现代协议、唯一 Tool、
  确定性结构化调用、stdout/stderr、退出和无残留进程；默认门禁保持 `85 passed, 1 skipped`。
- Step 4 独立 QA 发现 build job 缺少上传前制品检查；最小修复后，workflow 会先执行
  `inspect_artifacts.py dist` 再上传，静态契约同时固定该顺序。Step 3 固定制品和两套安装
  再次复验通过，2026-08-12 新 live contract 为 `1 passed in 2.73s`；用户随后在固定 wheel
  环境完成并确认 UAT，通过 provenance、唯一 Tool、结构化输出、stdio 纯净性和退出验收。
- Step 5 首次 PR run 暴露旧 artifact actions 的 Node.js 20 弃用告警；upload 更新到官方
  v7.0.1、download 更新到官方 v8.0.1 的完整 SHA，二者均使用 Node.js 24。最终 PR CI
  必须以该修复后的提交为准，旧成功 run 不能替代最新证据。

## 验收证据格式

每项证据至少记录命令/操作、环境、预期、实际、结论、覆盖范围和未覆盖风险。不得保存完整网络响应、凭证、Cookie、个人位置或冗长终端日志。

## R-002 Registry 登记契约

- Step 1 新增 `tests/release/test_mcp_registry_publish_contract.py`，只读取本地 manifest、包元数据、
  README、release plan 和 GitHub workflow，不执行 publisher 或网络请求。
- 四个初始绿灯固定现有正确边界：Registry/PyPI 0.1.0 身份、恰好一个 `uvx`/stdio package、
  workflow 无 Registry 命令，以及 manifest 无凭据或远程传输。
- 六个初始红灯要求 Step 2 补充：README 的 R-002 active/未登记状态；Registry preview 与
  CC0 1.0；手工 GitHub OAuth device flow；validate/login/publish/官方 API 分离；同版本不可
  原地覆盖与不确定 publish 恢复；复用固定 publisher 且禁止重新下载。
- Step 1 定向结果为 `6 failed, 4 passed`；完整套件为 `6 failed, 89 passed, 1 skipped`；
  排除故意红灯后既有回归仍为 `85 passed, 1 skipped`。
- Step 2 不得删除、跳过、`xfail` 或放宽红灯断言；只允许以批准范围内的最小实现转绿。
- Step 2 仅补齐 README 和 release plan 的真实发布边界，没有修改或放宽测试；10 项契约全部
  转绿，完整离线门禁为 `95 passed, 1 skipped`。现有 manifest 已符合身份/最小范围，无需改动。
- Step 3 重新核验官方 latest/tag、Windows AMD64 asset digest、固定二进制版本和 schema `$id`；
  唯一一次联网 `validate` 返回退出码 0，manifest SHA-256 与 Git 状态前后不变。该证据只证明
  当前 manifest 可被 Registry validator 接受，不证明已认证或发布。
- Step 4 独立 QA 将 11 个已跟踪差异和 2 个未跟踪文件全部纳入；冻结 manifest 的规范化
  JSON SHA-256 `7363235e...e39f0d` 并由契约检查，避免 CRLF/缩进差异。公开 PyPI marker、
  两个制品和 Terms 只读复核通过；完整离线结果为 `95 passed, 1 skipped`。用户 UAT 仍是
  独立门禁；用户已明确确认通过，Step 4 因而完成，但不授权 Git/PR 或 Registry 写入。
- Step 10 将原先要求“尚未登记”的静态断言升级为发布后契约：README 必须记录精确
  Registry 身份、`active` 和官方 API 复验，CHANGELOG 必须记录 0.1.0 的 Registry 状态，
  release plan 必须记录单次 publish、公开复验和官方 logout。先运行得到
  `5 failed, 25 passed`，五个失败均精确命中旧发布叙述；修正后定向契约为 `30 passed`，
  完整离线门禁为 `96 passed, 1 skipped`。项目外重建的 wheel/sdist 也通过更新后的制品检查器。

## 独立审查

F-001 Step 6 曾完成一次独立 QA/差异审查，覆盖全部已跟踪和未跟踪文件，重点复核错误语义、stdio stdout 污染、任意 URL 风险、fixture 与 live 结论混淆，以及 README 是否夸大发布状态。该段是 F-001 历史记录；F-002 的独立 QA/UAT 证据见上文及 `docs/evidence.md`。
