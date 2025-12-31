@echo off
:: 设置编码为 UTF-8
chcp 65001 >nul

:: 强制切换到脚本所在的实际目录
cd /d "%~dp0"

echo ============================================
echo   gmshToFoam 自动化打包程序 (GUI模式)
echo ============================================

:: 1. 环境检查
if not exist "gmshToFoam.py" (
    echo [错误] 找不到主程序文件 gmshToFoam.py！
    pause
    exit
)

:: 检查是否存在 gui 文件夹
if not exist "gui" (
    echo [警告] 找不到 gui 文件夹，界面可能无法正常加载！
)

:: 2. 执行 PyInstaller
:: 真正的代码块作用：
:: --onefile: 打包为单个 exe 文件
:: --windowed: 运行时不显示黑色命令行窗口
:: --add-data "gui;gui": 将 gui 文件夹及其内容打包进 exe
:: --distpath: 指定生成的 exe 存放位置
:: --workpath: 指定编译时的临时文件夹，避免占用 C 盘空间
:: 最后一行指定主入口文件为 gmshToFoam.py
python -m PyInstaller --noconfirm --onefile --windowed ^
--name="gmshToFoam" ^
--icon="C:\Users\EJI1WX\OneDrive - Bosch Group\PythonProject\SourceCodeBinder\resources\gmshToFoam.ico" ^
--add-data "gui;gui" ^
--add-data "C:\Users\EJI1WX\OneDrive - Bosch Group\PythonProject\SourceCodeBinder\resources\gmshToFoam.ico;." ^
--distpath="C:/Users/EJI1WX/OneDrive - Bosch Group/Program" ^
--workpath="C:/Temp_Build" ^
--clean gmshToFoam.py

echo.
echo --------------------------------------------
echo 打包执行完毕！EXE 文件名：gmshToFoam.exe
echo 输出目录: C:/Users/EJI1WX/OneDrive - Bosch Group/Program
echo --------------------------------------------
pause