# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['JDFOAM.py'],
    pathex=[],
    binaries=[],
    datas=[
        # 包含资源文件
        ('resources', 'resources'),  # 包含整个 resources 目录
    ],
    hiddenimports=[
        # PySide6 相关的隐式导入
        'PySide6.QtCore',
        'PySide6.QtGui',
        'PySide6.QtWidgets',
        'PySide6.QtSvg',
        # 项目模块
        'function.Gmsh2OpenFOAM',
        'function.config',
        'function.SourceCodeBinder',
        'function.md2pdf',
        'gui.main_window',
        'gui.theme',
        'gui.ui_JDFOAM',
        'gui.progressbar',
        # pdfkit 相关
        'pdfkit',
        'pdfkit.configuration',
        'markdown2',
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
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='JDFOAM',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='resources\\JDFOAM.ico',
)
