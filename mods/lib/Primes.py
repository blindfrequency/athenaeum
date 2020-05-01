#!/usr/bin/env python
# -*- coding: utf-8 -*-
import gmpy2
from sympy.ntheory import primefactors, factorint, isprime
from factordb.factordb import FactorDB
from fractions import gcd

class Primes:
    def decompose(self, number, baseCheck=10):
        l = makePrimeStringList(int(number)) #makbe make list of strings that matter more like 7**2
        return l

    def fullReptend(self, base, amount):
        return 0

    def decWithSpec(self, number, spectrum, base=10):
        spectrum = spectrum.toVariant()#[0,1,1,0,1,1,0,1,1,0]
        for i in range(len(spectrum)):
            spectrum[i] = int(spectrum[i])
        totalFound = []
        #if (len(str(gmpy2.mpz(number))) > 100): #USE DIFFERENT LIBS ON DIFFERENT DISTANCE
        f = FactorDB(number)
        connection = f.connect()
        l = f.get_factor_list()
        for p in l:
            spec = pseudoSpectrum(p, base)
            if spec == spectrum:
                totalFound.append(shortVersion(str(p)))
        return totalFound

def pseudoSpectrum(intNum, base): #this function anyway doesn't makes its work perfect - only when there is a repeat out of oroborus cycle
    theNum = intNum
    spec = [0]*base
    n = gmpy2.mpz(str(intNum), 10) #ohh
    s = n.digits(base) #numbers are like digits thats why not everythong may go
    #print('Pre debug chars',s)
    for char in s:
        #print('Debug chars',char, int(char))
        spec[int(char,base)] = 1
    return spec

def shortVersion(strValue):
    l = len(strValue)
    result = strValue[0] + '..' + strValue[-1] + '; ' + str(l) + ' digits; ' + str(int(l/6))  + ' cycles; '  + str(l - int(l/6)*6) + ' out of cycle: '
    return result

def numberToBase(n, b):
    if n == 0:
        return [0]
    digits = []
    while n:
        digits.append(int(n % b))
        n //= b
    return digits[::-1]

def makePrimeList(number):
    return expendPrimeDict(factorint(number))

def expendPrimeDict(dict):
    numberList = []
    for prime in dict:
        pow = dict.get(prime)
        number = prime ** pow
        numberList.append(number)
    return numberList


def makePrimeStringList(number):
    f = FactorDB(number)
    connection = f.connect()
    #print("Connection ",connection)
    l = f.get_factor_list()
    strList = []
    for el in l:
        strList.append(str(el))
    return strList


def expendPrimeStringDict(dict):
    numberList = []
    for prime in dict:
        pow = dict.get(prime)
        if pow > 1:
            number = str(prime) + '^' + str(pow) #or **
        else:
            number = str(prime)
        numberList.append(number)
    return numberList

def primeDecomposition(num, den):
    return makePrimeList(num), makePrimeList(den)



def primesPatternInList(primesList):
    flags = []
    for number in primesList:
        if isprime(number):
            flags.append(1)
        else:
            flags.append(0)
    return flags

def primesPatternString(primesList):
    result = ''
    for number in primesList:
        if isprime(number): #replaced from gmpy
            result += 'x'
        else:
            result += 'o'
    return result



'''
for i in range(1000,10000):
    s = '1'*i #generates primes on prime positions #also its just decimal, need look other reunits
    iNum = int(s)
    f = FactorDB(iNum)
    connection = f.connect()
    primes = f.get_factor_list()
    #print("Rep dig",s,'\n',primes)
    if len(primes) == 1:
        print("On ",i,' prime')
#and all the positions are prime
'''


#SO CYLIC PRIMES SEARCH OF ANY ARE ALSO HERE
'''
maxReduced = 0
rList = []
dList = []
r = Rational(1,7,10)
#print("TEST REMAINS",r.remains(), r, repr(r), format(r))
for n in range(1000):
    i = r.intFromFract(n)

    #also CHECK is I a prime, there was an idea about it #lol that idea did hit

    remain = i % 7
    #print('On ',n,' is ',remain)
    if remain == 0:
        d = i / 7
        dList.append(d)
        counter = 0
        if d % 7 == 0:
            print("SPECIAL CASE d = ",d)
            print(int(d))
            while d % 7 == 0:
                z = d / 7
                if z == 0: break
                print(int(z),'reduced ',counter)
                counter += 1
                if counter > maxReduced:
                    maxReduced = counter #THOSE COULD BE DECOMPOSED IN MORE DEPTH 1/7*N with just numbers
                d = z

    rList.append(int(remain))

print (rList)
print (dList)
print('Max reduction',maxReduced)
'''
