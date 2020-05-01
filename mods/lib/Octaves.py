#==================================================================================
# octaves ideas yet lay as function later maybe group them
import gmpy2
import time

from sympy.ntheory import primefactors, factorint, isprime
from fractions import gcd

def calculateOctaves(firstStep, n):
    octaves = [firstStep]
    currentStep = firstStep
    for i in range(n):
        currentStep *= 2
        octaves.append(currentStep)
    return octaves

def fillOctaveParts(firstStep):
    return [num for num in range(firstStep, firstStep*2)]

def checkStringSymmetry(checkString, octaveStart=0):
    slicer1 = slice(0,int(len(checkString)/2)+1)
    slicer2 = slice(int(len(checkString)/2),len(checkString))
    part1 = checkString[slicer1]
    part2 = checkString[slicer2]
    part2 = part2[::-1]
    print("Part1 ",part1)
    print("Part2 ",part2)

    if len(part1) != len(part2):
        print("Parts are not the same length")
        return

    for i in range(len(part1)):
        if part1[i] == 'x' and part2[i] == 'x':
            print("Both present at ", i+octaveStart+1, "and", len(checkString)-i+octaveStart)
        elif part1[i] == 'o' and part2[i] == 'x':
            print("Missing first ", i+octaveStart+1, "and second ", len(checkString)-i+octaveStart," factor ",factorint(i+octaveStart+1))
        elif part1[i] == 'x' and part2[i] == 'o':
            print("Only first here ", i+octaveStart+1, "and second missing", len(checkString)-i+octaveStart," factor ",factorint(len(checkString)-i+octaveStart))

def listToStr(scaleList):
    result = ''
    for el in scaleList:
        result += str(el) + ' '
    return result

def calculateOctaveScales(firstStep, n, type='lists'): #can also say about pentatonic later
    scales = []
    currentStep = gmpy2.mpz(firstStep)
    prevSize = len(str(currentStep)) #decimal integer
    anotherScale = []
    for i in range(n*7):

        #progres line
        if i % int(n*7/10) == 0:
            print(i, " elements ",i/7," scales")

        currentStep *= 2
        currentSize = len(str(currentStep))
        if currentSize == prevSize:
            anotherScale.append(2)
        else:
            anotherScale.append(1)
        prevSize = currentSize
        if len(anotherScale) == 7:
            #we can make a str of list and with its help get name or jusn # of scale
            if type == 'lists':
                scales.append(anotherScale)
            elif type == 'names':
                scales.append(translateScaleName(listToStr(anotherScale)))
            elif type == 'numbers':
                scales.append(getScaleNumber(listToStr(anotherScale)))
            anotherScale = []
    return scales

def translateScaleName(scale):
    scale = scale.strip()
    if scale=="2 2 1 2 2 2 1": return "Ionian major"
    elif scale=="2 1 2 2 2 1 2": return "Dorian minor"
    elif scale=="1 2 2 2 1 2 2": return "Frigian minor"
    elif scale=="2 2 2 1 2 2 1": return "Lidian major"
    elif scale=="2 2 1 2 2 1 2": return "Miksolidian major"
    elif scale=="2 1 2 2 1 2 2": return "Eolian minor"
    elif scale=="1 2 2 1 2 2 2": return "Lokrian"
    elif scale=="1 2 2 1 2 2 1": return "Symmetric 11"
    elif scale =="2 2 3 2 3": return "Major pent."
    elif scale =="3 2 2 3 2": return "Minor pent."
    return scale

def getScaleNumber(scale): #numbers according to how they appear in 1/7 also can make for start 1*2 octave
    scale = scale.strip()
    if scale=="2 2 1 2 2 2 1": return 0
    elif scale=="2 1 2 2 2 1 2": return 2
    elif scale=="1 2 2 2 1 2 2": return 4
    elif scale=="2 2 2 1 2 2 1": return 6
    elif scale=="2 2 1 2 2 1 2": return 1
    elif scale=="2 1 2 2 1 2 2": return 3
    elif scale=="1 2 2 1 2 2 2": return 7
    elif scale=="1 2 2 1 2 2 1": return 5
    return -1

def getScaleNameByNumber(scaleNumber):
    if scaleNumber==0: return "Ionian major"
    elif scaleNumber==2: return "Dorian minor"
    elif scaleNumber==4: return "Frigian minor"
    elif scaleNumber==6: return "Lidian major"
    elif scaleNumber==1: return "Miksolidian major"
    elif scaleNumber==3: return "Eolian minor"
    elif scaleNumber==7: return "Lokrian"
    elif scaleNumber==5: return "Symmetric 11"
    return 'unknown_scale#' + str(scaleNumber)

def getScaleFormulaByNumber(scaleNumber):
    scaleNumber = int(scaleNumber)
    if scaleNumber==0: return "2 2 1 2 2 2 1"
    elif scaleNumber==2: return "2 1 2 2 2 1 2"
    elif scaleNumber==4: return "1 2 2 2 1 2 2"
    elif scaleNumber==6: return "2 2 2 1 2 2 1"
    elif scaleNumber==1: return "2 2 1 2 2 1 2"
    elif scaleNumber==3: return "2 1 2 2 1 2 2"
    elif scaleNumber==7: return "1 2 2 1 2 2 2"
    elif scaleNumber==5: return "1 2 2 1 2 2 1"
    else: return 'unknown_scale#' + str(scaleNumber)

#
def getScaleNameFromList(scaleNumber, scalesNames):
    for scale, index in scalesNames:
        if scaleNumber == index:
            return translateScaleName(scale)
    return 'unknown_scale#' + str(scaleNumber)

def compareScaleFormulas(formula1, formula2):
    #print("Start compare ",formula1,' and ',formula2)
    if formula1 == formula2:
        return 0
    semiTones1 = [] #find index where '1'
    semiTones2 = []
    steps1 = formula1.split()
    steps2 = formula2.split() #insure there are 7 of them
    for i in range(len(steps1)):
        if steps1[i] == '1':
            semiTones1.append(i)
        if steps2[i] == '1':
            semiTones2.append(i)
    #print(len(semiTones1),len(semiTones2),' first DEBUG LINE')
    if len(semiTones1) == len(semiTones2) and len(semiTones1) == 2: #classis music scales compared
        firstAreEqual = False
        secondAreEqual = False
        directionSecond = 0
        directionFirst = 0
        if semiTones1[0] == semiTones2[0]:
            firstAreEqual = True
        else:
            directionFirst = semiTones1[0] - semiTones2[0]

        if semiTones1[1] == semiTones2[1]:
            secondAreEqual = True
        else:
            directionSecond = semiTones1[1] - semiTones2[1]
        #print(directionFirst,directionSecond,' another DEBUG LINE')
        if firstAreEqual and secondAreEqual == False:
           return directionSecond*2
        if secondAreEqual and firstAreEqual == False:
           return directionFirst
        if firstAreEqual == False and secondAreEqual == False:
           if directionFirst != directionSecond:
               print("Some issue(dirrections are opposite): ",directionFirst,directionSecond) #this would never happen in octave artiphmetics
               return 4
           return directionFirst*3
    else: #this is kind of fast thing
        if formula1 == '1 2 2 1 2 2 2' and formula2 == '1 2 2 1 2 2 1':
            return 5
        if formula1 == '1 2 2 1 2 2 1' and formula2 == '2 2 2 1 2 2 1':
            return 6
        if formula1 == '1 2 2 1 2 2 1' and formula2 == '2 2 1 2 2 2 1':
            return 7
        print("CASE 8: ", len(semiTones1), len(semiTones2),'formulas' ,formula1,' : ' ,formula2)
        return 8
    return 9

def describeCompareScaleResult(compareResult):
    if compareResult == 0: return 'Scales are equal'
    elif compareResult == 1: return 'First interval shifted'
    elif compareResult == -1: return 'First interval shifted (reversed)'
    elif compareResult == 2: return 'Second interval shifted'
    elif compareResult == -2: return 'Second interval shifted (reversed)'
    elif compareResult == 3: return 'Both intervals shifted'
    elif compareResult == -3: return 'Both intervals shifted (reversed)'
    elif compareResult == 4: return 'Big unknown difference but only 2 intervals'
    elif compareResult == 5: return '3 intervals scale appear, octave not finised'
    elif compareResult == 6: return '3 intervals scale leave, key shifted (a)'
    elif compareResult == 7: return '3 intervals scale leave, key shifted (b)'
    elif compareResult == 8: return 'NOT 2 intervals some unknown'
    elif compareResult == 9: return 'Some unexpected case'
    return 'UnknownCR' + str(compareResult)


def exploreScalesInSequence(sequenceString): #probably rename to scalesDict to be more obvious
    scalesNumbers = sequenceString.split()
    for i in range(1, len(scalesNumbers)):
        prevScale = getScaleFormulaByNumber(scalesNumbers[i-1])
        currentScale = getScaleFormulaByNumber(scalesNumbers[i])
        compareResult = compareScaleFormulas(prevScale,currentScale)
        print("Compare result ",compareResult, ' on ', i, describeCompareScaleResult(compareResult))

def compareScalesBetweenSequences(seqString1, seqString2):
    scalesNumbers1 = seqString1.split()
    scalesNumbers2 = seqString2.split()
    scale1 = getScaleFormulaByNumber(scalesNumbers1[-1])
    scale2 = getScaleFormulaByNumber(scalesNumbers2[0])
    compareResult = compareScaleFormulas(scale1,scale2)
    print("Compare result ",compareResult, describeCompareScaleResult(compareResult))

def findSequences(scalesList):
    sequences = []
    seqNumbers = {}
    seqCounter = 0
    newSeq = []
    for scale in scalesList:
        if scale == 0 and len(newSeq) > 0: #just if found first one
            currentSeqInd = 0
            seqStr = listToStr(newSeq)
            if seqNumbers.get(seqStr) != None:
                currentSeqInd = seqNumbers[seqStr]
            else:
                seqNumbers[seqStr] = seqCounter
                currentSeqInd = seqCounter
                seqCounter += 1
            sequences.append(currentSeqInd)
            newSeq = []
        newSeq.append(scale)
    return sequences, seqNumbers #also return seqNumbers

def digitSpectrumFromStr(inputStr):
    elements = inputStr.split() #only single digits yet
    spectrum = [0]*10 #works only in 10 basis yet
    for el in elements:
        if el.isdigit():
            spectrum[int(el)] += 1
    return spectrum

def digSpecDiff(digSp1, digSp2): #only first different spectrum column
    for i in range(len(digSp1)):
        if digSp1[i] != digSp2[i]:
            return i

def compareSequences(seqNames): #PLEASE REWORK _ even if they are not shown in return values, something wrong, check it back
    longestIndex = '' #longest name
    longestValue = 0
    compareResults = []
    for name, value in seqNames.items():
        currentLength = len(str(name))
        if currentLength > longestValue:
            longestValue = currentLength
            longestIndex = name
    #but basicly it the one withoun 0 scale need to find another that starts the same
    foundSet = set(longestIndex.split())
    shorterButFull = []
    for name, value in seqNames.items():
        currentSet = set(name.split())
        if currentSet == foundSet:
            if name != longestIndex:
                shorterButFull.append(name)

    fullSequence = shorterButFull[0]
    if len(shorterButFull) > 1:
        print("Found more then shorter but full value ", shorterButFull)
        expectedIndex = -1
        maxLen = 0
        for i in range( len(shorterButFull) ):
            checkName = shorterButFull[i]
            if len(checkName.split()) > maxLen:
                maxLen = len(checkName.split())
                expectedIndex = i
        fullSequence = shorterButFull[expectedIndex]
        print("Solution is ",fullSequence)

    #print("Shorter but full ",shorterButFull[0])
    #now find difference
    protoSpectrum = digitSpectrumFromStr(shorterButFull[0])
    print("Table: ")
    print(shorterButFull[0], ' the prototype')
    for name, value in seqNames.items():
        if name == shorterButFull[0]:
            pass #print("The prototype : ",name, '#',value)
        elif name == longestIndex:
            diffIndex = shorterButFull[0].find('0')
            diffStrList = list(shorterButFull[0])
            diffStrList[diffIndex] = '_' #MAYBE THERE IS SOMETHING NOT FINE IN _ that draws difference
            diffStr = "".join(diffStrList)
            compareResults.append((0, value))
            #ATTENTION getScaleByNumber probably cannot work properly it must depend on scalesNames that contain index in current search - so there must be +1 argument
            print(diffStr, ' (', 0, ') #',value,getScaleNameByNumber(0))
        else:
            currentSpectrum = digitSpectrumFromStr(name) #SETS ARE NOT BEST OPTION HERE, NEED CREATE SOMETHING LIKE digits Spectrum from string skipping spaces
            diff = digSpecDiff(protoSpectrum,currentSpectrum) # actually once will fail on 0 skip
            diffIndex = shorterButFull[0].find(str(diff))
            diffStrList = list(shorterButFull[0])
            diffStrList[diffIndex] = '_' #MAYBE THERE IS SOMETHING NOT FINE IN _ that draws difference check manually please
            diffStr = "".join(diffStrList)
            print(diffStr,' (', diff, ') #',value, getScaleNameByNumber(diff))
            compareResults.append((diff, value))
    #return list of diferences (seqIndex, diffScaleNumber)
    return compareResults


def findGroupsByPattern(sourceList, patternList):
    groups = []
    groupNumbers = {}
    groupCounter = 0
    newGroup = []
    templateStr = listToStr(patternList)
    prevBeginInd = 0
    for i in range(len(sourceList) - len(patternList)):
        subList = sourceList[i:len(patternList)+i] #check it
        subStr = listToStr(subList)
        if templateStr == subStr:
            #from prevBeginInd to i-1
            group = sourceList[prevBeginInd:i-1]
            groupStr = listToStr(group)
            prevBeginInd = i
            currentGroupInd = 0
            if groupNumbers.get(groupStr) != None:
                currentGroupInd = groupNumbers[groupStr]
            else:
                currentGroupInd = groupCounter
                groupNumbers[groupStr] = groupCounter
                groupCounter += 1
            groups.append(currentGroupInd)
    return groups, groupNumbers




'''
octs = calculateOctaves(1,6) #if -1 them will get those famos numbes, but +1 gives something too, 3 fits both of categories
#map make new?
nextToOct = list(map(lambda n: n+1, octs))
prevToOct = list(map(lambda n: n-1, octs))

print ('Octaves ',octs,' n ',nextToOct,' p ', prevToOct)

for o in octs:
    partsList = fillOctaveParts(o)
    partsList.pop(0) #remove first for symetry explore
    pStr = primesPatternString(partsList)
    print ('Fill ', o , pStr)#primesPatternInList(partsList))
    checkStringSymmetry(pStr,o)

startTime2 = time.time()
for freq in range(1,15): #there probably should be done some cool work to group all the changes from other octaves
    #THIS SHOULD BE DEVELOPED AND PROBABLY VISUALIZED FINE TO SEE AL THE DETAILS AT SAME TIME
    firstFreq = freq #14 #PLEASE CHECK HARD FOR BUGS
    scales = calculateOctaveScales(firstFreq,500,type='numbers') #5k scales takes 2.8 seconds
    print("Scales : ",scales[0:33])
    print("Scales calculated. Now search for sequences FOR THE OCTAVES FROM: ", firstFreq)
    sequences, seqNames = findSequences(scales)
    compared = compareSequences(seqNames) #MAYBE THERE IS SOMETHING NOT FINE IN _ that draws difference
    print("\ncompare result",compared)
    print("FOR ",seqNames)
#print('\nAnd seq', sequences, "\n\n\n", seqNames)
endTime2 = time.time()
diffTime2 = endTime2 - startTime2
print("time spent: " + str(diffTime2))
#pattern = [0, 1, 2, 0, 1, 3, 0, 1, 3, 0, 1, 3, 4, 1, 3, 4, 1, 3, 4, 5, 4, 5, 4, 5, 6, 5, 6, 5, 6, 5, 6, 7]
pattern = sequences[0:7]
#autosearch next or just produce as N first elements of sequences
groups, groupNames = findGroupsByPattern(sequences,pattern)
print("\n\n\nGroup names: ",groupNames) #check on auto or just switch
print("Groups: ",groups)
'''



'''
######SCALES CHECK############
prevSeq = ''
for seq, index in seqNames.items():
    print("\nSequence ",seq ," with idx ",index)
    exploreScalesInSequence(seq)

print("\nBETWEEN CHECKS")
for i in range(33):
    #print("Between ",i)
    seqNum = sequences[i]
    sequence = ''
    for seq, index in seqNames.items():
        if index == seqNum:
            sequence = seq

    if prevSeq != '':
        compareScalesBetweenSequences(prevSeq,sequence) #actually there may be different path of between appear
    prevSeq = sequence
'''
