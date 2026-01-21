"""主题管理模块

该模块提供应用程序的主题管理功能，支持浅色和深色两种主题模式，
通过调色板和样式表实现界面元素的颜色和外观定制。
功能包括：
- 浅色/深色主题切换
- 界面元素颜色统一管理
- 按钮样式动态调整
- 主题状态持久化保存
- Windows 标题栏主题切换
"""

import sys
from PySide6.QtWidgets import QApplication, QStyleFactory
from PySide6.QtGui import QColor, QPalette, QFont
from PySide6.QtCore import Qt

# Windows 标题栏主题支持
if sys.platform == "win32":
    try:
        import ctypes
        from ctypes import wintypes

        # 定义 Windows API 常量和结构体
        # DWMWA_ATTRIBUTE 枚举
        DWMWA_USE_IMMERSIVE_DARK_MODE = 20
        DWMWA_MICA_EFFECT = 1029

        # 定义 DwmSetWindowAttribute 函数原型
        dwmapi = ctypes.windll.dwmapi
        dwmapi.DwmSetWindowAttribute.restype = ctypes.HRESULT
        dwmapi.DwmSetWindowAttribute.argtypes = [
            wintypes.HWND,  # hwnd
            ctypes.c_ulong,  # dwAttribute
            ctypes.c_void_p,  # pvAttribute
            ctypes.c_ulong  # cbAttribute
        ]

        # 定义 DwmExtendFrameIntoClientArea 函数原型
        dwmapi.DwmExtendFrameIntoClientArea.restype = ctypes.HRESULT
        dwmapi.DwmExtendFrameIntoClientArea.argtypes = [
            wintypes.HWND,  # hwnd
            ctypes.c_void_p  # pMarInset
        ]

        # MARGINS 结构体
        class MARGINS(ctypes.Structure):
            _fields_ = [
                ("cxLeftWidth", ctypes.c_int),
                ("cxRightWidth", ctypes.c_int),
                ("cyTopHeight", ctypes.c_int),
                ("cyBottomHeight", ctypes.c_int),
            ]

        WINDOWS_API_AVAILABLE = True
    except (ImportError, AttributeError):
        WINDOWS_API_AVAILABLE = False
else:
    WINDOWS_API_AVAILABLE = False


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

    def set_windows_titlebar_theme(self, theme):
        """
        设置 Windows 标题栏主题

        在 Windows 10/11 上使用 DWM API 设置标题栏的深色/浅色模式

        Args:
            theme (str): 主题名称，"light" 或 "dark"
        """
        if not WINDOWS_API_AVAILABLE or sys.platform != "win32":
            return  # 非 Windows 平台或 API 不可用

        try:
            # 获取窗口句柄
            hwnd = int(self.parent.winId())

            # 设置深色模式 (Windows 10/11)
            use_dark_mode = 1 if theme == "dark" else 0

            # 方法1：使用 DWMWA_USE_IMMERSIVE_DARK_MODE (Windows 10 1803+)
            try:
                result = dwmapi.DwmSetWindowAttribute(
                    hwnd,
                    DWMWA_USE_IMMERSIVE_DARK_MODE,
                    ctypes.byref(ctypes.c_int(use_dark_mode)),
                    ctypes.sizeof(ctypes.c_int)
                )
                if result == 0:  # S_OK
                    print(f"标题栏主题设置成功: {theme}")
                else:
                    print(f"标题栏主题设置失败，错误码: {result}")
            except Exception as e:
                print(f"设置 DWMWA_USE_IMMERSIVE_DARK_MODE 失败: {e}")

            # 方法2：使用 DWMWA_WINDOW_CORNER_PREFERENCE (Windows 11)
            try:
                DWMWA_WINDOW_CORNER_PREFERENCE = 33
                corner_preference = 2  # DWMWCP_ROUND
                dwmapi.DwmSetWindowAttribute(
                    hwnd,
                    DWMWA_WINDOW_CORNER_PREFERENCE,
                    ctypes.byref(ctypes.c_int(corner_preference)),
                    ctypes.sizeof(ctypes.c_int)
                )
            except Exception:
                pass

            # 方法3：使用 DWMWA_BORDER_COLOR (设置边框颜色)
            try:
                DWMWA_BORDER_COLOR = 34
                if theme == "dark":
                    # 深色边框
                    border_color = 0x202020  # 深灰色
                else:
                    # 浅色边框
                    border_color = 0x000000  # 黑色

                dwmapi.DwmSetWindowAttribute(
                    hwnd,
                    DWMWA_BORDER_COLOR,
                    ctypes.byref(ctypes.c_int(border_color)),
                    ctypes.sizeof(ctypes.c_int)
                )
            except Exception:
                pass

            # 方法4：使用 DWMWA_CAPTION_COLOR (设置标题栏背景色)
            try:
                DWMWA_CAPTION_COLOR = 35
                if theme == "dark":
                    # 深色标题栏
                    caption_color = 0x202020  # 深灰色
                else:
                    # 浅色标题栏
                    caption_color = 0xFFFFFF  # 白色

                dwmapi.DwmSetWindowAttribute(
                    hwnd,
                    DWMWA_CAPTION_COLOR,
                    ctypes.byref(ctypes.c_int(caption_color)),
                    ctypes.sizeof(ctypes.c_int)
                )
            except Exception:
                pass

            # 方法5：使用 DWMWA_TEXT_COLOR (设置标题栏文本颜色)
            try:
                DWMWA_TEXT_COLOR = 36
                if theme == "dark":
                    # 深色模式文本为白色
                    text_color = 0xFFFFFF
                else:
                    # 浅色模式文本为黑色
                    text_color = 0x000000

                dwmapi.DwmSetWindowAttribute(
                    hwnd,
                    DWMWA_TEXT_COLOR,
                    ctypes.byref(ctypes.c_int(text_color)),
                    ctypes.sizeof(ctypes.c_int)
                )
            except Exception:
                pass

            # 强制刷新窗口
            self.parent.update()
            self.parent.repaint()

        except Exception as e:
            print(f"设置 Windows 标题栏主题时出错: {e}")

    def init_menu(self):
        """初始化主题菜单

        设置主题切换菜单项的属性和信号连接
        """
        # 使用 UI 中定义的动作
        light_action = self.parent.action_light_theme  # 浅色主题菜单项
        dark_action = self.parent.action_dark_theme    # 深色主题菜单项

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

        # 更新按钮图标颜色
        self.update_button_icons(theme)

        # 重新应用进度条样式
        if hasattr(self.parent, 'progressbar_manager'):
            self.parent.progressbar_manager.apply_progress_bar_style()

        # 最后再次刷新，确保图标颜色更新生效
        app.processEvents()
        for widget in QApplication.allWidgets():
            widget.update()

        # 延迟设置 Windows 标题栏主题，确保窗口完全显示后再设置
        # 使用 QTimer 单次触发，延迟 100ms 后设置标题栏主题
        from PySide6.QtCore import QTimer
        QTimer.singleShot(100, lambda: self.set_windows_titlebar_theme(theme))

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

        # 设置菜单栏样式
        self.apply_menu_style(theme)

    def apply_menu_style(self, theme):
        """
        应用菜单栏样式

        根据主题设置菜单栏和菜单项的样式，使用 VS Code 蓝色作为选中背景色

        Args:
            theme (str): 当前主题，"light" 或 "dark"
        """
        if theme == "dark":
            # Dark 模式菜单样式
            menu_style = """
QMenuBar {
    background-color: #3D3D3D;
    color: white;
    border-bottom: 1px solid #555555;
    font-size: 10pt;
}
QMenuBar::item {
    background-color: transparent;
    padding: 5px 10px;
    font-size: 10pt;
}
QMenuBar::item:selected {
    background-color: #007ACC;  /* VS Code 蓝色 */
    color: white;
}
QMenu {
    background-color: #3D3D3D;
    color: white;
    border: 1px solid #555555;
    font-size: 10pt;
}
QMenu::item {
    padding: 5px 30px 5px 20px;
    font-size: 10pt;
}
QMenu::item:selected {
    background-color: #007ACC;  /* VS Code 蓝色 */
    color: white;
}
QMenu::separator {
    height: 2px;
    background-color: #555555;
    margin: 4px 8px;
}
"""
        else:
            # Light 模式菜单样式
            menu_style = """
QMenuBar {
    background-color: #F0F0F0;
    color: black;
    border-bottom: 1px solid #BDBDBD;
    font-size: 10pt;
}
QMenuBar::item {
    background-color: transparent;
    padding: 5px 10px;
    font-size: 10pt;
}
QMenuBar::item:selected {
    background-color: #007ACC;  /* VS Code 蓝色 */
    color: white;
}
QMenu {
    background-color: white;
    color: black;
    border: 1px solid #BDBDBD;
    font-size: 10pt;
}
QMenu::item {
    padding: 5px 30px 5px 20px;
    font-size: 10pt;
}
QMenu::item:selected {
    background-color: #007ACC;  /* VS Code 蓝色 */
    color: white;
}
QMenu::separator {
    height: 2px;
    background-color: #BDBDBD;
    margin: 4px 8px;
}
"""

        # 应用样式到菜单栏
        if hasattr(self.parent, 'menubar'):
            self.parent.menubar.setStyleSheet(menu_style)