"""主题管理模块"""
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QColor, QPalette
from PySide6.QtCore import Qt


class ThemeManager:
    """主题管理器"""

    def __init__(self, parent_window):
        self.parent = parent_window
        self.current_theme = "light"
        self._original_style = None

    def init_menu(self):
        """初始化主题菜单"""
        # 使用 UI 中定义的动作
        light_action = self.parent.action_light_theme
        dark_action = self.parent.action_dark_theme

        # 设置为可选择
        light_action.setCheckable(True)
        dark_action.setCheckable(True)

        # 连接信号
        light_action.triggered.connect(lambda: self.set_theme("light"))
        dark_action.triggered.connect(lambda: self.set_theme("dark"))

    def set_theme(self, theme):
        """设置主题"""
        if self.current_theme == theme:
            return

        self.current_theme = theme

        # 更新菜单项状态
        self.parent.action_light_theme.setChecked(theme == "light")
        self.parent.action_dark_theme.setChecked(theme == "dark")

        # 应用主题
        self.apply_theme(theme)
        
        # 保存主题到配置文件
        self.parent.config_manager.set_theme(theme)

    def apply_theme(self, theme):
        """应用主题样式"""
        # 获取当前运行的QApplication实例
        app = QApplication.instance()
        
        # 首次调用时保存原始样式名称
        if self._original_style is None:
            self._original_style = app.style().objectName()
        
        # 创建全新的调色板
        palette = QPalette()
        
        if theme == "light":
            # 浅色主题 - 恢复系统默认样式
            if self._original_style and self._original_style != "Fusion":
                app.setStyle(self._original_style)
            else:
                app.setStyle("WindowsVista")  # 使用 Windows 默认样式
            
            # 清除调色板，使用系统默认
            app.setPalette(app.style().standardPalette())
        elif theme == "dark":
            # 深色主题 - 使用Fusion样式作为基础
            app.setStyle("Fusion")
            
            # 设置深色主题的各种颜色
            palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
            palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
            palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
            palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
            palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(53, 53, 53))
            palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
            palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
            palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
            palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
            palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
            palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
            palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
            palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)
            
            app.setPalette(palette)
        
        # 强制刷新所有控件，确保主题更改立即生效
        app.processEvents()
        for widget in QApplication.allWidgets():
            widget.style().unpolish(widget)
            widget.style().polish(widget)
            widget.update()
        
        # 更新按钮图标颜色
        self.update_button_icons(theme)
    
    def update_button_icons(self, theme):
        """更新按钮图标颜色"""
        # 为 combine_pdf_btn 设置固定的深灰色文字颜色，使其在两种主题下保持一致
        if self.parent.combine_pdf_btn:
            self.parent.combine_pdf_btn.setStyleSheet(
                self.parent.combine_pdf_btn.styleSheet() + 
                "QPushButton { color: #333333 !important; }"
            )