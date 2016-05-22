from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt
import sys
import pywapi


class Main(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)

        #self.setWindowFlags(Qt.FramelessWindowHint)
        #self.setStyleSheet("background-color:")

        self.clock = Clock2(self)
        self.weather = Weather(self)
        self.setCentralWidget(self.weather)

        self.resize(500,500)
        self.layout = QtGui.QGridLayout()
        #self.layout.addWidget(self.clock, 5, 0)
        #self.layout.addWidget(self.weather, 0, 1)


        self.show()


class Clock2(QtGui.QWidget):
    def __init__(self, parent):
        super(Clock2, self).__init__(parent)
        minWidth = 100
        minHeight = 200

        self.hourPixMap2 = QtGui.QPixmap("")
        self.minPixMap2 = QtGui.QPixmap("")
        self.secPixMap2 = QtGui.QPixmap("")
        self.hourHand = QtGui.QLabel(self)
        self.minHand = QtGui.QLabel(self)
        self.secHand = QtGui.QLabel(self)

        self.hourPixMap = QtGui.QPixmap("icons/hourhand.png")
        self.hourPixMap = self.hourPixMap.scaled(minWidth, minHeight, Qt.KeepAspectRatio)

        self.minPixMap = QtGui.QPixmap("icons/minutehand.png")
        self.minPixMap = self.minPixMap.scaled(minWidth, minHeight, Qt.KeepAspectRatio)

        self.secPixMap = QtGui.QPixmap("icons/sechand.png")

        self.hourHand.setPixmap(self.hourPixMap)
        self.secHand.setPixmap(self.secPixMap)

        self.minHand.move(0, 0)
        self.minHand.resize(minWidth, minHeight)
        self.minHand.setPixmap(self.minPixMap)
        self.minHand.show()

        self.hourHand.move(minWidth + 15, 0)
        self.hourHand.resize(minWidth, minHeight)
        self.hourHand.setPixmap(self.hourPixMap)
        self.hourHand.show()
        self.show()


class Weather(QtGui.QWidget):
    global picWidth
    global picHeight
    picWidth = 128
    picHeight = 128

    def __init__(self, parent):
        super(Weather, self).__init__(parent)
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
        self.temp.setStyleSheet("font-size:50px;")

        self.hum.move(410, 160)
        self.hum.resize(250, 100)
        self.hum.setStyleSheet("font-size:50px;")

        self.Src();

        self.show()

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
    main = Main()
    main.show()

    sys.exit(app.exec_())
