import QtQuick 2.10
import QtQuick.Window 2.10
import QtQuick.Controls 2.2
import Athenum 1.0

Item {
    id: pageProcess

    property string athenumPageName: "Noughts and crosses"

    property int requestedWidth: width
    property int requestedHeight: 500

    width: 1000 //anchors
    height: 600

    Rectangle{
        x: 10
        y: krestNol.y
        width: 100
        height: 40
        color: "lightGreen"
        Text{
            id:infoText
            text: "Game began"
        }
        id: rect
    }

    AnimationRecorder{
        y: 40 + rect.y
        x: 10
        width: 100
        height: 120
        framesLimit: 1000

        id:animationRecorder
        Component.onCompleted: {
            animationRecorder.qmlObject = krestNol
        }
    }

    NoughtsCrosses {
        id: krestNol

        property int playerNumber: 1

        function switchNextPlayer(){
            if (krestNol.playerNumber == 1){
                playerNumber = 2
            }else if (krestNol.playerNumber == 2){
                playerNumber = 1
            }
        }

        anchors.centerIn: parent
        width: 300; height: 300
        color: "green"
        MouseArea{
            anchors.fill: parent
            onClicked: {
                var cellIndex = krestNol.mouseHit(mouseX,mouseY)

                var preWinner = krestNol.checkWin()

                if (preWinner === 0)
                if (krestNol.setValue(cellIndex,krestNol.playerNumber))
                    krestNol.switchNextPlayer()

                var winner = krestNol.checkWin()
                if (winner !== 0) {
                    infoText.text = "Player " + winner +" won"
                }
                    krestNol.requestUpdate()
            }
        }
    }

    Button{
        x: parent.width - width - 20
        y: 100
        text: "Reset"
        onClicked: {
            krestNol.reset()
            krestNol.requestUpdate()
            infoText.text = ""
        }
    }
}
