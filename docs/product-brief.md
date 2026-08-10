# 产品 / 项目简述

## 用户与问题

主要用户是正在学习 MCP Server 工程实践的 Python 开发者（当前首先服务项目发起者）。用户需要一个足够小、可观察、可测试、可打包的真实案例，理解 Host/Client/Server、stdio、Tool Schema、错误语义、结构化输出和发布渠道之间的关系。

Datawhale 案例适合作为学习动机，但其天气实现使用 HelloAgents 自有 `MCPServer` 包装、硬编码城市映射、`wttr.in`、JSON 字符串返回和宽泛异常处理；发布章节还把第三方 Smithery 描述为官方平台。项目将保留“天气查询”这个学习场景，改用当前官方 SDK 和经核验的数据源/发布流程。

## 项目目标

1. 用当前官方 Python MCP SDK 的 FastMCP 构建最小 MCP Server。
2. 通过 stdio 被 MCP Inspector 或兼容 Host 启动和调用。
3. 设计一个名称、描述、输入 Schema、输出 Schema 和失败语义都明确的只读 Tool。
4. 用单元、协议集成和 stdio 冒烟测试形成可复现的本地学习闭环。
5. 形成 Python 包构建、干净环境安装、发布前检查、PyPI 发布和 MCP Registry 登记的分阶段闭环。
6. 在文档中清楚区分“代码可运行”“包已构建”“包已发布”“Registry 已登记”。

## 首期范围

- 一个 MCP Server。
- 一个 Tool：`get_current_weather`。
- 输入：地点名称；可选 ISO 3166-1 alpha-2 国家代码用于缩小歧义。
- 传输：stdio。
- 数据源：推荐 Open-Meteo Geocoding API + Weather Forecast API。
- 输出：解析后地点、坐标、时区、观测/模型有效时间、温度、体感温度、湿度、降水、天气代码/说明、风速/风向、昼夜标记、单位和来源。
- 错误：无效输入、地点无结果、超时、限流、上游不可用、上游响应不符合预期。

## 非目标

- 不实现未来预报、历史天气、空气质量、灾害预警和天气建议。
- 不实现第二个展示性 Tool；城市解析是首个 Tool 的内部步骤。
- 不构建 MCP Client、Agent、LLM 调用、RAG、多 Agent 或 UI。
- 不支持用户提供 URL，不访问非固定天气域名。
- 不保存查询历史、坐标或个人数据，不引入数据库。
- 不在首期提供远程 HTTP 服务、鉴权、生产部署或 SLA。
- 不在用户明确确认前发布 PyPI/TestPyPI 包、Registry 条目或社区平台条目。

## 最终交付物

- 可通过 stdio 启动的 Python MCP Server 与命令行入口。
- 可被 Inspector 发现并调用的单个只读 Tool。
- 结构化输入/输出模型和稳定错误分类。
- 单元测试、MCP 协议集成测试、stdio 子进程冒烟测试和可选 live contract 测试。
- `pyproject.toml`、锁文件、wheel/sdist 和干净环境安装验证流程。
- README、架构、测试、发布、路线、任务状态和最终证据文档。
- 经用户单独授权后，可能的 PyPI 包和 MCP Registry 元数据条目。

## 成功标准

- Inspector 能列出且只列出首期授权的一个 Tool，并展示准确 Schema/描述。
- 有效地点返回通过输出 Schema 校验的结构化数据，包含解析后地点和明确单位。
- 主要失败路径对模型可理解，不泄露堆栈、凭证或内部实现细节。
- stdio 的 `stdout` 不含日志污染。
- 项目能在干净环境安装、运行、测试和构建；每一状态均有真实证据。

## 已确认决策

- 项目整体按 M 级管理，Step 0 作为受控 S 级规划切片完成。
- Open-Meteo 是学习/非商业默认数据源；接受其无免费 SLA、免费层限额和 CC BY 4.0 署名要求。
- 首期仅一个 Tool，城市/地点名称优先，并返回实际解析地点。
- roadmap 顺序已批准，首个任务选择 F-001。
- 使用 uv 管理稳定 Python 3.12；不得直接覆盖 Cherry Studio 管理的 uv，版本不足时先说明独立安装方案和影响。
