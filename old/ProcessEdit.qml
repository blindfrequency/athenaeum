import QtQuick 2.10
import QtQuick.Window 2.10
import QtQuick.Controls 2.2
import QtQuick.Dialogs 1.0

import Athenum 1.0

Item {
    id: processEditItem

    property int flickContentY: 0

    function insureVisibility(){
            processView.visible = processView.y > processEditItem.flickContentY
            countSlider.visible = countSlider.y > processEditItem.flickContentY
            elementType.visible = elementType.y > processEditItem.flickContentY
            lineSlider.visible = lineSlider.y > processEditItem.flickContentY
            loadButton.visible = loadButton.y > processEditItem.flickContentY
            saveButton.visible = saveButton.y > processEditItem.flickContentY
            mainCombo.visible = mainCombo.y > processEditItem.flickContentY
            elemName.visible = elemName.y > processEditItem.flickContentY
            elemDesk.visible = elemDesk.y > processEditItem.flickContentY
            colorRect.visible = colorRect.y > processEditItem.flickContentY
            editButton.visible = editButton.y > processEditItem.flickContentY
            autoEditCheck.visible = autoEditCheck.y > processEditItem.flickContentY
            cyclicFlag.visible = cyclicFlag.y > processEditItem.flickContentY
    }

        Process{
            id: processObject
            Component.onCompleted: {
                processObject.setElementsCount(7)
                processView.setContainedObject(processObject)
                mainCombo.model = processObject.getElementsCount()
            }
        }

        ProcessView {
            x: 10;  y: 10
            id: processView
            width: parent.width - 20 //ONLY FOR FINITE
            height: 80          //NEED TO KNOW FROM PROCESS ITS SHAPES
            backgroundColor: "#eeeeee"
            MouseArea{
                anchors.fill: parent
                onClicked: {
                    var index = processView.mouseHit(mouseX,mouseY)
                    if (index != -1)
                        mainCombo.currentIndex = index
                }
            }
        }


        Slider {
            from: 1
            value: 7
            to: 12 //later make longer when page is scrollable, but then we must update content
            onValueChanged: {
                processObject.setElementsCount(value)
                //processView.requestUpdate() //signal
            }

            x: parent.width - 300 - 10
            y: 100
            width: 100
            id: countSlider
        }
        ComboBox {
            id: elementType
            model: ["empty","normal","blocked"]
            x: parent.width - 300 - 10
            y: 150
            width: 100
            currentIndex: 1

            onCurrentIndexChanged: {
                if (autoEditCheck.checked){
                    processObject.setElementType(mainCombo.currentIndex, elementType.currentIndex)
                    //processView.requestUpdate() //Need make auto signaling them
                }
            }
        }
        Slider {
            from: 15
            value: 100
            to: 200 //later make longer when page is scrollable
            onValueChanged: {
                processView.lineSize = value
                //processView.requestUpdate()
            }

            x: parent.width - 500 - 10
            y: 100
            width: 200
            id:lineSlider
        }

        Button{
            x: parent.width - 500 - 10
            y: 200
            width: 100
            text: "Save"
            onClicked: {
                processObject.saveToFile("filename")
            }
            id:saveButton
        }
        Button{
            x: parent.width - 400 - 10
            y: 200
            width: 100
            text: "Load"
            onClicked: {
                processObject.loadFromFile("filename")
                //processView.requestUpdate()
            }
            id:loadButton
        }


        ComboBox {
            id: mainCombo
            x: parent.width - width - 10
            y: 100
            width: 200
            onCurrentIndexChanged: {
                colorRect.color = processObject.getElementColor(currentIndex)
                elemName.text = processObject.getElementName(currentIndex)
                elemDesk.text = processObject.getElementDescription(currentIndex)
                elementType.currentIndex = processObject.getElementType(currentIndex)
            }
        }
        TextField {
            id: elemName
            x: parent.width - width - 10
            y: 150
            width: 200
            onEditingFinished: {
                if (autoEditCheck.checked){
                    processObject.setElementName(mainCombo.currentIndex,elemName.text)
                    //processView.requestUpdate() //Need make auto signaling them
                }
            }
        }
        TextField {
            id: elemDesk
            x: parent.width - width - 10
            y: 200
            width: 200
            onEditingFinished: {
                if (autoEditCheck.checked){
                    processObject.setElementDescription(mainCombo.currentIndex,elemDesk.text)
                    //processView.requestUpdate() //Need make auto signaling them
                }
            }
        }

        Rectangle{
            id: colorRect
            x: parent.width - 200 - 10
            y: 250
            width: 50
            height: 50
            color:"green"
            MouseArea{
                anchors.fill: parent
                onClicked: {
                   colorDialog.visible = true
                }
            }
            ColorDialog {
                id: colorDialog
                title: "Chose new color"
                onAccepted: {
                    colorRect.color = colorDialog.color
                    if (autoEditCheck.checked){
                        processObject.setElementColor(mainCombo.currentIndex,colorRect.color)
                        //processView.requestUpdate() //Need make auto signaling them
                    }

                }
                visible: false
            }
        }
        Button{
            x: parent.width - 100 - 10
            y: 250
            width: 100
            text: "Edit"
            onClicked: {
                processObject.setElementColor(mainCombo.currentIndex,colorRect.color)
                processObject.setElementName(mainCombo.currentIndex,elemName.text)
                processObject.setElementDescription(mainCombo.currentIndex,elemDesk.text)
                processObject.setElementType(mainCombo.currentIndex, elementType.currentIndex)
                //processView.requestUpdate() //Need make auto signaling them
            }
            id: editButton
        }
        CheckBox{
            id: cyclicFlag
            x: parent.width - width - 10
            y: 300
            width: 200
            text: "Cyclic"

            onCheckedChanged: {
                processObject.setCyclic(checked)
                if (checked){
                    processView.width = parent.width - 520
                    processView.height = parent.height - 20
                }else{
                    processView.width = parent.width - 20
                    processView.height = 80
                }

                //processView.requestUpdate()
            }
        }
        CheckBox{
            id: autoEditCheck
            x: parent.width - 100 - 10
            y: 300
            width: 100
            text: "Auto"
            checked: true
        }
}
