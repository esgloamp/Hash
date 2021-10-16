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
        self.labelicon.setPixmap(QPixmap("./icon32.png"))
        self.labeltitle = QLabel()
        self.labeltitle.setText("Hash By NZP")
        self.labelclose = ClickableLabel()
        self.labelclose.setPixmap(QPixmap("./close.png"))
        self.labelclose.clicked.connect(lambda: QApplication.exit())
        self.labelmin = ClickableLabel()
        self.labelmin.setPixmap(QPixmap("./min.png"))
        self.labelmin.clicked.connect(lambda: self.parent.showMinimized())

        lay = QHBoxLayout()
        lay.addWidget(self.labelicon)
        lay.addStretch()
        lay.addWidget(self.labeltitle)
        lay.addStretch()
        lay.addWidget(self.labelmin)
        lay.addWidget(self.labelclose)
        lay.setContentsMargins(0, 6, 0, 0)
        self.setLayout(lay)

    # 鼠标按下
    def mousePressEvent(self, e: QtGui.QMouseEvent) -> None:
        self.isPress = True
        self.startPos = e.globalPos()
        return super().mousePressEvent(e)

    # 鼠标移动
    def mouseMoveEvent(self, e: QtGui.QMouseEvent) -> None:
        if self.isPress:
            movePos = e.globalPos() - self.startPos
            self.startPos = e.globalPos()
            self.window().move(self.window().pos() + movePos)  # 移动窗口
        return super().mouseMoveEvent(e)

    # 鼠标松开
    def mouseReleaseEvent(self, e: QtGui.QMouseEvent) -> None:
        self.isPress = False
        return super().mouseReleaseEvent(e)
