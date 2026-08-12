# MCP1-天气查询 项目规则

本项目遵循 `E:\Vibe coding\AGENTS.md` 与 `E:\Vibe coding\vibe-methodology\`。发生冲突时，以用户本轮明确要求、项目真实代码/测试/Git 事实和工作区安全规则为准。

## 当前阶段

- 生命周期：roadmap 已批准；F-001、F-002、D-001、R-001 均已关闭。
- 项目整体等级：M；当前无活动任务。
- 当前状态：`mcp-weather-query==0.1.0` 已通过 Trusted Publishing 发布到生产 PyPI，
  公开制品、attestations 和双干净安装 stdio 已验证；MCP Registry 尚未登记。
- 禁止把“文档已建立”“本地可运行”“已构建”写成“已发布”。

## 范围边界

- 首个用户价值切片只实现一个只读当前天气查询 Tool。
- 默认传输为 stdio；Streamable HTTP 只有出现远程部署需求并经用户确认后才进入范围。
- 不新增 Agent、RAG、多 Agent、数据库、写入工具、任意 Shell 或任意 URL 请求能力。
- 外部天气请求只能发往已批准的数据源固定域名，用户输入不得决定请求 URL。
- 不在代码、日志、文档、测试数据或提交中保存 API Key、Token、Cookie、密码和真实敏感信息。

## 工作流与外部操作

- 当前只允许完成 R-001 Step 9 文档/Git 收口；不得自动启动 R-002。
- 后续 PyPI 版本、MCP Registry、GitHub Release 或公开仓库变更都需要新的任务卡和用户授权。
- 本项目只使用 `docs/` 作为长期文档目录，不创建重复的 `memory-bank/`。
- commit、push、PR、PyPI/TestPyPI 上传、MCP Registry 注册、社区平台发布、公开仓库创建均需用户明确授权。
- 不删除项目文件或目录；需要归档、迁移或清理时先列出影响并等待确认。

## 最低验证原则

- 工具输入/输出 Schema、成功路径、无结果、无效输入、超时、限流、上游错误和无效响应必须可验证。
- stdio 的 `stdout` 只允许 MCP 协议消息；诊断信息只能写 `stderr`。
- 实现完成不等于交付完成；测试、Inspector、干净环境安装、构建、发布和 Registry 登记分别记录真实状态。
