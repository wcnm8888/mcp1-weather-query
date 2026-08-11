# F-002 Progress

## 当前目标

把现有源码项目转换为可构建、可安装的 Python 包，并在项目外验证同一个 stdio MCP Server；本任务不执行外部发布。

## 当前状态

- 任务卡：已批准。
- 当前 Step：Step 6 已完成，Draft PR #3 已打开并等待用户审查。
- 当前分支：`feat/f-002-installable-package`，基于 `main == origin/main == 4d84ad0`。
- 文档治理：F-001 完整任务卡已归档，F-002 已成为唯一活动任务卡和实施计划。
- packaging：版本 `0.1.0` 的新 QA wheel/sdist 已真实构建、通过增强静态审查，并分别在新的项目外独立环境完成安装与 stdio 复验。
- Git/外部状态：功能分支已精确提交并推送；Draft PR #3 为 open/draft。没有推送 `main`、合并或发布。

## Step 0 结果

- 复用 Cherry Studio 管理的 uv 0.6.14 和项目内 CPython 3.12.10，未更新或覆盖任何环境。
- `uv help build` 证明该 CLI 具备 PEP 517、wheel 和 sdist 构建前端能力。
- Step 0 没有调用 `uv_build` 或执行 `uv build`，因此候选后端的实际版本兼容性仍待获准的后续构建 Step 验证。
- `uv lock --check`、Ruff format check、Ruff lint、严格 mypy 和 `git diff --check` 通过。
- 默认离线 pytest 为 `52 passed, 1 skipped`；唯一 skip 是显式 live contract，未访问 Open-Meteo。
- 变更范围仅包含任务归档和当前项目状态文档；没有修改 `pyproject.toml`、`uv.lock`、源码或测试。

## Step 1 结果

- 新增 `tests/packaging/test_project_contract.py`，把已批准的 distribution/import/command 命名、版本、`uv_build`、package 状态、MIT 和 NOTICE 变成可执行契约。
- wheel/sdist 制品矩阵要求 Step 3 覆盖两个制品；干净安装矩阵要求 Step 4 使用两个独立环境，且禁止 editable install 和 `PYTHONPATH`。
- 定向测试为 `6 failed, 4 passed`；失败准确对应当前尚未实现的六项 packaging 缺口。
- 完整 pytest 为 `6 failed, 56 passed, 1 skipped`，不能写成全量通过；唯一 skip 仍是显式 live contract。
- 排除新增红灯测试后，既有离线回归为 `52 passed, 1 skipped`；Ruff、严格 mypy、锁文件和 diff 检查通过。
- 没有修改生产 packaging 配置、源码或锁文件，没有生成 build/dist、安装环境或发布内容。

## Step 2 结果

- `pyproject.toml` 使用 `uv_build>=0.11.32,<0.12`，移除 `package=false`，并注册 `mcp-weather-query` console entry point。
- 版本从 `0.0.0` 更新为 `0.1.0`；新增 SPDX `MIT`、`license-files = ["LICENSE", "NOTICE"]`、MIT LICENSE 和独立 Open-Meteo CC BY 4.0 NOTICE。
- README 已区分项目代码 MIT 与第三方数据 CC BY 4.0，并说明结构化字段规范化不改变底层测量值。
- `uv.lock` 只把根项目从 `virtual / 0.0.0` 更新为 `editable / 0.1.0`，依赖数量仍为 46。
- 现有 uv 0.6.14 成功调用后端并把项目安装到现有项目环境；`.venv\Scripts\mcp-weather-query.exe` 存在。
- packaging 契约从 `6 failed, 4 passed` 转为 `10 passed`；完整默认测试为 `62 passed, 1 skipped`，唯一 skip 仍为 live contract。
- 未执行 `uv build`；没有 `dist/`、`build/`、wheel/sdist 或项目外安装证据。

## Step 3 结果

- `uv build` 成功先生成 sdist，再从 sdist 生成 pure-Python wheel。
- 最终 wheel 为 `mcp_weather_query-0.1.0-py3-none-any.whl`，15 个文件；最终 sdist 为 `mcp_weather_query-0.1.0.tar.gz`，14 个文件。
- `tests/packaging/inspect_artifacts.py` 检查精确文件白名单、METADATA/PKG-INFO、entry point、purelib/tag、运行依赖、Python 范围和法律文件。
- wheel RECORD 的覆盖、SHA-256 和大小全部复算一致；两个制品的生产源码和 LICENSE/NOTICE 与工作树逐字节一致。
- 本机绝对路径、`.runtime`、`.venv`、明显凭据赋值、tests/docs/cache/log 等未授权内容扫描通过。
- 初次制品内嵌构建前 README；更新状态并重建后，最终制品内嵌 README 与 Step 3 事实一致。
- 没有安装制品、创建项目外环境、访问 live API、运行 Inspector、上传或发布。

## Step 4 结果

- 在项目外 `E:\Agent\.tmp\mcp1-weather-query\f-002\step4-20260811-a` 创建
  `wheel-env` 和 `sdist-env`；两者均为 CPython 3.12.10，互不复用 site-packages。
- wheel 环境从 `mcp_weather_query-0.1.0-py3-none-any.whl` 安装；sdist 环境从
  `mcp_weather_query-0.1.0.tar.gz` 隔离构建后安装；均为 `mcp-weather-query==0.1.0`。
- 两套 import 均来自各自 `Lib\site-packages`，console 均来自各自 `Scripts`；
  子进程环境不含 `PYTHONPATH`、`PYTHONHOME` 或 `VIRTUAL_ENV`，工作目录在项目外。
- 生产 console 完成 raw initialize/tools-list，只发现 `get_current_weather`；退出码
  为 0、stdout 没有协议外文本、stderr 没有 traceback。
- 官方 SDK v2 Client 两套均协商 MCP 2026-07-28；测试专用 child 从已安装包创建
  Server，确定性调用返回通过 `CurrentWeatherResult` 的 `structuredContent`，诊断仅在 stderr。
- `tests/packaging/verify_installed_package.py` 未进入制品；没有 live API、Inspector、
  HTTP/SSE、第二 Tool、上传、发布、commit、push 或 PR。

## Step 5 独立 QA 结果

- 完整审查了 tracked/untracked 变更、packaging 配置、LICENSE/NOTICE、三个
  packaging 测试文件、F-001 归档和全部受影响文档；生产 `src` 没有变化。
- 发现旧 `dist` 内嵌 README/长描述落后于当前根 README；将门禁改为直接解码
  UTF-8 Core Metadata body 并要求与当前 README 一致，旧制品得到预期失败。
- 在 `E:\Agent\.tmp\mcp1-weather-query\f-002\step5-20260811-a` 构建新的 QA
  wheel/sdist；清单、元数据、RECORD、源码、法律文件、敏感路径和 README 均通过。
- 新候选分别安装到新 wheel-env/sdist-env，两套均通过来源、console stdio、唯一
  Tool、MCP 2026-07-28、structuredContent、stdout/stderr、退出和进程清理验证。
- 完整默认门禁为 `62 passed, 1 skipped`；Ruff、严格 mypy、锁文件和 diff 通过。
- 没有未解决的高、中优先级 F-002 范围内缺陷；用户已明确确认 UAT 通过。

## Step 6 Git/PR 交付结果

- 按意图拆分 build/package、packaging tests 和项目文档提交；没有使用未经审查的
  全量暂存，也没有提交 ignored 构建制品或项目外 QA 环境。
- 已推送 `origin/feat/f-002-installable-package`；推送后本地与远程功能分支一致。
- 已创建 [Draft PR #3](https://github.com/wcnm8888/mcp1-weather-query/pull/3)，
  base=`main`、head=`feat/f-002-installable-package`。
- PR 正文记录 `62 passed, 1 skipped`、制品/双安装/UAT 证据、回滚方式和不新增
  GitHub Actions 的 local-only 门禁例外。
- PR 仍为 Draft；未标记 Ready、未合并、未删除分支、未进入 Step 7 或发布。

## 唯一下一步

用户审查 Draft PR #3，并决定标记 Ready 或合并。合并前不得进入 Step 7 或外部发布。
