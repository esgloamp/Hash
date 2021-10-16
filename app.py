import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from mainwindow import MainWindow

if __name__ == "__main__":
    try:
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)  # 高清屏幕自适应
        app = QApplication(sys.argv)  # 初始化应用
        mainwindow = MainWindow()  # 创建窗口
        mainwindow.setWindowFlags(Qt.FramelessWindowHint)  # 去除窗口标题栏
        mainwindow.setWindowTitle("Hash By NZP")
        mainwindow.setWindowIcon(QIcon("./icon.png"))
        mainwindow.show()  # 窗口可见
    except Exception as e:
        print(e)

    try:
        sys.exit(app.exec_())  # 开始执行应用
    except Exception as e:
        print(e)
