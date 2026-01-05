"""主窗口模块"""
import os
import subprocess
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QTextEdit, QFileDialog,
                             QGroupBox, QProgressBar, QMessageBox)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QFont
from .worker_thread_gui import WorkerThread
from function.config import ConfigManager
from .theme_gui import ThemeManager
from .ui_JDFOAM import Ui_JDFOAM_GUI
from function.combine import scan_directory, combine_files_to_markdown
from function.pdf import markdown_to_pdf


class PySide6GmshConverterGUI(QMainWindow, Ui_JDFOAM_GUI):
    """PySide6 GUI 主窗口"""

    def __init__(self, update_func):
        super().__init__()
        self.update_func = update_func
        self.worker_thread = None
        self.config_manager = ConfigManager()
        self.theme_manager = ThemeManager(self)

        # 设置 UI
        self.setupUi(self)
        
        # 验证 UI 控件是否正确创建
        if not hasattr(self, 'Log'):
            print("警告: Log 未创建")
        if not hasattr(self, 'case_path_edit'):
            print("警告: case_path_edit 未创建")
        
        # 连接信号
        self.connect_signals()
        
        # 加载图标（使用绝对路径）
        self.load_icons()
        
        # 初始化配置和主题
        self.config_manager.load_config()
        
        # 从配置文件加载主题
        saved_theme = self.config_manager.get_theme()
        self.theme_manager.current_theme = saved_theme
        
        # 初始化主题菜单
        self.theme_manager.init_menu()
        
        # 应用主题
        self.theme_manager.apply_theme(saved_theme)
    
    def closeEvent(self, event):
        """关闭窗口时保存主题"""
        self.config_manager.set_theme(self.theme_manager.current_theme)
        super().closeEvent(event)

    def connect_signals(self):
        """连接所有信号和槽"""
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

    def load_icons(self):
        """加载按钮图标"""
        # 获取 resources 目录的绝对路径
        resources_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "resources")
        
        # 加载 TreeFoam 图标
        treefoam_icon_path = os.path.join(resources_path, "TreeFoam.png")
        if os.path.exists(treefoam_icon_path):
            self.treefoam_btn.setIcon(QIcon(treefoam_icon_path))
            self.treefoam_btn.setIconSize(QSize(25, 25))
        
        # 加载 Gmsh 图标
        gmsh_icon_path = os.path.join(resources_path, "gmsh.ico")
        if os.path.exists(gmsh_icon_path):
            self.gmsh_btn.setIcon(QIcon(gmsh_icon_path))
            self.gmsh_btn.setIconSize(QSize(25, 25))

    def select_msh(self):
        """选择MSH文件"""
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
        """选择算例目录"""
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
            self.combine_pdf_btn.setEnabled(False)

    def open_case_dir(self):
        """打开算例目录"""
        dir_path = self.case_path_edit.text()
        if dir_path and os.path.isdir(dir_path):
            os.startfile(dir_path)
        else:
            QMessageBox.warning(self, "提示", "请先选择有效的算例目录")

    def open_msh_dir(self):
        """打开MSH文件所在目录"""
        msh_path = self.msh_path_edit.text()
        if msh_path and os.path.isfile(msh_path):
            dir_path = os.path.dirname(msh_path)
            os.startfile(dir_path)
        else:
            QMessageBox.warning(self, "提示", "请先选择有效的MSH文件")

    def run_treefoam(self):
        """运行TreeFOAM命令"""
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
        """打开Gmsh程序"""
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
            self.log_msg(f"Gmsh 已启动: {gmsh_exe}")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"无法启动Gmsh: {str(e)}")

    def log_msg(self, msg):
        """添加日志消息"""
        self.Log.appendPlainText(msg)
        scrollbar = self.Log.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def select_msh(self):
        """选择MSH文件"""
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

    def combine_to_markdown(self):
        """合并源码为 Markdown"""
        dir_path = self.case_path_edit.text()

        if not dir_path or not os.path.isdir(dir_path):
            QMessageBox.warning(self, "提示", "请选择有效的算例目录")
            return

        # 禁用按钮，显示进度条
        self.combine_md_btn.setEnabled(False)
        self.progress_bar.show()
        self.Log.clear()
        self.log_msg("开始扫描项目文件...")

        # 扫描文件
        files = scan_directory(dir_path, progress_callback=lambda p: self.progress_bar.setValue(p))

        self.log_msg(f"找到 {len(files)} 个源代码文件")
        self.log_msg("正在合并为 Markdown...")

        # 生成输出文件名
        project_name = os.path.basename(dir_path)
        md_path = os.path.join(dir_path, f"{project_name}_source_code.md")

        # 合并文件
        success = combine_files_to_markdown(files, md_path, dir_path,
                                           progress_callback=lambda p: self.progress_bar.setValue(p))

        self.progress_bar.hide()
        self.combine_md_btn.setEnabled(True)

        if success:
            self.log_msg(f"Markdown 文件已生成: {md_path}")
            self.log_msg(f"Markdown 文件已生成: {os.path.basename(md_path)}")
            self.combine_pdf_btn.setEnabled(True)
            QMessageBox.information(self, "完成", "源码合并成功！")
        else:
            self.log_msg("源码合并失败")
            QMessageBox.critical(self, "错误", "源码合并失败，请查看日志输出。")

    def export_to_pdf(self):
        """导出为 PDF"""
        dir_path = self.case_path_edit.text()
        project_name = os.path.basename(dir_path)
        md_path = os.path.join(dir_path, f"{project_name}_source_code.md")
        pdf_path = os.path.join(dir_path, f"{project_name}_source_code.pdf")

        if not os.path.exists(md_path):
            QMessageBox.warning(self, "提示", "请先合并源码为 Markdown")
            return

        # 禁用按钮，显示进度条
        self.combine_pdf_btn.setEnabled(False)
        self.progress_bar.show()

        # 获取 wkhtmltopdf 路径
        wkhtmltopdf_path = self.config_manager.get_wkhtmltopdf_path()

        # 转换为 PDF
        success = markdown_to_pdf(md_path, pdf_path, wkhtmltopdf_path, logger=self.log_msg)

        self.progress_bar.hide()
        self.combine_pdf_btn.setEnabled(True)

        if success:
            self.log_msg(f"PDF 文件已生成: {pdf_path}")
            self.log_msg(f"PDF 文件已生成: {os.path.basename(pdf_path)}")
            QMessageBox.information(self, "完成", "PDF 导出成功！")
        else:
            self.log_msg("PDF 导出失败")
            QMessageBox.critical(self, "错误", "PDF 导出失败，请查看日志输出。")

    def start(self):
        """开始执行"""
        msh_path = self.msh_path_edit.text()
        case_path = self.case_path_edit.text()

        if not msh_path or not os.path.isfile(msh_path):
            QMessageBox.warning(self, "提示", "请选择具体的 .msh 文件")
            return

        if not case_path:
            QMessageBox.warning(self, "提示", "请选择算例目录")
            return

        self.start_btn.setEnabled(False)
        self.start_btn.setText("正在处理...")
        self.progress_bar.show()
        self.Log.clear()

        env_source = self.config_manager.get_openfoam_env_source()
        self.worker_thread = WorkerThread(self.update_func, msh_path, case_path, env_source)
        self.worker_thread.log_signal.connect(self.log_msg)
        self.worker_thread.finished_signal.connect(self.on_finished)
        self.worker_thread.start()

    def on_finished(self, success, error_msg):
        """工作线程完成回调"""
        self.progress_bar.hide()
        self.start_btn.setEnabled(True)
        self.start_btn.setText("开始执行 (WSL)")

        if success:
            QMessageBox.information(self, "完成", "网格转换及边界修正成功！")
        else:
            if error_msg:
                self.log_msg(f"错误: {error_msg}")
            QMessageBox.critical(self, "错误", "网格转换失败，请查看日志输出。")


def run_pyside6_gui(update_func):
    """运行PySide6 GUI"""
    app = QApplication([])
    gui = PySide6GmshConverterGUI(update_func)
    gui.show()
    app.exec()


__all__ = [
    'run_pyside6_gui',
    'PySide6GmshConverterGUI',
    'WorkerThread',
    'ConfigManager'
]