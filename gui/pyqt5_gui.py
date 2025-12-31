import sys
import os
import json
import subprocess
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QTextEdit, QFileDialog,
                             QGroupBox, QProgressBar, QMessageBox)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QFont


class WorkerThread(QThread):
    """工作线程，用于执行耗时操作"""
    log_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(bool, str)

    def __init__(self, update_func, msh_path, case_path):
        super().__init__()
        self.update_func = update_func
        self.msh_path = msh_path
        self.case_path = case_path

    def run(self):
        try:
            success = self.update_func(self.msh_path, self.case_path, logger=self.log_signal.emit)
            self.finished_signal.emit(success, "")
        except Exception as e:
            self.finished_signal.emit(False, str(e))


class PyQt5GmshConverterGUI(QMainWindow):
    def __init__(self, update_func):
        super().__init__()
        self.update_func = update_func
        self.config_file = "gui_config.json"
        self.worker_thread = None

        self.init_ui()
        self.load_config()

    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("JDFOAM")
        self.setFixedSize(700, 600)

        # 设置窗口图标
        icon_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                "resources", "gmsh.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        # 主窗口部件
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # 主布局
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)

        # 1. 路径配置区
        path_group = QGroupBox("路径配置")
        path_layout = QVBoxLayout()
        path_group.setLayout(path_layout)

        # MSH文件路径
        msh_layout = QHBoxLayout()
        msh_label = QLabel("MSH 文件/路径:")
        msh_label.setFixedWidth(120)
        self.msh_path_edit = QLineEdit()
        self.msh_path_edit.setPlaceholderText("选择 .msh 文件")
        msh_browse_btn = QPushButton("选择文件")
        msh_browse_btn.clicked.connect(self.select_msh)
        self.gmsh_btn = QPushButton()
        self.gmsh_btn.setFixedSize(30, 30)
        self.gmsh_btn.setToolTip("打开Gmsh")
        self.gmsh_btn.clicked.connect(self.open_gmsh)
        msh_layout.addWidget(msh_label)
        msh_layout.addWidget(self.msh_path_edit)
        msh_layout.addWidget(msh_browse_btn)
        msh_layout.addWidget(self.gmsh_btn)
        path_layout.addLayout(msh_layout)

        # 算例目录路径
        case_layout = QHBoxLayout()
        case_label = QLabel("算例目录:")
        case_label.setFixedWidth(120)
        self.case_path_edit = QLineEdit()
        self.case_path_edit.setPlaceholderText("选择算例目录")
        case_browse_btn = QPushButton("选择目录")
        case_browse_btn.clicked.connect(self.select_case)
        self.treefoam_btn = QPushButton()
        self.treefoam_btn.setFixedSize(30, 30)
        self.treefoam_btn.setToolTip("运行TreeFOAM")
        self.treefoam_btn.clicked.connect(self.run_treefoam)
        case_layout.addWidget(case_label)
        case_layout.addWidget(self.case_path_edit)
        case_layout.addWidget(case_browse_btn)
        case_layout.addWidget(self.treefoam_btn)
        path_layout.addLayout(case_layout)

        main_layout.addWidget(path_group)

        # 2. 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)  # 不确定进度模式
        self.progress_bar.setTextVisible(False)
        self.progress_bar.hide()
        main_layout.addWidget(self.progress_bar)

        # 3. 日志区域
        log_group = QGroupBox("日志输出")
        log_layout = QVBoxLayout()
        log_group.setLayout(log_layout)

        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setFont(QFont("Consolas", 11))
        log_layout.addWidget(self.log_area)

        main_layout.addWidget(log_group)

        # 4. 执行按钮
        self.start_btn = QPushButton("开始执行 (WSL)")
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        self.start_btn.clicked.connect(self.start)
        main_layout.addWidget(self.start_btn)

        # 加载Gmsh按钮图标
        self.load_gmsh_icon()
        # 加载TreeFOAM按钮图标
        self.load_treefoam_icon()

    def load_gmsh_icon(self):
        """加载Gmsh按钮图标"""
        icon_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                "resources", "gmsh.ico")
        if os.path.exists(icon_path):
            self.gmsh_btn.setIcon(QIcon(icon_path))
            self.gmsh_btn.setIconSize(self.gmsh_btn.size())

    def load_treefoam_icon(self):
        """加载TreeFOAM按钮图标"""
        icon_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                "resources", "TreeFoam.ico")
        if os.path.exists(icon_path):
            self.treefoam_btn.setIcon(QIcon(icon_path))
            self.treefoam_btn.setIconSize(self.treefoam_btn.size())

    def load_config(self):
        """加载配置文件"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    if 'gmsh_path' in config:
                        self.gmsh_exe_path = config['gmsh_path']
        except Exception as e:
            print(f"加载配置文件失败: {e}")
            self.gmsh_exe_path = ""

    def save_config(self, config):
        """保存配置文件"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"保存配置文件失败: {e}")

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

    def run_treefoam(self):
        """运行TreeFOAM命令"""
        try:
            env_source = "source /usr/lib/openfoam/openfoam2506/etc/bashrc"

            # 如果选择了算例目录，则进入该目录
            case_path = self.case_path_edit.text()
            if case_path and os.path.isdir(case_path):
                # 转换为WSL路径
                wsl_case = case_path.replace('\\', '/')
                if ':' in wsl_case:
                    drive, rest = wsl_case.split(':', 1)
                    wsl_case = f"/mnt/{drive.lower()}{rest}"
                cmd = f'wsl bash -c "{env_source} && cd \"{wsl_case}\" && treeFoam"'
                self.log_msg(f"运行 TreeFOAM: {case_path}")
            else:
                # 直接运行treefoam
                cmd = f'wsl bash -c "{env_source} && treeFoam"'
                self.log_msg("运行 TreeFOAM")

            # 在后台运行
            subprocess.Popen(cmd, shell=True)

        except Exception as e:
            QMessageBox.critical(self, "错误", f"运行 TreeFOAM 失败: {str(e)}")

    def open_gmsh(self):
        """打开Gmsh程序"""
        try:
            # 检查是否已有保存的路径
            gmsh_exe = getattr(self, 'gmsh_exe_path', '')

            # 如果没有保存的路径，尝试常见位置
            if not gmsh_exe or not os.path.exists(gmsh_exe):
                possible_paths = [
                    r"C:\Program Files\gmsh\gmsh.exe",
                    r"C:\Program Files (x86)\gmsh\gmsh.exe",
                    r"C:\gmsh\gmsh.exe"
                ]
                for path in possible_paths:
                    if os.path.exists(path):
                        gmsh_exe = path
                        break
                else:
                    # 尝试在PATH中查找
                    result = subprocess.run("where gmsh.exe", shell=True,
                                          capture_output=True, text=True)
                    if result.returncode == 0:
                        gmsh_exe = result.stdout.strip().split('\n')[0]

            # 如果还是找不到，让用户选择
            if not gmsh_exe or not os.path.exists(gmsh_exe):
                gmsh_exe, _ = QFileDialog.getOpenFileName(
                    self,
                    "选择Gmsh程序",
                    "",
                    "可执行文件 (*.exe);;所有文件 (*.*)"
                )
                if not gmsh_exe:
                    return

            # 保存路径
            self.gmsh_exe_path = gmsh_exe
            self.save_config({"gmsh_path": gmsh_exe})

            # 启动Gmsh
            subprocess.Popen(gmsh_exe)
            self.log_msg(f"Gmsh 已启动: {gmsh_exe}")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"无法启动Gmsh: {str(e)}")

    def log_msg(self, msg):
        """添加日志消息"""
        self.log_area.append(msg)
        # 滚动到底部
        scrollbar = self.log_area.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

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

        # 禁用按钮，显示进度条
        self.start_btn.setEnabled(False)
        self.start_btn.setText("正在处理...")
        self.progress_bar.show()
        self.log_area.clear()

        # 创建并启动工作线程
        self.worker_thread = WorkerThread(self.update_func, msh_path, case_path)
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


def run_pyqt5_gui(update_func):
    """运行PyQt5 GUI"""
    app = QApplication(sys.argv)
    gui = PyQt5GmshConverterGUI(update_func)
    gui.show()
    sys.exit(app.exec_())