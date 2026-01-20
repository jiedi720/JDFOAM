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

        # 设置默认值
        self.treefoam_command = '"C:\\Program Files\\WSL\\wslg.exe" -d DEXCS2025 -u jiedi -- bash -l -c "/usr/local/bin/start_treefoam.sh; echo \'----------------\'; echo \'Script execution completed\'; read -p \'Press Enter to close window...\'"'  # TreeFOAM 命令默认值

        # Gmsh 默认路径：优先检查 D 盘，然后检查 C 盘
        default_gmsh_d = "D:\\gmsh-4.15.0-Windows64\\gmsh.exe"
        default_gmsh_c = "C:\\gmsh-4.15.0-Windows64\\gmsh.exe"
        if os.path.exists(default_gmsh_d):
            self.gmsh_exe_path = default_gmsh_d
        elif os.path.exists(default_gmsh_c):
            self.gmsh_exe_path = default_gmsh_c
        else:
            self.gmsh_exe_path = ""

        self.wkhtmltopdf_path = ""  # wkhtmltopdf 可执行文件路径
        self.theme = "light"  # 当前主题，默认为浅色
        self.openfoam_env_source = "source /usr/lib/openfoam/openfoam2506/etc/bashrc"  # OpenFOAM 环境源路径
        self.case_path = ""  # 算例目录路径
        self.msh_path = ""  # MSH 文件路径
        
        # WSL 命令默认值
        self.wsl_files_command = '"C:\\Program Files\\WSL\\wslg.exe" -d DEXCS2025 --cd "~" -- nautilus --new-window'
        self.wsl_disk_analysis_command = '"C:\\Program Files\\WSL\\wslg.exe" -d DEXCS2025 --cd "~" -- baobab'
        self.wsl_appearance_command = '"C:\\Program Files\\WSL\\wslg.exe" -d DEXCS2025 --cd "~" -- gnome-tweaks'
        self.wsl_bashrc_path = 'Z:\\home\\jiedi\\.bashrc'

    def load_config(self):
        """加载配置文件

        从配置文件中读取所有配置项并初始化内部变量
        只有当配置文件中存在有效的非空值时才覆盖默认值
        """
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config.read_file(f)
                if self.config.has_section('General'):
                    if self.config.has_option('General', 'gmsh_path'):
                        value = self.config.get('General', 'gmsh_path')
                        if value:  # 只有非空值才覆盖默认值
                            self.gmsh_exe_path = value
                    if self.config.has_option('General', 'treefoam_command'):
                        value = self.config.get('General', 'treefoam_command')
                        if value:  # 只有非空值才覆盖默认值
                            self.treefoam_command = value
                    if self.config.has_option('General', 'wkhtmltopdf_path'):
                        value = self.config.get('General', 'wkhtmltopdf_path')
                        if value:
                            self.wkhtmltopdf_path = value
                    if self.config.has_option('General', 'theme'):
                        value = self.config.get('General', 'theme')
                        if value:
                            self.theme = value
                    if self.config.has_option('General', 'case_path'):
                        value = self.config.get('General', 'case_path')
                        if value:
                            self.case_path = value
                    if self.config.has_option('General', 'msh_path'):
                        value = self.config.get('General', 'msh_path')
                        if value:
                            self.msh_path = value
                    if self.config.has_option('General', 'openfoam_env_source'):
                        value = self.config.get('General', 'openfoam_env_source')
                        if value:
                            self.openfoam_env_source = value
                    if self.config.has_option('General', 'wsl_files_command'):
                        value = self.config.get('General', 'wsl_files_command')
                        if value:
                            self.wsl_files_command = value
                    if self.config.has_option('General', 'wsl_disk_analysis_command'):
                        value = self.config.get('General', 'wsl_disk_analysis_command')
                        if value:
                            self.wsl_disk_analysis_command = value
                    if self.config.has_option('General', 'wsl_appearance_command'):
                        value = self.config.get('General', 'wsl_appearance_command')
                        if value:
                            self.wsl_appearance_command = value
                    if self.config.has_option('General', 'wsl_bashrc_path'):
                        value = self.config.get('General', 'wsl_bashrc_path')
                        if value:
                            self.wsl_bashrc_path = value
        except Exception as e:
            print(f"加载配置文件失败: {e}")

    def save_config(self):
        """保存配置文件

        将当前配置项保存到配置文件中
        """
        # 直接写入文件，按指定顺序
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                f.write('[General]\n')
                # 将theme选项放在最顶部
                f.write(f'theme = {self.theme}\n')
                f.write(f'case_path = {self.case_path}\n')
                f.write(f'msh_path = {self.msh_path}\n')
                f.write(f'gmsh_path = {self.gmsh_exe_path}\n')
                f.write(f'openfoam_env_source = {self.openfoam_env_source}\n')
                f.write(f'wsl_bashrc_path = {self.wsl_bashrc_path}\n')
                f.write(f'treefoam_command = {self.treefoam_command}\n')
                f.write(f'wkhtmltopdf_path = {self.wkhtmltopdf_path}\n')
                f.write(f'wsl_files_command = {self.wsl_files_command}\n')
                f.write(f'wsl_disk_analysis_command = {self.wsl_disk_analysis_command}\n')
                f.write(f'wsl_appearance_command = {self.wsl_appearance_command}\n')
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
        # 直接写入文件，按指定顺序
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                f.write('[General]\n')
                # 将theme选项放在最顶部
                f.write(f'theme = {self.theme}\n')
                f.write(f'case_path = {self.case_path}\n')
                f.write(f'msh_path = {self.msh_path}\n')
                f.write(f'gmsh_path = {self.gmsh_exe_path}\n')
                f.write(f'openfoam_env_source = {self.openfoam_env_source}\n')
                f.write(f'wsl_bashrc_path = {self.wsl_bashrc_path}\n')
                f.write(f'treefoam_command = {self.treefoam_command}\n')
                f.write(f'wsl_files_command = {self.wsl_files_command}\n')
                f.write(f'wsl_disk_analysis_command = {self.wsl_disk_analysis_command}\n')
                f.write(f'wsl_appearance_command = {self.wsl_appearance_command}\n')
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

    def get_wsl_files_command(self):
        """
        获取 WSL Files (Nautilus) 命令

        Returns:
            str: WSL Files 命令
        """
        return self.wsl_files_command

    def set_wsl_files_command(self, command):
        """
        设置 WSL Files (Nautilus) 命令

        Args:
            command (str): WSL Files 命令
        """
        self.wsl_files_command = command
        self.save_all_config()

    def get_wsl_disk_analysis_command(self):
        """
        获取 WSL Disk Analysis (Baobab) 命令

        Returns:
            str: WSL Disk Analysis 命令
        """
        return self.wsl_disk_analysis_command

    def set_wsl_disk_analysis_command(self, command):
        """
        设置 WSL Disk Analysis (Baobab) 命令

        Args:
            command (str): WSL Disk Analysis 命令
        """
        self.wsl_disk_analysis_command = command
        self.save_all_config()

    def get_wsl_appearance_command(self):
        """
        获取 WSL Appearance (Gnome Tweaks) 命令

        Returns:
            str: WSL Appearance 命令
        """
        return self.wsl_appearance_command

    def set_wsl_appearance_command(self, command):
        """
        设置 WSL Appearance (Gnome Tweaks) 命令

        Args:
            command (str): WSL Appearance 命令
        """
        self.wsl_appearance_command = command
        self.save_all_config()

    def get_wsl_bashrc_path(self):
        """
        获取 WSL .bashrc 文件路径

        Returns:
            str: WSL .bashrc 文件路径
        """
        return self.wsl_bashrc_path

    def set_wsl_bashrc_path(self, path):
        """
        设置 WSL .bashrc 文件路径

        Args:
            path (str): WSL .bashrc 文件路径
        """
        self.wsl_bashrc_path = path
        self.save_all_config()