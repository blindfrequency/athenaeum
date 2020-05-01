import QtQuick 2.12
import QtQuick.Controls 2.5
import '../components'
import Athenum 1.0

Item {
    id: pageReversedPrime

    property string athName: "Reversed primes"
    property int requestedWidth: width
    property int requestedHeight: 500


    WikiLink{ //later we would rename it
        x:  parent.width - 50
        link: 'https://oeis.org/A321523'
        pageName: 'OEIS: Reversed prime'
        type: 'oeis' //instead wiki
    }

    RangeSlider{

        id: primeRange

        from: 2
        to: 200

        stepSize: 1
        snapMode: RangeSlider.SnapAlways

        first.value: 2
        second.value: 100

        y: 5
        x: 10
        width: parent.width - 120 //100 from wiki link 10 start 10 offset
        //soon we must start getting rid of such constructions using only rows and % method, and auto offest calculation

        first.onMoved: {
            fillResults()
        }
        second.onMoved: {
            fillResults()
        }
        Component.onCompleted: {
            fillResults()
        }
        function fillResults(){
            var reversedPrimes = primes.getReversePrimeInRange(primeRange.first.value, primeRange.second.value)
            textArea.text = reversedPrimes.toString()
            //also require JS Cut
        }

        ToolTip {
            parent: primeRange.handle
            visible: primeRange.hovered
            text: 'Range: ' + primeRange.first.value + ' ' + primeRange.second.value
        }

    } //maybe later make it better - to be possible use big numbers
    //but then algo also used to be reviewed

    Primes{
        id: primes
    }


    ScrollView{
        id: scrollView
        y: primeRange.y + primeRange.height + 10
        height: parent.height - y
        width: parent.width

        TextArea {
         id: textArea
         placeholderText: 'Here would appear results of search'
         selectByMouse: true
        }
    }

}
