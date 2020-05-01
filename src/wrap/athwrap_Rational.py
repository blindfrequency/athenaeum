from lib.Rational import Rational
from qtpy.QtCore import Qt, Slot, Signal, QObject
from qtpy.QtQml import qmlRegisterType
def registerQMLTypes():
    qmlRegisterType(WrapRational, 'Athenum', 1,0, 'Rational')
def getQMLTypes():
    theTypes = ['Rational']
    return theTypes

class WrapRational(QObject):
    def __init__(self,parent=None):
        QObject.__init__(self,parent)
        self._wrappedObject = Rational()

    @Slot('int','int','int')
    def calc(self, num = 1, den = 1, base = 10):
        self._wrappedObject.calc( num , den , base )

    @Slot('QVariant')
    def copy(self, r):
        self._wrappedObject.copy( r)

    @Slot()
    def reduce(self):
        self._wrappedObject.reduce()

    @Slot('QVariant','QVariant',result='QVariant')
    def findPeriodStart(self, digits, period):
        return self._wrappedObject.findPeriodStart( digits, period)

    @Slot('QVariant','QVariant','QVariant')
    def fillDigitsByInteger(self, number, base, digitsList):
        self._wrappedObject.fillDigitsByInteger( number, base, digitsList)

    @Slot('QVariant','QVariant','QVariant',result='QVariant')
    def calculateDigits(self, num, den, base):
        return self._wrappedObject.calculateDigits( num, den, base)

    @Slot('QVariant',result='QVariant')
    def establishPeriod(self, digits):
        return self._wrappedObject.establishPeriod( digits)

    @Slot('QVariant')
    def sum(self, rationalList):
        self._wrappedObject.sum( rationalList)

    @Slot(result='QVariant')
    def getNotationScale(self):
        return self._wrappedObject.getNotationScale()

    @Slot(result='QVariant')
    def getFullString(self):
        return self._wrappedObject.getFullString()

    @Slot('QVariant','int',result='QVariant')
    def digits(self, part='all', extendByPeriod=0):
        return self._wrappedObject.digits( part, extendByPeriod)

    @Slot('QVariant',result='QVariant')
    def intDigits(self, part='all'):
        return self._wrappedObject.intDigits( part)

    @Slot('QVariant',result='QVariant')
    def intFromFract(self, n):
        return self._wrappedObject.intFromFract( n)

    @Slot('int',result='QVariant')
    def intFromFractQML(self,n=0):
        return self._wrappedObject.intFromFractQML(n)

    @Slot(result='QVariant')
    def getPeriod(self):
        return self._wrappedObject.getPeriod()

    @Slot(result='QVariant')
    def getPeriodStart(self):
        return self._wrappedObject.getPeriodStart()

    @Slot(result='QVariant')
    def getIntPartLen(self):
        return self._wrappedObject.getIntPartLen()

    @Slot(result='QVariant')
    def getFractPartLen(self):
        return self._wrappedObject.getFractPartLen()

    @Slot('int',result='QVariant')
    def changeScaleOfNotation(self,base=10):
        return self._wrappedObject.changeScaleOfNotation(base)

    @Slot('QVariant',result='QVariant')
    def digitSpectrum(self, part='fract'):
        return self._wrappedObject.digitSpectrum( part)

    @Slot('QVariant',result='QVariant')
    def spectrumString(self, part='fract'):
        return self._wrappedObject.spectrumString( part)

    @Slot('QVariant',result='QVariant')
    def regularity(self, part='all'):
        return self._wrappedObject.regularity( part)

    @Slot(result='QVariant')
    def remains(self):
        return self._wrappedObject.remains()

    @Slot('QVariant',result='QVariant')
    def numReduction(self, part='all'):
        return self._wrappedObject.numReduction( part)

    @Slot(result='QVariant')
    def isCyclic(self):
        return self._wrappedObject.isCyclic()

    @Slot(result='QVariant')
    def getAmountOfCycles(self):
        return self._wrappedObject.getAmountOfCycles()

    @Slot(result='QVariant')
    def multiplyShift(self):
        return self._wrappedObject.multiplyShift()

    @Slot(result='QVariant')
    def verticalTables(self):
        return self._wrappedObject.verticalTables()

    @Slot(result='QVariant')
    def scalesPeriod(self):
        return self._wrappedObject.scalesPeriod()

    @Slot(result='QVariant')
    def cyclicPairNumber(self):
        return self._wrappedObject.cyclicPairNumber()

    @Slot('int','QVariant',result='QVariant')
    def findGeomProgress(self, decreaseCoef=100, epsCoef=0.000001):
        return self._wrappedObject.findGeomProgress( decreaseCoef, epsCoef)

    @Slot(result='QVariant')
    def getGeomProgCoef(self):
        return self._wrappedObject.getGeomProgCoef()

