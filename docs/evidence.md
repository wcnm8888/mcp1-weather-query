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

## F-002 / Step 7 合并后收口

日期：2026-08-11

### 合并与同步事实

- 用户已合并 [PR #3](https://github.com/wcnm8888/mcp1-weather-query/pull/3)；GitHub
  状态为 `MERGED`，合并时间为 `2026-08-11T11:18:27Z`，合并提交为
  `ac39554a87b8f8fde85ec6d893484c42d1c6b253`。
- 合并后执行 `git fetch origin`、切换 `main` 并使用 fast-forward 同步；本地
  `main` 与 `origin/main` 均为 `ac39554a87b8f8fde85ec6d893484c42d1c6b253`。
- 未直接在 `main` 提交收口变更，也未删除本地或远程分支。

### 合并后复验与最小修复

- 首轮执行锁文件、Ruff、严格 mypy、默认 pytest 和 Step 5 QA 制品复验；默认
  pytest 为 `62 passed, 1 skipped in 5.79s`，但制品检查报告
  `wheel legal file drift: LICENSE`。
- 根因是 Windows Git checkout 将工作树法律文本写为 CRLF，而已验收制品使用 LF；
  原检查器把跨平台文本换行差异误判为语义漂移。
- 在 `fix/f-002-post-merge-artifact-check` 上提交最小修复 `0a772fc`：仅规范化源文件、
  README 和法律文本的 CRLF/LF 后再比较；wheel `RECORD` 的原始字节长度、SHA-256
  和覆盖范围校验保持严格，没有放宽制品完整性要求。
- 修复后 Step 5 QA 制品再次通过，制品保持不变：
  - sdist：11,081 bytes，SHA-256
    `95efce0bce103b95765a613e89122a92e0338ecc9add644586f65fb2c4c58abf`；
  - wheel：15,535 bytes，SHA-256
    `1bdba3c8b87aca8782765d39950eb13abb6380de120905ac496e8ae4813d0fb0`。
- 复验结果：`uv lock --check` 通过；最终 Ruff format check 为 38 个文件通过；Ruff lint
  通过；严格 mypy 为 24 个源文件通过；默认 pytest 为
  `62 passed, 1 skipped`；`git diff --check` 通过。
- 唯一 skip 仍是显式 live contract；没有访问 Open-Meteo live API、运行 Inspector、
  构建/发布新制品、增加 Tool 或传输方式、更新依赖或修改系统环境。

### 收口交付

- 已推送 `fix/f-002-post-merge-artifact-check`，并创建
  [Draft PR #4](https://github.com/wcnm8888/mcp1-weather-query/pull/4)，目标为 `main`。
- F-002 完整任务卡已复制到
  `docs/archive/task-cards/F-002-可安装与可构建闭环.md`；当前任务和实施计划入口已
  重置为无活动任务，roadmap/progress/文档地图已压缩到当前事实。
- F-002 的实现、QA、UAT 与功能合并均已完成；当时最终收口等待用户审查
  Draft PR #4。本节保留当时的 Step 7 交付证据，最终合并事实见下节。

### PR #4 最终合并与 F-002 关闭

- 用户已合并 [PR #4](https://github.com/wcnm8888/mcp1-weather-query/pull/4)；GitHub
  状态为 `MERGED`，合并时间为 `2026-08-11T11:43:14Z`，merge commit 为
  `a3ef73c185084ae0a0e3374d78779f7618f0a16b`。
- D-001 Step 0 起点核验时，本地 `main`、`origin/main` 和 `HEAD` 均为该提交，分叉为
  `0/0`，起点工作树干净。
- F-002 完整任务卡的最终状态已修正为 `completed / merged / closed`；该修正只补充
  最终事实，不覆盖 F-002 的历史验证证据。

## D-001 / Step 0 文档治理与任务基线

日期：2026-08-11

### 起点与范围

- 用户从已批准 roadmap 选择 D-001，并明确允许进入 Step 0。
- D-001 维持 S 级，项目整体仍按 M 管理；唯一目标是发布候选与发布前审查，不执行
  PyPI、TestPyPI、MCP Registry、GitHub Release 或 tag 等外部发布。
- 环境保持 `uv 0.6.14` 和项目内 CPython `3.12.10`，未更新依赖、Node、uv、Python
  或系统配置。

### Git 与文档治理

- 起点为干净、同步的 `main`：`a3ef73c185084ae0a0e3374d78779f7618f0a16b`。
- 从该基线创建本地分支 `chore/d-001-release-candidate`；未 push、commit 或创建 PR。
- 已把 D-001 持久化为唯一活动任务，建立 Step 0–8 地图、验收、测试、文档和停止
  契约，并同步 AGENTS、文档地图、architecture、roadmap、progress 与实施计划。
- 未创建 `CHANGELOG.md`、`server.json`、构建制品或发布账号/平台条目；未安装或运行
  publisher。

### 离线门禁

- `uv lock --check`：通过，解析 46 个包，锁文件未变化。
- `uv run ruff format --check .`：通过，38 个文件已格式化。
- `uv run ruff check .`：通过。
- `uv run mypy`：通过，24 个源文件无问题。
- `uv run pytest -q --tb=short`：`62 passed, 1 skipped in 6.67s`；唯一 skip 为未设置
  `MCP_WEATHER_RUN_LIVE=1` 的真实 Open-Meteo contract，没有 live 请求。
- `git diff --check`：通过；只出现 Git 对 Windows 工作树未来 CRLF 转换的提示，不是
  whitespace error，也未改动已验证的制品比较规则。

### Step 0 结论

D-001 Step 0 已完成。变更只涉及任务治理和历史状态文档；没有修改 `src/`、`tests/`、
`pyproject.toml`、`uv.lock`、License/NOTICE 或运行时行为。当前停止在 Step 1 用户门禁。

## D-001 / Step 1 先失败的发布候选契约

日期：2026-08-11

### 官方格式核验

- MCP 官方 Registry package types 文档确认：PyPI 包使用 `registryType: pypi`，并通过
  包 README 中的 `mcp-name: $SERVER_NAME` 字符串验证归属；该字符串可以位于 HTML
  comment 中。
- 当前官方示例使用 Schema
  `https://static.modelcontextprotocol.io/schemas/2025-12-11/server.schema.json`。
- Step 1 只把这些值固定进后续验证矩阵；没有创建 `server.json`、下载 publisher、
  登录或调用 Registry。

### 新增契约

- 新增 `tests/release/test_release_candidate_contract.py`，共 10 项静态契约。
- 4 项立即通过：既有 distribution/import/console/version/License identity，以及
  Step 3 Registry、Step 4 wheel/sdist、Step 5 双干净安装矩阵。
- 6 项预期失败，逐项对应当前真实缺口：
  1. 根目录缺少 `CHANGELOG.md`；
  2. README 缺少从本地候选 wheel 安装且无需 `PYTHONPATH` 的命令；
  3. README 缺少明确标为“PyPI 发布后”的未来 `uvx` 命令；
  4. README 缺少直接调用 console command 的 stdio Host JSON；
  5. README 缺少 Registry ownership marker 和明确的 PyPI/Registry 未发布声明；
  6. release plan 缺少 `uv build --no-sources`、本地 `validate` 与禁止 `login/publish`
     的可复制命令边界。

### 验证结果

- release contract：`6 failed, 4 passed in 0.20s`，失败位置与上述缺口一一对应。
- 完整 pytest：`6 failed, 66 passed, 1 skipped in 6.69s`；唯一 skip 仍为显式 live
  contract，没有访问 Open-Meteo。
- 排除故意红灯后的既有回归：`62 passed, 1 skipped in 5.70s`。
- `uv lock --check` 通过（46 packages）；Ruff format 为 39 个文件通过；Ruff lint
  通过；严格 mypy 为 25 个源文件通过；`git diff --check` 通过。

### 边界与结论

- 未修改 `README.md`、`docs/release-plan.md`、`pyproject.toml`、`uv.lock`、`src/`、
  Tool 契约、依赖或运行时。
- 未创建 `CHANGELOG.md`、`server.json`、wheel/sdist、临时安装环境、tag、Release 或
  外部平台条目；未运行 live API、Inspector 或 publisher。
- D-001 Step 1 已完成，当前等待用户允许进入 Step 2；红灯在获准实现前必须保留。

## D-001 / Step 2 最小发布元数据与文档实现

日期：2026-08-11

### 实际实现

- 新建 `CHANGELOG.md`，以 `[0.1.0] - Unreleased` 记录唯一只读 Tool、stdio、console
  command、License/attribution、支持范围和真实限制，并明确 PyPI/Registry 均未发布。
- README 顶部增加官方 PyPI ownership marker
  `mcp-name: io.github.wcnm8888/mcp1-weather-query`；增加本地候选 wheel 的
  `uv tool install`、发布后才可用的固定版本 `uvx`、console stdio Host JSON 和
  `PYTHONPATH` 禁止边界。
- `docs/release-plan.md` 增加后续 Step 的 `uv build --no-sources`、项目外 E 盘候选
  目录、`mcp-publisher validate` 及禁止 `login`/`publish` 的命令契约。本 Step 未执行
  任一命令。
- uv 官方 tools 文档确认：`uv tool install` 支持具体本地 wheel/source archive；
  `uvx --from 'package==version' command` 在隔离环境运行指定发行版。

### 验证结果

- 定向 release contract：`10 passed in 0.04s`，Step 1 的 6 个红灯全部按原断言转绿。
- `uv lock --check`：通过（46 packages，锁文件未变化）。
- Ruff format：40 个文件通过；Ruff lint：通过。
- 严格 mypy：25 个源文件通过。
- 完整默认 pytest：`72 passed, 1 skipped in 6.77s`；唯一 skip 为显式 live contract，
  未访问 Open-Meteo。
- `git diff --check`：通过；Windows LF/CRLF 提示不属于 whitespace error。

### 边界与结论

- 未修改 `pyproject.toml`、`uv.lock`、`src/`、现有 Tool 契约、transport、依赖、
  License/NOTICE 或系统环境。
- 未创建 `server.json`，未构建 wheel/sdist，未创建临时安装环境，未安装/运行
  publisher，未登录或访问发布平台写接口。
- D-001 Step 2 已完成，当前等待用户允许进入 Step 3：Registry 草案与本地校验。

## D-001 / Step 3 Registry 草案与官方校验

日期：2026-08-11

### 官方基线与草案

- 执行时官方 Registry package types/quickstart 仍使用
  `https://static.modelcontextprotocol.io/schemas/2025-12-11/server.schema.json`，PyPI
  package 使用 `registryType=pypi`、固定 identifier/version 和 stdio transport。
- GitHub official release API 显示当前稳定 publisher 为 v1.8.1（2026-08-06，commit
  `f52dc8525a441a3abf5fedc9912152d95af5aab1`）。
- 新建 605-byte 根 `server.json`：server name
  `io.github.wcnm8888/mcp1-weather-query`、title、只读当前天气描述、版本 `0.1.0`、
  GitHub repository、唯一 PyPI package `mcp-weather-query==0.1.0`、`runtimeHint=uvx`
  和 stdio。
- manifest 没有 remotes、HTTP/SSE、environment variables、package/runtime arguments、
  任意 URL 输入或敏感字段。

### 固定工具与供应链证据

- Windows amd64 归档保存于项目外
  `E:\mcp-weather-query-tools\mcp-publisher\v1.8.1\mcp-publisher_windows_amd64.tar.gz`，
  7,547,008 bytes。
- 归档 SHA-256：
  `399ad0d6e00a50812b563a71d8bfbff5160c085e6b13aac6ec083d98d5ff7c45`，与官方
  GitHub release asset digest 一致。
- 解压后的 exe 为 20,393,472 bytes，SHA-256：
  `d021e6496bd10e5be4264e865f795c1c9802501699342a838b601f0f4d383fd5`；工具未加入
  PATH，未修改项目或系统环境。
- v1.8.1 存在一个 help-only 缺陷：顶层帮助列出 `validate`，但 `validate --help`
  显示 `Unknown command: validate`；直接执行 `validate` 正常工作，不影响本次结果。

### 校验结果与网络边界

- 静态 release/Registry contract：`14 passed in 0.05s`。
- 运行外部固定版 `mcp-publisher.exe validate`，输出
  `Validating against https://registry.modelcontextprotocol.io...`、
  `✅ server.json is valid`，exit code 0。
- 对 v1.8.1 tag 源码做只读核验：validate 以未认证 HTTP POST 调用
  `https://registry.modelcontextprotocol.io/v0/validate`，只返回 ValidationResult；没有
  调用 login/publish/status，也没有创建 Registry 条目。因此本证据是“官方验证端点
  校验”，不是纯离线校验。
- `uv lock --check` 通过；Ruff format 为 41 个文件通过；Ruff lint 通过；严格 mypy
  为 26 个源文件通过；完整 pytest 为 `76 passed, 1 skipped in 8.64s`；唯一 skip 为
  显式 Open-Meteo live contract；`git diff --check` 通过。

### 结论

- 未运行 `mcp-publisher login/publish/status`，未使用账号/Token，未上传 PyPI、登记
  Registry、创建 tag/Release 或修改外部平台持久状态。
- 未构建 wheel/sdist，未创建干净安装环境，未修改源码、Tool、transport、依赖、
  `pyproject.toml`、`uv.lock` 或系统环境。
- D-001 Step 3 已完成，当前等待用户允许进入 Step 4：候选构建与制品审查。

## D-001 / Step 4 候选构建与制品审查

日期：2026-08-11

### 构建环境与命令

- 分支 `chore/d-001-release-candidate`；继续复用 uv 0.6.14 和项目内 CPython 3.12.10，
  未更新依赖、锁文件或系统环境。
- 新建项目外候选目录
  `E:\mcp-weather-query-release-candidate\0.1.0\step4-20260811T205328\dist`；没有删除或
  覆盖既有候选。
- 执行 `uv build --no-sources --offline --out-dir <上述目录>`；uv 先构建 sdist，再从
  sdist 构建 wheel。`--offline` 成功，未访问包索引；`--no-sources` 禁用 source
  overrides。
- uv 在输出目录自动创建 1-byte、内容为 `*` 的 `.gitignore`；检查器将其作为唯一
  允许的非制品文件，任何其他文件或子目录都会失败。

### 候选身份与哈希

- wheel：`mcp_weather_query-0.1.0-py3-none-any.whl`，16,376 bytes，15 个归档文件，
  SHA-256 `3e526b64d7f41a50679a586f54cda108ac7a8cc8b15d432faca4108c76da438a`。
- sdist：`mcp_weather_query-0.1.0.tar.gz`，11,946 bytes，14 个归档文件，SHA-256
  `eff5f30a417886c4ea6069cfaf95d41eae13067be4e4dc64a0eff25658090f4f`。
- `CHANGELOG.md` 与 `server.json` 是仓库级发布协调材料；不在精确 wheel/sdist 白名单
  中。wheel 不含测试或发布工具；sdist 只含重建所需源码、README、pyproject 和法律
  文件。

### 静态制品审查

- wheel/sdist 的 Metadata-Version 为 2.4；Name/Version、`Requires-Python`、三项
  `Requires-Dist`、MIT expression 和 LICENSE/NOTICE 均与 `pyproject.toml` 一致。
- console entry point 精确为
  `mcp-weather-query = mcp_weather_query.__main__:main`；wheel 为 `py3-none-any`，RECORD
  精确覆盖所有文件且每项大小/哈希复算通过。
- wheel/sdist 内源码与当前 `src` 逐文件一致；法律文件按跨平台换行规则一致；嵌入
  README 与根 README 一致，并含 Registry ownership marker、Open-Meteo/CC BY 4.0
  attribution 和明确未发布状态。
- 全部 payload 未发现项目/用户绝对路径、`.runtime`、`.venv`、缓存、日志、测试、
  凭据或 secret-like assignment。
- 增强检查器仅增加外层目录白名单和 D-001 README 断言；F-002 的精确归档、源码、
  法律文本和 RECORD 检查未放宽。最终检查器输出两项制品摘要并退出 0。

### 回归门禁与边界

- `uv lock --check`：通过（46 packages）；Ruff format：41 个文件通过；Ruff lint：
  通过；严格 mypy：26 个源文件通过。
- 完整默认 pytest：`76 passed, 1 skipped in 8.55s`；唯一 skip 为显式 Open-Meteo live
  contract，没有网络请求；`git diff --check` 通过。
- 未安装、导入或执行候选，没有创建 wheel/sdist 环境或启动 stdio；未运行 live API、
  Inspector、publisher、login/publish/status，未上传或登记外部平台。
- D-001 Step 4 已完成，当前等待用户允许进入 Step 5：双干净安装与
  installed-package stdio 复验。

## D-001 / Step 5 双干净安装与 installed-package stdio 复验

日期：2026-08-11

### 固定制品与环境

- 本 Step 未构建或替换制品。复审 Step 4 固定目录后，wheel 仍为 16,376 bytes、15 个
  文件、SHA-256
  `3e526b64d7f41a50679a586f54cda108ac7a8cc8b15d432faca4108c76da438a`；sdist 仍为
  11,946 bytes、14 个文件、SHA-256
  `eff5f30a417886c4ea6069cfaf95d41eae13067be4e4dc64a0eff25658090f4f`。
- 新建项目外根
  `E:\mcp-weather-query-release-candidate\0.1.0\step5-20260811T210410`，包含独立
  `wheel-env`、`sdist-env` 及各自工作目录；没有覆盖既有候选或环境。
- 两个环境均由现有 uv 0.6.14 和项目内 CPython 3.12.10 创建。在清空
  `PYTHONPATH`、`PYTHONHOME`、`VIRTUAL_ENV`、`MCP_WEATHER_RUN_LIVE` 并设置
  `UV_OFFLINE=1` 后，分别安装固定 `.whl` 与 `.tar.gz`。sdist 隔离构建也在离线模式
  成功；两套环境均安装 34 个包。
- 两套 `direct_url.json` 精确指向对应本地制品，distribution 均为
  `mcp-weather-query==0.1.0`；模块来自各自 `Lib\site-packages\mcp_weather_query`，console
  来自各自 `Scripts\mcp-weather-query.exe`，不存在 editable 或源码目录安装。

### installed-package stdio 结果

- wheel 与 sdist 的生产 console 均完成 Legacy MCP 2025-11-25 initialize 和
  tools/list，只返回 `get_current_weather`。所有 stdout 行均为 JSON-RPC，关闭 stdin 后
  退出码均为 0，stderr 无 traceback。
- 各自环境 Python 运行官方 SDK v2 `Client(mode="auto")`，对生产 console 均完成 MCP
  2026-07-28 modern discovery，只发现 `get_current_weather`。
- 测试专用子进程从已安装生产包导入 `create_server` 并注入 synthetic handler；两套环境
  均以 MCP 2026-07-28 完成 Tool 调用，返回通过 `CurrentWeatherResult`/outputSchema 的
  `structuredContent`，输入规范化为北京/CN。该入口不是 console entry point，不发起 HTTP。
- synthetic 诊断标记只出现在两份 `fixed-stderr.log`；两份
  `production-modern-stderr.log` 均为 0 bytes。单步超时为 10 秒，finally 负责终止异常
  子进程；完成后没有来自 Step 5 环境的 Python、uv 或 Node 进程。

### 回归、修复与范围

- 初次 `ruff format --check` 发现复验脚本两处文案修改造成混合换行；仅对
  `tests/packaging/verify_installed_package.py` 执行 Ruff format 后修复，没有改生产代码
  或制品。该脚本的诊断名称由 F-002 历史文案改为发布候选通用文案。
- 最终 `uv lock --check` 通过（46 packages）；Ruff format 41 个文件通过；Ruff lint
  通过；严格 mypy 26 个源文件通过；最终 pytest 为 `76 passed, 1 skipped in 6.77s`，唯一 skip
  是显式 live contract；`git diff --check` 通过。
- 未访问 Open-Meteo live API，未运行 MCP Inspector 或 publisher，未更新依赖、uv、
  Python、Node、锁文件或系统环境，未登录、发布、提交、push 或创建 PR。
- D-001 Step 5 已完成，当前等待用户允许进入 Step 6：独立 QA 与用户 UAT。

## D-001 / Step 6 独立 QA 与用户 UAT

日期：2026-08-11

### 审查范围与基线

- 当前分支 `chore/d-001-release-candidate`；HEAD、本地 `main` 和本地现有
  `origin/main` 均为 `a3ef73c185084ae0a0e3374d78779f7618f0a16b`。
- 尝试只读 `git fetch origin main --quiet` 时 30 秒未返回，已终止本轮产生的挂起 Git
  进程；没有仓库写入。本次 QA 以现有本地 `origin/main` 引用审查，Step 7 必须重新刷新
  远程状态。
- 审查了 14 个已跟踪变更和 4 个未跟踪文件：`CHANGELOG.md`、`server.json` 及两份
  release contract。普通 `git diff` 未覆盖的未跟踪文件均已逐一读取。
- `src/`、`pyproject.toml`、`uv.lock`、LICENSE、NOTICE 均无 D-001 差异；仍恰好一个
  `@server.tool`，且生产源码没有普通 `print`。

### QA 发现与修复

- [P2] 根 README 仍写 D-001 “后续阶段会生成候选”和“拟交付能力”，与 Step 4–5
  已完成事实冲突；同时保留 F-002 的旧测试计数。已改为当前候选、已交付能力和 D-001
  `76 passed, 1 skipped`。
- [P2] 测试策略“当前门禁”仍把 F-002 的 `62 passed, 1 skipped` 写成当前结果；已区分
  F-002 历史与 D-001 当前结果。架构、发布方案和 release contract 模块说明中的模糊
  阶段文字也做了最小限定。
- 根 README 修复后，Step 4 wheel 被检查器以
  `wheel METADATA: embedded README differs from the current project README` 正确拒绝；
  没有把陈旧制品写成通过，也没有删除或覆盖旧目录。
- 修复后没有未解决的高、中优先级 D-001 范围内缺陷。

### 新 QA 候选与双安装

- 使用现有 uv 0.6.14、项目内 Python 3.12.10 和
  `uv build --no-sources --offline`，在
  `E:\mcp-weather-query-release-candidate\0.1.0\step6-qa-20260811T213511\dist`
  生成新候选；未访问包索引。
- wheel：16,340 bytes、15 个文件、SHA-256
  `c93ab54579fdd92c8ed91a5c6ea3fe2c8b97373fc50abfbc8d42fdbd01b661b6`。
- sdist：11,904 bytes、14 个文件、SHA-256
  `f9d68065233674f7413b95ee10b0d297bcbae8b8f3ff6cfceecb6d4e1b4d18f2`。
- 两个制品通过 Metadata 2.4、entry point、RECORD、精确文件白名单、源码/法律文件/
  当前 README 一致性和敏感信息扫描。
- 新 `wheel-env`/`sdist-env` 均为 Python 3.12.10，在 `UV_OFFLINE=1` 且无
  `PYTHONPATH`/`PYTHONHOME`/`VIRTUAL_ENV` 下分别从对应本地制品安装 34 个包；provenance
  精确匹配，不是 editable 或源码目录安装。
- 两套生产 console 均以 Legacy 2025-11-25 完成 initialize/tools-list，并以官方 SDK
  v2 MCP 2026-07-28 完成 modern discovery；只发现 `get_current_weather`。确定性调用返回
  合法 `structuredContent`；stdout 纯协议，生产 modern stderr 为 0 bytes，测试诊断只在
  stderr，退出码 0，完成后无 QA 环境 Python/uv/Node 残留进程。

### 最终门禁与当前结论

- `uv lock --check` 通过（46 packages）；Ruff format 41 个文件通过；Ruff lint 通过；
  严格 mypy 26 个源文件通过；文档收口后最终 pytest 为
  `76 passed, 1 skipped in 12.27s`，唯一 skip 是显式
  live contract；新候选制品复审和 `git diff --check` 通过。
- `server.json` 仍只有一个 PyPI package 和 stdio transport，无 remotes、环境变量、参数
  或秘密；变更文件未发现 secret-like assignment。没有第二 Tool、HTTP/SSE 入口、任意
  URL、写操作或系统环境修改。
- 未访问 Open-Meteo live API，未运行 MCP Inspector 或 publisher，未登录、发布、创建
  tag/Release、commit、push 或 PR。
- 用户于 2026-08-11 使用 QA wheel 环境执行
  `tests/packaging/verify_installed_package.py verify`，并要求验收通过后进入 Step 7。
  结果显示安装来源为 `mcp_weather_query-0.1.0-py3-none-any.whl`，distribution 为
  `mcp-weather-query==0.1.0`，模块来自该环境 `Lib\site-packages`，console 来自该环境
  `Scripts\mcp-weather-query.exe`。
- 用户 UAT 中，确定性调用和 modern discovery 均协商 MCP 2026-07-28，只发现
  `get_current_weather`，且 `structured_content=true`、诊断进入 stderr。生产 console
  Legacy 握手为 2025-11-25，`stdout_protocol_only=true`、`stderr_traceback=false`、
  `exit_code=0`。
- 因此 D-001 Step 6 独立 QA 与用户 UAT 均已通过；用户已允许进入 Step 7 Git/PR 交付。
  该授权不包含自动合并、tag、Release、PyPI 上传、Registry 登记或 publisher 登录/发布。

## D-001 / Step 7 Git/PR 交付

日期：2026-08-11

- `gh auth status` 确认 GitHub 账号 `wcnm8888` 已登录；`gh` 版本为 2.95.0。
- `git fetch origin main --prune` 成功；交付前 HEAD、本地 `main` 和 `origin/main` 均为
  `a3ef73c185084ae0a0e3374d78779f7618f0a16b`，没有基线漂移。
- 精确暂存 18 个 D-001 路径；未使用全量暂存。暂存范围不包含 wheel/sdist、项目外环境、
  缓存、日志、本机配置或凭据。
- 提交前 `uv lock --check` 通过（46 packages）；Ruff format 41 个文件通过；Ruff lint
  通过；严格 mypy 26 个源文件通过；pytest 为 `76 passed, 1 skipped in 5.74s`，唯一 skip
  为显式 live contract；`git diff --check` 通过。
- 固定 QA wheel/sdist 再次通过制品检查：wheel 15 个文件、16,340 bytes、SHA-256
  `c93ab54579fdd92c8ed91a5c6ea3fe2c8b97373fc50abfbc8d42fdbd01b661b6`；sdist 14 个文件、
  11,904 bytes、SHA-256 `f9d68065233674f7413b95ee10b0d297bcbae8b8f3ff6cfceecb6d4e1b4d18f2`。
- 创建提交 `f44e8b6a4df63016a639df4b7e2d5337c6fbf28d`
  （`docs(release): prepare D-001 release candidate`），并推送
  `chore/d-001-release-candidate`。
- 创建 Draft PR #5：`https://github.com/wcnm8888/mcp1-weather-query/pull/5`；目标为
  `main`，来源为 `chore/d-001-release-candidate`。创建后状态为 `OPEN / Draft / MERGEABLE`。
- 没有自动合并，没有创建 tag/Release，没有运行 publisher/login/publish，没有上传 PyPI
  或登记 Registry，也没有访问 Open-Meteo live API 或运行 Inspector。
- D-001 尚未关闭。当前停在用户 PR 审查门禁；合并后 Step 8 仍需用户单独允许。

## D-001 / Step 8 合并后收口

日期：2026-08-11

- 用户确认 PR #5 已合并并明确允许进入 Step 8。GitHub 复核 PR #5 状态为 `MERGED`，
  合并时间为 `2026-08-11T15:46:20Z`，merge commit 为
  `2e691c351b78a0281a4a1fcdb21eca90c8e2f580`。
- 合并前 PR #5 包含提交 `f44e8b6a4df63016a639df4b7e2d5337c6fbf28d` 与
  `e907e7a5df50c2031ddf901bde6930e29969757f`；目标为 `main`，来源为
  `chore/d-001-release-candidate`。
- 从干净工作树切回 `main`，执行 `git fetch origin main --prune` 和
  `git pull --ff-only origin main`；本地 `main` 与 `origin/main` 均同步到 `2e691c3`。
- 合并后使用既有环境运行完整离线门禁：`uv lock --check` 通过（46 packages）；Ruff
  format 41 个文件通过；Ruff lint 通过；严格 mypy 26 个源文件通过；pytest 为
  `76 passed, 1 skipped in 6.18s`，唯一 skip 仍为显式 live contract；`git diff --check`
  通过。
- 从合并后的 `main` 创建 `docs/d-001-post-merge`，只承载最终文档治理：归档完整 D-001
  任务卡、重置活动任务和实施计划入口、同步 roadmap/progress/文档地图/架构/测试状态。
- 创建提交 `47809656a218c80f196d6bd890d5410a22c23fbb`
  （`docs(project): close D-001 after merge`）并推送 `docs/d-001-post-merge`。
- 创建 Draft PR #6：`https://github.com/wcnm8888/mcp1-weather-query/pull/6`；目标为
  `main`，来源为 `docs/d-001-post-merge`。创建后状态为 `OPEN / Draft / MERGEABLE`。
- D-001 的代码、构建、QA、UAT 和功能合并均已完成；没有修改生产 Tool、依赖、锁文件
  或运行时环境。
- 未访问 Open-Meteo live API，未运行 Inspector/publisher，未登录或上传 PyPI，未登记
  Registry，未创建 tag/Release，也未进入 R-001/R-002。
- D-001 最终状态为：已完成发布候选与发布前审查，等待用户选择是否起草 R-001 候选任务卡。

## R-001 / Step 0 文档治理与 L 级基线

日期：2026-08-12

- 用户批准 R-001 任务卡、L 级风险流程、Trusted Publishing 方案、测试矩阵、Step 地图、
  完成定义和 16 项决策，并只授权进入 Step 0。
- Step 0 前确认工作树干净，本地 `main` 与 `origin/main` 均为
  `0d5d7be9271b71143cdbcdf768bfbde5ed4393d0`。
- 从该基线创建仅本地分支 `release/r-001-pypi-0.1.0`；没有 commit 或 push。
- 持久化 R-001 为唯一活动任务，建立独立 L 级 QA 清单，并同步实施计划、roadmap、
  progress、文档地图和项目规则。
- 使用现有 uv 0.6.14 和项目内 CPython 3.12.10，清空 `MCP_WEATHER_RUN_LIVE` 后运行：
  `uv lock --check` 通过（46 packages）；最终 Ruff format 43 个文件通过；Ruff lint 通过；
  严格 mypy 26 个源文件通过；pytest 为 `76 passed, 1 skipped in 5.61s`，唯一 skip 是
  显式 live contract；`git diff --check` 通过。
- 未创建 GitHub Actions workflow，未修改发布元数据、源码、Tool、transport、依赖或锁文件，
  未构建 wheel/sdist，未访问 Open-Meteo live API。
- 未登录 PyPI、未配置 Pending Publisher、未创建或推送 tag、未上传制品、未提交、推送或
  创建 PR。当前门禁为等待用户允许进入 R-001 Step 1。

## R-001 / Step 1 先失败的发布与 workflow 安全契约

日期：2026-08-12

- 核验 PyPI 官方 Trusted Publisher 文档：GitHub publisher identity 必须匹配 owner、
  repository、workflow filename 和可选 environment；Pending Publisher 首次使用前不占名。
- 核验 PyPA 官方 publish action：Trusted Publishing 要求发布 job 的 `id-token: write`，
  不需要 username/password/token；attestations 在该流程中默认开启。
- 通过官方仓库 ref 只读解析并固定 action SHA：checkout v6 `d23441a...`、setup-python v6
  `ece7cb0...`、setup-uv v9.0.0 `c771a70...`、upload-artifact v5 `330a01c...`、
  download-artifact v5 `634f93c...`、PyPA release/v1 `dc37677...`。
- 新增 `tests/release/test_pypi_publish_contract.py`，共 9 项静态离线契约。
- 定向结果为 `7 failed, 2 passed`。两个通过项固定已批准 package identity 和诚实的
  `Unreleased` 状态；七个失败对应五类缺失 workflow 契约、release plan 缺口和 README
  Open-Meteo 公共限制缺口。
- 完整套件为 `7 failed, 78 passed, 1 skipped in 5.79s`；排除新的故意红灯后为
  `76 passed, 1 skipped in 5.43s`，唯一 skip 为显式 live contract。
- `uv lock --check` 通过（46 packages）；Ruff format 44 个文件、lint、严格 mypy 27 个
  源文件和 `git diff --check` 通过；生产源码仍恰好一个 `@server.tool`。
- `.github/` 和 `v0.1.0` tag 均不存在；未修改 README、CHANGELOG、release plan、
  pyproject、源码、依赖或锁文件，未构建制品或访问 live API。
- 未登录 PyPI、未配置 Pending Publisher、未上传、commit、push 或创建 PR。当前等待
  用户允许进入 R-001 Step 2，使七个红灯以最小实现转绿。

## R-001 / Step 2 最小发布文档与安全 CI workflow

日期：2026-08-12

- 新增 `.github/workflows/release.yml`。触发器只有 PR 和精确 `v0.1.0` tag push，没有
  ordinary branch push、manual dispatch、TestPyPI 或 GitHub Release 路径。
- build job 继承顶层 `contents: read`，固定 Python 版本文件和 uv 0.6.14，运行 lock、
  format、lint、严格 mypy、默认离线 pytest 和 `uv build --no-sources` 后上传 distributions。
- publish job 同时检查 push event 与精确 tag，依赖 build，绑定 `pypi` environment；仅该
  job 拥有 `id-token: write`，且只下载 artifact 和调用官方 PyPA publish action。
- checkout/setup-python/setup-uv/upload/download/PyPA 六个 action 均固定完整 SHA。Step 2
  复核官方当前版本后，将 Step 1 的旧 setup-uv v7 pin 修正为不可变 v9.0.0 commit
  `c771a70...`；workflow 安装的 uv 仍固定为 0.6.14，本机环境未改变。
- README 新增非商业免费层、600 次/分钟、5,000 次/小时、10,000 次/日、无 SLA 和
  CC BY 说明；release plan 新增精确 Pending Publisher tuple、双授权、attestation 和 yank。
- 九项 R-001 契约全部通过；完整离线结果为 `85 passed, 1 skipped in 5.51s`，唯一 skip
  为显式 live contract。`uv lock --check`、Ruff format 44 个文件、lint、严格 mypy
  27 个源文件和 `git diff --check` 均通过。
- 安全扫描确认生产源码仍恰好一个 Tool；workflow 无 secrets/password/TestPyPI/
  `skip-existing`/关闭 attestation，OIDC 只存在于 publish job。
- 本机未安装新 YAML/actionlint 依赖；workflow 结构已由离线契约复核，真实 GitHub YAML
  解析和执行证据属于后续 PR CI，不在本 Step 冒充。
- 仓库根存在被 `.gitignore` 排除的历史 `dist/`，创建/最后修改时间均为 2026-08-11；
  Step 2 没有运行构建命令、没有修改或使用该目录，也不把历史文件作为本轮制品证据。
- 未在本地构建最终制品，未访问 Open-Meteo live API，未触发 Actions，未登录 PyPI、
  配置 Pending Publisher、创建 tag、上传、commit、push 或创建 PR。当前等待 Step 3。

## R-001 / Step 3 项目外候选、双干净安装与 stdio 复验

日期：2026-08-12

- 新建项目外候选根
  `E:\mcp-weather-query-release-candidate\0.1.0\r001-step3-20260812T003655`；没有覆盖或
  删除历史候选，也没有使用仓库根被忽略的旧 `dist/`。
- 在清空 live 开关并设置 `UV_OFFLINE=1` 后，以现有 uv 0.6.14 和项目内 Python 3.12.10
  执行 `uv build --no-sources --offline`；构建过程没有访问包索引或 source override。
- wheel：15 files、16,523 bytes、Core Metadata 2.4、SHA-256
  `e95429d4744e14f36efeecc08833269a0c72202bfdf4f9e3255412c73d225b6e`。
- sdist：14 files、12,107 bytes、Core Metadata 2.4、SHA-256
  `e824aa4c64cb7e202d60cbd6fe3f0920043401789b1f755967285cb76ee15b63`。
- `inspect_artifacts.py` 对两个制品的精确白名单、元数据、entry point、RECORD、源码、
  当前根 README、LICENSE/NOTICE、发布边界和敏感信息审查通过；双安装后复审哈希未变。
- 创建独立 `wheel-env` 与 `sdist-env`。清空 `PYTHONPATH`、`PYTHONHOME`、`VIRTUAL_ENV`
  并设置 `UV_OFFLINE=1` 后，分别从固定 wheel/sdist 离线安装，各解析并安装 34 packages。
- 两套 provenance 分别指向对应本地制品；distribution 为 `mcp-weather-query==0.1.0`，
  模块来自各环境 `Lib\site-packages`，console 来自各环境 `Scripts`，不是 editable/源码安装。
- 两套生产 console 均以 Legacy 2025-11-25 完成 initialize/tools-list，只发现
  `get_current_weather`；stdout 仅协议消息、stderr 无 traceback，关闭 stdin 后 exit code 0。
- 官方 SDK v2 Client 对两套 console 均以 MCP 2026-07-28 完成 modern discovery；测试
  专用固定子进程在同一协议下返回合法 `structuredContent`，诊断只写 stderr，不访问 HTTP。
- 两份 `production-modern-stderr.log` 均为 0 bytes，两份测试诊断日志均为 54 bytes；
  验证完成后没有命令行关联该候选根的 Python/uv/Node 残留进程。
- 最终离线门禁：`uv lock --check` 通过（46 packages）；Ruff format 44 files、lint、严格
  mypy 27 source files、pytest `85 passed, 1 skipped in 5.43s`、`git diff --check` 通过；
  唯一 skip 仍是显式 live contract，生产源码仍恰好一个 Tool。
- 未访问 Open-Meteo live API、未触发 GitHub Actions、未登录 PyPI、未配置 Pending
  Publisher、未创建/推送 tag、未上传、commit、push 或创建 PR。当前等待 Step 4。

## R-001 / Step 4 独立 QA、新 live contract 与用户 UAT 门禁

日期：2026-08-12

- 独立枚举并审查 10 个已跟踪变更和 3 个未跟踪文件；普通 `git diff` 与未跟踪清单均纳入。
  `src/`、`pyproject.toml`、`uv.lock`、`server.json`、`CHANGELOG.md`、LICENSE 和 NOTICE 无变更。
- 发现一个中优先级供应链缺口：`.github/workflows/release.yml` 原先在
  `uv build --no-sources` 后直接上传制品，没有执行项目已有的制品白名单与元数据检查。
- 最小修复为在上传前增加 `git diff --check` 和
  `uv run python tests/packaging/inspect_artifacts.py dist`，并扩展发布契约，固定
  build -> inspect -> upload 顺序。定向契约结果为 `9 passed`。
- 复审 Step 3 固定候选
  `E:\mcp-weather-query-release-candidate\0.1.0\r001-step3-20260812T003655`：wheel 保持
  15 files、16,523 bytes、SHA-256 `e95429d4744e14f36efeecc08833269a0c72202bfdf4f9e3255412c73d225b6e`；
  sdist 保持 14 files、12,107 bytes、SHA-256
  `e824aa4c64cb7e202d60cbd6fe3f0920043401789b1f755967285cb76ee15b63`。
- 两套项目外安装再次通过 provenance、MCP 2026-07-28 modern discovery、Legacy
  2025-11-25 production handshake、唯一 `get_current_weather`、确定性
  `structuredContent`、stdout 仅协议、stderr 边界和退出码 0；没有重建或替换制品。
- 显式设置 `MCP_WEATHER_RUN_LIVE=1` 后运行
  `uv run pytest -q --tb=short tests/integration/test_open_meteo_live.py`，新的 Open-Meteo
  live contract 结果为 `1 passed in 2.73s`。只访问获准的固定官方端点，未保存完整响应、
  用户位置或凭据；随后清除 live 开关。
- 完整离线门禁为 `85 passed, 1 skipped`，唯一 skip 是默认关闭的 live contract；
  `uv lock --check`、Ruff format/lint、严格 mypy、`git diff --check` 和范围扫描均通过。
- QA 确认仍只有一个只读 Tool；没有 HTTP/SSE/Streamable HTTP、任意 URL、secret/token、
  TestPyPI、GitHub Release、Registry 或额外发布路径。
- 用户在固定 wheel 环境执行验收并明确确认通过。截图证据显示 artifact 来源为固定
  `mcp_weather_query-0.1.0-py3-none-any.whl`，distribution 为 `mcp-weather-query==0.1.0`，
  模块来自该环境 `site-packages`；MCP 2026-07-28 discovery/确定性调用与 Legacy
  2025-11-25 production console 均只发现 `get_current_weather`，`structured_content=true`、
  `stdout_protocol_only=true`、`stderr_traceback=false`、exit code 0。
- 未触发 GitHub Actions，未登录 PyPI、配置 Pending Publisher/GitHub environment、创建 tag、
  上传制品、commit、push 或 PR。Step 4 已完成，等待用户明确允许进入 Step 5。

## R-001 / Step 5 Git/PR 交付（PR CI 待完成）

日期：2026-08-12

- 用户明确允许进入 R-001 Step 5 Git/PR 交付；该授权不包含 PyPI 登录、Publisher 配置、
  tag、发布 job、制品上传、合并或 Step 6。
- 刷新远程后确认 `main == origin/main == 0d5d7be9271b71143cdbcdf768bfbde5ed4393d0`，
  当前分支为 `release/r-001-pypi-0.1.0`，全部 13 个文件均属于 R-001。
- 提交前门禁通过：46 packages、Ruff format 44 files、lint、严格 mypy 27 source files、
  pytest `85 passed, 1 skipped in 5.49s`、`git diff --check`；唯一 skip 为默认关闭的 live contract。
- 精确暂存 13 个文件并通过 `git diff --cached --check`；未包含构建产物、日志、凭据、
  本机配置、`src/`、`pyproject.toml`、`uv.lock`、`server.json` 或 CHANGELOG 变更。
- 创建提交 `5f245ee6acc382400b28c557388a4aa114a9fb53`：
  `ci(release): prepare trusted PyPI publishing`，并推送远程同名分支。
- GitHub 连接器创建 PR 时发生传输错误且未产生 PR；按已批准 GitHub 交付流程使用已认证
  `gh` 后备，创建以 `main` 为目标的 Draft PR #7：
  `https://github.com/wcnm8888/mcp1-weather-query/pull/7`。
- PR 初始检查只出现 `Validate and build distributions`，没有 publish job；当前仍需等待
  最新文档提交对应的 PR CI 完成后，才能把 Step 5 写成通过。
- 提交 `144c7fd` 的 PR CI build job 首次成功，publish job 为 skipped，但 GitHub 标注旧
  `actions/upload-artifact` v5 使用已弃用 Node.js 20。官方只读核验确认当前最新
  upload v7.0.1 SHA 为 `043fb46d...d1fc6a0a`，download v8.0.1 SHA 为
  `3e5f45b2...a5461e7c`，二者均声明 Node.js 24。
- 为避免当前 build 告警和未来 publish job 的同类风险，最小更新 upload/download 两个
  action SHA 及静态 allowlist；定向契约 `9 passed`，完整离线门禁仍为
  `85 passed, 1 skipped`。等待该修复提交对应的新 PR CI，不复用旧 run 冒充最终证据。
- 修复提交 `b5b1ff3430bd6ea15be735ec0e925e664bceb9d3` 对应 PR run
  `31516139712` 完成且结论为 success。`Validate and build distributions` 的 setup、锁文件、
  Ruff、严格 mypy、默认离线测试、patch whitespace、wheel/sdist 构建、制品检查与 artifact
  上传全部成功；`Publish distributions to production PyPI` 结论为 skipped、零步骤。
- build check annotations 返回空数组，旧 Node.js 20 告警已消失。PR #7 保持 Draft，目标
  `main`、merge state clean；未创建 tag、未请求发布 OIDC、未登录/配置 PyPI 或上传公开制品。
- Step 5 已完成，当前停止在用户审查/合并 Draft PR #7 的门禁；PR 合并不等于 PyPI 发布，
  合并后仍需用户明确允许进入 Step 6。

## R-001 / Step 6 合并同步、名称复核与 Publisher 配置（已完成）

日期：2026-08-12

- 用户确认 PR #7 已合并并明确允许进入 Step 6；GitHub API 核验 merge commit 为
  `7cc304b47a094a33ccb90b13f411547a6a255e99`。
- 本地从干净工作树切换 `main`，以 fast-forward 同步到 `origin/main`；两者精确一致。
- 合并后门禁通过：46 packages、Ruff format 44 files、lint、严格 mypy 27 source files、
  pytest `85 passed, 1 skipped in 11.84s`、`git diff --check`；唯一 skip 为默认关闭的 live contract。
- 只读请求 PyPI 官方 JSON endpoint `https://pypi.org/pypi/mcp-weather-query/json` 返回 HTTP 404，
  表明当前没有该公开项目。按 PyPI 官方文档，Pending Publisher 在首次使用前不会创建项目或
  预留名称，因此 Step 7 前必须再次复核。
- GitHub 仓库仍为 private。通过 GitHub API 创建并复核 environment `pypi`；当前没有 secrets、
  protection rules 或 deployment branch policy。该配置不会自行触发 workflow 或发布。
- 精确 Pending Publisher tuple 仍为：PyPI project `mcp-weather-query`、owner `wcnm8888`、
  repository `mcp1-weather-query`、workflow `release.yml`、environment `pypi`。
- PyPI 官方 Publishing 页面在自动化会话中连续导航超时后，由用户本人在已登录的官方页面
  完成配置；未读取或记录密码、2FA、Cookie 或其他凭据。
- 用户提供的成功页面截图显示 Pending Publisher 已加入，精确字段为：project
  `mcp-weather-query`、publisher `GitHub`、repository `wcnm8888/mcp1-weather-query/`、
  workflow `release.yml`、environment `pypi`，与批准 tuple 完全一致。
- 页面同时明确提示 Pending Publisher 不会预留名称；项目需在首次可信发布成功后才创建。
- 未创建或推送 `v0.1.0`，未触发 publish job，未上传 wheel/sdist，项目仍未发布。
- Step 6 已完成，当前等待用户明确授权 Step 7；本证据不授权 tag 或发布。

## R-001 / Step 7 发布元数据修复门禁

日期：2026-08-12

- 用户明确授权进入 Step 7，并确认 PyPI 邮箱已验证。PR #8 已合并，merge commit 为
  `fb986bdda4fdba41327165f2f569fdd8c7d9d6a7`；本地 `main` 已 fast-forward 到同一提交。
- PR #8 build/QA 成功、publish job 在 PR 事件中明确 skipped；本地和远程都不存在
  `v0.1.0`。PyPI 官方 JSON endpoint 再次返回 404，说明名称仍未被公开项目占用。
- 最终离线门禁初次通过 `85 passed, 1 skipped` 和发布契约 `9 passed`，随后发现一个发布
  阻断缺陷：嵌入 PyPI 长描述的 README 仍称“当前尚未发布”，CHANGELOG 仍为
  `0.1.0 - Unreleased`，且制品/发布契约强制保留该状态。
- 因 PyPI 已上传版本文件不可覆盖，在 tag 前停止；用户授权创建独立发布元数据修复 PR。
- 修复将 README 改为由 PyPI 官方项目页核验公开可用性、文件和 attestation，将 CHANGELOG
  日期固定为 `2026-08-12`，同步制品/发布契约，并继续明确 MCP Registry 尚未登记。
- 定向契约结果为 `29 passed`。项目外以 `uv build --no-sources --offline` 重建：wheel
  15 files / 16,485 bytes / SHA-256 `48909c4c...3e4387`；sdist 14 files / 12,066 bytes /
  SHA-256 `ea8fa9cb...77b0c`。文件白名单、Core Metadata 2.4、README、LICENSE/NOTICE、
  wheel RECORD、本机路径和敏感信息扫描全部通过。
- 候选目录：
  `E:\mcp-weather-query-release-candidate\0.1.0\r001-step7-metadata-20260812T132608`。
- 修复后的完整离线门禁通过：46 packages、Ruff format 44 files、lint、严格 mypy 27 files、
  pytest `85 passed, 1 skipped in 5.71s`、`git diff --check`；唯一 skip 为显式 live contract。
  仍恰好一个 Tool，源码/包配置没有 HTTP/SSE，候选哈希复审不变。
- 创建提交 `8a74760` 并推送 `agent/r-001-step7-release-metadata`，形成 Draft PR #9。
  PR 正文回读问号乱码为 0，变更精确为 14 个获准文件。
- run `31566777632` 的 `Validate and build distributions` 成功；
  `Publish distributions to production PyPI` 在 PR 事件上明确 skipped。
- 本阶段尚未创建 tag、触发 OIDC publish 或上传 PyPI；当前等待用户合并 PR #9。

## R-001 / Step 7 最终发布

日期：2026-08-12

- 用户合并 PR #9 后，本地 `main` fast-forward 到
  `bb24624dcc8eb2efce5f4c49c80c850542c4d2b3`，与 `origin/main` 一致且工作树干净。
- tag 前 PyPI 官方 JSON 查询仍为 404；最终离线门禁通过：lock、Ruff format/lint、严格
  mypy、`85 passed, 1 skipped`、发布契约 `9 passed`、diff、唯一 Tool 和无 HTTP/SSE。
- 从合并后的 main 在项目外重建并审查最终候选；wheel 15 files、sdist 14 files，
  Metadata 2.4、README、LICENSE/NOTICE、文件白名单和敏感信息检查通过。
- 创建并推送唯一 `v0.1.0`，精确指向 `bb24624dcc8eb2efce5f4c49c80c850542c4d2b3`。
- GitHub Actions run `31567283749` 由该 tag push 触发；`Validate and build distributions`
  与 `Publish distributions to production PyPI` 均成功。认证为 GitHub OIDC Trusted
  Publishing；没有长期 PyPI Token、TestPyPI、GitHub Release 或 Registry 写入。

## R-001 / Step 8 公开 PyPI 与安装复验

日期：2026-08-12

- PyPI 官方版本 API 确认 `mcp-weather-query==0.1.0` 公开且未 yank；Python 范围为
  `>=3.12,<3.13`，License expression 为 MIT，三项运行依赖和公开 README 符合契约。
- 公开 wheel 为 16,341 bytes、SHA-256
  `7c305d46f1cb6d2d5072625f0aacdc6d2bc102ef39237f267a56bdfa83d8de8a`；公开 sdist 为
  11,931 bytes、SHA-256
  `573c7d4887d640714ba00f4d634d9300e7e763348025bfbd85088f9bd670ea25`。
- PyPI Integrity API 的两个 provenance 均绑定 GitHub repository
  `wcnm8888/mcp1-weather-query`、workflow `release.yml`、environment `pypi`；证书 claims
  进一步对应 `refs/tags/v0.1.0`、发布提交和 run `31567283749`。
- `pypi-attestations 0.0.30` 在线 TUF 刷新首次因 Windows 符号链接权限 `WinError 1314`
  停止；没有提权或修改系统。随后使用该官方工具支持的 `--offline` TUF 模式、PyPI 官方
  provenance 文件和已校验制品完成密码学验证，wheel 与 sdist 均返回 `OK`。
- 验证根位于
  `E:\mcp-weather-query-release-verification\0.1.0\step8-20260812T141500`；制品和临时环境
  均在项目外，未进入 Git。
- 公开 wheel/sdist 分别安装到全新 `wheel-env`/`sdist-env`，无 `PYTHONPATH`、
  `PYTHONHOME` 或活动 `VIRTUAL_ENV` 注入；模块来自各自 `site-packages`，console 来自各自
  `Scripts\mcp-weather-query.exe`。
- 两套环境均只发现 `get_current_weather`；官方 v2 Client 为 MCP `2026-07-28`，生产
  console Legacy 握手为 `2025-11-25`；确定性调用返回合法 `structuredContent`，stdout
  仅协议消息、stderr 无 traceback、退出码 0，且无遗留进程。
- 从 PyPI 下载的实际 wheel/sdist 再次通过项目制品白名单检查器：wheel 15 files、sdist
  14 files，Metadata 2.4 与当前源码/README/法律文件一致。

## R-001 / Step 9 发布后文档与 Git 收口

日期：2026-08-12

- 将 R-001 完整任务卡归档到
  `docs/archive/task-cards/R-001-PyPI首次外部发布.md`，重置 current-task 与实施计划为无活动任务。
- README、文档地图、roadmap、progress、QA 清单、release plan 与本证据同步到真实公开状态。
- R-001 关闭后仍未登记 MCP Registry、创建 GitHub Release、发布新版本或启动 R-002。
- 本节随独立文档收口 PR 交付；PR 合并前，`main` 中的治理文档仍是旧状态。

## R-002 / Step 0 文档治理与任务基线

日期：2026-08-12

- 用户批准 R-002 目标、范围、非目标、L 级风险判断、15 项决策、测试矩阵、Step 地图和
  完成定义，并明确允许进入 Step 0；该授权不包含 publisher、OAuth、Terms 或 Registry 写入。
- `git fetch origin --prune` 后确认 `main` 与 `origin/main` 均为
  `2fae2579517ebb5f7154f9646b54b4f174be6ffa`，起始工作树干净、远程为
  `wcnm8888/mcp1-weather-query`。
- `v0.1.0` 是附注标签；解引用 `refs/tags/v0.1.0^{}` 后精确指向发布提交
  `bb24624dcc8eb2efce5f4c49c80c850542c4d2b3`。
- 环境复核为 uv 0.6.14、项目 `.venv` Python 3.12.10、Node 22.16.0；没有更新或覆盖工具、
  依赖、系统环境或 Cherry Studio 管理的 uv。
- Step 0 前离线门禁通过：`uv lock --check`、Ruff format 45 files、lint、严格 mypy
  27 source files、pytest `85 passed, 1 skipped in 5.91s`、`git diff --check`；唯一 skip 是
  默认关闭的 Open-Meteo live contract。
- 从该基线创建本地 `release/r-002-mcp-registry-0.1.0`，未提交或推送。
- R-001 QA 原文安全归档到 `docs/archive/qa/R-001-PyPI首次外部发布-QA.md`；R-002 任务卡、
  活动 QA、实施计划、roadmap、progress、文档地图和项目规则同步到 Step 0 真实状态。
- 文档落盘后完整离线门禁再次通过：Ruff format 46 files、lint、严格 mypy 27 source files、
  pytest `85 passed, 1 skipped in 5.26s`、lock 与 `git diff --check`；相对 Markdown 链接检查通过。
- 未修改 `src/`、`tests/`、`.github/`、`pyproject.toml`、`uv.lock` 或 `server.json`；未运行
  `mcp-publisher`，未访问 Registry validate/login/publish，未接受 Terms，未产生外部写入。
- 当前停止在 Step 1 授权门禁；Step 0 完成不代表 Registry 已登记。

## R-002 / Step 1 先失败的 Registry 发布契约

日期：2026-08-12

- 用户明确允许进入 Step 1；范围只包含静态离线 RED 契约，不包含 `server.json`/README/
  release plan 实现、publisher、联网 validate、OAuth、Terms 或 publish。
- 新增 `tests/release/test_mcp_registry_publish_contract.py`，共 10 项契约，覆盖公开身份、唯一
  PyPI/stdio package、公开条款、OAuth 分段授权、Step 生命周期、不可变版本恢复、固定 publisher、
  CI 无 Registry 路径和 manifest 无凭据/远程传输。
- 新文件的 Ruff format/lint 和严格 mypy 通过；定向 pytest 为 `6 failed, 4 passed in 0.19s`。
- 四个通过项确认：当前 `server.json` 与 PyPI 0.1.0/ownership marker 一致；packages 精确为
  一个 `uvx` stdio 项；现有 GitHub workflow 不含 Registry validate/login/publish；manifest
  不含 credential、remote transport 或扩展参数。
- 六个红灯确认：根 README 尚未标记 R-002 active；release plan 尚缺 preview/CC0 公开边界、
  手工 GitHub OAuth device flow 与 login/publish 分离、Step 3/7/8/9 顺序、同版本不可变和不确定
  publish 的先查后停恢复、以及禁止重新下载已验证 publisher 的明确文字。
- 完整默认套件按预期返回退出码 1：`6 failed, 89 passed, 1 skipped in 5.91s`；排除新 RED
  文件后的既有回归返回退出码 0：`85 passed, 1 skipped in 5.59s`。唯一 skip 是默认关闭的
  Open-Meteo live contract；没有导入、收集、环境或现有功能回归错误。
- 未修改 README、release plan、`server.json`、业务源码、workflow、依赖或锁文件；未运行
  publisher、未联网、未登录、未接受 Terms、未写入 Registry，也未 commit、push 或创建 PR。
- Step 1 已完成，当前等待用户允许 Step 2 以最小实现使六个红灯转绿。

## R-002 / Step 2 最小 Registry 发布文档实现

日期：2026-08-12

- 用户明确允许进入 Step 2；实现范围限制为使 Step 1 六个文档红灯转绿，不运行 publisher、
  联网 validate、OAuth、Terms 或 Registry publish。
- README 新增 R-002 已进入准备阶段但 Registry 仍未登记的真实状态，并明确任务启动不代表
  Registry 条目存在；保留 PyPI ownership marker 和未登记边界。
- release plan 新增 preview、CC0 1.0、公开 GitHub 用户名/metadata、private repo 与公开 PyPI
  安装来源边界；固定手工 GitHub OAuth device flow，明确 login 不授权 publish，且不配置
  Registry GitHub Actions workflow/environment。
- 网络门禁精确拆分为 Step 3 validate、Step 7 login、Step 8 publish、Step 9 官方 API；每步
  分别授权并停止，不得合并。
- 恢复契约明确同版本不可原地覆盖；不确定 publish 不得盲目重试，先以官方 API 精确查询，
  对完全一致和不一致结果分别停止；deprecated/deleted 不视为数据擦除。
- 固定复用项目外官方 `mcp-publisher v1.8.1` 和 SHA-256
  `399ad0d6e00a50812b563a71d8bfbff5160c085e6b13aac6ec083d98d5ff7c45`；不下载、替换、
  安装、更新或加入 PATH。
- Step 1 契约未删除、跳过、xfail 或放宽；定向结果由 `6 failed, 4 passed` 转为
  `10 passed in 0.03s`。
- 完整离线门禁通过：46 locked packages、Ruff format 47 files、lint、严格 mypy 28 source
  files、pytest `95 passed, 1 skipped in 5.54s`、`git diff --check`；唯一 skip 是默认关闭的
  Open-Meteo live contract，生产源码仍恰好一个 Tool 且无 HTTP/SSE。
- 当前 `server.json` 已通过身份、唯一 PyPI/stdio package 和无 secret/remote transport 契约，
  因此未修改；业务源码、workflow、依赖和锁文件也未变化。
- 未运行 publisher、未联网 validate、未登录、未接受 Terms、未写入 Registry，也未 commit、
  push 或创建 PR。Step 2 已完成，等待用户允许 Step 3。

## R-002 / Step 3 固定 publisher、schema 与无写入 validate

日期：2026-08-12

- 用户明确允许进入 Step 3；授权只包含官方一手来源核验、现有项目外 publisher 复核和一次
  联网但无写入的 validate，不包含 Terms、OAuth、login 或 publish。
- GitHub 官方 Releases API 直接返回 latest/tag 均为 `v1.8.1`，发布时间
  `2026-08-06T23:35:18Z`。官方 Windows AMD64 asset 名为
  `mcp-publisher_windows_amd64.tar.gz`，大小 7,547,008 bytes，digest 为
  `sha256:399ad0d6e00a50812b563a71d8bfbff5160c085e6b13aac6ec083d98d5ff7c45`。
- 项目外现有归档大小和 SHA-256 与官方 asset 完全一致，没有重新下载。解包后二进制大小
  20,393,472 bytes、SHA-256 `d021e6496bd10e5be4264e865f795c1c9802501699342a838b601f0f4d383fd5`；
  `--version` 退出码 0，自报 `mcp-publisher 1.8.1`、commit
  `f52dc8525a441a3abf5fedc9912152d95af5aab1`、built `2026-08-06T23:36:13Z`。
- `Get-Command mcp-publisher` 返回 false；工具仍未加入 PATH，也未修改项目、系统或 Cherry
  Studio 管理环境。
- 官方 `https://static.modelcontextprotocol.io/schemas/2025-12-11/server.schema.json` 返回
  HTTP 200，`$id` 与项目 `server.json` 的 `$schema` 完全一致；本次响应 SHA-256 为
  `3fba09590c99f61735d234822279f4223fab9e300c0a81e81c91ab62a4114de0`。
- 2026-08-12T07:23:32Z 至 07:23:34Z 只运行一次固定二进制 `validate`。退出码 0，安全输出为
  `Validating against https://registry.modelcontextprotocol.io...` 和 `server.json is valid`。
- validate 前后 `server.json` SHA-256 均为
  `e0ad8ae8339d629629d7eef37f3927f081519e840eb85bfcf3297ba2bd6c6709`，Git status 完全一致；
  没有本地文件或 Registry 条目写入。
- 文档收口后的完整离线门禁通过：46 locked packages、Ruff format 47 files、lint、严格
  mypy 28 source files、pytest `95 passed, 1 skipped in 5.79s`、`git diff --check`；唯一 skip
  是默认关闭的 Open-Meteo live contract，生产源码仍恰好一个 Tool。
- 未执行 OAuth、Terms、login、publish、Registry API 登记查询或第三方目录操作；未 commit、
  push 或创建 PR。Step 3 已完成，等待用户允许 Step 4。

## R-002 / Step 4 独立 QA、metadata 冻结与 PyPI marker（UAT 待确认）

日期：2026-08-12

- 用户明确允许进入 Step 4；授权包含独立 QA、metadata 冻结、生产 PyPI/官方 Terms 只读复核
  和用户 UAT，不包含 readiness PR、Terms 接受、OAuth、login 或 publish。
- `git fetch origin --prune` 后确认分支起点仍为
  `main == origin/main == 2fae2579517ebb5f7154f9646b54b4f174be6ffa`。独立审查 11 个
  已跟踪差异及两个未跟踪文件；后者精确为 R-001 QA 归档和 R-002 Registry 契约测试。
- 发现并修复三处低风险文档漂移：根 README 与 docs 文档地图仍记录旧的 `85 passed`，任务卡
  仍称未执行 validate。均只做事实修正，没有高、中优先级范围内缺陷。
- `server.json` 未修改。原始文件 627 bytes，SHA-256
  `e0ad8ae8339d629629d7eef37f3927f081519e840eb85bfcf3297ba2bd6c6709`；按键排序、紧凑 UTF-8
  JSON 的规范化语义 SHA-256 为
  `7363235e462331ea3ea12914eacd959a43bb6fb556caad35ff087983d5e39f0d`。静态契约新增该语义
  digest 断言，避免 CRLF/缩进导致假漂移。
- 生产 PyPI 0.1.0 官方 JSON 返回 HTTP 200；名称/版本、Python `>=3.12,<3.13`、MIT、唯一
  `mcp-name: io.github.wcnm8888/mcp1-weather-query` marker 和“尚未登记/不代表条目存在”边界通过。
  wheel/sdist 均未 yank，SHA-256 分别仍为 `7c305d46...d8de8a` 和 `573c7d48...f9bd670ea25`。
- 第一次 Python stdlib PyPI 请求发生 `SSL: UNEXPECTED_EOF_WHILE_READING`；随后仅对同一 PyPI
  官方端点以 PowerShell 复核。一次 QA 断言使用了错误中文词序，真实返回 HTTP 200 但断言失败；
  按公开 README 实际词序“尚未登记 MCP Registry”修正检查后通过，未隐瞒失败或改动公开包。
- Official Registry Terms 官方源文件返回 HTTP 200，有效日期为 2025-09-02；preview/data reset、
  CC0 1.0、公开 metadata/GitHub username 和仅对 Registry Data 适用的范围均存在。本次响应
  SHA-256 为 `b810666747d1271633fbdd56e9b7b859a788b345fc5d57901f611a87b6fd6afc`。
- 独立离线 QA 通过：46 locked packages、Ruff format 47 files、lint、严格 mypy 28 source
  files、pytest `95 passed, 1 skipped in 5.46s`、Registry 契约 `10 passed in 0.05s`、diff、
  唯一 Tool、无 HTTP/SSE、无 Registry CI 路径和无默认 live 请求均通过。
- 未修改 `server.json`、业务源码、workflow、依赖、锁文件、CHANGELOG、License 或 NOTICE；
  未运行 publisher、login、publish，未接受 Terms，未写入 Registry，也未 commit、push 或创建 PR。
- 独立 QA 收口时用户 UAT 尚未确认，因此当时没有把 Step 4 标记完成；后续确认见下节。

### Step 4 用户 UAT

- 用户明确回复 `R-002 Step 4 UAT 通过`。
- 用户接受冻结 Registry 身份、PyPI 0.1.0/uvx/stdio/private repository 边界，以及 preview、
  data reset、CC0 1.0、公开 metadata/GitHub username 和同版本不可原地覆盖风险。
- 用户接受不确定 publish 必须先以官方 API 查询、不得盲目重试，deprecated/deleted 不等于擦除。
- 该 UAT 只完成 Step 4，不授权 Step 5 readiness Git/PR、Terms 接受、OAuth login 或 publish。
- UAT 状态落盘后复跑完整离线门禁：Ruff format 47 files、lint、严格 mypy 28 source files、
  pytest `95 passed, 1 skipped in 5.71s`、lock 与 `git diff --check` 全部通过。
- R-002 Step 4 已完成，当前等待用户明确允许进入 Step 5。

## R-002 / Step 5 readiness Git/PR 交付

日期：2026-08-12

- 用户明确允许进入 Step 5 readiness Git/PR 交付。
- 授权范围仅包括复核并精确提交当前冻结的 R-002 readiness 变更、推送
  `release/r-002-mcp-registry-0.1.0` 和创建 Draft PR；不授权自行合并。
- 本 Step 不接受 Registry Terms，不执行 GitHub OAuth、`mcp-publisher login/publish` 或任何
  Registry 写入，也不修改 `server.json`、业务源码、workflow、依赖或锁文件。
- 精确提交 13 个已审查文件，首个提交为
  `4d262c3648cb0f13b0b8cd350a94717d88b2c0a8`（`feat(registry): prepare R-002 readiness`），
  并推送到 `origin/release/r-002-mcp-registry-0.1.0`。
- GitHub 连接器因私有仓库可见性返回 404；按交付流程回退到已认证的 GitHub CLI，成功创建
  Draft PR #11：`https://github.com/wcnm8888/mcp1-weather-query/pull/11`，目标为 `main`。
- 提交 `00488f27627f2c7bc8167ec24009a9f513449e32` 记录 PR 交付事实；其 GitHub Actions
  run `31575380396` 成功，`Validate and build distributions` 的 lock、Ruff、严格 mypy、默认
  离线测试、patch whitespace、wheel/sdist 构建与制品审查全部通过。
- 同一 PR run 的 `Publish distributions to production PyPI` 作业明确跳过；没有 Registry
  login/publish 作业或命令，也没有外部 Registry 写入。
- Step 5 已完成，当前停止在用户审查/合并 Draft PR #11 的门禁；合并不授权 Step 6 及后续
  Terms、OAuth、login 或 publish。

## R-002 / Step 6 合并后同步、Registry 空状态与认证边界

日期：2026-08-12

- 用户确认已合并 PR #11，并明确允许进入 Step 6；该授权不包含 Terms 接受、OAuth login、
  publish 或 Registry 写入。
- GitHub 返回 PR #11 状态 `MERGED`，合并时间 `2026-08-12T07:51:46Z`，merge commit 为
  `900f71133ad9525ff65965d0822a1e92d06faead`。工作树干净时切换到 `main`，以
  `git pull --ff-only origin main` 同步；同步后 `main == origin/main == 900f711...`。
- 只读请求 Official Registry：包含 `include_deleted=true` 的精确名称搜索返回 HTTP 200、
  `servers=[]`；精确 `io.github.wcnm8888/mcp1-weather-query` / `0.1.0` detail 返回 HTTP 404。
  因此当前没有 active、deprecated 或 deleted 的同名版本。
- Registry version 端点返回 HTTP 200、服务 `1.8.1`、commit `f52dc852...`。官方 API 文档仍说明
  `io.github.*` 发布采用 GitHub OAuth，读取无需 login；快速入门仍将 `login github` 与
  `publish` 分成两个命令。
- Terms 官方源文件返回 HTTP 200、7,448 bytes，SHA-256 仍为
  `b810666747d1271633fbdd56e9b7b859a788b345fc5d57901f611a87b6fd6afc`；有效日期仍为
  2025-09-02，preview/data reset、CC0 1.0、公开 GitHub username 和仅 Registry Data 适用
  的边界均存在。
- 首次计算 Terms 哈希时调用了当前 PowerShell/.NET 不支持的静态 `SHA256.HashData`，只导致
  本地摘要变量为空；未产生写入。改用 `SHA256.Create().ComputeHash()` 后得到上述既有摘要。
- 固定项目外 publisher 存在、自报 `mcp-publisher 1.8.1`，且 `Get-Command mcp-publisher`
  仍为 false。只运行 `--version` 和 `login --help`，没有启动 device flow，也没有读取或记录
  token、Cookie、设备码或认证缓存。
- 完整离线门禁通过：46 locked packages、Ruff format 47 files、lint、严格 mypy 28 source
  files、pytest `95 passed, 1 skipped in 5.87s`、Registry 定向契约 `10 passed in 0.05s`、
  diff、唯一 Tool、生产源码无 HTTP/SSE/print、无 Registry CI 路径均通过。
- Step 6 已完成；当前停止在用户单独允许 Step 7 GitHub OAuth login 的门禁。login 成功也不
  授权 Step 8 publish。

## R-002 / Step 7 GitHub OAuth login

日期：2026-08-12

- 用户明确授权使用固定 `mcp-publisher v1.8.1` 执行 GitHub OAuth login，并要求认证成功后
  立即停止，不执行 publish。
- 登录前确认 `MCP_GITHUB_TOKEN` 不存在、`~/.config/mcp-publisher/token.json` 不存在；Registry
  health 返回 200 且 GitHub client ID 已配置。
- 固定 CLI 通过当前回环代理访问 `github.com/login/device/code` 时，两次返回 EOF、一次挂起
  超过两分钟。挂起进程已停止，没有遗留 publisher、设备码或认证文件；进程级禁用 HTTP/2
  仍返回 EOF。PowerShell 对同一官方 endpoint 的只读/临时 device 请求成功，证明服务可用。
- 根因是当前环境的 `HTTP_PROXY`/`HTTPS_PROXY` 指向本机回环代理，而 Go CLI 对该代理路径的
  GitHub device-code POST 不兼容。最终仅为一次固定 publisher 子进程设置
  `NO_PROXY=github.com`；未修改系统或全局环境，也未改用 PAT、OIDC 或其他认证方法。
- CLI 成功生成一次性 device code；设备码只经系统剪贴板交给用户，没有输出到聊天、日志、
  文档或 Git。用户在 GitHub 页面确认设备连接成功。
- 固定 CLI 完成 GitHub token 到生产 Registry JWT 的交换并安全写入既定配置文件，然后退出。
  只读取非敏感 JWT 声明：`auth_method=github-at`、身份匹配 `wcnm8888`、权限为
  `publish io.github.wcnm8888/*`、有效期 300 秒；未输出或记录 token 本体、Cookie 或设备码。
- 登录后 Official Registry 精确名称查询返回 HTTP 200、0 条；没有 publisher 后台进程，证明
  未执行 publish 或创建 Registry 条目。剪贴板不再保留设备码。
- Step 7 已完成并立即停止。当前等待用户单独允许 Step 8；由于 JWT 只有 300 秒，若届时已
  过期，Step 8 授权还需明确包含一次重新 GitHub OAuth login。

## R-002 / Step 8 唯一一次 Registry publish

日期：2026-08-12

- 用户明确授权：现有 JWT 过期时允许重新执行 GitHub OAuth，认证成功后只对冻结
  `server.json` 执行一次 publish，并要求完成后停止、不进入 Step 9。
- 第一次重新 login 已生成 device flow，但在用户完成授权前 exit 1；第二次在生成 device
  flow 前遇到网络错误。两次均没有进入发布段，publisher 进程归零，凭据文件未更新，
  Registry 精确查询仍为 0，publish 次数为 0；每次后续重试均重新获得用户明确授权。
- 第三次由用户预先打开 GitHub Device Activation 页面并明确授权。一次性设备码只写入系统
  剪贴板，未出现在聊天、日志、文档或 Git；用户截图确认 device success，CLI login 成功。
- 登录后的辅助冻结脚本因错误地给规范化 JSON 追加 LF，得到 `8997a571...032a66` 并安全停止，
  尚未调用 publish。随后只读复核证明原始 SHA-256 仍为
  `e0ad8ae8339d629629d7eef37f3927f081519e840eb85bfcf3297ba2bd6c6709`，无换行规范化语义
  SHA-256 仍为 `7363235e462331ea3ea12914eacd959a43bb6fb556caad35ff087983d5e39f0d`；
  误报来自辅助口径，不是 manifest 漂移。
- 在同一有效 JWT 内，仅调用一次固定 `mcp-publisher v1.8.1 publish`。CLI 退出码 0，安全输出
  明确为 `Successfully published` 和 server `io.github.wcnm8888/mcp1-weather-query`
  version `0.1.0`。没有第二次 publish，也没有在本 Step 提前执行公开 API/安装复验。
- 未输出 token、Cookie 或设备码；未修改 `server.json`、源码、依赖、workflow、PyPI 版本、
  tag、Release、仓库可见性或其他目录平台。项目外辅助脚本含已知 LF 口径错误，不得原样复用。

## R-002 / Step 9 Official Registry API 与公开安装复验

日期：2026-08-12

- 用户单独允许进入 Step 9；本 Step 只读访问 Official Registry API 和生产 PyPI，不执行
  login、publish、logout、凭据删除、live Open-Meteo、Inspector 或其他外部写入。
- `2026-08-12T09:27:26Z`，Official Registry `v0.1/servers` 精确名称、版本并包含 deleted 的
  查询返回 HTTP 200、恰好 1 条；状态为 active、`isLatest=true`，`publishedAt` 为
  `2026-08-12T09:25:56.19196Z`。
- 返回 server 的名称、`0.1.0`、schema、标题、描述、GitHub repository、唯一 PyPI package
  `mcp-weather-query==0.1.0`、`runtimeHint=uvx` 和 `transport.type=stdio` 与冻结
  `server.json` 完全一致；没有第二 package、remote transport 或额外版本。
- PyPI 官方 0.1.0 JSON 返回 HTTP 200：Python `>=3.12,<3.13`、MIT、三项运行依赖、唯一
  `mcp-name: io.github.wcnm8888/mcp1-weather-query` marker 均匹配。wheel/sdist 均未 yank，
  SHA-256 分别为 `7c305d46...d8de8a` 和 `573c7d48...670ea25`。
- 新建项目外验证根
  `E:\mcp-weather-query-release-verification\0.1.0\r002-step9-20260812T172900`，复用 uv 0.6.14
  和项目 managed CPython 3.12.10。清除 `PYTHONPATH`、`PYTHONHOME`、`VIRTUAL_ENV` 与 live
  开关，以 `--no-config --no-cache` 和显式 `https://pypi.org/simple` 安装精确 0.1.0；
  共解析并安装 34 个包。
- distribution 为 `mcp-weather-query==0.1.0`，`INSTALLER=uv`，没有 `direct_url.json`，证明
  不是本地文件、目录或 editable 安装；模块来自环境 `Lib/site-packages`，console 来自环境
  `Scripts/mcp-weather-query.exe`。
- 第一次验证仅因 PowerShell stdin 中的中文项目绝对路径编码偏差，无法导入测试辅助模块而停止；
  尚未启动安装包。改用子进程当前项目目录定位同一辅助模块后重跑，未改变环境或验证范围。
- 生产 console 完成 Legacy MCP 2025-11-25 initialize/tools-list，只发现
  `get_current_weather`，stdout 仅协议消息、stderr 无 traceback、退出码 0。官方 SDK v2 Client
  以 MCP 2026-07-28 完成 modern discovery；测试专用已安装包调用返回合法
  `structuredContent`，诊断只进入 stderr。验证结束后项目外环境遗留进程为 0。
- Step 9 默认离线门禁通过：46 个锁定包、Ruff format 47 files、lint、严格 mypy 28 files、
  pytest `95 passed, 1 skipped in 9.31s`、Registry 定向契约 `14 passed in 0.10s` 和
  `git diff --check`。唯一 skip 仍为显式 opt-in 的 Open-Meteo live contract；生产源码仍恰好
  一个 Tool，publisher 与验证环境遗留进程均为 0。
- 未访问 Open-Meteo live API、未运行 Inspector、未增加 Tool/HTTP/SSE、未创建新 PyPI 版本、
  GitHub Release 或社区目录条目，也未重复 Registry publish。Step 9 已完成，等待用户单独
  允许 Step 10 凭据处置、发布后文档/测试与 closure PR。

## R-002 / Step 10 凭据处置与发布后收口（closure PR 待创建）

日期：2026-08-12

- 用户明确允许 Step 10 的凭据处置、发布后文档/测试与 closure PR；该授权不包含 PR 合并、
  Step 11、再次 login/publish、Registry 状态变更或新的 PyPI/Registry 版本。
- 开始前 `git fetch origin --prune` 后确认 `main == origin/main ==
  900f71133ad9525ff65965d0822a1e92d06faead`，现有 10 个未提交文件均为 Step 6–9 的 R-002
  治理记录，没有源码、manifest、依赖、workflow 或来源不明变更。
- 固定 `mcp-publisher v1.8.1 logout --help` 明确该命令只清除保存的认证；随后只执行一次
  `logout`，安全输出为 `Successfully logged out`、退出码 0。publisher 管理的认证文件由工具
  移除，遗留 publisher 进程为 0；没有读取 token 内容或手工删除未知文件。
- 更新发布后静态契约，替换历史“未登记”断言：README 要求精确 Registry 身份、`active` 和
  官方 API 复验；CHANGELOG 要求记录 0.1.0 登记；release plan 要求记录单次 publish、公开复验
  与官方 logout。实现前定向结果为 `5 failed, 25 passed in 0.43s`，五个失败均准确命中旧文档。
- 文档修正后定向套件为 `30 passed in 0.18s`。完整离线门禁通过：46 locked packages、Ruff
  format 47 files、lint、严格 mypy 28 source files、pytest `96 passed, 1 skipped in 5.84s`、
  `git diff --check`；唯一 skip 是默认关闭的 Open-Meteo live contract。
- 为覆盖 closure PR 的 CI 构建路径，在项目外
  `E:\mcp-weather-query-release-verification\0.1.0\r002-step10-final-20260812T174654\dist`
  离线重建 wheel/sdist。更新后的制品检查器通过：wheel 15 files、SHA-256
  `cbb2728f...c3e9e5`；sdist 14 files、SHA-256 `bc01a2ff...2c6547`。制品未上传或提交。
- 从 `origin/main` 创建 `agent/r-002-step10-registry-closure`；当前正在修正文档并等待离线质量
  门禁与 Draft closure PR，R-002 仍为 active，不能标记 closed。
