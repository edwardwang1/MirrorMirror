import sys

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt


class clock2(QtGui.QWidget):
    def __init__(self, parent=None):
        minWidth = 100
        minHeight = 200
        QtGui.QWidget.__init__(self)
        self.setWindowTitle(QtCore.QObject.tr(self, "Analog Clock"))

        self.hourPixMap2 = QtGui.QPixmap("")
        self.minPixMap2 = QtGui.QPixmap("")
        self.secPixMap2 = QtGui.QPixmap("")
        self.hourHand = QtGui.QLabel(self)
        self.minHand = QtGui.QLabel(self)
        self.secHand = QtGui.QLabel(self)

        self.hourPixMap = QtGui.QPixmap("icons/hourhand.png")
        self.hourPixMap = self.hourPixMap.scaled(minWidth,minHeight,Qt.KeepAspectRatio)

        self.minPixMap = QtGui.QPixmap("icons/minutehand.png")
        self.minPixMap = self.minPixMap.scaled(minWidth, minHeight, Qt.KeepAspectRatio)

        self.secPixMap = QtGui.QPixmap("icons/sechand.png")

        # ---------Window settings --------------------------------
        self.setGeometry(300, 300, 750, 500)
        self.setFixedSize(500, 333)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet("background-color:")
        self.show()

        self.hourHand.setPixmap(self.hourPixMap)
        self.secHand.setPixmap(self.secPixMap)

        self.minHand.move(0, 0)
        self.minHand.resize(minWidth,minHeight)
        self.minHand.setPixmap(self.minPixMap)
        self.minHand.show()

        self.hourHand.move(minWidth + 15, 0)
        self.hourHand.resize(minWidth, minHeight)
        self.hourHand.setPixmap(self.hourPixMap)
        self.hourHand.show()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    clock = clock2()
    clock.show()
    sys.exit(app.exec_())
