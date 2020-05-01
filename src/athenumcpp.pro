TEMPLATE = app
CONFIG += console c++11
CONFIG -= app_bundle
CONFIG -= qt

SOURCES +=

#THIS PROJECT USED TO RUN PYTHON INTERPRITER, THAT WOULD RUN ATHENUM PYTHON but yet its just enough of python

linux:!android {
    message("* Using settings for Unix/Linux.")
    LIBS += -lpython3.6
    INCLUDEPATH += /usr/include/python3.6
}

DISTFILES += \
    ../qml/athenum.qml \
    ../qml/components/AthenumPage.qml \
    ../qml/components/CyclicPrime.qml \
    ../qml/components/InervalScales.qml \
    ../qml/components/PrimeComboBox.qml \
    ../qml/components/PrimeScalesTable.qml \
    ../qml/components/WikiLink.qml \
    ../qml/pages/VpageNumber.qml \
    ../qml/pages/pageCircles.qml \
    ../qml/pages/pagePrimeScales.qml \
    ../qml/pages/pageProcess.qml \
    ../qml/pages/mods.qml \
    ../qml/pages/pageReversedPrime.qml \
    example/Process.py \
    example/NoughtsCrosses.py \
    ../qml/NoughtsCrosses.qml \
    example/Snake.py \
    ../qml/pages/test.qml \
    ../qml/components/CircleView.qml \
    ../qml/components/Octavizer.qml \
    ../qml/components/AnimationRecorder.qml \
    ../qml/components/Summator2.qml \
    ../qml/components/AutoSum.qml \
    ../qml/pages/pageFullReptendPrime.qml \
    ../qml/pages/pageGeomProgression.qml \
    ../qml/pages/pageRepeatingFraction.qml \
    ../qml/pages/pageOctaves.qml \
    ../qml/components/LatexFormula.qml \
    ../qml/components/MultiSum.qml \
    ../qml/pages/pagePrime.qml \
    ../qml/pages/pageFraction.qml \
    ../qml/components/DigitalSpectrum.qml \
    ../qml/components/Regularity.qml \
    ../qml/components/ExpendableLoader.qml \
    ../qml/components/PageArea.qml \
    ../qml/pages/pageScaleOfNotation.qml \
    lib/SimpleNumbers.py \
    qt/AbstractOctaves.py \
    qt/DigitalCircle.py \
    ../qml/pages/test2.qml \
    lib/GeometricProgression.py \
    lib/Primes.py \
    lib/Rational.py \
    lib/ScalesOfNotation.py \
    qt/IntervalScales.py \
    qt/PrimeScales.py \
    qt/SumModels.py \
    lib/Octaves.py \
    lib/Athenum.py \
    ath.py \
    ../LICENSE.LGPLv3 \
    ../TODO \
    lib/CyclicPrimes.py \
    ../qml/pages/pageCyclicPrimes.qml \
    ../DESCRIPTION
