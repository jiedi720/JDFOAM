# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'JDFOAMCFTXlR.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLabel,
    QLineEdit, QMainWindow, QMenu, QMenuBar,
    QPlainTextEdit, QProgressBar, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_JDFOAM_GUI(object):
    def setupUi(self, JDFOAM_GUI):
        if not JDFOAM_GUI.objectName():
            JDFOAM_GUI.setObjectName(u"JDFOAM_GUI")
        JDFOAM_GUI.resize(630, 600)
        JDFOAM_GUI.setMinimumSize(QSize(630, 600))
        JDFOAM_GUI.setMaximumSize(QSize(630, 600))
        self.action_light_theme = QAction(JDFOAM_GUI)
        self.action_light_theme.setObjectName(u"action_light_theme")
        font = QFont()
        font.setHintingPreference(QFont.PreferNoHinting)
        self.action_light_theme.setFont(font)
        self.action_dark_theme = QAction(JDFOAM_GUI)
        self.action_dark_theme.setObjectName(u"action_dark_theme")
        self.action_dark_theme.setFont(font)
        self.centralwidget = QWidget(JDFOAM_GUI)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(10, 5, 10, 10)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.case_label = QLabel(self.centralwidget)
        self.case_label.setObjectName(u"case_label")
        font1 = QFont()
        font1.setPointSize(10)
        font1.setHintingPreference(QFont.PreferNoHinting)
        self.case_label.setFont(font1)
        self.case_label.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.case_label, 0, 0, 1, 1)

        self.case_path_edit = QLineEdit(self.centralwidget)
        self.case_path_edit.setObjectName(u"case_path_edit")
        self.case_path_edit.setMinimumSize(QSize(0, 30))
        self.case_path_edit.setStyleSheet(u"border-radius: 6px;")

        self.gridLayout_2.addWidget(self.case_path_edit, 0, 1, 1, 1)

        self.msh_label = QLabel(self.centralwidget)
        self.msh_label.setObjectName(u"msh_label")
        self.msh_label.setFont(font1)

        self.gridLayout_2.addWidget(self.msh_label, 1, 0, 1, 1)

        self.msh_path_edit = QLineEdit(self.centralwidget)
        self.msh_path_edit.setObjectName(u"msh_path_edit")
        self.msh_path_edit.setMinimumSize(QSize(0, 30))
        self.msh_path_edit.setStyleSheet(u"border-radius: 6px;")

        self.gridLayout_2.addWidget(self.msh_path_edit, 1, 1, 1, 1)


        self.horizontalLayout.addLayout(self.gridLayout_2)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(5)
        self.case_browse_btn = QPushButton(self.centralwidget)
        self.case_browse_btn.setObjectName(u"case_browse_btn")
        self.case_browse_btn.setMinimumSize(QSize(30, 30))
        self.case_browse_btn.setMaximumSize(QSize(30, 30))
        self.case_browse_btn.setStyleSheet(u"/* \u6309\u94ae\u9ed8\u8ba4\u6837\u5f0f */\n"
"QPushButton {\n"
"    border-radius: 6px;\n"
"    border: 1px solid rgb(160, 160, 160); \n"
"}\n"
"\n"
"/* \u60ac\u6d6e\u7279\u6548\uff1a\u80cc\u666f\u989c\u8272\u53d8\u6d45\uff0c\u5e76\u589e\u52a0\u84dd\u8272\u8fb9\u6846\u611f */\n"
"QPushButton:hover {\n"
"    background-color: rgb(160, 160, 160); /* \u989c\u8272\u6bd4\u9ed8\u8ba4\u7a0d\u4eae */\n"
"}\n"
"\n"
"/* \u6309\u4e0b\u7279\u6548\uff1a\u70b9\u51fb\u65f6\u989c\u8272\u53d8\u6df1\uff0c\u4ea7\u751f\u7269\u7406\u538b\u4e0b\u7684\u9519\u89c9 */\n"
"QPushButton:pressed {\n"
"    padding-top: 3px;\n"
"}\n"
"")
        icon = QIcon()
        icon.addFile(u"../JDFOAM/resources/search.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.case_browse_btn.setIcon(icon)
        self.case_browse_btn.setIconSize(QSize(20, 20))

        self.gridLayout.addWidget(self.case_browse_btn, 0, 0, 1, 1)

        self.case_open_btn = QPushButton(self.centralwidget)
        self.case_open_btn.setObjectName(u"case_open_btn")
        self.case_open_btn.setMinimumSize(QSize(30, 30))
        self.case_open_btn.setMaximumSize(QSize(30, 30))
        self.case_open_btn.setStyleSheet(u"/* \u6309\u94ae\u9ed8\u8ba4\u6837\u5f0f */\n"
"QPushButton {\n"
"    border-radius: 6px;\n"
"    border: 1px solid rgb(160, 160, 160); \n"
"}\n"
"\n"
"/* \u60ac\u6d6e\u7279\u6548\uff1a\u80cc\u666f\u989c\u8272\u53d8\u6d45\uff0c\u5e76\u589e\u52a0\u84dd\u8272\u8fb9\u6846\u611f */\n"
"QPushButton:hover {\n"
"    background-color: rgb(160, 160, 160); /* \u989c\u8272\u6bd4\u9ed8\u8ba4\u7a0d\u4eae */\n"
"}\n"
"\n"
"/* \u6309\u4e0b\u7279\u6548\uff1a\u70b9\u51fb\u65f6\u989c\u8272\u53d8\u6df1\uff0c\u4ea7\u751f\u7269\u7406\u538b\u4e0b\u7684\u9519\u89c9 */\n"
"QPushButton:pressed {\n"
"    padding-top: 3px;\n"
"}\n"
"")
        icon1 = QIcon()
        icon1.addFile(u"../JDFOAM/resources/open-folder.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.case_open_btn.setIcon(icon1)
        self.case_open_btn.setIconSize(QSize(22, 22))

        self.gridLayout.addWidget(self.case_open_btn, 0, 1, 1, 1)

        self.treefoam_btn = QPushButton(self.centralwidget)
        self.treefoam_btn.setObjectName(u"treefoam_btn")
        self.treefoam_btn.setMinimumSize(QSize(30, 30))
        self.treefoam_btn.setMaximumSize(QSize(30, 30))
        self.treefoam_btn.setStyleSheet(u"/* \u6309\u94ae\u9ed8\u8ba4\u6837\u5f0f */\n"
"QPushButton {\n"
"    border-radius: 6px;\n"
"    border: 1px solid rgb(160, 160, 160); \n"
"}\n"
"\n"
"/* \u60ac\u6d6e\u7279\u6548\uff1a\u80cc\u666f\u989c\u8272\u53d8\u6d45\uff0c\u5e76\u589e\u52a0\u84dd\u8272\u8fb9\u6846\u611f */\n"
"QPushButton:hover {\n"
"    background-color: rgb(160, 160, 160); /* \u989c\u8272\u6bd4\u9ed8\u8ba4\u7a0d\u4eae */\n"
"}\n"
"\n"
"/* \u6309\u4e0b\u7279\u6548\uff1a\u70b9\u51fb\u65f6\u989c\u8272\u53d8\u6df1\uff0c\u4ea7\u751f\u7269\u7406\u538b\u4e0b\u7684\u9519\u89c9 */\n"
"QPushButton:pressed {\n"
"    padding-top: 3px;\n"
"}\n"
"")
        icon2 = QIcon()
        icon2.addFile(u"../JDFOAM/resources/TreeFoam.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.treefoam_btn.setIcon(icon2)
        self.treefoam_btn.setIconSize(QSize(23, 23))

        self.gridLayout.addWidget(self.treefoam_btn, 0, 2, 1, 1)

        self.msh_browse_btn = QPushButton(self.centralwidget)
        self.msh_browse_btn.setObjectName(u"msh_browse_btn")
        self.msh_browse_btn.setMinimumSize(QSize(30, 30))
        self.msh_browse_btn.setMaximumSize(QSize(30, 30))
        self.msh_browse_btn.setStyleSheet(u"/* \u6309\u94ae\u9ed8\u8ba4\u6837\u5f0f */\n"
"QPushButton {\n"
"    border-radius: 6px;\n"
"    border: 1px solid rgb(160, 160, 160); \n"
"}\n"
"\n"
"/* \u60ac\u6d6e\u7279\u6548\uff1a\u80cc\u666f\u989c\u8272\u53d8\u6d45\uff0c\u5e76\u589e\u52a0\u84dd\u8272\u8fb9\u6846\u611f */\n"
"QPushButton:hover {\n"
"    background-color: rgb(160, 160, 160); /* \u989c\u8272\u6bd4\u9ed8\u8ba4\u7a0d\u4eae */\n"
"}\n"
"\n"
"/* \u6309\u4e0b\u7279\u6548\uff1a\u70b9\u51fb\u65f6\u989c\u8272\u53d8\u6df1\uff0c\u4ea7\u751f\u7269\u7406\u538b\u4e0b\u7684\u9519\u89c9 */\n"
"QPushButton:pressed {\n"
"    padding-top: 3px;\n"
"}\n"
"")
        self.msh_browse_btn.setIcon(icon)
        self.msh_browse_btn.setIconSize(QSize(20, 20))

        self.gridLayout.addWidget(self.msh_browse_btn, 1, 0, 1, 1)

        self.msh_open_btn = QPushButton(self.centralwidget)
        self.msh_open_btn.setObjectName(u"msh_open_btn")
        self.msh_open_btn.setMinimumSize(QSize(30, 30))
        self.msh_open_btn.setMaximumSize(QSize(30, 30))
        self.msh_open_btn.setStyleSheet(u"/* \u6309\u94ae\u9ed8\u8ba4\u6837\u5f0f */\n"
"QPushButton {\n"
"    border-radius: 6px;\n"
"    border: 1px solid rgb(160, 160, 160); \n"
"}\n"
"\n"
"/* \u60ac\u6d6e\u7279\u6548\uff1a\u80cc\u666f\u989c\u8272\u53d8\u6d45\uff0c\u5e76\u589e\u52a0\u84dd\u8272\u8fb9\u6846\u611f */\n"
"QPushButton:hover {\n"
"    background-color: rgb(160, 160, 160); /* \u989c\u8272\u6bd4\u9ed8\u8ba4\u7a0d\u4eae */\n"
"}\n"
"\n"
"/* \u6309\u4e0b\u7279\u6548\uff1a\u70b9\u51fb\u65f6\u989c\u8272\u53d8\u6df1\uff0c\u4ea7\u751f\u7269\u7406\u538b\u4e0b\u7684\u9519\u89c9 */\n"
"QPushButton:pressed {\n"
"    padding-top: 3px;\n"
"}\n"
"")
        self.msh_open_btn.setIcon(icon1)
        self.msh_open_btn.setIconSize(QSize(22, 22))

        self.gridLayout.addWidget(self.msh_open_btn, 1, 1, 1, 1)

        self.gmsh_btn = QPushButton(self.centralwidget)
        self.gmsh_btn.setObjectName(u"gmsh_btn")
        self.gmsh_btn.setMinimumSize(QSize(30, 30))
        self.gmsh_btn.setMaximumSize(QSize(30, 30))
        self.gmsh_btn.setStyleSheet(u"/* \u6309\u94ae\u9ed8\u8ba4\u6837\u5f0f */\n"
"QPushButton {\n"
"    border-radius: 6px;\n"
"    border: 1px solid rgb(160, 160, 160); \n"
"}\n"
"\n"
"/* \u60ac\u6d6e\u7279\u6548\uff1a\u80cc\u666f\u989c\u8272\u53d8\u6d45\uff0c\u5e76\u589e\u52a0\u84dd\u8272\u8fb9\u6846\u611f */\n"
"QPushButton:hover {\n"
"    background-color: rgb(160, 160, 160); /* \u989c\u8272\u6bd4\u9ed8\u8ba4\u7a0d\u4eae */\n"
"}\n"
"\n"
"/* \u6309\u4e0b\u7279\u6548\uff1a\u70b9\u51fb\u65f6\u989c\u8272\u53d8\u6df1\uff0c\u4ea7\u751f\u7269\u7406\u538b\u4e0b\u7684\u9519\u89c9 */\n"
"QPushButton:pressed {\n"
"    padding-top: 3px;\n"
"}\n"
"")
        icon3 = QIcon()
        icon3.addFile(u"../JDFOAM/resources/gmsh.ico", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.gmsh_btn.setIcon(icon3)
        self.gmsh_btn.setIconSize(QSize(23, 23))

        self.gridLayout.addWidget(self.gmsh_btn, 1, 2, 1, 1)


        self.horizontalLayout.addLayout(self.gridLayout)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.button_hbox = QHBoxLayout()
        self.button_hbox.setSpacing(20)
        self.button_hbox.setObjectName(u"button_hbox")
        self.start_mesh_btn = QPushButton(self.centralwidget)
        self.start_mesh_btn.setObjectName(u"start_mesh_btn")
        self.start_mesh_btn.setMinimumSize(QSize(0, 40))
        self.start_mesh_btn.setMaximumSize(QSize(200, 16777215))
        self.start_mesh_btn.setFont(font1)
        self.start_mesh_btn.setStyleSheet(u"/* \u6309\u94ae\u9ed8\u8ba4\u6837\u5f0f */\n"
"QPushButton {\n"
"    background-color:rgb(167, 83, 250);\n"
"    color: white;\n"
"    border-radius: 6px;\n"
"    padding: 5px 15px;\n"
"    border: none;\n"
"}\n"
"\n"
"/* \u60ac\u6d6e\u7279\u6548\uff1a\u80cc\u666f\u989c\u8272\u53d8\u6d45\uff0c\u5e76\u589e\u52a0\u84dd\u8272\u8fb9\u6846\u611f */\n"
"QPushButton:hover {\n"
"    background-color:rgb(127, 64, 191);\n"
"}\n"
"\n"
"/* \u6309\u4e0b\u7279\u6548\uff1a\u70b9\u51fb\u65f6\u989c\u8272\u53d8\u6df1\uff0c\u4ea7\u751f\u7269\u7406\u538b\u4e0b\u7684\u9519\u89c9 */\n"
"QPushButton:pressed {\n"
"    padding-top: 6px;\n"
"}\n"
"")

        self.button_hbox.addWidget(self.start_mesh_btn)

        self.combine_md_btn = QPushButton(self.centralwidget)
        self.combine_md_btn.setObjectName(u"combine_md_btn")
        self.combine_md_btn.setMinimumSize(QSize(0, 40))
        self.combine_md_btn.setMaximumSize(QSize(200, 16777215))
        self.combine_md_btn.setFont(font1)
        self.combine_md_btn.setStyleSheet(u"/* \u6309\u94ae\u9ed8\u8ba4\u6837\u5f0f */\n"
"QPushButton {\n"
"    background-color: rgb(63, 140, 243);\n"
"    color: white;\n"
"    border-radius: 6px;\n"
"    padding: 5px 15px;\n"
"    border: none;\n"
"}\n"
"\n"
"/* \u60ac\u6d6e\u7279\u6548\uff1a\u80cc\u666f\u989c\u8272\u53d8\u6d45\uff0c\u5e76\u589e\u52a0\u84dd\u8272\u8fb9\u6846\u611f */\n"
"QPushButton:hover {\n"
"    background-color: rgb(53, 118, 204); /* \u989c\u8272\u6bd4\u9ed8\u8ba4\u7a0d\u4eae */\n"
"}\n"
"\n"
"/* \u6309\u4e0b\u7279\u6548\uff1a\u70b9\u51fb\u65f6\u989c\u8272\u53d8\u6df1\uff0c\u4ea7\u751f\u7269\u7406\u538b\u4e0b\u7684\u9519\u89c9 */\n"
"QPushButton:pressed {\n"
"    padding-top: 6px;\n"
"}\n"
"")

        self.button_hbox.addWidget(self.combine_md_btn)

        self.combine_pdf_btn = QPushButton(self.centralwidget)
        self.combine_pdf_btn.setObjectName(u"combine_pdf_btn")
        self.combine_pdf_btn.setEnabled(True)
        self.combine_pdf_btn.setMinimumSize(QSize(0, 40))
        self.combine_pdf_btn.setMaximumSize(QSize(200, 16777215))
        self.combine_pdf_btn.setFont(font1)
        self.combine_pdf_btn.setStyleSheet(u"/* \u6309\u94ae\u9ed8\u8ba4\u6837\u5f0f */\n"
"QPushButton {\n"
"    background-color: rgb(207, 1, 56);\n"
"    color: white;\n"
"    border-radius: 6px;\n"
"    padding: 5px 15px;\n"
"    border: none;\n"
"}\n"
"\n"
"/* \u60ac\u6d6e\u7279\u6548\uff1a\u80cc\u666f\u989c\u8272\u53d8\u6d45\uff0c\u5e76\u589e\u52a0\u84dd\u8272\u8fb9\u6846\u611f */\n"
"QPushButton:hover {\n"
"    background-color: #a70832; /* \u989c\u8272\u6bd4\u9ed8\u8ba4\u7a0d\u4eae */\n"
"}\n"
"\n"
"/* \u6309\u4e0b\u7279\u6548\uff1a\u70b9\u51fb\u65f6\u989c\u8272\u53d8\u6df1\uff0c\u4ea7\u751f\u7269\u7406\u538b\u4e0b\u7684\u9519\u89c9 */\n"
"QPushButton:pressed {\n"
"    padding-top: 6px;\n"
"}\n"
"")

        self.button_hbox.addWidget(self.combine_pdf_btn)


        self.verticalLayout.addLayout(self.button_hbox)

        self.progress_bar = QProgressBar(self.centralwidget)
        self.progress_bar.setObjectName(u"progress_bar")
        self.progress_bar.setStyleSheet(u"/* \u8fdb\u5ea6\u6761\u80cc\u666f\u69fd */\n"
"QProgressBar {\n"
"    border: none;                /* \u53bb\u6389\u8fb9\u6846 */\n"
"    color: white;                /* \u767e\u5206\u6bd4\u6587\u5b57\u989c\u8272 */\n"
"    text-align: center;          /* \u6587\u5b57\u5c45\u4e2d */\n"
"    background: #e0e0e0;         /* \u69fd\u7684\u80cc\u666f\u8272 */\n"
"    border-radius: 5px;          /* \u5706\u89d2\u9ad8\u5ea6\u7684\u4e00\u534a\u901a\u5e38\u770b\u8d77\u6765\u5f88\u8212\u670d */\n"
"    height: 10px;                /* \u8fd9\u91cc\u7684 height \u4f1a\u5f71\u54cd\u69fd\u7684\u7c97\u7ec6 */\n"
"}\n"
"\n"
"/* \u5df2\u586b\u5145\u7684\u8fdb\u5ea6\u90e8\u5206 */\n"
"QProgressBar::chunk {\n"
"    background-color: #05B8CC;   /* \u8fdb\u5ea6\u6761\u989c\u8272\uff1a\u9752\u84dd\u8272 */\n"
"    border-radius: 5px;          /* \u8fdb\u5ea6\u6761\u7684\u5706\u89d2 */\n"
"}")
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)

        self.verticalLayout.addWidget(self.progress_bar)

        self.Log = QPlainTextEdit(self.centralwidget)
        self.Log.setObjectName(u"Log")
        self.Log.setStyleSheet(u"QPlainTextEdit {\n"
"    /* 1. \u5fc5\u987b\u6709\u8fb9\u6846\uff0c\u900f\u660e\u5373\u53ef */\n"
"    border: 1px solid transparent;\n"
"    \n"
"    /* 2. \u5b9a\u4e49\u5706\u89d2 */\n"
"    border-radius: 6px;\n"
"    \n"
"    /* 3. \u6838\u5fc3\uff1a\u5fc5\u987b\u5b9a\u4e49\u80cc\u666f\u8272\uff0c\u5706\u89d2\u624d\u80fd\u88ab\u201c\u586b\u5145\u201d\u51fa\u6765 */\n"
"    /* palette(base) \u4f1a\u81ea\u52a8\u8ddf\u968f\u4e3b\u9898\uff1a\u6d45\u8272\u65f6\u662f\u767d\u8272\uff0c\u6df1\u8272\u65f6\u662f\u6df1\u7070 */\n"
"    background-color: palette(base);\n"
"    \n"
"    /* 4. \u6587\u5b57\u989c\u8272\u4e5f\u8ddf\u968f\u4e3b\u9898 */\n"
"    color: palette(text);\n"
"    \n"
"    /* \u5efa\u8bae\u52a0\u70b9\u5185\u8fb9\u8ddd\uff0c\u5426\u5219\u5b57\u4f1a\u8d34\u5230\u5706\u89d2\u8fb9\u4e0a */\n"
"    padding: 3px;\n"
"}")
        self.Log.setReadOnly(True)

        self.verticalLayout.addWidget(self.Log)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        JDFOAM_GUI.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(JDFOAM_GUI)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 630, 33))
        self.menu_theme = QMenu(self.menubar)
        self.menu_theme.setObjectName(u"menu_theme")
        JDFOAM_GUI.setMenuBar(self.menubar)

        self.menubar.addAction(self.menu_theme.menuAction())
        self.menu_theme.addAction(self.action_light_theme)
        self.menu_theme.addAction(self.action_dark_theme)

        self.retranslateUi(JDFOAM_GUI)

        QMetaObject.connectSlotsByName(JDFOAM_GUI)
    # setupUi

    def retranslateUi(self, JDFOAM_GUI):
        JDFOAM_GUI.setWindowTitle(QCoreApplication.translate("JDFOAM_GUI", u"JDFOAM", None))
        self.action_light_theme.setText(QCoreApplication.translate("JDFOAM_GUI", u"light", None))
        self.action_dark_theme.setText(QCoreApplication.translate("JDFOAM_GUI", u"dark", None))
        self.case_label.setText(QCoreApplication.translate("JDFOAM_GUI", u"\u7b97\u4f8b\u76ee\u5f55:", None))
        self.case_path_edit.setPlaceholderText(QCoreApplication.translate("JDFOAM_GUI", u"\u9009\u62e9\u7b97\u4f8b\u9879\u76ee\u6839\u76ee\u5f55", None))
        self.msh_label.setText(QCoreApplication.translate("JDFOAM_GUI", u".msh\u6587\u4ef6:", None))
        self.msh_path_edit.setPlaceholderText(QCoreApplication.translate("JDFOAM_GUI", u"\u9009\u62e9\u5f85\u8f6c\u6362\u7684 .msh \u6587\u4ef6", None))
#if QT_CONFIG(tooltip)
        self.case_browse_btn.setToolTip(QCoreApplication.translate("JDFOAM_GUI", u"\u6d4f\u89c8\u6587\u4ef6\u5939", None))
#endif // QT_CONFIG(tooltip)
        self.case_browse_btn.setText("")
#if QT_CONFIG(tooltip)
        self.case_open_btn.setToolTip(QCoreApplication.translate("JDFOAM_GUI", u"\u6253\u5f00\u6587\u4ef6\u5939", None))
#endif // QT_CONFIG(tooltip)
        self.case_open_btn.setText("")
#if QT_CONFIG(tooltip)
        self.treefoam_btn.setToolTip(QCoreApplication.translate("JDFOAM_GUI", u"\u542f\u52a8TreeFoam", None))
#endif // QT_CONFIG(tooltip)
        self.treefoam_btn.setText("")
#if QT_CONFIG(tooltip)
        self.msh_browse_btn.setToolTip(QCoreApplication.translate("JDFOAM_GUI", u"\u6d4f\u89c8.msh\u6587\u4ef6\u8def\u5f84", None))
#endif // QT_CONFIG(tooltip)
        self.msh_browse_btn.setText("")
#if QT_CONFIG(tooltip)
        self.msh_open_btn.setToolTip(QCoreApplication.translate("JDFOAM_GUI", u"\u6253\u5f00.msh\u6240\u5728\u6587\u4ef6\u5939", None))
#endif // QT_CONFIG(tooltip)
        self.msh_open_btn.setText("")
#if QT_CONFIG(tooltip)
        self.gmsh_btn.setToolTip(QCoreApplication.translate("JDFOAM_GUI", u"\u542f\u52a8Gmsh", None))
#endif // QT_CONFIG(tooltip)
        self.gmsh_btn.setText("")
        self.start_mesh_btn.setText(QCoreApplication.translate("JDFOAM_GUI", u"\u5f00\u59cb\u8f6c\u6362\u7f51\u683c", None))
        self.combine_md_btn.setText(QCoreApplication.translate("JDFOAM_GUI", u"\u5408\u5e76\u4ee3\u7801\u4e3aMarkdown", None))
        self.combine_pdf_btn.setText(QCoreApplication.translate("JDFOAM_GUI", u"\u5bfc\u51fa\u4ee3\u7801\u4e3aPDF", None))
        self.progress_bar.setFormat("")
        self.menu_theme.setTitle(QCoreApplication.translate("JDFOAM_GUI", u"Theme", None))
    # retranslateUi

