# WeKnora 前端部署流程（Frontend Deploy Runbook）

> 适用场景：仅修改前端（`frontend/` 目录下的 Vue/TS/CSS/图片），需要重新打包并部署到生产服务器。
> 后端服务（app / postgres 等）保持 0.6.0 版本不变，本流程**只动 frontend 容器**。

---

## 1. 环境信息

| 项 | 值 |
| --- | --- |
| 生产服务器 | `10.56.5.140` |
| SSH 账号 | `root` |
| SSH 密码 | `Git@bjbus%` |
| 前端源码（本机） | `d:/AI-plat-form/01-githubcode/WeKnora/frontend` |
| 构建产物 dist（本机） | `d:/AI-plat-form/01-githubcode/WeKnora/frontend/dist` |
| 服务器 dist 目录 | `/data/WeKnora-build/frontend` |
| 服务器 compose 目录 | `/data/WeKnora-0.6.0` |
| 前端镜像 tag | `weknora-ui:0711-frontend-only` |
| 运行中的 frontend 容器 | `WeKnora-frontend` |

前端技术栈：Vue3 + Vite + TDesign，构建用 `npm`（本机 Node v24）。

---

## 2. 部署脚本（位于仓库根目录）

| 脚本 | 作用 | 依赖 |
| --- | --- | --- |
| `_tmp_upload_dist3.py` | ① 本机打包 `dist` → tar.gz ② SFTP 上传 → ③ 服务器备份旧 dist 并解压 | `paramiko`，密码读 `SERVER_PASSWORD` 环境变量 |
| `_tmp_rebuild_restart.py` | ① 服务器用最新 dist 重新 `docker build`（覆盖 tag）② `docker compose up -d frontend` 重启 ③ 校验并输出 HTTP 状态 | `paramiko`，密码读 `SERVER_PASSWORD` 环境变量 |
| `_tmp_transparent_logo.py` | 用 Pillow 把 `weknora.png` 白底去透明（仅换 logo 时才用） | `Pillow` |

> ⚠️ **关键陷阱（曾踩坑）**：compose 里 frontend 是 `image: weknora-ui:0711-frontend-only`，**没有 build 段**。
> 因此必须用 `_tmp_rebuild_restart.py` 在服务器 **真正重新 `docker build`** 把最新 dist 打进镜像。
> **不要**只 `docker tag` 旧镜像——旧镜像层里是旧 dist，容器不会更新（颜色/标题改了但不生效就是这个原因）。

---

## 3. 标准部署步骤

### 步骤 0：改完代码并保存
在 `frontend/` 下修改 Vue/TS/CSS/图片，保存。

### 步骤 1：本机构建 dist
在 **PowerShell** 中执行（仓库根目录或 frontend 目录均可，命令含 cd）：

```powershell
powershell -NoProfile -Command "cd d:/AI-plat-form/01-githubcode/WeKnora/frontend; if (Test-Path dist) { Remove-Item -Recurse -Force dist }; npm run build 2>&1 | Select-Object -Last 6"
```

- 等待 `✓ built in xx.xxs` 出现，exitCode 应为 0。
- Vite 构建约 50 秒，期间 PowerShell 可能看起来"卡住"，属正常，**耐心等完成再继续**。
- 不要 `Ctrl+C`，否则产物不完整。

### 步骤 2：上传 dist 到服务器
```powershell
powershell -NoProfile -Command "$env:SERVER_PASSWORD='Git@bjbus%'; cd d:/AI-plat-form/01-githubcode/WeKnora; python _tmp_upload_dist3.py"
```
- 脚本会：打包 → SFTP 上传 → 服务器备份旧 `dist` 为 `dist.bak.<时间戳>` → 解压新 `dist` → 校验透明 logo 资源。
- 看到 `[done]` 即成功。

### 步骤 3：服务器重新构建镜像并重启容器
```powershell
powershell -NoProfile -Command "$env:SERVER_PASSWORD='Git@bjbus%'; cd d:/AI-plat-form/01-githubcode/WeKnora; python _tmp_rebuild_restart.py"
```
- 脚本会：在 `/data/WeKnora-build/frontend` 用 `--no-cache` 重新 `docker build -t weknora-ui:0711-frontend-only .` → `docker compose up -d frontend` → 校验容器内 CSS 是否含新内容 → 输出 HTTP 状态码。
- 看到 `Successfully tagged weknora-ui:0711-frontend-only`、`Container WeKnora-frontend Started`、HTTP `200` 即成功。

### 步骤 4：浏览器强制刷新验证
打开 `http://10.56.5.140/`（或服务器对外域名/端口），**Ctrl+F5** 强刷清缓存，确认改动生效。

---

## 4. 常见问题排查

| 现象 | 原因 | 解决 |
| --- | --- | --- |
| 改了颜色/标题但页面没变 | 用了 `docker tag` 而非重新 `docker build`，容器跑旧镜像层 | 用 `_tmp_rebuild_restart.py` 真正重新 build |
| 构建命令被当成 cmd 执行报错 | 在 cmd 里跑了 PowerShell 语法 | 包一层 `powershell -NoProfile -Command "..."` |
| `tail` / `rmdir` 命令报错 | PowerShell 无这些命令 | 用 `Select-Object -Last N` / `Remove-Item -Recurse -Force` |
| 上传脚本卡住要输密码 | 未设置 `SERVER_PASSWORD` 环境变量 | 命令前缀加 `$env:SERVER_PASSWORD='Git@bjbus%';` |
| 登录页 logo 白底突兀 | png 带白底 | 用 `_tmp_transparent_logo.py` 去白底生成透明 png |

---

## 5. 回滚

若部署异常，服务器上旧 dist 已备份为 `/data/WeKnora-build/frontend/dist.bak.<时间戳>`，可恢复后重新执行步骤 3。
也可 `cd /data/WeKnora-0.6.0 && docker compose down frontend` 后用之前的镜像 tag 重新拉起。
