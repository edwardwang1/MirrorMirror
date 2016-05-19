#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, platform, signal
import datetime, time, json
import random
sys.dont_write_bytecode = True

from PyQt4 import QtGui, QtCore, QtNetwork
from PyQt4.QtGui import QPixmap, QMovie
from PyQt4.QtCore import Qt, QByteArray, QUrl, QFile, QIODevice
from PyQt4.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply, QNetworkProxy
from subprocess import Popen



def tick():
    global hourpixmap, minpixmap, secpixmap
    global hourpixmap2, minpixmap2, secpixmap2
    global lastmin
    global clockrect
    global datex, datex2, datey2

    now = datetime.datetime.now()
    angle = now.second * 6
    ts = secpixmap.size()
    secpixmap2 = secpixmap.transformed(
        QtGui.QMatrix().scale(
                float(clockrect.width())/ts.height(),
                float(clockrect.height())/ts.height()
                ).rotate(angle),
            Qt.SmoothTransformation
        )
    sechand.setPixmap(secpixmap2)
    ts = secpixmap2.size()
    sechand.setGeometry(
        clockrect.center().x()-ts.width()/2,
        clockrect.center().y()-ts.height()/2,
        ts.width(),
        ts.height()
    )
    if now.minute != lastmin:
        lastmin = now.minute
        angle = now.minute * 6
        ts = minpixmap.size()
        minpixmap2 = minpixmap.transformed(
                QtGui.QMatrix().scale(
                    float(clockrect.width())/ts.height(),
                    float(clockrect.height())/ts.height()
                    ).rotate(angle),
                Qt.SmoothTransformation
            )
        minhand.setPixmap(minpixmap2)
        ts = minpixmap2.size()
        minhand.setGeometry(
            clockrect.center().x()-ts.width()/2,
            clockrect.center().y()-ts.height()/2,
            ts.width(),
            ts.height()
        )

        angle = ((now.hour % 12) + now.minute / 60.0) * 30.0
        ts = hourpixmap.size()
        hourpixmap2 = hourpixmap.transformed(
                QtGui.QMatrix().scale(
                    float(clockrect.width())/ts.height(),
                    float(clockrect.height())/ts.height()
                    ).rotate(angle),
                Qt.SmoothTransformation
            )
        hourhand.setPixmap(hourpixmap2)
        ts = hourpixmap2.size()
        hourhand.setGeometry(
            clockrect.center().x()-ts.width()/2,
            clockrect.center().y()-ts.height()/2,
            ts.width(),
            ts.height()
        )
        # date
        sup = 'th'
        if (now.day == 1 or now.day == 21 or now.day == 31): sup = 'st'
        if (now.day == 2 or now.day == 22): sup = 'nd'
        if (now.day == 3 or now.day == 23): sup = 'rd'
        ds = "{0:%A %B} {0.day}<sup>".format(now)+sup+"</sup> {0.year}".format(now)
        datex.setText(ds)
        datex2.setText(ds)
        datey2.setText("{0:%I:%M %p}".format(now))

configname = 'Config'

if len(sys.argv) > 1:
    configname = sys.argv[1]

if not os.path.isfile(configname+".py"):
    print( "Config file not found %s" % configname+".py")
    exit(1)

Config = __import__(configname)

lastmin = -1
lastkeytime = 0;
lastapiget = time.time()

app = QtGui.QApplication(sys.argv)
desktop = app.desktop()
rec = desktop.screenGeometry()
height = rec.height()
width = rec.width()


w = QtGui.QWidget();
w.setWindowTitle(os.path.basename(__file__))
w.setStyleSheet("QWidget { background-color: black;}")


xscale = float(width)/1440.0
yscale = float(height)/900.0

frames = []
framep = 0


frame1 = QtGui.QFrame(w)
frame1.setObjectName("frame1")
frame1.setGeometry(0,0,width,height)
frame1.setStyleSheet("#frame1 { background-color: black;}")
frames.append(frame1)

frame2 = QtGui.QFrame(w)
frame2.setObjectName("frame2")
frame2.setGeometry(0,0,width,height)
frame2.setStyleSheet("#frame2 { background-color: blue;}")
frame2.setVisible(False)
frames.append(frame2)

squares1 = QtGui.QFrame(frame1)
squares1.setObjectName("squares1")
squares1.setGeometry(0,height-yscale*600,xscale*340,yscale*600)
squares1.setStyleSheet("#squares1 { background-color: transparent;}")

squares2 = QtGui.QFrame(frame1)
squares2.setObjectName("squares2")
squares2.setGeometry(width-xscale*340,0,xscale*340,yscale*900)
squares2.setStyleSheet("#squares2 { background-color: transparent;}")

clockface = QtGui.QFrame(frame1)
clockface.setObjectName("clockface")
clockrect = QtCore.QRect(width/2-height*.4, height*.45-height*.4,height * .8, height * .8)
clockface.setGeometry(clockrect)
clockface.setStyleSheet("#clockface { background-color: transparent;}")

hourhand = QtGui.QLabel(frame1)
hourhand.setObjectName("hourhand")
hourhand.setStyleSheet("#hourhand { background-color: transparent; }")

minhand = QtGui.QLabel(frame1)
minhand.setObjectName("minhand")
minhand.setStyleSheet("#minhand { background-color: transparent; }")

sechand = QtGui.QLabel(frame1)
sechand.setObjectName("sechand")
sechand.setStyleSheet("#sechand { background-color: transparent; }")


hourpixmap = QtGui.QPixmap(Config.hourhand)
hourpixmap2 = QtGui.QPixmap(Config.hourhand)
minpixmap = QtGui.QPixmap(Config.minhand)
minpixmap2 = QtGui.QPixmap(Config.minhand)
secpixmap = QtGui.QPixmap(Config.sechand)
secpixmap2 = QtGui.QPixmap(Config.sechand)
