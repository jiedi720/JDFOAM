# -*- mode: python ; coding: utf-8 -*-

# JDFOAM PyInstaller 配置文件
# 用于将 Python 项目打包为 Windows 可执行文件

import os
import sys

# 获取当前目录
current_dir = os.path.dirname(os.path.abspath(SPEC))

block_cipher = None

a = Analysis(
    ['JDFOAM.py'],  # 主程序入口文件
    pathex=[current_dir],  # 搜索路径
    binaries=[],
    datas=[
        # 包含资源文件
        ('resources', 'resources'),  # 包含整个 resources 目录
        ('JDFOAM.ini', '.'),  # 包含配置文件
    ],
    hiddenimports=[
        # PySide6 相关的隐式导入
        'PySide6.QtCore',
        'PySide6.QtGui',
        'PySide6.QtWidgets',
        'PySide6.QtSvg',
        # 项目模块
        'function.mesh_processor',
        'function.msh_parser',
        'function.boundary_modifier',
        'function.path_utils',
        'function.config',
        'function.combine',
        'function.pdf',
        'function.worker_thread',
        'gui.main_window_gui',
        'gui.theme_gui',
        'gui.ui_JDFOAM',
        'gui.worker_thread_gui',
        # pdfkit 相关
        'pdfkit',
        'pdfkit.configuration',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # 排除不需要的模块以减小体积
        'tkinter',
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'IPython',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='JDFOAM',  # 生成的可执行文件名称
    debug=False,  # 不生成调试信息
    bootloader_ignore_signals=False,
    strip=False,  # 不剥离符号表
    upx=True,  # 使用 UPX 压缩
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # 不显示控制台窗口（GUI 模式）
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='resources/JDFOAM.ico',  # 应用图标
)

# 注意事项：
# 1. 打包前请确保已安装所有依赖: pip install -r requirements.txt
# 2. 打包命令: pyinstaller JDFOAM.spec
# 3. 或使用批处理脚本: build_exe.bat
# 4. 打包后的可执行文件在当前目录的 dist 文件夹中
# 5. 首次运行时会在程序目录生成 JDFOAM.ini 配置文件
# 6. wkhtmltopdf 需要单独安装并配置路径
# 7. WSL 和 OpenFOAM 需要在系统中预装配置