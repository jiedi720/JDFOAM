# 1. 环境初始化与编码设置
$OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

function Stop-Run {
    Write-Host "`n[Process Finished] Press any key to exit..." -ForegroundColor Gray
    $null = [Console]::ReadKey($true)
    exit
}

# 2. 博世 Px 代理逻辑：确保 Git 能联网
Write-Host ">> Checking Bosch PX Proxy..." -ForegroundColor Cyan
$pxPort = 3128
# 自动寻找 PX 路径，防止路径写错
$pxPath = "C:\Program Files\RB Local Proxy Manager\px.exe"
if (-not (Test-Path $pxPath)) { $pxPath = "C:\Program Files\px\px.exe" }

$pxAccessible = (Test-NetConnection -ComputerName 127.0.0.1 -Port $pxPort -ErrorAction SilentlyContinue).TcpTestSucceeded

if (!$pxAccessible) {
    Write-Host ">> Starting PX Proxy..." -ForegroundColor Yellow
    Start-Process -FilePath $pxPath -WindowStyle Hidden -ArgumentList "--pac=http://rbins-ap.bosch.com/hk.pac", "--foreground=1", "--log=4"
    Start-Sleep -Seconds 5
} else {
    Write-Host ">> PX Proxy is already running." -ForegroundColor Green
}

# 同时设置环境变量和 Git 全局配置（最稳妥）
$proxyUrl = "http://127.0.0.1:$pxPort"
$env:http_proxy = $proxyUrl
$env:https_proxy = $proxyUrl
git config --global http.proxy $proxyUrl
git config --global https.proxy $proxyUrl

try {
    # 3. 切换到项目目录（使用引号包裹路径）
    $path = "C:\Users\EJI1WX\OneDrive - Bosch Group\PythonProject\JDFOAM"
    if (Test-Path $path) {
        Set-Location -Path $path
    } else {
        throw "Project path not found: $path"
    }

    # 4. 配置身份
    git config user.name "jiedi720"
    Write-Host "`n--- Ready to Upload JDFOAM ---" -ForegroundColor Cyan

    # 5. Git 流程
    Write-Host ">> Adding files..."
    git add .

    $msg = Read-Host "Enter Commit Message (Default: Daily Update)"
    if ([string]::IsNullOrWhiteSpace($msg)) { $msg = "Daily Update" }

    Write-Host ">> Committing..."
    git commit -m $msg

    Write-Host ">> Pushing to GitHub (via PX Proxy)..." -ForegroundColor Yellow
    # 尝试推送
    git push -u origin main --force

    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n✅ Success! Files are now on GitHub." -ForegroundColor Green
    } else {
        Write-Host "`n❌ Failed! Checking if GitHub is accessible..." -ForegroundColor Red
    }

} catch {
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
} finally {
    # 推送完后可选：清理 Git 全局代理，以免影响其他不使用代理的任务
    # git config --global --unset http.proxy
    # git config --global --unset https.proxy
}

Stop-Run