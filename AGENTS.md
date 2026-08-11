# MCP1-天气查询 项目规则

本项目遵循 `E:\Vibe coding\AGENTS.md` 与 `E:\Vibe coding\vibe-methodology\`。发生冲突时，以用户本轮明确要求、项目真实代码/测试/Git 事实和工作区安全规则为准。

## 当前阶段

- 生命周期：roadmap 已批准；F-001、F-002 均已完成、合并、归档并关闭；D-001 Step 6 独立 QA 与用户 UAT 均已完成，Step 7 已交付 Draft PR #5。
- 项目整体等级：M；当前活动任务 D-001 是一个 S 级发布准备切片。
- 当前状态：D-001 Draft PR #5 为 OPEN，等待用户审查并决定 Ready/合并；不得自动合并或提前进入 Step 8。
- 禁止把“文档已建立”“本地可运行”“已构建”写成“已发布”。

## 范围边界

- 首个用户价值切片只实现一个只读当前天气查询 Tool。
- 默认传输为 stdio；Streamable HTTP 只有出现远程部署需求并经用户确认后才进入范围。
- 不新增 Agent、RAG、多 Agent、数据库、写入工具、任意 Shell 或任意 URL 请求能力。
- 外部天气请求只能发往已批准的数据源固定域名，用户输入不得决定请求 URL。
- 不在代码、日志、文档、测试数据或提交中保存 API Key、Token、Cookie、密码和真实敏感信息。

## 工作流与外部操作

- 当前只允许完成 D-001 已获准的 Step；不得跨 Step 或自动进入 R-001/R-002。
- D-001 只准备和审查发布候选，不授权上传 PyPI/TestPyPI、登记 MCP Registry、创建 GitHub Release 或 tag。
- 本项目只使用 `docs/` 作为长期文档目录，不创建重复的 `memory-bank/`。
- commit、push、PR、PyPI/TestPyPI 上传、MCP Registry 注册、社区平台发布、公开仓库创建均需用户明确授权。
- 不删除项目文件或目录；需要归档、迁移或清理时先列出影响并等待确认。

## 最低验证原则

- 工具输入/输出 Schema、成功路径、无结果、无效输入、超时、限流、上游错误和无效响应必须可验证。
- stdio 的 `stdout` 只允许 MCP 协议消息；诊断信息只能写 `stderr`。
- 实现完成不等于交付完成；测试、Inspector、干净环境安装、构建、发布和 Registry 登记分别记录真实状态。
