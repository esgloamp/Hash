from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QLabel


class ClickableLabel(QLabel):
    clicked = pyqtSignal()  # 点击信号

    def __init__(self, parent=None):
        super(ClickableLabel, self).__init__(parent)

    def mouseReleaseEvent(self, ev: QtGui.QMouseEvent) -> None:
        self.clicked.emit()  # 发送点击信号
        return super().mousePressEvent(ev)  # 交由父类鼠标按下事件进行后续处理
