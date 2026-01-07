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
                             QGroupBox, QProgressBar, QMessageBox)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QFont
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
        # 获取 resources 目录的绝对路径
        resources_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "resources")

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
                icon_path = os.path.join(resources_path, icon_file)
                if os.path.exists(icon_path):
                    button.setIcon(QIcon(icon_path))
                    print(f"按钮图标已设置: {button_name} -> {icon_path}")
                else:
                    print(f"警告: 图标文件不存在: {icon_path}")

    def set_window_icon(self):
        """设置窗口图标

        从传入的路径或 resources 目录加载并设置应用程序图标
        """
        # 优先使用传入的图标路径
        if self.app_icon_path and os.path.exists(self.app_icon_path):
            window_icon_path = self.app_icon_path
        else:
            # 获取 resources 目录的绝对路径
            resources_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "resources")
            # 尝试查找 JDFOAM.png
            window_icon_path = os.path.join(resources_path, "JDFOAM.png")

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


def run_pyside6_gui(update_func, app_icon_path=None):
    """
    运行 PySide6 GUI

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
    'run_pyside6_gui',
    'PySide6GmshConverterGUI',
    'WorkerThread',
    'ConfigManager'
]