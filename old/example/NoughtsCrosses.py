#!/usr/bin/env python
# -*- coding: utf-8 -*-
from utils import text_type
from PySide2.QtQuick import QQuickPaintedItem
from PySide2.QtGui import QPen, QPainter, QColor
from PySide2.QtCore import Property, Signal, QUrl, Slot
from PySide2.QtQml import qmlRegisterType

class NoughtsCrosses (QQuickPaintedItem):
    def __init__(self, parent = None):
        QQuickPaintedItem.__init__(self, parent)
        self._cellsList = [0]*9
        self._backgroundColor = QColor('white')
        'In future we could made changable cells count from 3x3 till 7x7,'
        'and algo to detect win from 3to6 together, and also 2-4 players'

    def getBGColor(self):
        return self._backgroundColor

    def setBGColor(self, value):
        self._backgroundColor = value

    def paint(self, painter):
        pen = QPen(self.color, 2)
        painter.fillRect(0,0,300,300,self._backgroundColor)
        painter.setPen(pen);
        painter.setRenderHints(QPainter.Antialiasing, True);
        painter.drawRect(0,0,300,300)
        painter.drawLine(0,100,300,100)  #there would be for cycle to draw the line for 3x3 up to 7x7
        painter.drawLine(0,200,300,200)
        painter.drawLine(100,0,100,300)
        painter.drawLine(200,0,200,300)
        for i in range(0, 9):
            if self._cellsList[i] > 0:
                xCell = i % 3           #seams here we can see the algo for 7x7 its i%7 and i/7
                yCell = int(i / 3)
                xCenter = 25 + xCell*100
                yCenter = 25 + yCell*100
                if self._cellsList[i] == 1:
                    painter.drawEllipse(xCenter,yCenter,50,50)
                elif self._cellsList[i] == 2:
                    painter.drawLine(xCenter,yCenter,xCenter+50,yCenter+50)
                    painter.drawLine(xCenter+50,yCenter,xCenter,yCenter+50)

    @Slot(int, int, result='int')
    def mouseHit(self, hitX, hitY):
        xCell = int(hitX / 100) #cellSize
        yCell = int(hitY / 100)
        cellNum = xCell + (yCell)*3
        return cellNum

    @Slot(int, int, result='bool')
    def setValue(self, cell, newValue):
        if self._cellsList[cell] == 0:
            self._cellsList[cell] = newValue
            return True
        return False

    @Slot(result='int') #alfo will have to be shifted, to work from 2 to 6 points on different fields sizes
    def checkWin(self):
        if self._cellsList[0] == self._cellsList[1] and self._cellsList[1] == self._cellsList[2] : return self._cellsList[0]
        if self._cellsList[3] == self._cellsList[4] and self._cellsList[4] == self._cellsList[5] : return self._cellsList[3]
        if self._cellsList[6] == self._cellsList[7] and self._cellsList[7] == self._cellsList[8] : return self._cellsList[6]
        if self._cellsList[0] == self._cellsList[3] and self._cellsList[3] == self._cellsList[6] : return self._cellsList[0]
        if self._cellsList[1] == self._cellsList[4] and self._cellsList[4] == self._cellsList[7] : return self._cellsList[1]
        if self._cellsList[2] == self._cellsList[5] and self._cellsList[5] == self._cellsList[8] : return self._cellsList[2]
        if self._cellsList[0] == self._cellsList[4] and self._cellsList[4] == self._cellsList[8] : return self._cellsList[0]
        if self._cellsList[2] == self._cellsList[4] and self._cellsList[4] == self._cellsList[6] : return self._cellsList[2]
        return 0

    def getColor(self):
        return self._color
    def setColor(self, value):
        self._color = value
    @Slot()
    def requestUpdate(self):
        self.update()
    @Slot()
    def reset(self):
        self._cellsList = [0]*9 #will depend on real size when changable

    color = Property(QColor, getColor, setColor)
    backgroundColor = Property(QColor, getBGColor, setBGColor)

def registerQMLTypes():
    qmlRegisterType(NoughtsCrosses, 'Athenum', 1, 0, 'NoughtsCrosses');

def getQMLTypes():
    theTypes = ['NoughtsCrosses']
    return theTypes
