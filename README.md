# JDFOAM

OpenFOAM 网格转换与源码管理工具 - 基于 PySide6 的图形界面应用。

## 功能特性

### 网格转换
- **自动网格转换**: 将 Gmsh 生成的 `.msh` 文件转换为 OpenFOAM 格式
- **智能边界识别**: 自动解析 `.msh` 文件中的物理边界名称
- **边界类型修正**: 根据边界名称自动设置正确的边界类型
  - 包含 "wall" 的边界自动设置为 `wall` 类型
  - 其他边界默认设置为 `patch` 类型
  - `defaultFaces` 自动设置为 `wall` 类型
- **单位转换**: 自动将网格从毫米转换为米 (缩放因子 0.001)
- **WSL 集成**: 通过 Windows Subsystem for Linux (WSL) 运行 OpenFOAM 命令
- **进度反馈**: 实时显示转换进度，任务完成后进度条自动归零

### 源码管理
- **代码扫描**: 自动扫描项目目录中的源代码文件
- **Markdown 合并**: 将多个源文件合并为一个结构化的 Markdown 文档
- **PDF 导出**: 将 Markdown 文档转换为 PDF 格式，支持 GitHub 风格样式
- **进度反馈**: 实时显示扫描和转换进度

### 图形界面
- **现代 UI**: 基于 PySide6 的现代化图形界面
- **主题切换**: 支持 Light/Dark 两种主题模式
- **配置管理**: 使用 INI 文件管理配置，支持持久化
- **TreeFoam 集成**: 一键启动 TreeFoam 工具
- **Gmsh 集成**: 一键启动 Gmsh 网格生成工具
- **WSL 工具集成**: 通过 WSL 菜单快速访问 Nautilus、Baobab、GNOME Tweaks 等工具
- **实时日志**: 显示操作过程中的详细日志信息

## 系统要求

- Windows 10/11
- Python 3.7+
- PySide6
- WSL (Windows Subsystem for Linux) with Ubuntu
- OpenFOAM (推荐 OpenFOAM-2506 或更高版本)
- GmshToFoam 工具 (OpenFOAM 内置)
- wkhtmltopdf (用于 PDF 导出)

## 安装

1. 克隆仓库:
```bash
git clone https://github.com/jiedi720/JDFOAM.git
cd JDFOAM
```

2. 安装依赖:
```bash
pip install -r requirements.txt
```

3. 安装 wkhtmltopdf:
   - 下载并安装 [wkhtmltopdf](https://wkhtmltopdf.org/downloads.html)
   - 配置路径到 `JDFOAM.ini` 文件

4. 确保 WSL 和 OpenFOAM 已安装:
```bash
# 在 WSL 中检查 OpenFOAM 是否可用
wsl bash -c "source /usr/lib/openfoam/openfoam2506/etc/bashrc && gmshToFoam -help"
```

## 使用方法

### 图形界面模式

直接运行主程序:
```bash
python JDFOAM.py
```

### 网格转换操作步骤:

1. 选择算例项目根目录
2. 选择待转换的 `.msh` 文件
3. 点击"开始转换网格"按钮
4. 查看日志输出确认转换结果

### 源码管理操作步骤:

1. 选择算例项目根目录
2. 点击"合并代码为Markdown"按钮
3. 等待代码扫描和合并完成
4. 点击"导出代码为PDF"按钮生成 PDF 文档

### 配置说明

编辑 `JDFOAM.ini` 文件配置以下选项:

```ini
[General]
# Gmsh 可执行文件路径（支持多个路径）
gmsh_path = D:/gmsh-4.15.0-Windows64/gmsh.exe
gmsh_path_2 = C:/gmsh-4.15.0-Windows64/gmsh.exe

# TreeFoam 启动命令
treefoam_command = "C:\Program Files\WSL\wslg.exe" -d DEXCS2025 -u jiedi -- bash -l -c "/usr/local/bin/start_treefoam.sh"

# wkhtmltopdf 可执行文件路径
wkhtmltopdf_path = C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe

# OpenFOAM 环境变量源文件
openfoam_env_source = source /usr/lib/openfoam/openfoam2506/etc/bashrc

# 界面主题 (light/dark)
theme = dark

# WSL 命令配置
wsl_files_command = "C:\Program Files\WSL\wslg.exe" -d DEXCS2025 --cd "~" -- nautilus --new-window
wsl_disk_analysis_command = "C:\Program Files\WSL\wslg.exe" -d DEXCS2025 --cd "~" -- baobab
wsl_appearance_command = "C:\Program Files\WSL\wslg.exe" -d DEXCS2025 --cd "~" -- gnome-tweaks
wsl_bashrc_path = Z:\home\jiedi\.bashrc
```

## 工作流程

### 网格转换流程

1. **解析 MSH 文件**: 提取物理边界名称
2. **复制文件**: 将 `.msh` 文件复制到算例目录
3. **网格转换**: 使用 `gmshToFoam` 转换网格格式
4. **清理区域**: 删除不需要的 cellZones、faceZones、pointZones
5. **单位转换**: 使用 `transformPoints` 缩放网格 (mm → m)
6. **边界修正**: 使用 `sed` 自动修正边界类型
7. **网格检查**: 运行 `checkMesh` 验证网格质量

### 源码管理流程

1. **目录扫描**: 递归扫描项目目录，过滤二进制文件和排除目录
2. **文件读取**: 读取所有支持的源代码文件
3. **Markdown 生成**: 生成包含目录、文件路径、代码内容的 Markdown 文档
4. **PDF 转换**: 使用 wkhtmltopdf 将 Markdown 转换为 PDF

## 边界命名规则

程序根据边界名称自动判断边界类型:

| 边界名称包含 | OpenFOAM 类型 |
|------------|--------------|
| `wall` (不区分大小写) | `wall` |
| 其他名称 | `patch` |
| `defaultFaces` | `wall` |

示例:
- `walls`, `WALL`, `Wall` → `wall`
- `inlet`, `outlet`, `atmosphere` → `patch`

## 支持的文件类型

源码扫描支持以下文件扩展名:

- **编程语言**: `.py`, `.js`, `.ts`, `.jsx`, `.tsx`, `.vue`, `.html`, `.css`, `.c`, `.cpp`, `.h`, `.java`, `.go`, `.rs`, `.swift`, `.kt`, `.php`, `.rb`, `.lua`, `.dart`, `.scala`
- **脚本语言**: `.sh`, `.bash`, `.ps1`, `.bat`, `.cmd`, `.pl`, `.r`
- **配置文件**: `.json`, `.xml`, `.yaml`, `.yml`, `.toml`, `.ini`, `.cfg`, `.conf`
- **文档文件**: `.md`, `.txt`, `.rst`, `.tex`

## 默认排除目录

以下目录会被自动排除:
- `.git`, `.idea`, `.vscode`
- `node_modules`, `venv`, `env`, `__pycache__`
- `dist`, `build`, `.pytest_cache`, `.mypy_cache`
- `htmlcov`, `.tox`, `site-packages`, `egg-info`

## 常见问题

### WSL 命令执行失败
- 确保 WSL 已正确安装并配置
- 检查 OpenFOAM 环境变量路径是否正确
- 确认 WSL 中的 OpenFOAM 版本与配置一致

### 网格转换失败
- 检查 `.msh` 文件格式是否正确
- 确认 `.msh` 文件包含 `$PhysicalNames` 块
- 查看日志输出获取详细错误信息

### 边界类型未正确修正
- 检查边界名称是否符合命名规则
- 确认 `constant/polyMesh/boundary` 文件存在
- 验证 `sed` 命令在 WSL 中可用

### PDF 导出失败
- 确认 wkhtmltopdf 已正确安装
- 检查 `JDFOAM.ini` 中的 `wkhtmltopdf_path` 配置
- 确保已先执行"合并代码为Markdown"操作

## 打包为可执行文件

### 打包步骤

1. 确保已安装 PyInstaller:
```bash
pip install pyinstaller
```

2. 运行打包脚本:
```bash
build_exe.bat
```

3. 打包完成后，可执行文件位于:
```
./JDFOAM/JDFOAM.exe
```

### 打包说明

- 使用目录模式 (-D)，所有依赖文件在同一文件夹中
- 输出目录: `./JDFOAM/`
- 打包时会自动包含 `function/`、`gui/` 和 `icons/` 目录
- 图标路径已修复为绝对路径，确保在打包后按钮图标能正常显示

### 图标修复

程序已修复按钮图标路径问题，使用绝对路径加载图标，确保在开发环境和打包后的 EXE 中都能正确显示所有按钮图标。

## 项目结构

```
JDFOAM/
├── JDFOAM.py              # 主程序入口
├── JDFOAM.ini             # 配置文件 (打包后自动生成)
├── JDFOAM.spec            # PyInstaller 配置文件
├── build_exe.bat          # 打包脚本
├── README.md              # 项目文档
├── requirements.txt       # 依赖包列表
├── function/              # 功能模块
│   ├── __init__.py
│   ├── Gmsh2OpenFOAM.py   # GMSH 到 OpenFOAM 转换核心模块 (包含 WorkerThread)
│   ├── config.py          # 配置管理
│   ├── SourceCodeBinder.py # 源码扫描与合并模块
│   └── md2pdf.py          # Markdown 到 PDF 转换模块
├── gui/                   # 图形界面
│   ├── __init__.py
│   ├── main_window.py     # 主窗口 (包含图标路径修复逻辑)
│   ├── progressbar.py     # 进度条管理
│   ├── theme.py           # 主题管理
│   └── ui_JDFOAM.py       # UI 定义
└── icons/                 # 资源文件
    ├── JDFOAM.png         # 应用图标 (PNG 格式)
    ├── gmsh.ico           # Gmsh 图标
    ├── search.png         # 搜索图标
    ├── open-folder.png    # 打开文件夹图标
    └── TreeFoam.png       # TreeFoam 图标
```

## 开发说明

### 修改 OpenFOAM 版本

在 `JDFOAM.ini` 中修改:
```ini
openfoam_env_source = source /usr/lib/openfoam/openfoam2506/etc/bashrc
```

将 `openfoam2506` 替换为您的 OpenFOAM 版本。

### 修改缩放因子

在 `function/Gmsh2OpenFOAM.py` 中修改 `transformPoints` 命令:
```python
"transformPoints -scale '(0.001 0.001 0.001)'"
```

### 添加新的文件扩展名支持

在 `function/SourceCodeBinder.py` 的 `include_extensions` 字典中添加:
```python
include_extensions = {
    # ... 现有扩展名 ...
    '.xyz': 'xyz',
}
```

## 许可证

本项目采用 MIT 许可证。

## 贡献

欢迎提交 Issue 和 Pull Request。

## 联系方式

- GitHub: https://github.com/jiedi720/JDFOAM