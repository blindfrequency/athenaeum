#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
#comment next line to get to PyQt - yet it not works whole
os.environ['QT_API'] = 'pyside2'
from qtpy import QtGui, QtCore, QtQml, QtQuick
from qtpy.QtGui import QGuiApplication
from qtpy.QtCore import Property, Signal, QUrl, QObject, QDir, Slot, QFile, QIODevice, QCryptographicHash, QByteArray
from qtpy.QtQml import qmlRegisterType, QQmlContext, QQmlApplicationEngine, QQmlEngine
from qtpy.QtQuick import QQuickView
import importlib
import platform
useGmpy = True # flag created, but yet it cannot work well anyway


def playGroundArea(): #this function used to check some console functions without running the whole thing

    athInfo = AthenumInfo()
    # presets/ ComponentNames / preset name
    print("Ath info created")



def athenumEngineStart():

    import qtpy
    print("qtpy version: ", qtpy.__version__)
    print("dest: ", os.environ['QT_API'])
    
    app = QGuiApplication(sys.argv)

    athenumInfo = AthenumInfo()
    athenumModules = AthenumModules()

    playGroundMode = False

    if len(sys.argv) > 1:
        if sys.argv[1] == '-platform' and sys.argv[2].find('webgl') != -1:
            print("Starting WebGl mode")
            athenumInfo.setWebGL()
        if sys.argv[1] == '-pg':
            playGroundMode = True
            print("PlayGround mode activated")
            playGroundArea()
            sys.exit(0)
    else:
        pass

    app.setOrganizationName("Athenum NPO")
    app.setOrganizationDomain("none.ru")
    app.setApplicationName("Athenum")

    athenumModules.wrapAndLoad('lib/Rational.py')
    athenumModules.wrapAndLoad('lib/Primes.py')
    athenumModules.wrapAndLoad('lib/GeometricProgression.py')
    athenumModules.wrapAndLoad('lib/ScalesOfNotation.py')
    athenumModules.wrapAndLoad('lib/CyclicPrimes.py')

    athenumModules.wrapAndLoad('lib/SimpleNumbers.py')

    athenumModules.load("qt.SumModels")
    athenumModules.load("qt.DigitalCircle")
    athenumModules.load("qt.PrimeScales")
    athenumModules.load("qt.AbstractOctaves")
    athenumModules.load("qt.IntervalScales")

    engine = QQmlApplicationEngine()
    athenumModules.setQmlEngine( engine )

    platformName = platform.system()
    print('Platform name is',platformName)

    if platformName == 'Linux':
        athenumModules.loadQMLPlugin("qt/libqmlideas.so","IdeasLib")


    #qmlLatex = QMLLatex()
    copyClipboard = CopyClipboard()

    engine.rootContext().setContextProperty("athenumInfo",athenumInfo)
    engine.rootContext().setContextProperty("athenumModules",athenumModules)
    #engine.rootContext().setContextProperty("QMLLatex",qmlLatex)
    engine.rootContext().setContextProperty("copyClipboard",copyClipboard)

    engine.load('../qml/athenum.qml')

    if platformName != 'Windows':
        import resource
    print("Starting viewer")

    res = app.exec_()
    if platformName != 'Windows':
        print('Max RAM usage: ',resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    del engine
    #serverthread.stop()
    sys.exit(res)


def listToStr(scaleList):
    result = ''
    for el in scaleList:
        if result != '':
            result += ','
        result += str(el)
    return result

class AthenumWrapper: #TODO move to sepparated place + make proper refactoring + wipe issues
    def __init(self,parent=None):
        pass

    #LATER WE CAN: A) mercge few classes into one, holding their functions together
    #B) add global functions
    #C)translate value, for example QJSValue to normal Python, or to int if needed
    #D)Configuration, to change any of params
    #E) teach to make wrapper even for pre compiled wheels

    def open(self, filename): #just need cut empty lines, and thats it
        f = open(filename,'r')
        self._openedFile = filename
        allData = f.read()
        f.close()
        fileLines = allData.split('\n')
        #print('File got ',len(fileLines))
        for i in range(len(fileLines)):
            if len(fileLines[i]):
                if fileLines[i].find('#') == 0:
                    pass #skip comment
                elif fileLines[i].find("'''") == 0:
                    pass
                    #print('Many lines comment found on ',i+1)
                else:
                    pass
                    #print(i+1,"'",fileLines[i],"'")

            if fileLines[i].find('class') == 0:
                classDefinition = fileLines[i]

                #find className its after class , but before ( or : what is first
                nameEnd = classDefinition.find('(')
                if nameEnd == -1:
                    nameEnd = classDefinition.find(':')
                className = classDefinition[6:nameEnd]

                #print('Found ', className, 'on',i+1,' and',classDefinition)
                firstLine = fileLines[i+1] #expects that all the comments are deleted
                firstDepth = len(firstLine) - len(firstLine.lstrip(' '))
                #print('Depth of first line is ',firstDepth)

                functionList = []
                returnFlags = []
                n = i+1
                while True:
                    #print('N and len',n,len(fileLines))
                    if n >= len(fileLines):
                        break
                    lstripLine = fileLines[n].lstrip(' ')
                    depth = len(fileLines[n]) - len(lstripLine)
                    if depth < firstDepth and len(fileLines[n]) and fileLines[n].find('#') != 0:
                        #print("Depth broken on ",n)
                        i = n-1
                        break
                    if lstripLine.find('def') == 0:
                        bStart = lstripLine.find('(')
                        bEnd = lstripLine.find(')')
                        fName = lstripLine[4:bStart]
                        params = lstripLine[bStart+1:bEnd]
                        pList = params.split(',')
                        #clean default arguments

                        #please skip all the _ and __ functions
                        if fName.find('_') != 0:
                            functionList.append([fName,pList])#fileLines[n])
                            returnFlags.append(False)
                        #FIND () - find amount of parameters, sepparate them
                    if lstripLine.find('return') != -1:
                        returnFlags[-1] = True
                    n += 1

                #print('For ',classDefinition, functionList, returnFlags)

                wrapFileName = 'wrap/athwrap_' + className + '.py'
                importFileName = filename[0:filename.find('.py')]
                importFileName = importFileName.replace('/','.')
                wf = open(wrapFileName,'w') #autogenerate fine later lol

                #qmlf = open('wrap/athqml_' +className +'.qml','w')


                wf.write('from ' + importFileName + ' import ' + className + '\n')
                wf.write('from qtpy.QtCore import Qt, Slot, Signal, QObject\n')
                wf.write('from qtpy.QtQml import qmlRegisterType')
                wf.write('\n')
                wf.write('def registerQMLTypes():\n')
                wf.write("    qmlRegisterType(Wrap" + className + ", 'Athenum', 1,0, '" + className + "')\n")
                wf.write('def getQMLTypes():\n')
                wf.write("    theTypes = ['" + className + "']\n")
                wf.write('    return theTypes\n')
                wf.write('\n')
                wf.write('class Wrap' + className + '(QObject):\n')
                wf.write('    def __init__(self,parent=None):\n')
                wf.write('        QObject.__init__(self,parent)\n')
                wf.write('        self._wrappedObject = ' + className + '()\n')
                wf.write('\n')

                for j in range(len(functionList)):

                    if len(functionList[j][1]):
                        slots = ["'QVariant'"]*(len(functionList[j][1])-1)
                    if returnFlags[j]:
                        slots.append("result='QVariant'")

                    functionName = functionList[j][0]
                    arguments = listToStr(functionList[j][1])
                    callArg = ''

                    for argInd in range(1,len(functionList[j][1])):
                        if len(callArg) > 0:callArg += ','
                        arg = functionList[j][1][argInd]
                        if arg.find('=') != -1:
                            defaultPart = arg[arg.find('=')+1:]
                            defaultPart = defaultPart.strip()
                            arg = arg[0:arg.find('=')]

                            #print('DEBUG DEFAULT part for arg',defaultPart,arg,defaultPart.isdigit())
                            if defaultPart.isdigit():
                                slots[argInd-1] = "'int'"
                                #print('Type changed to int on index ',argInd-1)
                                #print('Change result: ',slots,'for',functionName)
                        callArg += arg

                    #print(j, functionList[j], returnFlags[j])

                    wf.write('    @Slot(' + listToStr(slots) + ')\n')
                    wf.write('    def ' + functionName + '(' + arguments+ '):\n')

                    #HEY HEY JUST HERE - we can also make QML from document above
                    #PageArea and inside it : function name, + parameters name
                    # + Repeater that make textfields in amount of arguments


                    if returnFlags[j]:
                        wf.write('        return self._wrappedObject.' + functionName+ '(' + callArg + ')\n')
                    else:
                        wf.write('        self._wrappedObject.' + functionName + '(' + callArg + ')\n')
                    wf.write('\n')

                wf.close()
                return wrapFileName

    def wrap(self, outputFile):
        pass



class AthenumInfo (QObject): #TODO Move to sepparated place
    def __init__(self, parent = None):
        QObject.__init__(self, parent)
        self._path = QDir.currentPath()
        self._OS = str("linux")
        self._webGL = False
    @Slot(result='QString')
    def getQMLPath(self):
        return QDir.cleanPath(self._path  + '/../qml')
    @Slot(result='QString')
    def getPath(self): #https://stackoverflow.com/questions/110362/how-can-i-find-the-current-os-in-python
        return self._path
    @Slot(result='QString')
    def getOS(self):
        return self._OS
    @Slot(str,result='QString')
    def cutShortURL(self, sourceURL):
        replaceString = str("file://") + self._path + '/../qml'
        sourceURL = sourceURL.replace(replaceString,"%app%")
        return sourceURL
    @Slot(str,result='QString')
    def extendURL(self, sourceURL):
        replaceString = str("file://") + self._path + '/../qml'
        sourceURL = sourceURL.replace("%app%",replaceString)
        return sourceURL
    @Slot(str,result='QString')
    def cutAppPath(self, sourceURL):
        replaceString = str("file://") + self._path + '/../qml'
        sourceURL = sourceURL.replace(replaceString,"")
        return sourceURL
    @Slot(result='QVariant')
    def isWebGl(self):
        return self._webGL
    def setWebGL(self):
        self._webGL = True

    @Slot(str,result='QString')
    def md5fromFile(self, filename):
        filename = filename.replace("file://","")
        filename = filename.replace("file://","")#dirty trick for both os
        file = QFile(filename)
        file.open(QIODevice.ReadOnly)
        hash = QCryptographicHash(QCryptographicHash.Md5);
        hash.addData(file)
        strVal = str(hash.result().toHex())
        return strVal

    def findQmlNames(self, dir, shortDir):
        resultList = []
        d = QDir("")
        d.cd(dir)
        l = d.entryList()
        for file in l:
            anotherFile = shortDir + file
            resultList.append(anotherFile)
        resultList.pop(0)
        resultList.pop(0)
        return resultList


    @Slot(result='QVariant')
    def loadQmlFilesList(self):
        pageList = self.findQmlNames("../qml/pages","/pages/")
        compList = self.findQmlNames("../qml/components","/components/")
        return pageList + compList


    def addPreset(componentName, presetName, presetJson, description=''):
        pass
        #Если запись уже есть с таким именем пресета - она просто редактируется
        #Если нет - добавляется новая

    def listOfComponents(): #returns all the component names
        pass

    def listOfPresets(componentName):
        pass

    def editPreset(componentName, presetName, newPresetName, presetJson, description=''):
        pass

    def parseArray(jsonArrayString):
        pass #return list of strings

    def makeArray(listOfStrings):
        pass


def athenumModuleImport(moduleName):
    module = importlib.import_module(moduleName)
    module.registerQMLTypes()
    return module

class AthenumModules (QObject): #TODO Move to sepparated place
    def __init__(self, parent = None):
        QObject.__init__(self,parent)
        self._modules = []
        self._modulesNames = []
        self._pluginsNames = []
        self._pluginsFiles = []

    @Slot('QString')
    def wrapAndLoad(self,moduleName):
        a = AthenumWrapper()
        wrapName = a.open(moduleName)
        self.load(wrapName)

    @Slot('QString')
    def load(self, moduleName):
        moduleName = moduleName.replace("/",".")
        moduleName = moduleName.replace(".py","")
        self._modules.append(athenumModuleImport(moduleName))
        self._modulesNames.append(moduleName)

    @Slot(result='QVariant')
    def getModulesNames(self):
        return self._modulesNames
    @Slot(int,result='QVariant')
    def getQMLTypes(self,index):
        return self._modules[index].getQMLTypes()
    @Slot(str,str,result='bool')
    def loadQMLPlugin(self, filename, importName):
        print("Starting loading of plugin " + filename)
        errList = []
        result = self._engine.importPlugin(filename,importName,errList)
        if result == True:
            self._pluginsFiles.append(filename)
            self._pluginsNames.append(importName)
        print("Loading qml plugin ended with result " + str(result))
        return result
    @Slot(result='QVariant')
    def getPluginsNames(self):
        return self._pluginsNames
    @Slot(result='QVariant')
    def getPluginsFiles(self):
        return self._pluginsFiles
    def setQmlEngine(self, eng):
        self._engine = eng


#LATEX from sympy was removed

from qtpy.QtCore import QMimeData
from qtpy.QtGui import QImage
from qtpy.QtGui import QGuiApplication
from qtpy.QtGui import QClipboard

class CopyClipboard(QObject): #TODO Move to sepparated place
    def __init__(self, parent=None):
        QObject.__init__(self,parent)

    @Slot('QString')
    def copyImageFile(self, filename):
        clipboard = QGuiApplication.clipboard()
        image = QImage(filename)
        data = QMimeData()
        data.setImageData(image)
        clipboard.setMimeData(data, mode)

    @Slot('QVariant')
    def copyImageSrc(self, image):
        clipboard = QGuiApplication.clipboard()
        clipboard.setImage(image)

    @Slot('QString')
    def copyText(self, text):
        clipboard = QGuiApplication.clipboard()
        clipboard.setText(text)

