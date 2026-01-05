"""JDFOAM 主入口"""
import os
import sys

# 确保当前目录被识别，解决多文件调用的导入问题
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from function.mesh_processor import update_mesh_and_bc


if __name__ == "__main__":
    if len(sys.argv) >= 3:
        update_mesh_and_bc(sys.argv[1], sys.argv[2])
    else:
        from gui.main_window_gui import run_pyside6_gui
        run_pyside6_gui(update_func=update_mesh_and_bc)