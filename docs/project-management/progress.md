# Project Progress

## 当前状态

- F-001、F-002、D-001 与 R-001 均已完成并关闭。
- `mcp-weather-query==0.1.0` 已通过 GitHub Actions Trusted Publishing 发布到生产 PyPI。
- `v0.1.0`、`main` 与发布 workflow 均对应提交
  `bb24624dcc8eb2efce5f4c49c80c850542c4d2b3`。
- PyPI 的 wheel/sdist、SHA-256、Metadata 2.4、公开 README、License、依赖和
  attestations 已复核。
- wheel 与 sdist 已分别从生产 PyPI 下载，在两个项目外干净环境安装并完成
  installed-package stdio 复验。
- MCP Registry 尚未登记；当前无活动任务，等待用户从 roadmap 选择下一项。

## 最近完成：R-001

- 最终离线门禁：`85 passed, 1 skipped`；唯一 skip 为显式 live contract。
- 发布 run：`31567283749`；build 与 production PyPI publish job 均成功。
- wheel：16,341 bytes，SHA-256
  `7c305d46f1cb6d2d5072625f0aacdc6d2bc102ef39237f267a56bdfa83d8de8a`。
- sdist：11,931 bytes，SHA-256
  `573c7d4887d640714ba00f4d634d9300e7e763348025bfbd85088f9bd670ea25`。
- 两个制品的 PyPI publish attestations 均通过 `pypi-attestations 0.0.30` 验证，身份为
  `wcnm8888/mcp1-weather-query` / `release.yml` / `pypi` / `refs/tags/v0.1.0`。
- 两套公开安装均只发现 `get_current_weather`；现代协议为 `2026-07-28`，生产 Legacy
  握手为 `2025-11-25`，structuredContent、stdout/stderr、退出和进程残留检查均通过。

完整过程与最终证据见 `docs/evidence.md` 和归档的 R-001 任务卡。
