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
        self.wsl_bashrc_path = ""  # WSL .bashrc 路径，将在 load_config 中自动检测
        self.wsl_base = ""  # WSL 基础命令，将在 load_config 中自动检测

        # Light 主题的默认命令（只包含后面的部分，wsl_base 会自动添加）
        self.light_wsl_treefoam_command = '-u jiedi -- bash -l -c "/usr/local/bin/start_treefoam.sh; echo \'----------------\'; echo \'Script execution completed\'; read -p \'Press Enter to close window...\'"'
        self.light_wsl_files_command = '--cd "~" -- nautilus'
        self.light_wsl_disk_analysis_command = '--cd "~" -- baobab'
        self.light_wsl_appearance_command = '--cd "~" -- gnome-tweaks'

        # Dark 主题的默认命令（只包含后面的部分，wsl_base 会自动添加）
        self.dark_wsl_treefoam_command = '-u jiedi -- env GTK_THEME=Adwaita:dark GDK_DPI_SCALE=1.25 GDK_BACKEND=x11 bash -l -c "/usr/local/bin/start_treefoam.sh; echo \'----------------\'; echo \'Script execution completed\'; read -p \'Press Enter to close window...\'"'
        self.dark_wsl_files_command = '--cd "~" -- bash -ic "nautilus"'
        self.dark_wsl_disk_analysis_command = '--cd "~" -- bash -ic "baobab"'
        self.dark_wsl_appearance_command = '--cd "~" -- bash -ic "gnome-tweaks"'

        # 保留旧的默认值用于兼容
        self.treefoam_command = f'{self.wsl_base} {self.light_wsl_treefoam_command}'
        self.wsl_files_command = f'{self.wsl_base} {self.light_wsl_files_command}'
        self.wsl_disk_analysis_command = f'{self.wsl_base} {self.light_wsl_disk_analysis_command}'
        self.wsl_appearance_command = f'{self.wsl_base} {self.light_wsl_appearance_command}'

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
                    if self.config.has_option('General', 'wsl_bashrc_path'):
                        value = self.config.get('General', 'wsl_bashrc_path')
                        if value:
                            self.wsl_bashrc_path = value
                    if self.config.has_option('General', 'wsl_base'):
                        value = self.config.get('General', 'wsl_base')
                        if value:
                            self.wsl_base = value

                # 如果配置文件中没有设置 wsl_base，则自动检测盘符
                if not self.wsl_base:
                    for drive_letter in ['C', 'D', 'E']:
                        wslg_path = f"{drive_letter}:\\Program Files\\WSL\\wslg.exe"
                        if os.path.exists(wslg_path):
                            self.wsl_base = f'"{wslg_path}" -d DEXCS2025'
                            break

                # 如果配置文件中没有设置 wsl_bashrc_path，则自动检测盘符
                if not self.wsl_bashrc_path:
                    for drive_letter in ['Z', 'Y', 'X', 'W', 'V', 'U', 'T', 'S', 'R', 'Q', 'P', 'O', 'N', 'M', 'L', 'K', 'J', 'I', 'H']:
                        bashrc_path = f"{drive_letter}:\\home\\jiedi\\.bashrc"
                        if os.path.exists(bashrc_path):
                            self.wsl_bashrc_path = bashrc_path
                            break

                # 读取 [light] 和 [dark] section 的命令配置
                # 这些配置会在 get_*_command 方法中根据主题动态获取
        except Exception as e:
            print(f"加载配置文件失败: {e}")

    def save_config(self):
        """保存配置文件

        将当前配置项保存到配置文件中，包含 [General]、[light] 和 [dark] 三个 section
        保留用户在配置文件中已经设置的命令，只更新 [General] section 的内容
        """
        try:
            # 读取现有配置文件，保留 [light] 和 [dark] section 的内容
            light_commands = {}
            dark_commands = {}

            if os.path.exists(self.config_file):
                temp_config = configparser.RawConfigParser()
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    temp_config.read_file(f)

                # 读取 [light] section 的命令
                if temp_config.has_section('light'):
                    if temp_config.has_option('light', 'light_wsl_treefoam_command'):
                        light_commands['light_wsl_treefoam_command'] = temp_config.get('light', 'light_wsl_treefoam_command')
                    if temp_config.has_option('light', 'light_wsl_files_command'):
                        light_commands['light_wsl_files_command'] = temp_config.get('light', 'light_wsl_files_command')
                    if temp_config.has_option('light', 'light_wsl_disk_analysis_command'):
                        light_commands['light_wsl_disk_analysis_command'] = temp_config.get('light', 'light_wsl_disk_analysis_command')
                    if temp_config.has_option('light', 'light_wsl_appearance_command'):
                        light_commands['light_wsl_appearance_command'] = temp_config.get('light', 'light_wsl_appearance_command')

                # 读取 [dark] section 的命令
                if temp_config.has_section('dark'):
                    if temp_config.has_option('dark', 'dark_wsl_treefoam_command'):
                        dark_commands['dark_wsl_treefoam_command'] = temp_config.get('dark', 'dark_wsl_treefoam_command')
                    if temp_config.has_option('dark', 'dark_wsl_files_command'):
                        dark_commands['dark_wsl_files_command'] = temp_config.get('dark', 'dark_wsl_files_command')
                    if temp_config.has_option('dark', 'dark_wsl_disk_analysis_command'):
                        dark_commands['dark_wsl_disk_analysis_command'] = temp_config.get('dark', 'dark_wsl_disk_analysis_command')
                    if temp_config.has_option('dark', 'dark_wsl_appearance_command'):
                        dark_commands['dark_wsl_appearance_command'] = temp_config.get('dark', 'dark_wsl_appearance_command')

            # 写入配置文件
            with open(self.config_file, 'w', encoding='utf-8') as f:
                # [General] section
                f.write('[General]\n')
                f.write(f'theme = {self.theme}\n')
                f.write(f'case_path = {self.case_path}\n')
                f.write(f'msh_path = {self.msh_path}\n')
                f.write(f'gmsh_path = {self.gmsh_exe_path}\n')
                f.write(f'openfoam_env_source = {self.openfoam_env_source}\n')
                f.write(f'wsl_bashrc_path = {self.wsl_bashrc_path}\n')
                f.write(f'wkhtmltopdf_path = {self.wkhtmltopdf_path}\n')
                f.write('\n')

                # [light] section - 使用保存的值或默认值
                f.write('[light]\n')
                f.write(f'light_wsl_treefoam_command = {light_commands.get("light_wsl_treefoam_command", self.light_wsl_treefoam_command)}\n')
                f.write(f'light_wsl_files_command = {light_commands.get("light_wsl_files_command", self.light_wsl_files_command)}\n')
                f.write(f'light_wsl_disk_analysis_command = {light_commands.get("light_wsl_disk_analysis_command", self.light_wsl_disk_analysis_command)}\n')
                f.write(f'light_wsl_appearance_command = {light_commands.get("light_wsl_appearance_command", self.light_wsl_appearance_command)}\n')
                f.write('\n')

                # [dark] section - 使用保存的值或默认值
                f.write('[dark]\n')
                f.write(f'dark_wsl_treefoam_command = {dark_commands.get("dark_wsl_treefoam_command", self.dark_wsl_treefoam_command)}\n')
                f.write(f'dark_wsl_files_command = {dark_commands.get("dark_wsl_files_command", self.dark_wsl_files_command)}\n')
                f.write(f'dark_wsl_disk_analysis_command = {dark_commands.get("dark_wsl_disk_analysis_command", self.dark_wsl_disk_analysis_command)}\n')
                f.write(f'dark_wsl_appearance_command = {dark_commands.get("dark_wsl_appearance_command", self.dark_wsl_appearance_command)}\n')
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

        根据当前主题从配置文件读取对应的命令配置。
        如果该主题下没有配置，则使用默认值。
        返回的命令会自动添加 wsl_base 前缀。

        Returns:
            str: TreeFOAM 命令
        """
        command_suffix = ""
        try:
            if self.config.has_section(self.theme):
                if self.theme == 'light':
                    option_name = 'light_wsl_treefoam_command'
                else:
                    option_name = 'dark_wsl_treefoam_command'

                if self.config.has_option(self.theme, option_name):
                    value = self.config.get(self.theme, option_name)
                    if value:
                        command_suffix = value
        except Exception as e:
            print(f"读取 TreeFOAM 命令失败: {e}")

        # 如果没有找到配置，使用默认值
        if not command_suffix:
            if self.theme == 'light':
                command_suffix = self.light_wsl_treefoam_command
            else:
                command_suffix = self.dark_wsl_treefoam_command

        # 返回完整的命令（wsl_base + 命令后缀）
        return f'{self.wsl_base} {command_suffix}'

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
        # 重新加载配置文件，确保 self.config 对象包含最新的配置
        self.load_config()

    def save_all_config(self):
        """保存所有配置

        将所有配置项保存到配置文件中，包含 [General]、[light] 和 [dark] 三个 section
        保留用户在配置文件中已经设置的命令，只更新 [General] section 的内容
        """
        try:
            # 读取现有配置文件，保留 [light] 和 [dark] section 的内容
            light_commands = {}
            dark_commands = {}

            if os.path.exists(self.config_file):
                temp_config = configparser.RawConfigParser()
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    temp_config.read_file(f)

                # 读取 [light] section 的命令
                if temp_config.has_section('light'):
                    if temp_config.has_option('light', 'light_wsl_treefoam_command'):
                        light_commands['light_wsl_treefoam_command'] = temp_config.get('light', 'light_wsl_treefoam_command')
                    if temp_config.has_option('light', 'light_wsl_files_command'):
                        light_commands['light_wsl_files_command'] = temp_config.get('light', 'light_wsl_files_command')
                    if temp_config.has_option('light', 'light_wsl_disk_analysis_command'):
                        light_commands['light_wsl_disk_analysis_command'] = temp_config.get('light', 'light_wsl_disk_analysis_command')
                    if temp_config.has_option('light', 'light_wsl_appearance_command'):
                        light_commands['light_wsl_appearance_command'] = temp_config.get('light', 'light_wsl_appearance_command')

                # 读取 [dark] section 的命令
                if temp_config.has_section('dark'):
                    if temp_config.has_option('dark', 'dark_wsl_treefoam_command'):
                        dark_commands['dark_wsl_treefoam_command'] = temp_config.get('dark', 'dark_wsl_treefoam_command')
                    if temp_config.has_option('dark', 'dark_wsl_files_command'):
                        dark_commands['dark_wsl_files_command'] = temp_config.get('dark', 'dark_wsl_files_command')
                    if temp_config.has_option('dark', 'dark_wsl_disk_analysis_command'):
                        dark_commands['dark_wsl_disk_analysis_command'] = temp_config.get('dark', 'dark_wsl_disk_analysis_command')
                    if temp_config.has_option('dark', 'dark_wsl_appearance_command'):
                        dark_commands['dark_wsl_appearance_command'] = temp_config.get('dark', 'dark_wsl_appearance_command')

            # 写入配置文件
            with open(self.config_file, 'w', encoding='utf-8') as f:
                # [General] section
                f.write('[General]\n')
                f.write(f'theme = {self.theme}\n')
                f.write(f'case_path = {self.case_path}\n')
                f.write(f'msh_path = {self.msh_path}\n')
                f.write(f'gmsh_path = {self.gmsh_exe_path}\n')
                f.write(f'openfoam_env_source = {self.openfoam_env_source}\n')
                f.write(f'wsl_bashrc_path = {self.wsl_bashrc_path}\n')
                f.write(f'wsl_base = {self.wsl_base}\n')
                f.write('\n')

                # [light] section - 使用保存的值或默认值
                f.write('[light]\n')
                f.write(f'light_wsl_treefoam_command = {light_commands.get("light_wsl_treefoam_command", self.light_wsl_treefoam_command)}\n')
                f.write(f'light_wsl_files_command = {light_commands.get("light_wsl_files_command", self.light_wsl_files_command)}\n')
                f.write(f'light_wsl_disk_analysis_command = {light_commands.get("light_wsl_disk_analysis_command", self.light_wsl_disk_analysis_command)}\n')
                f.write(f'light_wsl_appearance_command = {light_commands.get("light_wsl_appearance_command", self.light_wsl_appearance_command)}\n')
                f.write('\n')

                # [dark] section - 使用保存的值或默认值
                f.write('[dark]\n')
                f.write(f'dark_wsl_treefoam_command = {dark_commands.get("dark_wsl_treefoam_command", self.dark_wsl_treefoam_command)}\n')
                f.write(f'dark_wsl_files_command = {dark_commands.get("dark_wsl_files_command", self.dark_wsl_files_command)}\n')
                f.write(f'dark_wsl_disk_analysis_command = {dark_commands.get("dark_wsl_disk_analysis_command", self.dark_wsl_disk_analysis_command)}\n')
                f.write(f'dark_wsl_appearance_command = {dark_commands.get("dark_wsl_appearance_command", self.dark_wsl_appearance_command)}\n')
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

        根据当前主题从配置文件读取对应的命令配置。
        如果该主题下没有配置，则使用默认值。
        返回的命令会自动添加 wsl_base 前缀。

        Returns:
            str: WSL Files 命令
        """
        command_suffix = ""
        try:
            if self.config.has_section(self.theme):
                if self.theme == 'light':
                    option_name = 'light_wsl_files_command'
                else:
                    option_name = 'dark_wsl_files_command'

                if self.config.has_option(self.theme, option_name):
                    value = self.config.get(self.theme, option_name)
                    if value:
                        command_suffix = value
        except Exception as e:
            print(f"读取 WSL Files 命令失败: {e}")

        # 如果没有找到配置，使用默认值
        if not command_suffix:
            if self.theme == 'light':
                command_suffix = self.light_wsl_files_command
            else:
                command_suffix = self.dark_wsl_files_command

        # 返回完整的命令（wsl_base + 命令后缀）
        return f'{self.wsl_base} {command_suffix}'

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

        根据当前主题从配置文件读取对应的命令配置。
        如果该主题下没有配置，则使用默认值。
        返回的命令会自动添加 wsl_base 前缀。

        Returns:
            str: WSL Disk Analysis 命令
        """
        command_suffix = ""
        try:
            if self.config.has_section(self.theme):
                if self.theme == 'light':
                    option_name = 'light_wsl_disk_analysis_command'
                else:
                    option_name = 'dark_wsl_disk_analysis_command'

                if self.config.has_option(self.theme, option_name):
                    value = self.config.get(self.theme, option_name)
                    if value:
                        command_suffix = value
        except Exception as e:
            print(f"读取 WSL Disk Analysis 命令失败: {e}")

        # 如果没有找到配置，使用默认值
        if not command_suffix:
            if self.theme == 'light':
                command_suffix = self.light_wsl_disk_analysis_command
            else:
                command_suffix = self.dark_wsl_disk_analysis_command

        # 返回完整的命令（wsl_base + 命令后缀）
        return f'{self.wsl_base} {command_suffix}'

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

        根据当前主题从配置文件读取对应的命令配置。
        如果该主题下没有配置，则使用默认值。
        返回的命令会自动添加 wsl_base 前缀。

        Returns:
            str: WSL Appearance 命令
        """
        command_suffix = ""
        try:
            if self.config.has_section(self.theme):
                if self.theme == 'light':
                    option_name = 'light_wsl_appearance_command'
                else:
                    option_name = 'dark_wsl_appearance_command'

                if self.config.has_option(self.theme, option_name):
                    value = self.config.get(self.theme, option_name)
                    if value:
                        command_suffix = value
        except Exception as e:
            print(f"读取 WSL Appearance 命令失败: {e}")

        # 如果没有找到配置，使用默认值
        if not command_suffix:
            if self.theme == 'light':
                command_suffix = self.light_wsl_appearance_command
            else:
                command_suffix = self.dark_wsl_appearance_command

        # 返回完整的命令（wsl_base + 命令后缀）
        return f'{self.wsl_base} {command_suffix}'

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