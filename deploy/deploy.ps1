<#
.SYNOPSIS
    WeKnora 一键部署/升级脚本 (Windows PowerShell, SSH 密钥免密)
.DESCRIPTION
    支持两种模式:
      -frontend : 仅升级前端 (本地构建 dist -> 上传 -> 重建 ui 镜像 -> 重启)
      -all       : 全量升级 (前端 + 远程从源码重建 app/docreader 镜像 -> 重启)
    依赖: Git for Windows 的 bash/ssh/scp (路径见 $BASH), 以及已配置好的 SSH 公钥免密登录。

.EXAMPLE
    .\deploy.ps1 -mode frontend
    .\deploy.ps1 -mode all -version 0.7.3
#>

param(
    [Parameter(Mandatory = $true)]
    [ValidateSet('frontend', 'all')]
    [string]$mode,

    # 镜像 tag, 默认 latest。compose 中通过 WEKNORA_VERSION 引用
    [string]$version = 'latest'
)

$ErrorActionPreference = 'Stop'

# ============ 服务器连接信息 (SSH 密钥免密) ============
$HOST     = '10.56.5.140'
$USER     = 'root'
$REMOTE   = '/data/weknora'
$KEY      = "$env:USERPROFILE\.ssh\weknora_deploy"   # 私钥路径
$BASH     = 'C:\Program Files\Git\bin\bash.exe'       # Git Bash 绝对路径
# ========================================================

$projRoot  = Resolve-Path (Join-Path $PSScriptRoot '..')
$distLocal = Join-Path $projRoot 'frontend/dist'

function Write-Step($msg) { Write-Host "`n==> $msg" -ForegroundColor Cyan }

# 统一通过 Git bash 调用 ssh/scp (免密, 无需密码)
function Invoke-Remote($cmd) {
    & $BASH -c "ssh -i '$KEY' -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null '${USER}@${HOST}' '$cmd'"
}
function Copy-ToRemote($local, $remote) {
    & $BASH -c "scp -i '$KEY' -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -r '$local' '${USER}@${HOST}:${remote}'"
}

# ---------- 1. 本地构建前端 ----------
Write-Step "本地构建前端 dist (npm ci && npm run build)"
Push-Location (Join-Path $projRoot 'frontend')
try { npm ci; npm run build }
finally { Pop-Location }

# ---------- 2. 上传 dist 到服务器 ----------
Write-Step "上传 frontend/dist -> ${REMOTE}/frontend/dist"
Copy-ToRemote $distLocal "${REMOTE}/frontend/"

# ---------- 3. 按模式构建镜像 ----------
if ($mode -eq 'all') {
    Write-Step "全量模式: 远程构建 app + docreader 镜像"
    $remote = "export WEKNORA_VERSION=${version}; cd ${REMOTE}; docker compose build app docreader"
}
else {
    Write-Step "前端模式: 仅重建 ui 镜像"
    $remote = "export WEKNORA_VERSION=${version}; cd ${REMOTE}; docker compose build ui"
}
Invoke-Remote $remote

# ---------- 4. 重启服务 ----------
Write-Step "重启服务 (docker compose up -d)"
$up = "export WEKNORA_VERSION=${version}; cd ${REMOTE}; docker compose up -d"
Invoke-Remote $up

# ---------- 5. 健康检查 ----------
Write-Step "等待并健康检查 http://${HOST}/health"
Start-Sleep -Seconds 8
try {
    $r = Invoke-WebRequest -Uri "http://${HOST}/health" -UseBasicParsing -TimeoutSec 10
    Write-Host "健康检查状态: $($r.StatusCode)" -ForegroundColor Green
}
catch {
    Write-Warning "健康检查未通过, 请登录服务器查看: docker compose logs --tail=50 app"
}

Write-Host "`n部署完成 ($mode 模式, 版本 tag=$version)" -ForegroundColor Green
