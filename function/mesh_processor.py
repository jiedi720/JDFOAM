"""网格处理核心模块"""
import os
import subprocess
from .msh_parser import get_boundary_names_from_msh
from .path_utils import to_wsl_path
from .boundary_modifier import generate_boundary_sed_commands


def update_mesh_and_bc(msh_file, case_dir, logger=print, env_source=None):
    """
    更新网格和边界条件
    
    Args:
        msh_file: MSH 文件路径
        case_dir: 算例目录路径
        logger: 日志输出函数，默认为 print
        env_source: OpenFOAM 环境源路径，默认为 "source /usr/lib/openfoam/openfoam2506/etc/bashrc"
        
    Returns:
        bool: 处理是否成功
    """
    wsl_msh = to_wsl_path(msh_file)
    wsl_case = to_wsl_path(case_dir)
    if env_source is None:
        env_source = "source /usr/lib/openfoam/openfoam2506/etc/bashrc"
    
    # 获取边界名并生成 sed 命令
    boundary_names = get_boundary_names_from_msh(msh_file)
    logger(f">>> MSH 解析成功，包含边界: {', '.join(boundary_names)}")

    sed_commands = generate_boundary_sed_commands(boundary_names)

    commands = [
        f"cd \"{wsl_case}\"",
        f"cp -fv \"{wsl_msh}\" .",
        "if [ -f 'system/controlDict' ]; then sed -i 's/writeControl    adjustable;/writeControl    adjustableRunTime;/g' system/controlDict; fi",
        f"gmshToFoam \"{os.path.basename(msh_file)}\" || exit 1",
        "rm -f constant/polyMesh/cellZones constant/polyMesh/faceZones constant/polyMesh/pointZones",
        "transformPoints -scale '(0.001 0.001 0.001)'",
        # 将动态生成的多个 sed 命令合并执行
        "if [ -f 'constant/polyMesh/boundary' ]; then " + " && ".join(sed_commands) + "; fi",
        "checkMesh"
    ]

    full_cmd = f"wsl bash -c \"{env_source} && {' && '.join(commands)}\""
    
    process = subprocess.Popen(full_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for line in process.stdout:
        logger(line.strip())
    process.wait()
    
    return process.returncode == 0