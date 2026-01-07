@echo off
chcp 65001 >nul

echo ============================================
echo Clear Parent Folder Script (Move to Recycle Bin)
echo ============================================
echo.
echo This will MOVE all files and folders in the parent directory to Recycle Bin
echo EXCEPT:
echo   - .git folder (Git repository)
echo   - GitSync folder (This script's location)
echo.
echo WARNING: Files will be moved to Recycle Bin, not permanently deleted!
echo.
echo Current parent directory:
cd /d "%~dp0.."
cd
echo.
echo Files and folders to be moved to Recycle Bin (excluded: .git, GitSync):
echo.
dir /b /a-d
dir /b /ad | findstr /v "^\.git$" | findstr /v "^GitSync$"
echo.
echo Press Ctrl+C to cancel, or any key to continue...
pause >nul

echo.
echo Starting cleanup...
echo.

REM Change to parent directory
cd /d "%~dp0.."

REM Create a temporary VBScript to move files to Recycle Bin
set "VBS_SCRIPT=%TEMP%\MoveToRecycleBin.vbs"

echo Set objShell = CreateObject("Shell.Application") > "%VBS_SCRIPT%"
echo Set objFolder = objShell.Namespace(0) >> "%VBS_SCRIPT%"
echo Set objFolderItem = objFolder.ParseName("%TEMP%\RecycleBinTemp") >> "%VBS_SCRIPT%"
echo objFolderItem.InvokeVerb "delete" >> "%VBS_SCRIPT%"

REM Create temporary directory for files to be recycled
set "TEMP_DIR=%TEMP%\RecycleBinTemp"
if exist "%TEMP_DIR%" rd /s /q "%TEMP_DIR%"
mkdir "%TEMP_DIR%"

REM Move all files to temp directory (except those in .git and GitSync)
echo [==========                    ] 25%% Moving files to temp directory...
for /f "delims=" %%f in ('dir /b /a-d ^| findstr /v "^GitSync"') do (
    echo Moving file: %%f
    move /y "%%f" "%TEMP_DIR%\" >nul 2>&1
)

REM Move all folders to temp directory except .git and GitSync
echo [==================            ] 50%% Moving folders to temp directory...
for /f "delims=" %%d in ('dir /b /ad ^| findstr /v "^\.git$" ^| findstr /v "^GitSync$"') do (
    echo Moving folder: %%d
    move /y "%%d" "%TEMP_DIR%\" >nul 2>&1
)

REM Move temp directory to Recycle Bin
echo [========================      ] 75%% Moving to Recycle Bin...
powershell -Command "Add-Type -AssemblyName Microsoft.VisualBasic; [Microsoft.VisualBasic.FileIO.FileSystem]::DeleteDirectory('%TEMP_DIR%', 'OnlyErrorDialogs', 'SendToRecycleBin')" 2>nul

REM Clean up temp directory if still exists
if exist "%TEMP_DIR%" rd /s /q "%TEMP_DIR%"

REM Clean up VBScript
if exist "%VBS_SCRIPT%" del /f /q "%VBS_SCRIPT%"

echo [============================] 100%% Complete!

echo.
echo ============================================
echo Cleanup completed!
echo ============================================
echo.
echo All files and folders have been moved to Recycle Bin.
echo You can restore them from Recycle Bin if needed.
echo.
echo Remaining folders:
dir /b /ad
echo.
echo Remaining files:
dir /b /a-d 2>nul
if errorlevel 1 (
    echo (No files remaining)
)
echo.
pause