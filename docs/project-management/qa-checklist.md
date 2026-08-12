# R-001 L 级 QA 清单

> 状态：`active / step_7_metadata_remediation / awaiting_pr_merge`。本清单用于 R-001 的独立 QA 与发布授权审计；勾选项必须
> 有可复核证据。它不是发布证明，也不授权任何外部写入。

## 身份与公开边界

- [x] distribution/import/console/version/tag 全部一致。
- [ ] PyPI 页面公开内容仅包含批准的项目、License 和 Open-Meteo 限制说明。
- [x] 仓库继续 private，R-002、TestPyPI、GitHub Release、npm/MCPB 不在范围。

## Workflow 与供应链安全

- [x] 静态契约确认 PR/普通分支无发布路径；PR 上 publish job 因精确事件/ref guard 跳过。
- [x] publish job 只响应精确 `v0.1.0`，绑定 `pypi` environment。
- [x] 权限最小化，使用 Trusted Publishing，不保存长期 PyPI Token。
- [x] 发布 action 来自官方 PyPA 且固定完整 SHA；attestation 未被关闭。
- [x] build 与 publish 通过同一 artifact 交接，publish job 不隐式重建。
- [x] build 在上传前运行 patch whitespace 和制品内容/元数据检查，契约固定执行顺序。

## 本地和 CI 门禁

- [x] 当前基线：lock、format、lint、严格 mypy、`85 passed, 1 skipped`、diff 检查通过。
- [x] 发布契约覆盖触发器、权限、environment、action SHA 和无 secret 路径；Step 2 已全部转绿。
- [x] Step 3 wheel/sdist 文件、元数据、哈希、法律文本和敏感信息审查通过；Step 4 独立复审哈希不变。
- [x] Step 3 wheel/sdist 双干净安装与 installed-package stdio 通过。
- [x] Step 4 独立 QA 和新的显式 Open-Meteo live contract 通过。
- [x] 用户在固定 wheel 环境完成 UAT 并明确确认通过。
- [x] PR CI 通过且 publish job 明确 skipped，没有执行发布。

## 外部授权与发布

- [x] 用户单独授权并完成 PyPI 登录和 Pending Publisher 配置。
- [x] PyPI 项目名和 Publisher tuple 已由用户在官方页面核对并成功添加。
- [x] 用户确认 PyPI 邮箱已验证；PyPI 账号已按平台强制 2FA 完成登录和 Publisher 配置。
- [x] GitHub environment `pypi` 可用；没有 secrets，当前无额外保护规则。
- [x] 用户已明确授权 Step 7；实际创建/推送 `v0.1.0` 仍等待元数据修复 PR 合并和最终门禁。
- [ ] GitHub Actions 发布 run 成功，且仅发布 wheel/sdist 两个预期文件。

## 公开验证与恢复

- [ ] PyPI 项目、版本、README、Python 范围、依赖、License、文件哈希可复核。
- [ ] PyPI attestations 可见且与 workflow/commit/tag 对应。
- [ ] 从生产 PyPI 的全新环境安装，不使用本地缓存制品或源码目录。
- [ ] 公共安装后的 stdio、唯一 Tool、structuredContent、stdout/stderr 和退出通过。
- [ ] yank、补丁版本和失败记录策略已复核；不删除或覆盖公开版本。
- [ ] 发布后文档与 Git 收口完成，R-002 仍未启动。
