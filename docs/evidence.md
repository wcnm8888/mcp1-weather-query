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

- `uv --version`：`uv 0.6.14`；项目解释器：`Python 3.12.10`；当前分支：`feat/f-001-local-weather-tool`；无 Git remote。
- `uv lock --check`：通过，解析 46 个包。
- `uv run ruff format --check .`：通过，33 个文件已格式化。
- `uv run ruff check .`：通过。
- `uv run mypy`：通过，21 个源码/测试文件无问题。
- Git 交付前清除 `MCP_WEATHER_RUN_LIVE` 并执行 `uv run pytest -q --tb=short`：`52 passed, 1 skipped in 5.51s`；唯一 skip 是显式 live contract。
- `git diff --check`：无空白错误；Git 仅提示现有 LF 文件未来可能按 Windows 配置转换为 CRLF。
- Step 6 QA 执行过程未联网、未运行 Inspector、未构建或打包；用户随后选择远程 PR 流程并授权形成本地提交，仍未创建远程、push 或 PR。

## 未完成证据

- F-001 Step 5 协议对齐：现代/Legacy 两条 stdio 证据已完成。
- F-001 Step 5 用户 UAT：用户于 2026-08-11 明确确认通过。
- F-001 Step 6 独立 QA：已完成；用户已选择远程 PR 流程并形成精确本地提交，提交哈希以 Git 事实为准。
- 远程 PR 交付：当前无 remote，未 push、未创建 PR；等待远程仓库信息和外部写入授权，F-001 尚未关闭。
- 构建、打包、干净安装和发布不属于 F-001，且无通过结论。
