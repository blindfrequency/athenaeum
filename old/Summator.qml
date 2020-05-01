import QtQuick 2.10
import QtQuick.Window 2.10

import QtQuick.Controls 2.2
import QtQuick.Controls 1.4 as Q1

import QtQuick.Controls.Styles 1.4

import IdeasLib 1.0


Item {

    anchors.fill: parent

    CopyClipboard{
        id:clipboard
    }

    Item
    {
        id: controllsItem

        y: 0
        width: parent.width
        height: 50

        TextEdit{

            x: 20
            y: 20
            width: 150+30

            id: importInput

            text: "{1/7,10,14,2,+,*};"
        }

        Button{
            y: 20

            text: "Import"
            x: 210
            width: 100

            onClicked: {
                seriesSummator.importFromString(importInput.text)
            }
        }


        ComboBox {
            y:20

            x: 340-50+30//sorry for stupid shifts (later here would be auto resizer, like one done for aim)
            width: 200

            /*
0188679245283 1/53
016949152542372881355932203389305084 .. unknown period 1/59
1/61 same
01492537313432835820895523880597 1\67
1/73 01369863
01265822784810126582278481 1/79
01123595505617977528089887640449438202247191 1\89
1\97 длинный период
101 фуфлыжка
103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199
127 007874015748031496062992125984251968503937
1\41 02439
1\43 023255813953488372093023255813953488372093
1\137 0072992
1\173 0057803468208092485549132947976878612716763
*/

            model:["{1/7,10,14,2,+,*};",
                "{2/7,10,28,2,+,*};",
                "{3/7,10,42,2,+,*};",
                "{4/7,10,56,2,+,*};",
                "{5/7,10,70,2,+,*};",
                "{6/7,10,84,2,+,*};",
                "{1/7,10,7,5,-,*,1}; inv",
                "{1/7,10,14,2,-,/,1}; inv v2",
                "{1/13,10,23,3,+,/,2,1,-}; ",
                "{1/13,10,23,3,-,*}; inv",
                "{1/17,10,47,8,-,*};",
                "{1/17,10,47,125,+,*}; (undone) but idea is ok",
                "{1/19,10,5,5,+,*};",
                "{1/19,10,1,2,-,*,1}; inv",
                "{1/19,10,5,5,-,/,1}; inv v2",
                "{1/23,10,4,8,+,*};",
                "{1/23,10,4,125,-,*}; (undone) but idea is ok",
                "{1/29,10,31,9,-,*};",
                "{1/29,10,31,9,+,/}; dont think it works",
                "{1/31,10,3,7,+,*};",
                "{1/31,10,3,7,-,/}; inv (if would work its mirracle)",
                "{1/47,10,17,8,-,*};",
                "{1/47,10,17,125,+,*}; (undone) but idea is ok",
                "{1/71,10,14,6,+,*,3};",
                "{1/73,10,13,5,+,*,2,1} wrong",
                "{1/83,10,12,4,+,*,3};",
                "{1/83,10,12,4,-,/,1}; not working",//hmm
                "{1/199,10,5,5,+,*,3};",
                "--OTHER SCALES---",
                "{1/7,2,14,2,+,*,2,5};",
                "{1/7,5,14,2,+,*};",
                "{1/7,12,14,2,+,*};",
                "{1/13,2,23,3,+,/,2,1,-};",
                "{1/13,2,23,3,+,/,2,1,-};"]

            onActivated:   {
                importInput.text = currentText
            }
        }


            TextEdit{

                x: 20
                y: 20
                width: 100

                id: numInput

                text: "1"
                visible: false
            }

            TextEdit {
                y: 20

                text: "7"

                id: primeInput

                x: 130
                width: 100
                visible: false
            }

            TextEdit {
                y: 20

                text: "10"

                id: scaleNotationInput

                x: 250
                width: 100
                visible: false
            }


            TextEdit {
                y: 20

                text: "14"

                id: seriesBase

                x: 360
                width: 100
                visible: false
            }

            TextEdit {
                y: 20

                text: "2"

                id: seriesMultiply

                x: 470
                width: 100
                visible: false
            }

            Button{
                y: 20

                text: "<"
                x: 580-50//sorry for stupid shifts
                width: 50

                onClicked: {
                    seriesSummator.movePosition(-1*parseInt(scrollFactor.text))
                }
            }

            TextEdit {
                y: 20

                text: "1"
                id: scrollFactor

                x: 690-50-50//sorry for stupid shifts
                width: 50
            }

            Button{
                y: 20

                text: ">"
                x: 800-100-50//sorry for stupid shifts
                width: 50
                onClicked: {
                      seriesSummator.movePosition(parseInt(scrollFactor.text))
                }
            }

            Button{
                y:20
                text: "Copy"
                x:760-50//sorry for stupid shifts
                width: 50
                onClicked: {
                    seriesSummator.grabToImage(function(result) {
                                             result.saveToFile("series.png");
                                          //  clipboard.copyImage("series.png")
                                            clipboard.copyImageSrc(result.image)
                                            console.log("Image saved to series.png - copy to clipboard")
                                         });
                }
            }

            Dialog{
                visible: false
                id: positionDialog
                contentItem: Rectangle {
                    color: "lightgreen"
                    implicitWidth: 400
                    implicitHeight: 100
                    TextEdit  {
                        id: posText
                        text: "100"
                        color: "navy"
                        anchors.centerIn: parent
                    }
                    Button
                    {
                        y:25
                        text: "Ok"
                        onClicked: {
                            seriesSummator.moveTo(parseInt(posText.text))
                            positionDialog.close()
                        }
                    }
                }
            }

            Button{
                y: 20
                text: "Go"
                x: 820-50//sorry for stupid shifts
                width: 45
                onClicked: {
                      //input N to move to exact position
                    positionDialog.visible = true
                }
            }

            /*
            Button {
                y: 20
                x: 825
                width: 25
                text: "N"
                onClicked: seriesSummator.setCellsToFill(100) //later set prompt please
            }*/

            CheckBox
            {
                y:20
                x: 910-40//sorry for stupid shifts

                text: "Hide zeros"

                onCheckStateChanged:
                {
                    seriesSummator.setSkipZeros(checked)
                }
            }


            MouseArea {

                x: 10
                y: 50

                width: parent.width - 10
                height: parent.height - 100

                //can make 3 different areas on each textEdit

                onWheel: {

                    var text
                    if (primeInput.focus)
                        text = primeInput.text
                    if (numInput.focus)
                        text = numInput.text
                    if (scaleNotationInput.focus)
                        text = scaleNotationInput.text

                    if (seriesBase.focus)
                        text = seriesBase.text
                    if (seriesMultiply.focus)
                        text = seriesMultiply.text

                    var a = parseInt(text)
                    var b =  wheel.angleDelta.y / 120 ;
                    a +=  b;

                    if (scaleNotationInput.focus)
                        scaleNotationInput.text = a.toString();
                    if (primeInput.focus)
                        primeInput.text = a.toString();
                    if (numInput.focus)
                        numInput.text = a.toString();

                    if (seriesBase.focus)
                        seriesBase.text = a.toString();
                    if (seriesMultiply.focus)
                        seriesMultiply.text = a.toString();
                }
    }
}



    SeriesSummator
    {
        id:seriesSummator

        y: controllsItem.height + 10
        x: 0
        width: parent.width
        height: 400

        Component.onCompleted:
        {
            seriesSummator.importFromString("{1/7,10,14,2,+,*};");
        }
    }

/*
    Rectangle
    {
        y: controllsItem.height + 20 + seriesSummator.height
        x: 0
        width: 50
        height: 50
        color: "green"
    }*/

}
