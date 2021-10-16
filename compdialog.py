from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont, QPalette
from PyQt5.QtWidgets import (QApplication, QDialog, QFrame, QHBoxLayout,
                             QLabel, QLayout, QLineEdit,
                             QPlainTextDocumentLayout, QPushButton,
                             QVBoxLayout, QWidget)

from titlebar import TitleBar


class CompDialog(QDialog):
    def __init__(self, parent: QWidget = None):
        super(CompDialog, self).__init__(parent)
        self.parent = parent
        self.setFixedSize(300, 300)
        self.init_ui()
        self.conn()

    def init_ui(self):
        self.lineedit1 = QLineEdit(self)
        self.lineedit1.setFixedHeight(30)
        self.lineedit2 = QLineEdit(self)
        self.lineedit2.setFixedHeight(30)
        self.info = QLabel()
        self.info.setText("把要比较的两个字符串分别放到两个输入框内")
        self.info.setFixedHeight(30)
        self.info.setAlignment(Qt.AlignCenter)

        contentLay = QVBoxLayout()
        contentLay.addWidget(self.lineedit1)
        contentLay.addWidget(self.lineedit2)
        contentLay.addWidget(self.info)
        self.setLayout(contentLay)
        self.setContentsMargins(0, 0, 0, 0)

    def conn(self):
        self.lineedit1.textChanged.connect(self.compare)
        self.lineedit2.textChanged.connect(self.compare)

    def compare(self):
        print('hello')
        if self.lineedit1.text() == self.lineedit2.text():
            self.info.setStyleSheet("color: green")
            self.info.setText("相等")
        else:
            self.info.setStyleSheet("color: red")
            self.info.setText("不相等")
