# 验收证据索引

## F-001 / Step 0

日期：2026-08-11

### 项目与 Git 前置事实

- 操作：列出项目文件，执行 Git worktree 探测。
- 结果：Step 0 前仅有 9 份 Markdown 规划文档，目录不是 Git 仓库，无源码、依赖、分支或远程。
- 结论：符合“启动新项目”和用户授权的本地 Git 初始化前提。

### uv 能力

- 命令摘要：`uv --version`、`uv python install --help`。
- 结果：Cherry Studio 管理的 uv 0.6.14 支持 managed Python 安装；未更新或覆盖该可执行文件。
- 未覆盖：F-001 项目依赖解析属于 Step 1。

### Python 3.12 基线

- 环境边界：`UV_PYTHON_INSTALL_DIR` 和 `UV_CACHE_DIR` 临时指向项目 `.runtime/`，未设置全局环境变量。
- 操作摘要：安装 Python 3.12；使用 `uv python find --managed-python --no-python-downloads 3.12` 查找；直接运行解释器 `--version`。
- 结果：找到项目内 CPython 3.12.10，解释器报告 `Python 3.12.10`。
- 异常说明：首次前台安装命令因工具 64 秒上限中断；续行完成后以 managed-python 查找和解释器版本进行最终验证，未把超时写成成功。
- 风险：系统注册表仍残留一个不存在的 Python 3.12 路径；项目通过 `--managed-python` 和项目安装目录绕开，未修改注册表。

### 文档与敏感信息

- 操作：检查文档入口、任务卡状态、相对链接、非 Markdown 业务产物和常见敏感信息模式。
- 预期：Step 0 只有基线/状态文件，无业务代码或凭证。
- 结果：通过；最终 Git diff 和 staged diff 在基线提交前再次检查。

### Git 基线

- 范围：本文件所在的 root baseline commit，以及由其创建的 `feat/f-001-local-weather-tool`。
- 复现：`git log --oneline --decorate -n 3`、`git status --short --branch`、`git remote -v`。
- 预期：`main` 与功能分支起点一致；当前位于功能分支；无远程；工作树干净。
- 结果：由 Step 0 最终 Git 验证确认，提交哈希以 Git 事实为准，不在提交内容中自引用。

## 未完成证据

- F-001 Step 1–6：未执行。
- 天气业务、自动化测试、live API、Inspector、构建、发布：均无通过结论。
