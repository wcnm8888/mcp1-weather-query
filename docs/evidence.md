# 验收证据索引

## F-001 / Step 0

日期：2026-08-11

### 项目与 Git 前置事实

- 操作：列出项目文件，执行 Git worktree 探测。
- 结果：Step 0 前仅有 9 份 Markdown 规划文档，目录不是 Git 仓库，无源码、依赖、分支或远程。
- 结论：符合“启动新项目”和用户授权的本地 Git 初始化前提。

### uv 能力

- 命令摘要：`uv --version`、`uv python install --help`。
- 结果：Cherry Studio 管理的 uv 0.6.14 支持 managed Python 安装；未更新或覆盖该可执行文件。
- Step 1 结果：现有 uv 成功完成依赖解析、锁定和同步，无需更换 uv。

### Python 3.12 基线

- 环境边界：`UV_PYTHON_INSTALL_DIR` 和 `UV_CACHE_DIR` 临时指向项目 `.runtime/`，未设置全局环境变量。
- 操作摘要：安装 Python 3.12；使用 `uv python find --managed-python --no-python-downloads 3.12` 查找；直接运行解释器 `--version`。
- 结果：找到项目内 CPython 3.12.10，解释器报告 `Python 3.12.10`。
- 异常说明：首次前台安装命令因工具 64 秒上限中断；续行完成后以 managed-python 查找和解释器版本进行最终验证，未把超时写成成功。
- 风险：系统注册表仍残留一个不存在的 Python 3.12 路径；项目通过 `--managed-python` 和项目安装目录绕开，未修改注册表。

### 文档与敏感信息

- 操作：检查文档入口、任务卡状态、相对链接、非 Markdown 业务产物和常见敏感信息模式。
- 预期：Step 0 只有基线/状态文件，无业务代码或凭证。
- 结果：通过；最终 Git diff 和 staged diff 在基线提交前再次检查。

### Git 基线

- 范围：本文件所在的 root baseline commit，以及由其创建的 `feat/f-001-local-weather-tool`。
- 复现：`git log --oneline --decorate -n 3`、`git status --short --branch`、`git remote -v`。
- 预期：`main` 与功能分支起点一致；当前位于功能分支；无远程；工作树干净。
- 结果：由 Step 0 最终 Git 验证确认，提交哈希以 Git 事实为准，不在提交内容中自引用。

## F-001 / Step 1

日期：2026-08-11

### SDK 与依赖锁

- 官方核验：PyPI 当前稳定版为 `mcp 2.0.0`，SDK v2 将 v1 `FastMCP` 重命名为 `MCPServer`。
- 声明：Python `>=3.12,<3.13`；直接依赖 `mcp>=2,<3`、`httpx>=0.28,<1`、`pydantic>=2.12,<3`。
- 操作：`uv lock --python 3.12`、`uv sync --locked --python 3.12`、`uv lock --check`。
- 结果：通过；锁定 46 个包，项目环境使用 Python 3.12.10、`mcp 2.0.0`、`httpx 0.28.1`、`pydantic 2.13.4`。
- 边界：`.venv/` 与 `.runtime/` 均被 Git 忽略；未更新 Cherry Studio uv。

### 工程骨架质量

- `uv run --locked ruff format --check .`：通过，23 个文件已格式化。
- `uv run --locked ruff check .`：通过。
- `uv run --locked mypy`：通过，11 个源码/测试文件无问题。

### 红灯契约测试

- 命令：`uv run --locked pytest -q --tb=short`。
- 结果：按预期 `15 failed`，退出码 1；0 个收集/导入/环境错误。
- 失败边界：输入规范化与拒绝、稳定错误与 retryable、两个固定 HTTPS endpoint、结构化输出模型。
- 结论：这是有效 RED 阶段证据，不是通过结论；Step 2 才能使相关边界转绿。
- fixture：仅为 synthetic/offline 测试数据，不代表 live API 证据。

## F-001 / Step 2

日期：2026-08-11

### Open-Meteo 契约

- 官方核验：地理编码使用固定 `/v1/search`、`name`、可选 `countryCode` 和 `count=1`；current conditions 基于 15 分钟天气模型数据。
- 天气请求：固定 `/v1/forecast`，仅请求 8 个 current variables，显式使用 Celsius、km/h、mm 和解析地点时区。
- 安全边界：两个固定 HTTPS host、10 秒总超时/5 秒连接与连接池超时、禁止重定向、无重试、无调用方 URL。

### 离线自动化验证

- `uv run --locked pytest -q --tb=short`：`41 passed in 1.65s`。
- 覆盖：输入 trim/大写/拒绝、结构化模型、6 个错误码、WMO、固定 endpoint、恶意 URL 形态输入、服务编排和成功转换。
- 失败路径：无结果、400、429、503、读取超时、连接失败、坏 JSON、非对象 JSON、缺字段、错误单位、错误时区、未知 WMO code、天气请求超时。
- `uv run --locked ruff format --check .`：通过，28 个文件已格式化。
- `uv run --locked ruff check .`：通过。
- `uv run --locked mypy`：通过，16 个源码/测试文件无问题。
- `uv lock --check`：通过。

### 证据边界

- 全部 HTTP 测试使用 `httpx.MockTransport` 和 synthetic fixture，不声称 Open-Meteo live 可用。
- 未创建 MCP server/Tool，未执行协议、stdio、Inspector、构建或发布验证。

## F-001 / Step 3

日期：2026-08-11

### 官方 SDK v2 契约

- 使用 `mcp.server.MCPServer` 与 `@server.tool(...)` 注册 Tool；没有沿用 v1 `FastMCP` 示例。
- Pydantic 返回模型由 SDK 生成 `outputSchema` 和 `structuredContent`，成功结果没有自造 `result` 包装层。
- 已声明 `readOnlyHint=true`、`destructiveHint=false`、`idempotentHint=true`、`openWorldHint=true`。
- 业务/上游失败抛出普通异常，由 SDK 表现为 `isError=true` 的 Tool execution error；意外内部异常转换为通用 MCP `INTERNAL_ERROR`。

### 内存协议与质量门禁

- `uv run --locked pytest -q --tb=short`：最终复核为 `48 passed in 1.43s`。
- MCP 覆盖：只发现一个 Tool；resources/prompts 为空；输入/输出 Schema、描述、annotations、成功结构化结果、无效输入、地点无结果和意外内部异常均通过。
- `uv run --locked ruff format --check .`：通过。
- `uv run --locked ruff check .`：通过。
- `uv run --locked mypy`：通过，18 个源码/测试文件无问题。
- `uv lock --check`：通过。

### 启动边界与未覆盖范围

- 已建立 `python -m mcp_weather_query` 模块入口；仅通过导入 `main` 和 `MCPServer` 对象验证入口可解析，没有调用 `main()`，没有启动 stdio 子进程。
- 因 F-001 不打包且 `tool.uv.package = false`，裸 `uv run ... import mcp_weather_query` 会得到预期的 `ModuleNotFoundError`；显式设置项目 `src` 的绝对 `PYTHONPATH` 后导入成功。精确 Host 命令留到 Step 4 验证。
- 全部 MCP 调用使用注入的离线 handler，没有访问 Open-Meteo live API。
- 未运行真实 stdio、Inspector、构建、打包、提交或发布。

## F-001 / Step 4

日期：2026-08-11

### 官方 stdio 契约与红灯

- 官方 SDK v2 核验：客户端使用 `StdioServerParameters`、`stdio_client()` 和 `ClientSession.initialize()`；上下文退出负责关闭 stdin、限时等待并清理进程树。
- 官方日志边界：stdio Server 的 stdout 属于 MCP 协议，标准日志应写 stderr。
- 红灯命令：只运行确定性 stdio Tool call；结果为 `1 failed, 1 deselected`，原因是测试专用固定 Server 尚不存在而连接关闭，不是网络或测试收集错误。
- 最小实现：新增 `tests/smoke/stdio_fixed_server.py`，通过 `create_server()` 注入 synthetic fixture；不修改生产 Tool 契约，不访问 HTTP。
- 首次局部门禁发现 Ruff `SIM117`（嵌套异步上下文）和单独运行 `mypy tests/smoke` 时 `src` 包不可发现；分别合并上下文并声明 `mypy_path = "src"` 后，局部与全量门禁均通过。这两项不是协议或网络失败。

### 真实子进程验证

- 生产入口：项目虚拟环境 Python + `-m mcp_weather_query`，工作目录为项目根目录，子进程环境显式设置绝对 `PYTHONPATH` 指向 `src`。
- 原始协议：发送 initialize、initialized notification 和 tools/list；只发现 `get_current_weather`。
- 关闭：关闭 stdin 后进程在 10 秒内以退出码 0 结束；`finally` 会终止异常残留进程。
- stdout：预期响应逐行通过 JSON 解析，读取预期响应后剩余 stdout 为 0 字节。
- stderr：生产入口无 traceback；测试专用诊断标记由官方 client 捕获在 stderr。
- 确定性调用：官方 `stdio_client` + `ClientSession` 对测试专用 Server 调用 Tool，返回无 `result` 包装层的合法 structuredContent，地点和国家代码规范化为 `北京`/`CN`。

### 全量离线门禁

- `uv run --locked pytest -q --tb=short`：最终复核为 `50 passed in 5.94s`。
- `uv run --locked ruff format --check .`：通过，32 个文件已格式化。
- `uv run --locked ruff check .`：通过。
- `uv run --locked mypy`：通过，20 个源码/测试文件无问题。
- `uv lock --check`：通过，仍锁定 46 个包。
- 为支持独立检查 smoke 目录，在 mypy 配置中显式声明 `mypy_path = "src"`；未新增依赖。

### 证据边界

- production discovery 不调用 Tool；确定性 Tool call 只读取 synthetic fixture，因此没有 Open-Meteo live 请求。
- 测试专用 Server 位于 `tests/smoke/`，不是生产、Host 配置或未来发布入口。
- 未运行 Inspector、live API、构建、打包、提交或发布。

## F-001 / Step 5

日期：2026-08-11

### 官方契约复核

- MCP Inspector 官方文档确认可用 `npx @modelcontextprotocol/inspector <command> <args>` 启动本地 stdio Server；本次固定使用 Registry 当日版本 `@modelcontextprotocol/inspector@2.1.0`，没有全局安装。
- MCP Python SDK v2 文档确认 `MCPServer.run()` 默认使用 stdio；Inspector 连接生产模块入口，不使用 FastMCP v1、SSE 或 Streamable HTTP。
- Open-Meteo 官方 geocoding/forecast 文档再次确认 `name`、可选 `countryCode`、坐标驱动 current weather 和模型数据语义；免费非商业层仍有每日限额、无 SLA 和 CC BY 4.0 署名要求。

### live contract

- 新增 `tests/integration/test_open_meteo_live.py`；未设置 `MCP_WEATHER_RUN_LIVE` 时结果为 `1 skipped`，不联网。
- 第一次显式运行在发出请求前因系统 `ALL_PROXY` 指向 SOCKS 且环境没有 `socksio` 失败。诊断只记录代理类型，不记录地址或凭证。
- 使用 `trust_env=False` 对固定允许 endpoint 直连后，中文 `北京` + `CN` 得到 HTTP 200 但没有候选；改用任务允许的稳定非敏感输入 `Beijing` + `CN`。
- 生产默认 HTTP client 同步设置 `trust_env=False`，并新增回归测试证明不继承环境代理；没有引入 SOCKS 依赖，没有更改系统代理。
- 显式命令：设置 `MCP_WEATHER_RUN_LIVE=1` 后运行该测试；实际为 `1 passed in 3.37s`，只执行一次 geocoding 和一次 forecast 请求，无重试。
- 断言覆盖：两个固定 HTTPS endpoint、请求地点/国家代码、解析地点、坐标/时区、current weather 模型、单位、provider、attribution 和 license；没有保存完整 live 响应。

### MCP Inspector

- 裸 `npx --yes @modelcontextprotocol/inspector` 意外解析为已弃用的 1.0.1，立即停止且不作为证据；随后固定为 `@modelcontextprotocol/inspector@2.1.0`。
- Inspector 2.1.0 声明 Node `>=22.19`，本机 Node 22.16.0 产生 npm engine warning；未升级 Node。尽管如此，本次 Web UI、stdio 连接、discovery 和调用均成功。
- 首次 v2 启动未显式传源码路径，生产子进程报 `No module named mcp_weather_query`；使用 `--web -e PYTHONPATH=<项目 src> --cwd <项目目录> <项目 Python> -m mcp_weather_query` 后连接成功。
- initialize 成功；Inspector 显示 Server `mcp-weather-query`，只发现 `get_current_weather`。Tool 描述、Location/Country Code 输入、`read-only`、`idempotent`、`open-world` 标记可见；destructive 为 false。
- 成功路径：`Beijing` + `CN` 返回通过输出契约的结构化结果，包含 requested/resolved location、current weather 和 Open-Meteo 来源/许可证元数据。
- 错误路径：`A` + `CN` 返回 Tool Error，稳定语义为 `INVALID_LOCATION`、`retryable=false` 和修正提示；没有 traceback 或本机绝对路径。
- Inspector 客户端本次协商显示 MCP `2025-11-25`，低于项目 SDK 支持的 `2026-07-28`；本次功能验证不受影响，但作为 Inspector 客户端兼容事实保留。
- 浏览器会话、Inspector、MCP 子进程和本地监听端口均已关闭；临时认证令牌已失效且未写入项目文档。

### 最终离线门禁

- `uv lock --check`：通过，继续复用 uv 0.6.14。
- `uv run ruff format --check .`：通过，33 个文件已格式化。
- `uv run ruff check .`：通过。
- `uv run mypy`：通过，21 个源码/测试文件无问题。
- 清除 live opt-in 后执行 `uv run pytest -q --tb=short`：`51 passed, 1 skipped in 4.10s`；唯一 skip 是显式 live contract。
- 范围结果：唯一 Tool、固定域名、无 HTTP/SSE 传输、无普通 stdout `print`、无第二 Tool；未构建、打包、提交、push、创建 PR 或发布。

### Step 5 兼容性修复与复验

- [Node 官方版本目录](https://nodejs.org/download/release/latest-v24.x/)核验：Node 24 为 LTS；执行时 `latest-v24.x` 为 24.19.0，官方目录提供 `node-v24.19.0-win-x64.zip` 与 `SHASUMS256.txt`。
- 项目独立环境：解压到 `.runtime/node/node-v24.19.0-win-x64/`；Node 24.19.0、npm/npx 11.17.0。ZIP SHA256 为 `57f71ab3652e797d84acddc79c81cc9ff1c6ddb2a1974cdb83f00fee9bff4c73`，与官方清单一致。
- 系统边界：系统 `node --version` 复核仍为 22.16.0；未修改系统 PATH、注册表、系统 Python、Cherry Studio uv 或用户级全局环境。
- npm Registry 元数据：`@modelcontextprotocol/inspector` latest 为 2.1.0，`engines.node` 为 `>=22.19.0`；`v1-latest=1.0.1`、`latest=2.1.0`。
- 独立 Node 首次 `npx` 启动花费较长时间并出现一次 npm peer dependency `ERESOLVE` warning；最终 Inspector 正常监听。该 warning 不是 engine warning，也没有改变项目依赖或 `uv.lock`。
- 进程事实：Inspector launcher 的 `ExecutablePath` 指向项目 `.runtime/node/.../node.exe`；stderr 中没有 `EBADENGINE`、unsupported engine 或 engine incompatibility，Node 兼容问题已解决。
- [MCP 2026-07-28 官方说明](https://blog.modelcontextprotocol.io/posts/2026-07-28/)：新规范已移除 `initialize/initialized` 和 session；现代请求自行携带版本/身份/能力，可选 `server/discover`。因此“initialize 请求/响应等于 2026-07-28”不是有效的现代协议验收条件。
- [Python SDK v2 官方说明](https://github.com/modelcontextprotocol/python-sdk/blob/main/docs/whats-new.md)：SDK 同时服务 2026 现代客户端和 2025 Legacy 客户端；旧客户端发起 initialize 时，Server 进入兼容路径。
- Inspector 官方 2.1.0 发布包 README 将 `protocolEra: auto|modern`、`server/discover` 和 sessionless 现代路径说明为 Streamable HTTP；stdio 作为真实子进程路径单独存在，没有现代 stdio 配置说明。
- 真实复验：项目独立 Node + Inspector 2.1.0 + 生产 stdio 入口连接成功；UI 显示 `MCP 2025-11-25` 和 `Legacy`。展开 initialize 后，Client 请求 `protocolVersion=2025-11-25`，Server 响应同为 `2025-11-25`，随后发送 `notifications/initialized`。
- 停止结论：当前稳定 Inspector 无法在本项目批准的 stdio-only 边界内提供 2026-07-28 现代协议证据；启用 Streamable HTTP 会扩大架构范围。按授权停止条件，本轮没有继续 Tool live 成功/错误复验，没有修改 Python SDK、`uv.lock`、Tool 契约或传输。
- 清理：Playwright、Inspector、MCP 和 Node 子进程全部关闭；6274/6277/26737 监听数为 0；临时认证 Token 已从运行日志脱敏。
- 停止后的离线门禁：`uv lock --check`、Ruff format、Ruff lint、严格 mypy 通过；pytest 为 `51 passed, 1 skipped in 7.68s`。唯一 Tool、无普通 stdout print、无 HTTP/SSE 传输和固定 endpoint 扫描通过。

### Step 5 现代 stdio 协议证据补充

- 用户选择保持 stdio，并使用官方 Python SDK v2 `Client` 补充 MCP 2026-07-28 证据；不要求 Inspector Legacy UI 冒充现代客户端。
- 红灯诊断：旧 `ClientSession.initialize()` 对测试专用 stdio Server 得到 `observed=2025-11-25; expected=2026-07-28` 并按预期断言失败，证明旧测试路径只能覆盖 handshake-era 协议。
- 最小测试调整：原始 initialize smoke 改为显式使用 SDK 的 `LATEST_HANDSHAKE_VERSION` 并断言 Server 返回相同 Legacy 版本；新增 `Client(stdio_client(...), mode="auto")` 现代路径。
- 生产入口现代 discovery：SDK Client 对 `python -m mcp_weather_query` 的真实 stdio 子进程先执行 `server/discover`；`client.protocol_version` 为 `2026-07-28`，`discover_result` 存在、`initialize_result` 为空，且 `tools/list` 只发现 `get_current_weather`。
- 确定性现代调用：同一 SDK Client 对测试专用 stdio Server 调用唯一 Tool，返回合法 structuredContent 并通过 `CurrentWeatherResult` 校验；只读取 synthetic fixture，没有访问 Open-Meteo。
- 局部转绿：`tests/smoke/test_stdio_subprocess.py` 为 `3 passed in 7.41s`；首次 Ruff format check 真实报告文件需要格式化，执行 Ruff format 后转绿。
- 全量门禁：`uv lock --check`、Ruff format check、Ruff lint、严格 mypy 全部通过；默认离线 pytest 为 `52 passed, 1 skipped in 8.25s`，唯一 skip 是显式 live contract。
- 结论：同一生产 Server 的现代 SDK Client stdio 路径使用 MCP 2026-07-28，Inspector stdio 路径使用 Legacy MCP 2025-11-25；这是 SDK v2 的双协议兼容能力，不需要 HTTP、依赖升级或生产代码修改。

## F-001 / Step 6 QA

日期：2026-08-11

### 审查范围与发现

- 使用 `git status --short`、`git diff`、`git ls-files --others --exclude-standard` 和 `rg --files` 枚举并审查全部已跟踪及未跟踪源码、测试、fixture、配置和文档；没有只依赖普通 diff。
- Tool/协议复核：源码仅有一个 `@server.tool`，名称为 `get_current_weather`；input/output Schema、四个 annotations、structuredContent 和稳定 Tool execution error 与任务卡一致。
- 网络/安全复核：生产源码仅含两个固定 Open-Meteo HTTPS endpoint 和 CC BY 4.0 license URL；无任意 URL、HTTP/SSE 传输、Shell、文件写入或普通 stdout `print`。
- `uv tree --locked` 显示 `sse-starlette`/`uvicorn` 是官方 `mcp` SDK 的传递依赖；项目源码没有导入或启用它们，实际生产入口仍只有 stdio。
- 敏感信息扫描只命中测试中的 synthetic `secret-upstream-body` 负向样本和文档中的禁止/未来发布说明，没有真实凭证。
- 没有高、中优先级范围内缺陷。修正一处包级说明中“transport 尚未建立”的陈旧事实，并同步 Step 6 状态、实际结构化输出和当前门禁文档。
- 运行态审查发现 PID 36956 是指向项目 `.runtime/npm-cache` 的孤立 Playwright CLI daemon，父进程已不存在；停止该进程后复核没有项目 Python/uv/Node 子进程残留。未触碰用户编辑器或其他项目进程。

### 默认离线门禁

- Step 6 QA 当时的环境：`uv --version` 为 `uv 0.6.14`，项目解释器为 `Python 3.12.10`，分支为 `feat/f-001-local-weather-tool`，尚无 Git remote；后续远程和合并事实见下方 GitHub 交付证据。
- `uv lock --check`：通过，解析 46 个包。
- `uv run ruff format --check .`：通过，33 个文件已格式化。
- `uv run ruff check .`：通过。
- `uv run mypy`：通过，21 个源码/测试文件无问题。
- Git 交付前清除 `MCP_WEATHER_RUN_LIVE` 并执行 `uv run pytest -q --tb=short`：`52 passed, 1 skipped in 5.51s`；唯一 skip 是显式 live contract。
- `git diff --check`：无空白错误；Git 仅提示现有 LF 文件未来可能按 Windows 配置转换为 CRLF。
- Step 6 QA 执行过程未联网、未运行 Inspector、未构建或打包；该阶段收口时只形成了本地提交，远程、push 和 PR 事实记录在后续 GitHub 交付证据中。

## GitHub 交付与未完成证据

- F-001 Step 5 协议对齐：现代/Legacy 两条 stdio 证据已完成。
- F-001 Step 5 用户 UAT：用户于 2026-08-11 明确确认通过。
- F-001 Step 6 独立 QA：已完成；用户已选择远程 PR 流程并形成精确本地提交，提交哈希以 Git 事实为准。
- GitHub 远程：通过已认证账号 `wcnm8888` 创建 private 仓库 `wcnm8888/mcp1-weather-query`，配置 HTTPS `origin`，成功推送 `main` 和 `feat/f-001-local-weather-tool`。
- PR 创建：GitHub App 因新 private 仓库尚未进入安装可见范围返回 404；按 `github:yeet` fallback 使用已认证 GitHub CLI 创建 draft PR #1，没有重复 PR。
- PR 创建时复核：`main` ← `feat/f-001-local-weather-tool`，状态 OPEN、draft、MERGEABLE；URL 为 `https://github.com/wcnm8888/mcp1-weather-query/pull/1`。这是 PR 创建时的历史证据，不代表当前状态。
- 后续由用户将 PR #1 标记 ready 并成功合并、关闭；合并提交为 `514b3a987a3e`（短哈希 `514b3a9`）。
- 本地同步：执行 `git fetch origin`、`git switch main` 和 `git pull --ff-only origin main`，本地 `main` 从基线 `b13d9bd` fast-forward 到 `514b3a9`，与 `origin/main` 一致。
- 合并后文档收口：从 `514b3a9` 创建 `docs/f-001-post-merge`，仅承载 F-001 最终关闭状态，并按用户授权通过独立文档 PR 交付到 `main`。
- 合并后离线复验：清除 `MCP_WEATHER_RUN_LIVE` 后，`uv lock --check`、Ruff format check、Ruff lint、严格 mypy、`git diff --check` 均通过；最终 `pytest` 为 `52 passed, 1 skipped in 8.50s`，唯一 skip 仍是显式 live contract。
- 分支清理：在 `git merge-base --is-ancestor feat/f-001-local-weather-tool main` 返回 0 后，删除远程和本地 `feat/f-001-local-weather-tool`；合并内容仍由 `main` 的 `514b3a9` 保留。
- F-001 已关闭；未创建 release、未执行其他发布，也未自动进入 F-002。
- 构建、打包、干净安装和发布不属于 F-001，且无通过结论。

## F-002 / Step 0 任务与构建基线

日期：2026-08-11

### Git 与文档基线

- Step 开始前工作树干净，`main` 与 `origin/main` 均为 `4d84ad07c1d45ee84446879947cd9051cc0356ec`。
- 从该提交创建本地 `feat/f-002-installable-package`；本 Step 未 commit、push、创建 PR 或修改远程。
- F-001 完整任务卡归档到 `docs/archive/task-cards/F-001-一个-Tool-的本地天气闭环.md`。
- F-002 已成为唯一活动任务卡；任务状态为 Step 0 已完成、等待 Step 1 用户门禁。

### 环境与兼容边界

- `uv --version`：`uv 0.6.14 (a4cec56dc 2025-04-09)`。
- 项目解释器：`Python 3.12.10`。
- `uv help build` 明确列出 PEP 517、`--sdist` 和 `--wheel`，证明现有 uv 具备所需构建前端能力。
- Step 0 没有执行 `uv build`，也没有实际调用候选 `uv_build` 后端；因此具体后端版本兼容性尚未验证。若后续必须升级 uv，应停止并提交 E 盘独立 uv 方案，不覆盖 Cherry Studio 管理的 uv。

### 默认离线门禁

- 清除 `MCP_WEATHER_RUN_LIVE` 后，`uv lock --check` 通过，解析 46 个包。
- `uv run ruff format --check .`：通过，34 个文件已格式化。
- `uv run ruff check .`：通过。
- `uv run mypy`：通过，21 个源码/测试文件无问题。
- `uv run pytest -q --tb=short`：`52 passed, 1 skipped in 8.92s`；唯一 skip 是显式 live contract，未访问 Open-Meteo。
- `git diff --check`：通过；只有现有 Windows 行尾转换提示，没有空白错误。

### Step 0 范围结论

- 没有修改 `pyproject.toml`、`uv.lock`、源码、测试、LICENSE 或 NOTICE。
- 没有构建 wheel/sdist，没有创建 `dist/` 或干净安装环境。
- 没有运行 live API、Inspector、HTTP/SSE、第二 Tool、外部发布或系统环境更新。

## F-002 / Step 1 packaging 红灯契约

日期：2026-08-11

### 规范依据

- [uv build backend 官方文档](https://docs.astral.sh/uv/configuration/build-backend/)：纯 Python `src` layout 可使用 `uv_build`；后端要求应有上界，当前兼容系列为 `>=0.11.x,<0.12`。
- [uv 项目配置官方文档](https://docs.astral.sh/uv/concepts/projects/config/)：console command 使用 `[project.scripts]`，且项目需要显式 build system；`tool.uv.package=false` 会强制禁止项目包安装。
- [PyPA pyproject.toml 规范](https://packaging.python.org/en/latest/specifications/pyproject-toml/)：`license` 使用 SPDX 字符串，`license-files` 可列出许可证和其他法律声明。

### 新增契约

- `tests/packaging/test_project_contract.py` 静态读取 `pyproject.toml`，不调用构建后端。
- 固定 distribution `mcp-weather-query`、import package `mcp_weather_query`、console command `mcp-weather-query` 和 target `mcp_weather_query.__main__:main`。
- 要求版本 `0.1.0`、显式且有界的 `uv_build`、取消 source-only override、SPDX `MIT`、根目录 LICENSE/NOTICE。
- 定义 Step 3 的 wheel/sdist 双制品矩阵和 Step 4 的 wheel-env/sdist-env 双隔离安装矩阵；两种安装均禁止 editable install 和 `PYTHONPATH`。

### 红灯与回归结果

- `uv run pytest -q --tb=short tests\packaging\test_project_contract.py`：`6 failed, 4 passed`，退出码 1，符合预期。
- 六个失败分别证明：`package=false`、缺 `[build-system]`、版本仍为 `0.0.0`、缺 `[project.scripts]`、缺许可证元数据、缺 LICENSE/NOTICE。
- 完整 `uv run pytest -q --tb=short`：`6 failed, 56 passed, 1 skipped in 8.34s`；不得写成全量通过。
- 排除新增红灯后的既有回归：`52 passed, 1 skipped in 7.96s`；唯一 skip 仍是显式 live contract。
- `uv lock --check`、Ruff format check、Ruff lint、严格 mypy 和 `git diff --check` 通过。

### 范围结论

- 未修改 `pyproject.toml`、`uv.lock`、生产源码或 Tool 契约。
- 未创建 LICENSE/NOTICE、build/dist、wheel/sdist 或干净安装环境。
- 未访问 live API、运行 Inspector、更新环境、commit、push、创建 PR 或发布。

## F-002 / Step 2 最小 packaging 配置

日期：2026-08-11

### 配置依据与实现

- [uv 当前项目初始化文档](https://docs.astral.sh/uv/concepts/projects/init/)给出的当前纯 Python backend 范围为 `uv_build>=0.11.32,<0.12`；项目采用该有界范围和默认 `src/mcp_weather_query` 发现规则。
- [uv build backend 文档](https://docs.astral.sh/uv/configuration/build-backend/)确认 `project.license-files` 会进入 sdist，并复制到 wheel `.dist-info`；实际制品内容留在 Step 3 验证。
- [Open-Meteo 官方许可页](https://open-meteo.com/en/license)要求适当署名、许可证链接和变更说明；README/NOTICE 已注明 Open-Meteo、CC BY 4.0 和字段规范化边界。
- `pyproject.toml` 版本设为 `0.1.0`，注册 `mcp-weather-query = "mcp_weather_query.__main__:main"`，使用 SPDX `MIT` 和 `license-files = ["LICENSE", "NOTICE"]`。
- 根目录 LICENSE 使用 MIT 标准文本；NOTICE 只说明第三方天气/地理编码数据许可，不改变项目代码 MIT License。

### 锁文件与后端兼容性

- 修改前 `uv lock --check` 退出码为 2，并明确要求更新锁文件。
- 执行一次 `uv lock` 后，根项目仅从 `version = "0.0.0" / source = { virtual = "." }` 更新为 `version = "0.1.0" / source = { editable = "." }`；解析包数量仍为 46。
- 后续 `uv lock --check` 通过。
- uv 0.6.14 成功调用声明的 `uv_build` 后端并把项目安装到现有项目虚拟环境；`.venv\Scripts\mcp-weather-query.exe` 存在，无需更新或覆盖 Cherry Studio uv。
- 项目环境 console command 在 stdin 关闭时以退出码 0 结束；本 Step 不把该结果冒充项目外安装或完整 stdio 协议证据。

### 绿灯与回归结果

- 修改生产配置前，Step 1 定向契约为 `6 failed, 4 passed`。
- 修改后 `uv run pytest -q --tb=short tests\packaging\test_project_contract.py`：`10 passed`。
- 完整默认 `uv run pytest -q --tb=short`：`62 passed, 1 skipped in 8.01s`；唯一 skip 是显式 live contract。
- `uv run ruff format --check .`、`uv run ruff check .` 和严格 `uv run mypy` 通过，覆盖 35 个格式文件和 22 个类型检查文件。
- `git diff --check` 通过；只有现有 Windows 行尾转换提示。

### 范围结论

- 没有修改 MCP Tool、领域逻辑、Open-Meteo 适配器或 stdio 生产入口。
- 没有执行 `uv build`；根目录不存在 `dist/` 或 `build/`，没有 wheel/sdist。
- 没有创建项目外临时环境、访问 live API、运行 Inspector、commit、push、PR 或发布。

## F-002 / Step 3 真实构建与制品审查

日期：2026-08-11

### 构建结果

- `uv build` 使用现有 uv 0.6.14 成功执行：先构建 source distribution，再从该 sdist 构建 wheel。
- sdist：`mcp_weather_query-0.1.0.tar.gz`，10,955 bytes，SHA-256 `a29536321c24912553051cd96c416a83c44f120724c265010f0363d4fcee7c25`。
- wheel：`mcp_weather_query-0.1.0-py3-none-any.whl`，15,406 bytes，SHA-256 `2fa3f09f5c1f7a6c6d7075e408159b8ef31d2f00b5aeb7bea5607e3bc328579c`。
- `dist/` 由现有 `.gitignore` 明确忽略；`git ls-files dist build` 为空，制品没有进入待提交文件。

### 自动制品门禁

- 新增 `tests/packaging/inspect_artifacts.py`，只读检查真实归档，不提取或安装制品。
- wheel 精确包含 15 个文件：9 个生产 Python 文件、LICENSE/NOTICE、WHEEL、entry_points、METADATA 和 RECORD；不含 tests、fixture、docs、缓存、日志或本机配置。
- sdist 精确包含 14 个文件：9 个生产 Python 文件、PKG-INFO、pyproject、README、LICENSE 和 NOTICE；不含缓存、日志、临时制品或私有配置。
- METADATA/PKG-INFO：Metadata-Version 2.4、Name `mcp-weather-query`、Version `0.1.0`、License-Expression `MIT`、两个 License-File、三个批准的 Requires-Dist 和 `Requires-Python: >=3.12, <3.13`。
- entry point 精确为 `mcp-weather-query = mcp_weather_query.__main__:main`；wheel 为 `Root-Is-Purelib: true` 和 `py3-none-any`。
- 对 wheel RECORD 逐项复算 SHA-256 和文件大小，覆盖集合与归档文件集合完全一致。
- wheel/sdist 中的生产源码和法律文件与工作树逐字节一致。
- 制品内容不含工作区/用户目录绝对路径、`.runtime`、`.venv` 或明显凭据赋值。

### 构建过程发现与修复

- 初次制品内嵌的是构建前 README，仍声明等待 Step 3；自动门禁加入 Step 3/4 状态检查后拒绝该陈旧制品。
- 更新 README 并重新运行 `uv build` 后，sdist 和 wheel 均嵌入真实 Step 3 状态。
- 审查脚本最初对 Windows 生成的 entry point 换行要求过窄，随后统一 CRLF/LF 后再比较；另将内嵌状态检查改为稳定 ASCII Step 标记，避免 email parser 对非 ASCII payload 表示造成假失败。
- 最终 `python tests\packaging\inspect_artifacts.py dist` 退出码 0，并输出上述安全摘要。

### 回归和范围结果

- `uv lock --check`、Ruff format check、Ruff lint、严格 mypy 和 `git diff --check` 通过；Ruff 检查 36 个文件，mypy 检查 23 个文件。
- 完整默认 pytest：`62 passed, 1 skipped in 7.94s`；唯一 skip 仍为显式 live contract。
- `git diff -- src` 为空；没有修改 MCP Tool、领域逻辑、Open-Meteo 适配器或生产 stdio 入口。
- 本 Step 未安装 wheel/sdist、未创建项目外环境、未访问 live API、未运行 Inspector、未上传、未发布、未 commit/push/PR。

## F-002 / Step 4 双干净安装与 installed-package stdio

日期：2026-08-11

### 环境与安装来源

- 项目外根目录：`E:\Agent\.tmp\mcp1-weather-query\f-002\step4-20260811-a`；
  执行前确认该目录不存在，本 Step 新建后按“不得删除/清理”边界原样保留。
- 使用现有 uv 0.6.14 和项目 CPython 3.12.10 创建相互独立的 `wheel-env` 与
  `sdist-env`，工作目录分别为 `wheel-work` 与 `sdist-work`，均位于项目外。
- `uv pip install --python <wheel-env-python> <absolute-wheel>` 成功直接安装
  `mcp_weather_query-0.1.0-py3-none-any.whl`。
- `uv pip install --python <sdist-env-python> <absolute-sdist>` 成功从
  `mcp_weather_query-0.1.0.tar.gz` 隔离构建并安装；两套环境均安装
  `mcp-weather-query==0.1.0`。
- 安装时首次解析/获取已声明的 Python 运行依赖；没有访问 Open-Meteo。uv 因缓存与
  目标文件系统不能 hardlink 而回退到完整复制，这只是性能提示，不影响安装结果。
- 两套 distribution 的 `direct_url.json` 分别精确指向上述 `.whl` 和 `.tar.gz`，
  且不存在 `dir_info`；因此不是 editable 或目录安装。
- 两套 module origin 均为各自 `Lib\site-packages\mcp_weather_query\__init__.py`，
  console origin 均为各自 `Scripts\mcp-weather-query.exe`。验证器拒绝项目 `src` 出现
  在 `sys.path`，子进程环境明确不含 `PYTHONPATH`、`PYTHONHOME` 和 `VIRTUAL_ENV`。

### stdio、Tool 与进程证据

- 新增 `tests/packaging/verify_installed_package.py`；它不进入 wheel/sdist，也不是
  console entry point。父验证器由目标干净环境自己的 Python 运行。
- 对两套生产 console 分别执行 raw Legacy stdio：`initialize(2025-11-25)`、
  `notifications/initialized`、`tools/list` 均成功；只发现 `get_current_weather`。
- 两套 raw console 均在关闭 stdin 后 10 秒超时内以退出码 0 结束；全部 stdout
  响应可解析为 JSON-RPC，响应后没有剩余 stdout，stderr 没有 traceback。
- 对两套生产 console 分别使用官方 Python SDK v2 `Client(mode="auto")`；均通过
  `server/discover` 协商 MCP `2026-07-28`，只发现唯一 Tool，未执行天气 Tool。
- 测试专用 `serve-fixed` child 使用已安装包的 `create_server()` 和内嵌 synthetic
  数据，不读取项目 fixture、不访问网络。两套调用均返回 `is_error=false` 和合法
  `structuredContent`；`CurrentWeatherResult` 校验通过，无额外 `result` wrapper，
  地点/国家代码规范化仍为“北京”/`CN`。
- fixed child 的诊断标记只出现在 stderr；生产现代 stderr 文件为空，四个日志均无
  traceback。检查命令排除自身 PowerShell 后，没有包含 Step 4 目录的遗留子进程。

### 离线回归与范围

- `uv lock --check` 通过，锁定 46 个包。
- `uv run ruff format --check .`：37 个文件均已格式化；`uv run ruff check .` 通过。
- 严格 `uv run mypy`：24 个 source files 无问题。
- 清除 `MCP_WEATHER_RUN_LIVE` 后完整 pytest：`62 passed, 1 skipped in 8.14s`；唯一
  skip 是显式 live contract，没有意外网络请求。
- `python tests\packaging\inspect_artifacts.py dist` 再次通过；安装的是 Step 3 已审查
  的精确制品：sdist SHA-256
  `a29536321c24912553051cd96c416a83c44f120724c265010f0363d4fcee7c25`，wheel
  SHA-256 `2fa3f09f5c1f7a6c6d7075e408159b8ef31d2f00b5aeb7bea5607e3bc328579c`。
- `git diff --check` 通过；只有既有 Windows LF→CRLF 提示。
- 生产源码仍恰好一个 `@server.tool`、没有普通 `print`，Open-Meteo 仍为两个固定
  HTTPS endpoint；未新增 Tool、HTTP/SSE、写操作或任意 URL。
- 未运行 live API 或 Inspector，未更新 uv/Python/Node/系统环境，未重建制品，未
  commit、push、创建 PR、上传或发布。

### 当前结论

F-002 Step 4 验收通过，等待用户明确允许进入 Step 5 独立 QA 与用户 UAT。本结论
只证明本地制品可在两个项目外独立环境安装并运行，不代表已发布或已完成 Git 交付。

## F-002 / Step 5 独立 QA（用户 UAT 待确认）

日期：2026-08-11

### 独立审查范围

- 审查分支 `feat/f-002-installable-package` 相对 `main == origin/main == 4d84ad0`
  的完整 tracked diff，并通过 `git ls-files --others --exclude-standard` 枚举全部
  untracked 文件；没有只依赖普通 `git diff`。
- 逐项审查 `pyproject.toml`、`uv.lock`、LICENSE、NOTICE、三个 packaging 测试/
  验证文件、F-001 归档任务卡和所有受影响文档。
- `git diff -- src` 为空；Tool、领域模型、错误语义、Open-Meteo 固定适配器和
  生产 stdio 入口均未修改。
- 范围扫描确认仍只有一个 `@server.tool`、生产源码没有普通 `print`，没有新增
  Streamable HTTP/SSE、任意 URL、写操作、敏感信息或发布配置。

### QA 发现与修复

- 发现：Step 4 后根 README 已更新，而 Step 3 `dist` 制品仍内嵌旧 README；原制品
  门禁只检查 `Step 3`/`Step 4` ASCII 标记，会把陈旧长描述误判为通过。
- 修复：根 README 的包长描述部分改用稳定能力/发布边界，不再依赖临时 Step 号；
  `inspect_artifacts.py` 改为直接从 Core Metadata 原始 bytes 分离 UTF-8 body，并
  要求 wheel METADATA、sdist PKG-INFO 和 sdist README 与当前根 README 一致。
- 红灯证据：增强后的检查对旧 `dist` 返回退出码 1，错误为 embedded README 与
  current project README 不一致。
- 首次实现直接使用 Python email parser 的 payload 比较，因无 charset header 而把
  中文解码为替换字符，产生假失败；改为解码 Core Metadata 原始 UTF-8 body 后，
  既保留严格一致性，又避免编码假阴性/假阳性。

### 新 QA 候选与双安装复验

- 新项目外目录：`E:\Agent\.tmp\mcp1-weather-query\f-002\step5-20260811-a`；
  未删除、覆盖或复用 Step 4 环境和旧 `dist`。
- `uv build --out-dir <qa-artifacts>` 成功生成：
  - sdist：11,081 bytes，SHA-256
    `95efce0bce103b95765a613e89122a92e0338ecc9add644586f65fb2c4c58abf`；
  - wheel：15,535 bytes，SHA-256
    `1bdba3c8b87aca8782765d39950eb13abb6380de120905ac496e8ae4813d0fb0`。
- 两个制品的精确文件清单、Metadata-Version 2.4、名称/版本/Python/依赖、MIT、
  License-File、entry point、purelib/tag、RECORD、源码/法律文件、敏感路径和当前
  README 一致性全部通过。
- 新候选分别安装到 QA `wheel-env`/`sdist-env`；`direct_url.json` 分别证明来源为
  QA `.whl`/`.tar.gz`，module/console 均来自各自环境，不是 editable 或源码导入。
- 两套生产 console 的 raw stdio 都只发现 `get_current_weather`，stdout 仅协议消息、
  stderr 无 traceback、退出码 0；官方 SDK v2 均协商 MCP 2026-07-28。
- 两套测试专用 installed-package 调用均返回合法 `structuredContent`，诊断只在
  stderr；检查完成后没有包含 Step 5 QA 目录的遗留子进程。

### 最终自动化 QA 门禁

- `uv lock --check`：通过，解析 46 个包。
- `uv run ruff format --check .`：37 个文件通过；`uv run ruff check .`：通过。
- 严格 `uv run mypy`：24 个 source files 无问题。
- 清除 `MCP_WEATHER_RUN_LIVE` 后 `uv run pytest -q --tb=short`：
  `62 passed, 1 skipped in 7.98s`；唯一 skip 是显式 live contract。
- 对新 QA artifact directory 执行 `inspect_artifacts.py`：通过。
- `git diff --check`：通过；只有 Windows LF→CRLF 提示。
- 没有未解决的高、中优先级 F-002 范围内缺陷。

### 当前结论与未完成项

独立 QA 已通过，但用户 UAT 尚未发生，不能把 Step 5、F-002 或 Git 交付写成完成。
旧 `dist` 作为历史制品保留并明确不用于 UAT；UAT 只使用 Step 5 QA wheel 环境。
未运行 live API、Inspector，未 commit、push、创建 PR、上传或发布。

### 用户 UAT 确认

- 用户于 2026-08-11 使用给定的 Step 5 QA wheel 环境验证命令完成验收，并明确
  回复“F-002 Step 5 UAT 通过”。
- 因此 Step 5 独立 QA 与用户 UAT 均已完成；F-002 仍未关闭，下一门禁是由用户
  明确允许进入 Step 6 Git/PR 交付。
- 本次确认没有授权 commit、push、PR、外部上传或发布。

## F-002 / Step 6 Git/PR 交付

日期：2026-08-11

### 提交前事实与门禁

- GitHub CLI 2.95.0 已认证为 `wcnm8888`；remote 为 private
  `wcnm8888/mcp1-weather-query`。
- 当前分支为 `feat/f-002-installable-package`；执行 `git fetch origin main` 后，
  `main == origin/main == merge-base == 4d84ad0`，功能分支提交前与 base 无漂移。
- 完整 tracked/untracked 文件再次枚举，全部属于 F-002；生产 `src` 无 diff。
- 提交前门禁再次通过：Ruff 37 个文件、严格 mypy 24 个文件、
  `62 passed, 1 skipped in 6.76s`、锁文件、QA artifact 和 diff 检查均通过。
- 敏感词命中仅为扫描规则、历史脱敏记录及发布边界说明；没有真实凭据。没有跟踪
  `dist`、wheel/sdist、`.venv`、`.runtime` 或项目外 QA 环境。

### 精确提交与推送

- `af1f4af build(package): make weather server installable`：仅含
  `pyproject.toml`、`uv.lock`、README、MIT LICENSE 和 Open-Meteo NOTICE。
- `64e0328 test(packaging): verify build and clean installs`：仅含三个 packaging
  契约/制品/installed-package 验证文件。
- `docs(project): record F-002 draft PR delivery`：任务归档、长期文档和本次 Git/PR
  状态证据；不含生产代码或制品。
- 各提交均使用精确路径暂存，并在提交前检查 staged names/stat/diff/check；没有
  使用未经审查的 `git add -A`、强推或修改 `main`。
- 首次推送后，本地与 `origin/feat/f-002-installable-package` divergence 为 `0 0`。

### Draft PR

- 已创建 [PR #3](https://github.com/wcnm8888/mcp1-weather-query/pull/3)：
  `feat/f-002-installable-package → main`。
- 标题：`build: complete F-002 installable package`；状态：`OPEN / Draft`。
- PR 正文覆盖变更、原因、用户/开发者影响、验证、回滚、非目标及风险边界。
- F-002 已批准不新增 GitHub Actions；PR 明确写出 local-only 门禁例外，未宣称远程
  CI 通过。
- 未标记 Ready、未合并、未删除分支、未创建 Release/tag、未上传 PyPI 或登记
  MCP Registry。

### 当前门禁

Step 6 Git/PR 交付已完成，F-002 尚未关闭。当前等待用户审查 Draft PR #3，并决定
标记 Ready 或合并；合并后还需单独授权 Step 7 同步 main、归档 F-002 和分支收口。
