# F-002 Implementation Plan

## 当前状态

- 当前任务：F-002 可安装与可构建闭环
- 当前状态：`approved / step_6_completed / draft_pr_open / awaiting_user_review`
- 当前分支：`feat/f-002-installable-package`
- 基线：`main` 与 `origin/main` 均为 `4d84ad0`
- 当前唯一目标：等待用户审查 Draft PR #3，并决定 Ready/合并
- 下一门禁：用户 PR 审查；合并后才可授权 Step 7 收口
- 禁止：自动标记 Ready、合并、删除分支、进入 Step 7 或发布

## Step 0：任务与构建基线

状态：`completed`（2026-08-11）

- [x] 用户批准 F-002 任务卡及 14 项命名、License、构建、测试和交付决策。
- [x] 确认工作树干净，`main == origin/main == 4d84ad0`。
- [x] 创建 `feat/f-002-installable-package`。
- [x] 将 F-001 完整任务卡归档到 `docs/archive/task-cards/`。
- [x] 建立 F-002 current-task、implementation-plan 和短 progress 入口。
- [x] 只读核验 uv 0.6.14 的 build frontend 能力与候选 `uv_build` 兼容边界。
- [x] 运行 F-002 修改前默认离线基线门禁：`52 passed, 1 skipped`，其余门禁通过。
- [x] 复核 Step 0 diff 只有任务、计划、归档和状态文档。
- [x] 将 Step 0 标记完成并停止，等待用户允许进入 Step 1。

Step 0 不修改 `pyproject.toml`、`uv.lock`、源码、测试、License/NOTICE，不执行 `uv build`。

只读兼容性结论：uv 0.6.14 的 CLI 支持 PEP 517、`--wheel` 和 `--sdist`；本 Step
没有调用候选 `uv_build`，其实际后端兼容性仍须在获准的后续构建 Step 验证。

## Step 1：先失败的 packaging 契约测试

状态：`completed`（2026-08-11）

- [x] 建立 build-system、package、entry point、版本、License/NOTICE 契约。
- [x] 建立 wheel/sdist 和双干净安装隔离矩阵骨架。
- [x] 定向红灯稳定为 `6 failed, 4 passed`。
- [x] 完整 pytest 如实为 `6 failed, 56 passed, 1 skipped`。
- [x] 排除新增红灯后，既有离线回归仍为 `52 passed, 1 skipped`。
- [x] Ruff format/lint 和严格 mypy 通过。
- [x] 未修改 `pyproject.toml`、`uv.lock`、源码、LICENSE/NOTICE，未构建制品。

## Step 2：最小可安装包配置

状态：`completed`（2026-08-11）

- [x] 配置官方当前 `uv_build>=0.11.32,<0.12` 和默认 `src` layout。
- [x] 启用 package，设置版本 `0.1.0` 和 `mcp-weather-query` console script。
- [x] 新增 MIT LICENSE、Open-Meteo NOTICE 和必要元数据。
- [x] 锁文件只发生根项目 `virtual` → `editable` 和 `0.0.0` → `0.1.0` 变化。
- [x] Step 1 契约为 `10 passed`，完整默认测试为 `62 passed, 1 skipped`。
- [x] Ruff、严格 mypy、锁文件和 diff 门禁通过。
- [x] 未执行 `uv build`，未生成 wheel/sdist 或项目外安装环境。

## Step 3：真实构建与制品审查

状态：`completed`（2026-08-11）

- [x] 使用 `uv build` 生成 sdist 和从 sdist 构建的 wheel。
- [x] 新增并运行 `tests/packaging/inspect_artifacts.py`，精确审查两个制品。
- [x] wheel 15 个文件、sdist 14 个文件，清单符合任务卡。
- [x] METADATA/PKG-INFO、entry point、purelib/tag、依赖、Python、MIT 和
  License-File 检查通过。
- [x] RECORD 覆盖、SHA-256 和大小复算通过；源码/法律文件与工作树一致。
- [x] 绝对本机路径、runtime/venv、明显凭据赋值和未授权文件扫描通过。
- [x] 更新 README 后重新构建并复核最终制品，避免嵌入陈旧状态。
- [x] 未安装、上传或提交 `dist/`。

## Step 4：双干净环境安装与 stdio smoke

状态：`completed`（2026-08-11）

- [x] 在 `E:\Agent\.tmp\mcp1-weather-query\f-002\step4-20260811-a` 创建独立
  `wheel-env`、`sdist-env` 和各自外部工作目录。
- [x] 分别从约定 `.whl`/`.tar.gz` 安装，不使用 editable install 或 `PYTHONPATH`。
- [x] `direct_url.json`、module 与 console 路径证明制品和安装环境来源准确。
- [x] 两套生产 console 均完成 stdio handshake/tools-list，只发现唯一 Tool，
  stdout 仅协议消息，退出码 0，stderr 无 traceback。
- [x] 两套官方 SDK v2 Client 均通过现代 MCP 2026-07-28 discovery；测试 runner
  使用已安装包完成 synthetic/offline Tool call，返回合法 `structuredContent`。
- [x] 测试 runner 未进入 wheel/sdist；未访问 live API、运行 Inspector或遗留子进程。

## Step 5：独立 QA 与用户 UAT

状态：`completed`（2026-08-11）

- [x] 独立审查任务卡、完整 tracked/untracked diff、制品和双安装证据。
- [x] 修复制品门禁未能拒绝陈旧 README 的缺陷；旧 `dist` 预期失败。
- [x] 在新项目外 QA 目录构建、审查并双安装验证最终 UAT 候选。
- [x] lock、format、lint、严格 mypy、全量默认 pytest、artifact、范围和敏感信息门禁通过。
- [x] 用户从 QA wheel 环境运行验证命令并确认无需源码路径，UAT 通过。
- [x] 未把本地构建/安装写成外部发布。

## Step 6：Git/PR 交付

状态：`completed / draft_pr_open / awaiting_user_review`（2026-08-11）

- [x] 精确审查和分批暂存；构建配置/License、测试、文档按意图提交。
- [x] 推送 `feat/f-002-installable-package` 并创建 Draft PR #3，目标为 `main`。
- [x] F-002 不新增 GitHub Actions；PR 明确记录 local-only 门禁例外。
- [ ] 用户审查后决定 Ready/merge；不自动合并。

## Step 7：合并后收口

状态：`pending`

- 验证远程合并并安全同步本地 main。
- 归档 F-002，重置 current-task，压缩 roadmap/progress/evidence。
- 删除已合并分支前取得用户确认。
- 不自动选择或执行 D-001。

## 默认质量门禁

Step 0 基线和后续默认离线门禁：

```powershell
$env:MCP_WEATHER_RUN_LIVE = $null
uv lock --check
uv run ruff format --check .
uv run ruff check .
uv run mypy
uv run pytest -q --tb=short
git diff --check
```

F-002 后续追加的门禁必须来自任务卡：build、artifact、clean-install、console stdio 和 installed-package offline call。

## 停止条件

- Git 基线或工作树出现无法解释的差异。
- 真实制品构建暴露现有 uv/backend 不兼容，或需要更新 Cherry Studio/系统环境。
- 需要修改 Tool 契约、数据源、错误语义、增加 transport 或第二 Tool。
- 需要 live API、Inspector、GitHub Actions、外部上传、Registry 或 Release。
- 干净安装只能依赖 editable install、源码目录或 `PYTHONPATH`。
- 需要删除/覆盖用户文件、出现敏感信息或范围扩大到 M。
