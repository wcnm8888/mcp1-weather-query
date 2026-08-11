# MCP1-天气查询

一个用于学习 MCP Server 设计、stdio 调试、结构化 Tool 输出、测试、打包与发布流程的 Python 小项目。项目将复现 Datawhale《第十章 智能体通信协议》的天气案例，但以 2026-07-28 MCP 规范和当前官方 Python SDK 为基线，不直接复制教程中的旧封装、数据源或发布叙述。

## 当前状态

- 项目类型：启动新项目。
- 项目整体等级：M；规划、roadmap 和执行基线已完成。
- 当前任务：F-001 已完成并关闭；当前没有已批准的活动任务。
- 代码：领域/服务/Open-Meteo 适配器已实现；官方 v2 `MCPServer` 只注册 `get_current_weather`，并提供输入/输出 Schema、只读 annotations、结构化成功结果和稳定 Tool execution error。
- Git：private 仓库为 [wcnm8888/mcp1-weather-query](https://github.com/wcnm8888/mcp1-weather-query)；[PR #1](https://github.com/wcnm8888/mcp1-weather-query/pull/1) 已把 `feat/f-001-local-weather-tool` 合并到 `main`，原本地和远程功能分支已删除。
- 发布：未构建、未上传、未注册任何外部条目。
- 测试：Step 6 默认离线门禁为 `52 passed, 1 skipped`；格式、lint、严格类型、依赖锁、SDK in-memory、现代/Legacy stdio 子进程测试和范围扫描通过。唯一 skip 是显式 opt-in 的 live contract；此前 live contract 为 `1 passed`，Inspector 已完成唯一 Tool 的发现、成功和错误路径验证。
- 启动边界：已验证项目虚拟环境 Python 通过 `-m mcp_weather_query` 启动、握手、发现唯一 Tool 并在 stdin 关闭后以退出码 0 结束。F-001 未配置打包，源码启动仍需显式设置 `PYTHONPATH=<项目目录>\src`。
- Node 兼容性：项目独立 Node 24.19.0 已通过官方 SHA256 校验，Inspector 2.1.0 不再产生 engine warning；系统 Node 22.16.0 未改变。
- 协议证据：官方 Python SDK v2 `Client(mode="auto")` 通过生产 stdio 入口完成 `server/discover`，协商 MCP 2026-07-28，且未执行 Legacy initialize；同一 Server 继续允许 Inspector 2.1.0 以 Legacy MCP 2025-11-25 调试。
- Step 6 QA：已审查全部已跟踪和未跟踪文件，没有未解决的高、中优先级范围内缺陷；未构建、打包或发布。
- 下一步：等待用户从已批准 roadmap 中选择是否进入 F-002；不得自动创建任务卡、批准或执行后续任务。

## 拟交付能力

首个闭环拟提供一个只读 MCP Tool：`get_current_weather`。它接收地点名称和可选国家代码，通过固定天气数据源解析地点并返回带单位、时间、解析后地点和数据来源的结构化当前天气结果。

## 明确非目标

- 不构建完整 Agent、聊天 UI、RAG 或多 Agent 系统。
- 不提供天气预报、历史天气、空气质量、灾害预警或穿衣建议。
- 不提供写入、删除、任意 Shell、任意文件访问或任意 URL 请求。
- 首期不提供 Streamable HTTP、远程托管、账号体系和生产 SLA。
- 不因教程示例存在多个 Tool 而增加“城市列表”或“服务器信息”等展示性 Tool。

## 文档入口

项目定义、架构、测试、发布和路线状态见 [docs/README.md](docs/README.md)。

## 参考基线

- [MCP 2026-07-28 规范](https://modelcontextprotocol.io/specification/2026-07-28)
- [MCP Python SDK v2](https://py.sdk.modelcontextprotocol.io/)
- [MCP Inspector](https://modelcontextprotocol.io/docs/tools/inspector)
- [Official MCP Registry](https://registry.modelcontextprotocol.io/)
- [Datawhale 第十章](https://github.com/datawhalechina/hello-agents/blob/main/docs/chapter10/%E7%AC%AC%E5%8D%81%E7%AB%A0%20%E6%99%BA%E8%83%BD%E4%BD%93%E9%80%9A%E4%BF%A1%E5%8D%8F%E8%AE%AE.md)
