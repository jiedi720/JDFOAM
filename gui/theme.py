"""主题管理模块

该模块提供应用程序的主题管理功能，支持浅色和深色两种主题模式，
通过调色板和样式表实现界面元素的颜色和外观定制。
功能包括：
- 浅色/深色主题切换
- 界面元素颜色统一管理
- 按钮样式动态调整
- 主题状态持久化保存
"""

from PySide6.QtWidgets import QApplication, QStyleFactory
from PySide6.QtGui import QColor, QPalette, QFont
from PySide6.QtCore import Qt


class ThemeManager:
    """主题管理器

    管理应用程序的视觉主题，包括颜色方案、字体设置和界面元素样式，
    提供浅色和深色两种主题模式的切换功能。
    """

    def __init__(self, parent_window):
        """
        初始化主题管理器

        Args:
            parent_window: 父窗口对象，用于访问界面组件
        """
        self.parent = parent_window      # 父窗口引用
        self.current_theme = "light"     # 当前主题，默认为浅色
        self._original_style = None      # 保存原始样式名称

    def init_menu(self):
        """初始化主题菜单

        设置主题切换菜单项的属性和信号连接
        """
        # 使用 UI 中定义的动作
        light_action = self.parent.action_light_theme  # 浅色主题菜单项
        dark_action = self.parent.action_dark_theme    # 深色主题菜单项

        # 设置为可选择
        light_action.setCheckable(True)
        dark_action.setCheckable(True)

        # 连接信号到主题切换方法
        light_action.triggered.connect(lambda: self.set_theme("light"))
        dark_action.triggered.connect(lambda: self.set_theme("dark"))

    def set_theme(self, theme):
        """
        设置应用程序主题

        切换到指定主题并保存设置到配置文件

        Args:
            theme (str): 主题名称，"light" 或 "dark"
        """
        if self.current_theme == theme:
            return  # 主题未变化，直接返回

        self.current_theme = theme  # 更新当前主题

        # 更新菜单项状态，显示当前选中的主题
        self.parent.action_light_theme.setChecked(theme == "light")
        self.parent.action_dark_theme.setChecked(theme == "dark")

        # 应用新主题
        self.apply_theme(theme)

        # 保存主题到配置文件
        self.parent.config_manager.set_theme(theme)

    def apply_theme(self, theme):
        """
        应用主题样式到整个应用程序

        根据指定主题设置应用程序的调色板和样式

        Args:
            theme (str): 主题名称，"light" 或 "dark"
        """
        # 获取当前运行的QApplication实例
        app = QApplication.instance()

        # 首次调用时保存原始样式名称
        if self._original_style is None:
            self._original_style = app.style().objectName()

        if theme == "light":
            # 浅色主题 - 使用 Fusion 样式，与 dark 模式保持一致的渲染
            app.setStyle("Fusion")

            # 创建浅色调色板
            palette = QPalette()
            palette.setColor(QPalette.ColorRole.Window, QColor(240, 240, 240))          # 窗口背景色
            palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.black)        # 窗口文本色
            palette.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255))            # 基础背景色
            palette.setColor(QPalette.ColorRole.AlternateBase, QColor(245, 245, 245))   # 交替背景色
            palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 220))     # 工具提示背景色
            palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.black)       # 工具提示文本色
            palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.black)              # 文本色
            palette.setColor(QPalette.ColorRole.Button, QColor(240, 240, 240))          # 按钮背景色
            palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.black)        # 按钮文本色
            palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)          # 高亮文本色
            palette.setColor(QPalette.ColorRole.Link, QColor(0, 0, 255))                # 链接色
            palette.setColor(QPalette.ColorRole.Highlight, QColor(0, 120, 215))         # 选中背景色
            palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.white)   # 选中文本色

            app.setPalette(palette)

            # 设置统一的字体，确保与 dark 模式一致
            font = app.font()
            font.setPointSize(10)  # 与 UI 文件中的字体大小一致
            app.setFont(font)
        elif theme == "dark":
            # 深色主题 - 使用Fusion样式作为基础
            app.setStyle("Fusion")

            # 创建深色调色板
            palette = QPalette()
            palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))             # 窗口背景色：深灰色
            palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)        # 窗口文本色：白色
            palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))               # 基础背景色：更深灰色
            palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))      # 交替背景色：深灰色
            palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(53, 53, 53))        # 工具提示背景色：深灰色
            palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)       # 工具提示文本色：白色
            palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)              # 文本色：白色
            palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))             # 按钮背景色：深灰色
            palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)        # 按钮文本色：白色
            palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)          # 高亮文本色：红色
            palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))             # 链接色：蓝色
            palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))        # 选中背景色：蓝色
            palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)   # 选中文本色：黑色
            palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(150, 150, 150))  # 占位符文本色：浅灰色

            # 应用调色板到应用程序
            app.setPalette(palette)

        # 强制刷新所有控件，确保主题更改立即生效
        # 使用多次刷新确保样式完全更新
        app.processEvents()
        for widget in QApplication.allWidgets():
            widget.style().unpolish(widget)  # 取消现有样式
            widget.style().polish(widget)    # 应用新样式
            widget.update()                  # 更新界面

        # 再次处理事件，确保所有更新都完成
        app.processEvents()

        # 为菜单项设置统一的字体，确保两种模式下字体一致
        menu_font = QFont()
        menu_font.setHintingPreference(QFont.PreferNoHinting)
        menu_font.setPointSize(10)  # 统一字体大小
        self.parent.action_light_theme.setFont(menu_font)
        self.parent.action_dark_theme.setFont(menu_font)

        # 更新按钮图标颜色
        self.update_button_icons(theme)

        # 重新应用进度条样式
        if hasattr(self.parent, 'progressbar_manager'):
            self.parent.progressbar_manager.apply_progress_bar_style()

        # 最后再次刷新，确保图标颜色更新生效
        app.processEvents()
        for widget in QApplication.allWidgets():
            widget.update()

    def update_button_icons(self, theme):
        """
        更新按钮图标颜色

        根据当前主题调整图标按钮的背景色和边框样式

        Args:
            theme (str): 当前主题，"light" 或 "dark"
        """
        # 更新所有使用本地图标的按钮
        # 这些按钮现在使用本地图片文件（search.png、open-folder.png）
        # 本地图片的颜色是固定的，不会跟随主题变化
        # 我们只需要设置背景色和边框，不设置 color 属性
        icon_buttons = [
            self.parent.case_browse_btn,   # search.png
            self.parent.msh_browse_btn,    # search.png
            self.parent.case_open_btn,     # open-folder.png
            self.parent.msh_open_btn,      # open-folder.png
            self.parent.treefoam_btn,      # TreeFoam.png
            self.parent.gmsh_btn,          # gmsh.ico
        ]

        for btn in icon_buttons:
            if btn:
                if theme == "dark":
                    # 深色主题：设置深灰色背景
                    new_style = """
QPushButton {
    background-color: #3D3D3D;
    border: 1px solid #555555;
    border-radius: 6px;
    padding: 5px 10px;
    font-size: 10pt;
}
QPushButton:hover {
    background-color: #4D4D4D;
}
QPushButton:pressed {
    background-color: #2D2D2D;
    padding-top: 3px;
}
"""
                else:
                    # 浅色主题：设置浅灰色背景
                    new_style = """
QPushButton {
    background-color: #E0E0E0;
    border: 1px solid #BDBDBD;
    border-radius: 6px;
    padding: 5px 10px;
    font-size: 10pt;
}
QPushButton:hover {
    background-color: #D0D0D0;
}
QPushButton:pressed {
    background-color: #C0C0C0;
    padding-top: 3px;
}
"""

                btn.setStyleSheet(new_style)  # 应用新样式
                # 强制刷新按钮样式
                btn.style().unpolish(btn)  # 取消现有样式
                btn.style().polish(btn)    # 应用新样式
                btn.update()               # 更新界面

        # 刷新主窗口样式
        self.parent.style().unpolish(self.parent)  # 取消现有样式
        self.parent.style().polish(self.parent)    # 应用新样式
        self.parent.update()                       # 更新界面