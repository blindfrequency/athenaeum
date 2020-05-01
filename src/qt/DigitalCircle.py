#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from utils import text_type #check out it please
from qtpy.QtQuick import QQuickPaintedItem
from qtpy.QtGui import QPen, QPainter, QColor, QBrush
from qtpy.QtCore import Property, Signal, Slot, QTimer, Qt, QObject, SIGNAL, SLOT
from qtpy.QtQml import qmlRegisterType
from math import sin, cos

from qtpy.QtQml import QJSValue


def registerQMLTypes():
    qmlRegisterType(DigitalCircle,'Athenum',1,0,'DigitalCircle')
    qmlRegisterType(DigitalCircleList,'Athenum',1,0,'DigitalCircleList')


def getQMLTypes():
    theTypes = ['DigitalCircle','DigitalCircleList']
    return theTypes

class DigitalCircleList(QQuickPaintedItem):
    def __init__(self,parent=None):
        QQuickPaintedItem.__init__(self,parent)
        self._circles = []
        self._timer = QTimer()
        #pyqtSignal need to rewrite here to make possible usage
        QObject.connect(self._timer, SIGNAL('timeout()'), self, SLOT('requestSpecialUpdate()'))
        self._speedRatio = 1.0
        self._timerInterval = 25 * self._speedRatio

    @Slot(result='QString')
    def exportJson(self):
        jsonString = '{"circles": ['
        totalCount = 0
        for c in self._circles:
            expStr = c.exportJson()
            totalCount += 1
            if totalCount < len(self._circles):
                jsonString += expStr + ","
            else:
                jsonString += expStr
        jsonString += "]}"
        return jsonString

    @Slot('QString')
    def importJson(self, jsonString):
        from qtpy.QtCore import QJsonDocument, QByteArray, QJsonArray
        jBytes = QByteArray(jsonString.encode())
        jDoc = QJsonDocument.fromJson(jBytes)
        jObj = jDoc.object()
        #MAKE NEW PAGE CIRCLES
        #print(jObj, jDoc.isObject(), jDoc.isEmpty(), jDoc.isNull(), jDoc.isArray())
        circles = jObj["circles"]
        for c in circles:
            pass
            #print(c, " - circle")
        self.update()

    @Slot('QVariant',int, bool, bool, 'QColor')
    def add(self, digitsList, scale, cycleFlag, oroborusFlag, dotColor):

       #print("Adding new circle ",digitsList,scale,cycleFlag,oroborusFlag)

       c = DigitalCircle()
       c.set(digitsList, scale, cycleFlag, oroborusFlag)
       c.setDotColor(dotColor)
       self._circles.append(c)
       self.update()

    @Slot(result='int')
    def size(self):
        return len(self._circles)

    @Slot(int)
    def remove(self, index):
        c = self._circles.pop(index)
        self.update()

    def paint(self, painter):
        if len(self._circles) == 0:
            return
        for c in self._circles:
            c.paintWithoutNotation(painter)
        self._circles[0].drawNotation(painter) #Only if all are the same - maybe let to chose

    @Slot(float)
    def setSpeedRatio(self, newRate):
        self._speedRatio = newRate
        self._timerInterval = 25 * self._speedRatio
        self._timer.setInterval(self._timerInterval)
        #for c in self._circles:
        #    c.setSpeedRatio(newRate)

    @Slot()
    def startAnimation(self):

        if len(self._circles) == 0:
            return

        for c in self._circles:
            if len(c._digitsList) == 0:
                continue
            c.prepareAnimation()
        self._timer.setInterval(self._timerInterval)
        self._timer.start()

    @Slot()
    def requestSpecialUpdate(self):
        for c in self._circles:
            c.requestSpecialUpdateSafe()
        self.update()


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
        self._posX = 0
        self._posY = 0
        self._speedRatio = 1.0
        self._timerInterval = 25 * self._speedRatio
        self._animationIndex = 0
        self._timer = QTimer() 
        #PySide2
        QObject.connect(self._timer, SIGNAL('timeout()'), self, SLOT('requestSpecialUpdate()'))
        #PyQt
        #and here pyqtSignal
        self._dotColor = QColor(Qt.green)
        self._lineWidth = 1
        self._lineColor = QColor(Qt.black)

    @Slot(result='QString')
    def exportJson(self):
        from qtpy.QtCore import QJsonDocument, QByteArray, QJsonArray
        jDoc = QJsonDocument()
        jObj = dict()
        if self._oroborusFlag == False:
            jObj["oroborusFlag"] = self._oroborusFlag
        if self._cycleFlag == False:
            jObj["cycleFlag"] = self._cycleFlag
        if self._radius != 100:
            jObj["radius"] = self._radius
        if self._speedRatio != 1.0:
            jObj["speedRatio"] = self._speedRatio
        if self._lineWidth != 1:
            jObj["lineWidth"] = self._lineWidth
        #jObj["digits"] = len(self._digitsList) #QJsonArray.fromVariantList(self._digitsList)
        digitsArray = QJsonArray()
        for d in self._digitsList:
            digitsArray.append(int(d))
        jObj["digits"] = digitsArray
        jObj["scale"] = self._scale

        if self._dotColor !=  QColor(Qt.green):
            jObj["dotColor"] = self._dotColor.name()
        if self._lineColor !=  QColor(Qt.black):
            jObj["lineColor"] = self._lineColor.name()
        jDoc.setObject(jObj)
        jsonString = jDoc.toJson(QJsonDocument.Compact).data().decode() #'utf-8'
        #print("EXP STR_",jsonString)
        return jsonString


    @Slot('QString')
    def importJson(self, jsonString):
        from qtpy.QtCore import QJsonDocument, QByteArray, QJsonArray
        jBytes = QByteArray(jsonString.encode())
        jDoc = QJsonDocument.fromJson(jBytes)
        jObj = jDoc.object()
        if "oroborusFlag" in jObj:
            self._oroborusFlag = jObj["oroborusFlag"]
        else:
            self._oroborusFlag = True
        if "cycleFlag" in jObj:
            self._cycleFlag = jObj["cycleFlag"]
        else:
            self._cycleFlag = True
        if "radius" in jObj:
            self._radius = jObj["radius"]
        else:
            self._radius = 100
        if "speedRatio" in jObj:
            self._speedRatio = jObj["speedRatio"]
        else:
            self._speedRatio = 1.0
        if "lineWidth" in jObj:
            self._lineWidth = jObj["lineWidth"]
        else:
            self._lineWidth = 1
        if "dotColor" in jObj:
            self._dotColor = QColor(jObj["dotColor"])
        else:
            self._dotColor = QColor(Qt.green)
        if "lineColor" in jObj:
            self._lineColor = QColor(jObj["lineColor"])
        else:
            self._lineColor = QColor(Qt.green)
        self._digitsList = jObj["digits"]
        self._scale = int(jObj["scale"])
        self.update()


    @Slot(float)
    def setSpeedRatio(self, newRate):
        self._speedRatio = newRate
        self._timerInterval = 25 * self._speedRatio
        self._timer.setInterval(self._timerInterval)

    @Slot('QColor')
    def setDotColor(self, newColor):
        self._dotColor = newColor

    @Slot('QColor')
    def setLineColor(self, newColor):
        self._lineColor = newColor

    @Slot(int)
    def setLineWidth(self, newLineWidth):
        self._lineWidth = newLineWidth

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
        brushBackup = painter.brush()
        self.paintWithoutNotation(painter)
        self.drawNotation(painter)
        painter.setBrush(brushBackup)

    def paintWithoutNotation(self, painter):
        brushBackup = painter.brush()
        penBackup = painter.pen()
        localPen = QPen(self._lineColor)
        localPen.setWidth(self._lineWidth)
        painter.setPen(localPen)
        painter.drawEllipse(self._borderOffset, self._borderOffset, self._radius*2,self._radius*2)
        if self._scale == 0 or len(self._digitsList) == 0:
            return
        for i in range(1, len(self._digitsList)):
            prevDigit = self._digitsList[i-1]
            currentDigit = self._digitsList[i]
            self.drawLine(painter, prevDigit, currentDigit)
        if self._cycleFlag:
            firstDigit = self._digitsList[0]
            lastDigit = self._digitsList[-1]
            self.drawLine(painter, lastDigit, firstDigit)
        painter.setBrush(self._dotColor)
        painter.drawEllipse(self._radius - self._posX + self._borderOffset - 10/2, self._radius - self._posY + self._borderOffset - 10/2, 10, 10)
        painter.setBrush(brushBackup)
        painter.setPen(penBackup)

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
        if len(self._digitsList) == 0:
            return

        scale = self._scale
        radius = self._radius
        if self._oroborusFlag == True:
            scale -= 1
        for i in range(0, scale):
            degree = (scale - i) * 360.0 / scale
            x = radius * sin(degree * 3.14159265 / 180.0)
            y = radius * cos(degree * 3.14159265 / 180.0)
            xWide = (radius + 12) * sin(degree * 3.14159265 / 180.0)
            yWide = (radius + 12) * cos(degree * 3.14159265 / 180.0)
            #xShort = (radius - 3) * sin(degree * 3.14159265 / 180.0)
            #yShort = (radius - 3) * cos(degree * 3.14159265 / 180.0)
            #Place for start & end sequence nodes - and later all the colors
            painter.drawEllipse(radius - x + self._borderOffset, radius - y + self._borderOffset, 3, 3)

            if self._digitsList[0] == i or self._digitsList[-1] == i:
                if self._digitsList[0] == i:
                    painter.setBrush(Qt.white)
                else:
                    painter.setBrush(Qt.black)
                painter.drawEllipse(radius - x + self._borderOffset - 10/2, radius - y + self._borderOffset - 10/2, 10, 10)

            if i == 0 and self._oroborusFlag == True:
                digitText = str(scale)
            else:
                digitText = str(i)
            painter.drawText(radius - xWide + self._borderOffset - 12/2, radius - yWide + self._borderOffset - 12/2, 20, 20, 0, digitText)




    def tracePositions(self, x1, y1, x2, y2, steps):
        result = []
        deltaX = x2-x1
        deltaY = y2-y1
        stepX = deltaX / steps
        stepY = deltaY / steps
        for s in range(0, steps):
            anotherPosition = [x1 + stepX*s, y1 + stepY*s]
            result.append(anotherPosition)
        return result


    def prepareAnimation(self):
        scale = self._scale
        radius = self._radius
        if self._oroborusFlag == True:
            scale -= 1
        stepsBetweenNodes = 20
        digitsPositions = []
        for digit in self._digitsList:
            degree = (scale - digit) * 360.0 / scale
            x = radius * sin(degree * 3.14159265 / 180.0)
            y = radius * cos(degree * 3.14159265 / 180.0)
            anotherPosition = [x,y]
            digitsPositions.append(anotherPosition)
        #self._animationTrace = digitsPositions
        #print("Digits positions", digitsPositions)
        traces = []
        for i in range(0, len(digitsPositions)-1):
            x1 = digitsPositions[i][0] #make a class?
            y1 = digitsPositions[i][1]
            x2 = digitsPositions[i+1][0]
            y2 = digitsPositions[i+1][1]
            anotherTrace = self.tracePositions(x1,y1,x2,y2,stepsBetweenNodes)
            traces.extend(anotherTrace)
            #print("A trace: ", anotherTrace)
            #better just copy into traces
        x1 = digitsPositions[-1][0] #make a class?
        y1 = digitsPositions[-1][1]
        x2 = digitsPositions[0][0]
        y2 = digitsPositions[0][1]
        anotherTrace = self.tracePositions(x1,y1,x2,y2,stepsBetweenNodes)
        traces.extend(anotherTrace)
        self._animationTrace = traces
        #print("Traces: ", traces)

    @Slot()
    def startAnimation(self):

        if len(self._digitsList) == 0:
            return
        #print("Starting animation with ", self._timerInterval, self._speedRatio)
            #TODO: check if not prepared

        self.prepareAnimation()
        #self.resetAnimation()

        self._timer.setInterval(self._timerInterval) #10 steps each 0.5 second
        #self._backgroundColor = QColor('white')
        self._timer.start()


    @Slot()
    def requestSpecialUpdate(self):
        self.requestSpecialUpdateSafe()
        self.update()

    @Slot()
    def requestSpecialUpdateSafe(self):
        newX = self._animationTrace[self._animationIndex][0]
        newY = self._animationTrace[self._animationIndex][1]
        self._posX = newX
        self._posY = newY
        self._animationIndex += 1
        if self._animationIndex >= len(self._animationTrace):
            self._animationIndex = 0


    @Slot()
    def stopAnimation(self):
        self._timer.stop()
        self.resetAnimation()

    @Slot()
    def pauseAnimation(self):
        self._timer.stop()
        #dont clean the position + #dont prepareAnimation again in startAnimation

    @Slot(result='bool')
    def animationIsRunning(self):
        return self._timer.isActive()

    @Slot()
    def resetAnimation(self):
        self._animationIndex = 0


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



