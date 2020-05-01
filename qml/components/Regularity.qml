import QtQuick 2.12
import QtQuick.Controls 2.5

Item {
    id: digitalSpectrumItem

    function plot(listOfDigits){
        regText.text = "Regularity: [" + listOfDigits + "]"
        regRep.model = listOfDigits.length

        var maxSpec = 0
        for (var i = 0; i < regRep.model; ++i)
            if (Math.abs(listOfDigits[i]) > maxSpec) //Just debugging
                maxSpec = Math.abs(listOfDigits[i])

        console.log('MaxSpec',maxSpec)

        for (i = 0; i < regRep.model; ++i){
            var digit = listOfDigits[i]

            if (digit > 0)
                regRep.itemAt(i).color = 'green'
            else
                regRep.itemAt(i).color = 'lightgreen'

            var height = 100*(Math.abs(digit)/maxSpec)
            regRep.itemAt(i).height = height
            regRep.itemAt(i).digit = digit
        }
    }
    Text{
        id: regText
        text:"Regularity : "
    }
    Repeater{
        id: regRep
        model: 0
        Rectangle{
            id: innerRect
            x: index*(pageFullReptendPrime.width/regRep.model) //the page must escape from here
            y: 30
            width: 30
            height: 100
            color: 'green'
            property int digit: -1
            Text{
                text: digit //ToolTip doesn't works but it looks even better
            }
        }
        anchors.fill: parent
    }
}
