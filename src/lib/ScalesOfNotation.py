#!/usr/bin/env python
# -*- coding: utf-8 -*-
from fractions import gcd
import math
from lib.Rational import Rational

import lib.Athenum as Athenum
if Athenum.useGmpy == True:
    import gmpy2



def reduceFraction(num, den):
    common_divisor = gcd(num, den)
    (rNum, rDen) = (num / common_divisor, den / common_divisor)
    return int(rNum), int(rDen)

class ScaleOfNotation: #rename here or file
    def __init__(self,parent=None):
        pass

    def translate(self, origin, originBase=10, destBase=2):
        origin = origin.upper()
        if Athenum.useGmpy == True:
            n = gmpy2.mpz(origin,originBase)
            result = n.digits(destBase)
            return result
        else:
            print("Gmpy is out, check [undone]")
            return []

    def translateSepparated(self, strList, originBase=10, destBase=2):
        digits = strList.split()
        origin = 0
        for d in digits:
            origin *= originBase
            origin += int(d)

        if Athenum.useGmpy == True:
            n = gmpy2.mpz(origin,originBase)
            result = n.digits(destBase)
            return result
        else:
            print("Gmpy is out, check [undone]")
            return []

    def translateRational(self, rStr, originBase=10, destBase=2):
        divisor = rStr.find('/')
        numStr = rStr[0:divisor]
        denStr = rStr[divisor+1:]
        if Athenum.useGmpy == True:
            num = gmpy2.mpz(numStr, originBase)
            den = gmpy2.mpz(denStr, originBase)
        else:
            print('Gmpy is out, check [undone]')
            num = int(numStr, originBase)
            den = int(denStr, originBase)

        n, d = reduceFraction(num,den)
        print('Debug trans rat ',num,den, n, d)
        r = Rational(n,d,destBase)
        return str(r)

    def translateFraction(self, fStr, originBase=10, destBase=2):
        r = transFract(fStr, originBase, destBase)
        print('Debug translate fraction ',repr(r),r)
        return str(r)
