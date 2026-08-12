# Changelog

本文件记录用户可见的版本变化。版本日期在对应发布内容冻结、进入最终 tag 门禁时确定。

## [0.1.0] - 2026-08-12

### Added

- 一个只读 MCP Tool：`get_current_weather`。
- 使用地点名称和可选国家代码查询 Open-Meteo 当前天气，并返回符合 output Schema 的
  `structuredContent`。
- 官方 MCP Python SDK v2、stdio transport、稳定 Tool execution error 和 stderr 诊断。
- `mcp-weather-query` console command，以及本地 wheel/sdist 构建和双干净安装验证。
- MIT License 与 Open-Meteo / CC BY 4.0 attribution。

### Limitations

- 只提供当前天气；没有预报、历史天气、空气质量或第二个 Tool。
- 只支持 stdio；没有 HTTP、Streamable HTTP、SSE 或远程托管。
- 天气和地点解析依赖固定的 Open-Meteo 官方端点；免费层没有项目自有 SLA。
- 当前支持的 Python 范围为 `>=3.12,<3.13`。

### Publication status

版本 `0.1.0` 是生产 PyPI 首发内容；公开可用性、文件和 attestation 以 PyPI 官方项目页
为准。MCP Registry 尚未登记，本次 PyPI 发布不等于 Registry 登记。
