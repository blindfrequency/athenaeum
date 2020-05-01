import QtQuick 2.12
import QtQuick.Controls 2.2
import Athenum 1.0
import QtQml 2.12


Item {
    id: pageOctaves
    property string athName: "Octaves"
    property int requestedWidth: width
    property int requestedHeight: 500
    property string descriptionText: "Some fun idea about prime regularities between octaves of any integer."

    function calc(){
        abstractOctaves.calculate(1,128)
        octavesTable.model = abstractOctaves
    }

    AbstractOctaves{
        id: abstractOctaves
    }

    Component.onCompleted: {
        calc()
    }


    Rectangle{
    id: visualArea
    width: parent.width
    height: parent.height - 50
    y:50
    x:0
    border.color: 'green'
        TableView{
            id: octavesTable
            y: 50
            width: parent.width
            height: parent.height - y

            delegate:
                Rectangle{
                    Text {
                    width: 20
                    text: display //LATER: a) nice to color the P-1 periods, as they are special, same with 0 and 1
                    //great to find the law where position P-1 are primes, like 17 and 19
                }
                implicitWidth: 25
                implicitHeight: 25
                border.color: 'lightgray'
                MouseArea{
                    anchors.fill: parent
                    onClicked: {
                        if (column < 2)
                            return
                        if (row > 0)
                            return
                        subOctavePopUp.calc(column-1) //check it
                        subOctavePopUp.visible = true
                    }
                }
            }
        }
    }

    Popup{
        x:(parent.width-width)/2
        y:(parent.height-height)/2

        id: subOctavePopUp
        width: parent.width - parent.width/5
        height: 250
        visible: false

        function calc(startOct){
            var coef = 32
            if (startOct > 7)
                coef = 16
            if (startOct > 12)
                coef = 8
            if (startOct > 37)
                coef = 4

            subOctaves.calculate(startOct, startOct*coef)
            subOctavesTable.model = subOctaves
        }

        AbstractOctaves{
            id: subOctaves
        }

        TableView{
            id: subOctavesTable
            y: 50
            width: parent.width
            height: parent.height - y

            delegate:
                Rectangle{
                    Text {
                        width: 20
                        text: display //LATER: a) nice to color the P-1 periods, as they are special, same with 0 and 1
                        //great to find the law where position P-1 are primes, like 17 and 19
                    }
                    implicitWidth: 25
                    implicitHeight: 25
                    border.color: 'lightgray'
                }
            }
    }

}
