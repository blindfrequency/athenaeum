import QtQuick 2.10
import QtQuick.Window 2.10

import QtQuick.Controls 2.2
import QtQuick.Controls 1.4 as Q1

import QtQuick.Controls.Styles 1.4

import IdeasLib 1.0

Item {

    CopyClipboard{
        id:clipboard
    }

    id:  circleView
    visible: true

    anchors.fill: parent
    //title: qsTr("ideas")

    onWidthChanged: {
       // console.log("New width circle " + width)
        repeatersGrid.columns = (circleView.width / (parseInt(repeatorsRadius.text)*2 + 20))
      //  console.log("New colums " + repeatersGrid.columns)
    }

    CircleDigitDiagram
    {
        id: mainCircle
        //circle diagram

        anchors.horizontalCenter: parent.horizontalCenter

        x: 10
        y: addAllButton.height + addAllButton.y + 10

        width: mainCircleSlider.value
        height: mainCircleSlider.value //must be changable

        //Need to try to put in center

        Component.onCompleted: {
            mainCircle.addNum(1,7,10)
            mainCircle.addNum(1,13,10)
    
        }
    }


    Popup
    {
        x:(parent.width-width)/2
        y:(parent.height-height)/2

        id: exportPopup
        width: parent.width - parent.width/5
        height: parent.height - parent.height/2

        Text{
            x: 10
            y: 10
            text: "Export or import text below:"
        }

        Q1.TextArea {

            id: exportText
            font.pointSize: 20
            x: 10
            y: 40
            width: parent.width - 20
            height: parent.heght
            text: ""

            style: TextAreaStyle {
                       // backgroundColor : "yellow"
                    }

            function loadCircle()
            {
                var newText = mainCircle.exportToString()
                exportText.text = newText
            }
        }

        Button{
            text: "Import"
            x: parent.width - 110
            y: exportText.height + exportText.y + 20

            onPressed: {
                mainCircle.importFromString(exportText.text)
                exportPopup.close()
            }
        }

        Button{
            text: "Close"
            x: 10
            y: exportText.height + exportText.y + 20
            onPressed: {
                exportPopup.close()
            }
        }

    }

    Button{
        x: 10
        y: 10

        id: addAllButton

        ToolTip.text: "Ads every small circles to the big one"
        ToolTip.visible: hovered

        text: "Add all"
        onPressed: {
            var  prime = parseInt(primeInput.text);
            var base = parseInt(scaleNotationInput.text)

            for (var i = 0; i < circleRepeater.model; ++i)
              mainCircle.addNum(1+i,prime,base);

           exportText.loadCircle()
        }
    }

    Button{
        x: addAllButton.x + addAllButton.width + 10
        y: 10

        ToolTip.text: "Opens popup to export main circle"
        ToolTip.visible: hovered

        id: exportButton

        text: "Export"
        onPressed: {
            exportText.loadCircle()
            exportPopup.open() //should just configure the buttons export & import there
        }
    }

    Button{
        x: exportButton.x + exportButton.width + 10
        y: 10

        ToolTip.text: "Opens popup to import main circle"
        ToolTip.visible: hovered

        id: importButton

        text: "Import"
        onPressed: {
            exportText.text = "";
            exportPopup.open() //should just configure the buttons export & import there
        }
    }

    Button{
        x: importButton.x + importButton.width + 10
        y: 10

        ToolTip.text: "Cleans main circle"
        ToolTip.visible: hovered

        id: cleanButton

        text: "Clean"
        onPressed: {
            //should be a request
            mainCircle.clear()
        }
    }

    Button{
        x: cleanButton.x + cleanButton.width + 10
        y: 10

        ToolTip.text: "Copy main circle to clipboard"
        ToolTip.visible: hovered

        id: copyButton

        text: "Copy"
        onPressed: {

            mainCircle.grabToImage(function(result) {
                                     result.saveToFile("circle.png");
                                     clipboard.copyImageSrc(result.image)
                                        console.log("Image saved to circle.png and copied")
                                 });
        }
    }

   /* Button{
        x: copyButton.x + copyButton.width + 10
        y: 10

        id: changeSizeButton

        text: "Change Size"
    }*/

    Button{
        x: copyButton.x + copyButton.width + 10//changeSizeButton.x + changeSizeButton.width + 10
        y: 10
        id: helpButton

        text: "Help"

        ToolTip.text: "Shows some tips on import/export"
        ToolTip.visible: hovered

        onPressed: helpPopup.open()
    }

    Slider{

        x: helpButton.x + helpButton.width + 10
        y: 10

        ToolTip.text: "Changes the size of main circle"
        ToolTip.visible: hovered

        from: 20
        to: 600
        value:250

        id:mainCircleSlider

        onMoved: {
            mainCircle.setRadius(mainCircleSlider.value/2 - 10)
        }
    }

    Button{
        x: mainCircleSlider.x + mainCircleSlider.width + 10
        y: 10

        ToolTip.text: "Switches onn and off labels on main circle"
        ToolTip.visible: hovered

        text: "On/off labels"
        onPressed: mainCircle.changeLabelsStatus()
    }

    Popup
    {
        x:(parent.width-width)/2
        y:(parent.height-height)/2

        id: helpPopup
        width: parent.width - parent.width/5
        height: parent.height - parent.height/4

        Text{
            x: 10
            y: 10
            text: "Shortcuts to remeber how can we import numbers:\n
                  Please write all the circles from new line\n\n
                  {n/m,notationScale}; - simple division\n
                  {n/m(o),notationScale}; - division in pow o\n
                  {n*m(o),notationScale}; - multiply in pow o\n
                  {(digits with spaces),notationScale}; - just paint circle with digits\n
                  {>>2 2 1 2 2 2 1,13}; - fill with shifts\n
                  {Py[1+2+3+4.0/7.0]Py}; - fill with any Python code\n
                  \n Also each usual circle can have own radius, and color:\n
                  {(1 2 3),10,red,50}; {(4 5 6),10,blue,80}; - will paint 2 lines";
            //{NumReduction(142857),10}; - Numerological reduction\n Primes etc undone
        }

        Button {
            text: "Ok"
            y: helpPopup.height - 60
            x: helpPopup.width - 120
            onPressed: helpPopup.close()
        }
    }


   Item
   {
       id: multyCircles

       y: mainCircleSlider.value + 60
       width: parent.width
       height: parent.height - y


    TextEdit{

        x: 20
        y: 20
        width: 100

        id: numInput

        text: "1"
    }

    TextEdit {
        y: 20

        text: "7"

        id: primeInput

        x: 130
        width: 100
    }

    TextEdit {
        y: 20

        text: "10"

        id: scaleNotationInput

        x: 250
        width: 100
    }


    TextEdit {
        y: 20

        text: "6"

        id: repeatorsAmount

        x: 360
        width: 100

    }

    TextEdit {
        y: 20

        text: "100"

        id: repeatorsRadius

        x: 470
        width: 100

    }

    TextEdit {
        y: 20

        text: "1" //step between each of the circles

        id: repeatorStep

        x: 580
        width: 100
    }


    MouseArea {
        x: 10
        y: 50

        width: parent.width - 10
        height: parent.height - 100

        onWheel: {

            var text
            if (primeInput.focus)
                text = primeInput.text
            if (numInput.focus)
                text = numInput.text
            if (scaleNotationInput.focus)
                text = scaleNotationInput.text
            if (repeatorsAmount.focus)
                text = repeatorsAmount.text

            if (repeatorsRadius.focus)
                text = repeatorsRadius.text
            if (repeatorStep.focus)
                text = repeatorStep.text


            var a = parseInt(text)
            var b =  wheel.angleDelta.y / 120 ;
            a +=  b;

            if (scaleNotationInput.focus)
                scaleNotationInput.text = a.toString();
            if (primeInput.focus)
                primeInput.text = a.toString();
            if (repeatorsAmount.focus)
                repeatorsAmount.text = a.toString();
            if (numInput.focus)
                numInput.text = a.toString();
            if (repeatorsRadius.focus)
                repeatorsRadius.text = a.toString();
            if (repeatorStep.focus)
                repeatorStep.text = a.toString();


            circleRepeater.model = parseInt(repeatorsAmount.text)
            repeatersGrid.columns = (circleView.width / (parseInt(repeatorsRadius.text)*2 + 20))

            var  prime = parseInt(primeInput.text);
            var base = parseInt(scaleNotationInput.text)

            for (var i = 0; i < circleRepeater.model; ++i)
            {
                circleRepeater.itemAt(i).replaceNum(1+i*parseInt(repeatorStep.text),prime,base);
                circleRepeater.itemAt(i).setRadius(parseInt(repeatorsRadius.text))
            }

        }
    }

    Grid {
        id: repeatersGrid
            x: 10; y: 50
            rows: 10
            columns: (circleView.width / (parseInt(repeatorsRadius.text)*2 + 20))
            spacing: 10

            //ON RESIZE rows: (thatWindow.width / (260 + 10)) + 1;

    Repeater
    {
        id: circleRepeater
        model: 0

        CircleDigitDiagram
        {
            id: circle
            //circle diagram
            x: 10 + (parseInt(repeatorsRadius.text)*2+60)*index
            y: 10
            width: parseInt(repeatorsRadius.text)*2 + 10
            height: parseInt(repeatorsRadius.text)*2 + 10
            //color: "green"

            Component.onCompleted:
            {
                circle.setRadius(parseInt(repeatorsRadius.text))
            }
        }

        Component.onCompleted:
        {
            repeatersGrid.columns = (circleView.width / (parseInt(repeatorsRadius.text)*2 + 20))
            circleRepeater.model = 6

            //or just 4 for start and its ok
            ///console.log("Columns " + repeatersGrid.columns)

            var  prime = parseInt(primeInput.text);
            var base = parseInt(scaleNotationInput.text)

            for (var i = 0; i < circleRepeater.model; ++i)
            {
                circleRepeater.itemAt(i).replaceNum(1+i*parseInt(repeatorStep.text),prime,base);
                circleRepeater.itemAt(i).setRadius(parseInt(repeatorsRadius.text))
            }

        }
    }
    }
   }//end of item

}
