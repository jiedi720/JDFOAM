@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo Switching to main branch...
git checkout main

echo Adding files...
git add -A

echo Committing changes...
set /p msg="Enter update message (press Enter for default 'Daily update'): "
if "%msg%"=="" set msg=Daily update
git commit -m "%msg%"

echo Force pushing to GitHub...
git push origin main --force

if %errorlevel% == 0 (
    echo.
    echo Update completed! Project synced to main branch.
) else (
    echo.
    echo Push failed, please check VPN connection.
)
pause