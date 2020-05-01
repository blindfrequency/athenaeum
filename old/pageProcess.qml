import QtQuick 2.10
import QtQuick.Window 2.10
import QtQuick.Controls 2.2
import Athenum 1.0

import '../components'

Item {
    id: pageProcess
    anchors.fill: parent

    property string athName: "Process"
    property string descriptionText: "Some dream, to prove truth and lie"
    property int requestedHeight: 800

    property int flickContentY: 0

    function insureVisibility(){
        upperText.visible = upperText.y > pageProcess.flickContentY
        processView.visible = processView.y > pageProcess.flickContentY
        //inner one
        var diff = pageProcess.flickContentY-processEdit.y
        //if (diff < 0) diff = 0
        processEdit.flickContentY = diff
        processEdit.insureVisibility()
    }

    Text{
        id: upperText
        x:10
        y:20
        text: "Ниже представленна модель простого конечного процесса..."
    }
    ProcessView {

        x: 10;  y: 70
        id:processView
        width: 500; height: 80
        //backgroundColor: "gray"
    }
    Process{

        id: processObject
        Component.onCompleted: {
            //console.log("Process object created. Resizing.")
            processObject.setElementsCount(5)

            processObject.setElementName(0,"First name")
            processObject.setElementName(1,"Second name")
            processObject.setElementName(2,"Third name")
            processObject.setElementName(3,"KA")
            processObject.setElementName(4,"bulkabulka")

            processView.setContainedObject(processObject)
        }
    }
    ProcessEdit{

        id: processEdit
        visible: y+width > pageProcess.flickContentY

        y: 150
        x: 10
        width: 990
        height: 400
    }
}
