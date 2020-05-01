
from qtpy.QtCore import  QAbstractTableModel, QAbstractItemModel, QModelIndex, Qt, Slot, Signal, QObject, Slot
from qtpy.QtQml import qmlRegisterType

from lib.Primes import Primes
import lib.Octaves

#probably work around here
#==============================================================
#      octs = lib.Octaves.calculateOctaves(1,6)
#==============================================================
#to make them hidden, and avoid usage of Primes


def registerQMLTypes():
    qmlRegisterType(AbstractOctaves, 'Athenum', 1,0, 'AbstractOctaves')
def getQMLTypes():
    theTypes = ['AbstractOctaves']
    return theTypes


class AbstractOctaves(QAbstractTableModel):
    def __init__(self, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self._numbers = []
        self._start = 1
        self._end = 128
        self._tableWidth = self._end - self._start + 3 #3 for empty places
        self._primes = Primes()
        self._octaves = set()


    @Slot(int, int)
    def calculate(self, start=1, end=128):
        self._start = start
        self._end   = end
        self._tableWidth = end - start + 3 #3 for empty places
        #fullfill flags

        self._octaves = set()
        currentPosition = start
        while currentPosition <= end:
            self._octaves.add(currentPosition)
            currentPosition *= 2

        #print('Finished filling octaves',start,end)

        self.dataChanged.emit(self.index(0,0) , self.index(self.rowCount()-1, self.columnCount()-1) ,[])


    def rowCount(self, parent = QModelIndex()):
        return 7 #numbers, blank, flags: oct, prime, out of symmetry + 2 blanks

    def columnCount(self, parent = QModelIndex()):
        return self._tableWidth


    def data(self, index, role = Qt.DisplayRole):
        if not index.isValid():
            return None
        elif role != Qt.DisplayRole:
            return None

        row = index.row()
        column = index.column()

        currentPosition = column - 2 + self._start

        if row == 0:
            if column > 1:
                return currentPosition
        elif row == 2:
            if column > 1:
                if currentPosition in self._octaves:
                    return 'x'

        elif row == 3:
            if self._primes.isPrime(currentPosition):
                return 'x'

        elif row == 4:
            pass #out of symmetry flags

        if column == 0:
            if row == 2:
                return 'O' # X only
            if row == 3:
                return 'P' # X only
            if row == 4:
                return 'S' # + or - other empty

        return '   '
