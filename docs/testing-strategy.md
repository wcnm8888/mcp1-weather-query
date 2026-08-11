# 测试策略

## 目标

测试从用户行为和风险推导，覆盖 Tool schema、地点解析、上游错误、结构化输出和 stdio 协议边界。Mock 测试只证明确定性逻辑；外部 API 的真实可用性必须单独标记为 live contract 证据，不能由 fixture 冒充。

## 分层

| 层级 | 主要内容 | 是否默认联网 |
| --- | --- | --- |
| 领域/服务单元测试 | 输入规范化、WMO code 映射、两步编排、错误分类、单位和模型组装 | 否 |
| HTTP 适配器测试 | query params、固定域名、超时、429、4xx/5xx、坏 JSON、缺字段 | 否，使用 MockTransport/fixture |
| MCP 协议集成测试 | `tools/list`、inputSchema/outputSchema、annotations、`tools/call`、Tool error | 否，优先 SDK in-memory session |
| stdio 冒烟测试 | 子进程启动、Tool 发现、一次调用、退出、stdout 无协议外文本 | 否，可注入固定适配器或测试模式；不得把测试模式用于发布运行 |
| live contract 测试 | Open-Meteo 地理编码和当前天气最小响应契约 | 是，显式 opt-in，失败需区分网络/上游/代码 |
| Inspector 人工验收 | 连接、Tool 描述/Schema、成功与错误显示 | 查询天气时联网 |
| 构建/安装测试 | wheel/sdist 内容、双干净环境安装、console entry point、官方 SDK Client 从包启动 | 构建可离线；首次依赖解析可能联网 |

## 最低行为矩阵

- 有效中文城市、有效英文城市、带 `country_code` 的地点。
- 输入前后空白、过短/过长地点、非法国家代码。
- 地理编码无结果。
- 同名地点：返回解析后地点，使调用方能识别实际选择；限制写入文档。
- 地理编码超时、天气请求超时。
- 429、5xx、连接失败、无效 JSON、必填字段缺失。
- 成功结果通过输出 Schema，所有数值带明确单位和有效时间。
- Tool 列表只有首期授权的 `get_current_weather`。
- annotations 与只读/开放世界边界一致。
- 日志进入 `stderr`；`stdout` 不出现普通 `print`、调试文本或堆栈。
- 用户输入无法改变 scheme、host 或 path 基址。

## 当前门禁

F-002 继续复用以下默认离线门禁：

```text
uv lock --check
uv run ruff format --check .
uv run ruff check .
uv run mypy
清除 MCP_WEATHER_RUN_LIVE 后运行 uv run pytest -q --tb=short
git diff --check
```

Step 2 已使 packaging 配置契约全部转绿；当前完整默认 pytest 为
`62 passed, 1 skipped`，唯一 skip 仍是显式 live contract。Step 1 的历史红灯是
`6 failed, 56 passed, 1 skipped`，对应六项真实配置缺口。

`uv build`、wheel/sdist 审查属于 F-002 Step 3，双干净安装与 installed-package
stdio 验证属于 Step 4，两者均已通过。Inspector 是人工协议调试工具，不替代自动化协议集成测试；live API 测试
不应成为每次离线单元测试的硬依赖。

## F-002 packaging 测试分层

- Step 1 配置契约：静态读取 `pyproject.toml`，验证 package 状态、显式
  `uv_build`、`0.1.0`、console entry point、SPDX MIT 和 LICENSE/NOTICE。
- Step 1 制品骨架：明确 wheel/sdist 都是 Step 3 强制制品，不在红灯阶段调用构建。
- Step 1 安装骨架：明确 wheel-env/sdist-env 分离，并禁止 editable install 和
  `PYTHONPATH`；真实创建环境留在 Step 4。
- Step 2 已通过最小配置使 `10` 项 packaging 契约全部转绿，没有用生成空制品、
  跳过测试或放宽断言规避契约。
- Step 3 已执行真实构建，并使用 `tests/packaging/inspect_artifacts.py` 检查精确
  文件白名单、Core Metadata、entry point、wheel RECORD、源码一致性和敏感路径。
- Step 4 已在项目外 `wheel-env`/`sdist-env` 分别安装约定制品；安装 provenance、
  无 `PYTHONPATH` 的 console stdio、唯一 Tool、现代 discovery、确定性
  `structuredContent`、stdout/stderr、退出码和无遗留进程均通过。
- `tests/packaging/verify_installed_package.py` 不进入制品；它从安装环境自身导入
  包并读取 `direct_url.json` 区分 wheel/sdist 来源，固定 Tool handler 不访问网络。
- Step 5 独立 QA 将内嵌 README 检查从临时 Step 文字升级为与当前根 README
  UTF-8 内容一致；旧 `dist` 得到预期失败，新 QA 候选通过并重新完成两套安装验证。
- 用户随后从 Step 5 QA wheel 干净环境运行同一 installed-package 验证命令，并明确
  确认 UAT 通过；该确认不替代自动门禁，也不代表外部发布。
- F-002 按已批准决策不新增 GitHub Actions；Draft PR #3 明确记录 local-only 门禁
  例外，因此 PR 页面没有新增远程 CI 不能被误写成“CI 通过”或“未测试”。

截至 Step 6 QA，MCP 协议集成层已通过官方 SDK in-memory client 验证；真实子进程层分别验证生产入口的 Legacy 原始协议握手/discovery/退出、官方 v2 Client 的现代 discovery，以及测试专用固定 Server 的结构化 Tool call。默认测试仍全部离线；`tests/integration/test_open_meteo_live.py` 只有在显式设置 `MCP_WEATHER_RUN_LIVE=1` 时才执行真实 Open-Meteo 两步契约。最近一次默认结果为 `52 passed, 1 skipped`，唯一 skip 是 live contract。

子进程测试使用 10 秒单步超时；原始进程测试在 `finally` 中终止未退出进程，SDK client 则使用其上下文管理器执行关闭 stdin、限时等待和进程树清理。测试专用 Server 的诊断标记必须出现在 `stderr`，所有生产入口 `stdout` 行必须能解析为 JSON-RPC。

live contract 只断言固定 endpoint、响应模型、解析地点和来源/许可证元数据，不保存完整响应。Inspector 使用精确 v2.1.0、项目虚拟环境 Python、显式源码 `PYTHONPATH` 与工作目录；人工验证唯一 Tool、输入字段、annotations、结构化成功结果和稳定错误语义，结束后关闭进程并使临时认证令牌失效。

兼容性复验使用项目独立 Node 24.19.0 消除 Inspector engine warning。协议证据区分两条路径：stdio Inspector 的 Legacy `initialize`/2025-11-25 只证明向后兼容；官方 SDK v2 `Client(mode="auto")` 对生产 stdio 入口执行 `server/discover`，以 `protocol_version=2026-07-28`、存在 `discover_result` 且不存在 `initialize_result` 证明现代路径。测试专用 stdio Server 在同一现代协议下完成离线 Tool call。不得要求一个 2026 会话展示 `initialize=2026-07-28`，也不得把 Legacy Inspector 会话冒充现代协议证据。

## 验收证据格式

每项证据至少记录命令/操作、环境、预期、实际、结论、覆盖范围和未覆盖风险。不得保存完整网络响应、凭证、Cookie、个人位置或冗长终端日志。

## 独立审查

F-001 Step 6 曾完成一次独立 QA/差异审查，覆盖全部已跟踪和未跟踪文件，重点复核错误语义、stdio stdout 污染、任意 URL 风险、fixture 与 live 结论混淆，以及 README 是否夸大发布状态。该段是 F-001 历史记录；F-002 的独立 QA/UAT 证据见上文及 `docs/evidence.md`。
