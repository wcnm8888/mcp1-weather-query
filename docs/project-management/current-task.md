# R-001 任务卡：PyPI 首次外部发布

## 生命周期状态

- 任务编号：`R-001`
- 状态：`approved / step_7_metadata_remediation / awaiting_pr_merge`
- 风险等级：`L`（公开发布、供应链配置和不可覆盖版本）
- 起点提交：`0d5d7be9271b71143cdbcdf768bfbde5ed4393d0`
- 本地分支：`agent/r-001-step7-release-metadata`
- PR 目标：`main`
- 外部发布：Step 7 已授权；尚未创建 tag、触发或执行上传

## 用户目标与业务价值

把已经通过本地构建、双干净安装和 installed-package stdio 验证的
`mcp-weather-query==0.1.0` 安全地发布到生产 PyPI，使外部用户能从公共 Python 包索引
安装并启动同一个 MCP Server，同时保留可复核的供应链、制品、协议和回滚证据。

## 当前能力与缺口

- 已有：可构建 wheel/sdist、稳定 console entry point、唯一只读 Tool、发布候选文档、
  `server.json` 草案、项目外双安装和 UAT。
- 已完成安全 workflow、项目外候选、独立 QA、live/UAT、PR 非发布 CI、PR #7/#8 合并、
  GitHub `pypi` environment 与精确 Pending Publisher 配置。
- Step 7 最终门禁发现 README/CHANGELOG 仍含发布前陈旧措辞；当前修复已把公开可用性改为
  PyPI 官方页面可核验状态，并把 `0.1.0` 日期冻结为 `2026-08-12`。尚待修复 PR 的 CI/合并、
  精确 tag、公开 PyPI/attestation、公共安装验证和发布后收口。

## 已批准决策

1. R-001 是独立 L 级任务，使用独立 QA 清单和分段外部授权。
2. 只发布到生产 PyPI，不使用 TestPyPI。
3. distribution 为 `mcp-weather-query`，import package 为 `mcp_weather_query`，console command 为 `mcp-weather-query`。
4. 首发版本固定为 `0.1.0`，Git tag 固定为 `v0.1.0`。
5. 使用 PyPI Pending Trusted Publisher，不使用长期 API Token。
6. 使用 GitHub Actions 构建和发布，仓库保持 private。
7. 优先使用 GitHub environment `pypi`；若当前账户/计划不可用，停止并由用户决策。
8. 只有推送精确 tag `v0.1.0` 才能进入发布 job；PR 和普通分支不得发布。
9. 不创建 GitHub Release。
10. wheel 与 sdist 都是强制发布制品。
11. 发布 action 使用官方 PyPA action，并保留默认 provenance/attestation。
12. 发布前需要新的 Open-Meteo live contract 证据，不复用 D-001 旧证据。
13. 公共说明必须标明学习项目、Open-Meteo 非商业免费 API、限额、无 SLA 和署名。
14. 严重缺陷优先 yank，不删除公开版本；版本和文件不可覆盖。
15. R-002 Registry 登记保持独立，不进入本任务。
16. PyPI 登录、Pending Publisher、tag 和上传分别保留明确门禁。

## 范围

- 固化发布契约和 workflow 安全边界。
- 完成最终发布元数据、CHANGELOG 和公开限制说明。
- 通过 GitHub Actions 以 Trusted Publishing 发布一个 wheel 和一个 sdist。
- 核对 PyPI 文件、元数据和 attestations；从公共 PyPI 干净安装并复验 stdio。
- 记录失败、恢复、yank 和后续版本策略。

## 非目标

- 不使用 TestPyPI、API Token、手工 `uv publish` 或 Twine 上传。
- 不登记 MCP Registry，不创建 GitHub Release，不公开仓库。
- 不发布 npm/MCPB，不进入 R-002。
- 不增加第二 Tool、HTTP/SSE/Streamable HTTP，不修改 Tool 契约或业务语义。
- 不更新 uv、Python、Node、依赖或系统环境，不修改 Cherry Studio 管理文件。
- 不采用 Open-Meteo 商业服务，不扩大到远程部署。

## 输入、输出与状态变化

- 输入：合并后的 D-001 基线、已批准身份/版本、受保护的 GitHub/PyPI 配置和逐门禁授权。
- 本地输出：发布契约测试、安全 workflow、最终元数据、构建/QA/授权证据。
- 外部输出：仅在后续明确授权后产生 PyPI `mcp-weather-query==0.1.0` 页面及两个制品。
- 状态按 `draft -> approved -> active -> QA/UAT -> PR -> merged -> publisher-ready -> published -> verified -> closed` 推进；任何本地成功都不能跳写为 `published`。

## Workflow 与权限边界

- PR job 只执行离线质量门禁、构建和制品审查，不申请 PyPI OIDC 权限、不上传。
- publish job 仅响应精确 tag `v0.1.0`，绑定 `pypi` environment，使用最小
  `id-token: write` 和 `contents: read` 权限；不得使用仓库密钥保存 PyPI Token。
- workflow 必须从同一源码构建 wheel/sdist，并把经过审查的制品交给官方 PyPA publish action。
- PyPI 账号登录、2FA、verified email、Pending Publisher 和 GitHub environment 均由用户控制；
  自动化不得读取或记录凭据。
- 若 private 仓库不能使用所需 environment，或 PyPI 名称/Publisher 配置被拒绝，立即停止。

## 测试矩阵

| 层级 | 重点 | 允许网络 | 通过条件 |
| --- | --- | --- | --- |
| 静态契约 | 触发器、权限、environment、action 固定版本、无 secret/token 路径 | 否 | 发布只能由精确 tag 触发 |
| 默认离线门禁 | lock、Ruff、mypy、pytest、范围扫描 | 否 | live contract 仅显式跳过 |
| 最终制品 | wheel/sdist、元数据、文件白名单、哈希、法律文本、敏感信息 | 否 | 两个制品均通过 |
| 双干净安装 | wheel 与 sdist 来源、console、唯一 Tool、structuredContent、退出 | 否 | 不依赖源码或 PYTHONPATH |
| 新 live contract | Open-Meteo 固定端点与真实响应契约 | 是，需 Step 4 授权 | 新证据通过且不冒充发布证据 |
| PR CI | PR 只检查/构建、不发布 | GitHub Actions | 无 OIDC 发布或外部写入 |
| 公开发布 | Trusted Publishing、文件、attestation | PyPI/GitHub | 精确版本和两个制品可见 |
| 公共安装 | 从生产 PyPI 安装并执行 stdio | PyPI | provenance 指向 PyPI，协议验收通过 |

## 验收标准

1. package/import/console/version/tag 身份一致。
2. PR 和普通分支不能触发上传，只有精确 `v0.1.0` tag 可进入发布 job。
3. workflow 使用 GitHub OIDC Trusted Publishing，无长期 PyPI Token。
4. 权限最小化，发布 job 绑定 `pypi` environment，第三方 action 固定不可变版本。
5. `uv build --no-sources` 生成且只生成约定 wheel/sdist。
6. 两个制品通过文件、元数据、README、LICENSE、NOTICE、哈希与秘密扫描。
7. wheel/sdist 分别在项目外干净环境安装并完成 installed-package stdio 验证。
8. 安装后只发现 `get_current_weather`，确定性调用返回合法 `structuredContent`。
9. stdout 仅协议消息，诊断仅 stderr，进程有限时间退出且无残留。
10. 默认离线门禁继续通过，默认不访问 live API。
11. 发布前有一次新的、明确标记的 live contract 证据和用户 UAT。
12. PR CI 通过且证明未发布；合并前不创建 tag。
13. 用户另行授权并成功配置 Pending Publisher 后，才可进入最终 tag 门禁。
14. 用户再次精确授权后才可创建并推送 `v0.1.0`。
15. PyPI 公共页面、版本、Python 范围、依赖、README、License、文件和 attestations 可复核。
16. 从生产 PyPI 安装不依赖项目源码、缓存制品或 `PYTHONPATH`。
17. 公开安装后的 console stdio、唯一 Tool、结构化输出和退出行为通过。
18. Open-Meteo 署名、非商业免费层、限额与无 SLA 限制在公开材料中清晰可见。
19. 没有 TestPyPI、Registry、GitHub Release、npm/MCPB 或额外 transport。
20. 失败不会被写成成功；名称冲突、环境不可用或 publish 失败会停止并保留证据。
21. 严重缺陷有 yank/后续补丁版本方案，不删除或覆盖 `0.1.0`。
22. 独立 QA、用户验收、Git/PR、发布后验证和文档收口全部完成后才关闭 R-001。

## Step 地图

- [x] Step 0：持久化任务卡、L 级治理基线、创建本地发布分支、运行离线基线。
- [x] Step 1：建立先失败的发布/workflow 安全契约。
- [x] Step 2：实现最终发布元数据和安全 CI workflow。
- [x] Step 3：本地重建、制品审查和双干净安装。
- [x] Step 4：独立 QA、新 live contract 和用户 UAT。
- [x] Step 5：Git/PR 交付；PR CI 只能检查，不能发布。
- [x] Step 6：合并后同步、公开名称复核和 Pending Publisher 配置；已单独授权并完成。
- [ ] Step 7：最终发布门禁与精确 `v0.1.0` tag；需要再次明确授权。
- [ ] Step 8：公开 PyPI 文件、attestation、安装和 stdio 验证。
- [ ] Step 9：发布后文档、Git 收口；停止在 R-002 之前。

## 文件影响范围

- 预期：`.github/workflows/`、`pyproject.toml`、`CHANGELOG.md`、`README.md`、
  `docs/release-plan.md`、发布契约测试、打包/安装验证脚本和项目管理文档。
- 原则上不改：`src/`、Tool Schema、`uv.lock`、`server.json` 的 Registry 发布状态。
- 构建制品、临时环境、日志和凭据必须留在仓库外且不得提交。

## 风险、依赖与回滚

- PyPI 名称在实际创建时仍可能被占用或拒绝；不得擅自改名。
- private 仓库的 GitHub environment 能力取决于账户计划；不可用即停止。
- 公开发布不可撤回为“从未发生”，版本/文件不可覆盖；错误版本优先 yank 并发布补丁。
- workflow/OIDC 配置错误可能造成失败或错误发布；必须用静态契约、PR 无发布证明和双授权降低风险。
- 依赖用户持有 PyPI 账号、verified email、2FA，以及后续分别执行/批准外部配置与 tag。
- 回滚只撤销未发布的本地/PR 变更；已发布版本不删除、不覆盖，按 yank/补丁版本处理。

## 停止条件

- 需要改变包名、版本、Tool 契约、transport、License 或公开范围。
- 需要 TestPyPI、长期 Token、公开仓库、GitHub Release 或 R-002。
- GitHub environment `pypi` 不可用，PyPI 名称/Publisher 配置被拒绝，或基线发生来源不明漂移。
- 需要登录 PyPI、配置 Pending Publisher、创建/推送 tag 或上传制品而尚无对应明确授权。
- 质量门禁、制品、live contract、PR CI 或公开安装验证失败且无法在本任务最小范围修复。
- 发现敏感信息、越权网络写入或不可复核的发布证据。

## 完成定义

R-001 只有在 `0.1.0` 已由获准 Trusted Publishing 发布到生产 PyPI、公开文件与
attestation 已核验、公共安装和 stdio 验证通过、文档/Git 收口完成后才能关闭。
本地构建、PR 合并、Publisher 配置或 tag 单独完成均不等于发布完成。

## 批准记录

用户已批准本任务卡的目标、范围、非目标、L 级风险判断、Trusted Publishing 方案、
测试矩阵、Step 地图、完成定义和 16 项决策，并已依次允许进入 Step 0 至 Step 7。
Step 4 的独立 QA、新 live contract 和用户 UAT 已通过；Step 5 Git/PR 已交付并合并；
Step 6 的环境与 Publisher 配置已完成。用户已确认 PyPI 邮箱已验证并授权 Step 7；该授权
不允许跳过修复 PR、最终门禁或扩大到 R-002。

PR #7 已由用户合并，merge commit 为 `7cc304b47a094a33ccb90b13f411547a6a255e99`；本地
`main` 已 fast-forward 到同一提交。用户已允许 Step 6；公开 PyPI JSON 查询为 404，说明
当前没有公开项目，且 Pending Publisher 不会预留名称。GitHub `pypi` environment 已创建并
可读取；用户已在 PyPI 官方页面成功添加精确 Pending Publisher：`mcp-weather-query` /
`wcnm8888` / `mcp1-weather-query` / `release.yml` / `pypi`。PR #8 已合并为 `fb986bd`。
Step 7 首次最终门禁因公开元数据仍写“未发布”而停止；用户随后授权本修复 PR。修复 PR
已创建为 Draft PR #9；首个 CI run `31566777632` 的 build/QA 成功且 publish job skipped。
合并前不得创建或推送 `v0.1.0`。

## 历史任务卡

- [`F-001 一个 Tool 的本地天气闭环`](../archive/task-cards/F-001-一个-Tool-的本地天气闭环.md)
- [`F-002 可安装与可构建闭环`](../archive/task-cards/F-002-可安装与可构建闭环.md)
- [`D-001 发布候选与发布前审查`](../archive/task-cards/D-001-发布候选与发布前审查.md)
