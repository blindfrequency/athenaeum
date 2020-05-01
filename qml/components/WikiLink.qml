import QtQuick 2.12
import Athenum 1.0
import QtQuick.Controls 2.5

Rectangle {
    id: wikiItem
    Image{
        id: wikiImage
        width: 30
        height: 30
        source:'file:///home/constcut/dev/athenum/img/' + wikiItem.type + '.png'
        ToolTip {
            visible: mouseArea.containsMouse
            text: pageName + ' ' + link
        }
    }
    width: 30
    height: 30
    Component.onCompleted: {
        //console.log('IMAGE ',wikiImage.source)
    }
    property string pageName: 'name'
    property string link: 'localhost'
    property string type: 'wiki'

    MouseArea{
        id: mouseArea
        anchors.fill: parent
        hoverEnabled: true
        onDoubleClicked: {
            Qt.openUrlExternally(link) //wouldn' and shouldn't work in webgl
        }
    }
    border.color: 'lightgreen'
}



