from lib.Primes import Primes
from qtpy.QtCore import Qt, Slot, Signal, QObject
from qtpy.QtQml import qmlRegisterType
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

    @Slot('QVariant',result='QVariant')
    def findPrimeSeqGroups(self, border):
        return self._wrappedObject.findPrimeSeqGroups( border)

    @Slot('QVariant','QVariant','int',result='QVariant')
    def decWithSpec(self, number, spectrum, base=10):
        return self._wrappedObject.decWithSpec( number, spectrum, base)

    @Slot('int','int',result='QVariant')
    def getPrimesList(self, start=2, end=50):
        return self._wrappedObject.getPrimesList( start, end)

    @Slot('int',result='QVariant')
    def isPrime(self, number=1):
        return self._wrappedObject.isPrime( number)

    @Slot('int',result='QVariant')
    def isReversePrime(self, number=1):
        return self._wrappedObject.isReversePrime( number)

    @Slot('int','int',result='QVariant')
    def getReversePrimeInRange(self, start=2, end=10):
        return self._wrappedObject.getReversePrimeInRange( start, end)

