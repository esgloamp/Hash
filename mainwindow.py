import os
import platform
import time

from PyQt5 import QtGui
from PyQt5.QtCore import QFileInfo, QSize, Qt, pyqtSlot
from PyQt5.QtGui import QKeyEvent, QTextCursor
from PyQt5.QtWidgets import (QApplication, QDial, QDialog, QFileDialog, QFrame,
                             QHBoxLayout, QProgressBar, QPushButton, QTextEdit,
                             QVBoxLayout, QWidget)

from compdialog import CompDialog
from hash import HashTest, hash_count
from titlebar import TitleBar


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.init_ui()
        self.conn()

    def init_ui(self):
        self.setFixedSize(QSize(900, 500))  # 窗口长宽固定900x500
        self.setAcceptDrops(True)  # 主窗口允许拖拽文件
        self.setStyleSheet("color:red;")
        self.pgbsingle = QProgressBar(self)  # 进度条1
        self.pgbsingle.setAlignment(Qt.AlignCenter)  # 进度条文字信息上下左右居中
        self.pgbsingle.setStyleSheet(
            "QProgressBar{"
            "	font:9pt;"
            "	border-radius:5px;"
            "	text-align:center;"
            "	border:1px solid #E8EDF2;"
            "	background-color: rgb(255, 255, 255);"
            "	border-color: rgb(180, 180, 180);"
            "}"
            "QProgressBar:chunk{"
            "	border-radius:3px;"
            "	background-color:#1ABC9C;"
            "}")
        self.pgbmulti = QProgressBar(self)  # 进度条2
        self.pgbmulti.setAlignment(Qt.AlignCenter)
        self.pgbmulti.setStyleSheet(
            "QProgressBar{"
            "	font:9pt;"
            "	border-radius:5px;"
            "	text-align:center;"
            "	border:1px solid #E8EDF2;"
            "	background-color: rgb(255, 255, 255);"
            "	border-color: rgb(180, 180, 180);"
            "}"
            "QProgressBar:chunk{"
            "	border-radius:3px;"
            "	background-color:#1ABC9C;"
            "}")

        self.textedit = QTextEdit()  # 文本框
        self.textedit.setAcceptDrops(False)  # 禁用QTextEdit自带的拖拽事件
        self.textedit.setReadOnly(True)  # 只读模式

        # 按钮组,宽度取决于按钮个数
        self.btnopen = QPushButton("打开(Ctrl+O)")  # 打开按钮
        self.btnopen.setFixedHeight(30)    # 高度固定30px
        self.btnsave = QPushButton("保存(Ctrl+S)")
        self.btnsave.setFixedHeight(30)
        self.btnclear = QPushButton("清除(Ctrl+D)")
        self.btnclear.setFixedHeight(30)
        self.btncopy = QPushButton("复制(Ctrl+Shift+C)")
        self.btncopy.setFixedHeight(30)
        self.btncomp = QPushButton("比较(Ctrl+P)")
        self.btncomp.setFixedHeight(30)

        self.btnopen.setStyleSheet(
            "QPushButton{background-color: #1ABC9C;border-radius: 3px;}QPushButton:hover{background-color: #24C6A6;}")
        self.btnclear.setStyleSheet(
            "QPushButton{background-color: #1ABC9C;border-radius: 3px;}QPushButton:hover{background-color: #24C6A6;}")
        self.btnsave.setStyleSheet(
            "QPushButton{background-color: #1ABC9C;border-radius: 3px;}QPushButton:hover{background-color: #24C6A6;}")
        self.btncomp.setStyleSheet(
            "QPushButton{background-color: #1ABC9C;border-radius: 3px;}QPushButton:hover{background-color: #24C6A6;}")
        self.btncopy.setStyleSheet(
            "QPushButton{background-color: #1ABC9C;border-radius: 3px;}QPushButton:hover{background-color: #24C6A6;}")
        # 按钮组布局为水平布局
        btnlay = QHBoxLayout()
        btnlay.setContentsMargins(0, 6, 0, 6)  # 内边距设置为6px
        btnlay.addWidget(self.btnopen)         # 添加按钮控件
        btnlay.addWidget(self.btnsave)
        btnlay.addWidget(self.btnclear)
        btnlay.addWidget(self.btncopy)
        btnlay.addWidget(self.btncomp)

        self.titlebar = TitleBar(self)

        # 主布局设置为垂直布局
        hlay = QVBoxLayout()
        hlay.setContentsMargins(6, 0, 6, 0)
        hlay.addWidget(self.titlebar)
        hlay.addWidget(self.pgbsingle)  # 添加进度条1
        hlay.addWidget(self.pgbmulti)   # 添加进度条2
        hlay.addWidget(self.textedit)   # 添加文本框
        hlay.addLayout(btnlay)          # 添加按钮组

        # 将所有控件加入控件容器
        self.setLayout(hlay)
        self.setStyleSheet("#titlebar{background-color:black;}")

        self.hashtest = HashTest()

    def conn(self):
        # 各个按钮连接各自的槽
        self.btnopen.clicked.connect(self.open)
        self.btnsave.clicked.connect(self.save)
        self.btnclear.clicked.connect(self.clear)
        self.btncopy.clicked.connect(self.copy)
        self.btncomp.clicked.connect(self.popup)
        self.hashtest.signal_update.connect(
            lambda x: self.update_pgb(x))  # 自定义信号必须写成lambda，不能写成.connect(self.update_pgb)，不然程序崩溃

    # 处理鼠标拖拽进入主界面后的事件
    def dragEnterEvent(self, e: QtGui.QDragEnterEvent) -> None:
        # 判断拖拽的目标是否有url，如果有，进入下一步判断，否则不接受此次拖拽事件
        if e.mimeData().hasUrls():
            # 遍历拖拽目标url，判断是否有目录，如果有，则不接受此次拖拽事件，否则接受
            for url in e.mimeData().urls():
                # 判断url是否为目录
                # 获取的url默认带有/前缀，Windows下该url错误，所以Windows需要删除前缀，Linux不需要
                if QFileInfo(url.path()[1:] if platform.system() == "Windows" else url.path()).isDir():
                    e.ignore()
                    break
            else:
                e.acceptProposedAction()
        else:
            e.ignore()

    #  处理松开鼠标后的拖拽事件
    def dropEvent(self, e: QtGui.QDropEvent) -> None:
        print("drop")
        #  将所有需要测试的文件以列表形式传入testfiles方法
        #  获取的url默认带有/前缀，Windows下该url错误，所以Windows需要删除前缀，Linux不需要
        self.testfiles(sorted([i.path()[1:] if platform.system() == "Windows" else i.path()
                               for i in e.mimeData().urls()]))
        return super().dropEvent(e)  # 将事件传给父类，由其处理

    def setenable(self, enable: bool) -> None:
        #  设置按钮是否可用
        self.btnsave.setEnabled(enable)
        self.btnopen.setEnabled(enable)
        self.btnclear.setEnabled(enable)
        self.btncopy.setEnabled(enable)

    def testfiles(self, files: list) -> None:
        print(files)
        self.setenable(False)  # 按钮设置为不可用

        #  设置进度条1的范围、初始值、显示格式
        self.pgbsingle.setRange(0, hash_count)
        self.pgbsingle.setValue(0)
        self.pgbsingle.setFormat(f"{0}/{len(files)}")

        #  设置进度条2的范围、初始值、显示格式
        self.pgbmulti.setRange(0, len(files))
        self.pgbmulti.setValue(0)
        self.pgbmulti.setFormat(f"{0}/{len(files)}")
        pg = 0  # 初始化进度条2数据

        for file in files:
            print(f"processing {file}")

            # 光标移动到文本框最后
            self.textedit.moveCursor(QTextCursor.MoveOperation.End)

            # 插入文件名
            self.textedit.insertPlainText(f"文件: {file}\n")

            # 获取文件信息
            filestat = os.stat(file)

            # 插入文件大小
            self.textedit.insertPlainText(f"大小: {filestat.st_size} 字节\n")

            #  格式化文件最后修改时间
            mtime = time.strftime("%Y/%m/%d %H:%M:%S",
                                  time.localtime(filestat.st_mtime))
            #  插入格式化后的时间
            self.textedit.insertPlainText(f"最后修改时间: {mtime}\n")

            # 开始计算hash值
            hashes = self.hashtest.test(file)

            # 计算完后进度+1
            pg += 1

            # 更新进度条2信息
            self.pgbmulti.setValue(pg)
            self.pgbmulti.setFormat(f"{pg}/{len(files)}")

            # 插入hash信息
            for k, v in hashes.items():
                self.textedit.insertPlainText(f"{k}: {v}\n")

            # 插入分隔线
            self.textedit.insertPlainText("-" * 20 + "\n\n")

        # 按钮设置可用
        self.setenable(True)

    # 打开文件
    @ pyqtSlot()  # <-这个是槽函数修饰器
    def open(self) -> None:
        try:
            filedlg = QFileDialog()
            # 打开文件对话框
            filenames = filedlg.getOpenFileNames(
                self, "Open Files", "./", "All Files(*.*)")
            print(filenames)
            # 选择文件数量大于0
            if len(filenames[0]) > 0:
                # 开始计算hash值
                self.testfiles([i for i in filenames[0]])
        except Exception as e:
            print(e)

    # 保存到文件
    @pyqtSlot()
    def save(self) -> None:
        filedlg = QFileDialog()
        filename = filedlg.getSaveFileName(
            self, "Save File", "./", "Text File(*.txt)")

        #  点了取消
        if filename[0] == '':
            return

        print(filename)
        with open(filename[0], "w", encoding="utf8") as savefile:
            currtime = time.strftime(
                "%Y/%m/%d %H:%M:%S", time.localtime(time.time()))
            print(currtime)
            savefile.write("*" * 55 + "\n")
            savefile.write(
                f"This file was created by hashes on {currtime}\n")
            savefile.write("*" * 55 + "\n\n\n")
            a = savefile.write(self.textedit.toPlainText())
            print(a)

    # 清除文本框
    @pyqtSlot()
    def clear(self) -> None:
        self.textedit.clear()

    # 复制文本框信息到剪贴板
    @pyqtSlot()
    def copy(self) -> None:
        clipboard = QApplication.clipboard()
        clipboard.setText(self.textedit.toPlainText())

    # 进度条1信息
    def testinfo(self, v: int) -> str:
        print(v)
        rets = (
            "正在计算 CRC32",
            "正在计算 ADLER32",
            "正在计算 MD5",
            "正在计算 SHA1",
            "正在计算 SHA224",
            "正在计算 SHA384",
            "正在计算 SHA512",
        )
        return rets[v]

    # 弹出操作窗口
    def popup(self):
        dialog = CompDialog(self)
        dialog.show()

    # 更新进度条1的信息
    @pyqtSlot()
    def update_pgb(self, v: int) -> None:
        self.pgbsingle.setFormat(
            "100%" if v == self.pgbsingle.maximum() else f"{self.testinfo(v - 1)}")
        self.pgbsingle.setValue(v)

    def keyPressEvent(self, e: QtGui.QKeyEvent) -> None:
        if e.modifiers() == Qt.ControlModifier:  # 按下ctrl键
            if e.key() == Qt.Key_O:
                self.open()
            if e.key() == Qt.Key_S:
                self.save()
            if e.key() == Qt.Key_D:
                self.clear()
            if e.key() == Qt.Key_P:
                self.popup()
            if e.key() == Qt.Key_W:
                QApplication.exit()  # 退出应用
        # 按下ctrl+shift
        if e.modifiers() == Qt.ControlModifier | Qt.ShiftModifier and e.key() == Qt.Key_C:
            self.copy()

        # 按下esc键
        if e.key() == Qt.Key_Escape:
            self.showMinimized()  # 最小化
        return super().keyPressEvent(e)
