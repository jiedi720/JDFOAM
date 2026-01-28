# -*- mode: python ; coding: utf-8 -*-
import os

# 获取当前目录的绝对路径
current_dir = os.path.dirname(os.path.abspath(SPEC))

# 图标文件的完整路径
ICON_PATH = os.path.join(current_dir, 'icons', 'JDFOAM.png')

a = Analysis(
    ['JDFOAM.py'],
    pathex=[],
    binaries=[],
    datas=[
        # 包含资源文件
        ('function', 'function'),  # 包含整个 function 目录
        ('gui', 'gui'),            # 包含整个 gui 目录
        ('icons', 'icons'),  # 包含整个 resources 目录
    ],
    hiddenimports=[
        # PySide6 相关的隐式导入
        'PySide6.QtCore',
        'PySide6.QtGui',
        'PySide6.QtWidgets',
        # Windows 相关
        'win32com.client',
        'winreg',
        # 项目模块
        'function.Gmsh2OpenFOAM',
        'function.config',
        'function.SourceCodeBinder',
        'function.md2pdf',
        'gui.qt_gui',
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
        'PySide6.Qt3DAnimation',
        'PySide6.Qt3DCore',
        'PySide6.Qt3DExtras',
        'PySide6.Qt3DInput',
        'PySide6.Qt3DLogic',
        'PySide6.Qt3DRender',
        'PySide6.QtCharts',
        'PySide6.QtConcurrent',
        'PySide6.QtDataVisualization',
        'PySide6.QtDesigner',
        'PySide6.QtHelp',
        'PySide6.QtLocation',
        'PySide6.QtMultimedia',
        'PySide6.QtMultimediaWidgets',
        'PySide6.QtNetwork',
        'PySide6.QtNetworkAuth',
        'PySide6.QtNfc',
        'PySide6.QtOpenGL',
        'PySide6.QtOpenGLWidgets',
        'PySide6.QtPdf',
        'PySide6.QtPdfWidgets',
        'PySide6.QtPositioning',
        'PySide6.QtPrintSupport',
        'PySide6.QtQml',
        'PySide6.QtQuick',
        'PySide6.QtQuick3D',
        'PySide6.QtQuickControls2',
        'PySide6.QtQuickWidgets',
        'PySide6.QtRemoteObjects',
        'PySide6.QtScxml',
        'PySide6.QtSensors',
        'PySide6.QtSerialPort',
        'PySide6.QtSql',
        'PySide6.QtStateMachine',
        'PySide6.QtSvg',
        'PySide6.QtSvgWidgets',
        'PySide6.QtTest',
        'PySide6.QtTextToSpeech',
        'PySide6.QtUiTools',
        'PySide6.QtWebChannel',
        'PySide6.QtWebEngine',
        'PySide6.QtWebEngineCore',
        'PySide6.QtWebEngineQuick',
        'PySide6.QtWebEngineWidgets',
        'PySide6.QtWebSockets',
        'PySide6.QtXml',
        'PySide6.QtXmlPatterns',
    ],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='JDFOAM',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=ICON_PATH,
)

coll = COLLECT(
    exe,                # 包含之前定义的 EXE 对象（主程序）
    a.binaries,         # 收集所有依赖的 DLL/动态库
    a.datas,            # 收集所有的资源文件（图片、配置等）
    strip=False,        # 是否移除符号表（通常选 False 以防报错）
    upx=True,           # 是否使用 UPX 压缩混淆
    upx_exclude=[],     # 排除不压缩的文件
    name='JDFOAM',      # 最终生成的文件夹名称
)
