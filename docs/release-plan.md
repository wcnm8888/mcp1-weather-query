# 发布方案（PyPI 首发已完成）

## 结论

推荐顺序是：**先完成可安装的 Python 包 → 发布到 PyPI → 再登记 Official MCP Registry**。
`0.1.0` 已按该顺序完成 PyPI 发布、Registry 登记和公开安装复验。npm 不作为 Python 实现的
首发渠道；MCP Registry 是发现/元数据层，不托管 Python wheel/sdist，不能替代 PyPI。

任何 TestPyPI/PyPI 上传、Registry 注册、GitHub 公共仓库创建或社区平台发布都属于外部写入，执行前必须获得用户明确确认。

## R-002 Official MCP Registry 登记契约

R-002 只登记已经公开的 PyPI `mcp-weather-query==0.1.0`，Registry 名称固定为
`io.github.wcnm8888/mcp1-weather-query`，运行提示为 `uvx`，传输方式只允许 stdio。
Official MCP Registry 只保存发现元数据，不托管 wheel/sdist；安装来源继续是公开 PyPI。
当前 Registry 仍处于 **preview**，服务和数据可能重置。本任务接受 Registry Data 按
**CC0 1.0** 提供，也接受 Registry metadata、GitHub 用户名和项目描述公开；代码仓库保持
private，公开安装包与 ownership marker 由 PyPI 提供。仓库保持 private 不妨碍登记，但
Registry 登记也不会自动公开仓库或保证每个 MCP Host 都直接展示该条目。

### 工具与身份边界

- 复用项目外已验证的官方 `mcp-publisher v1.8.1`，归档 SHA-256 固定为
  `399ad0d6e00a50812b563a71d8bfbff5160c085e6b13aac6ec083d98d5ff7c45`。
- 该工具未加入 PATH；R-002 不下载、替换、安装或更新 publisher，也不修改 uv、Python、
  Node、依赖或系统环境。
- 首次 `io.github.*` 登记只采用手工 **GitHub OAuth device flow**，认证身份必须是
  `wcnm8888`。不保存或记录 token、Cookie、设备码和认证缓存。
- 本项目不配置 Registry GitHub Actions workflow/environment，不使用自动 OIDC 发布。
- **login 不授权 publish**；认证完成后必须停止，等待独立的 publish 授权。

### 分段网络和外部写入门禁

以下 Step 必须按顺序、分别获得授权并在各自完成后停止：

1. **Step 3 — validate**：核验固定 publisher/schema 后，只运行联网但不写入 Registry 的
   `mcp-publisher validate`。validate 成功只证明 manifest 可接受，不代表已经登录或登记。
2. **Step 7 — login**：readiness PR 合并、Registry 名称仍为空且用户接受公开条款后，才执行
   GitHub OAuth login；成功后停止，不运行 publish。
3. **Step 8 — publish**：用户再次明确授权后，只对冻结的 `server.json` 执行一次
   `mcp-publisher publish`，不得顺带创建 PyPI 版本、tag、Release 或其他目录条目。
4. **Step 9 — 官方 API**：发布结果明确后，使用 Official MCP Registry 官方 API 精确查询
   名称和 0.1.0，并重新验证公开 PyPI 安装与 installed-package stdio。

Step 3、Step 7、Step 8 和 Step 9 不得合并；Terms 接受、OAuth 登录和 Registry 写入也不得
由 CI、旧授权或一次笼统确认替代。

R-002 Step 3 已于 2026-08-12 完成：GitHub 官方 Releases API 确认 latest/tag 均为
`v1.8.1`，Windows AMD64 asset digest 与项目外归档一致；固定二进制自报版本 1.8.1，
未加入 PATH。官方 schema URL 返回 200，`$id` 与 `server.json` 的 `$schema` 一致。
唯一一次 `mcp-publisher validate` 退出码为 0 并返回 `server.json is valid`；manifest 哈希和
Git 状态前后不变。该结果不包含 OAuth、Terms、login、publish 或 Registry 条目写入。

R-002 readiness PR #11 已由用户合并；Step 6 将本地 `main` 以 fast-forward-only 同步到
`900f71133ad9525ff65965d0822a1e92d06faead`。Official Registry 包含 deleted 的精确名称搜索
仍为 0 条，精确 `0.1.0` detail 为 404；Terms 有效日期、SHA-256、preview、CC0 和公开身份
边界均未漂移。该结果不接受 Terms、不启动 OAuth，也不授权或执行 login/publish。

R-002 Step 7 已由用户单独授权并完成：固定 `mcp-publisher v1.8.1` 通过 GitHub device flow
认证为 `wcnm8888`，Registry JWT 权限仅覆盖 `publish io.github.wcnm8888/*`，随后立即停止。
JWT 有效期只有 300 秒；Step 8 若在过期后获得授权，必须同时明确允许一次重新 login。登录
没有创建 Registry 条目，精确名称搜索仍为空，也不构成 publish 授权。

R-002 Step 8 已由用户分段授权并完成：发布前重新核对冻结 manifest，随后固定
`mcp-publisher v1.8.1` 仅执行一次 `publish`。CLI 退出码为 0，明确发布
`io.github.wcnm8888/mcp1-weather-query==0.1.0`；没有第二次 publish 或其他 Registry 写入。

R-002 Step 9 已完成公开复验：Official Registry API 精确返回唯一 `active`/latest 的
`0.1.0`，metadata 与冻结 `server.json` 一致；从生产 PyPI 全新安装 `mcp-weather-query==0.1.0`
后，Legacy/现代 stdio、唯一 Tool、结构化结果、stdout/stderr、退出和无遗留进程均通过。

R-002 Step 10 已按用户授权使用固定官方命令 `mcp-publisher logout` 处置本机凭据。命令退出码
为 0，publisher 管理的认证文件已移除，且没有遗留 publisher 进程；没有手工删除未知文件，
也没有改变已经公开的 Registry 条目。

### 不可变版本与失败恢复

- Registry 的 `0.1.0` 按**同版本不可原地覆盖**处理；登记前冻结名称、版本、package、
  transport、repository 和 manifest 哈希。
- Step 4 冻结后的原始 `server.json` SHA-256 为
  `e0ad8ae8339d629629d7eef37f3927f081519e840eb85bfcf3297ba2bd6c6709`；按键排序、无多余空白
  的 UTF-8 规范化 JSON SHA-256 为
  `7363235e462331ea3ea12914eacd959a43bb6fb556caad35ff087983d5e39f0d`。发布前以后者作为
  跨平台语义冻结门禁，前者作为当前工作树字节证据。
- `publish` 超时、连接中断或返回不确定结果时**不得盲目重试**，必须先用官方 API 精确查询。
- 若查到的名称/版本/metadata **完全一致**，停止并记录为可能已成功，不再 publish；若名称或
  版本已存在但 metadata **不一致**，立即停止并审计，不覆盖、不创建补丁版本。
- `deprecated` 或 `deleted` 只按隐藏/状态变化理解，不视为从 Registry 数据中擦除；任何状态
  变更、恢复写入或凭据处置都需要新的用户明确授权。
- R-002 不承诺登记后的删除回滚。登记前错误用 Git/PR 修复；登记后以官方 API 事实和新的
  授权为准，不用历史 fixture、缓存或第三方目录冒充公开证据。

## R-001 生产 PyPI 发布契约

R-001 只面向生产 PyPI，**不使用 TestPyPI**。认证方案固定为 PyPI
**Pending Trusted Publisher** 与 GitHub Actions OIDC，不使用长期 PyPI API Token、
username/password、手工 `uv publish` 或 Twine 上传。

后续由用户在 PyPI 和 GitHub 页面配置的 publisher identity 必须精确为：

| 字段 | 固定值 |
| --- | --- |
| PyPI project | `mcp-weather-query` |
| GitHub owner | `wcnm8888` |
| GitHub repository | `mcp1-weather-query` |
| Workflow filename | `release.yml` |
| GitHub environment | `pypi` |
| Release tag | `v0.1.0` |

仓库内专用 workflow 位于 `.github/workflows/release.yml`。PR 只执行 build job；只有精确
tag `v0.1.0` 的 push 才允许 publish job 运行。build job 只具备 `contents: read`，发布 job
额外获得最小 `id-token: write`，并绑定 `pypi` environment。构建与发布分离：publish job
只下载 build job 的 wheel/sdist，再调用官方 PyPA action；所有 action 使用完整提交 SHA。
Trusted Publishing 的 attestation 保持默认开启，不配置 `attestations: false`。

安全 workflow 已经 PR #7 合并；GitHub environment `pypi` 和 PyPI Pending Publisher 已按
精确身份配置。`v0.1.0` 已触发 run `31567283749`，build 与 production PyPI publish job
均成功，`mcp-weather-query==0.1.0` 已公开。首发时采用的分层授权为：

1. PR 合并并复核公开包名后，用户单独授权登录 PyPI、配置 Pending Publisher 和
   GitHub environment；配置失败时停止，不降级为长期 Token。
2. Publisher、PR CI、最终制品、live contract 与 UAT 全部通过后，用户再次精确授权
   创建并推送 `v0.1.0`；该 tag 才可能触发真实上传。

PyPI 已发布的版本和文件不可覆盖。若 `0.1.0` 存在严重缺陷，优先在 PyPI **yank** 该
版本并准备新的补丁版本，不删除公开项目、不覆盖原文件，也不使用 `skip-existing` 掩盖
重复发布或版本冲突。

## 渠道对比

| 渠道 | 承载内容 | 适合本项目 | 前置条件 | 限制/风险 | 推荐 |
| --- | --- | --- | --- | --- | --- |
| PyPI | Python sdist/wheel 和元数据 | 与 Python/uv/`uvx` 最匹配 | 唯一包名、账号、Token 或 Trusted Publisher、完整包元数据 | 上传版本不可覆盖；公开发布；凭证和供应链风险 | **首个制品渠道** |
| npm | Node/TS 包和 `npx` 入口 | Inspector 本身使用 npm，但 Server 是 Python | npm 账号、2FA/token、Node 包装或重写 | 双生态维护、包装层无学习价值、可能造成版本漂移 | 不推荐首发 |
| Official MCP Registry | `server.json` 元数据、包/远程引用和发现 | PyPI 包发布后可提高 MCP 发现性 | 已发布制品；GitHub/DNS/HTTP 命名空间验证；官方 publisher CLI | Registry 不托管 artifact；登记是独立外部发布状态 | **PyPI 之后推荐** |
| GitHub Releases/源码仓库 | 源码、发行说明、可审查历史 | 有利于开源、Registry 命名空间和 Trusted Publishing | GitHub 账号、公开仓库授权、License | 不是 Python 包索引；公开范围需确认 | 可作为支撑渠道 |
| MCPB | 桌面端一键安装 bundle | 以后若明确需要桌面分发可评估；当前规范支持 uv runtime 类型 | 兼容 Host、manifest、跨平台验证 | 增加另一种打包与兼容矩阵 | 后续候选，不进入首期 |
| Smithery 等社区目录 | 第三方发现/托管能力 | 可能增加曝光 | 第三方账号、条款和元数据写入 | 不是官方 Registry；平台依赖和重复维护 | 首期不选 |

Datawhale 章节把 Smithery 称作“官方发布平台”，本项目不沿用这一表述。当前 Official MCP Registry 位于 `registry.modelcontextprotocol.io`；其官方 quickstart 明确说明 Registry 只存元数据，不存 artifact，并支持 npm、PyPI、OCI、MCPB 等包引用。

## 本地学习闭环

1. 使用 uv 管理稳定 Python 和锁定依赖。
2. 在项目环境运行已配置的唯一 `mcp-weather-query` console entry point，默认 stdio。
3. 用 SDK in-memory client 验证 Tool discovery/call/schema/error。
4. 用 stdio 子进程 smoke 验证真实进程边界和 stdout 纯净性。
5. 用 MCP Inspector 启动本地命令，人工检查 Tool 描述、Schema、成功和错误路径。
6. 运行单元、集成、lint、格式、类型和敏感信息检查。
7. 生成 wheel/sdist，在干净临时环境安装并再次执行 stdio smoke/Inspector。

F-002 已完成并关闭：新的本地 QA wheel/sdist 已生成、审查，并分别在项目外独立环境
完成无 `PYTHONPATH` 安装、stdio 复验和用户 UAT；PR #3 与收口 PR #4 均已合并，
但仍没有上传或发布。Inspector 不属于 D-001 默认验收，除非用户另行批准。

## D-001 发布候选命令契约

以下命令是 D-001 各 Step 使用的发布前检查基线；实际路径和结果分别记录在对应 Step。
候选目录固定在项目外
E 盘，避免把 wheel、sdist、publisher binary 或临时环境提交到仓库：

```powershell
$candidateRoot = 'E:\mcp-weather-query-release-candidate\0.1.0'
uv build --no-sources --out-dir "$candidateRoot\dist"
```

Step 4 必须同时得到一个 wheel 和一个 sdist，并在继续前检查文件清单、包元数据、
README、LICENSE、NOTICE、哈希及敏感信息。Step 5 再从这两个具体制品分别安装到两个
项目外干净环境；不得使用 editable install、源码目录或 `PYTHONPATH`。

Step 3 的通用阶段命令是 `mcp-publisher validate`。本次实际使用放在项目外且固定版本的
官方工具执行：

```powershell
E:\mcp-weather-query-tools\mcp-publisher\v1.8.1\bin\mcp-publisher.exe validate
```

在整个 D-001 中禁止执行以下外部写入命令：

```powershell
mcp-publisher login
mcp-publisher publish
```

同样禁止 `uv publish`、Twine 上传、创建 tag/Release 或任何 Registry/PyPI 写入。
v1.8.1 的 `validate` 会把本地 `server.json` 发送到未认证的官方
`https://registry.modelcontextprotocol.io/v0/validate` 端点，因此不是纯离线验证；它不读取
发布凭据、不调用 publish 端点，也不创建 Registry 条目。本次结果为
`✅ server.json is valid`，只代表 Schema/语义检查通过，不代表包已在 PyPI 发布或条目
已登记。

固定工具归档来自官方 v1.8.1 release，保存于项目外；归档 SHA-256 为
`399ad0d6e00a50812b563a71d8bfbff5160c085e6b13aac6ec083d98d5ff7c45`，与 GitHub
release asset digest 一致。该工具未加入 PATH，也未修改系统或项目环境。

## D-001 Step 4 候选制品

本次使用现有 uv 0.6.14 和项目内 Python 3.12.10，在项目外执行：

```powershell
uv build --no-sources --offline --out-dir `
  E:\mcp-weather-query-release-candidate\0.1.0\step4-20260811T205328\dist
```

`--offline` 成功，说明本次构建没有访问包索引；`--no-sources` 禁止使用 uv 的本地
source overrides。uv 先生成 sdist，再从该 sdist 生成 wheel。候选目录仅允许：

- uv 自动生成、内容为 `*` 的 1-byte `.gitignore`；
- `mcp_weather_query-0.1.0-py3-none-any.whl`；
- `mcp_weather_query-0.1.0.tar.gz`。

wheel SHA-256 为
`3e526b64d7f41a50679a586f54cda108ac7a8cc8b15d432faca4108c76da438a`；sdist
SHA-256 为 `eff5f30a417886c4ea6069cfaf95d41eae13067be4e4dc64a0eff25658090f4f`。
两者已通过文件白名单、Core Metadata 2.4、entry point、wheel RECORD、源码/法律文件
一致性、嵌入 README、Registry marker、未发布声明、本机路径和秘密扫描。Step 4 没有
安装或运行这些制品；安装与 stdio 验证属于 Step 5。

## D-001 Step 5 双干净安装

Step 5 没有重建制品，而是固定使用上节两个文件，在项目外新目录
`E:\mcp-weather-query-release-candidate\0.1.0\step5-20260811T210410` 创建独立
`wheel-env` 与 `sdist-env`。两者均使用 Python 3.12.10，并在 `UV_OFFLINE=1`、无
`PYTHONPATH`/`PYTHONHOME`/`VIRTUAL_ENV` 下分别从本地 wheel 与 sdist 安装。

安装 provenance 精确指向对应制品；模块来自各自 `Lib\site-packages`，console 来自各自
`Scripts\mcp-weather-query.exe`。两套环境均通过生产 stdio Legacy initialize/tools-list、
官方 SDK v2 MCP 2026-07-28 discovery 和确定性离线 Tool 调用，只暴露
`get_current_weather`。stdout 仅含协议消息，诊断仅进入 stderr，进程退出码为 0，且没有
遗留 Step 5 运行时进程。本结果只证明固定本地候选可安装、可启动，不代表已上传 PyPI
或登记 Registry。

## D-001 Step 6 QA 候选

独立 QA 修正根 README 的陈旧阶段文字后，Step 4 制品被嵌入 README 一致性门禁正确
判定为过期。旧目录保留为历史证据；新的用户 UAT 候选位于
`E:\mcp-weather-query-release-candidate\0.1.0\step6-qa-20260811T213511`。

- wheel：16,340 bytes，15 个文件，SHA-256
  `c93ab54579fdd92c8ed91a5c6ea3fe2c8b97373fc50abfbc8d42fdbd01b661b6`；
- sdist：11,904 bytes，14 个文件，SHA-256
  `f9d68065233674f7413b95ee10b0d297bcbae8b8f3ff6cfceecb6d4e1b4d18f2`。

该候选已重新通过静态审查、wheel/sdist 双独立安装和 installed-package stdio 复验。
用户 UAT 只能使用这组 QA 候选；它仍是本地文件，不代表 PyPI 或 Registry 发布。

## 发布闭环

1. 确认 License、Open-Meteo attribution、包名、console script、Python 版本范围和依赖范围。
2. 运行锁定门禁、live contract、干净构建和安装测试。
3. 审查 wheel/sdist 文件清单、README 渲染、元数据和敏感信息。
4. 生成版本号、CHANGELOG 和可回滚/弃用说明。
5. 如需 TestPyPI，先请求用户确认；TestPyPI 也是外部公开写入。
6. 用户确认后发布 PyPI；验证 `uvx`/干净环境从 PyPI 安装并运行。
7. 通过官方工具生成/校验 `server.json`，确保 PyPI 包中的 `mcp-name` 标记、版本、console 参数和 Registry 名称一致。
8. 用户再次确认后进行命名空间认证并发布 Registry 元数据。
9. 验证 Registry 条目实际指向已发布版本；分别记录 PyPI 与 Registry 状态。

## R-001 生产发布结果

包名为 `mcp-weather-query`；项目使用 MIT 与 Open-Meteo CC BY 4.0 署名；仓库保持
private；首发只使用生产 PyPI Trusted Publishing，没有 Token、人工上传或 TestPyPI。

- 发布版本/tag：`0.1.0` / `v0.1.0`。
- 发布提交：`bb24624dcc8eb2efce5f4c49c80c850542c4d2b3`。
- GitHub Actions run：`31567283749`；build 与 publish 均成功。
- wheel：16,341 bytes，SHA-256
  `7c305d46f1cb6d2d5072625f0aacdc6d2bc102ef39237f267a56bdfa83d8de8a`。
- sdist：11,931 bytes，SHA-256
  `573c7d4887d640714ba00f4d634d9300e7e763348025bfbd85088f9bd670ea25`。
- 两个 PyPI publish attestations 均绑定 `wcnm8888/mcp1-weather-query`、`release.yml`、
  environment `pypi`、`refs/tags/v0.1.0` 与上述提交，并通过官方验证器检查。
- 两个公开制品分别完成项目外干净安装和 installed-package stdio 复验。

后续 PyPI 版本、yank、GitHub Release 或仓库公开范围变化仍需独立任务和用户授权。
R-002 已完成 `0.1.0` 的 Official MCP Registry 单次登记与公开复验；当前 `server.json`
是该公开条目的冻结来源。任何后续版本、metadata 更新、deprecated/deleted 状态变更或
重新认证/发布都需要新的任务和用户授权。

## R-001 Step 3 固定候选

本地候选位于项目外
`E:\mcp-weather-query-release-candidate\0.1.0\r001-step3-20260812T003655`，由现有
uv 0.6.14 和项目内 CPython 3.12.10 以 `uv build --no-sources --offline` 生成：

- wheel：`mcp_weather_query-0.1.0-py3-none-any.whl`，16,523 bytes，15 files，
  SHA-256 `e95429d4744e14f36efeecc08833269a0c72202bfdf4f9e3255412c73d225b6e`；
- sdist：`mcp_weather_query-0.1.0.tar.gz`，12,107 bytes，14 files，
  SHA-256 `e824aa4c64cb7e202d60cbd6fe3f0920043401789b1f755967285cb76ee15b63`。

两个制品均通过静态审查，并分别在全新 `wheel-env`/`sdist-env` 中离线安装和完成
installed-package stdio 复验。它们仍是本地候选，不是 GitHub Actions artifact，更不是
已上传 PyPI 的公开文件；Step 4 独立 QA 若修改包体文件，必须重新构建而不能沿用旧哈希。

Step 4 独立 QA 没有修改任何包体文件，固定候选哈希保持不变。QA 修复了 workflow 的
供应链缺口：build job 现在必须在上传前运行 patch whitespace 检查和项目现有制品检查器，
确认 wheel/sdist 文件、元数据和内容白名单后才允许形成 CI artifact。新的显式 Open-Meteo
live contract 和用户固定 wheel UAT 均已通过，当前仍不授权 PR、Publisher 配置、tag 或上传。

## 参考资料

- [uv: Building and publishing a package](https://docs.astral.sh/uv/guides/package/)
- [PyPA: Packaging Python Projects](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
- [npm public package publishing](https://docs.npmjs.com/creating-and-publishing-unscoped-public-packages/)
- [Official MCP Registry quickstart](https://github.com/modelcontextprotocol/registry/blob/main/docs/modelcontextprotocol-io/quickstart.mdx)
- [Official MCP Registry API](https://registry.modelcontextprotocol.io/docs)
- [MCPB](https://github.com/modelcontextprotocol/mcpb)
