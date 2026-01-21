"""主窗口模块

该模块实现 JDFOAM 应用程序的主界面，提供：
- GMSH 网格到 OpenFOAM 的转换功能
- 源代码合并为 Markdown 功能
- Markdown 转 PDF 功能
- 主题切换功能
- 日志输出和进度显示
"""

import os
import subprocess
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QPlainTextEdit, QFileDialog,
                             QGroupBox, QProgressBar, QMessageBox, QMenu)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QFont, QAction
from function.Gmsh2OpenFOAM import WorkerThread
from function.config import ConfigManager
from .theme import ThemeManager
from .progressbar import ProgressBarManager
from .ui_JDFOAM import Ui_JDFOAM_GUI
from function.SourceCodeBinder import scan_directory, combine_files_to_markdown
from function.md2pdf import markdown_to_pdf


class PySide6GmshConverterGUI(QMainWindow, Ui_JDFOAM_GUI):
    """PySide6 GUI 主窗口

    实现 JDFOAM 应用程序的主界面，集成所有功能模块，
    提供用户友好的图形界面进行 GMSH 网格转换和源代码管理。
    """

    def __init__(self, update_func, app_icon_path=None):
        """
        初始化主窗口

        Args:
            update_func: 网格更新函数，用于执行 GMSH 到 OpenFOAM 的转换
            app_icon_path: 应用程序图标文件路径（可选）
        """
        super().__init__()
        self.update_func = update_func          # 网格更新函数
        self.worker_thread = None               # 工作线程对象
        self.config_manager = ConfigManager()   # 配置管理器
        self.theme_manager = ThemeManager(self) # 主题管理器
        self.progressbar_manager = ProgressBarManager(self)  # 进度条管理器
        self.app_icon_path = app_icon_path      # 应用程序图标路径

        # 设置 UI
        self.setupUi(self)

        # 修复按钮图标路径（使用绝对路径）
        self.fix_button_icons()

        # 设置窗口图标
        self.set_window_icon()

        # 验证 UI 控件是否正确创建
        if not hasattr(self, 'Log'):
            print("警告: Log 未创建")
        if not hasattr(self, 'case_path_edit'):
            print("警告: case_path_edit 未创建")
        if not hasattr(self, 'progress_bar'):
            print("警告: progress_bar 未创建")

        # 初始化进度条
        self.progressbar_manager.init_progress_bar()
        # 初始时显示进度条，值为0
        self.progressbar_manager.show_progress_bar()

        # 连接信号
        self.connect_signals()

        # 初始化配置和主题
        self.config_manager.load_config()

        # 从配置文件加载路径
        saved_case_path = self.config_manager.get_case_path()
        if saved_case_path:
            self.case_path_edit.setText(saved_case_path)

        saved_msh_path = self.config_manager.get_msh_path()
        if saved_msh_path:
            self.msh_path_edit.setText(saved_msh_path)

        # 从配置文件加载主题
        saved_theme = self.config_manager.get_theme()
        self.theme_manager.current_theme = saved_theme

        # 初始化主题菜单
        self.theme_manager.init_menu()

        # 应用主题
        self.theme_manager.apply_theme(saved_theme)

        # 为日志框设置上下文菜单
        self.Log.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.Log.customContextMenuRequested.connect(self.show_log_context_menu)
    
    def closeEvent(self, event):
        """
        窗口关闭事件处理

        在窗口关闭时保存当前主题设置到配置文件

        Args:
            event: 关闭事件对象
        """
        self.config_manager.set_theme(self.theme_manager.current_theme)
        super().closeEvent(event)

    def fix_button_icons(self):
        """修复按钮图标路径

        将按钮的图标路径从相对路径改为绝对路径，确保在打包后能正确加载
        """
        # 获取 icons 目录的绝对路径
        icons_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "icons")

        # 定义按钮和对应的图标文件名
        button_icons = {
            'case_browse_btn': 'search.png',
            'case_open_btn': 'open-folder.png',
            'treefoam_btn': 'TreeFoam.png',
            'msh_browse_btn': 'search.png',
            'msh_open_btn': 'open-folder.png',
            'gmsh_btn': 'gmsh.ico',
        }

        # 为每个按钮设置正确的图标
        for button_name, icon_file in button_icons.items():
            if hasattr(self, button_name):
                button = getattr(self, button_name)
                icon_path = os.path.join(icons_path, icon_file)
                if os.path.exists(icon_path):
                    button.setIcon(QIcon(icon_path))
                    print(f"按钮图标已设置: {button_name} -> {icon_path}")
                else:
                    print(f"警告: 图标文件不存在: {icon_path}")

    def set_window_icon(self):
        """设置窗口图标

        从传入的路径或 icons 目录加载并设置应用程序图标
        """
        # 优先使用传入的图标路径
        if self.app_icon_path and os.path.exists(self.app_icon_path):
            window_icon_path = self.app_icon_path
        else:
            # 获取 icons 目录的绝对路径
            icons_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "icons")
            # 尝试查找 JDFOAM.png
            window_icon_path = os.path.join(icons_path, "JDFOAM.png")

        # 设置窗口图标
        if os.path.exists(window_icon_path):
            self.setWindowIcon(QIcon(window_icon_path))
            print(f"窗口图标已设置: {window_icon_path}")
        else:
            print(f"警告: 窗口图标文件不存在: {window_icon_path}")

    def connect_signals(self):
        """连接所有信号和槽

        将界面控件的信号连接到相应的处理方法
        """
        # 路径选择按钮
        self.case_browse_btn.clicked.connect(self.select_case)
        self.case_open_btn.clicked.connect(self.open_case_dir)
        self.msh_browse_btn.clicked.connect(self.select_msh)
        self.msh_open_btn.clicked.connect(self.open_msh_dir)

        # 工具按钮
        self.treefoam_btn.clicked.connect(self.run_treefoam)
        self.gmsh_btn.clicked.connect(self.open_gmsh)

        # 操作按钮
        self.start_mesh_btn.clicked.connect(self.start)
        self.combine_md_btn.clicked.connect(self.combine_to_markdown)
        self.combine_pdf_btn.clicked.connect(self.export_to_pdf)

        # WSL 菜单操作
        self.actionNautilus.triggered.connect(self.run_wsl_nautilus)
        self.actionBaobab.triggered.connect(self.run_wsl_baobab)
        self.actionGnome_tweaks.triggered.connect(self.run_wsl_gnome_tweaks)
        self.action_bashrc.triggered.connect(self.open_wsl_bashrc)

        # checkMesh 菜单操作
        self.actioncheckMesh.triggered.connect(self.check_mesh)

    def select_msh(self):
        """选择 MSH 文件

        打开文件对话框让用户选择 GMSH 生成的 .msh 文件
        """
        current_path = self.msh_path_edit.text()
        if current_path and os.path.isdir(current_path):
            start_dir = current_path
        else:
            start_dir = ""

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择MSH文件",
            start_dir,
            "Gmsh Files (*.msh);;All Files (*.*)"
        )
        if file_path:
            self.msh_path_edit.setText(file_path)

    def select_case(self):
        """选择算例目录

        打开目录对话框让用户选择 OpenFOAM 算例目录
        """
        current_path = self.case_path_edit.text()
        if current_path and os.path.isdir(current_path):
            start_dir = current_path
        else:
            start_dir = ""

        dir_path = QFileDialog.getExistingDirectory(
            self,
            "选择算例目录",
            start_dir
        )
        if dir_path:
            self.case_path_edit.setText(dir_path)
            self.config_manager.set_case_path(dir_path)

    def open_case_dir(self):
        """打开算例目录

        使用系统默认文件管理器打开指定的算例目录
        """
        dir_path = self.case_path_edit.text()
        if dir_path and os.path.isdir(dir_path):
            os.startfile(dir_path)
        else:
            QMessageBox.warning(self, "提示", "请先选择有效的算例目录")

    def open_msh_dir(self):
        """打开 MSH 文件所在目录

        使用系统默认文件管理器打开 MSH 文件所在的目录
        """
        msh_path = self.msh_path_edit.text()
        if msh_path and os.path.isfile(msh_path):
            dir_path = os.path.dirname(msh_path)
            os.startfile(dir_path)
        else:
            QMessageBox.warning(self, "提示", "请先选择有效的MSH文件")

    def show_log_context_menu(self, pos):
        """显示日志框的右键菜单

        在日志框上右键点击时显示上下文菜单，包含复制、粘贴、全选、清除日志和保存日志选项

        Args:
            pos: 鼠标点击位置
        """
        menu = QMenu(self)

        # 设置菜单样式，确保分隔线在 Dark 模式下可见
        if self.theme_manager.current_theme == "dark":
            menu.setStyleSheet("""
QMenu {
    background-color: #3D3D3D;
    color: white;
    border: 1px solid #555555;
}
QMenu::separator {
    height: 2px;
    background-color: #555555;
    margin: 4px 8px;
}
QMenu::item {
    padding: 5px 30px 5px 20px;
}
QMenu::item:selected {
    background-color: #42A5F5;
}
""")
        else:
            menu.setStyleSheet("""
QMenu::separator {
    height: 2px;
    background-color: #BDBDBD;
    margin: 4px 8px;
}
""")

        # 复制选项
        copy_action = QAction("复制", self)
        copy_action.triggered.connect(self.Log.copy)
        menu.addAction(copy_action)

        # 粘贴选项
        paste_action = QAction("粘贴", self)
        paste_action.triggered.connect(self.Log.paste)
        menu.addAction(paste_action)

        # 全选选项
        select_all_action = QAction("全选", self)
        select_all_action.triggered.connect(self.Log.selectAll)
        menu.addAction(select_all_action)

        # 添加分隔线
        menu.addSeparator()

        # 清除日志选项
        clear_action = QAction("清除", self)
        clear_action.triggered.connect(self.clear_log)
        menu.addAction(clear_action)

        # 添加分隔线
        menu.addSeparator()

        # 保存日志选项
        save_action = QAction("保存日志", self)
        save_action.triggered.connect(self.save_log_to_file)
        menu.addAction(save_action)

        # 在鼠标位置显示菜单
        menu.exec(self.Log.mapToGlobal(pos))

    def clear_log(self):
        """清除日志框内容"""
        self.Log.clear()

    def save_log_to_file(self):
        """保存日志内容到文件"""
        log_content = self.Log.toPlainText()

        if not log_content:
            QMessageBox.information(self, "提示", "日志内容为空，无需保存")
            return

        # 获取算例目录作为默认保存路径
        default_dir = self.case_path_edit.text()
        if not default_dir or not os.path.isdir(default_dir):
            default_dir = ""

        # 生成默认文件名
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"JDFOAM_log_{timestamp}.txt"

        # 打开保存文件对话框
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "保存日志",
            os.path.join(default_dir, default_filename),
            "文本文件 (*.txt);;所有文件 (*.*)"
        )

        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(log_content)
                QMessageBox.information(self, "完成", f"日志已保存到:\n{file_path}")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"保存日志失败:\n{str(e)}")

    def run_treefoam(self):
        """运行 TreeFOAM 命令

        执行 TreeFOAM 命令来显示算例目录的文件结构
        """
        try:
            treefoam_cmd = self.config_manager.get_treefoam_command()
            if not treefoam_cmd:
                QMessageBox.warning(self, "提示", "TreeFOAM 命令未配置，请检查配置文件")
                return

            case_path = self.case_path_edit.text()
            if case_path and os.path.isdir(case_path):
                self.log_msg(f"运行 TreeFOAM: {case_path}")

            subprocess.Popen(treefoam_cmd, shell=True)

        except Exception as e:
            QMessageBox.critical(self, "错误", f"运行 TreeFOAM 失败: {str(e)}")

    def open_gmsh(self):
        """打开 Gmsh 程序

        启动 Gmsh 前处理软件，支持自动查找和手动选择
        """
        try:
            gmsh_exe = self.config_manager.get_gmsh_path()

            if not gmsh_exe or not os.path.exists(gmsh_exe):
                possible_paths = [
                    r"D:\gmsh-4.15.0-Windows64\gmsh.exe",
                    r"C:\gmsh-4.15.0-Windows64\gmsh.exe",
                    r"C:\Program Files\gmsh\gmsh.exe",
                    r"C:\Program Files (x86)\gmsh\gmsh.exe",
                    r"C:\gmsh\gmsh.exe"
                ]
                for path in possible_paths:
                    if os.path.exists(path):
                        gmsh_exe = path
                        break
                else:
                    result = subprocess.run("where gmsh.exe", shell=True,
                                          capture_output=True, text=True)
                    if result.returncode == 0:
                        gmsh_exe = result.stdout.strip().split('\n')[0]

            if not gmsh_exe or not os.path.exists(gmsh_exe):
                gmsh_exe, _ = QFileDialog.getOpenFileName(
                    self,
                    "选择Gmsh程序",
                    "",
                    "可执行文件 (*.exe);;所有文件 (*.*)"
                )
                if not gmsh_exe:
                    return

            self.config_manager.set_gmsh_path(gmsh_exe)
            subprocess.Popen(gmsh_exe)
        except Exception as e:
            QMessageBox.critical(self, "错误", f"无法启动Gmsh: {str(e)}")

    def run_wsl_nautilus(self):
        """运行 WSL Nautilus (文件管理器)

        启动 WSL 中的 Nautilus 文件管理器
        """
        try:
            command = self.config_manager.get_wsl_files_command()
            if not command:
                QMessageBox.warning(self, "提示", "WSL Files 命令未配置，请检查配置文件")
                return

            self.log_msg(f"运行 WSL Nautilus...")
            subprocess.Popen(command, shell=True)
        except Exception as e:
            QMessageBox.critical(self, "错误", f"运行 WSL Nautilus 失败: {str(e)}")

    def run_wsl_baobab(self):
        """运行 WSL Baobab (磁盘分析工具)

        启动 WSL 中的 Baobab 磁盘分析工具
        """
        try:
            command = self.config_manager.get_wsl_disk_analysis_command()
            if not command:
                QMessageBox.warning(self, "提示", "WSL Disk Analysis 命令未配置，请检查配置文件")
                return

            self.log_msg(f"运行 WSL Baobab...")
            subprocess.Popen(command, shell=True)
        except Exception as e:
            QMessageBox.critical(self, "错误", f"运行 WSL Baobab 失败: {str(e)}")

    def run_wsl_gnome_tweaks(self):
        """运行 WSL GNOME Tweaks (外观设置)

        启动 WSL 中的 GNOME Tweaks 外观设置工具
        """
        try:
            command = self.config_manager.get_wsl_appearance_command()
            if not command:
                QMessageBox.warning(self, "提示", "WSL Appearance 命令未配置，请检查配置文件")
                return

            self.log_msg(f"运行 WSL GNOME Tweaks...")
            subprocess.Popen(command, shell=True)
        except Exception as e:
            QMessageBox.critical(self, "错误", f"运行 WSL GNOME Tweaks 失败: {str(e)}")

    def open_wsl_bashrc(self):
        """打开 WSL .bashrc 文件

        使用系统默认编辑器打开 WSL 的 .bashrc 配置文件
        """
        try:
            bashrc_path = self.config_manager.get_wsl_bashrc_path()
            if not bashrc_path:
                QMessageBox.warning(self, "提示", "WSL .bashrc 路径未配置，请检查配置文件")
                return

            if os.path.exists(bashrc_path):
                self.log_msg(f"打开 .bashrc: {bashrc_path}")
                os.startfile(bashrc_path)
            else:
                QMessageBox.warning(self, "提示", f".bashrc 文件不存在: {bashrc_path}")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"打开 .bashrc 失败: {str(e)}")

    def check_mesh(self):
        """运行 checkMesh 命令

        在当前算例目录通过 WSL 运行 checkMesh，并将结果保存到当前目录的 checkMesh时间.txt 文件中
        """
        try:
            case_path = self.case_path_edit.text()
            if not case_path or not os.path.isdir(case_path):
                QMessageBox.warning(self, "提示", "请先选择有效的算例目录")
                return

            # 获取当前时间作为文件名的一部分
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M")
            output_filename = f"checkMesh_{timestamp}.txt"
            output_path = os.path.join(case_path, output_filename)

            self.log_msg(f"开始运行 checkMesh...")
            self.log_msg(f"输出文件: {output_filename}")

            # 将 Windows 路径转换为 WSL 路径
            wsl_case_path = case_path.replace('\\', '/')
            if wsl_case_path[1] == ':':
                wsl_case_path = f"/mnt/{wsl_case_path[0].lower()}{wsl_case_path[2:]}"

            # 获取 OpenFOAM 环境源路径
            openfoam_env_source = self.config_manager.get_openfoam_env_source()

            # 构建命令
            command = f'wsl bash -c "cd {wsl_case_path} && {openfoam_env_source} && checkMesh > checkMesh_{timestamp}.txt 2>&1"'

            self.log_msg(f"执行命令: {command}")

            # 执行命令（不捕获输出，避免编码问题）
            result = subprocess.run(command, shell=True, timeout=300)

            # 等待文件写入完成
            import time
            time.sleep(0.5)

            # 读取结果文件内容
            result_content = ""
            if os.path.exists(output_path):
                with open(output_path, 'r', encoding='utf-8', errors='ignore') as f:
                    result_content = f.read()
            else:
                self.log_msg(f"警告: 输出文件未生成: {output_path}")

            # OpenFOAM 的 checkMesh 在发现问题时返回非零退出码，这是正常行为
            # 只要结果文件生成了，就认为执行成功
            if os.path.exists(output_path):
                self.log_msg("=" * 60)
                self.log_msg("checkMesh 执行结果:")
                self.log_msg("=" * 60)
                self.log_msg(result_content)
                self.log_msg("=" * 60)

                # 提取网格质量指标
                cells = None
                aspect_ratio = None
                non_orthogonality_max = None
                non_orthogonality_avg = None
                skewness = None

                for line in result_content.split('\n'):
                    # 提取单元总数：格式如 "cells: 12345"
                    if line.strip().startswith('cells:'):
                        cells = line.strip()
                    # 提取最大伸缩比：格式如 "Max aspect ratio = 1.23"
                    elif 'Max aspect ratio' in line and '=' in line:
                        aspect_ratio = line.strip()
                    # 提取非正交度：格式如 "Mesh non-orthogonality Max: 64.757824 average: 22.320833"
                    elif 'Mesh non-orthogonality Max:' in line:
                        non_orthogonality_max = line.strip()
                        non_orthogonality_avg = line.strip()
                    # 提取最大偏斜度：格式如 "Max skewness = 0.45"
                    elif 'Max skewness' in line and '=' in line:
                        skewness = line.strip()

                # 提取数值并保留2位小数
                import re

                def extract_value(text):
                    match = re.search(r'[\d.]+', str(text))
                    if match:
                        try:
                            return float(match.group())
                        except ValueError:
                            return None
                    return None

                # 从 "cells: 12345" 提取数值
                cells_value = None
                if cells:
                    match = re.search(r'cells:\s*([\d.]+)', cells)
                    if match:
                        cells_value = float(match.group(1))

                aspect_ratio_value = extract_value(aspect_ratio)

                # 从 "Mesh non-orthogonality Max: 64.757824 average: 22.320833" 提取两个值
                non_orthogonality_max_value = None
                non_orthogonality_avg_value = None
                if non_orthogonality_max:
                    max_match = re.search(r'Max:\s*([\d.]+)', non_orthogonality_max)
                    avg_match = re.search(r'average:\s*([\d.]+)', non_orthogonality_max)
                    if max_match:
                        non_orthogonality_max_value = float(max_match.group(1))
                    if avg_match:
                        non_orthogonality_avg_value = float(avg_match.group(1))

                skewness_value = extract_value(skewness)

                # 保存网格质量指标到单独的文件
                quality_filename = f"MeshQuality_{timestamp}.txt"
                quality_path = os.path.join(case_path, quality_filename)

                with open(quality_path, 'w', encoding='utf-8') as f:
                    f.write("网格质量指标\n")
                    f.write("=" * 40 + "\n\n")
                    if cells_value is not None:
                        f.write(f"单元总数\ncells = {cells_value:.0f}\n\n")
                    if aspect_ratio_value is not None:
                        f.write(f"最大伸缩比\nMax aspect ratio = {aspect_ratio_value:.2f}\n\n")
                    if non_orthogonality_max_value is not None:
                        f.write(f"最大非正交度\nMesh non-orthogonality Max = {non_orthogonality_max_value:.2f}\n\n")
                    if non_orthogonality_avg_value is not None:
                        f.write(f"平均非正交度\nMesh non-orthogonality average = {non_orthogonality_avg_value:.2f}\n\n")
                    if skewness_value is not None:
                        f.write(f"最大偏斜度\nMax skewness = {skewness_value:.2f}\n\n")
                    f.write("=" * 40 + "\n")
                    f.write(f"生成时间: {timestamp}\n")

                self.log_msg(f"网格质量指标已保存到: {quality_filename}")

                # 检查结果中是否包含 "Mesh OK"
                if "Mesh OK" in result_content:
                    QMessageBox.information(self, "完成", f"checkMesh 执行完成！\n网格状态: OK\n结果已保存到: {output_filename}\n网格质量指标已保存到: {quality_filename}")
                else:
                    QMessageBox.warning(self, "完成", f"checkMesh 执行完成！\n网格存在问题，请查看日志详情。\n结果已保存到: {output_filename}\n网格质量指标已保存到: {quality_filename}")
            else:
                self.log_msg(f"checkMesh 执行失败，返回码: {result.returncode}")
                self.log_msg(f"错误信息: {result.stderr}")
                QMessageBox.critical(self, "错误", f"checkMesh 执行失败，结果文件未生成。")

        except subprocess.TimeoutExpired:
            QMessageBox.critical(self, "错误", "checkMesh 执行超时（超过5分钟）")
            self.log_msg("checkMesh 执行超时")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"运行 checkMesh 失败: {str(e)}")
            self.log_msg(f"错误: {str(e)}")

    def log_msg(self, msg):
        """
        添加日志消息

        将消息添加到日志显示区域，并自动滚动到底部

        Args:
            msg (str): 要添加的日志消息
        """
        self.Log.appendPlainText(msg)
        scrollbar = self.Log.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def combine_to_markdown(self):
        """合并源码为 Markdown

        扫描指定目录下的所有源代码文件，将它们合并为一个带目录的 Markdown 文档
        """
        dir_path = self.case_path_edit.text()

        if not dir_path or not os.path.isdir(dir_path):
            QMessageBox.warning(self, "提示", "请选择有效的算例目录")
            return

        # 禁用按钮，显示进度条
        self.combine_md_btn.setEnabled(False)
        self.progressbar_manager.show_progress_bar()
        self.Log.clear()
        self.log_msg("开始扫描项目文件...")

        # 处理事件循环，让UI有机会更新
        self.progressbar_manager.process_events()

        # 扫描文件
        files = scan_directory(dir_path,
                              progress_callback=lambda p: self.progressbar_manager.update_progress(p),
                              log_callback=lambda msg: self.log_msg(msg))

        self.log_msg(f"找到 {len(files)} 个源代码文件")
        self.log_msg("正在合并为 Markdown...")

        # 生成输出文件名
        project_name = os.path.basename(dir_path)
        md_path = os.path.join(dir_path, f"{project_name}_source_code.md")

        # 合并文件
        success = combine_files_to_markdown(files, md_path, dir_path,
                                           progress_callback=lambda p: self.progressbar_manager.update_progress(p))

        # 任务完成后将进度条重置为0
        from PySide6.QtCore import QTimer
        QTimer.singleShot(1000, lambda: self.progressbar_manager.update_progress(0))

        self.combine_md_btn.setEnabled(True)

        if success:
            self.log_msg(f"Markdown 文件已生成: {md_path}")
            self.log_msg(f"Markdown 文件已生成: {os.path.basename(md_path)}")
            QMessageBox.information(self, "完成", "源码合并成功！")
        else:
            self.log_msg("源码合并失败")
            QMessageBox.critical(self, "错误", "源码合并失败，请查看日志输出。")

    def export_to_pdf(self):
        """导出为 PDF

        将之前生成的 Markdown 文档转换为 PDF 文件
        """
        dir_path = self.case_path_edit.text()
        project_name = os.path.basename(dir_path)
        md_path = os.path.join(dir_path, f"{project_name}_source_code.md")
        pdf_path = os.path.join(dir_path, f"{project_name}_source_code.pdf")

        if not os.path.exists(md_path):
            QMessageBox.warning(self, "提示", "请先合并源码为 Markdown")
            return

        # 显示进度条
        self.progressbar_manager.show_progress_bar()

        # 处理事件循环，让UI有机会更新
        self.progressbar_manager.process_events()

        # 获取 wkhtmltopdf 路径
        wkhtmltopdf_path = self.config_manager.get_wkhtmltopdf_path()

        # 转换为 PDF
        success = markdown_to_pdf(md_path, pdf_path, wkhtmltopdf_path,
                                  logger=self.log_msg,
                                  progress_callback=lambda p: self.progressbar_manager.update_progress(p))

        # 任务完成后将进度条重置为0
        from PySide6.QtCore import QTimer
        QTimer.singleShot(1000, lambda: self.progressbar_manager.update_progress(0))

        if success:
            self.log_msg(f"PDF 文件已生成: {pdf_path}")
            self.log_msg(f"PDF 文件已生成: {os.path.basename(pdf_path)}")
            QMessageBox.information(self, "完成", "PDF 导出成功！")
        else:
            self.log_msg("PDF 导出失败")
            QMessageBox.critical(self, "错误", "PDF 导出失败，请查看日志输出。")

    def start(self):
        """开始执行网格转换

        启动后台线程执行 GMSH 到 OpenFOAM 的网格转换过程
        """
        msh_path = self.msh_path_edit.text()
        case_path = self.case_path_edit.text()

        if not msh_path or not os.path.isfile(msh_path):
            QMessageBox.warning(self, "提示", "请选择具体的 .msh 文件")
            return

        if not case_path:
            QMessageBox.warning(self, "提示", "请选择算例目录")
            return

        self.start_mesh_btn.setEnabled(False)
        self.start_mesh_btn.setText("正在处理...")
        self.progressbar_manager.show_progress_bar()
        self.Log.clear()

        env_source = self.config_manager.get_openfoam_env_source()
        self.worker_thread = WorkerThread(self.update_func, msh_path, case_path, env_source)
        self.worker_thread.log_signal.connect(self.log_msg)
        self.worker_thread.progress_signal.connect(self.progressbar_manager.update_progress)
        self.worker_thread.finished_signal.connect(self.on_finished)
        self.worker_thread.start()

    def on_finished(self, success, error_msg):
        """
        工作线程完成回调

        当后台网格转换线程完成时调用此方法

        Args:
            success (bool): 操作是否成功
            error_msg (str): 错误消息（如果有的话）
        """
        # 更新进度到100%以显示完成状态
        self.progressbar_manager.update_progress(100)
        # 短暂延迟后将进度条重置为0
        from PySide6.QtCore import QTimer
        QTimer.singleShot(1000, self._reset_progress_bar)  # 1秒后将进度条重置为0

        self.start_mesh_btn.setEnabled(True)
        self.start_mesh_btn.setText("开始转换网格")

        if success:
            QMessageBox.information(self, "完成", "网格转换及边界修正成功！")
        else:
            if error_msg:
                self.log_msg(f"错误: {error_msg}")
            QMessageBox.critical(self, "错误", "网格转换失败，请查看日志输出。")

    def _reset_progress_bar(self):
        """将进度条重置为0的辅助方法"""
        self.progressbar_manager.update_progress(0)


def run_jdfoam_gui(update_func, app_icon_path=None):
    """
    运行 JDFOAM GUI

    启动图形用户界面应用程序

    Args:
        update_func: 网格更新函数
        app_icon_path: 应用程序图标文件路径（可选）
    """
    app = QApplication([])

    # 设置应用程序图标
    if app_icon_path and os.path.exists(app_icon_path):
        app.setWindowIcon(QIcon(app_icon_path))

    gui = PySide6GmshConverterGUI(update_func, app_icon_path)
    gui.show()
    app.exec()


__all__ = [
    'run_jdfoam_gui',
    'PySide6GmshConverterGUI',
    'WorkerThread',
    'ConfigManager'
]