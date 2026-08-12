# R-002：Official MCP Registry 登记

## 生命周期

- 状态：`active / Step 5 complete / Draft readiness PR #11 awaiting user review and merge`。
- 等级：L；原因是首次向 Official MCP Registry 写入公开、同版本不可原地覆盖的元数据，
  并涉及 GitHub OAuth、公开条款和失败恢复。
- 起点：`main` 与 `origin/main` 均为
  `2fae2579517ebb5f7154f9646b54b4f174be6ffa`。
- 当前本地分支：`release/r-002-mcp-registry-0.1.0`；提交 `4d262c3` 已推送，Draft readiness PR #11 已创建。
- 交付策略：同一任务分两次 PR；readiness PR 先交付登记准备，closure PR 仅在公开登记复验后收口。
- 外部状态：PyPI `mcp-weather-query==0.1.0` 已公开；Official MCP Registry 尚未登记。

## 用户目标与业务价值

将已经公开并验证的 PyPI 版本 `mcp-weather-query==0.1.0` 登记到 Official MCP Registry，
使 Registry API 和下游聚合器能发现准确的包、版本、stdio 传输、运行提示和仓库元数据。
本任务不承诺所有 MCP Host 都会直接展示该条目。

## 当前能力与缺口

- 已有：唯一只读 `get_current_weather` Tool、stdio、公开 PyPI wheel/sdist、Trusted
  Publishing attestations、公开双干净安装与 installed-package stdio 证据。
- 已有：根目录 `server.json` 已通过静态契约和固定 publisher validate，公开包 README 含
  `mcp-name` ownership marker。
- 已有：当前 Registry schema、公开身份、OAuth 边界、不可变版本和失败恢复已有本地契约证据。
- 缺口：尚未完成 Draft readiness PR #11 的用户合并、Terms 接受、OAuth login、publish 或
  Registry API 公开条目复验。

## 已批准身份契约

| 维度 | 固定值 |
| --- | --- |
| Registry server name | `io.github.wcnm8888/mcp1-weather-query` |
| Python distribution | `mcp-weather-query` |
| 已发布版本 | `0.1.0` |
| import package | `mcp_weather_query` |
| console command | `mcp-weather-query` |
| package registry | PyPI |
| runtime hint | `uvx` |
| transport | `stdio` |
| repository | `https://github.com/wcnm8888/mcp1-weather-query`（保持 private） |
| ownership marker | PyPI 公开 README 中的 `mcp-name` marker |
| schema 基线 | `https://static.modelcontextprotocol.io/schemas/2025-12-11/server.schema.json` |
| 冻结语义 SHA-256 | `7363235e462331ea3ea12914eacd959a43bb6fb556caad35ff087983d5e39f0d` |

## 范围

- 固化 Registry 身份、安全、公开条款、版本生命周期和恢复契约。
- 使用已验证的官方 `mcp-publisher v1.8.1`，先独立校验，再分 Step 完成 GitHub OAuth 与单次发布。
- 只登记已公开的 `0.1.0`，不创建新 PyPI 版本。
- 通过 Official MCP Registry API 复核精确名称、版本、PyPI 引用、stdio 和仓库元数据。
- 公开登记后再次从 PyPI 安装并复验唯一 Tool 与 stdio，完成凭据处置和文档/Git 收口。

## 非目标

- 不修改 Tool 名称、描述、Schema、annotations、错误语义或天气业务代码。
- 不增加第二个 Tool、HTTP、Streamable HTTP、SSE、远程部署或任意 URL。
- 不发布新的 PyPI 版本，不上传 TestPyPI，不创建 GitHub Release，不登记社区目录。
- 不公开当前 private 仓库，不配置 Registry GitHub Actions workflow/environment。
- 不保证 Cherry Studio 或其他具体 Host 直接消费 Official Registry。
- 不下载或替换 publisher，不更新 uv、Python、Node、依赖或系统环境。

## 输入、输出与状态变化

- 输入：已公开 PyPI 0.1.0、固定 `server.json` 身份、官方 publisher、GitHub 账号
  `wcnm8888`、已批准的 Registry Terms/公开边界。
- 输出：Official MCP Registry 中唯一精确的 0.1.0 条目、官方 API 验证证据、登记后安装/stdio
  证据、关闭文档与两次 PR 交付记录。
- 状态只允许按以下顺序推进：
  `approved -> active -> registry-ready -> readiness PR -> merged -> terms accepted -> authenticated`
  `-> publish authorized -> published -> verified -> closure PR -> merged -> closed`。
- `validate`、`login`、`publish` 和公开复验必须是分离门禁；login 不授权 publish。

## 安全、条款与恢复边界

- 首次登记采用官方 GitHub OAuth device flow；不输出、提交或记录 token、Cookie、设备码和认证缓存。
- Registry metadata、GitHub 用户名和项目描述会公开，Registry Data 按 CC0 1.0 提供；仓库保持 private，
  安装来源为公开 PyPI 包。
- Registry 仍处 preview，允许服务或数据重置风险；同名同版本元数据按不可原地覆盖处理。
- publish 返回不确定结果时禁止盲目重试，先用官方 API 精确查询；已存在且完全一致则停止并审计，
  已存在但不一致则停止，不覆盖、不创建补丁版本。
- deprecated/deleted 只视为隐藏/状态变化，不视为擦除；任何恢复写入都需要新的明确授权。
- 登记后是否执行官方 logout/凭据处置属于独立确认，不手工删除认证文件。

## 测试矩阵与验收

| 层级 | 核心验证 | 网络/写入 |
| --- | --- | --- |
| 静态契约 | 身份、schema、唯一 package/version、stdio、无 secret/remote transport | 离线/无写入 |
| publisher 校验 | 固定 v1.8.1、摘要/来源、`validate` 成功与失败证据 | 可联网/无 Registry 写入 |
| readiness QA | PyPI marker、公开版本、Terms、OAuth tuple、恢复预案、全部离线门禁 | 只读 |
| OAuth | 官方 GitHub device flow，认证身份正确且无凭据泄漏 | 外部认证写入，单独授权 |
| publish | 仅一次发布已冻结的 0.1.0 metadata | Registry 写入，单独授权 |
| 公开复验 | 官方 API 精确条目、PyPI 引用、安装、唯一 Tool、stdio | 只读公网 |
| 收口 | 凭据处置、closure PR、合并后归档与状态一致 | 分段授权 |

最低验收标准：

1. Registry 身份与 PyPI 0.1.0、仓库、stdio/uvx 完全一致。
2. `server.json` 通过当前官方 schema 和固定 publisher validate。
3. 仓库保持 private，且没有 token、任意 URL、第二 Tool、HTTP/SSE 或额外发布路径。
4. readiness PR 的 CI 只执行安全构建/验证，不登录或发布 Registry。
5. Terms、OAuth、publish 均在各自门禁获得用户明确授权。
6. publish 不确定时按官方 API 先查后停，不盲重试。
7. 发布后官方 API 只出现精确名称和 `0.1.0`，元数据与冻结契约一致。
8. 安装来源仍为公开 PyPI，installed-package stdio 只发现 `get_current_weather`，结构化输出、
   stdout/stderr 和退出行为继续通过。
9. 凭据处置经用户确认，closure PR 合并后才允许归档并关闭 R-002。

## 文件与文档契约

- 预计允许影响：`server.json`、`tests/release/`、必要的制品状态断言、`README.md`、
  `docs/release-plan.md`、本任务治理文档和证据。
- 默认不影响：`src/`、Tool 契约、依赖、`pyproject.toml`、`uv.lock`、发布 workflow。
- 若需要改变默认不影响范围、公开仓库、创建新版本或增加传输方式，立即停止并重新批准范围。
- 当前任务状态以本文件为唯一入口；历史 R-001 任务卡和 QA 清单只读归档，不覆盖或删除。

## Step 地图

| Step | 唯一目标 | 当前状态 |
| --- | --- | --- |
| 0 | 任务基线、文档治理、R-001 QA 归档、本地分支与离线门禁 | **已完成** |
| 1 | 建立先失败的 Registry 身份、安全与生命周期契约 | **已完成：6 failed, 4 passed** |
| 2 | 最小修正 `server.json`、文档和契约，使红灯转绿 | **已完成：10 passed** |
| 3 | 核验固定 publisher/schema 并运行联网但不写入的 validate | **已完成** |
| 4 | 独立 QA、最终元数据冻结、公开 PyPI marker 复核与 UAT | **已完成** |
| 5 | readiness Git/PR；CI 不得 login/publish | 未开始 |
| 6 | 合并后同步 main、确认 Registry 仍为空、Terms 与认证边界 | 未开始 |
| 7 | 经单独授权执行 GitHub OAuth login，随后停止 | 未开始 |
| 8 | 经单独授权执行唯一一次 Registry publish | 未开始 |
| 9 | 官方 API、PyPI 引用、安装与 stdio 公开复验 | 未开始 |
| 10 | 经授权处置凭据、更新发布后文档/测试并创建 closure PR | 未开始 |
| 11 | 用户合并 closure PR 后同步、归档并关闭 R-002 | 未开始 |

Step 7、8、9 不得合并执行；每一 Step 完成后停止。

## 风险、依赖、回滚与停止条件

- 依赖：生产 PyPI 0.1.0、公开 ownership marker、Official Registry/API、GitHub OAuth、
  固定 publisher v1.8.1 和用户分段授权。
- 高风险：Registry preview/数据重置、公开 CC0 元数据、同版本不可变、名称冲突、OAuth 凭据、
  网络超时造成结果不确定、下游同步延迟。
- 回滚原则：登记前用 Git 分支/PR 回滚文档；登记后不承诺删除，按官方状态机制和新授权处置。
- 立即停止：身份或版本不一致、名称已被占用、schema/publisher 需要升级、需要修改业务代码或
  Tool 契约、需要公开仓库/新 PyPI 版本/新传输、发现敏感信息、OAuth 身份错误、publish 结果不确定、
  外部条款变化或任何未授权写入。

## 完成定义

R-002 只有在 readiness PR 合并、Terms 与 OAuth/publish 分段授权完成、Registry 官方 API 和
PyPI 安装/stdio 复验通过、凭据处置已决定、closure PR 已由用户合并、任务卡与 QA 已归档，且
`main == origin/main`、工作树干净时，才能标记为 closed。Step 0 仅建立治理基线，不代表已登记。

## 批准记录与下一门禁

- 用户已批准任务目标、范围、非目标、L 级判断、身份/认证/恢复方案、测试矩阵、Step 地图、
  完成定义及 15 项推荐决策，并先后明确允许进入 Step 0、Step 1、Step 2、Step 3 和 Step 4。
- Step 1 新增静态离线契约；定向结果为 `6 failed, 4 passed`，完整套件为
  `6 failed, 89 passed, 1 skipped`。排除故意红灯后既有回归为 `85 passed, 1 skipped`。
- Step 2 仅更新 README 与 release plan，补齐 active/未登记状态、preview/CC0、OAuth 分段
  授权、Step 3/7/8/9、不可变版本恢复和 publisher 复用边界；定向契约 `10 passed`，完整
  离线套件 `95 passed, 1 skipped`。
- 现有 `server.json` 已通过身份和最小范围契约，无需修改；Step 2 未改源码、workflow、依赖或锁文件。
- Step 3 通过 GitHub 官方 API 确认 latest/tag 均为 `v1.8.1`，官方 Windows AMD64 asset
  SHA-256 与本地归档一致；schema URL 返回 200 且 `$id` 与 manifest 一致。
- 固定二进制自报 `mcp-publisher 1.8.1`，未加入 PATH；唯一一次联网 `validate` 退出码 0，
  `server.json` 与 Git 状态前后不变。
- Step 4 独立审查全部已跟踪差异和两个未跟踪文件，修复两处门禁计数漂移及一处 validate
  陈旧描述；没有高、中优先级范围内缺陷。
- `server.json` 原始 SHA-256 为 `e0ad8ae8...c6709`，跨行尾/缩进的冻结语义 SHA-256 为
  `7363235e...e39f0d`，静态契约已固定该值。
- 生产 PyPI 0.1.0 的唯一 `mcp-name` marker、两个未 yank 制品和既有 SHA-256 均只读复核通过；
  Official Registry Terms 的 preview/data reset、CC0、公开 metadata/GitHub 用户名边界未漂移。
- Step 0–4 未执行 Registry login/publish、Terms 接受、外部写入、
  commit、push 或 PR。
- 用户已明确确认 `R-002 Step 4 UAT 通过`，并随后明确允许进入 `R-002 Step 5` readiness Git/PR。
- Step 5 授权仅覆盖当前冻结变更的精确提交、功能分支推送和 Draft PR；不授权合并、Terms、OAuth、login 或 publish。

## Step 4 用户 UAT 记录

用户已确认接受以下冻结事实：

1. 登记名称为 `io.github.wcnm8888/mcp1-weather-query`，版本仅为 `0.1.0`，引用公开 PyPI
   `mcp-weather-query`，运行提示 `uvx`，传输仅 stdio，仓库继续 private。
2. Registry 仍是 preview，可能发生 breaking changes/data reset；提交的 Registry Data 将按
   CC0 1.0 永久公开，可能包含 GitHub 用户名和 server description。
3. 同名同版本按不可原地覆盖处理；不确定 publish 必须先查询官方 API，不盲目重试；
   deprecated/deleted 不等于擦除。
4. 当前只完成 validate、QA 与 UAT；UAT 通过仍不授权 readiness PR、Terms、OAuth login 或 publish。
