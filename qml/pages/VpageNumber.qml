import QtQuick 2.10
import QtQuick.Window 2.10
import QtQuick.Controls 2.2
import Athenum 1.0
import '../components'


Item {
    id: pageNumber

    property string athName: "Циферки" //My dear son, I love you so much
    property int requestedWidth: width
    property int requestedHeight: 600

    Button {
        highlighted: true
        y: 80
        x: 20
        text: "-"
        onPressed:  {
            var num = parseInt(numberText.text)
            num -= 1
            numberText.text = num
            labelNumber()
        }
    }
    Button {
        highlighted: true
        y: 80
        x: parent.width - width - 20
        text: "+"
        onPressed: {
            var num = parseInt(numberText.text)
            num += 1
            numberText.text = num
            labelNumber()
        }
    }

    SimpleNumbers {
        id: simpleNumbers
    }

    function labelNumber() {
        var num = parseInt(numberText.text)
        var numText = simpleNumbers.numberToText(num)
        wordText.text = numText
        voiceTimer.running = true
    }

    Timer{
        id: voiceTimer
        repeat: false
        running: false
        interval: 10

        onTriggered: {
            simpleNumbers.voiceText(wordText.text)
        }
    }

    Button {
        anchors.horizontalCenter: parent.horizontalCenter
        y: 10
        onPressed: {
            countTimer.running = true
        }
        text: "Счёт"
    }

    Timer{
        id: countTimer
        repeat: true
        running: false
        interval: 2000

        property int count: 21

        onTriggered: {
            numberText.text = countTimer.count
            labelNumber()
            countTimer.count += 1
            if (countTimer.count > 100)
                countTimer.repeat = false
        }
    }


    TextEdit {
        id: numberText
        text: "10"
        anchors.horizontalCenter: parent.horizontalCenter
        y: 80
        font.pixelSize: 80
    }

    Text {
        id: wordText
        text: "Десять"
        anchors.horizontalCenter: parent.horizontalCenter
        y: 300
        font.pixelSize: 60
        font.capitalization: Font.Capitalize
    }
}
