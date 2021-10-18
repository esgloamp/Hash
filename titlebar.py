from PyQt5 import QtGui
from PyQt5.QtCore import Qt, pyqtBoundSignal, pyqtSignal
from PyQt5.QtGui import QIcon, QMouseEvent, QPixmap
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPushButton,
                             QStyle, QWidget)
from PyQt5.sip import ispycreated

from clickablelabel import ClickableLabel


class TitleBar(QWidget):
    def __init__(self, parent=None) -> None:
        self.parent = parent
        super(TitleBar, self).__init__(parent)
        self.setMouseTracking(True)
        self.init_ui()

        self.isPress = False

    def init_ui(self):
        self.labelicon = QLabel()
        self.labelicon.setPixmap(QPixmap("./assets/icon32.png"))  # label设置图片
        self.labeltitle = QLabel()
        self.labeltitle.setText("Hash By NZP")  # lable设置文本
        self.labelclose = ClickableLabel()
        self.labelclose.setPixmap(QPixmap("./assets/close.png"))
        self.labelclose.clicked.connect(lambda: QApplication.exit())  # 退出应用
        self.labelmin = ClickableLabel()
        self.labelmin.setPixmap(QPixmap("./assets/min.png"))
        self.labelmin.clicked.connect(
            lambda: self.parent.showMinimized())  # 最小化

        lay = QHBoxLayout()
        lay.addWidget(self.labelicon)
        lay.addStretch()  # 保证程序图标居左，标题居中
        lay.addWidget(self.labeltitle)
        lay.addStretch()  # 保证标题居中，最小化、关闭图标居右
        lay.addWidget(self.labelmin)
        lay.addWidget(self.labelclose)
        # 设置内部控件距离边框的像素值，从参数左到右分别是左、上、右、下的距离
        lay.setContentsMargins(0, 6, 0, 0)
        self.setLayout(lay)

    # 鼠标按下
    def mousePressEvent(self, e: QtGui.QMouseEvent) -> None:
        self.isPress = True
        self.startPos = e.globalPos()  # 获取鼠标全局坐标
        return super().mousePressEvent(e)  # 交由父类鼠标按下事件进行后续处理

    # 鼠标移动
    def mouseMoveEvent(self, e: QtGui.QMouseEvent) -> None:
        if self.isPress:  # 如果已经按下，则可以移动
            movePos = e.globalPos() - self.startPos  # 移动的距离是按下时当前的距离-按下时的距离
            self.startPos = e.globalPos()  # 更新按下时的距离为当前距离
            self.window().move(self.window().pos() + movePos)  # 移动窗口
        return super().mouseMoveEvent(e)  # 交由父类鼠标移动事件进行后续处理

    # 鼠标松开
    def mouseReleaseEvent(self, e: QtGui.QMouseEvent) -> None:
        self.isPress = False
        return super().mouseReleaseEvent(e)  # 交由父类鼠标松开事件进行后续处理
