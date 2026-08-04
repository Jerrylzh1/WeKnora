# WeKnora 分支管理规范（二开原则）

本规范用于约束本仓库的分支协作方式，并通过 Git 钩子从机制上强制拦截错误操作。

## 1. 分支角色

| 分支 | 角色 | 来源 | 更新方式 |
| --- | --- | --- | --- |
| `main` | 上游主干镜像（trunk） | 远程 `origin/main` | 仅 `git pull` 快进，**禁止直接推送、禁止本地合并** |
| `dev` | 个人二开分支（fork） | 从 `main` 切出 | 自由推送；通过 `git merge main` 吸收主干更新 |

## 2. 红线（强制）

1. ❌ **禁止 `git push origin main`**：`main` 只允许通过 Pull Request 合入。
2. ❌ **禁止把 `dev`（或其它分支）合并回 `main`**：同步方向只能 `main -> dev`，单向。
3. ✅ 只允许：`main` 从 `origin/main` 拉取；`dev` 把 `main` 的更新合并进来。

## 3. 日常操作流程

### 3.1 同步上游主干到本地 main
```bash
git checkout main
git pull                       # 等价于 git fetch + 快进到 origin/main
```

### 3.2 把 main 的更新带入 dev（单向合并）
```bash
git checkout dev
git merge main                 # 生成 merge 提交，记录本次同步
git push origin dev            # 快进推送，安全
```

### 3.3 提交你的二开改动
```bash
git checkout dev
# ... 编码、git add、git commit ...
git push origin dev
```

### 3.4 把 dev 的贡献合回主干
通过 GitHub 发起 **Pull Request**：`dev → main`，由仓库管理员评审后合并。
**绝不在本地执行** `git checkout main && git merge dev`。

## 4. 强制机制（Git 钩子）

钩子位于仓库 `.githooks/`，由 `core.hooksPath` 启用（见下方“启用方式”）：

- `pre-push`：拦截任何以远程 `main` 为目标的推送。
- `pre-merge-commit`：拦截在 `main` 分支上执行的合并（含 `dev` 合回 `main`）。

### 启用方式（每个克隆只需执行一次）
```bash
git config core.hooksPath .githooks
```

> 若 CI 也需要保护，请在仓库 Settings → Branches 为 `main` 开启
> **Branch protection（禁止直接 push / 要求 PR + 评审）**。

## 5. 错误示例与正确做法

| 错误操作 | 现象 | 正确做法 |
| --- | --- | --- |
| `git push origin main` | 被 `pre-push` 拒绝 | 推 `dev`，走 PR |
| `git checkout main && git merge dev` | 被 `pre-merge-commit` 拒绝 | `git checkout dev && git merge main` |
| `git checkout main && git merge feature` | 被 `pre-merge-commit` 拒绝 | 主干只通过 `git pull` 更新 |
