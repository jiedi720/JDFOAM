@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ============================================
echo   JDFOAM Auto Build Script
echo ============================================

if not exist "JDFOAM.py" (
    echo [Error] JDFOAM.py not found!
    pause
    exit /b 1
)

echo [Info] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [Error] Python is not installed or not in PATH!
    pause
    exit /b 1
)

echo [Info] Installing dependencies from requirements.txt...
pip install -r requirements.txt

echo [Info] Starting build process...
python -m PyInstaller JDFOAM.spec --distpath="." --workpath="C:/Temp_Build" --clean

if errorlevel 1 (
    echo [Error] Build failed!
    pause
    exit /b 1
)

echo.
echo --------------------------------------------
echo Build completed successfully!
echo Executable: JDFOAM.exe
echo Output directory: Current directory
echo --------------------------------------------
pause
