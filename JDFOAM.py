"""JDFOAM 主入口模块

JDFOAM (JD's OpenFOAM Assistant) 是一个用于 GMSH 网格转换和 OpenFOAM 仿真的 Python 工具。
该模块作为程序的主入口点，支持命令行模式和图形界面模式两种运行方式。

功能特性：
- 支持命令行参数直接执行网格转换
- 提供图形用户界面进行交互式操作
- 集成 GMSH 到 OpenFOAM 的完整工作流程
- 支持源代码文档生成和PDF导出
"""

import os
import sys

# 确保当前目录被识别，解决多文件调用的导入问题
# 将当前目录添加到 Python 模块搜索路径中
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# 导入核心网格转换功能
from function.Gmsh2OpenFOAM import update_mesh_and_bc


if __name__ == "__main__":
    # 检查命令行参数数量
    # 如果提供了至少2个参数（脚本名、MSH文件、算例目录），则执行命令行模式
    if len(sys.argv) >= 3:
        # 执行网格转换和边界条件更新
        # 参数1: MSH文件路径
        # 参数2: OpenFOAM算例目录路径
        update_mesh_and_bc(sys.argv[1], sys.argv[2])
    else:
        # 参数不足，启动图形用户界面模式
        from gui.main_window import run_pyside6_gui
        # 使用网格转换函数初始化GUI
        run_pyside6_gui(update_func=update_mesh_and_bc)