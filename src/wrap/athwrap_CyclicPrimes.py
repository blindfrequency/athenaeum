from lib.CyclicPrimes import CyclicPrimes
from qtpy.QtCore import Qt, Slot, Signal, QObject
from qtpy.QtQml import qmlRegisterType
def registerQMLTypes():
    qmlRegisterType(WrapCyclicPrimes, 'Athenum', 1,0, 'CyclicPrimes')
def getQMLTypes():
    theTypes = ['CyclicPrimes']
    return theTypes

class WrapCyclicPrimes(QObject):
    def __init__(self,parent=None):
        QObject.__init__(self,parent)
        self._wrappedObject = CyclicPrimes()

    @Slot('int','int','int','QVariant',result='QVariant')
    def findInRange(self, prime=7, baseNumberStart=0, baseNumberEnd=2, type='sub'):
        return self._wrappedObject.findInRange( prime, baseNumberStart, baseNumberEnd, type)

    @Slot('int','int','int',result='QVariant')
    def getRangeScales(self, prime=7, baseNumberStart=0, baseNumberEnd=2):
        return self._wrappedObject.getRangeScales( prime, baseNumberStart, baseNumberEnd)

    @Slot('int','int','QVariant',result='QVariant')
    def find(self, prime=7, base=10, type='sub'):
        return self._wrappedObject.find( prime, base, type)

    @Slot('QVariant','QVariant','QVariant',result='QVariant')
    def descriptionForFullCycle(self, prime, primeList, base):
        return self._wrappedObject.descriptionForFullCycle( prime, primeList, base)

