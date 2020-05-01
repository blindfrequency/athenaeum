import QtQuick 2.12
import QtQuick.Controls 2.2
import Athenum 1.0
import QtQml 2.12

Item {
    id: autoSumItem

    property string athName: "AutoSum"
    property int prime: 7

    Component.onCompleted:{
        nom.text = '1'
        den.text = prime.toString()
        calcButton.calc()
    }

    TextField{
        placeholderText: "num"
        width: 100
        x: 0
        y: 5
        text: '1'
        id: nom
    }
    Text{
        x:102
        text:"/"
        y: 5
    }
    TextField{
        placeholderText: "den"
        width: 125
        x: 110
        y: 5
        text: '7'
        id: den
    }
    Button{
     y: 5
     x: 240
     text: 'calc'
     id: calcButton

     function calc(){
         sumModel.calculate(nom.text,den.text,base.value,geoNumber.value,geoElements.value)
         sumModel.setTableWidth(1000)

         var f = sumModel.firstStep()
         var m = sumModel.multiply()
         var d = sumModel.decrease()

         sumTable.model = sumModel
     }

     onPressed: calcButton.calc()
    }

    Slider{
        x: 350
        from: 2
        to: 62
        value: 10
        id: base
        y: 5
        stepSize: 1

        onValueChanged: {
            //use there value but 10, but yet we not ready :(
            //sumModel.calculate(nom.text,den.text,10,geoNumber.value)
        }

        ToolTip {
            parent: base.handle
            visible: base.hovered
            text: 'Base: ' + base.value
        }
    }

    Slider{
        x: 550
        from: 0
        value: 0
        to: 49 //later expend
        id: geoNumber
        y: 5
        stepSize: 1
        onValueChanged: {
            //use there value but 10, but yet we not ready :(
           // console.log("GEO number change",value)
           // sumModel.calculate(nom.text,den.text,10,geoNumber.value)
        }
        ToolTip {
            parent: geoNumber.handle
            visible: geoNumber.hovered
            text: 'Progression: ' + geoNumber.value
        }
    }

    Slider{
        x: 750
        from: 1
        value: 50 //check its ok not to make slow
        to: 500
        id: geoElements
        y: 5
        stepSize: 1

        ToolTip {
            parent: geoElements.handle
            visible: geoElements.hovered
            text: 'Members: ' + geoElements.value
        }
    }

    CheckBox{
        text: '0'
        x: 950
        id: displayZeros
        onCheckStateChanged: {
            //USE IT IN MODEL
            sumModel.switchZeroes()
        }
        ToolTip {
            parent: displayZeros.handle
            visible: displayZeros.hovered
            text: 'Display zeroes'
        }
    }


    Button{
        x: 1250
        text: "copy"
        onClicked: {
            visualArea.grabToImage(function(result) {
                                     result.saveToFile("autosum.png");
                                     copyClipboard.copyImageSrc(result.image)
                                      console.log("Image saved to autosum.png and copied")
                                 });
        }
    }


    Button{
        x: 1050
        text: "go"
        onClicked: timer.running = !timer.running
    }
    Timer{
        id: timer
        running: false
        repeat: true

        property int counter: 0
        interval: 250
        onTriggered: {
            geoNumber.value += 1
            geoNumber.value = geoNumber.value % 7
            calcButton.calc()
            //console.log("Triggered timer ")
        }
    }


    SumModel{
        id: sumModel
    }


   Rectangle{
   id: visualArea
   width: parent.width
   height: parent.height - 50

   y:50
   x:0

    TableView{
        id: sumTable
        y: 50

        width: parent.width
        height: parent.height - y

        delegate:
            Rectangle{
                Text {
                width: 10
                text: display
            }

            implicitWidth: 15
            implicitHeight: 15
            border.color: 'lightgray'
        }
    }
    }
}
