"""配置管理模块

该模块提供应用程序的配置管理功能，包括：
- 配置文件的读取和保存
- 各种路径和参数的管理
- 用户偏好设置的持久化
- 配置项的统一访问接口
"""

import os
import configparser


class ConfigManager:
    """配置管理器

    管理应用程序的各种配置项，包括外部工具路径、用户偏好设置、
    环境变量等，提供统一的配置读取和保存接口。
    """

    def __init__(self, config_file="JDFOAM.ini"):
        """
        初始化配置管理器

        Args:
            config_file (str): 配置文件名，默认为 "JDFOAM.ini"
        """
        # 获取可执行文件所在目录，以确保在打包后也能正确找到配置文件
        import sys
        if getattr(sys, 'frozen', False):
            # 如果是打包后的可执行文件
            self.root_dir = os.path.dirname(sys.executable)
        else:
            # 如果是开发环境
            self.root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.config_file = os.path.join(self.root_dir, config_file)
        # 使用 RawConfigParser 来正确处理包含引号的值
        self.config = configparser.RawConfigParser()
        self.gmsh_exe_path = ""  # Gmsh 可执行文件路径
        self.treefoam_command = ""  # TreeFOAM 命令
        self.wkhtmltopdf_path = ""  # wkhtmltopdf 可执行文件路径
        self.theme = "light"  # 当前主题，默认为浅色
        self.openfoam_env_source = "source /usr/lib/openfoam/openfoam2506/etc/bashrc"  # OpenFOAM 环境源路径
        self.case_path = ""  # 算例目录路径
        self.msh_path = ""  # MSH 文件路径

    def load_config(self):
        """加载配置文件

        从配置文件中读取所有配置项并初始化内部变量
        """
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config.read_file(f)
                if self.config.has_section('General'):
                    if self.config.has_option('General', 'gmsh_path'):
                        self.gmsh_exe_path = self.config.get('General', 'gmsh_path')
                    if self.config.has_option('General', 'treefoam_command'):
                        self.treefoam_command = self.config.get('General', 'treefoam_command')
                    if self.config.has_option('General', 'wkhtmltopdf_path'):
                        self.wkhtmltopdf_path = self.config.get('General', 'wkhtmltopdf_path')
                    if self.config.has_option('General', 'theme'):
                        self.theme = self.config.get('General', 'theme')
                    if self.config.has_option('General', 'case_path'):
                        self.case_path = self.config.get('General', 'case_path')
                    if self.config.has_option('General', 'msh_path'):
                        self.msh_path = self.config.get('General', 'msh_path')
                    if self.config.has_option('General', 'openfoam_env_source'):
                        self.openfoam_env_source = self.config.get('General', 'openfoam_env_source')
        except Exception as e:
            print(f"加载配置文件失败: {e}")
            self.gmsh_exe_path = ""
            self.treefoam_command = ""
            self.wkhtmltopdf_path = ""

    def save_config(self):
        """保存配置文件

        将当前配置项保存到配置文件中
        """
        try:
            if not self.config.has_section('General'):
                self.config.add_section('General')
            self.config.set('General', 'gmsh_path', self.gmsh_exe_path)
            self.config.set('General', 'treefoam_command', self.treefoam_command)
            self.config.set('General', 'wkhtmltopdf_path', self.wkhtmltopdf_path)

            with open(self.config_file, 'w', encoding='utf-8') as f:
                self.config.write(f)
        except Exception as e:
            print(f"保存配置文件失败: {e}")

    def get_gmsh_path(self):
        """
        获取 Gmsh 可执行文件路径

        Returns:
            str: Gmsh 可执行文件路径
        """
        return self.gmsh_exe_path

    def set_gmsh_path(self, path):
        """
        设置 Gmsh 可执行文件路径

        Args:
            path (str): Gmsh 可执行文件路径
        """
        self.gmsh_exe_path = path
        self.save_config()

    def get_treefoam_command(self):
        """
        获取 TreeFOAM 命令

        Returns:
            str: TreeFOAM 命令
        """
        return self.treefoam_command

    def set_treefoam_command(self, command):
        """
        设置 TreeFOAM 命令

        Args:
            command (str): TreeFOAM 命令
        """
        self.treefoam_command = command
        self.save_all_config()

    def get_theme(self):
        """
        获取当前主题

        Returns:
            str: 当前主题名称 ("light" 或 "dark")
        """
        return self.theme

    def set_theme(self, theme):
        """
        设置当前主题

        Args:
            theme (str): 主题名称 ("light" 或 "dark")
        """
        self.theme = theme
        self.save_all_config()

    def save_all_config(self):
        """保存所有配置

        将所有配置项保存到配置文件中
        """
        if not self.config.has_section('General'):
            self.config.add_section('General')
        self.config.set('General', 'gmsh_path', self.gmsh_exe_path)
        self.config.set('General', 'openfoam_env_source', self.openfoam_env_source)
        self.config.set('General', 'treefoam_command', self.treefoam_command)
        self.config.set('General', 'theme', self.theme)
        self.config.set('General', 'case_path', self.case_path)
        self.config.set('General', 'msh_path', self.msh_path)

        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                self.config.write(f)
        except Exception as e:
            print(f"保存配置文件失败: {e}")

    def get_wkhtmltopdf_path(self):
        """
        获取 wkhtmltopdf 可执行文件路径

        Returns:
            str: wkhtmltopdf 可执行文件路径
        """
        return self.wkhtmltopdf_path

    def set_wkhtmltopdf_path(self, path):
        """
        设置 wkhtmltopdf 可执行文件路径

        Args:
            path (str): wkhtmltopdf 可执行文件路径
        """
        self.wkhtmltopdf_path = path
        self.save_config()

    def get_openfoam_env_source(self):
        """
        获取 OpenFOAM 环境源路径

        Returns:
            str: OpenFOAM 环境源路径
        """
        return self.openfoam_env_source

    def set_openfoam_env_source(self, env_source):
        """
        设置 OpenFOAM 环境源路径

        Args:
            env_source (str): OpenFOAM 环境源路径
        """
        self.openfoam_env_source = env_source
        self.save_all_config()

    def get_case_path(self):
        """
        获取算例目录路径

        Returns:
            str: 算例目录路径
        """
        return self.case_path

    def set_case_path(self, path):
        """
        设置算例目录路径

        Args:
            path (str): 算例目录路径
        """
        self.case_path = path
        self.save_all_config()

    def get_msh_path(self):
        """
        获取 MSH 文件路径

        Returns:
            str: MSH 文件路径
        """
        return self.msh_path

    def set_msh_path(self, path):
        """
        设置 MSH 文件路径

        Args:
            path (str): MSH 文件路径
        """
        self.msh_path = path
        self.save_all_config()