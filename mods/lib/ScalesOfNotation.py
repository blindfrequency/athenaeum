#!/usr/bin/env python
# -*- coding: utf-8 -*-
from fractions import gcd
import math #useless?
import gmpy2

from mods.lib.Rational import Rational

def reduceFraction(num, den):
    common_divisor = gcd(num, den)
    (rNum, rDen) = (num / common_divisor, den / common_divisor)
    return int(rNum), int(rDen)

class ScaleOfNotation:
    def __init__(self,parent=None):
        pass

    def translate(self, origin, originBase=10, destBase=2):
        origin = origin.upper()
        n = gmpy2.mpz(origin,originBase)
        result = n.digits(destBase)
        return result

    def translateSepparated(self, strList, originBase=10, destBase=2):
        digits = strList.split()
        origin = 0
        for d in digits:
            origin *= originBase
            origin += int(d)
        n = gmpy2.mpz(origin)
        result = n.digits(destBase)
        return result

    def translateRational(self, rStr, originBase=10, destBase=2):
        divisor = rStr.find('/')
        numStr = rStr[0:divisor]
        denStr = rStr[divisor+1:]
        num = gmpy2.mpz(numStr, originBase)
        den = gmpy2.mpz(denStr, originBase)
        n, d = reduceFraction(num,den)
        print('Debug trans rat ',num,den, n, d)
        r = Rational(n,d,destBase)
        return str(r)

    def translateFraction(self, fStr, originBase=10, destBase=2):
        r = transFract(fStr, originBase, destBase)
        print('Debug translate fraction ',repr(r),r)
        return str(r)
