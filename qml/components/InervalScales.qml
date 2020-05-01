import QtQuick 2.14
import QtQuick.Controls 2.2
import Athenum 1.0
//import IdeasLib 1.0
import QtQml 2.12

Item {
    id: autoSumItem

    property string athName: "IntervalsScales"
    property int prime: 7

    Component.onCompleted:{
        intModel.setTableWidth(100)
        intModel.calc()
        //TODO new class for all 4 scales (interval, scales, sequence, group)
        intervalsTable1.model = intModel
        intervalsTable2.model = intModel
        intervalsTable3.model = intModel
        intervalsTable4.model = intModel
    }

    IntervalScalesModel{
        id: intModel
    }


    Rectangle{
    id: visualArea1
    width: parent.width
    height: 30
    y: 50
    x:0
    TableView{
        id: intervalsTable1
        onContentXChanged:  {
            //intervalsTable1.contentX = contentX
            intervalsTable2.contentX = contentX
            intervalsTable3.contentX = contentX
            intervalsTable4.contentX = contentX
        }
        y: 0
        width: parent.width
        height: parent.height - y
        property var rowWidths: [50, 30, 50, 100, 30]
        columnWidthProvider: function (column) { return rowWidths[column] }
        delegate:
            Rectangle{
                Text {
                width: 10
                text: display[1]
            }
            implicitHeight: 15
            implicitWidth: 30
            border.color: 'lightgray'
        }
    }
   }
    //todo REFACT WITH REPEATER
    Rectangle{
    id: visualArea2
    width: parent.width
    height: 30
    y: visualArea1.y + visualArea1.height
    x:0
    TableView{
        onContentXChanged:  {
            intervalsTable1.contentX = contentX
            //intervalsTable2.contentX = contentX
            intervalsTable3.contentX = contentX
            intervalsTable4.contentX = contentX
        }
        id: intervalsTable2
        y: 0
        width: parent.width
        height: parent.height - y
        property var rowWidths: [100, 50, 30, 50, 30]
        columnWidthProvider: function (column) { return rowWidths[column] }
        delegate:
            Rectangle{
                Text {
                width: 10
                text: display[1]
            }
            implicitHeight: 15
            implicitWidth: 30
            border.color: 'lightgray'
        }
    }
   }

    Rectangle{
    id: visualArea3
    width: parent.width
    height: 30
    y: visualArea2.y + visualArea2.height
    x:0
    TableView{
        onContentXChanged:  {
            intervalsTable1.contentX = contentX
            intervalsTable2.contentX = contentX
            //intervalsTable3.contentX = contentX
            intervalsTable4.contentX = contentX
        }
        id: intervalsTable3
        y: 0
        width: parent.width
        height: parent.height - y
        property var rowWidths: [200, 50, 30, 50, 30]
        columnWidthProvider: function (column) { return rowWidths[column] }
        delegate:
            Rectangle{
                Text {
                width: 10
                text: display[1]
            }
            implicitHeight: 15
            implicitWidth: 30
            border.color: 'lightgray'
        }
    }
   }

    Rectangle{
    id: visualArea4
    width: parent.width
    height: 30
    y: visualArea3.y + visualArea3.height
    x:0
    TableView{
        onContentXChanged:  {
            intervalsTable1.contentX = contentX
            intervalsTable2.contentX = contentX
            intervalsTable3.contentX = contentX
            //intervalsTable4.contentX = contentX
        }
        id: intervalsTable4
        y: 0
        width: parent.width
        height: parent.height - y
        property var rowWidths: [500, 30, 50, 30, 100, 60]
        columnWidthProvider: function (column) { return rowWidths[column] }
        delegate:
            Rectangle{
                Text {
                width: 10
                text: display[1]
            }
            implicitHeight: 15
            implicitWidth: 30
            border.color: 'lightgray'
        }
    }
   }

}
