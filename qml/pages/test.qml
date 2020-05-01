import QtQuick 2.10
import QtQuick.Window 2.10
import QtQuick.Controls 2.2
import Athenum 1.0
//import IdeasLib 1.0
import '../components'


Item {
    id: pageNumber

    property string athName: "Циферки"
    property int requestedWidth: width
    property int requestedHeight: 800

    Text {
        id: numberText
        text: "10"
    }
}
