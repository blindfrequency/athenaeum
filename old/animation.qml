import QtQuick 2.10
import QtQuick.Window 2.10
import QtQuick.Controls 2.2
import Athenum 1.0
//import IdeasLib 1.0
import QtQml 2.12

import '../components'

Item {
    id: animationExample

    property string athName: "Animation example"

    property int requestedWidth: width
    property int requestedHeight: 500

    AnimationRecorder{
        y: 10
        x: 10
        width: 100
        height: 120
        framesLimit: 2000

        id:animationRecorder
        Component.onCompleted: {
            animationRecorder.qmlObject = mainObject
        }
    }

    Component.onCompleted: {
        rect1.updateColor()
        rect2.updateColor()
    }

    width: 1000 //anchors
    height: 600

    PolyRythm {
        id: mainObject

        anchors.centerIn: parent
        width: 300; height: 300
        color: "green"
    }

    Button{
        x: parent.width - width - 20
        y: 10
        text: "Stop/Start"
        width: 100
        onClicked: {
            if (mainObject.isRunning())
                mainObject.stop()
            else{
                //.animationCounter = 0
                mainObject.start()
            }
        }
    }
    Slider{
        x: parent.width - width - 20 - 100
        y: 10

        from: 10
        value: 50
        to: 500

        width: 200

        onValueChanged: {
            mainObject.setInterval(value)
        }
    }

    ComboBox{
        x: parent.width - width - 20
        y: 90
        width: 300
    }
    Slider{
        x: parent.width - width - 20
        y: 130
        width: 300
        from: 1
        value: 6
        to: 96
    }
    CheckBox{
        x: parent.width - width - 20 - 150
        y: 170
        width: 150
        text: "Clockwise"
    }
    CheckBox{
        x: parent.width - width - 20
        y: 170
        width: 150
        text: "Center line"
    }
    Slider{
        x: parent.width - width - 20-200
        y: 210
        width: 100
        from: 0
        value: 1
        to: 255
    }
    Slider{
        x: parent.width - width - 20-100
        y: 210
        width: 100
        from: 0
        value: 1
        to: 255
    }
    Slider{
        x: parent.width - width - 20
        y: 210
        width: 100
        from: 0
        value: 1
        to: 255
    }

    Slider{
        x: parent.width - width - 20-200
        y: 250
        width: 100
        from: 0
        value: 1
        to: 255
    }
    Slider{
        x: parent.width - width - 20-100
        y: 250
        width: 100
        from: 0
        value: 1
        to: 255
    }
    Slider{
        x: parent.width - width - 20
        y: 250
        width: 100
        from: 0
        value: 1
        to: 255
    }

    Rectangle{
        id: rect1
        x: parent.width - 300
        y: 290

        width: 20
        height: 20

        border.color: "black"
        function updateColor(){
           rect1.color = Qt.rgba(redBG1.value/255.0,blueBG1.value/255.0,greenBG1.value/255.0)}
    }

    Rectangle{
        id: rect2
        x: parent.width - 150
        y: 290

        width: 20
        height: 20

        border.color: "black"
        function updateColor(){
           rect2.color = Qt.rgba(redBG2.value/255.0,blueBG2.value/255.0,greenBG2.value/255.0)}
    }

    Slider{
        id: redBG1
        x: parent.width - width - 20-200
        y: 310
        width: 100
        from: 0
        value: 0
        to: 255
        onValueChanged: rect1.updateColor()
    }
    Slider{
        id: greenBG1
        x: parent.width - width - 20-100
        y: 310
        width: 100
        from: 0
        value: 0
        to: 255
        onValueChanged: rect1.updateColor()
    }
    Slider{
        id: blueBG1
        x: parent.width - width - 20
        y: 310
        width: 100
        from: 0
        value: 0
        to: 255
        onValueChanged: rect1.updateColor()
    }

    Slider{
        id: redBG2
        x: parent.width - width - 20-200
        y: 350
        width: 100
        from: 0
        value: 0
        to: 255
        onValueChanged: rect2.updateColor()
    }
    Slider{
        id: greenBG2
        x: parent.width - width - 20-100
        y: 350
        width: 100
        from: 0
        value: 0
        to: 255
        onValueChanged: rect2.updateColor()
    }
    Slider{
        id: blueBG2
        x: parent.width - width - 20
        y: 350
        width: 100
        from: 0
        value: 0
        to: 255
        onValueChanged: rect2.updateColor()
    }

}
