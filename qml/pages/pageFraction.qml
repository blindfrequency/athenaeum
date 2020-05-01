import QtQuick 2.12
import QtQuick.Controls 2.5
import Athenum 1.0

import '../components'

Item {

    id: pageRational

    property string athName: "Rational"
    property int requestedWidth: width
    property int requestedHeight: 800

    TextField{
        id: num
        y: 5
        x: 0
        width: parent.width/2 - 10
        placeholderText: 'num'
        text: "1"
    }
    TextField{
        id: den
        y: 5
        x: parent.width/2
        width: parent.width/2 - 10
        placeholderText: 'den'
        text:  "7"
    }
    TextField{
        id: originScale
        y: 55
        x: 0
        width: parent.width/4 - 10
        placeholderText: 'origin scale'
        text:  "10"
    }
    TextField{
        id: destScale
        y: 55
        x: parent.width/4
        width: parent.width/4 - 10
        placeholderText: 'dest scale'
    }

    Button{
        text: 'change scale'
        onClicked: {
            result.text = translator.translate(num.text, parseInt(originScale.text), parseInt(destScale.text))
            result.text += ' / '
            result.text += translator.translate(den.text, parseInt(originScale.text), parseInt(destScale.text))
            rNum.calc(parseInt(num.text),parseInt(den.text),parseInt(destScale.text))
            result.text += ' = '
            result.text += rNum.getFullString()
        }
        y: 55
        x: 2*parent.width/4
        width: parent.width/4 - 10
    }

    Button{
        text: 'reduce'
        onClicked: {
            rNum.calc(parseInt(num.text),parseInt(den.text),parseInt(originScale.text))
            result.text = num.text + '/' + den.text
            result.text += ' = '
            result.text += rNum.getFullString()
            //can also extend decomposing on primes
            //can even make somewat to cross those that can be reduced, but
        }
        y: 55
        x: 3*parent.width/4
        width: parent.width/4 - 10
    }

    Text{
        y: 110
        font.pixelSize: 20
        color: 'green'
        id: result
        anchors.horizontalCenter: parent.horizontalCenter
    }

    //num denum reduction
    //change scale of notation

    Rational{
        id: rNum
    }

    ScaleOfNotation{
        id: translator
    }


    WikiLink{
        x: parent.width - width - 30
        y: 120
        link: 'https://en.wikipedia.org/wiki/Rational_number'
        pageName: 'Rational number'
    }

}
