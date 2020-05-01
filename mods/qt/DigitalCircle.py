#!/usr/bin/env python
# -*- coding: utf-8 -*-
from utils import text_type #check out it please
from PySide2.QtQuick import QQuickPaintedItem
from PySide2.QtGui import QPen, QPainter, QColor
from PySide2.QtCore import Property, Signal, Slot, QTimer, SIGNAL, SLOT
from PySide2.QtQml import qmlRegisterType
from math import sin, cos

from PySide2.QtQml import QJSValue


def registerQMLTypes():
    qmlRegisterType(DigitalCircle,'Athenum',1,0,'DigitalCircle')

def getQMLTypes():
    theTypes = ['DigitalCircle']
    return theTypes


class DigitalCircle(QQuickPaintedItem):
    def __init__(self,parent=None):
        QQuickPaintedItem.__init__(self,parent)
        self._oroborusFlag = True #radius, color, line width
        self._cycleFlag = True
        self._radius = 100
        self._borderOffset = 15
        #also please don't forget about multiple figures on one circle like we did before in C++
        self._digitsList = []
        self._scale = 0 #fix with 0?

    @Slot('QVariant',int, bool, bool)
    def set(self, digitsList, scale, cycleFlag, oroborusFlag):
        #print(type(digitsList), 'and check with', 'PySide2.QtQml.QJSValue')
        if type(digitsList) is QJSValue:
            digitsList = digitsList.toVariant()
        #print('Debug circle set',digitsList,scale,cycleFlag,oroborusFlag)
        self._digitsList = digitsList
        self._scale = scale
        self._cycleFlag = cycleFlag
        self._oroborusFlag = oroborusFlag
        self.update()

    #set/get for radius, and border offset maybe, and line width at least, color is good too
    #best to make them all properties

    def paint(self, painter):
        painter.drawEllipse(self._borderOffset, self._borderOffset, self._radius*2,self._radius*2)
        if self._scale == 0 or len(self._digitsList) == 0:
            return
        self.drawNotation(painter)
        for i in range(1, len(self._digitsList)):
            prevDigit = self._digitsList[i-1]
            currentDigit = self._digitsList[i]
            self.drawLine(painter, prevDigit, currentDigit)
        if self._cycleFlag:
            firstDigit = self._digitsList[0]
            lastDigit = self._digitsList[-1]
            self.drawLine(painter, lastDigit, firstDigit)


    def drawLine(self, painter, start, end):
        scale = self._scale
        radius = self._radius
        if self._oroborusFlag == True:
            scale -= 1
        degree1 = (scale - start) * 360.0 / scale
        y1 = radius * cos(degree1 * 3.14159265 / 180.0)
        x1 = radius * sin(degree1 * 3.14159265 / 180.0)
        degree2 = (scale - end) * 360.0 / scale
        y2 = radius * cos(degree2 * 3.14159265 / 180.0)
        x2 = radius * sin(degree2 * 3.14159265 / 180.0)
        radius += self._borderOffset #this is fast way to shift it all
        painter.drawLine(radius-x1, radius-y1, radius-x2, radius-y2)


    def drawNotation(self, painter):
        scale = self._scale
        radius = self._radius
        if self._oroborusFlag == True:
            scale -= 1
        for i in range(0, scale):
            degree = (scale - i) * 360.0 / scale
            x = radius * sin(degree * 3.14159265 / 180.0)
            y = radius * cos(degree * 3.14159265 / 180.0)
            xWide = (radius + 10) * sin(degree * 3.14159265 / 180.0)
            yWide = (radius + 10) * cos(degree * 3.14159265 / 180.0)
            painter.drawEllipse(radius - x + self._borderOffset, radius - y + self._borderOffset, 3, 3)
            if i == 0 and self._oroborusFlag == True:
                digitText = str(scale)
            else:
                digitText = str(i)
            painter.drawText(radius - xWide + self._borderOffset, radius - yWide + self._borderOffset - 5, 20, 20, 0, digitText)
            #-5 looks not good, better cover it all to make more readable later


    @Slot(int)
    def setRadius(self, newRadius):
        self._radius = newRadius
        self.update()
    def getRadius(self):
        return self._radius

    def setBorderOffset(self, newBorderOffset):
        self._borderOffset = newBorderOffset
        self.update()
    def getBorderOffset(self):
        return self._borderOffset

    radius = Property(int, getRadius, setRadius)
    borderOffset = Property(int, getBorderOffset, setBorderOffset)

    #color
    #widthOfLine



