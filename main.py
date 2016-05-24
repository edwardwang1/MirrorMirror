#!/usr/bin/env python

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt
import sys
import pyowm
from datetime import datetime
import httplib2
import os
import oauth2client
from oauth2client import client
from oauth2client import tools
from apiclient import discovery
import pytz

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'MirrorMirror'


class ClockandWeather(QtGui.QWidget):
    ##clock variables
    # Emitted when the clock's time changes.
    timeChanged = QtCore.pyqtSignal(QtCore.QTime)
    # Emitted when the clock's time zone changes.
    timeZoneChanged = QtCore.pyqtSignal(int)

    ##weather variables
    global lastmin, picDimen
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
        self.weatherFrame.resize(500, 500)

        self.weatherIcon = QtGui.QLabel(self.weatherFrame)
        self.picDimen = self.weatherFrame.width() * 6 / 10
        self.weatherIcon.resize(self.picDimen, self.picDimen)
        self.weatherFrame.setStyleSheet("background-color: ")
        self.weatherPixMap = QtGui.QPixmap("")

        self.temp = QtGui.QLabel(self.weatherFrame)
        self.temp.setStyleSheet("font-size: 50px;")
        self.weatherDescrip = QtGui.QLabel(self.weatherFrame)
        self.weatherDescrip.setStyleSheet("font-size: 50px;")
        self.highLowFrame = QtGui.QFrame(self)
        self.high = QtGui.QLabel(self.highLowFrame)
        self.high.setStyleSheet("font-size: 25px;")
        self.low = QtGui.QLabel(self.highLowFrame)
        self.low.setStyleSheet("font-size: 25px;")

        # setting up grid layout for weather frame
        self.grid = QtGui.QGridLayout(self.weatherFrame)
        self.grid.addWidget(self.weatherIcon, 0, 0, 12, 12, QtCore.Qt.AlignBottom)
        self.grid.addWidget(self.temp, 3, 16, 8, 8, QtCore.Qt.AlignCenter)
        self.grid.addWidget(self.weatherDescrip, 12, 0, 1, 12, QtCore.Qt.AlignCenter)
        self.grid.addWidget(self.high, 8, 16, 4, 4, QtCore.Qt.AlignLeft)
        self.grid.addWidget(self.low, 8, 20, 4, 4, QtCore.Qt.AlignRight)

        self.Src()

        # ---------------------------Calendar Portion----------------------------
        self.calendarFrame = QtGui.QFrame(self)
        self.calendarFrame.move(1200, 300)
        self.calendarFrame.setStyleSheet("background-color: white; font-size: 50px;")
        self.calendarTitle = QtGui.QLabel(self.calendarFrame)
        self.calendarTitle.setText("Today's Events")
        self.calendarGrid = QtGui.QGridLayout(self.calendarFrame)
        self.calendarGrid.addWidget(self.calendarTitle, 0, 0, 1, 2, QtCore.Qt.AlignCenter)
        self.eventList = []
        self.updateCalendar()

        # ---------Window settings --------------------------------
        self.showFullScreen()
        # self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet("background-color: ")
        self.show()


        ##-----------------------------------clock-------------------------------------------------------

    def tick(self):
        global lastmin
        global clockrect
        now = datetime.now()

        # Rotate from initial image to avoid cumulative deformation from
        # transformation
        # --------second hand
        self.secPixMap = QtGui.QPixmap("icons/hourHand.png")
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
            self.hourPixMap = QtGui.QPixmap("icons/clockFaceGrid.png")
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

    ##-------------------------------------------------Weather------------------------------------------------
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

        self.temp.setText(str(int(tempDict['temp'])) + "°C")
        self.high.setText(str(int(tempDict['temp_max'])) + "°C")
        self.low.setText(str(int(tempDict['temp_min'])) + "°C")
        self.weatherDescrip.setText(descrip)

        self.weatherIcon.show()
        self.temp.show()

        if "cloud" in descrip.lower():
            self.weatherPixMap = QtGui.QPixmap("icons/cloudy.png")

        elif "snow" in descrip.lower():
            self.weatherPixMap = QtGui.QPixmap("icons/snowy.png")

        elif "rain" in descrip.lower():
            self.weatherPixMap = QtGui.QPixmap("icons/rainy.png")

        elif "clear" in descrip.lower():
            self.weatherPixMap = QtGui.QPixmap("icons/clear.png")

        elif "storm" in descrip.lower():
            self.weatherPixMap = QtGui.QPixmap("icons/stormy.png")

        elif "mist" in descrip.lower():
            self.weatherPixMap = QtGui.QPixmap("icons/misty.png")

        self.weatherPixMap = self.weatherPixMap.scaled(self.picDimen, self.picDimen)
        self.weatherIcon.setPixmap(self.weatherPixMap)

        # ------------------------------------Calendar-------------------------------------------------

    def get_credentials(self):
        try:
            import argparse

            flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
        except ImportError:
            flags = None
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'calendar-python-quickstart.json')

        store = oauth2client.file.Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
        return credentials

    def updateCalendar(self):
        """Shows basic usage of the Google Calendar API.

        Creates a Google Calendar API service object and outputs a list of the next
        10 events on the user's calendar.
        """
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)

        # calculates the start and the end of today in UTC
        tz = pytz.timezone("America/Vancouver")
        today = datetime.now(tz)
        midnightPrev = today.replace(hour=00, minute=00, second=00, microsecond=000000)
        midnightPrev = midnightPrev.astimezone(pytz.timezone("utc")).isoformat()
        midnightNext = today.replace(hour=23, minute=59, second=59, microsecond=999999)
        midnightNext = midnightNext.astimezone(pytz.timezone("utc")).isoformat()
        # now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        midnightPrev2 = midnightPrev[:-6] + 'Z'
        midnightNext2 = midnightNext[:-6] + 'Z'

        print('Getting the upcoming 10 events')
        eventsResult = service.events().list(
                calendarId='lauriej.chang@gmail.com', timeMin=midnightPrev2, timeMax=midnightNext2, maxResults=10,
                singleEvents=True,
                orderBy='startTime').execute()
        events = eventsResult.get('items', [])
        self.calendarFrame.resize(500, (len(events) + 1) * 100)
        self.eventList.clear()
        self.eventList = [[0 for x in range(2)] for y in range(len(events))]
        print(self.eventList)

        if not events:
            print('No upcoming events found.')

        for index, event in enumerate(events, start=0):
            self.eventList[index][0] = QtGui.QLabel(self.calendarFrame)
            self.eventList[index][1] = QtGui.QLabel(self.calendarFrame)
            start = event['start'].get('dateTime', event['start'].get('date'))
            start24 = start[11:16]
            d = datetime.strptime(start24, "%H:%M")
            start12 = d.strftime("%I:%M %p")
            self.eventList[index][0].setText(start12)
            self.eventList[index][1].setText(event['summary'])
            self.calendarGrid.addWidget(self.eventList[index][0], index + 1, 0, 1, 1, QtCore.Qt.AlignLeft)
            self.calendarGrid.addWidget(self.eventList[index][1], index + 1, 1, 1, 1, QtCore.Qt.AlignRight)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    main = ClockandWeather()
    main.show()

    sys.exit(app.exec_())
