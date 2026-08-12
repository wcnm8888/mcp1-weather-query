# Roadmap（已批准）

> 状态：`approved`。F-001、F-002、D-001、R-001 已完成并关闭。R-002 任务卡已获批准，
> Step 0–4 已完成；Step 5 Draft readiness PR #11 已创建并等待 CI；后续仍按 Step 分段授权。

## 推荐顺序

| 编号 | 任务 | 状态 | 用户价值 | 主要范围 | 非目标 | 依赖 | 等级 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| F-001 | 一个 Tool 的本地天气闭环 | **已完成并关闭** | 用户能在 Inspector/Host 通过 stdio 查询当前天气并获得结构化结果 | Python 工程基线、官方 SDK v2、Open-Meteo 适配器、一个 Tool、错误映射、现代/Legacy stdio 测试、Inspector 人工验收 | 打包发布、第二 Tool、HTTP、Agent | PR #1 已合并；关闭证据已收口 | M 内的首个垂直切片 |
| F-002 | 可安装与可构建闭环 | **已完成并关闭** | 用户能从 wheel/sdist 在干净环境安装并启动同一 Server | console entry point、包元数据、License/署名、`uv build`、artifact 审查、干净安装 smoke | 真实上传、Registry 登记 | PR #3、收口 PR #4 已合并；归档和复验完成 | S |
| D-001 | 发布候选与发布前审查 | **已完成并关闭** | 用户获得可审查、不会误发布的发布材料 | README 安装示例、CHANGELOG、发布清单、`server.json` 草案/校验、命名检查、安全审查 | 外部上传和注册 | QA/UAT 已通过；PR #5 已合并；任务卡已归档 | S |
| R-001 | PyPI 外部发布 | **已完成并关闭** | 外部用户可通过 Python 包索引安装 Server | Trusted Publishing workflow、最终候选、分段授权发布、公开制品与安装验证 | TestPyPI、npm、Registry、GitHub Release、远程托管 | `0.1.0` 已发布；attestation 与双公开安装已验证；任务卡已归档 | L |
| R-002 | Official MCP Registry 登记 | **已批准；Step 5 Draft PR #11 等待 CI** | Registry API 与下游聚合器可发现已发布 Server | 固定 `io.github.wcnm8888/mcp1-weather-query` 身份、GitHub OAuth、分段发布与官方 API/安装复验 | 修改业务代码、第二 Tool、新 PyPI 版本、社区多平台铺开 | R-001 已关闭；公开 PyPI 0.1.0；每个外部门禁单独授权 | L |

## 当前任务

当前活动任务为 R-002。状态入口见 `docs/project-management/current-task.md`；当前只执行已获授权的
Step 5 readiness Git/PR，不得运行 Terms、OAuth、Registry login/publish 或自行合并 PR。

## 暂不进入路线的候选

- 第二个 Tool（坐标查询、天气预报或城市候选选择）。
- Streamable HTTP 与远程部署。
- MCPB、Smithery 或其他社区目录。
- Agent、RAG、多 Agent 和 UI。

这些只有出现真实用户需求并由用户调整 roadmap 时才进入候选任务。

## 已确认路线门禁

用户已确认：项目整体按 M 管理；Open-Meteo 数据源限制可接受；首期恰好一个 Tool；发布顺序为 PyPI 后 Registry；外部发布仍分两次独立确认。D-001 只形成发布候选和发布前审查证据，不等于真实发布。
