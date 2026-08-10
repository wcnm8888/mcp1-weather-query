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
| 构建/安装测试 | wheel/sdist 内容、干净环境安装、console entry point、Inspector 从包启动 | 构建可离线；首次依赖解析可能联网 |

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

## 候选门禁

任务卡批准后再锁定精确命令，目标至少包含：

```text
uv sync --locked
uv run ruff format --check .
uv run ruff check .
uv run <type-checker> ...
uv run pytest
uv build --no-sources
干净临时环境安装 wheel 并执行 stdio smoke
npx @modelcontextprotocol/inspector <本地包启动命令>
```

Inspector 是人工协议调试工具，不替代自动化协议集成测试；live API 测试不应成为每次离线单元测试的硬依赖。

## 验收证据格式

每项证据至少记录命令/操作、环境、预期、实际、结论、覆盖范围和未覆盖风险。不得保存完整网络响应、凭证、Cookie、个人位置或冗长终端日志。

## 独立审查

首个实现任务完成后，需要一次独立 QA/差异审查，重点验证错误语义、stdio stdout 污染、任意 URL 风险、fixture 与 live 结论混淆，以及 README 中是否夸大发布状态。
