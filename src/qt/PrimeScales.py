#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from qtpy.QtCore import  QAbstractTableModel, QAbstractItemModel, QModelIndex, Qt, Slot, Signal, QObject, Slot
from qtpy.QtQml import qmlRegisterType
from qtpy.QtGui import QColor, QBrush

from lib.Primes import Primes
from lib.Rational import Rational

def registerQMLTypes():
    qmlRegisterType(PrimeScales, 'Athenum', 1,0, 'PrimeScales')
def getQMLTypes():
    theTypes = ['PrimeScales']
    return theTypes


class PrimeScales(QAbstractTableModel):
    def __init__(self,parent=None):
        QAbstractTableModel.__init__(self,parent)
        self._primesList = []
        self._rationalList = []
        self._scalesPeriods = []
        self._tableWidth = 100

    @Slot(int, result='int')
    def getPrime(self, position):
        return self._primesList[position]

    @Slot(int, int, int)
    def calculate(self, startPrime=1, endPrime=11, cellsAmount=100):
        self._tableWidth = cellsAmount
        p = Primes()
        self._primes = p
        self._primesList = p.getPrimesList(startPrime, endPrime)
        self._rationalList = [ Rational(1,localPrime) for localPrime in self._primesList ] # I LOVE PYTHON
        self._scalesPeriods = [ r.scalesPeriod() for r in self._rationalList ] #FOR SIMPLICITY, NO MORE CPP WITH NO NEED
        self.dataChanged.emit(self.index(0,0) , self.index(self.rowCount()-1, self.columnCount()-1) ,[])

    def rowCount(self, parent = QModelIndex()):
        return len(self._primesList) + 2 #first row is number, then white space

    def columnCount(self, parent = QModelIndex()):
        return self._tableWidth

    def data(self, index, role = Qt.DisplayRole):

        displayClass = 0

        if not index.isValid():
            return ["",displayClass] #None
        elif role != Qt.DisplayRole:
            return ["",displayClass] #None

        row = index.row()
        column = index.column()

        if row == 0:
            if column == 0:
                return ['P', displayClass]
            elif column >= 2:
                return [column,displayClass]
        elif row == 1:
            return ['   ',displayClass]
        else:
            if column == 0:
                return [self._primesList[row-2], displayClass]
            elif column == 1:
                return ['   ', displayClass]
            else:
                localScalePeriod = self._scalesPeriods[row-2]
                primeNum = self._primesList[row-2]

                """if column-2 < len(localScalePeriod):
                    if localScalePeriod[column-2] == primeNum - 1:
                        displayClass = 1
                    elif localScalePeriod[column-2] == primeNum / 2.0 - 1:
                        displayClass = 2
                    elif localScalePeriod[column-2] == primeNum / 3.0 - 1:
                        displayClass = 3
                    return [localScalePeriod[column-2],displayClass]
                else:"""
                subIndex = (column-2) % len(localScalePeriod) #this must work always  TODO make single code
                if localScalePeriod[subIndex] == primeNum - 1 :
                    displayClass = 1
                elif localScalePeriod[subIndex] == (primeNum- 1) / 2:
                    displayClass = 2
                elif localScalePeriod[subIndex] == (primeNum - 1) / 3:
                    displayClass = 3
                return [localScalePeriod[subIndex],displayClass]

        return ['   ',displayClass]
