import QtQuick 2.10
import QtQuick.Controls 2.2

import QtQuick 2.0
import Athenum 1.0

//import IdeasLib 1.0 //no need
import QtQml 2.12
Item {
    id: animationRecorderItem

    //CopyClipboard{
    //    id:recorderClipboard
    //}

    OSforQML{
        id: osAccess //MARK AS EXPERIMENTS AND DON"T LET TO PUBLISH SEPPARATE
    }

    property int animationCounter: 0
    property int framesLimit: 1000
    property var qmlObject : undefined

    Rectangle
    {
        anchors.fill: parent
        border.color: "darkGreen"

        //clean pictures temp button too in AnimationRecorder
        Button{
            y: 45
            text: "Create video"
            onClicked: { //10 or 25
                osAccess.execute('ffmpeg -r 10 -f image2 -s 300x300 -i %d.png -vcodec libx264 -crf 10 -pix_fmt yuv420p a.mp4')
            }
        }

        Button{
            id: startButton
            text: "Start"
            onClicked: {
                if (startButton.text === "Start"){
                    animationRecorderItem.animationCounter = 0
                    animationTimer.running = true
                    startButton.text = "Stop"
                }else{
                    animationTimer.running = false
                    startButton.text = "Start"
                }
            }
        }

        Button{
            y: 90
            text: "Clear frames"
            onClicked: {
                //also please note that itworks only on linux, should use related path
                osAccess.cleanDir('/home/constcut/dev/projects/athenum/temp/render','*.png') //THIS IS WRONG: ATTENTION - MAKE PATH CUTTER IN JavaScript utils
            }
        }

        Timer {
            id: animationTimer
            interval: 40
               running: false; repeat: true
                       onTriggered:{
                            if (animationRecorderItem.animationCounter < animationRecorderItem.framesLimit){
                                qmlObject.grabToImage(function(result) {
                                    var filename = "render/" + animationRecorderItem.animationCounter + ".png"; //or png
                                                         animationRecorderItem.animationCounter++
                                                         result.saveToFile(filename); });
                            }
                            else{
                                animationTimer.running = false
                                console.log("Done " + animationRecorderItem.framesLimit + " shots!")
                           }
                       }
        }

    }
}
