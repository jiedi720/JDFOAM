@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ============================================
echo   JDFOAM Auto Build Script
echo ============================================

if not exist "JDFOAM.py" (
    echo [Error] JDFOAM.py not found!
    pause
    exit
)

python -m PyInstaller JDFOAM.spec --distpath="." --workpath="C:/Temp_Build" --clean

echo.
echo --------------------------------------------
echo Build completed!
echo --windowed mode enabled.
echo Output directory: Current directory
echo --------------------------------------------
pause
