# 发布方案（方向已确认，未授权执行）

## 结论

推荐顺序是：**先完成可安装的 Python 包 → 发布到 PyPI → 再登记 Official MCP Registry**。npm 不作为 Python 实现的首发渠道；MCP Registry 是发现/元数据层，不托管 Python wheel/sdist，不能替代 PyPI。

任何 TestPyPI/PyPI 上传、Registry 注册、GitHub 公共仓库创建或社区平台发布都属于外部写入，执行前必须获得用户明确确认。

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

当前 F-002 Step 5 已完成：新的本地 QA wheel/sdist 已生成、审查，并分别在项目外
独立环境完成无 `PYTHONPATH` 安装、stdio 复验和用户 UAT；仍没有上传或发布。
Draft PR #3 只交付源码、测试、配置和证据，不包含构建制品或发布动作。Inspector
不属于 F-002 默认验收，除非用户另行批准。

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

## 发布前必须确认

- 最终 PyPI 包名和 MCP Registry server name。
- License 与 Open-Meteo CC BY 4.0 署名文本。
- 是否创建公开 GitHub 仓库，以及账号/组织命名空间。
- 使用 PyPI Token、Trusted Publisher 还是人工上传；不把凭证写入项目。
- 是否先使用 TestPyPI。
- 是否接受 Open-Meteo 免费层仅限非商业、10,000 次/日且无 SLA；若不接受则重新选源或确认付费服务。

## 参考资料

- [uv: Building and publishing a package](https://docs.astral.sh/uv/guides/package/)
- [PyPA: Packaging Python Projects](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
- [npm public package publishing](https://docs.npmjs.com/creating-and-publishing-unscoped-public-packages/)
- [Official MCP Registry quickstart](https://github.com/modelcontextprotocol/registry/blob/main/docs/modelcontextprotocol-io/quickstart.mdx)
- [Official MCP Registry API](https://registry.modelcontextprotocol.io/docs)
- [MCPB](https://github.com/modelcontextprotocol/mcpb)
