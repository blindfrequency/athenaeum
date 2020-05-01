#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mods.lib.Rational import Rational #maybe make also Arithmetic progression
#sometimes default parameters is force to use it for wrapper

class GeometricProgression:
    def set(self, first=14, inc=2, dec=100):
        self._firstStep = first
        self._increseCoef = inc
        self._decreaseCoef = dec

    def getInc(self):
        return self._increseCoef
    def getDec(self):
        return self._decreaseCoef
    def getFirst(self):
        return self._firstStep

    def getQ(self):
        return self._increseCoef / self._decreaseCoef

    def firstElement(self):
        return self._firstStep / self._decreaseCoef

    def converges(self):
        if self.getQ() < 1.0: return True
        return False

    def countAt(self, n=0):
       #t = time.time()
       nom = self._firstStep * (self._increseCoef ** n)
       den = self._decreaseCoef ** (n+1)
       result = Rational(nom,den)
       #dT = time.time() - t
       return result

    def sumAt(self,n):
        n += 1
        sum = self.countAt(0)
        for i in range(1,n):
            newSum = sum + self.countAt(i)
            #print("AT ",i,repr(sum),repr(self.countAt(i)),repr(newSum))
            sum = newSum
        return sum

    def fullSum(self):
       sum = (self._firstStep / self._decreaseCoef) / (1.0 - self._increseCoef/self._decreaseCoef)
       return sum

    def rationalSum(self):
       den = Rational(self._firstStep, self._decreaseCoef)
       num = Rational(self._decreaseCoef-self._increseCoef,self._decreaseCoef)
       sum = den/num
       return sum

    def rSumQML(self):
       r = self.rationalSum()
       result = [str(r._num),str(r._den),str(r._scaleOfNotation), r.__str__()]
       return result

    def rElementQML(self,n=0):
        r = self.countAt(n)
        result = [str(r._num),str(r._den),str(r._scaleOfNotation), r.__str__()]
        return result

    def reducedElementQML(self,n=0):
        r = self.countAt(n)
        r.reduce()
        result = [str(r._num),str(r._den),str(r._scaleOfNotation), r.__str__()]
        return result
