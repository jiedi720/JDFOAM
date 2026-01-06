"""进度条管理模块

该模块提供对 GUI 进度条的统一管理功能，包括样式设置、进度更新、
显示/隐藏控制等，确保用户界面的进度反馈一致性和可用性。
功能包括：
- 进度条样式统一管理
- 进度值更新
- 进度条显示/隐藏控制
- UI 事件循环处理
"""

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont


class ProgressBarManager:
    """进度条管理器

    管理 GUI 界面中的进度条组件，提供统一的接口进行样式设置、
    进度更新和显示控制，确保在各种操作中为用户提供清晰的进度反馈。
    """

    # 进度条样式定义
    # 使用青蓝色渐变设计，提供现代化的视觉效果
    PROGRESS_BAR_STYLE = """
        QProgressBar {
            border: none;
            color: white;
            text-align: center;
            background: #e0e0e0;
            border-radius: 5px;
            height: 10px;
        }
        QProgressBar::chunk {
            background-color: #05B8CC;
            border-radius: 5px;
        }
    """

    def __init__(self, parent_window):
        """
        初始化进度条管理器

        Args:
            parent_window: 父窗口对象，包含进度条组件
        """
        self.parent = parent_window  # 父窗口引用

    def init_progress_bar(self):
        """初始化进度条

        设置进度条的初始状态，包括进度值为0、应用样式等
        """
        if hasattr(self.parent, 'progress_bar'):
            self.parent.progress_bar.setValue(0)  # 设置初始进度为0
            # 应用进度条样式
            self.apply_progress_bar_style()
            # 不隐藏进度条，让它始终可见
            print("进度条已初始化")
            print("进度条可见性:", self.parent.progress_bar.isVisible())
            print("进度条大小:", self.parent.progress_bar.size())
            print("进度条位置:", self.parent.progress_bar.pos())
        else:
            print("警告: progress_bar 未创建")

    def show_progress_bar(self):
        """显示进度条并重置

        显示进度条组件并将进度值重置为0，准备开始新的进度跟踪
        """
        if hasattr(self.parent, 'progress_bar'):
            self.parent.progress_bar.show()  # 显示进度条
            self.parent.progress_bar.setValue(0)  # 重置进度值
            self.parent.progress_bar.update()  # 更新界面
            self.parent.progress_bar.repaint()  # 重绘界面
            # 强制应用样式
            self.apply_progress_bar_style()
            print("进度条已显示，当前值:", self.parent.progress_bar.value())
            print("进度条可见性:", self.parent.progress_bar.isVisible())
            print("进度条大小:", self.parent.progress_bar.size())

    def hide_progress_bar(self):
        """隐藏进度条

        隐藏进度条组件，通常在操作完成后调用
        """
        if hasattr(self.parent, 'progress_bar'):
            self.parent.progress_bar.hide()

    def update_progress(self, value):
        """更新进度条值

        更新进度条的显示值，提供实时的进度反馈

        Args:
            value (int): 进度值，范围 0-100
        """
        if hasattr(self.parent, 'progress_bar'):
            print(f"更新进度: {value}%")
            self.parent.progress_bar.setValue(value)  # 设置进度值
            self.parent.progress_bar.update()  # 更新界面
            self.parent.progress_bar.repaint()  # 重绘界面
        else:
            print("警告: progress_bar 不存在，无法更新进度")

    def apply_progress_bar_style(self):
        """应用进度条样式

        为进度条组件应用预定义的样式，确保视觉效果的一致性
        """
        if hasattr(self.parent, 'progress_bar'):
            self.parent.progress_bar.setStyleSheet(self.PROGRESS_BAR_STYLE)
            self.parent.progress_bar.update()

    def process_events(self):
        """处理事件循环，让UI有机会更新

        处理 Qt 事件循环，确保界面能够及时响应和更新，
        避免在长时间操作中界面冻结
        """
        QApplication.processEvents()