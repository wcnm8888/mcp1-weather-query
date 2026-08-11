# MCP1-天气查询

<!-- mcp-name: io.github.wcnm8888/mcp1-weather-query -->

一个用于学习 MCP Server 设计、stdio 调试、结构化 Tool 输出、测试、打包与发布流程的 Python 小项目。项目将复现 Datawhale《第十章 智能体通信协议》的天气案例，但以 2026-07-28 MCP 规范和当前官方 Python SDK 为基线，不直接复制教程中的旧封装、数据源或发布叙述。

## 当前状态

- 项目类型：启动新项目。
- 项目整体等级：M；规划、roadmap 和执行基线已完成。
- 本地打包能力：项目可生成并审查 wheel/sdist，也已在两个项目外独立环境完成无 `PYTHONPATH` 安装与 stdio 验证；实时任务状态以 `docs/project-management/current-task.md` 为准。
- 代码：领域/服务/Open-Meteo 适配器已实现；官方 v2 `MCPServer` 只注册 `get_current_weather`，并提供输入/输出 Schema、只读 annotations、结构化成功结果和稳定 Tool execution error。
- Git：private 仓库为 [wcnm8888/mcp1-weather-query](https://github.com/wcnm8888/mcp1-weather-query)；[PR #1](https://github.com/wcnm8888/mcp1-weather-query/pull/1) 已把 `feat/f-001-local-weather-tool` 合并到 `main`，原本地和远程功能分支已删除。
- 制品/发布：已生成本地 wheel/sdist 并通过内容审查；未上传、未注册任何外部条目，不代表已经发布。
- 测试：最近一次完整默认门禁为 `76 passed, 1 skipped`；唯一 skip 是显式 opt-in 的 live contract。此前 live contract 为 `1 passed`，Inspector 已完成唯一 Tool 的发现、成功和错误路径验证。
- 启动边界：项目已注册 `mcp-weather-query` console command；wheel 与 sdist 已分别在项目外独立环境安装，并在无 `PYTHONPATH`、非源码工作目录下启动同一 stdio Server。
- Node 兼容性：项目独立 Node 24.19.0 已通过官方 SHA256 校验，Inspector 2.1.0 不再产生 engine warning；系统 Node 22.16.0 未改变。
- 协议证据：官方 Python SDK v2 `Client(mode="auto")` 通过生产 stdio 入口完成 `server/discover`，协商 MCP 2026-07-28，且未执行 Legacy initialize；同一 Server 继续允许 Inspector 2.1.0 以 Legacy MCP 2025-11-25 调试。
- F-002 packaging：版本 `0.1.0`、`uv_build`、console script、MIT LICENSE 和 Open-Meteo NOTICE 已转绿；Step 3 生成的本地 wheel/sdist 已完成制品审查，Step 4 双干净安装验证通过。
- 安装证据：两个环境都从约定制品安装 `mcp-weather-query==0.1.0`，只发现 `get_current_weather`；生产 console 的 stdout 仅含 MCP 消息、退出码为 0，确定性离线调用返回合法 `structuredContent`。
- 交付边界：这些都是本地构建、安装和测试证据，不代表已经上传到 PyPI、登记 MCP Registry 或完成其他外部发布。

## 安装与启动

### 从本地发布候选 wheel 安装

D-001 已在项目外生成并审查本地候选制品。获得已审查的 `0.1.0` wheel 后，
可在包含 `dist/` 的候选目录运行：

```powershell
uv tool install ./dist/mcp_weather_query-0.1.0-py3-none-any.whl
mcp-weather-query
```

这会通过发行包提供的 console entry point 启动生产 stdio MCP Server，不需要
editable install、项目源码目录或 `PYTHONPATH`。`mcp-weather-query` 必须位于当前
`PATH`；可用 `uv tool dir --bin` 查看 uv 的工具命令目录。

### PyPI 发布后的临时运行方式

以下命令只描述用户明确授权并完成 PyPI 发布后的预期用法；当前尚未发布到 PyPI，
现在执行不会得到本项目的已发布包：

```powershell
uvx --from mcp-weather-query==0.1.0 mcp-weather-query
```

### stdio Host 配置

本地 wheel 安装完成且 console command 已位于 `PATH` 后，Host 可使用以下最小配置：

```json
{
  "mcpServers": {
    "weather": {
      "command": "mcp-weather-query",
      "args": []
    }
  }
}
```

Server 通过 stdin/stdout 交换 MCP 协议消息；普通诊断只写入 stderr。不同 Host 的
配置文件位置和外层字段可能不同，但 command 不应改为源码路径，也不应注入
`PYTHONPATH`。

## 发布状态

- `mcp-weather-query==0.1.0` 当前只是本地发布候选，尚未发布到 PyPI。
- Registry 候选名称为 `io.github.wcnm8888/mcp1-weather-query`，尚未登记 MCP Registry。
- README 顶部的 `mcp-name` 注释只为未来 PyPI ownership verification 准备，不代表
  Registry 条目已经存在。
- 任何 PyPI 上传、Registry 登录/发布、Git tag 或 GitHub Release 都需要新的用户授权。

## 已交付能力

首个闭环拟提供一个只读 MCP Tool：`get_current_weather`。它接收地点名称和可选国家代码，通过固定天气数据源解析地点并返回带单位、时间、解析后地点和数据来源的结构化当前天气结果。

## 明确非目标

- 不构建完整 Agent、聊天 UI、RAG 或多 Agent 系统。
- 不提供天气预报、历史天气、空气质量、灾害预警或穿衣建议。
- 不提供写入、删除、任意 Shell、任意文件访问或任意 URL 请求。
- 首期不提供 Streamable HTTP、远程托管、账号体系和生产 SLA。
- 不因教程示例存在多个 Tool 而增加“城市列表”或“服务器信息”等展示性 Tool。

## 文档入口

项目定义、架构、测试、发布和路线状态见 [docs/README.md](docs/README.md)。

## 许可证与数据署名

- 项目源代码采用 [MIT License](LICENSE)。
- 天气与地理编码数据由 [Open-Meteo](https://open-meteo.com/) 提供，数据依照
  [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) 使用。
- 本项目会把选定的上游字段规范化为结构化 MCP Tool 输出，不改变底层测量值；
  详细第三方数据说明见 [NOTICE](NOTICE)。

## 参考基线

- [MCP 2026-07-28 规范](https://modelcontextprotocol.io/specification/2026-07-28)
- [MCP Python SDK v2](https://py.sdk.modelcontextprotocol.io/)
- [MCP Inspector](https://modelcontextprotocol.io/docs/tools/inspector)
- [Official MCP Registry](https://registry.modelcontextprotocol.io/)
- [Datawhale 第十章](https://github.com/datawhalechina/hello-agents/blob/main/docs/chapter10/%E7%AC%AC%E5%8D%81%E7%AB%A0%20%E6%99%BA%E8%83%BD%E4%BD%93%E9%80%9A%E4%BF%A1%E5%8D%8F%E8%AE%AE.md)
