import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt

import pywapi


class Main(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.pix = QtGui.QPixmap("")
        self.pic = QtGui.QLabel(self)
        self.loc = QtGui.QLabel(self)
        self.temp = QtGui.QLabel(self)
        self.hum = QtGui.QLabel(self)
        self.text = QtGui.QLabel(self)
        self.time = QtGui.QLabel(self)
        self.initUI()

    def initUI(self):
        self.pic.move(90, 110)
        self.pic.resize(128, 128)
        self.pic.setPixmap(self.pix)

        self.loc.move(250, 90)
        self.loc.resize(500, 100)
        self.loc.setStyleSheet("font-size: 30px; font-color: #FFFFFF;")

        self.temp.move(250, 160)
        self.temp.resize(150, 100)
        self.temp.setStyleSheet("font-size:50px; font-color: #FFFFFF;")

        self.hum.move(410, 160)
        self.hum.resize(250, 100)
        self.hum.setStyleSheet("font-size:50px;")

        self.text.move(70, 236)
        self.text.resize(180, 50)
        self.text.setStyleSheet("font-size: 20px;")
        self.text.setAlignment(Qt.AlignCenter)

        self.time.move(250, 211)
        self.time.resize(400, 100)
        self.time.setStyleSheet("font-size: 20px;")

        self.Src();

        # ---------Window settings --------------------------------
        self.setGeometry(300,300,750,500)
        self.setFixedSize(760,520)
        self.setWindowTitle("PySun")
        self.setWindowIcon(QtGui.QIcon("icons/partly.png"))
        self.setStyleSheet("background-color: #01060E")
        #self.setStyleSheet("background-color:")
        self.show()

    def Src(self):
        global text
        global temp
        global loc
        global time
        global hum

        location_id = "CAXX0518"  # vancouver ID
        loc = "Vancouver,BC"

        weather_com_result = pywapi.get_weather_from_weather_com(location_id)
        print(weather_com_result['current_conditions']['text'],
              weather_com_result['current_conditions']['temperature'] + "°",
              weather_com_result['current_conditions']['last_updated'],
              weather_com_result["current_conditions"]["humidity"])

        text = weather_com_result['current_conditions']['text']
        temp = weather_com_result['current_conditions']['temperature'] + "°C"
        time = "last updated " + weather_com_result['current_conditions']['last_updated']
        hum = "☂ " + weather_com_result['current_conditions']['humidity'] + "%"

        self.Forecast()

    def Forecast(self):
        global text
        global temp
        global loc
        global time
        global hum

        self.loc.setText(loc)
        self.temp.setText(temp)
        self.text.setText(text)
        self.time.setText(time)
        self.hum.setText(hum)

        self.text.show()
        self.time.show()
        self.pic.show()
        self.temp.show()
        self.loc.show()
        self.hum.show()

        if text == "Partly Cloudy" or text == "Fair" or text == "AM Clouds / PM Sun":
            self.pix = QtGui.QPixmap("icons/partly.png")
            self.pic.setPixmap(self.pix)

        elif text == "Cloudy" or text == "Mostly Cloudy":
            self.pix = QtGui.QPixmap("icons/cloudy.png")
            self.pic.setPixmap(self.pix)

        elif text == "Sunny" or text == "Mostly Sunny":
            self.pix = QtGui.QPixmap("icons/sunny.png")
            self.pic.setPixmap(self.pix)

        elif text == "Showers Early" or text == "Showers" or text == "AM Showers" or text == "Few Showers" or text == "Scattered Showers" or text == "Light Rain Shower":
            self.pix = QtGui.QPixmap("icons/rainy.png")
            self.pic.setPixmap(self.pix)

        elif text == "Clear" or text == "Mostly Clear":
            self.pix = QtGui.QPixmap("icons/clear.png")
            self.pic.setPixmap(self.pix)
            self.pic.move(110, 110)

        elif text == "Isolated T-Storms" or text == "PM T-Storms" or text == "Scattered T-Storms":
            self.pix = QtGui.QPixmap("icons/stormy.png")
            self.pic.setPixmap(self.pix)


def main():
    app = QtGui.QApplication(sys.argv)
    main = Main()
    main.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
