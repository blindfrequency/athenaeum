# This Python file uses the following encoding: utf-8

# if__name__ == "__main__":
#     pass

from qtpy import QtGui, QtQml, QtCore
from qtpy.QtCore import  QAbstractTableModel, QAbstractItemModel, QModelIndex, Qt, Slot, Signal, QObject, Slot
from qtpy.QtQml import qmlRegisterType
from qtpy.QtGui import QColor, QBrush

def registerQMLTypes():
    qmlRegisterType(IntervalScalesModel, 'Athenum', 1,0, 'IntervalScalesModel')
def getQMLTypes():
    theTypes = ['IntervalScalesModel']
    return theTypes

class IntervalScalesModel(QAbstractTableModel):
    def __init__(self,parent=None):
        QAbstractTableModel.__init__(self,parent)
        self._tableWidth = 300

    @Slot()
    def calc(self):
        self.dataChanged.emit(self.index(0,0) , self.index(self.rowCount()-1, self.columnCount()-1) ,[])

    @Slot(int)
    def setTableWidth(self, newWidth):
        self._tableWidth = newWidth
        print("New width for ISM", newWidth)

    def rowCount(self, parent = QModelIndex()):
        return 1

    def columnCount(self, parent = QModelIndex()):
        return self._tableWidth

    def data(self, index, role = Qt.DisplayRole):
        if not index.isValid():
            return None
        elif role != Qt.DisplayRole:
            return None

        row = index.row()
        column = index.column()

        #name, width, class, color
        elementWidth = column + row
        classType = 0 #
        color = QColor(0,255,255) #depends on classType
        return ['name', elementWidth, classType, color]



