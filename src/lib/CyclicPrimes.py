#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lib.Rational import Rational
from lib.Primes import Primes
#from lib.ScalesOfNotation import ScaleOfNotation #maybe do it at the level of the page


class CyclicPrimes:
    def __init__(self, checkDigitsLimit=100):
        self._digitsToCheck = checkDigitsLimit #later add function to edit it so we can set it from qml

    def findInRange(self, prime=7, baseNumberStart=0, baseNumberEnd=2, type='sub'):
        fullReptendPositions = self._getFullReptendPositions(prime)
        totalPrimes = []
        if len(fullReptendPositions) == 0:
            return totalPrimes
        for i in range(baseNumberStart, baseNumberEnd+1):
            scale = self._rangeIterationBasement(prime, i, fullReptendPositions)
            #print('For n=',i,' scale is ',scale)
            foundPrimes = self.find(prime, scale, type)
            totalPrimes.append(foundPrimes)
        return totalPrimes

    def _getFullReptendPositions(self, prime):
        r = Rational(1,prime,10)
        scalesPeriod = r.scalesPeriod()
        fullReptendPositions = []
        for i in range(len(scalesPeriod)):
            if scalesPeriod[i] == prime - 1:
                fullReptendPositions.append(i+2)
        return fullReptendPositions

    def _rangeIterationBasement(self, prime, currentNumber, fullReptendPositions):
        if currentNumber < len(fullReptendPositions):
            researchBasement = fullReptendPositions[currentNumber]
        else:
            totalCycles = int(currentNumber / len(fullReptendPositions))
            localCycle = currentNumber % len(fullReptendPositions)
            researchBasement = fullReptendPositions[localCycle]
            researchBasement += prime * totalCycles
        return researchBasement

    def getRangeScales(self, prime=7, baseNumberStart=0, baseNumberEnd=2):
        fullReptendPositions = self._getFullReptendPositions(prime)
        totalScales = []
        if len(fullReptendPositions) == 0:
            return totalScales
        for i in range(baseNumberStart, baseNumberEnd+1):
            scale = self._rangeIterationBasement(prime, i, fullReptendPositions)
            totalScales.append(scale)
        return totalScales


    def find(self, prime=7, base=10, type='sub'):
        if type == 'sub':
            return self._findSubPrimes(prime,base)
        if type == 'full':
            return self._findFullPrimes(prime,base) #probably need to limit amount of digits to check
        if type == 'combined':
            return self._findCombinedPrimes(prime, base) #amount, and also depth of bases to go needed
        print('Unknown Cyclic Prime type ',type)
        return []


    def _findFullPrimes(self, prime, base):
        fullCyclePrimes = set()
        primes = Primes()
        rList = [] #SEAMS NO NEED LATER REFACT
        for n in range(1,prime-1): #fill all possible cycle shifts
            rList.append(Rational(n, prime, base))
            for i in range(prime, self._digitsToCheck): #now search firstStep of length 1 to P-1
                number = rList[n-1].intFromFract(i) #later need to make for all the shifts (all of rList elements)
                if primes.isPrime(number):
                    fullCyclePrimes.add(int(number))
        intList = sorted(fullCyclePrimes)
        strList = [str(num) for num in intList]
        return strList


    def descriptionForFullCycle(self, prime, primeList, base):
        #this code maybe very slow, we can update it with gmpy2 later
        rational = Rational(1, prime, base) #please not that we must search in certain basement, and probably it would have to be updated later
        rDigits = rational.digits('period')
        #on the start from qml we can call this function only if there is sinlge basement used
        for i in range(len(primeList[0])): #emm I don't know really why 0 sorry lol
            amountOfCycles = int( len(primeList[0][i]) / len(rDigits) )#emm I don't know really why 0 sorry lol - pay attention :)
            print('For number ', primeList[0][i], 'amount of cycles is',amountOfCycles) #emm I don't know really why 0 sorry lol
            #then use trace sub to find real positions
        return 'some text to describe full cycle prime number'

   #and make help function to make short label about found full-cycle-primes


    def _findSubPrimes(self, prime, base):
        #print('Searching sub-cyclic primes for ',prime, base)
        subPrimes = set()
        primes = Primes()
        rList = [] #SEAMS NO NEED LATER REFACT
        for n in range(1,prime-1): #fill all possible cycle shifts
            rList.append(Rational(n, prime, base))
            #ok maybe later it would be good to show from which exactly parts each prime came, as only 1/p doesn't show all of them!
            for i in range(1, prime-1): #now search firstStep of length 1 to P-1
                number = rList[n-1].intFromFract(i) #later need to make for all the shifts (all of rList elements)
                primesFromNumber = primes.decompose(number)
                #here must be check for all of them are they inside
                ##print("Primes from ",number," are ", primesFromNumber)
                for checkPrime in primesFromNumber:
                    if int(checkPrime) in subPrimes:
                        continue #and maybe create list notSubPrimes to skip already checked
                    if self._checkPrimeIsSub(checkPrime, base, rList[n-1]) == True:
                        subPrimes.add(int(checkPrime))
        return sorted(subPrimes)


    def _checkPrimeIsSub(self, prime, base, rational):
        #print('Checking prime is sub, for ', prime, base, rational)
        primePart = int(prime) #or gmpy later, but yet is very ok, as numbers are short
        firstDigit = primePart % base
        rDigits = rational.digits('period')
        possibleStartIndex = []
        for i in range(len(rDigits)):
            if rDigits[i] == firstDigit:
                possibleStartIndex.append(i)
        if len(possibleStartIndex) == 1:
            #print("We have only one possible start index: best option, lets check next ")
            return self._traceSub(primePart, base, possibleStartIndex[0], rDigits)
        elif len(possibleStartIndex) == 0:
            #print("We dont have any possible start index: number not sub-cyclic")
            return False
        else:
            for checkStart in possibleStartIndex:
                if self._traceSub(primePart, base, checkStart, rDigits):
                    return True
            return False


    def _traceSub(self, prime, base, startIndex, rDigits): #later reuse this for combined or write similiar function
        #print('Starting trace sub ', prime, base, startIndex, rDigits)
        primePart = prime
        currentIndex = startIndex

        while primePart > 0:
            currentDigit = primePart % base
            primePart = int(primePart / base)

            rationalDigit = rDigits[currentIndex]
            if rationalDigit != currentDigit:
                #print('NOT TRACED on ', rationalDigit, currentDigit, currentIndex)
                return False

            currentIndex -= 1
            if currentIndex < 0:
                currentIndex = len(rDigits) - 1
        return True


