#!/usr/bin/env python

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt
import sys
import pyowm
import datetime


class ClockandWeather(QtGui.QWidget):
    ##clock variables
    # Emitted when the clock's time changes.
    timeChanged = QtCore.pyqtSignal(QtCore.QTime)
    # Emitted when the clock's time zone changes.
    timeZoneChanged = QtCore.pyqtSignal(int)

    ##weather variables
    global picWidth, picHeight, lastmin
    picWidth = 128
    picHeight = 128
    lastmin = -1

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self)
        super(ClockandWeather, self).__init__(parent)

        # --------------------------------Clock Portion-----------------------------------------
        # Intitialze and set Frame that surrounds clock
        self.clockFrame = QtGui.QFrame(self)
        self.clockFrame.move(200, 200)
        self.clockFrame.resize(300, 300)
        self.clockFrame.setObjectName("clockFrame")
        self.clockFrame.setStyleSheet(
                "#clockFrame {background-color: transparent; border-image: url('icons/clockFace.png');}")

        # Initialize variables for clock hands
        self.hourHand = QtGui.QLabel(self.clockFrame)
        self.minHand = QtGui.QLabel(self.clockFrame)
        self.secHand = QtGui.QLabel(self.clockFrame)
        self.hourHand.setAlignment(QtCore.Qt.AlignCenter)
        self.minHand.setAlignment(QtCore.Qt.AlignCenter)
        self.secHand.setAlignment(QtCore.Qt.AlignCenter)
        self.hourHand.setStyleSheet("background-color: transparent")
        self.minHand.setStyleSheet("background-color: transparent")
        self.secHand.setStyleSheet("background-color: transparent")

        # Initialize clock timer
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.tick)
        timer.start(1000)

        # initialize pixmap
        self.secPixMap = QtGui.QPixmap("")
        self.minPixMap = QtGui.QPixmap("")
        self.hourPixMap = QtGui.QPixmap("")

        # ------------------------------------------------Weather Portion----------------------------------------
        self.weatherFrame = QtGui.QFrame(self)
        self.weatherFrame.move(500, 0)
        self.weatherPixMap = QtGui.QPixmap("")
        self.weatherIcon = QtGui.QLabel(self.weatherFrame)
        self.temp = QtGui.QLabel(self.weatherFrame)
        self.weatherDescrip = QtGui.QLabel(self.weatherFrame)
        self.highLowFrame = QtGui.QFrame(self)
        self.high = QtGui.QLabel(self.highLowFrame)
        self.low = QtGui.QLabel(self.highLowFrame)

        # setting up grid layout fo weather frame
        self.grid = QtGui.QGridLayout(self.weatherFrame)
        self.grid.addWidget(self.weatherIcon, 0, 0)
        self.grid.addWidget(self.temp, 0, 1, QtCore.Qt.AlignLeft)
        self.grid.addWidget(self.weatherDescrip, 1, 0, QtCore.Qt.AlignCenter)
        self.grid.addWidget(self.highLowFrame, 1, 1)

        # setting up High, Low
        self.highLowGrid = QtGui.QGridLayout(self.highLowFrame)
        self.highLowGrid.addWidget(self.high, 0, 0, QtCore.Qt.AlignLeft)
        self.highLowGrid.addWidget(self.low, 0, 1, QtCore.Qt.AlignRight)

        self.Src()

        # ---------Window settings --------------------------------
        self.setGeometry(300, 300, 750, 500)
        self.showFullScreen()
        # self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet("background-color: ")
        self.show()

        ##clock

    def tick(self):
        global lastmin
        global clockrect
        now = datetime.datetime.now()

        # Rotate from initial image to avoid cumulative deformation from
        # transformation
        # --------second hand
        self.secPixMap = QtGui.QPixmap("icons/clockFaceGrid.png")
        self.secPixMap = self.secPixMap.scaled(float(self.clockFrame.width()) * 0.6,
                                               float(self.clockFrame.height()) * 0.6, Qt.KeepAspectRatio)
        secHandDim = (self.secPixMap.width() ** 2 + self.secPixMap.height() ** 2) ** 0.5
        self.secHand.setGeometry(self.clockFrame.width() / 2 - secHandDim / 2,
                                 self.clockFrame.height() / 2 - secHandDim / 2, secHandDim,
                                 secHandDim)
        self.angle = now.second * 6
        transform = QtGui.QTransform().rotate(self.angle)
        self.secPixMap = self.secPixMap.transformed(transform, QtCore.Qt.SmoothTransformation)

        # ---- update label ----
        self.secHand.setPixmap(self.secPixMap)

        if now.minute != lastmin:
            lastmin = now.minute
            # -------minute hand
            self.minPixMap = QtGui.QPixmap("icons/minHand.png")
            self.minPixMap = self.minPixMap.scaled(float(self.clockFrame.width()) * 0.6,
                                                   float(self.clockFrame.height()) * 0.6, Qt.KeepAspectRatio)
            minHandDim = (self.minPixMap.width() ** 2 + self.minPixMap.height() ** 2) ** 0.5
            self.minHand.setGeometry(self.clockFrame.width() / 2 - minHandDim / 2,
                                     self.clockFrame.height() / 2 - minHandDim / 2, minHandDim,
                                     minHandDim)
            self.angle = now.minute * 6
            transform = QtGui.QTransform().rotate(self.angle)
            self.minPixMap = self.minPixMap.transformed(transform, QtCore.Qt.SmoothTransformation)
            self.minHand.setPixmap(self.minPixMap)

            # ---------hour hand
            self.hourPixMap = QtGui.QPixmap("icons/hourHand.png")
            self.hourPixMap = self.hourPixMap.scaled(float(self.clockFrame.width()) * 0.6,
                                                     float(self.clockFrame.height()) * 0.6, Qt.KeepAspectRatio)
            hourHandDim = (self.hourPixMap.width() ** 2 + self.hourPixMap.height() ** 2) ** 0.5
            self.hourHand.setGeometry(self.clockFrame.width() / 2 - hourHandDim / 2,
                                      self.clockFrame.height() / 2 - hourHandDim / 2, hourHandDim,
                                      hourHandDim)
            self.angle = ((now.hour % 12) + now.minute / 60.0) * 30.0
            transform = QtGui.QTransform().rotate(self.angle)
            self.hourPixMap = self.hourPixMap.transformed(transform, QtCore.Qt.SmoothTransformation)
            self.hourHand.setPixmap(self.hourPixMap)

    ##Weather
    def Src(self):
        global descrip
        global tempDict

        descrip = "Fair"

        owm = pyowm.OWM('03a8ab2b5c706e0321e66420998f0141')
        observation = owm.weather_at_place('Vancouver,BC')
        w = observation.get_weather()
        tempDict = w.get_temperature('celsius')
        descrip = w.get_status()

        self.Forecast()

    def Forecast(self):
        global descrip
        global temp
        global hum

        self.temp.setText(str(int(tempDict['temp'])))
        self.high.setText(str(int(tempDict['temp_max'])))
        self.low.setText(str(int(tempDict['temp_min'])))
        self.weatherDescrip.setText(descrip)

        self.weatherIcon.show()
        self.temp.show()

        if "cloud" in descrip.lower():
            self.weatherPixMap = QtGui.QPixmap("icons/cloudy.png")
            self.weatherPixMap = self.weatherPixMap.scaled(picWidth, picHeight)
            self.weatherIcon.setPixmap(self.weatherPixMap)

        elif "snow" in descrip.lower():
            self.weatherPixMap = QtGui.QPixmap("icons/sunny.png")
            self.weatherPixMap = self.weatherPixMap.scaled(picWidth, picHeight)
            self.weatherIcon.setPixmap(self.weatherPixMap)

        elif "rain" in descrip.lower():
            self.weatherPixMap = QtGui.QPixmap("icons/rainy.png")
            self.weatherPixMap = self.weatherPixMap.scaled(picWidth, picHeight)
            self.weatherIcon.setPixmap(self.weatherPixMap)

        elif "clear" in descrip.lower():
            self.weatherPixMap = QtGui.QPixmap("icons/clear.png")
            self.weatherPixMap = self.weatherPixMap.scaled(picWidth, picHeight)
            self.weatherIcon.setPixmap(self.weatherPixMap)

        elif "storm" in descrip.lower():
            self.weatherPixMap = QtGui.QPixmap("icons/stormy.png")
            self.weatherPixMap = self.weatherPixMap.scaled(picWidth, picHeight)
            self.weatherIcon.setPixmap(self.weatherPixMap)

        elif "mist" in descrip.lower():
            self.weatherPixMap = QtGui.QPixmap("icons/misty.png")
            self.weatherPixMap = self.weatherPixMap.scaled(picWidth, picHeight)
            self.weatherIcon.setPixmap(self.weatherPixMap)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    main = ClockandWeather()
    main.show()

    sys.exit(app.exec_())
