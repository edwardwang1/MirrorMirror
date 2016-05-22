import sys
import datetime

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt


class clock2(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self)
        self.setWindowTitle(QtCore.QObject.tr(self, "Analog Clock"))

        self.hourPixMap2 = QtGui.QPixmap("")
        self.minPixMap2 = QtGui.QPixmap("")
        self.secPixMap2 = QtGui.QPixmap("")
        self.hourHand = QtGui.QLabel(self)
        self.minHand = QtGui.QLabel(self)
        self.secHand = QtGui.QLabel(self)
        self.hourPixMap = QtGui.QPixmap("icons/hourhand.png")
        self.minPixMap = QtGui.QPixmap("icons/minutehand.png")
        self.secPixMap = QtGui.QPixmap("icons/sechand.png")


        self.tick();
        # ---------Window settings --------------------------------
        self.setGeometry(300, 300, 750, 500)
        self.setFixedSize(1500, 1000)
        #self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet("background-color:")
        self.show()

    def tick(self):
        global lastmin
        global clockrect

        now = datetime.datetime.now()

        angle = now.second * 6
        ts = self.secPixMap.size()
        self.secPixMap2 = self.secPixMap.transformed(
                QtGui.QMatrix().scale(
                        float(clockrect.width()) / ts.height(),
                        float(clockrect.height()) / ts.height()
                ).rotate(angle),
                Qt.SmoothTransformation
        )
        self.secHand.setPixmap(self.secPixMap2)
        ts = self.secPixMap2.size()
        self.secHand.setGeometry(
                clockrect.center().x() - ts.width() / 2,
                clockrect.center().y() - ts.height() / 2,
                ts.width(),
                ts.height()
        )

        if now.minute != lastmin:
            lastmin = now.minute
            angle = now.minute * 6
            ts = self.minPixMap.size()
            self.minPixMap2 = self.minPixMap.transformed(
                    QtGui.QMatrix().scale(
                            float(clockrect.width()) / ts.height(),
                            float(clockrect.height()) / ts.height()
                    ).rotate(angle),
                    Qt.SmoothTransformation
            )
            self.minHand.setPixmap(self.minPixMap2)
            ts = self.minPixMap2.size()
            self.minHand.setGeometry(
                    clockrect.center().x() - ts.width() / 2,
                    clockrect.center().y() - ts.height() / 2,
                    ts.width(),
                    ts.height()
            )

            angle = ((now.hour % 12) + now.minute / 60.0) * 30.0
            ts = self.hourPixMap.size()
            self.hourpixmap2 = self.hourPixMap.transformed(
                    QtGui.QMatrix().scale(
                            float(clockrect.width()) / ts.height(),
                            float(clockrect.height()) / ts.height()
                    ).rotate(angle),
                    Qt.SmoothTransformation
            )
            self.hourHand.setPixmap(self.hourpixmap2)
            ts = self.hourpixmap2.size()
            self.hourHand.setGeometry(
                    clockrect.center().x() - ts.width() / 2,
                    clockrect.center().y() - ts.height() / 2,
                    ts.width(),
                    ts.height()
            )

            self.hourHand.show()
            self.minHand.show()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    clock = clock2()
    clockFrame = QtGui.QFrame(clock)

    #variables
    height = 500
    width = 333
    lastmin = -1
    clockrect = QtCore.QRect(width / 2 - height * .4, height * .45 - height * .4, height * .8, height * .8)
    #

    clock.show()
    sys.exit(app.exec_())
