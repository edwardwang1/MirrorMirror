#!/usr/bin/env python

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt
import sys
import pywapi
import datetime
import math


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

        # Initialize clock timer
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.tick)
        timer.start(1000)

        # ------------------------------------------------Weather Portion----------------------------------------
        self.pix = QtGui.QPixmap("")
        self.pic = QtGui.QLabel(self)
        self.temp = QtGui.QLabel(self)
        self.hum = QtGui.QLabel(self)
        self.initUI()

    def initUI(self):
        self.pic.move(90, 110)
        self.pic.resize(picWidth, picHeight)
        self.pic.setPixmap(self.pix)

        self.temp.move(250, 160)
        self.temp.resize(150, 100)
        self.temp.setStyleSheet("font-size:50px; font-color: #FFFFFF;")

        self.hum.move(410, 160)
        self.hum.resize(250, 100)
        self.hum.setStyleSheet("font-size:50px;")

        self.Src()

        # ---------Window settings --------------------------------
        self.setGeometry(300, 300, 750, 500)
        self.setFixedSize(760, 520)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet("background-color: ")
        self.show()

        ##clock

    def tick(self):
        global lastmin
        global clockrect
        now = datetime.datetime.now()

        # Rotate from initial image to avoid cumulative deformation from
        # transformation
        self.secPixMap = QtGui.QPixmap("icons/clockFaceGrid.png")
        self.secPixMap = self.secPixMap.scaled(float(self.clockFrame.width()) * 0.6,
                                               float(self.clockFrame.height()) * 0.6, Qt.KeepAspectRatio)
        secHandDim = (self.secPixMap.width() ** 2 + self.secPixMap.height() ** 2) ** 0.5
        self.secHand.setGeometry(self.clockFrame.width() / 2 - secHandDim / 2, self.clockFrame.height() / 2 - secHandDim / 2, secHandDim,
                                 secHandDim)
        self.angle = now.second * 6
        transform = QtGui.QTransform().rotate(self.angle)
        self.secPixMap = self.secPixMap.transformed(transform, QtCore.Qt.SmoothTransformation)

        # ---- update label ----

        self.secHand.setPixmap(self.secPixMap)



        # self.clockFrame.show()

    ##Weather
    def Src(self):
        global text
        global temp
        global hum

        location_id = "CAXX0518"  # vancouver ID

        weather_com_result = pywapi.get_weather_from_weather_com(location_id)
        print(weather_com_result['current_conditions']['text'],
              weather_com_result['current_conditions']['temperature'] + "°",
              weather_com_result['current_conditions']['last_updated'],
              weather_com_result["current_conditions"]["humidity"])

        text = weather_com_result['current_conditions']['text']
        temp = weather_com_result['current_conditions']['temperature'] + "°C"
        hum = "☂ " + weather_com_result['current_conditions']['humidity'] + "%"

        self.Forecast()

    def Forecast(self):
        global text
        global temp
        global hum

        self.temp.setText(temp)
        self.hum.setText(hum)

        self.pic.show()
        self.temp.show()
        self.hum.show()

        if text == "Partly Cloudy" or text == "Fair" or text == "AM Clouds / PM Sun":
            self.pix = QtGui.QPixmap("icons/partly.png")
            self.pix = self.pix.scaled(picWidth, picHeight)
            self.pic.setPixmap(self.pix)

        elif text == "Cloudy" or text == "Mostly Cloudy":
            self.pix = QtGui.QPixmap("icons/cloudy.png")
            self.pix = self.pix.scaled(picWidth, picHeight)
            self.pic.setPixmap(self.pix)

        elif text == "Sunny" or text == "Mostly Sunny":
            self.pix = QtGui.QPixmap("icons/sunny.png")
            self.pix = self.pix.scaled(picWidth, picHeight)
            self.pic.setPixmap(self.pix)

        elif text == "Showers Early" or text == "Showers" or text == "AM Showers" or text == "Few Showers" or text == "Scattered Showers" or text == "Light Rain Shower":
            self.pix = QtGui.QPixmap("icons/rainy.png")
            self.pix = self.pix.scaled(picWidth, picHeight)
            self.pic.setPixmap(self.pix)

        elif text == "Clear" or text == "Mostly Clear":
            self.pix = QtGui.QPixmap("icons/clear.png")
            self.pix = self.pix.scaled(picWidth, picHeight)
            self.pic.setPixmap(self.pix)

        elif text == "Isolated T-Storms" or text == "PM T-Storms" or text == "Scattered T-Storms":
            self.pix = QtGui.QPixmap("icons/stormy.png")
            self.pix = self.pix.scaled(picWidth, picHeight)
            self.pic.setPixmap(self.pix)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    main = ClockandWeather()
    main.show()

    sys.exit(app.exec_())
