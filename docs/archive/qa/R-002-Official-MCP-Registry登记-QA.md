# R-002 L 级 QA 清单

> 状态：`closed / published / verified / credentials disposed`。勾选项必须有本任务的新证据；历史 R-001 或草案不能
> 冒充 Registry 登记证据。本清单不授权 validate、login、publish 或任何外部写入。

## Step 0 基线

- [x] R-002 目标、L 级风险、15 项决策、Step 地图和完成定义已获用户批准。
- [x] `main == origin/main == 2fae2579517ebb5f7154f9646b54b4f174be6ffa`，起始工作树干净。
- [x] `v0.1.0` 解引用到发布提交 `bb24624dcc8eb2efce5f4c49c80c850542c4d2b3`。
- [x] 已创建本地 `release/r-002-mcp-registry-0.1.0`，未提交或推送。
- [x] R-001 QA 已安全归档，R-001 任务卡与历史证据未删除或覆盖。
- [x] 基线 lock、format、lint、严格 mypy、`85 passed, 1 skipped` 和 diff 检查通过。
- [x] 未运行 publisher、Registry validate/login/publish、Terms 接受或外部写入。

## 身份与 schema（Step 1–3）

- [x] Registry 名称固定为 `io.github.wcnm8888/mcp1-weather-query`。
- [x] PyPI `mcp-weather-query==0.1.0`、import、console、`uvx`、stdio 和仓库引用完全一致。
- [x] 当前官方 schema 与固定 `mcp-publisher v1.8.1` 的来源、摘要和行为已重新核验。
- [x] 先失败契约覆盖唯一 package/version、ownership marker、无 secret 和无远程传输；
  定向结果为 `6 failed, 4 passed`，失败均为待实现文档边界。
- [x] Step 2 未删除或放宽契约；10 项静态离线契约全部转绿，完整门禁为
  `95 passed, 1 skipped`。
- [x] `server.json` 通过静态契约和 publisher validate；退出码 0，manifest/Git 前后不变，
  validate 没有 Registry 写入。

## 公开边界与恢复（Step 4）

- [x] 用户复核 Registry preview、CC0 1.0、公开 GitHub 用户名/项目 metadata 和 private repo 边界。
- [x] 同版本不可原地覆盖、名称冲突和不确定 publish 的先查后停策略有可执行静态契约。
- [x] PyPI 0.1.0 与公开 README 唯一 `mcp-name` marker 在 readiness 前再次核验。
- [x] 独立 QA 和用户 UAT 通过，冻结待登记 metadata；UAT 不授权 Step 5 或外部写入。

## Git 与认证（Step 5–7）

- [x] readiness PR 精确包含获准文件，CI 不执行 Registry login/publish。
- [x] readiness PR 已由用户合并，本地 main 同步且 Registry 精确名称仍为空。
- [x] 用户在官方界面复核 Terms 与认证边界，并单独授权 GitHub OAuth login。
- [x] OAuth 身份为 `wcnm8888`，没有 token、Cookie、设备码或认证缓存进入日志、文档或 Git。
- [x] login 后停止；没有把认证成功当作 publish 授权。

## 登记与公开复验（Step 8–9）

- [x] 用户单独授权单次 publish，待发布文件哈希/内容与冻结版本一致。
- [x] publish 结果明确；若不确定，先查官方 API 且没有盲目重试。
- [x] 官方 API 只出现精确名称和 0.1.0，PyPI、stdio/uvx、仓库元数据一致。
- [x] 从公开 PyPI 安装后仍只发现 `get_current_weather`，stdio/structuredContent/
  stdout/stderr/退出继续通过。
- [x] 未创建新 PyPI 版本、第二 Tool、HTTP/SSE、GitHub Release 或社区目录条目。

## 凭据、关闭与完成（Step 10–11）

- [x] 用户已决定官方 logout/凭据处置；固定 publisher logout 成功，没有手工删除未知认证文件。
- [x] 发布后文档、测试和证据与 Registry/PyPI/Git 事实一致。
- [x] Draft closure PR #12 已创建，目标为 `main`，没有自行合并。
- [x] closure PR #12 已由用户审查并合并。
- [x] Step 11 已同步 `main == origin/main`，任务卡与本清单已归档，R-002 标记 closed。
