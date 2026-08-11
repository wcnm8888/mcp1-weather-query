# F-001 Implementation Plan

## 当前状态

- 当前任务：F-001 一个 Tool 的本地天气闭环
- 当前 Step：Step 6 draft PR #1 已创建，等待用户审查/合并决策
- 当前分支：`feat/f-001-local-weather-tool`
- 下一步：等待用户决定是否将 draft PR #1 标记 ready 或合并
- 禁止：自动标记 ready、合并、关闭 F-001、进入后续任务、打包或发布

## Step 0：执行基线与本地 Git 启动

状态：`completed`

- [x] 复核任务卡、目录、Git、工具版本和用户授权。
- [x] 使用现有 uv 0.6.14，不覆盖 Cherry Studio 管理的 uv。
- [x] 将 uv managed CPython 3.12.10 安装到项目 `.runtime/`，并由 `.gitignore` 排除。
- [x] 使用 `.python-version` 固定 Python 3.12。
- [x] 建立本计划、短进度和证据索引。
- [x] 初始化本地 `main`，创建精确基线提交，并创建 F-001 功能分支。
- [x] 未写业务代码、未安装项目依赖、未配置远程、未发布。

## Step 1：工程骨架与失败测试

状态：`completed`

- [x] 建立 `pyproject.toml`、`src/mcp_weather_query/` 和授权测试目录。
- [x] 使用 Python 3.12.10 锁定最小运行/开发依赖；`mcp` 锁定为 2.0.0。
- [x] 建立输入、错误、固定 endpoint 和结构模型的失败测试/fixture。
- [x] 15 个测试按预期失败，0 个收集错误；失败原因均为批准边界尚未实现。
- [x] Ruff format、Ruff lint 和严格 mypy 通过。
- [x] 未实现对外 Tool、天气领域逻辑或 HTTP 调用。

验证结果：项目只使用 uv managed Python 3.12；失败测试证明任务卡核心边界尚未实现；diff 不含构建或发布文件。

## Step 2：Open-Meteo 适配器与天气用例

状态：`completed`

- [x] 实现 Pydantic 输入/结构化输出模型与 ISO 时间、坐标、范围和单位校验。
- [x] 实现 6 个稳定错误码、retryable 规则、安全 message/hint 和内部异常载体。
- [x] 实现官方 WMO weather code 映射；未知 code 拒绝为无效上游响应。
- [x] 实现固定 geocoding/forecast HTTPS endpoint、有限超时、禁止重定向和显式单位。
- [x] 实现最佳地点解析、current conditions 转换和无状态两步应用服务。
- [x] 覆盖无结果、超时、429、5xx、连接失败、坏 JSON、缺字段、错误单位/时区和未知 WMO code。
- [x] 41 个离线测试、Ruff format/lint、严格 mypy 和 lock check 通过。
- [x] 未访问 live API，未注册 MCP Tool，未创建 `server.py`，未启用 stdio。

## Step 3：MCPServer Tool 与结构化输出

状态：`completed`

- [x] 使用官方 v2 `MCPServer`，且只注册 `get_current_weather`。
- [x] 声明地点/国家代码输入 Schema、完整结构化输出 Schema、描述和四个 annotations。
- [x] 成功结果直接生成 `structuredContent`，没有额外 `result` 包装层。
- [x] 业务/上游失败映射为带稳定 code、message、retryable、hint 的 Tool execution error。
- [x] 意外内部异常收敛为通用 MCP 协议错误，不泄露堆栈或本机路径。
- [x] 建立 stdio 模块入口但未启动；使用依赖注入完成 SDK in-memory discovery/call 测试。
- [x] 48 个离线测试、Ruff format/lint、严格 mypy 和 lock check 通过。
- [x] 未启动 stdio 子进程、未访问 live API、未运行 Inspector、未打包或发布。

## Step 4：stdio 与自动化门禁

状态：`completed`

- [x] 使用项目虚拟环境 Python、源码 `PYTHONPATH` 和生产模块入口启动真实子进程。
- [x] 完成 MCP initialize、唯一 Tool discovery、stdin 关闭、退出码 0 和无额外 stdout 验证。
- [x] 使用官方 `stdio_client` + `ClientSession` 调用测试专用固定 Server，返回合法 structuredContent。
- [x] 测试专用诊断进入 stderr；所有子进程步骤均有 10 秒超时和失败清理。
- [x] 保留红灯证据：固定 Server 尚不存在时连接关闭；补充最小测试入口后转绿。
- [x] 50 个离线测试、Ruff format/lint、严格 mypy、lock check 和范围门禁通过。
- [x] 未访问 live API、未运行 Inspector、未打包、未提交或发布。

## Step 5：live contract、Inspector 与用户验收

状态：`completed`

- [x] live contract 默认跳过，只有 `MCP_WEATHER_RUN_LIVE=1` 时显式联网。
- [x] 真实 Open-Meteo 地理编码与 current weather 两步契约通过，且只访问固定 endpoint。
- [x] Inspector v2.1.0 通过 stdio 连接生产模块入口，只发现 `get_current_weather`。
- [x] Inspector 成功调用返回合法结构化结果和解析地点/来源元数据。
- [x] Inspector 非法输入返回稳定 `INVALID_LOCATION` Tool execution error，无 traceback 或本机路径。
- [x] 默认离线门禁最终为 `52 passed, 1 skipped`；Ruff、严格 mypy 和 lock check 通过。
- [x] 官方 Node 24.19.0 Windows x64 ZIP 通过 SHA256 校验并安装到项目 `.runtime/`；不修改系统环境。
- [x] Inspector 2.1.0 在受支持 Node 下无 engine warning。
- [x] 真实证据确认 Inspector stdio 请求和 Server 响应均为 MCP 2025-11-25，界面标记 Legacy。
- [x] SDK v2 `Client(mode="auto")` 对生产 stdio Server 执行 `server/discover` 并协商 MCP 2026-07-28，不产生 initialize 结果。
- [x] 现代 stdio production discovery 只发现唯一 Tool；测试专用 Server 完成离线 structuredContent 调用。
- [x] 默认离线门禁更新为 `52 passed, 1 skipped`；没有启用 HTTP/SSE 或重复 live API。
- [x] Inspector stdio 作为 Legacy 2025 UI 调试路径单独记录，不作为现代协议证据。
- [x] 用户于 2026-08-11 明确通过 UAT。

## Step 6：独立 QA、文档与 Git 收口

状态：`draft_pr_open / awaiting_user_review`

- [x] 审查完整已跟踪 diff 和全部未跟踪源码、测试、配置与文档。
- [x] 复核唯一 Tool、稳定错误、固定端点、stdout/stderr、现代/Legacy 协议证据和敏感信息边界。
- [x] 全量默认离线门禁通过：`52 passed, 1 skipped`；唯一 skip 是显式 live contract。
- [x] 修正陈旧包说明和文档状态/架构表述。
- [x] 核实并停止一个遗留的项目 Playwright CLI daemon；未触碰用户编辑器或其他项目进程。
- [x] 用户选择远程 PR 流程。
- [x] 形成精确本地提交；提交哈希以 Git 事实为准，不在提交内容中自引用。
- [x] 创建 private GitHub 仓库 `wcnm8888/mcp1-weather-query`，配置 `origin` 并推送 `main`/功能分支。
- [x] 创建 draft PR #1：`feat/f-001-local-weather-tool` → `main`；核验为 OPEN、MERGEABLE。
- [ ] 用户审查并决定是否标记 ready 或合并。
- [ ] 未经确认不关闭 F-001、不进入 F-002。

## 停止条件

- 需要第二 Tool、HTTP、打包、发布或任务卡外文件。
- 需要覆盖 Cherry Studio uv、修改系统 Python/注册表或全局环境变量。
- 同一根因连续三次无法证明或验证。
- 必需真实验收无法取得证据。
