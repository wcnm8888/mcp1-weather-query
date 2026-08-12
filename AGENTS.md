# MCP1-天气查询 项目规则

本项目遵循 `E:\Vibe coding\AGENTS.md` 与 `E:\Vibe coding\vibe-methodology\`。发生冲突时，以用户本轮明确要求、项目真实代码/测试/Git 事实和工作区安全规则为准。

## 当前阶段

- 生命周期：roadmap 已批准；F-001、F-002、D-001、R-001、R-002 均已完成并关闭；当前无活动任务。
- 项目整体等级：M；新的任务必须由用户明确选择并独立批准。
- 当前状态：`mcp-weather-query==0.1.0` 已通过 Trusted Publishing 发布到生产 PyPI，
  `io.github.wcnm8888/mcp1-weather-query==0.1.0` 也已登记到 Official MCP Registry；
  官方 API、公开 PyPI 安装和 installed-package stdio 已验证。
- 禁止把“文档已建立”“本地可运行”“已构建”写成“已发布”。

## 范围边界

- 首个用户价值切片只实现一个只读当前天气查询 Tool。
- 默认传输为 stdio；Streamable HTTP 只有出现远程部署需求并经用户确认后才进入范围。
- 不新增 Agent、RAG、多 Agent、数据库、写入工具、任意 Shell 或任意 URL 请求能力。
- 外部天气请求只能发往已批准的数据源固定域名，用户输入不得决定请求 URL。
- 不在代码、日志、文档、测试数据或提交中保存 API Key、Token、Cookie、密码和真实敏感信息。

## 工作流与外部操作

- R-002 readiness PR #11 与 closure PR #12 均已合并，Step 11 已同步、归档并关闭任务。
- 当前不授权新的 Registry 操作。已发布的 `0.1.0` 不得重复 publish；新版本、metadata 更新、
  deprecated/deleted 状态变更或重新认证均需新任务和用户明确授权。
- 未经对应 Step 授权，不得运行 `mcp-publisher validate/login/publish`、接受 Registry Terms
  或写入外部 Registry。
- 后续 PyPI 版本、MCP Registry 实际登录/登记、GitHub Release 或公开仓库变更仍需对应 Step
  的用户明确授权；登录不等于授权发布。
- 本项目只使用 `docs/` 作为长期文档目录，不创建重复的 `memory-bank/`。
- commit、push、PR、PyPI/TestPyPI 上传、MCP Registry 注册、社区平台发布、公开仓库创建均需用户明确授权。
- 不删除项目文件或目录；需要归档、迁移或清理时先列出影响并等待确认。

## 最低验证原则

- 工具输入/输出 Schema、成功路径、无结果、无效输入、超时、限流、上游错误和无效响应必须可验证。
- stdio 的 `stdout` 只允许 MCP 协议消息；诊断信息只能写 `stderr`。
- 实现完成不等于交付完成；测试、Inspector、干净环境安装、构建、发布和 Registry 登记分别记录真实状态。
