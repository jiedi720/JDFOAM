"""配置管理模块"""
import os
import configparser


class ConfigManager:
    """配置管理器"""

    def __init__(self, config_file="JDFOAM.ini"):
        # 获取项目根目录（function 目录的父目录）
        self.root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.config_file = os.path.join(self.root_dir, config_file)
        # 使用 RawConfigParser 来正确处理包含引号的值
        self.config = configparser.RawConfigParser()
        self.gmsh_exe_path = ""
        self.treefoam_command = ""
        self.wkhtmltopdf_path = ""
        self.theme = "light"  # 默认主题
        self.openfoam_env_source = "source /usr/lib/openfoam/openfoam2506/etc/bashrc"

    def load_config(self):
        """加载配置文件"""
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
        except Exception as e:
            print(f"加载配置文件失败: {e}")
            self.gmsh_exe_path = ""
            self.treefoam_command = ""
            self.wkhtmltopdf_path = ""

    def save_config(self):
        """保存配置文件"""
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
        """获取Gmsh路径"""
        return self.gmsh_exe_path

    def set_gmsh_path(self, path):
        """设置Gmsh路径"""
        self.gmsh_exe_path = path
        self.save_config()

    def get_treefoam_command(self):
        """获取TreeFOAM命令"""
        return self.treefoam_command

    def set_treefoam_command(self, command):
        """设置TreeFOAM命令"""
        self.treefoam_command = command
        self.save_all_config()

    def get_theme(self):
        """获取当前主题"""
        return self.theme

    def set_theme(self, theme):
        """设置主题"""
        self.theme = theme
        self.save_all_config()

    def save_all_config(self):
        """保存所有配置"""
        if not self.config.has_section('General'):
            self.config.add_section('General')
        self.config.set('General', 'gmsh_path', self.gmsh_exe_path)
        self.config.set('General', 'openfoam_env_source', self.openfoam_env_source)
        self.config.set('General', 'treefoam_command', self.treefoam_command)
        self.config.set('General', 'theme', self.theme)
        
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                self.config.write(f)
        except Exception as e:
            print(f"保存配置文件失败: {e}")

    def get_wkhtmltopdf_path(self):
        """获取wkhtmltopdf路径"""
        return self.wkhtmltopdf_path

    def set_wkhtmltopdf_path(self, path):
        """设置wkhtmltopdf路径"""
        self.wkhtmltopdf_path = path
        self.save_config()
    
    def get_openfoam_env_source(self):
        """获取OpenFOAM环境源路径"""
        return self.openfoam_env_source

    def set_openfoam_env_source(self, env_source):
        """设置OpenFOAM环境源路径"""
        self.openfoam_env_source = env_source
        self.save_all_config()