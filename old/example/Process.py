#!/usr/bin/env python
# -*- coding: utf-8 -*-
from utils import text_type
from math import sin, cos
from PySide2.QtQuick import QQuickPaintedItem
from PySide2.QtGui import QPen, QPainter, QColor, QFont, QBrush
from PySide2.QtCore import Property, Signal, QUrl, Slot, QObject, Qt, QDataStream, QFile, QIODevice, SIGNAL, SLOT
from enum import IntEnum
from PySide2.QtQml import qmlRegisterType

class ProcessKnotType(IntEnum):
    Empty = 0
    Normal = 1
    Blocked = 2

class ProcessElement (QObject):
    def __init__(self, parent = None):
        QObject.__init__(self, parent)
        self.color = QColor("#333333")
        self.name = str()
        self.descriptionText = str()
        self.knotType = ProcessKnotType.Normal

class ProcessContainer (QObject):
    def __init__(self, parent = None):
        QObject.__init__(self, parent)
        self._elementsCount = 0
        self._isCyclic = False
        self._elements = []

    @Slot(result='bool')
    def getCyclic(self):
        return self._isCyclic

    @Slot(bool)
    def setCyclic(self, newValue):
        self._isCyclic = newValue
        self.objectUpdated.emit()

    @Slot(int)
    def setElementsCount(self, newElementsCount):
        diff = newElementsCount - self._elementsCount
        if diff > 0:
            for i in range(0, diff):
             anotherElement = ProcessElement()
             self._elements.append(anotherElement)
        elif diff < 0:
            for i in range(0,abs(diff)):
                 self._elements.pop( len(self._elements) - 1) #pop last
        self._elementsCount = newElementsCount
        self.objectUpdated.emit()

    @Slot(result='int')
    def getElementsCount(self):
        return self._elementsCount

    @Slot(int,result='QColor')
    def getElementColor(self, index):
        return self._elements[index].color

    @Slot(int,'QColor')
    def setElementColor(self, index, newColor):
        self._elements[index].color = newColor
        self.objectUpdated.emit()

    @Slot(int,result='QString')
    def getElementName(self, index):
        return self._elements[index].name

    @Slot(int,'QString')
    def setElementName(self, index, newName):
        self._elements[index].name = newName
        self.objectUpdated.emit()

    @Slot(int,result='QString')
    def getElementDescription(self, index):
        return self._elements[index].descriptionText

    @Slot(int,'QString')
    def setElementDescription(self, index, newDescription):
        self._elements[index].descriptionText = newDescription
        #self.objectUpdated.emit() - not really yeah?

    @Slot(int,result='int')
    def getElementType(self, index):
        return self._elements[index].knotType

    @Slot(int, int)
    def setElementType(self, index, newKnotType):
        self._elements[index].knotType = newKnotType
        self.objectUpdated.emit()

    @Slot('QString')
    def loadFromFile(self, filename):
        file = QFile(filename)
        file.open(QIODevice.ReadOnly)
        readStream = QDataStream(file)

        readStream >> self._elementsCount
        self.setElementsCount(self._elementsCount)
        readStream >> self._isCyclic

        for i in range (0,self._elementsCount):
            newColor = QColor(); readStream >> newColor; self.setElementColor(i,newColor)
            newName =  readStream.readQString(); self.setElementName(i,newName)
            newDescr = readStream.readQString(); self.setElementDescription(i,newDescr)
            newType = 1; readStream >> newType; self.setElementType(i,newType)
        self.objectUpdated.emit()

    @Slot('QString')
    def saveToFile(self, filename):
        file = QFile(filename)
        file.open(QIODevice.WriteOnly)
        newStream = QDataStream(file)
        newStream << self._elementsCount
        newStream << self._isCyclic
        for i in range (0,self._elementsCount):
            newStream << self.getElementColor(i)
            newStream << self.getElementName(i)
            newStream << self.getElementDescription(i)
            newStream << self.getElementType(i)
        file.close()

    #Signal to autoupdate process view
    objectUpdated = Signal()


class ProcessView (QQuickPaintedItem):
    def __init__(self, parent = None):
        QQuickPaintedItem.__init__(self, parent)
        self._containedObject = ProcessContainer()
        self._lineSize = 100
        self._backgroundColor = QColor('white')

    def getBGColor(self):
        return self._backgroundColor

    def setBGColor(self, value):
        self._backgroundColor = value

    def paint(self, painter):
        greenPen = QPen(QColor('green'), 2)
        blackPen = QPen(QColor('black'), 2)
        fullLineLen = self._lineSize * (self._containedObject.getElementsCount() - 1)

        xOffset = 10
        painter.fillRect(0,0,1000,600,self._backgroundColor)

        painter.setPen(blackPen)
        painter.setRenderHints(QPainter.Antialiasing, True);

        if self._containedObject.getCyclic() == False:
            painter.drawLine(xOffset,30,xOffset+fullLineLen,30)
            painter.setPen(greenPen)
            painter.drawLine(xOffset,32,xOffset+fullLineLen,32)
            painter.setPen(blackPen)
            painter.drawLine(xOffset,34,xOffset+fullLineLen,34)
        else:
            painter.drawEllipse(xOffset+10,30,self._lineSize*3,self._lineSize*3)

        anotherFont = painter.font()
        anotherFont.setPointSize(10)
        painter.setFont(anotherFont)

        totalElements = self._containedObject.getElementsCount()
        for i in range(0,totalElements):

            if self._containedObject.getCyclic() == False:
                knotX = xOffset + i*self._lineSize - 3
                knotY = 30
            else:
                degree = (totalElements-i)*360.0/totalElements + 180.0
                knotX = (self._lineSize*1.5)*sin(degree*3.14159265 / 180.0) + self._lineSize*1.5 + xOffset+10
                knotY = (self._lineSize*1.5)*cos(degree*3.14159265 / 180.0) + self._lineSize*1.5 + 30 #from above refactore yes

            localPen = QPen(self._containedObject.getElementColor(i),2)
            painter.setPen(localPen)

            elementType = self._containedObject.getElementType(i)

            if elementType == ProcessKnotType.Normal: #normal type - enumerate
                painter.drawEllipse(knotX,knotY,6,6)
                painter.drawEllipse(knotX-2,knotY-5,11,11)
            elif elementType == ProcessKnotType.Blocked:
                if self._containedObject.getCyclic() == False:
                    painter.drawLine(knotX,knotY-10,knotX,knotY+13) #blocked type - UPDATE FOR CYCLIC
                else:
                    dot1X = (self._lineSize*1.5+8)*sin(degree*3.14159265 / 180.0) + self._lineSize*1.5 + xOffset+10
                    dot1Y = (self._lineSize*1.5+8)*cos(degree*3.14159265 / 180.0) + self._lineSize*1.5 + 30
                    dot2X = (self._lineSize*1.5-8)*sin(degree*3.14159265 / 180.0) + self._lineSize*1.5 + xOffset+10
                    dot2Y = (self._lineSize*1.5-8)*cos(degree*3.14159265 / 180.0) + self._lineSize*1.5 + 30
                    painter.drawLine(dot1X,dot1Y,dot2X,dot2Y)

            if self._containedObject.getCyclic() == False:
                if i % 2 == 0:
                    painter.drawText(knotX,60,self._containedObject.getElementName(i))
                else:
                    painter.drawText(knotX,10,self._containedObject.getElementName(i))
            else:
                painter.drawText(knotX+20,knotY,self._containedObject.getElementName(i))

    @Slot(QObject)
    def setContainedObject(self, newObject):
        self._containedObject =  newObject
        QObject.connect(self._containedObject, SIGNAL('objectUpdated()'), self, SLOT('requestUpdate()'))

    @Slot()
    def requestUpdate(self):
        self.update()

    @Slot(int, int, result='int')
    def mouseHit(self, hitX, hitY):
        totalElements = self._containedObject.getElementsCount()
        for i in range(0,totalElements):
            if self._containedObject.getCyclic() == False:
                knotX = 10 + i*self._lineSize - 3 #10 is x offset
                if abs(knotX-hitX) < 30:
                    return i
            else:
                degree = (totalElements-i)*360.0/totalElements + 180.0
                knotX = (self._lineSize*1.5)*sin(degree*3.14159265 / 180.0) + self._lineSize*1.5 + 10+10  #10 is x offset
                knotY = (self._lineSize*1.5)*cos(degree*3.14159265 / 180.0) + self._lineSize*1.5 + 30 #from above refactore yes
                if abs(knotX-hitX) < 20 and abs(knotY-hitY) < 20:
                    return i

        return -1

    def getLineSize(self):
        return self._lineSize

    def setLineSize(self, newLineSize):
        self._lineSize = newLineSize

    backgroundColor = Property(QColor, getBGColor, setBGColor)
    lineSize = Property(int, getLineSize, setLineSize)


def registerQMLTypes():
    qmlRegisterType(ProcessView, 'Athenum', 1, 0, 'ProcessView');
    qmlRegisterType(ProcessContainer,'Athenum',1,0,'Process')

def getQMLTypes():
    theTypes = ['Process','ProcessView']
    return theTypes
