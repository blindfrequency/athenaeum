#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
import gmpy2
import time

from qtpy.QtCore import  QAbstractTableModel, QAbstractItemModel, QModelIndex, Qt, Slot, Signal, QObject, Slot
from qtpy.QtQml import qmlRegisterType
from qtpy.QtGui import QColor, QBrush

from lib.Rational import Rational
from lib.GeometricProgression import GeometricProgression

def registerQMLTypes():
    qmlRegisterType(SumGroupModel, 'Athenum', 1,0, 'MultiSumModel')
    qmlRegisterType(SumModel, 'Athenum', 1,0, 'SumModel')
def getQMLTypes():
    theTypes = ['SumGroupModel','SumModel']
    return theTypes

class SumGroupModel(QAbstractTableModel):
    def __init__(self,parent=None):
        QAbstractTableModel.__init__(self,parent)
        self._sumModels = []

    @Slot(int, int, int, int, int)
    def addNew(self, num, den, base, progressionNumber, amountOfElements):
        model = SumModel()
        model.calculate(num, den, base, progressionNumber, amountOfElements)
        self._sumModels.append(model)

    @Slot()
    def refresh(self):
        self.dataChanged.emit(self.index(0,0) , self.index(self.rowCount()-1, self.columnCount()-1) ,[])

    def get(self, index):
        pass

    @Slot()
    def clear(self):
        self._sumModels = []

    def remove(self, index):
        pass

    def colorMap(self): #make another table and incapsulate it
        pass

#And the default definition
    def rowCount(self, parent = QModelIndex()):
        maxRows = 0
        for model in self._sumModels:
            if model.rowCount() > maxRows:
                maxRows = model.rowCount()
        return maxRows

    def columnCount(self, parent = QModelIndex()):
        maxColumns = 0
        for model in self._sumModels:
            if model.columnCount() > maxColumns:
                maxColumns = model.columnCount()
        return maxColumns

    def data(self, index, role = Qt.DisplayRole):
       if not index.isValid():
           return None
       elif role != Qt.DisplayRole:
           return None

       row = index.row()
       column = index.column()

       cells = []
       indexColor = 0
       localIndex = 1
       for model in self._sumModels:
           cell = model.data(index,role)
           if cell != '   ':
                cells.append(cell)
                indexColor += localIndex
           localIndex *= 2
           if localIndex > 4:
               localIndex = 1 #crazy cycle

       if indexColor == 1:
           color = QColor(255,20,10)
       elif indexColor == 2:
           color = QColor(10,255,20)
       elif indexColor == 4:
           color = QColor(60,180,255)
       elif indexColor == 5:
           color = QColor(255,0,255)
       elif indexColor == 6:
           color = QColor(0,255,255)
       elif indexColor == 3:
           color = QColor(255,255,0)
       elif indexColor >= 7:
           color = QColor('white') #great to adapt and show white only in all
       else:
            color = QColor('gray')

       if len(set(cells)) == 1:
           return [cells[0],color]
       elif len(set(cells)) > 1:
           return ['x',color]
       else:
           return ['   ',color]


class SumModel(QAbstractTableModel):
    def __init__(self,parent=None):
        QAbstractTableModel.__init__(self,parent)
        self._hideStartingZeroes = True
        self._tableWidth = 300
        self._progressionMembers = []
        #self._fraction = Rational(1,1)

   #need to have some functions to update latex
    @Slot()
    def switchZeroes(self):
        self._hideStartingZeroes = not self._hideStartingZeroes
        self.dataChanged.emit(self.index(0,0) , self.index(self.rowCount()-1, self.columnCount()-1) ,[])

    @Slot(result='QString')
    def firstStep(self):
       return str(self._progression.getFirst())

    @Slot(result='QString')
    def multiply(self):
       return str(self._progression.getInc())

    @Slot(result='QString')
    def decrease(self):
       return str(self._progression.getDec())


    @Slot(int, int, int, int, int)
    def calculate(self, num, den, base, progressionNumber, amountOfElements):
        print("Sum Model calculation: ",num,den,base,progressionNumber,amountOfElements)
        self._fraction = Rational(num,den,base) #there used to be full reptend prime, or one of its cycles

        searchBasis = base
        while den > searchBasis:
            searchBasis *= base
        for i in range(progressionNumber):
            searchBasis *= base

        startT = time.time()
        #there may be a tweak we can calculate in 10 to check it full reptend
        self._fraction.isCyclic()
        gProg = self._fraction.findGeomProgress(searchBasis)
        spendTime = time.time() - startT
        self._progression = gProg

        print("Pre remains ",self._fraction.remains())
        print("Progression ",gProg.firstElement(),gProg.getInc(),' time: ',spendTime)

        if base != 10: return #JUST FOR A SHORTEST WHILE IN DEBUG

        self._progressionMembers = []
        if amountOfElements == -1:
            amountOfElements = 100

        self._sequencePattern = []

        allTheDigits = []
        maxDigitsLen = 0

        for i in range(amountOfElements):
            #print("calculating member ",i)
            rElement = gProg.countAt(i)
            digits = rElement.digits(part='fract')
            counter = 0
            while digits[counter] == 0:
                counter += 1
            #counter is kind of maj seq
            self._sequencePattern.append(counter)
            self._progressionMembers.append(rElement) #also if its pow of 10 we can make cheat digits generator, that for example counts only 14*2n and amount  of digits in 10^n
            localDigits = rElement.digits()
            allTheDigits.append(localDigits)
            if maxDigitsLen < len(localDigits):
                maxDigitsLen = len(localDigits)

        self._finalLine = []
        self._elementsUsed = []
        for i in range(maxDigitsLen):
            newDigit = 0
            countElements = 0
            for digs in allTheDigits:
                if len(digs) > i:
                    if digs[i] != 0:
                        newDigit += digs[i]
                        countElements += 1
            self._finalLine.append(newDigit)
            self._elementsUsed.append(countElements)

        self._sumLine = gProg.sumAt(7)
        print('Sum line is ',self._sumLine,repr(self._sumLine))

        self.dataChanged.emit(self.index(0,0) , self.index(self.rowCount()-1, self.columnCount()-1) ,[])

    @Slot(int)
    def setTableWidth(self, newWidth):
        self._tableWidth = newWidth

    def rowCount(self, parent = QModelIndex()):
        return len(self._progressionMembers) + 3

    def columnCount(self, parent = QModelIndex()):
        return self._tableWidth #or something like this

    def data(self, index, role = Qt.DisplayRole):
        if not index.isValid():
            return None
        elif role != Qt.DisplayRole:
            return None

        row = index.row()
        column = index.column()

        if row == 0:
            return self.getRdigit(self._fraction,column)
        elif row == 1:
            for point in self._sequencePattern:
                if column == point+1:
                    return '*'
        elif row == 2:
            pass
        else:
            rowIndex = row - 3
            if len(self._progressionMembers) > rowIndex and rowIndex >= 0:
                #print("GOING TO INDEX",rowIndex," on ", len(self._progressionMembers))
                return self.getRdigit(self._progressionMembers[rowIndex],column)
        return '   '

    def getRdigit(self, rational, digIndex): #maybe just move this function under rational it may be helpful later for summation of few elements and finding it period
        digits = rational.digits()
        if len(digits) > digIndex:
            if self._hideStartingZeroes == True:
                allZeroes = True
                for i in range(digIndex+1):
                    if digits[i] != 0:
                        allZeroes = False
                        break
                if allZeroes: return '   '
            return int(digits[ digIndex ])
        else:
            if rational.getPeriod() == 0: return '   '
            offset = digIndex - len(digits)
            startOfPeriod = rational.getPeriodStart()
            index = offset % rational.getPeriod()
            return int(digits[index+startOfPeriod])
        return 0
