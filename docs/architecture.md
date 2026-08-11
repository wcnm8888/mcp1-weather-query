# 架构说明（已确认基线）

## 规模判断

虽然代码量较小，但项目涉及 Agent Tool、结构化数据、失败兜底、新依赖、外部 API、stdio 子进程、打包和未来外部发布，按 Vibe Coding 分类规则整体为 **M 级**。用户已确认该判断；F-001 已按批准任务卡完成实现、技术验收和独立 QA，Git 交付决策仍待确认。

## 推荐技术栈

| 项目 | 推荐 | 说明 |
| --- | --- | --- |
| 语言 | Python 3.12 稳定版 | 官方 SDK 要求 Python 3.10+；避免使用本机当前的 Python 3.11.0rc2 作为发布基线 |
| 项目管理 | `uv` | 管理 Python、虚拟环境、依赖、锁文件、运行和构建 |
| MCP | 官方 `mcp` Python SDK v2 + `MCPServer` | v2 将 v1 的 `FastMCP` 重命名为 `MCPServer`；使用当前 API，不依赖 HelloAgents 自有包装 |
| 传输 | stdio | `MCPServer.run()` 的默认本地路径；首期不启用旧 SSE 或远程 HTTP |
| HTTP | `httpx.AsyncClient` | 明确超时、状态码和可替换 transport，便于测试 |
| Schema | Pydantic/类型注解 | `MCPServer` 自动生成输入/输出 Schema 并校验结构化结果 |
| 测试 | `pytest`、`pytest-asyncio`、HTTP mock/MockTransport | 单元、协议集成和子进程冒烟分层 |
| 质量 | Ruff + 静态类型检查 | 格式、lint 和类型门禁，具体工具在任务卡批准时锁定 |
| 调试 | MCP Inspector（`npx`） | 不要求全局安装，直接启动本地 stdio Server |
| 构建 | `uv build` + 标准 `pyproject.toml` build backend | 生成 wheel/sdist；build backend 在工程基线任务中确定并锁定 |

当前本机已发现 Git 2.49、系统 Node 22.16/npm+npx 10.9.2、uv 0.6.14；Python 命令指向 3.11.0rc2，`py` 启动器还引用了不可用的 Python 3.13。F-001 使用 uv 管理的稳定 Python 3.12；不得覆盖 Cherry Studio 管理的 uv 可执行文件。Inspector 兼容性复验另在项目 `.runtime/node/` 中使用经官方 SHA256 校验的 Node 24.19.0/npm+npx 11.17.0，不修改系统 PATH 或注册表。

## 最小 MCP Server

### 对外 Tool

名称：`get_current_weather`

已实现描述：

> Resolve a city or postal-code-like location and return read-only, model-based current conditions. This Tool does not provide forecasts, alerts, advice, or arbitrary URL content. Always inspect resolved_location because place names can be ambiguous.

实际输入：

| 字段 | 类型 | 必填 | 约束 | 作用 |
| --- | --- | --- | --- | --- |
| `location` | string | 是 | 去除首尾空白后 2–100 字符 | 城市名或邮编式地点查询 |
| `country_code` | string/null | 否 | ISO 3166-1 alpha-2，规范化为大写 | 缩小同名地点歧义 |

实际结构化输出：

```text
WeatherResult
├── requested_location
├── resolved_location
│   ├── name / country / country_code / admin1
│   ├── latitude / longitude / timezone
├── current
│   ├── time / interval_seconds / is_day
│   ├── temperature_c / apparent_temperature_c
│   ├── relative_humidity_percent / precipitation_mm
│   ├── weather_code / condition
│   ├── wind_speed_kmh / wind_direction_degrees
└── metadata
    ├── units
    ├── provider
    ├── model_based_current_conditions
    └── attribution / license_url
```

失败分类：

| 错误码 | 场景 | 调用方可采取的动作 |
| --- | --- | --- |
| `INVALID_LOCATION` | 空白、过短、过长或国家代码非法 | 修改参数后重试 |
| `LOCATION_NOT_FOUND` | 地理编码无结果 | 改用更完整地点或增加国家代码 |
| `UPSTREAM_TIMEOUT` | 任一步请求超时 | 稍后有限重试 |
| `UPSTREAM_RATE_LIMITED` | 上游 429 | 遵循退避，不立即循环重试 |
| `UPSTREAM_UNAVAILABLE` | 5xx、网络失败或服务不可用 | 稍后重试或报告暂不可用 |
| `UPSTREAM_INVALID_RESPONSE` | 响应缺字段或类型异常 | 不返回半真半假的天气数据，记录脱敏诊断 |

协议级未知 Tool/畸形 MCP 请求由 SDK 作为 JSON-RPC 错误处理；业务输入和上游失败应作为可供模型修正的 Tool execution error。错误文本不得包含堆栈、完整上游响应或本地路径。

Tool annotations 实际值：`readOnlyHint=true`、`destructiveHint=false`、`idempotentHint=true`、`openWorldHint=true`。这些是客户端提示，不替代固定域名、无写入代码和测试等硬边界。

## 模块边界与数据流

```text
Host / Inspector
  → stdio MCP transport
  → MCPServer + get_current_weather schema
  → weather application service
  → fixed Open-Meteo geocoding adapter
  → fixed Open-Meteo forecast adapter
  → validated WeatherResult
  → structuredContent + compatibility text content
```

| 模块 | 职责 | 不应承担 |
| --- | --- | --- |
| MCP 入口 | 使用 v2 `MCPServer` 注册 Tool、Schema、annotations、stdio 生命周期 | 拼 URL、解释上游 JSON、隐藏重试 |
| 应用服务 | 编排“解析地点 → 查询当前天气 → 组装结果” | 直接依赖 Host/Inspector |
| Open-Meteo 适配器 | 固定端点、查询参数、HTTP 状态和响应转换 | MCP 协议逻辑、任意 URL |
| 领域模型/错误 | 输入、输出、单位和稳定错误分类 | 网络 IO |
| 测试夹具 | 确定性上游样本和边界场景 | 冒充 live/生产验证 |

## 天气数据源选型

| 方案 | 优点 | 代价/限制 | 结论 |
| --- | --- | --- | --- |
| Open-Meteo 经纬度直查 | 无 Key；一次天气请求；Schema 简单 | Host/模型必须先知道坐标，用户体验弱 | 作为内部天气调用接口，不作为首期唯一用户输入 |
| Open-Meteo 城市解析 + 经纬度天气 | 无 Key；全球多语言地理编码；官方文档完整；同一提供方；能返回时区/坐标 | 两次请求；同名地点有歧义；免费层非商业、限额且无 SLA | **推荐首期方案** |
| MET Norway Locationforecast | 无 Key；全球预报；开放数据 | 只接受坐标；强制可联系的 User-Agent、缓存/流量规则；仍需独立地理编码 | 适合作为以后可替换适配器，不作为首期默认 |
| NOAA/NWS | 官方公共数据 | 主要面向美国，全球案例不合适 | 不选 |
| OpenWeather/WeatherAPI 等 Key API | 商业支持和产品功能丰富 | 需要账号/Key，增加凭证和发布门槛 | 首期不选 |
| `wttr.in` | 使用简单、城市路径直查 | 教程示例缺少明确的发布/SLA/结构化契约基线；路径拼接和响应稳定性不利于教学 | 不选 |

Open-Meteo 官方文档说明 Geocoding API 可按名称/邮编搜索，Forecast API 按 WGS84 坐标查询当前变量；免费 API 不要求 Key，但仅限非商业用途、日限 10,000 次且无可用性保证。数据采用 CC BY 4.0，需要署名。项目必须在输出/README 中保留来源与许可说明；商业化或 SLA 需求会触发重新选型或付费方案确认。

## 是否需要第二个 Tool

不需要。`list_supported_cities` 会人为制造封闭城市列表，`get_server_info` 只是展示性元数据，坐标查询也可以先作为内部适配器能力。只有真实 Host 使用反馈证明城市歧义无法接受，或出现明确的坐标输入用户场景，才把第二 Tool 作为新的 roadmap 候选，由用户单独选择。

## 当前与后续目录

```text
MCP1-天气查询/
├── AGENTS.md
├── README.md
├── LICENSE                         # 发布准备阶段
├── pyproject.toml                  # 首个实现任务
├── uv.lock                         # 首个实现任务
├── src/
│   └── mcp_weather_query/
│       ├── __init__.py
│       ├── __main__.py             # 已验证的源码 stdio 模块入口
│       ├── server.py               # MCPServer、唯一 Tool 与错误边界
│       ├── models.py               # Pydantic 输入/输出
│       ├── service.py              # 单一用例编排
│       ├── errors.py               # 稳定错误分类
│       ├── wmo.py                  # WMO code 映射
│       └── providers/
│           └── open_meteo.py       # 固定域名适配器
├── tests/
│   ├── unit/
│   ├── integration/                # Step 3/4
│   ├── smoke/                      # 真实子进程与测试专用固定 Server
│   └── fixtures/
├── docs/
│   ├── README.md
│   ├── product-brief.md
│   ├── architecture.md
│   ├── testing-strategy.md
│   ├── release-plan.md
│   ├── project-management/
│   │   ├── roadmap.md
│   │   └── current-task.md
│   └── archive/                    # 有已关闭任务时再建立
└── server.json                     # Registry 发布准备阶段，由官方工具生成/校验
```

截至 Step 6 QA，`server.py` 使用官方 v2 `MCPServer` 注册唯一 `get_current_weather`，通过可注入的查询 handler 分离协议测试与网络 IO；模块级默认 handler 才组装 Open-Meteo 服务。`__main__.py` 的 SDK 默认 stdio 入口已通过真实子进程和 Inspector 完成 Legacy initialize、现代 discovery、Tool 调用与关闭验证。

F-001 仍设置 `tool.uv.package = false`，因为打包属于 F-002。因此从源码启动模块时必须由 Host 使用项目虚拟环境 Python、`-m mcp_weather_query`、项目工作目录和绝对 `PYTHONPATH=<项目目录>\src`。真实子进程测试还使用 `tests/smoke/stdio_fixed_server.py` 注入 synthetic 结果验证 Tool call；该文件只属于测试，不是生产或未来发布入口。Open-Meteo 适配器仍固定两个 HTTPS endpoint、显式单位和有限超时，不跟随重定向、不重试、不记录响应正文；生产 `httpx.AsyncClient` 设置 `trust_env=False`，避免继承系统代理并保持固定域名直连边界。

Step 5 使用精确版本 `@modelcontextprotocol/inspector@2.1.0`，并通过 Inspector 的 `--web -e PYTHONPATH=... --cwd ... <python> -m mcp_weather_query` 连接源码入口。项目独立 Node 24.19.0 已消除 Inspector 的 engine warning，系统 Node 22.16.0 保持不变。

MCP 2026-07-28 属于现代无握手协议：请求自行携带版本/身份/能力，可选 `server/discover`，不再使用 `initialize/initialized`。Python SDK v2 同时服务现代 2026 与 Legacy 2025 客户端。生产 stdio 入口现有两条明确证据：官方 SDK v2 `Client(mode="auto")` 通过 `server/discover` 协商 2026-07-28；Inspector 2.1.0 则发送 `initialize(protocolVersion=2025-11-25)` 并进入 Legacy 兼容路径。同一 Server 同时服务两代客户端，不需要 HTTP，也不把 Inspector Legacy UI 冒充现代协议证据。

## 参考资料

- [MCP Python SDK v2](https://py.sdk.modelcontextprotocol.io/)
- [MCP Tools](https://py.sdk.modelcontextprotocol.io/servers/tools/)
- [Structured Output](https://py.sdk.modelcontextprotocol.io/servers/structured-output/)
- [Error Handling](https://py.sdk.modelcontextprotocol.io/servers/handling-errors/)
- [Open-Meteo Forecast API](https://open-meteo.com/en/docs)
- [Open-Meteo Geocoding API](https://open-meteo.com/en/docs/geocoding-api)
- [Open-Meteo Pricing / free tier limits](https://open-meteo.com/en/pricing)
- [Open-Meteo License](https://open-meteo.com/en/license)
- [MET Norway Terms of Service](https://api.met.no/doc/TermsOfService)
