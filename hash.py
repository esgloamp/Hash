import hashlib
import threading
import zlib

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget

hash_count = int(8)


class HashTest(QWidget):
    signal_update = pyqtSignal(int)  # 更新进度条信号

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

    def test(self, path: str) -> dict:
        ret = {}
        with open(path, "rb") as file:
            buf = file.read()

            ret["CRC32"] = crc32(buf)
            self.signal_update.emit(1)  # 发送进度条1进度

            ret['ADLER32'] = adler32(buf)
            self.signal_update.emit(2)

            ret["MD5"] = md5(buf)
            self.signal_update.emit(3)

            ret["SHA1"] = sha1(buf)
            self.signal_update.emit(4)

            ret["SHA224"] = sha224(buf)
            self.signal_update.emit(5)

            ret["SHA256"] = sha256(buf)
            self.signal_update.emit(6)

            ret["SHA384"] = sha384(buf)
            self.signal_update.emit(7)

            ret["SHA512"] = sha512(buf)
            self.signal_update.emit(8)

        return ret


def crc32(buf: bytes) -> str:
    k = zlib.crc32(buf)
    return hex(k)[2:].upper().zfill(8)  # 去除前缀0x，大写，前面补零到8个字符


def adler32(buf: bytes) -> str:
    k = zlib.adler32(buf)
    return hex(k)[2:].upper().zfill(8)


def md5(buf: bytes) -> str:
    m = hashlib.md5()
    m.update(buf)
    return m.hexdigest().upper()


def sha1(buf: bytes) -> str:
    sh = hashlib.sha1()
    sh.update(buf)
    return sh.hexdigest().upper()


def sha224(buf: bytes) -> str:
    sh = hashlib.sha224()
    sh.update(buf)
    return sh.hexdigest().upper()


def sha256(buf: bytes) -> str:
    sh = hashlib.sha256()
    sh.update(buf)
    return sh.hexdigest().upper()


def sha384(buf: bytes) -> str:
    sh = hashlib.sha384()
    sh.update(buf)
    return sh.hexdigest().upper()


def sha512(buf: bytes) -> str:
    sh = hashlib.sha512()
    sh.update(buf)
    return sh.hexdigest().upper()
