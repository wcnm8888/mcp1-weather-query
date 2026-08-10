# MCP1-天气查询

一个用于学习 MCP Server 设计、stdio 调试、结构化 Tool 输出、测试、打包与发布流程的 Python 小项目。项目将复现 Datawhale《第十章 智能体通信协议》的天气案例，但以 2026-07-28 MCP 规范和当前官方 Python SDK 为基线，不直接复制教程中的旧封装、数据源或发布叙述。

## 当前状态

- 项目类型：启动新项目。
- 项目整体等级：M；Step 0 规划和 roadmap 确认已完成。
- 当前任务：F-001 任务卡已批准，Step 0 执行基线完成。
- 代码：未实现。
- Git：已建立本地 `main` 基线并进入 `feat/f-001-local-weather-tool`；未配置远程、未推送。
- 发布：未构建、未上传、未注册任何外部条目。
- 下一步：等待用户允许进入 F-001 Step 1；当前没有业务代码。

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
