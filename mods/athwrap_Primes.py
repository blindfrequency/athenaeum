from mods.lib.Primes import Primes
from PySide2.QtCore import Qt, Slot, Signal, QObject
from PySide2.QtQml import qmlRegisterType
def registerQMLTypes():
    qmlRegisterType(WrapPrimes, 'Athenum', 1,0, 'Primes')
def getQMLTypes():
    theTypes = ['Primes']
    return theTypes

class WrapPrimes(QObject):
    def __init__(self,parent=None):
        QObject.__init__(self,parent)
        self._wrappedObject = Primes()

    @Slot('QVariant','int',result='QVariant')
    def decompose(self, number, baseCheck=10):
        return self._wrappedObject.decompose( number, baseCheck)

    @Slot('QVariant','QVariant',result='QVariant')
    def fullReptend(self, base, amount):
        return self._wrappedObject.fullReptend( base, amount)

    @Slot('QVariant','QVariant','int',result='QVariant')
    def decWithSpec(self, number, spectrum, base=10):
        return self._wrappedObject.decWithSpec( number, spectrum, base)

