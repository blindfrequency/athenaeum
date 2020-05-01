from lib.SimpleNumbers import SimpleNumbers
from qtpy.QtCore import Qt, Slot, Signal, QObject
from qtpy.QtQml import qmlRegisterType
def registerQMLTypes():
    qmlRegisterType(WrapSimpleNumbers, 'Athenum', 1,0, 'SimpleNumbers')
def getQMLTypes():
    theTypes = ['SimpleNumbers']
    return theTypes

class WrapSimpleNumbers(QObject):
    def __init__(self,parent=None):
        QObject.__init__(self,parent)
        self._wrappedObject = SimpleNumbers()

    @Slot('int',result='QVariant')
    def numberToText(self,number=1):
        return self._wrappedObject.numberToText(number)

    @Slot('QVariant')
    def voiceText(self, text=''):
        self._wrappedObject.voiceText( text)

