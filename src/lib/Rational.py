#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math

from sympy.ntheory import primefactors, factorint, isprime
from fractions import gcd


import lib.Athenum as Athenum
if Athenum.useGmpy == True:
    import gmpy2


def lcm(x, y):
    return x * y // gcd(x, y) # or can import gcd from `math` in Python 3

def reduceFraction(num, den):
    common_divisor = gcd(num, den)
    (rNum, rDen) = (num / common_divisor, den / common_divisor)
    return int(rNum), int(rDen)


class Rational:
    def __init__(self, num = 1, den = 1, base = 10, parent = None):
        self.calc(num,den,base)

    def calc(self, num = 1, den = 1, base = 10):
        self._flush()
        self._R(num,den,base)

    def copy(self, r):
        self.calc(r._num, r._den, r._scaleOfNotation)

    def reduce(self):
        common_divisor = gcd(self._num, self._den)
        (rNum, rDen) = (self._num / common_divisor, self._den / common_divisor)
        self._num = int(rNum)
        self._den = int(rDen)

    def _flush(self):
        self._dotPosition = -1
        self._startOfPeriod = 0 #means none as 0 is always integer at least 0
        self._intDigitsCount = 1 #at least 0, yes, sorry we won't have this cool feature to know there exactly 0 but this helps with remains
        self._period = -1
        self._isCyclic = False #as de

    def _R(self, num, den, base):
        self._num = num; self._den = den
        self._scaleOfNotation = base

        if (den % base) == 0: #works only for 10

            if Athenum.useGmpy == True:
                self._digitsLimit = len(str(gmpy2.mpz(den))) #update it laster to work fast with any length
            else:
                self._digitsLimit = len(str(den))

            self._digits, self._remains = self.calculateDigits(num,den,base)
            self._period = 0
        else:
            self._num, self._den =  reduceFraction(num,den)
            self._digitsLimit = den * 11 #what should be the coef? there was 11 it may fail yet weak place of design
            #THANKX to Ales now I know that period is n, where (10 ** n) % den == 1, so we can sount only needed digits and just check the
            #I FOUND THAT 10**N will have % as remains in the process, so we can work till remains will hit 1 twice :) ok will check it
            self._digits, self._remains = self.calculateDigits(num,den,base)
            self._period = self.establishPeriod(self._digits)

            if self._period != 0:
                self._startOfPeriod = self.findPeriodStart(self._digits,self._period)
                slicer = slice(0,self._startOfPeriod+self._period)
                self._digits = self._digits[slicer]
                slicerMods = slice(0,self._period + self._startOfPeriod - self._intDigitsCount)
                self._remains = self._remains[slicerMods]

    def findPeriodStart(self, digits, period):
        rangeBegin = self._intDigitsCount
        if rangeBegin == 0: rangeBegin = 1
        for startingPoint in range(rangeBegin,self._digitsLimit-1):
            slicerFirst = slice(startingPoint,startingPoint + period)
            slicerNext = slice(startingPoint + period, startingPoint + period*2)
            checkListFirst = digits[slicerFirst]
            checkListNext = digits[slicerNext]

            if checkListFirst == checkListNext:
                return startingPoint
        return None

    def fillDigitsByInteger(self, number, base, digitsList): #probably all should be protected only operators opened and special properties
        self._intDigitsCount = 0
        if number < base:
            digitsList.insert(0,number)
            self._intDigitsCount += 1
        while number >= base:

            if Athenum.useGmpy == True:
                d,m = gmpy2.f_divmod(number,base)
            else:
                d = number / base
                m = number % base
                print("Skip gmpy check its work [undone]")

            digitsList.insert(0,m)
            self._intDigitsCount += 1
            number = d
            if number < base:
                digitsList.insert(0,d)
                self._intDigitsCount += 1
                break

    def calculateDigits(self, num, den, base):#yet is correct only fo num < den, doesn't works fine with integers and num > den

        if Athenum.useGmpy == True:
            num = gmpy2.mpz(num)
            den = gmpy2.mpz(den)
        else:
            print("Skip gmpy check it [undone]")
            num = int(num)
            den = int(den)

        baseScale = base
        digits = []
        mods = []

        if num == den: #as long as the whole function used only for constructor
            digits.append(1)
            self._period = 0
            return digits, mods

        if den == 0:
            self._period = 0
            return digits, mods

        for i in range(0, self._digitsLimit):
            if Athenum.useGmpy == True:
                d,m = gmpy2.f_divmod(num,den)
            else:
                d = num / den
                m = num % den
                print("Skip gmpy check its work [undone]")

            num = m * baseScale
            if i==0 and d > 0: #originaly there was d > base
                self.fillDigitsByInteger(d, base, digits)
                mods.append(m)
            else:
                digits.append(d)
                mods.append(m)
                if i != 0 and self._dotPosition == -1:
                    self._dotPosition = len(digits)-1
            if num == 0:
                break

            #probably best option is half of den
            if len(digits) % 1000 == 0: #ALSO IF BAS IS PRIME AND CONDITION MET WE CAN BE SURE THAT AMOUNT OF CYCLES = P-1/period
                checkPeriod = self.establishPeriod(digits)
                #print("DEBUG Check period on ",len(digits), checkPeriod) #digits
                if checkPeriod > 0: #it was kind of error :)
                    return digits, mods #stop if there is already period

        return digits, mods


    def establishPeriod(self, digits):
        digitsLen = len(digits)
        #if digitsLen < self._den: #this is not always error case !!
        #    return 0
        for period in range(1,self._den): #Periods don't exceed denumerators
            firstSlice = slice(digitsLen-1-period, digitsLen-1) #(1, 1+period) #shift for 1 because of '0.'
            firstPeriod = digits[firstSlice]
            fineRepeatedPeriods = 0
            insureAmount = 10 #should be grow much on long numbers so 10 was replaced with 5
            #if base is low insureAmount should be increased
            for insureRepeats in range(1,insureAmount): #this value is last week place because of long numbers give many zeroes first
                anotherSlice = slice(digitsLen-1-period*insureRepeats-period,digitsLen-1-period*insureRepeats)#1 + period*insureRepeats, 1 + period*insureRepeats + period)
                anotherPeriod = digits[anotherSlice]
                if firstPeriod == anotherPeriod:
                    fineRepeatedPeriods += 1
                    if fineRepeatedPeriods >= insureAmount-1:
                        if period == 1 and anotherPeriod[0] == 0:
                            period = 0
                        return period
                else:
                    #print ("Fail establish on ",fineRepeatedPeriods," for period ", period)
                    break
        return 0

    def __str__(self):
        fullString = ''
        sepparator = ' '  if self._scaleOfNotation > 10 else ''
        for digitIndex, digit in enumerate(self._digits):
            if self._dotPosition == digitIndex:  fullString += '.'
            if self._startOfPeriod != 0 and self._startOfPeriod == digitIndex:  fullString += '('
            fullString += str(digit) + sepparator
        if self._startOfPeriod != 0:
            fullString += ')'
        return fullString

    def __repr__(self):
        result = 'Rational(' + str(self._num) + '/' + str(self._den) + ','+ str(self._scaleOfNotation)  + ',p:' + str(self._period) + ')'
        return result

    def __format__(self, type):
        if type == "digits":
            return self.__str__()
        else:
            fullString = ''
            for digitIndex, digit in enumerate(self._digits):
                if self._dotPosition == digitIndex:
                    fullString += '.'
                if self._startOfPeriod != 0 and self._startOfPeriod == digitIndex:  fullString += '('
                if digit <= 9:
                    fullString += str(digit)
                else:
                    fullString += chr(digit-10 + 65) # there mus be done break, also works only on not crazy systems like 35+
            if self._startOfPeriod != 0:
                fullString += ')'
            return fullString

    def sum(self, rationalList):#kind of OPERATOR and different
    #it was implemented, find its place, also amount of elements in each digit if its list
        pass

    def getNotationScale(self):
        return self._scaleOfNotation;

    def getFullString(self):
        fullStr = self.__str__() + ' ' + repr(self)
        return fullStr


    def digits(self, part='all', extendByPeriod=0):
        beginRange = 0; endRange = len( self._digits ) #default part='all'
        if part == 'period': beginRange = self._startOfPeriod
        elif part == 'int': endRange = self._intDigitsCount
        elif part == 'fract': beginRange = self._intDigitsCount
        slicer = slice(beginRange,endRange)
        resultList = self._digits[slicer] #ITS NOT A .copy() !!

        if self._period == 0: #attention
            return resultList

        if extendByPeriod != 0:
            for i in range(extendByPeriod):
                periodDigit = self._digits[self._startOfPeriod + i % self._period]
                resultList.append(periodDigit)
        return resultList

    def intDigits(self, part='all'):
        x = self.digits(part)
        newList = []
        for any in x:
            newList.append(int(any))
        return newList


    def intFromFract(self, n):
        if n > self._period:
            diff = n - self._period
            d = self.digits(part='fract',extendByPeriod=diff)
        else:
            d = self.digits(part='fract')
            d = d[0:n]
        sumInt = 0
        for digit in d:
            sumInt *= self._scaleOfNotation
            sumInt += digit
        return sumInt


    def intFromFractQML(self,n=0):
        return str(self.intFromFract(n))

    def getPeriod(self):
        return self._period

    def getPeriodStart(self):
        return self._startOfPeriod

    def getIntPartLen(self):
        return self._intDigitsCount

    def getFractPartLen(self):
        return len(self._digits) - self._intDigitsCount

    def changeScaleOfNotation(self,base=10): #returns new object in other base
        return Rational(self._num,self._den,base)


    def digitSpectrum(self, part='fract'): #period, int, fraction, all self._startOfPeriod+self._period+self._intDigitsCount
        spectrum = [0]*self._scaleOfNotation
        digits = self.digits(part)
        for digit in digits:
            spectrum[ digit ] += 1
        return spectrum

    def spectrumString(self, part='fract'):
        spec = self.digitSpectrum(part)
        resultString = ''
        for dig in spec:
            resultString += str(dig) + ' '
        return resultString

    def regularity(self, part='all'): #sifts between digits
        regs = []
        extension = 1 #extend one digits to calculate from last to first in period in one
        if self._period == 0 or part == 'int':
            extesion = 0
        digits = self.digits(part,extension)
        for digInd in range(0, len(digits)-1):
            diff = digits[ digInd+1 ] - digits[digInd]
            regs.append(diff)
        #return regs
        intRegs = []
        for reg in regs:
            intRegs.append(int(reg))
        return intRegs

    def remains(self): #like digits - another list from divmod
        intRemains = []
        for rem in self._remains:
            intRemains.append(int(rem))
        return intRemains

    def numReduction(self, part='all'):
        digits = self.digits(part)
        while 'the earth spins round':
            result = 0
            for digit in digits:
                result += digit
            if result >= self._scaleOfNotation:
                newDigits = []
                self.fillDigitsByInteger(result, self._scaleOfNotation, newDigits)
                digits = newDigits
            else:
                return result

    def isCyclic(self):
        #if hasattr(self,'_isCyclic'):
            #return self._isCyclic
        primesList = primefactors(self._den)
        isDenPrime = len(primesList) == 1
        self._isCyclic = False
        if isDenPrime and self._num < self._den and self._period != 0: # extend it would also work for 91 not only prime?
            #print("Number is cyclic : ",self._den) #put in bool
            self._isCyclic = True
            cycleList = []
            spectrumsSet = set()
            for n in range(1,self._den):
                number = Rational(n,self._den, self._scaleOfNotation)
                cycleList.append(number)
                spectrumsSet.add(number.spectrumString())
            if len(spectrumsSet) == (self._den-1)/self._period:
                #print("Amount of cycles: ", len(spectrumsSet))
                self._amountOfCycles = len(spectrumsSet)
            print(cycleList)
            self._vertTables = []
            for i in range(self._period):
                singleVerTab = []
                for j in range(1, self._den):
                    singleVerTab.append(int(cycleList[j-1].digits()[i+1]))
                self._vertTables.append(singleVerTab)
            #print("Vertical tables ", len(self._vertTables))
            self._multiplyShiftList = [0]
            protoPeriod = cycleList[0].digits(part='period')
            for i in range(2,self._den): #skip 1/N as its the prototype
                firstPeriodDigit = cycleList[i-1].digits(part='period')[0]
                for index, digit  in enumerate(protoPeriod):
                    if digit == firstPeriodDigit:
                        self._multiplyShiftList.append(index)
            #print ("Multy shifts ",self._multiplyShiftList)
            cyclicNumber = int( (self._scaleOfNotation ** self._period) * (1.0 / self._den) )
            #print("CYCLIC NUMBER INSIDE IS",cyclicNumber, makePrimeList(cyclicNumber))
            #later explore how multiply shifts for example structure 142857 starts login some part at the end, and gain same part at begining
        return self._isCyclic

    def getAmountOfCycles(self):
        return self._amountOfCycles

    def multiplyShift(self):
        return self._multiplyShiftList

    def verticalTables(self):
        return self._vertTables

    def scalesPeriod(self):
        periodList = []
        for i in range(2, self._den + 2):
            num = Rational(self._num, self._den, i)
            periodList.append(num.getPeriod())
        return periodList

    def cyclicPairNumber(self):
        if self._isCyclic: # and self._amountOfCycles == 1
            repunitString = '9'*self._period #should be adaptable to other bases

            if Athenum.useGmpy == True:
                periodBorder = gmpy2.mpz(repunitString)
            else:
                print("Gmpy skipped check it [undone]")
                periodBorder = int(repunitString)

            primes = primefactors(periodBorder)
            #print("Cyclic pair : ",repunitString,primes)
            primesSet = set(primes)
            equalPeriods = []
            for primeNumber in primesSet:
                pass
                rational = Rational(1,primeNumber,self._scaleOfNotation) #NEED SPEED UP PERIOD CALCULATION FOR LONG DENUMSrimefac documentation
                if rational.getPeriod() == self._period:
                    equalPeriods.append(primeNumber)
            return equalPeriods
            #print("Equal periods : ",equalPeriods) #exclude itself

    def __add__(self, other):
        baseLcm = lcm(self._den,other._den)
        newDen = baseLcm
        newNum = int(self._num * baseLcm / self._den + other._num * baseLcm / other._den)
        return Rational(newNum,newDen, self._scaleOfNotation)

    def __sub__(self, other):
        baseLcm = lcm(self._den,other._den)
        newDen = baseLcm
        newNum = int(baseLcm / self._den - baseLcm / other._den)
        return Rational(newNum,newDen, self._scaleOfNotation)

    def __mul__(self, other):
        newNum = self._num * other._num
        newDen = self._den * other._den
        n,d = reduceFraction(newNum,newDen)
        return Rational(n,d, self._scaleOfNotation)

    def __truediv__(self, other):
        newNum = self._num * other._den
        newDen = self._den * other._num
        n,d = reduceFraction(newNum,newDen)
        return Rational(n,d, self._scaleOfNotation)

    def __pow__(self, other):
        newNum = self._num ** other
        newDen = self._den ** other
        n,d = reduceFraction(newNum,newDen)
        return Rational(n,d, self._scaleOfNotation)
    #maybe add mod later

    def __eq__(self,other):
        if self._num == other._num and self._den == other._den: return True
        return False

    def __lt__(self,other):  # operator <
        pass
    def __gt__(self,other): # operator  >
        pass

    def findGeomProgress(self, decreaseCoef=100, epsCoef=0.000001):

        if self._isCyclic:   #if it is a reptend prime, I can just take n of the digits, and match it with remains
            origin = Rational(1, self._den, self._scaleOfNotation)
            l = round(math.log(decreaseCoef,self._scaleOfNotation)) #yet only for 10 round(math.log10(decreaseCoef)
            multiplyBy = origin.remains()[l % len(self._remains)]
            f = origin.intFromFract(l) #could I don't use the self? hmm
            while f == 0:
                l += 1
                f = origin.intFromFract(l)
                decreaseCoef *= self._scaleOfNotation #ok rename to base but comment it well
            from lib.GeometricProgression import GeometricProgression
            g = GeometricProgression()
            g.set(f*self._num, multiplyBy,decreaseCoef)
            return g
        print("SEARCHING FOR GEOM PROGRESSION OF NONE CYCLIC")

        epsCoef = 1.0 / (self._scaleOfNotation ** self._period) #later we will fait to calculate fast and good at some position float is not enough
        firstStepLength = math.log(decreaseCoef, self._scaleOfNotation)
        firstStep = int( (self._scaleOfNotation ** firstStepLength) * (1.0 / self._den) )
        equalent = self._num / self._den
        for checkMult in self.remains():
            gpCheck = GeometricProgression(firstStep,checkMult,decreaseCoef)
            sum = gpCheck.fullSum()
            if abs(sum-equalent) < epsCoef: #rationalSum == self:
                return gpCheck
        return None

    def getGeomProgCoef(self): #probably this function should be updated to be more usefull
        decreasor = 0
        for i in range(1,21):
            decreasor = self._scaleOfNotation ** i
            if decreasor > self._den:
                break
        geo = self.findGeomProgress(decreasor)
        result = (decreasor, geo.getInc())
        return result


def transFract(periodString, base=10, newBase=10):
    brBegin = periodString.find('(')
    brEnd = periodString.find(')')
    if brBegin == -1 or brEnd == -1:
        #print('Yet work only with periodic fractions') #its very simple if no period just like period but +1 for den
        dotPosition = periodString.find('.')
        digits = periodString[dotPosition+1:]
        #print('Digits cutten ', digits)
        denum = 10 ** len(digits)
        n,d = reduceFraction(int(digits), denum)
        print('Num ', digits, ' den ', denum)
        return Rational(n,d,newBase)
    else:
        period = periodString[brBegin+1:brEnd]
        repDig = str(base-1)*len(period) #works only for 2-10 but not 11 or more update formula later, no need now

        if Athenum.useGmpy == True:
            num = gmpy2.mpz(period,base)
            den = gmpy2.mpz(repDig,base)
        else:
            print("Gmpy turned off, check result [undone]")
            num = int(period,base)
            den = int(repDig,base)
        #print("CHECK ",period,repDig," and integers are ",num,den)
        n,d = reduceFraction(num,den)
        return Rational(n,d,newBase)


# 6-perios classification

'''
startTime3 = time.time()

specSet = set()

specDict = {}
for i in range(0,10):
    print("Starting i ",i)

    for j in range(0,10):
        currentSet = {i}
        if j in currentSet: continue

        for k in range(0,10):
            currentSet = {i,j}
            if k in currentSet: continue

            for l in range(0,10):
                currentSet = {i,j,k}
                if l in currentSet: continue

                for m in range(0,10):
                    currentSet = {i,j,k,l}
                    if m in currentSet: continue

                    for n in range(0,10):
                        currentSet = {i,j,k,l,m}
                        if n in currentSet: continue

                        num = i*(10**5) + j*(10**4) + k*(10**3) + l*100 + m*10 + n
                        den = 999999

                        r = Rational(num,den)
                        spec = r.digitSpectrum() #period only
                        specStr = listToStr(spec)

                        specSet.add(specStr)

                        if specDict.get(specStr) == None:
                            specDict[specStr] = [r]
                        else:
                            specDict[specStr].append(r)

                        #NEED group for multiply shifts

                        #SEARCH FOR SYMMERY IN REGULARITIES


endTime3 = time.time()
diffTime3 = endTime3 - startTime3
print("time spent: " + str(diffTime3))

print("Dict len ",len(specDict))
print(specSet)
'''



'''
def lcm(x, y):
    # or can import gcd from `math` in Python 3
    return x * y // gcd(x, y)

#r = Rational(1,8191,10) #may be bug at least too long, of course its really long one, but it made longer
#print(repr(r), r)
#binnay periods, and polyrithms
octaves = calculateOctaves(1,11) #Some positions cout too long, like 131071
preNext = list(map(lambda n: n-1, octaves))

fullPeriod = 1 #RATIONALS are interesting way of representing rythm, good for futer experiments, and attempt to recognize how rythm works
#MAKE RYTHM FROM RATIONAL PLAYER - and just set whole rational or sum of some 2n-1 maybe even multiplied on different *m
for num in preNext:
    if num == 0: continue
    r2 = Rational(1,num,2)
    r10 = Rational(1,num,10)
    print(repr(r10),r2)
    print(r10)
    #GCD of period is how the sum is going
    if r2.getPeriod() != 0:
        fullPeriod = lcm(fullPeriod, r2.getPeriod())
        print("Full period is ",fullPeriod)

number = preNext[2]
for i in range(1,number):
    r = Rational(i,number,2)
    r10 = Rational(i,number,10)
    print(i, " : ", repr(r10),r, r10)
'''
