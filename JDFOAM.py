import os
import subprocess
import sys
import re

# 真正的代码块作用：确保当前目录被识别，解决多文件调用的导入问题
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

def get_boundary_names_from_msh(msh_file):
    """
    真正的代码块作用：
    解析 .msh 文件以提取 PhysicalNames。
    它会返回如 ['walls', 'inlet', 'outlet', 'atmosphere'] 的列表。
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

def update_mesh_and_bc(msh_file, case_dir, logger=print):
    def to_wsl_path(win_path):
        path = win_path.replace('\\', '/')
        if ':' in path:
            drive, rest = path.split(':', 1)
            return f"/mnt/{drive.lower()}{rest}"
        return path

    wsl_msh = to_wsl_path(msh_file)
    wsl_case = to_wsl_path(case_dir)
    env_source = "source /usr/lib/openfoam/openfoam2506/etc/bashrc"
    
    # 获取边界名并生成 sed 命令
    boundary_names = get_boundary_names_from_msh(msh_file)
    logger(f">>> MSH 解析成功，包含边界: {', '.join(boundary_names)}")

    sed_commands = []
    for name in boundary_names:
        # 真正的代码块作用：
        # 根据名称决定 type。如果名字含 'wall'，则 type 改为 wall，否则保持 patch。
        target_type = "wall" if "wall" in name.lower() else "patch"
        
        # 精准匹配：只替换该边界名对应花括号区块内的 type
        sed_cmd = f"sed -i '/{name}/,/}}/ s/type[[:space:]]\\+patch;/type            {target_type};/' constant/polyMesh/boundary"
        sed_commands.append(sed_cmd)

    # 兜底处理 defaultFaces
    sed_commands.append("sed -i '/defaultFaces/,/}/ s/type[[:space:]]\\+patch;/type            wall;/' constant/polyMesh/boundary")

    commands = [
        f"cd \"{wsl_case}\"",
        f"cp -fv \"{wsl_msh}\" .",
        "if [ -f 'system/controlDict' ]; then sed -i 's/writeControl    adjustable;/writeControl    adjustableRunTime;/g' system/controlDict; fi",
        f"gmshToFoam \"{os.path.basename(msh_file)}\" || exit 1",
        "rm -f constant/polyMesh/cellZones constant/polyMesh/faceZones constant/polyMesh/pointZones",
        "transformPoints -scale '(0.001 0.001 0.001)'",
        # 真正的代码块作用：将动态生成的多个 sed 命令合并执行
        "if [ -f 'constant/polyMesh/boundary' ]; then " + " && ".join(sed_commands) + "; fi",
        "checkMesh"
    ]

    full_cmd = f"wsl bash -c \"{env_source} && {' && '.join(commands)}\""
    
    process = subprocess.Popen(full_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for line in process.stdout:
        logger(line.strip())
    process.wait()
    
    return process.returncode == 0

if __name__ == "__main__":
    if len(sys.argv) >= 3:
        update_mesh_and_bc(sys.argv[1], sys.argv[2])
    else:
        from gui.pyqt5_gui import run_pyqt5_gui
        run_pyqt5_gui(update_func=update_mesh_and_bc)