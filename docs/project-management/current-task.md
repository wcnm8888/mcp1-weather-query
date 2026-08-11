# 任务卡：F-001 一个 Tool 的本地天气闭环

## 任务状态

- 状态：`approved / step_6_local_complete / awaiting_remote_pr_authorization`
- 项目等级：M
- 用户选择：已选择 F-001
- 任务卡批准：已批准（2026-08-11）
- 实现：领域/服务/Open-Meteo 适配器、唯一 MCP Tool、真实 stdio、live contract、Inspector 技术验证与独立 QA 已完成
- 当前分支：`feat/f-001-local-weather-tool`
- Git 事实：本地 `main` 已建立基线提交；功能分支已形成 F-001 精确提交；无远程、未推送、未创建 PR
- 外部发布：不在本任务范围，未授权

本文件是唯一已批准活动任务卡。Step 5 已分别证明 SDK v2 Client 的现代 MCP 2026-07-28 stdio 路径和 Inspector 的 Legacy 2025 stdio 兼容路径，并已通过用户 UAT；Step 6 本地 QA 与精确提交已完成。用户已选择远程 PR 流程，当前停在远程仓库信息和外部写入授权门禁。

## 用户目标

正在学习 MCP Server 的 Python 开发者，希望在本地使用 MCP Inspector 或兼容 Host，通过 stdio 调用一个只读的 `get_current_weather` Tool；输入城市/地点名称后，获得经过 Schema 校验、带实际解析地点、明确单位、数据时间和来源的结构化当前天气结果，并能观察可理解的失败语义。

## 业务价值

完成后，用户得到第一个真实 MCP 用户价值闭环，而不是空 Server 或静态演示：

```text
Host / Inspector 发现 Tool
→ 按 inputSchema 提交地点
→ Server 固定访问 Open-Meteo
→ 返回 outputSchema 约束的当前天气
→ 对无结果、超时、限流和上游异常给出可恢复错误
```

该闭环证明 MCP Server、Tool 设计、stdio、结构化输出、外部适配器、自动化测试和 Inspector 调试可以协同工作。

## 范围

- 建立最小 Python 3.12 + uv 工程基线和 `src/` 包结构。
- 使用官方 `mcp` Python SDK v2 的 `MCPServer`（v1 `FastMCP` 的后继 API）。
- 实现且只注册一个只读 Tool：`get_current_weather`。
- 使用 Open-Meteo Geocoding API 解析地点，再使用 Forecast API 查询 model-based current conditions。
- 使用固定 HTTPS endpoint；用户输入只能作为 query parameter，不能控制 scheme、host 或基础 path。
- 定义 Pydantic/类型化输入输出、WMO code 映射和稳定错误分类。
- 实现离线单元测试、HTTP 适配器测试、MCP in-memory 协议测试和 stdio 子进程冒烟测试。
- 执行一次显式联网 live contract 测试和 MCP Inspector 人工验收。
- 运行格式、lint、类型、测试和范围/敏感信息门禁。
- 按契约更新 README、架构、测试、进度和证据文档。

## 非目标

- 不增加第二个 Tool、天气预报、历史天气、空气质量、灾害预警或天气建议。
- 不构建 Agent、MCP Client 产品代码、LLM 调用、RAG、多 Agent、UI 或数据库。
- 不提供 Streamable HTTP、SSE、远程部署、鉴权、缓存服务、重试队列或生产 SLA。
- 不构建 wheel/sdist，不做干净环境包安装；它们属于 F-002。
- 不创建 `server.json`、CHANGELOG 或外部发布材料；它们属于 D-001。
- 不创建远程 Git 仓库，不 push、不创建 PR，不发布 TestPyPI/PyPI/Registry/社区条目。
- 不更新或覆盖 Cherry Studio 管理的 uv 可执行文件。

## 前置条件

- 当前项目：`E:\Agent\开发实践\MCP1-天气查询`
- 当前分支：`feat/f-001-local-weather-tool`。
- 当前权威文档：`AGENTS.md`、`docs/README.md`、`product-brief.md`、`architecture.md`、`testing-strategy.md`、`release-plan.md`、`roadmap.md` 和本文件。
- 已确认依赖决策：M 级、Open-Meteo、一个 Tool、地点名称输入、uv 管理 Python 3.12、F-001 优先。
- 本机事实：Git 2.49、系统 Node 22.16/npx 10.9.2、项目独立 Node 24.19.0/npm+npx 11.17.0、Cherry Studio 管理的 uv 0.6.14、系统 Python 3.11.0rc2。
- 环境边界：local development；离线测试使用 synthetic fixture/mock；一次显式 live Open-Meteo 验收；不是 production 或 production-like。
- 执行人工门禁：Step 0 至 Step 6 本地提交已获用户授权并完成；用户 UAT 已通过并已选择远程 PR；remote、push 和 PR 尚未授权。

## 工程与依赖约束

- Python：由 uv 管理的稳定 Python 3.12，项目用 `.python-version` 固定。
- uv：先验证现有 0.6.14 是否满足本任务；不得原地更新 Cherry Studio 的 uv。若不满足，暂停并提出 E 盘独立 uv 安装位置、版本和影响，获得确认后再执行。
- 运行时直接依赖候选：`mcp>=2,<3`、`httpx`、`pydantic`；实际兼容范围在 Step 0/1 根据解析结果锁定。
- 开发依赖候选：pytest、pytest-asyncio、Ruff、静态类型检查器；避免为展示引入无关库。
- 首期从源码/项目环境以模块入口启动 stdio；console script 和分发包留给 F-002。
- 不读取 `.env`，不需要 API Key，不新增 secrets 配置。

## Tool 契约

### 名称与描述

- 名称：`get_current_weather`
- 描述必须说明：解析城市或邮编式地点；返回 model-based current conditions；只读；不提供预报、预警、建议或任意 URL；调用方应检查返回的 resolved location。

### 输入

| 字段 | 类型 | 必填 | 规则 |
| --- | --- | --- | --- |
| `location` | string | 是 | trim 后 2–100 字符；不解释为 URL |
| `country_code` | string/null | 否 | 两位 ISO 3166-1 alpha-2；接受大小写输入并规范化为大写 |

地点解析采用 Open-Meteo 的最佳排序结果；Server 必须返回实际解析地点、国家、行政区、坐标和时区，使歧义可见。首期不增加候选选择 Tool。

### 成功输出

| 分组 | 字段 |
| --- | --- |
| 请求 | `requested_location`、规范化后的 `country_code` |
| 解析地点 | `name`、`country`、`country_code`、可选 `admin1`、`latitude`、`longitude`、`timezone` |
| 当前天气 | `time`、`interval_seconds`、`is_day`、`temperature_c`、`apparent_temperature_c`、`relative_humidity_percent`、`precipitation_mm`、`weather_code`、`condition`、`wind_speed_kmh`、`wind_direction_degrees` |
| 元数据 | 明确 units、provider、`model_based_current_conditions` 标记、attribution 和 license URL |

成功结果必须通过 `MCPServer` 暴露的 outputSchema 校验；不以手写 JSON 字符串作为主要结构化结果。

### 失败输出

| 稳定错误码 | 场景 | `retryable` | 调用方提示 |
| --- | --- | --- | --- |
| `INVALID_LOCATION` | 地点或国家代码非法 | false | 修改参数 |
| `LOCATION_NOT_FOUND` | 地理编码无结果 | false | 补充行政区/国家代码 |
| `UPSTREAM_TIMEOUT` | 地理编码或天气请求超时 | true | 稍后有限重试 |
| `UPSTREAM_RATE_LIMITED` | 上游 429 | true | 退避后重试 |
| `UPSTREAM_UNAVAILABLE` | 网络、5xx 或临时服务失败 | true | 稍后重试 |
| `UPSTREAM_INVALID_RESPONSE` | JSON/字段/类型不满足契约 | false | 报告服务异常，不返回部分天气 |

业务/上游失败必须表现为 MCP Tool execution error，使 Host/模型可见稳定错误码、简短 message、retryable 和修正 hint；不得暴露堆栈、完整上游 body、本地绝对路径或环境信息。未知 Tool 和畸形 MCP 请求由 SDK 的协议错误处理。

### Tool annotations

- `readOnlyHint = true`
- `destructiveHint = false`
- `idempotentHint = true`
- `openWorldHint = true`

annotations 是提示而非安全控制；固定域名和无写入实现才是硬边界。

## 输入、输出与状态

- 输入：MCP `tools/call` 参数；不读取文件、环境凭证或用户账户。
- 外部读取：固定 Open-Meteo 地理编码和天气 endpoint。
- 输出：结构化天气或明确 Tool execution error。
- 关键状态：无持久状态、无 session 业务状态、无数据库；每次调用独立。
- 生命周期：进程由 Host/Inspector 通过 stdio 启停。

## 数据影响

- 发送到 Open-Meteo：地点查询文本、可选国家代码；天气请求发送解析出的坐标和所需变量。
- 外部服务可见调用端 IP；本任务不额外收集、持久化或转发用户数据。
- 新增或修改的持久业务数据：无。
- 缓存、唯一性、事务、并发：首期无缓存/事务；服务不得使用可变全局业务状态；并发安全依赖无状态调用和独立响应模型。
- 回滚：停止本地 Server 或切换/回退功能分支；无外部数据需要恢复。

## 权限与安全边界

- 允许角色：能启动本地 Server 的开发者和其授权 Host/Inspector。
- 必须拒绝：空/非法地点、非法国家代码、试图把 URL/路径作为 endpoint、未定义 Tool、上游不可信/畸形结果。
- 固定允许域名：`geocoding-api.open-meteo.com`、`api.open-meteo.com`；仅 HTTPS。
- Tool 不得执行文件、Shell、数据库、写入或删除动作，不得跟随用户指定 URL。
- 日志只写 `stderr`；`stdout` 只允许有效 MCP 协议消息。
- 日志/证据不得包含完整上游响应、请求头、Cookie、Token、精确个人位置历史或本机隐私路径。
- 数据源内容属于开放世界输入；所有响应都必须经过类型和范围校验，不能直接拼入控制指令。

## UI 与交互状态

本任务没有图形 UI、Figma 或响应式要求。交互状态映射到 MCP/Inspector：

- normal/success：Tool 可发现，成功结果结构化展示。
- loading/submitting：由 Host/Inspector 表示调用进行中；Server 设置有限超时，不自行伪造进度 UI。
- empty：地点无结果映射为 `LOCATION_NOT_FOUND`，不返回空成功对象。
- error：稳定 Tool error；Inspector 可见错误码和提示。
- permission denied：不适用，无认证系统。
- disabled：不适用，不暴露禁用 Tool。
- 视觉设计与视觉验收：不适用。

## 验收标准

1. Given F-001 环境已建立，when Host/SDK 调用 `tools/list`，then 只发现 `get_current_weather`，且名称、描述、inputSchema、outputSchema 和四个 annotations 与任务卡一致。
2. Given 网络可访问 Open-Meteo，when 以 `location="北京"` 调用 Tool，then 返回通过 outputSchema 的结构化结果，并包含实际解析地点、坐标、时区、有效时间、天气字段、单位、provider 和 CC BY 4.0 署名。
3. Given `country_code="cn"`，when 调用 Tool，then 输入被规范化为 `CN`，结果明确返回解析后的国家代码。
4. Given 地点含首尾空格，when 调用 Tool，then Server trim 后查询；Given trim 后少于 2 字符、超过 100 字符或国家代码非法，then 返回可修正的 `INVALID_LOCATION`，不发起外部请求。
5. Given 地理编码没有结果，when 调用 Tool，then 返回 `LOCATION_NOT_FOUND`，不继续调用天气 endpoint。
6. Given mock 上游分别发生 timeout、429、5xx、连接失败和坏 JSON/缺字段，when 调用 Tool，then 分别映射到任务卡定义的稳定错误，并且不返回部分成功数据或堆栈。
7. Given 恶意地点字符串看似 URL/路径，when 调用 Tool，then HTTP 请求仍只能发往两个固定 HTTPS 域名，用户输入只作为编码后的 query parameter。
8. Given stdio smoke 启动 Server，when 执行 Tool discovery、一次成功或固定 mock 调用并退出，then 进程正常结束，`stdout` 无 MCP 协议外文本，诊断信息仅在 `stderr`。
9. Given MCP Inspector 使用项目命令连接，when 人工查看并调用 Tool，then 连接、Schema、成功结果和至少一个错误路径可复现；记录简短脱敏证据。
10. Given默认离线门禁，when 运行格式、lint、类型、单元、适配器、协议和 stdio 测试，then 全部通过且不依赖 live API；live contract 由显式命令单独运行。
11. Given F-001 diff，when 独立 QA 审查，then 没有第二 Tool、任意 URL、旧 SSE、外部发布、敏感信息、无关文件或把 mock 写成 live 证据。
12. Given 任一必需 live/Inspector 验收无法完成，then 任务保持未完成并说明环境/上游阻塞，不能写成已交付或已发布。

## 测试矩阵

| 风险/行为 | 测试层级 | 核心用例 | 失败证明 | 角色 |
| --- | --- | --- | --- | --- |
| 输入约束 | 单元/Schema | trim、长度、国家代码规范化和拒绝 | 错误实现会接受非法输入或发起 HTTP | 实现者 + 独立 QA |
| 地点解析 | 适配器/服务 | 成功、无结果、国家过滤、最佳结果透明返回 | 响应字段或编排错误时断言失败 | 实现者 |
| 天气转换 | 单元/适配器 | WMO code、单位、时间、可选字段、边界数值 | 删除/错配字段后 output model 校验失败 | 实现者 |
| 上游失败 | 适配器/服务 | timeout、429、5xx、连接失败、坏 JSON、缺字段 | 各错误必须映射到唯一稳定码 | 实现者 + 独立 QA |
| SSRF/任意 URL | 单元/差异审查 | 恶意 location 不改变 host/scheme/path | 捕获请求并断言固定 endpoint | 独立 QA |
| MCP 契约 | SDK in-memory 集成 | tools/list、schema、annotations、成功/错误 call | Tool 名、Schema 或 isError 漂移时失败 | 实现者 + 独立 QA |
| stdio 边界 | 子进程 smoke | 启动、消息交换、退出、stdout 纯净 | 普通 print 会破坏协议/断言 | 实现者 + 独立 QA |
| 真实数据契约 | opt-in live | 北京或稳定测试地点两步请求 | 只证明当时契约；失败需分类，不可用 fixture 代替 | 实现者 + 用户 UAT |
| Inspector 可用性 | 人工验收 | 发现、成功、错误显示 | 截止验收时无法操作即不通过 | 用户 UAT |

至少对一个核心错误边界保留红绿证明：先让测试在实现缺失/错误下失败，再完成最小实现使其通过；不保留故意错误代码。

## 文件影响范围

允许新增或修改：

- `.gitignore`、`.python-version`、`pyproject.toml`、`uv.lock`
- `src/mcp_weather_query/**`
- `tests/unit/**`、`tests/integration/**`、`tests/smoke/**`、`tests/fixtures/**`
- `AGENTS.md`、`README.md`
- `docs/README.md`、`docs/product-brief.md`、`docs/architecture.md`、`docs/testing-strategy.md`
- `docs/project-management/current-task.md`
- 任务获批后按需新增 `docs/project-management/implementation-plan.md`、`progress.md` 和 `docs/evidence.md`
- 经任务卡批准的本地 `.git/` 元数据、`main` 基线提交和 `feat/f-001-local-weather-tool` 分支

明确不新增或修改：

- `docs/release-plan.md`、F-002 及后续 roadmap 范围（除真实状态同步）
- `LICENSE`、`CHANGELOG.md`、`server.json`、`dist/`
- Git 远程、GitHub Actions、远程仓库、PR、release、PyPI、Registry 或社区平台
- `E:\Vibe coding` 方法论、Cherry Studio 文件、系统配置和全局环境变量
- 任何项目外个人文件、凭证或无关项目

## Step 地图

### Step 0：执行基线与本地 Git 启动

- 复核任务卡批准、目录、Git 和环境事实。
- 获得授权后初始化 `main`，精确审查并创建 Step 0 文档基线提交，再创建 `feat/f-001-local-weather-tool`。
- 验证现有 uv 能否管理 Python 3.12；不得覆盖 Cherry Studio uv，不满足时停止并提交 E 盘独立 uv 方案。
- 建立 implementation-plan、短 progress 和 evidence 索引。
- 本 Step 不写天气业务代码。

### Step 1：工程骨架与失败测试

- 状态：已完成（2026-08-11）。
- 建立 pyproject、src/test 结构、项目模块入口和依赖锁。
- 先建立输入、模型、错误与固定 endpoint 的失败测试/fixture。
- 不实现对外 Tool 成功逻辑。

### Step 2：Open-Meteo 适配器与天气用例

- 状态：已完成（2026-08-11）。
- 实现地理编码、天气查询、响应校验、WMO 映射和稳定错误分类。
- 完成服务层离线单元/适配器测试。
- 保持 MCP 协议逻辑与 HTTP 适配器分离。

### Step 3：MCPServer Tool 与结构化输出

- 状态：已完成（2026-08-11）。
- 注册唯一 Tool、Schema、描述、annotations 和 stdio 模块入口。
- 映射 Tool execution errors，源码入口不输出普通文本。
- 完成 SDK in-memory 协议测试。

### Step 4：stdio 与自动化门禁

- 状态：已完成（2026-08-11）。
- 完成真实子进程 smoke、退出和日志边界测试。
- 运行 Ruff、类型检查和默认离线测试集。
- 修复范围内失败，不进入打包/发布。

### Step 5：live contract、Inspector 与用户验收

- 状态：`completed`（2026-08-11，含现代 stdio 协议证据与用户 UAT）。
- [x] 显式运行一次 Open-Meteo live contract。
- [x] 用 MCP Inspector 验证 discovery、成功和错误路径。
- [x] 提交脱敏人工验收步骤和结果。
- [x] 项目独立 Node 24.19.0 通过官方 SHA256 校验，Inspector engine warning 消除，系统 Node 未改变。
- [x] 官方 SDK v2 `Client(mode="auto")` 通过生产 stdio 入口执行 `server/discover`，协商 MCP 2026-07-28；`discover_result` 存在且 `initialize_result` 为空。
- [x] 同一现代协议下只发现 `get_current_weather`，测试专用 stdio Server 完成合法 structuredContent 调用；未访问 live API。
- [x] Inspector 2.1.0 的 stdio UI 明确记录为 Legacy MCP 2025-11-25 兼容路径，不再冒充现代协议证据，也不要求引入 HTTP。
- [x] 用户于 2026-08-11 明确通过 UAT；随后单独授权 Step 6 QA。

### Step 6：独立 QA、文档与 Git 收口

- 状态：`local_completed / awaiting_remote_pr_authorization`（2026-08-11）。
- [x] 独立审查完整已跟踪 diff、全部未跟踪文件、负向测试、固定域名、stdout、证据真实性和范围。
- [x] 运行全量适用门禁，更新 README/架构/测试/current-task/progress/evidence。
- [x] 没有未解决的高、中优先级范围内缺陷；唯一 Tool、协议、网络和安全边界保持不变。
- [x] 用户选择远程 PR 流程，并形成精确本地提交；提交哈希以 Git 事实为准。
- [ ] 当前无远程；配置 remote、push 和创建 PR 必须另行获得明确授权。
- 不自动进入 F-002。

## 文档更新契约

- 当前任务入口：本文件。
- 执行计划：任务卡批准后建立 `implementation-plan.md`，只维护 F-001 Step。
- 短状态：`progress.md` 只记录当前 Step、已验证结果、阻塞和下一批准动作。
- 证据：`docs/evidence.md` 只保存命令/环境/结论/风险索引，不复制完整日志或响应。
- 架构/测试文档：只有实现事实或测试策略真实变化时覆盖更新。
- README：只在运行方式真实可用后更新，不提前写“可运行/已发布”。
- roadmap：F-001 关闭后压缩为一行结果；用户选择前不得激活 F-002。
- 归档位置：任务真正关闭后进入 `docs/archive/task-cards/F-001-local-weather-tool.md`；迁移前仍需遵守不删除和用户确认边界。
- 一致性检查：README、roadmap、current-task、progress、evidence、分支、提交、测试和外部发布状态必须一致。

## 风险、依赖与回滚

### 主要风险

- Open-Meteo 免费层无 SLA、限额且仅限非商业；live 测试可能因网络或上游暂时失败。
- 城市最佳结果存在歧义；通过返回 resolved location 降低误判，但首期不提供候选选择。
- 当前 conditions 是模型数据而非站点实测，必须明确标记。
- 官方 SDK v2 和本机旧 uv 的组合可能暴露兼容问题。
- 系统 Python 为 RC 版本且 `py` 启动器异常；任务必须只使用 uv 管理的 Python 3.12。
- Inspector 依赖 npm/npx，首次运行可能联网下载。

### 未覆盖风险

- 高并发、长期缓存、商业 SLA、跨平台矩阵和远程部署不在 F-001 验收范围。
- 免费 API 条款未来变化需要在发布任务再次核验。

### 回滚与恢复

- 无数据库或外部写入；停止 Server 即停止运行影响。
- 代码变更隔离在功能分支；回滚优先通过保留 main 基线、切换分支或精确反向提交。
- 不使用 `git reset --hard`、`git clean` 或批量删除；需要删除生成文件时先请求确认。
- 依赖/环境失败时保留诊断摘要，恢复到 Step 0，不通过修改系统 Python 或 Cherry Studio uv 绕过。

### 需要人工确认的动作

- 允许进入 Step 5，并执行显式 live API/Inspector 验收。
- 若现有 uv 不满足要求，批准具体的 E 盘独立 uv 安装方案。
- Step 5 用户 UAT：已于 2026-08-11 通过。
- Step 6 Git 选择：用户已选择远程 PR 流程。
- 任何 push、远程仓库、PR 或发布动作必须另行明确授权。

## 上下文与预算

- 预计直接读取：当前 9 份规划文档，以及每个 Step 实际涉及的少量源码/测试；不重复读取完整历史。
- 预计执行：6 个 Step，按 Step 小步推进，不并行创建第二任务。
- 未设置显式 Token 预算；以最小上下文和权威文件恢复状态。
- 停止并重切条件：范围出现第二 Tool/HTTP/打包/发布；文件影响超过任务卡授权；同一阻塞连续三次无法证明根因；必须修改系统/Cherry Studio 环境；live/Inspector 无法获得真实证据。

## 完成定义

- [x] 任务卡已由用户批准，Step 0 Git/环境边界获授权并完成。
- [x] Step 1 工程骨架、依赖锁和预期红灯契约测试获授权并完成。
- [x] Step 2 模型、错误、WMO、服务和固定 Open-Meteo 适配器获授权并完成，41 个离线测试通过。
- [x] Step 3 唯一 MCP Tool、Schema、annotations、结构化结果和 Tool execution error 获授权并完成，48 个离线测试通过。
- [x] Step 4 真实 stdio 握手、唯一 Tool discovery、固定 Tool call、stdout/stderr 与退出边界获授权并完成，50 个离线测试通过。
- [x] Step 5 显式 live contract 通过；Inspector 完成唯一 Tool discovery、结构化成功调用和稳定错误路径技术验证。
- [x] `get_current_weather` 是唯一注册的业务 Tool。
- [x] 输入、输出、annotations 和稳定错误与任务卡一致。
- [x] 只访问固定 Open-Meteo HTTPS endpoint，无写入、Shell、文件或任意 URL 能力。
- [x] 单元、适配器、MCP in-memory 和 stdio smoke 测试通过，核心边界有红绿证明。
- [x] 格式、lint、静态类型和当前范围/敏感信息门禁通过。
- [x] 显式 live contract 通过，且没有用 fixture 冒充 live 证据。
- [x] MCP Inspector discovery、成功和错误路径技术验证通过。
- [x] 独立 QA 已完成。
- [x] 用户 UAT 已通过。
- [x] README、架构、测试、current-task、progress、evidence、roadmap 与当前代码、测试和 Git 事实一致。
- [x] 本地 diff 和提交可审查；无远程时已获得远程 PR 流程的人工决策。
- [x] 没有构建包、创建第二 Tool、启用 HTTP、提交敏感信息或执行外部发布。
- [ ] F-001 真正关闭后才归档；未自动创建或执行 F-002。

## 审批记录与下一门禁

用户于 2026-08-11 批准本任务卡，并允许：初始化本地 Git、创建仅含基线文档的本地提交、创建 `feat/f-001-local-weather-tool`；优先复用现有 uv，不覆盖 Cherry Studio uv；F-001 不打包、不发布。

Step 0 已验证现有 uv 0.6.14 能管理项目内 E 盘 CPython 3.12.10，无需更新 uv。Step 1 建立工程骨架、依赖锁和预期红灯测试；Step 2 将领域、服务和固定 Open-Meteo 适配器转绿；Step 3 完成唯一 MCP Tool 和内存协议验证；Step 4 完成真实 stdio 与全量离线门禁；Step 5 完成 live/Inspector 功能验证、独立 Node 修复、现代 MCP 2026-07-28 stdio 证据和用户 UAT；Step 6 已完成独立 QA、文档收口和精确本地提交。用户已选择远程 PR 流程；当前授权不包含创建远程、配置 remote、push、PR、F-002 或任何发布。
