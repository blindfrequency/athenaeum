from mods.lib.GeometricProgression import GeometricProgression
from PySide2.QtCore import Qt, Slot, Signal, QObject
from PySide2.QtQml import qmlRegisterType
def registerQMLTypes():
    qmlRegisterType(WrapGeometricProgression, 'Athenum', 1,0, 'GeometricProgression')
def getQMLTypes():
    theTypes = ['GeometricProgression']
    return theTypes

class WrapGeometricProgression(QObject):
    def __init__(self,parent=None):
        QObject.__init__(self,parent)
        self._wrappedObject = GeometricProgression()

    @Slot('int','int','int')
    def set(self, first=14, inc=2, dec=100):
        self._wrappedObject.set( first, inc, dec)

    @Slot(result='QVariant')
    def getInc(self):
        return self._wrappedObject.getInc()

    @Slot(result='QVariant')
    def getDec(self):
        return self._wrappedObject.getDec()

    @Slot(result='QVariant')
    def getFirst(self):
        return self._wrappedObject.getFirst()

    @Slot(result='QVariant')
    def getQ(self):
        return self._wrappedObject.getQ()

    @Slot(result='QVariant')
    def firstElement(self):
        return self._wrappedObject.firstElement()

    @Slot(result='QVariant')
    def converges(self):
        return self._wrappedObject.converges()

    @Slot('int',result='QVariant')
    def countAt(self, n=0):
        return self._wrappedObject.countAt( n)

    @Slot('QVariant',result='QVariant')
    def sumAt(self,n):
        return self._wrappedObject.sumAt(n)

    @Slot(result='QVariant')
    def fullSum(self):
        return self._wrappedObject.fullSum()

    @Slot(result='QVariant')
    def rationalSum(self):
        return self._wrappedObject.rationalSum()

    @Slot(result='QVariant')
    def rSumQML(self):
        return self._wrappedObject.rSumQML()

    @Slot('int',result='QVariant')
    def rElementQML(self,n=0):
        return self._wrappedObject.rElementQML(n)

    @Slot('int',result='QVariant')
    def reducedElementQML(self,n=0):
        return self._wrappedObject.reducedElementQML(n)

