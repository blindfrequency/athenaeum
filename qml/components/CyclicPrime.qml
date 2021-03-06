import QtQuick 2.12
import QtQuick.Controls 2.5
import '../components'
import Athenum 1.0

Item {
    id: cyclicPrimesItem

    property int prime: 0
    property string primeTypeStr: "sub"
    property bool dontScroll: false

    Component.onCompleted: {
        if (prime !== 0)
            calc()
        primeCombo.setPrime(prime)
    }

    function calc(){
        var scales = cyclicPrimes.getRangeScales(prime,parseInt(baseRange.first.value),parseInt(baseRange.second.value))
        var primeNumber = prime
        if (decimalFlag.checked){
            var subCyclic = cyclicPrimes.find(primeNumber,10,primeType.currentText)
            textArea.text = 'Prime numbers:\n' + subCyclic.toString() + '\n'
            return;
        }

        if (showBase.checked === false){
            var subCyclic = cyclicPrimes.findInRange(primeNumber,parseInt(baseRange.first.value),parseInt(baseRange.second.value), primeType.currentText) //depend type on ComboBox
            textArea.text = 'Scales are:\n' + scales.toString() + '\nPrime numbers:\n' + subCyclic.toString() + '\n'
            //ALSO when the line is very long need to sepparate subCyclic string into several
            //need to have some nice JavaScript utils that could be connected to any qml file
            //that would split string into several with '\n' according to
            if (parseInt(baseRange.first.value) === parseInt(baseRange.second.value))
                    if (primeType.currentText === 'full'){
                        textArea.text += cyclicPrimes.descriptionForFullCycle(primeNumber, subCyclic, parseInt(baseRange.first.value))
                    //full description is jet to be done, sorry :) but there is first stone here
                    }
        }
        else{

            textArea.text = ''
            for (var i = 0; i < scales.length; ++i){
                var nextPrimes = cyclicPrimes.findInRange(primeNumber, parseInt(i), parseInt(i), primeType.currentText) //depend type on ComboBox
                textArea.text += 'For scale: ' + scales[i] + ' primes are ' + nextPrimes + '\n'
            }
        }


    }

    ComboBox{
        id: primeType
        model: ['sub', 'full','combined'] //full-cycle and scale-shaped
        y: 5
        x: 10
    }


    PrimeComboBox{
        id: primeCombo
        y: 5
        x: primeType.width + 20
        //later extend with some special types, like full reptend based on scale of notation

        //on change?
        onTextChanged: {
            prime = parseInt(primeCombo.text)
        }
    }


    RangeSlider { //TODO replace by basic one or make it an alternative option
        id: baseRange

        from: 0
        to: 21
        stepSize: 1
        snapMode: RangeSlider.SnapAlways

        property string scalesRange: ''

        first.value: 0
        second.value: 1

        ToolTip {
            parent: baseRange.handle
            visible: baseRange.hovered
            text: 'Bases n: ' + baseRange.first.value + ' ' + baseRange.second.value + ' [' + baseRange.scalesRange + ']'
            //THERE MUST BE DECRIPTION it could be done now!
        }

        first.onMoved: {
            showScales()
        }
        second.onMoved: {
            showScales()
        }
        Component.onCompleted: {
            showScales()
        }
        function showScales(){
            var scales = cyclicPrimes.getRangeScales(prime,parseInt(baseRange.first.value),parseInt(baseRange.second.value))
            baseRange.scalesRange = scales.toString()
        }

        y: 5
        x: parent.width/2 - width/2
        width: 400
    }

    Button{
        y:5
        x: parent.width - width - 10
        text: 'Calc'
        onPressed: {
            cyclicPrimesItem.calc()
        }
    }

    CheckBox {
        y: 5
        x: baseRange.x + baseRange.width + 10
        text: 'Show base groups'
        id: showBase
    }

    CheckBox {
        y: 5
        x: showBase.x + showBase.width + 10
        text: 'dec'
        id: decimalFlag
    }


    CyclicPrimes{
        id: cyclicPrimes
    }

    ScrollView{
        id: scrollView
        y: primeType.y + primeType.height + 10
        height: parent.height - y
        width: parent.width

        TextArea {
         id: textArea
         placeholderText: 'Here would appear results of search'
         selectByMouse: !dontScroll
        }

    }

}
