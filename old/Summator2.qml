import QtQuick 2.10
import QtQuick.Controls 2.2
import Athenum 1.0
import IdeasLib 1.0
import QtQml 2.12

Item {
    id: serSummator

    property string athName: "Py ser Summator"

    property int requestedWidth: width
    property int requestedHeight: 500

    TextField{
        placeholderText: "N"
        width: 100
        x: 0
    }
    Text{
        x:102
        text:"/"
    }
    TextField{
        placeholderText: "M"
        width: 100
        x: 110
    }


    Button{
        text: "calc"
        x: 250
    }

    TextField{
        placeholderText: "start"
        width: 100
        onEditingFinished: {
        }
        x: 400
    }
    TextField{
        id: secondParam
        placeholderText: "rise"
        width: 100
        onEditingFinished: {
        }
        x: 500
    }
    TextField{
        id: thirdParam
        placeholderText: "fall"
        width: 100
        onEditingFinished: {
        }
        x: 600
    }

    TextField{
        placeholderText: "base"
        width: 100
        onEditingFinished: {
        }
        x: 700
    }

    CheckBox{
        text:"ABfall"
        x: 800
        onCheckedChanged: {
            if (checked){
                secondParam.placeholderText = "a fall"
                thirdParam.placeholderText = "b fall"
            }else{
                secondParam.placeholderText = "rise"
                thirdParam.placeholderText = "fall"
            }
        }
    }
    CheckBox {
        text: "Skip '0'"
        x: 900
    }
}
