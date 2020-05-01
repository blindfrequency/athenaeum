from lib.ScalesOfNotation import ScaleOfNotation
from qtpy.QtCore import Qt, Slot, Signal, QObject
from qtpy.QtQml import qmlRegisterType
def registerQMLTypes():
    qmlRegisterType(WrapScaleOfNotation, 'Athenum', 1,0, 'ScaleOfNotation')
def getQMLTypes():
    theTypes = ['ScaleOfNotation']
    return theTypes

class WrapScaleOfNotation(QObject):
    def __init__(self,parent=None):
        QObject.__init__(self,parent)
        self._wrappedObject = ScaleOfNotation()

    @Slot('QVariant','int','int',result='QVariant')
    def translate(self, origin, originBase=10, destBase=2):
        return self._wrappedObject.translate( origin, originBase, destBase)

    @Slot('QVariant','int','int',result='QVariant')
    def translateSepparated(self, strList, originBase=10, destBase=2):
        return self._wrappedObject.translateSepparated( strList, originBase, destBase)

    @Slot('QVariant','int','int',result='QVariant')
    def translateRational(self, rStr, originBase=10, destBase=2):
        return self._wrappedObject.translateRational( rStr, originBase, destBase)

    @Slot('QVariant','int','int',result='QVariant')
    def translateFraction(self, fStr, originBase=10, destBase=2):
        return self._wrappedObject.translateFraction( fStr, originBase, destBase)

