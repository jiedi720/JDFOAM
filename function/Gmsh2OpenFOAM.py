"""GMSH 到 OpenFOAM 网格转换模块

该模块提供完整的 GMSH 网格到 OpenFOAM 格式的转换功能，包括：
- MSH 文件解析和边界名称提取
- Windows 路径到 WSL 路径的转换
- 边界类型自动识别和修改
- 网格转换和边界条件更新的完整流程
- 支持进度回调和日志输出
"""

"""MSH 文件解析模块

提供对 GMSH 生成的 .msh 文件的解析功能，提取其中的物理边界名称，
用于后续的边界条件设置和类型修改。
"""

import os
import re

def get_boundary_names_from_msh(msh_file):
    """
    解析 .msh 文件以提取 PhysicalNames。
    返回边界名称列表，如 ['walls', 'inlet', 'outlet', 'atmosphere']。

    Args:
        msh_file (str): MSH 文件路径

    Returns:
        list: 边界名称列表
    """
    names = []
    if not os.path.exists(msh_file):
        print(f"错误: MSH 文件不存在 - {msh_file}")
        return names

    try:
        with open(msh_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            # 匹配 $PhysicalNames ... $EndPhysicalNames 之间的块
            block = re.search(r'\$PhysicalNames(.*?)\$EndPhysicalNames', content, re.DOTALL)
            if block:
                # 在块中查找双引号内的所有边界名称
                names = re.findall(r'"([^"]+)"', block.group(1))
            else:
                print(f"警告: 未在 {msh_file} 中找到 $PhysicalNames 块")
    except Exception as e:
        print(f"解析 MSH 失败: {e}")
    return names


"""路径转换工具模块

提供 Windows 路径到 WSL (Windows Subsystem for Linux) 路径的转换功能，
确保在 Windows 环境下调用 Linux 工具时路径的正确性。
"""


def to_wsl_path(win_path):
    """
    将 Windows 路径转换为 WSL 路径

    Args:
        win_path (str): Windows 路径

    Returns:
        str: WSL 路径
    """
    path = win_path.replace('\\', '/')
    if ':' in path:
        drive, rest = path.split(':', 1)
        # 确保路径中的空格被正确处理
        return f"/mnt/{drive.lower()}{rest}"
    return path


"""边界类型修改模块

根据边界名称自动识别边界类型，生成相应的 sed 命令来修改 OpenFOAM 的边界条件。
例如，包含 'wall' 的边界名称会被设置为 wall 类型，其他边界保持 patch 类型。
"""


def generate_boundary_sed_commands(boundary_names):
    """
    根据边界名称生成 sed 命令，用于修改边界类型

    Args:
        boundary_names (list): 边界名称列表

    Returns:
        list: sed 命令列表
    """
    sed_commands = []
    for name in boundary_names:
        # 根据名称决定 type。如果名字含 'wall'，则 type 改为 wall，否则保持 patch
        target_type = "wall" if "wall" in name.lower() else "patch"

        # 精准匹配：只替换该边界名对应花括号区块内的 type
        sed_cmd = f"sed -i '/{name}/,/}}/ s/type[[:space:]]\\+patch;/type            {target_type};/' constant/polyMesh/boundary"
        sed_commands.append(sed_cmd)

    # 兜底处理 defaultFaces
    sed_commands.append("sed -i '/defaultFaces/,/}/ s/type[[:space:]]\\+patch;/type            wall;/' constant/polyMesh/boundary")

    return sed_commands


"""网格处理核心模块

提供完整的网格转换和边界条件更新功能，包括：
- 调用 gmshToFoam 工具进行网格转换
- 自动缩放网格单位（从毫米到米）
- 根据边界名称修改边界类型
- 执行网格质量检查
"""

import subprocess


def update_mesh_and_bc(msh_file, case_dir, logger=print, env_source=None, progress_callback=None):
    """
    更新网格和边界条件

    该函数执行完整的 GMSH 到 OpenFOAM 网格转换流程，包括：
    1. 解析 MSH 文件获取边界名称
    2. 将网格文件复制到算例目录
    3. 调用 gmshToFoam 进行格式转换
    4. 缩放网格单位（从毫米到米）
    5. 根据边界名称修改边界类型
    6. 执行网格质量检查

    Args:
        msh_file (str): MSH 文件路径
        case_dir (str): OpenFOAM 算例目录路径
        logger (callable): 日志输出函数，默认为 print
        env_source (str): OpenFOAM 环境源路径
        progress_callback (callable): 进度回调函数，接收0-100的进度值

    Returns:
        bool: 处理是否成功
    """
    wsl_msh = to_wsl_path(msh_file)
    wsl_case = to_wsl_path(case_dir)
    if env_source is None:
        env_source = "source /usr/lib/openfoam/openfoam2506/etc/bashrc"

    # 更新进度：开始处理
    if progress_callback:
        progress_callback(5)

    # 获取边界名并生成 sed 命令
    boundary_names = get_boundary_names_from_msh(msh_file)
    logger(f">>> MSH 解析成功，包含边界: {', '.join(boundary_names)}")

    # 更新进度：MSH 解析完成
    if progress_callback:
        progress_callback(15)

    sed_commands = generate_boundary_sed_commands(boundary_names)

    # 更新进度：开始执行命令
    if progress_callback:
        progress_callback(15)

    # 定义命令列表和对应的进度值
    commands = [
        (f"cp -fv \"{wsl_msh}\" .", 20),
        ("if [ -f 'system/controlDict' ]; then sed -i 's/writeControl    adjustable;/writeControl    adjustableRunTime;/g' system/controlDict; fi", 25),
        (f"gmshToFoam \"{os.path.basename(msh_file)}\" 2>&1 || exit 1", 50),
        ("rm -f constant/polyMesh/cellZones constant/polyMesh/faceZones constant/polyMesh/pointZones", 60),
        ("transformPoints -scale '(0.001 0.001 0.001)'", 70),
        # 将动态生成的多个 sed 命令合并执行
        ("if [ -f 'constant/polyMesh/boundary' ]; then " + " && ".join(sed_commands) + "; fi", 90),
        ("checkMesh", 95)
    ]

    # 执行命令并更新进度
    for cmd, progress_val in commands:
        # 使用更安全的命令构建方式，确保路径被正确引用
        # 使用双引号包裹 bash -c 的命令，并转义内部的双引号
        escaped_cmd = cmd.replace('"', '\\"')
        full_cmd = f"wsl bash -c \"cd \\\"{wsl_case}\\\" && {env_source} && {escaped_cmd}\""
        process = subprocess.Popen(full_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='replace')
        for line in process.stdout:
            logger(line.strip())
        process.wait()

        # 更新进度
        if progress_callback:
            progress_callback(progress_val)

        # 如果命令执行失败，提前返回
        if process.returncode != 0 and not cmd.startswith("if [ -f"):  # 忽略条件命令的返回值
            return False

    # 最终进度
    if progress_callback:
        progress_callback(100)

    return process.returncode == 0


"""工作线程模块，用于执行耗时操作

提供在后台线程中执行网格转换等耗时操作的功能，避免阻塞 GUI 线程，
同时支持日志输出、进度更新和完成状态通知。
"""

from PySide6.QtCore import QThread, Signal


class WorkerThread(QThread):
    """工作线程，用于执行耗时操作

    该线程类封装了网格转换操作，提供信号机制与主线程通信：
    - log_signal: 发送日志消息
    - progress_signal: 发送进度更新
    - finished_signal: 发送完成状态
    """
    # 定义线程间通信的信号
    log_signal = Signal(str)          # 日志信号，用于发送日志消息
    progress_signal = Signal(int)     # 进度信号，用于发送进度值 (0-100)
    finished_signal = Signal(bool, str)  # 完成信号，发送成功状态和错误信息

    def __init__(self, update_func, msh_path, case_path, env_source=None):
        """
        初始化工作线程

        Args:
            update_func (callable): 网格更新函数
            msh_path (str): MSH 文件路径
            case_path (str): 算例目录路径
            env_source (str): OpenFOAM 环境源路径
        """
        super().__init__()
        self.update_func = update_func  # 网格更新函数
        self.msh_path = msh_path        # MSH 文件路径
        self.case_path = case_path      # 算例目录路径
        self.env_source = env_source    # OpenFOAM 环境源路径

    def run(self):
        """执行线程主任务

        在后台线程中执行网格转换操作，并通过信号与主线程通信
        """
        try:
            # 执行网格更新函数，传入信号发射器作为回调
            success = self.update_func(
                self.msh_path,           # MSH 文件路径
                self.case_path,          # 算例目录路径
                logger=self.log_signal.emit,           # 日志回调
                env_source=self.env_source,            # 环境变量
                progress_callback=self.progress_signal.emit  # 进度回调
            )
            # 发送完成信号，表示操作成功
            self.finished_signal.emit(success, "")
        except Exception as e:
            # 发送完成信号，表示操作失败
            self.finished_signal.emit(False, str(e))