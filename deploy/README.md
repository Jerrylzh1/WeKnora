# WeKnora 部署 / 升级脚本

本目录包含一键部署脚本 `deploy.ps1`(Windows PowerShell),用于把本地构建产物推送到服务器 `10.56.5.140` 并重启服务,方便后续版本迭代升级。

## 前置要求

- Windows + PowerShell
- 已安装 **Git for Windows**(脚本依赖其 `bash.exe`、`ssh`、`scp`,位于 `C:\Program Files\Git\bin`)
- 已配置 **SSH 公钥免密登录**(私钥默认 `~/.ssh/weknora_deploy`)
  - 公钥需写入服务器 `root@10.56.5.140:~/.ssh/authorized_keys`
  - 未配置则脚本无法在非交互环境自动连接
- Node.js + npm(用于本地构建前端)
- 服务器已部署好 `/data/weknora`(含 `docker-compose.yml` 与 `.env`)

## 脚本说明

文件:`deploy/deploy.ps1`

通过 SSH 密钥免密连接服务器(私钥路径见脚本顶部 `$KEY`),无需在脚本里写密码:

```powershell
$HOST   = '10.56.5.140'
$USER   = 'root'
$REMOTE = '/data/weknora'
$KEY    = "$env:USERPROFILE\.ssh\weknora_deploy"
$BASH   = 'C:\Program Files\Git\bin\bash.exe'
```

支持两种模式:

| 模式 | 作用 | 适用场景 |
|------|------|----------|
| `frontend` | 本地构建前端 → 上传 dist → 重建 `ui` 镜像 → 重启 | 仅改了前端文案/UI(如 `zh-CN.ts`、`Login.vue`) |
| `all` | 前端 + 远程从源码重建 `app`、`docreader` 镜像 → 重启 | 后端代码有改动需要升级 |

镜像 tag 通过 `WEKNORA_VERSION` 传入,compose 中以 `${WEKNORA_VERSION:-latest}` 引用。

## 使用方式

在 PowerShell 中进入项目根目录,执行:

```powershell
# 仅升级前端(最常用, 速度快)
.\deploy\deploy.ps1 -mode frontend

# 全量升级(后端有改动), 指定版本 tag
.\deploy\deploy.ps1 -mode all -version 0.7.3
```

脚本执行流程:

1. 本地 `npm ci && npm run build` 构建前端静态资源
2. `scp` 上传 `frontend/dist` 到服务器 `${REMOTE}/frontend/`
3. 远程 `docker compose build ui`(或 `app docreader`,取决于模式)
4. 远程 `docker compose up -d` 重启相关服务
5. 轮询 `http://10.56.5.140/health` 做健康检查

## 注意事项

- 改服务器密码时,只需修改脚本顶部 `$PASS` 一处
- `frontend` 模式不会重建后端镜像,后端升级务必用 `all` 模式
- 健康检查未通过时,登录服务器查看日志:`docker compose logs --tail=50 app`
- 若后续迁移到 SSH 公钥免密登录,可移除脚本中的 `sshpass -p` 部分
