#!/usr/bin/env python
# -*- coding: utf-8 -*-
from utils import text_type
from PySide2.QtQuick import QQuickPaintedItem
from PySide2.QtGui import QPen, QPainter, QColor
from PySide2.QtCore import Property, Signal, QUrl, Slot, QTimer, SIGNAL, SLOT, QObject, QDir
from PySide2.QtQml import qmlRegisterType
from math import sin, cos
import subprocess
import os

class OSforQML(QObject):
    def __init__(self,parent=None):
        QObject.__init__(self,parent)

    @Slot('QString')
    def execute(self, commandLine): # - this function could be created better using some ffmpeg library, but yet just fast way
        #PATH MUST BECOME RELATED not ABSOLUTE
        os.chdir("/home/constcut/dev/projects/athenum/temp/render")
        #//THIS IS WRONG: ATTENTION - MAKE PATH CUTTER IN JavaScript utils
        subprocess.call([commandLine],shell=True) #should be many checks here - first one that its a string
        os.chdir("/home/constcut/dev/projects/athenum") #sorry yet unfammiliar
        #//THIS IS WRONG: ATTENTION - MAKE PATH CUTTER IN JavaScript utils

    @Slot('QString','QString')
    def cleanDir(self, dir, extension): # - this function needed only because of wiered image rendering for video - it also could be improved muc
        dir = QDir("/home/constcut/dev/projects/athenum/temp/render") #//THIS IS WRONG: ATTENTION - MAKE PATH CUTTER IN JavaScript utils
        dir.setNameFilters(['*.png'])
        dir.setFilter(QDir.Files)
        files = dir.entryList()
        for i, filename in enumerate(files):
            dir.remove(filename)


class Animation (QQuickPaintedItem):
    def __init__(self, parent = None):
        QQuickPaintedItem.__init__(self, parent)
        self._status = 0
        self._timer = QTimer()
        QObject.connect(self._timer, SIGNAL('timeout()'), self, SLOT('requestSpecialUpdate()'))
        self._timer.setInterval(50)
        self._backgroundColor = QColor('white')

    def getBGColor(self):
        return self._backgroundColor

    def setBGColor(self, value):
        self._backgroundColor = value

    def paint(self, painter):
        pen = QPen(QColor(self._status*179%180,self._status*239%240,220-self._status*219%220), 10)
        painter.setPen(pen);
        painter.setRenderHints(QPainter.Antialiasing, True);

        painter.fillRect(0,0,300,300,self._backgroundColor)
        painter.drawRect(0,0,300,300)

        #painter.drawEllipse(self._status % 300, 30, 5,5)
        #painter.drawEllipse(30, self._status*2 % 300, 5,5)
        #painter.drawEllipse(self._status*3 % 300,self._status*3 % 300,5,5)
        #painter.drawEllipse(self._status*4 % 300,300 -(self._status*4 % 300),5,5)
        #painter.drawEllipse(self._status*5 % 300,150,5,5)

        degree = (360-(self._status*3 %360)) + 180.0
        knotX = (75*1.5)*sin(degree*3.14159265 / 180.0) + 100*1.5
        knotY = (75*1.5)*cos(degree*3.14159265 / 180.0) + 100*1.5
        painter.drawEllipse(knotX,knotY,5,5)

        degree1 = (360-(360- (self._status*3 %360))) + 180.0
        knotX1 = (75*1.5)*sin(degree1*3.14159265 / 180.0) + 100*1.5
        knotY1 = (75*1.5)*cos(degree1*3.14159265 / 180.0) + 100*1.5
        painter.drawEllipse(knotX1,knotY1,5,5)

        degree2 = (360-(self._status*5 %360)) + 180.0
        knotX2 = (75*1.5)*sin(degree2*3.14159265 / 180.0) + 100*1.5
        knotY2 = (75*1.5)*cos(degree2*3.14159265 / 180.0) + 100*1.5
        painter.drawEllipse(knotX2,knotY2,5,5)

        degree3 = (360-(360- (self._status*5%360) )) + 180.0
        knotX3 = (75*1.5)*sin(degree3*3.14159265 / 180.0) + 100*1.5
        knotY3 = (75*1.5)*cos(degree3*3.14159265 / 180.0) + 100*1.5
        painter.drawEllipse(knotX3,knotY3,5,5)

        degree4 = (360-(self._status*7%360)) + 180.0
        knotX4 = (75*1.5)*sin(degree4*3.14159265 / 180.0) + 100*1.5
        knotY4 = (75*1.5)*cos(degree4*3.14159265 / 180.0) + 100*1.5
        painter.drawEllipse(knotX4,knotY4,5,5)

        degree5 = (360-(360- (self._status*7%360))) + 180.0
        knotX5 = (75*1.5)*sin(degree5*3.14159265 / 180.0) + 100*1.5
        knotY5 = (75*1.5)*cos(degree5*3.14159265 / 180.0) + 100*1.5
        painter.drawEllipse(knotX5,knotY5,5,5)

        painter.drawLine(150,150,knotX,knotY)
        painter.drawLine(150,150,knotX1,knotY1)
        painter.drawLine(150,150,knotX2,knotY2)
        painter.drawLine(150,150,knotX3,knotY3)
        painter.drawLine(150,150,knotX4,knotY4)
        painter.drawLine(150,150,knotX5,knotY5)


    def getColor(self):
        return self._color
    def setColor(self, value):
        self._color = value

    @Slot(int)
    def setInterval(self,newInterval):
        self._timer.setInterval(newInterval)

    @Slot()
    def stop(self):
        self._timer.stop()

    @Slot()
    def start(self):
        self._timer.start()

    @Slot(result='bool')
    def isRunning(self):
        return self._timer.isActive()

    @Slot()
    def requestSpecialUpdate(self):
        self._status = self._status + 1
        self.update()

    @Slot()
    def reset(self):
        self._cellsList = [0]*9 #will depend on real size when changable

    color = Property(QColor, getColor, setColor)
    backgroundColor = Property(QColor, getBGColor, setBGColor)

def registerQMLTypes():
    qmlRegisterType(Animation, 'Athenum', 1, 0, 'PolyRythm');
    qmlRegisterType(OSforQML, 'Athenum', 1, 0, 'OSforQML');

def getQMLTypes():
    theTypes = ['PolyRythm','OSforQML']
    return theTypes
