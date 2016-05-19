import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt

import pywapi


class Main(QtGui.QMainWindow):
    global picWidth
    global picHeight
    picWidth = 128
    picHeight = 128

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
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


def main():
    app = QtGui.QApplication(sys.argv)
    main = Main()
    main.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
