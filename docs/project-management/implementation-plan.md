# F-001 Implementation Plan

## 当前状态

- 当前任务：F-001 一个 Tool 的本地天气闭环
- 当前 Step：Step 0 已完成
- 当前分支：`feat/f-001-local-weather-tool`
- 下一步：等待用户允许进入 Step 1
- 禁止：自动进入后续 Step、打包、发布、push 或创建 PR

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

状态：`pending_approval`

- 建立 `pyproject.toml`、`src/mcp_weather_query/` 和授权测试目录。
- 锁定最小运行/开发依赖与静态类型检查工具。
- 先写输入、错误、固定 endpoint 和结构模型的失败测试/fixture。
- 不实现对外 Tool 成功逻辑。

验证目标：项目只使用 uv managed Python 3.12；失败测试能证明任务卡核心边界尚未实现；diff 不含无关或发布文件。

## Step 2：Open-Meteo 适配器与天气用例

状态：`pending`

实现地理编码、当前天气适配、响应校验、WMO 映射和错误分类，并通过离线测试。

## Step 3：FastMCP Tool 与结构化输出

状态：`pending`

注册唯一 Tool、Schema、描述、annotations、stdio 模块入口和 Tool execution errors。

## Step 4：stdio 与自动化门禁

状态：`pending`

完成 SDK in-memory、真实子进程 smoke、stdout/stderr、格式、lint、类型和默认离线测试。

## Step 5：live contract、Inspector 与用户验收

状态：`pending`

显式联网验证 Open-Meteo，使用 Inspector 验证 discovery/成功/错误，并等待用户 UAT。

## Step 6：独立 QA、文档与 Git 收口

状态：`pending`

独立审查、全量门禁、文档一致性和精确本地提交；不 push、不自动进入 F-002。

## 停止条件

- 需要第二 Tool、HTTP、打包、发布或任务卡外文件。
- 需要覆盖 Cherry Studio uv、修改系统 Python/注册表或全局环境变量。
- 同一根因连续三次无法证明或验证。
- 必需真实验收无法取得证据。
