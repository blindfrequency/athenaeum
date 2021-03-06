import QtQuick 2.13
import QtQuick.Controls 2.2
import Athenum 1.0
//import IdeasLib 1.0
import QtQml 2.13

//import IdeasLib 1.0//clipboard replace on refact for sure

Item {
    id: primeScalesItem //RENAME IT HERE
    property string athName: "PrimeScales"

    property int elementSize: 70
    property int primeLow: 2
    property int primeHigh: 62
    property int cells: 1000
    property string viewMode: "P-1"

    signal requestToOpenPage(var pageName)

    //property int selectedCell: 0 //Some way to locate through it

    PrimeScales{
        id: primeScales
    }
    Rational{
        id:rational
    }
    Component.onCompleted: {
        calc()
    }
    function calc(){
        primeScales.calculate(primeScalesItem.primeLow, primeScalesItem.primeHigh, primeScalesItem.cells)
        scalesTable.model = primeScales
    }
    Rectangle {
    id: visualArea
    width: parent.width
    height: parent.height - 50
    y:0
    x:0
    border.color: 'green'
        TableView{
            id: scalesTable
            y: 50
            width: parent.width
            height: parent.height - y

            //columnWidthProvider: autoSumItem.elementSize
            //columnHeightProvider: autoSumItem.elementSize

            delegate:Component{

                //property int row : styleData.row
                //property int column: styleData.column
                //id: delegComp

                Rectangle{
                id: globalDelegate
                color:   {
                            var color = "white"
                            if (viewMode === "All") {
                                var color = display[1] === 1 ?
                                "lightGreen"
                                : display[1] === 2 ?
                                "lightBlue"
                                : display[1] === 3 ?
                                "#FFFF77"
                                : "white"     
                            }
                            if (viewMode === "P-1") {
                                if (display[1]  === 1)
                                    color = "lightGreen"
                            }
                            if (viewMode === "(P-1)/2") {
                                if (display[1] === 2) 
                                    color = "lightBlue"   
                            }
                            if (viewMode === "(P-1)/3"){
                                if (display[1] === 3) 
                                    color = "#FFFF77"    
                            }

                            return color
                        }  
                    Text {
                    visible: primeScalesItem.elementSize > 20
                    width: 20
                    text: display[0] !== undefined ? display[0] : ""

                    //LATER: a) nice to color the P-1 periods, as they are special, same with 0 and 1
                    //great to find the law where position P-1 are primes, like 17 and 19
                }

                Button {
                    visible: primeScalesItem.elementSize > 120 // && display[1] === 1
                    text: "Open popup"
                    y: subText.height
                    anchors.horizontalCenter: parent.horizontalCenter
                    height: 20

                }
                Button{
                    visible: primeScalesItem.elementSize > 120
                    text: "Full reptend page"
                    y: subText.height + 33
                    anchors.horizontalCenter: parent.horizontalCenter
                    height: 20
                }
                Button{
                    visible: primeScalesItem.elementSize > 120
                    text: "Cyclic prime page"
                    y: subText.height + 72
                    anchors.horizontalCenter: parent.horizontalCenter
                    height: 20
                }

                Text{
                    id: subText
                    text:
                        display[1] === 1 ?
                            "P-1"
                          : display[1] === 2 ?
                            "P-2"
                          : ""
                    y: parent.height - height
                    visible: primeScalesItem.elementSize > 70
                }

                border.color: 'lightgray'
                //width: autoSumItem.elementSize
                //height: autoSumItem.elementSize
                implicitHeight: primeScalesItem.elementSize
                implicitWidth: primeScalesItem.elementSize

                MouseArea{
                    anchors.fill: parent
                    onClicked: {
                        if (column < 2)
                            return
                        //console.log('We pressed on cell',row,column)
                        var primeNumber = primeScales.getPrime(row-2)
                        rational.calc(1,primeNumber,column)
                        popupText.text =  'Rational: ' + rational.getFullString()
                        rationalPopup.visible = true

                        rationalCircle.stopAnimation()
                        var digits = rational.digits('fract', 0)
                        if (column < primeNumber)
                            rationalCircle.set(digits, column, true, false)
                        else
                            rationalCircle.set(digits, column, true, true)//always oro, always cycle
                        rationalCircle.startAnimation()
                    }
                }
            }
            }
        }
    }

    Popup {
        x:(parent.width-width)/2
        y:(parent.height-height)/2

        id: rationalPopup
        width: parent.width - parent.width/5
        height: 300
        visible: false

        Text{
            id: popupText
            x: 10
            y: 10
            text: "Rational number: "
        }
        DigitalCircle{
            y: 10 + popupText.height
            anchors.horizontalCenter: parent.horizontalCenter
            id: rationalCircle
            width: 240
            height: 240
        }

        Menu{
            id: popupMenu
            MenuItem {
                 text: "Open full reptend prime page"
                 onTriggered: {

                     //TODO fill real prime number, fill real numeric system
                      primeScalesItem.parent.parent.parent.parent.parent.parent.requestToOpenUrl("/pages/pageFullReptendPrime.qml",
                                                                                                 "{\"prime\":7,\"numericSystem\":10}");
                 }
            }
            MenuItem {
                 text: "Open circles preset"
                 onTriggered: {
                     //TODO need to make autosearch of prime parent by not undefined special field
                     primeScalesItem.parent.parent.parent.parent.parent.parent.requestToOpenUrl("/pages/test2.qml")
                 }
            }
        }

        Button {
            x: parent.width - width - 5
            text: ":"
            onPressed: {
                popupMenu.popup()
            }
        }
    }
}
