# Roadmap（已批准）

> 状态：`approved`。F-001 已完成并关闭；F-002 功能 PR #3 已合并，Draft PR #4 正在完成合并后收口。本文件不授权自动合并、跨 Step 或执行任何外部发布。

## 推荐顺序

| 编号 | 任务 | 状态 | 用户价值 | 主要范围 | 非目标 | 依赖 | 等级 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| F-001 | 一个 Tool 的本地天气闭环 | **已完成并关闭** | 用户能在 Inspector/Host 通过 stdio 查询当前天气并获得结构化结果 | Python 工程基线、官方 SDK v2、Open-Meteo 适配器、一个 Tool、错误映射、现代/Legacy stdio 测试、Inspector 人工验收 | 打包发布、第二 Tool、HTTP、Agent | PR #1 已合并；原功能分支已删除；关闭证据已收口 | M 内的首个垂直切片 |
| F-002 | 可安装与可构建闭环 | **已完成；收口 PR #4 等待审查** | 用户能从 wheel/sdist 在干净环境安装并启动同一 Server | console entry point、包元数据、License/署名、`uv build`、artifact 审查、干净安装 smoke | 真实上传、Registry 登记 | PR #3 已合并；QA/UAT 与合并后复验通过；PR #4 承载最终收口 | S |
| D-001 | 发布候选与发布前审查 | 待选择 | 用户获得可审查、不会误发布的发布材料 | README 安装示例、CHANGELOG、发布清单、`server.json` 草案/校验、命名检查、安全审查 | 外部上传和注册 | F-002 收口 PR #4 合并后由用户选择 | S |
| R-001 | PyPI 外部发布 | 待选择、需外部授权 | 外部用户可通过 Python 包索引安装 Server | 授权后上传、验证公开制品、记录版本和回滚/弃用方案 | npm、Registry、远程托管 | D-001；PyPI 账号/Token 或 Trusted Publisher；用户明确授权 | 高影响发布动作 |
| R-002 | Official MCP Registry 登记 | 待选择、需外部授权 | MCP 客户端/目录可发现已发布 Server | 命名空间认证、发布 Registry 元数据、验证包引用 | 修改业务代码、社区多平台铺开 | R-001；GitHub/DNS/HTTP 认证；用户再次授权 | 高影响发布动作 |

## 当前任务

当前没有活动任务。F-001 已完成并关闭；F-002 功能 PR #3 已合并，完整任务卡已归档，Draft PR #4 等待用户审查并完成最终收口。不得自动选择 D-001。

## 暂不进入路线的候选

- 第二个 Tool（坐标查询、天气预报或城市候选选择）。
- Streamable HTTP 与远程部署。
- MCPB、Smithery 或其他社区目录。
- Agent、RAG、多 Agent 和 UI。

这些只有出现真实用户需求并由用户调整 roadmap 时才进入候选任务。

## 已确认路线门禁

用户已确认：项目整体按 M 管理；Open-Meteo 数据源限制可接受；首期恰好一个 Tool；发布顺序为 PyPI 后 Registry；外部发布仍分两次独立确认。
