#!/usr/bin/env python

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt
import sys
import pywapi

class ClockandWeather(QtGui.QWidget):
    ##clock variables
    # Emitted when the clock's time changes.
    timeChanged = QtCore.pyqtSignal(QtCore.QTime)
    # Emitted when the clock's time zone changes.
    timeZoneChanged = QtCore.pyqtSignal(int)

    ##weather variables
    global picWidth
    global picHeight
    picWidth = 128
    picHeight = 128

    def __init__(self, parent=None):

        ##clock
        super(ClockandWeather, self).__init__(parent)

        self.timeZoneOffset = 0

        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update)
        timer.timeout.connect(self.updateTime)
        timer.start(1000)

        self.setWindowTitle(QtCore.QObject.tr(self, "Analog Clock"))
        self.resize(200, 200)

        self.hourHand = QtGui.QPolygon([
            QtCore.QPoint(7, 8),
            QtCore.QPoint(-7, 8),
            QtCore.QPoint(0, -40)
        ])
        self.minuteHand = QtGui.QPolygon([
            QtCore.QPoint(7, 8),
            QtCore.QPoint(-7, 8),
            QtCore.QPoint(0, -70)
        ])

        self.hourColor = QtGui.QColor(0, 127, 0)
        self.minuteColor = QtGui.QColor(0, 127, 127, 191)

        ##weather
        QtGui.QWidget.__init__(self)
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

        self.Src();

        # ---------Window settings --------------------------------
        self.setGeometry(300,300,750,500)
        self.setFixedSize(760,520)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet("background-color:")
        self.show()

    ##clock
    def paintEvent(self, event):

        side = min(self.width(), self.height())
        time = QtCore.QTime.currentTime()
        time = time.addSecs(self.timeZoneOffset * 3600)

        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)
        painter.scale(side / 200.0, side / 200.0)

        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtGui.QBrush(self.hourColor))

        painter.save()
        painter.rotate(30.0 * ((time.hour() + time.minute() / 60.0)))
        painter.drawConvexPolygon(self.hourHand)
        painter.restore()

        painter.setPen(self.hourColor)

        for i in range(0, 12):
            painter.drawLine(88, 0, 96, 0)
            painter.rotate(30.0)

        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtGui.QBrush(self.minuteColor))

        painter.save()
        painter.rotate(6.0 * (time.minute() + time.second() / 60.0))
        painter.drawConvexPolygon(self.minuteHand)
        painter.restore()

        painter.setPen(QtGui.QPen(self.minuteColor))

        for j in range(0, 60):
            if (j % 5) != 0:
                painter.drawLine(92, 0, 96, 0)
            painter.rotate(6.0)

        painter.end()

    def minimumSizeHint(self):

        return QtCore.QSize(50, 50)

    def sizeHint(self):

        return QtCore.QSize(100, 100)

    def updateTime(self):

        self.timeChanged.emit(QtCore.QTime.currentTime())

    # The timeZone property is implemented using the getTimeZone() getter
    # method, the setTimeZone() setter method, and the resetTimeZone() method.

    # The getter just returns the internal time zone value.
    def getTimeZone(self):

        return self.timeZoneOffset

    # The setTimeZone() method is also defined to be a slot. The @pyqtSlot
    # decorator is used to tell PyQt which argument type the method expects,
    # and is especially useful when you want to define slots with the same
    # name that accept different argument types.

    @QtCore.pyqtSlot(int)
    def setTimeZone(self, value):

        self.timeZoneOffset = value
        self.timeZoneChanged.emit(value)
        self.update()

    # Qt's property system supports properties that can be reset to their
    # original values. This method enables the timeZone property to be reset.
    def resetTimeZone(self):

        self.timeZoneOffset = 0
        self.timeZoneChanged.emit(0)
        self.update()

    # Qt-style properties are defined differently to Python's properties.
    # To declare a property, we call pyqtProperty() to specify the type and,
    # in this case, getter, setter and resetter methods.
    timeZone = QtCore.pyqtProperty(int, getTimeZone, setTimeZone, resetTimeZone)

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
            self.pix = self.pix.scaled(picWidth,picHeight)
            self.pic.setPixmap(self.pix)

        elif text == "Cloudy" or text == "Mostly Cloudy":
            self.pix = QtGui.QPixmap("icons/cloudy.png")
            self.pix = self.pix.scaled(picWidth,picHeight)
            self.pic.setPixmap(self.pix)

        elif text == "Sunny" or text == "Mostly Sunny":
            self.pix = QtGui.QPixmap("icons/sunny.png")
            self.pix = self.pix.scaled(picWidth,picHeight)
            self.pic.setPixmap(self.pix)

        elif text == "Showers Early" or text == "Showers" or text == "AM Showers" or text == "Few Showers" or text == "Scattered Showers" or text == "Light Rain Shower":
            self.pix = QtGui.QPixmap("icons/rainy.png")
            self.pix = self.pix.scaled(picWidth,picHeight)
            self.pic.setPixmap(self.pix)

        elif text == "Clear" or text == "Mostly Clear":
            self.pix = QtGui.QPixmap("icons/clear.png")
            self.pix = self.pix.scaled(picWidth,picHeight)
            self.pic.setPixmap(self.pix)

        elif text == "Isolated T-Storms" or text == "PM T-Storms" or text == "Scattered T-Storms":
            self.pix = QtGui.QPixmap("icons/stormy.png")
            self.pix = self.pix.scaled(picWidth,picHeight)
            self.pic.setPixmap(self.pix)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    main = ClockandWeather()
    main.show()

    sys.exit(app.exec_())