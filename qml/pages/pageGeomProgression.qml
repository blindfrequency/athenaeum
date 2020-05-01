import QtQuick 2.12
import QtQuick.Controls 2.2
import Athenum 1.0
import QtQml 2.12

import '../components'

Item {
    id: pageGeometricProgression

    property string athName: "Geometric progression"
    property int requestedWidth: width
    property int requestedHeight: 500

    Component.onCompleted: {
        //abstractFormula1.sum('first','{rise^{n}}','{fall^{n+1}}', '{N}', '{D}')
    }


    WikiLink{
        x: parent.width - width*2
        link: 'https://en.wikipedia.org/wiki/Geometric_progression'
        pageName: 'Geometric progression'
    }
    Text{
        y:80
        id: curElText
    }

    TextField{
        placeholderText: "first step"
        width: 100
        x: 0
        y: 5
        text: '14'
        id: firstStep
        onEditingFinished: {
             pageGeometricProgression.updateState()
        }
    }
    TextField{
        placeholderText: "rise coef"
        width: 125
        x: 110
        y: 5
        text: '2'
        id: rise
        onEditingFinished: {
             pageGeometricProgression.updateState()
        }
    }
    TextField{
        placeholderText: "fall coef"
        width: 125
        x: 245
        y: 5
        text: '100'
        id: fall
        onEditingFinished: {
             pageGeometricProgression.updateState()
        }
    }
    Text{
        id: state
        x: 380
    }
    Rational{
        id: rNumber
    }
    GeometricProgression{
        id: gProgress
    }

    Slider{
        id: elements
        y: 40
        from: 1
        to: 40
        value: 10
        stepSize: 1
        ToolTip {
            parent: elements.handle
            visible: elements.hovered
            text: 'Elements amount: ' + elements.value
        }

        onValueChanged: {
             pageGeometricProgression.updateState()
        }
    }

    function updateState(){
        if (parseInt(fall.text) > parseInt(rise.text)){
            console.log("Setting g progression")
            gProgress.set(firstStep.text,rise.text,fall.text)
            var sum = gProgress.rSumQML()
            console.log(sum,'obtained params')
            currentFormula.sum(firstStep.text,rise.text,fall.text,'{'+sum[0]+'}','{'+sum[1]+'}')
            state.text = 'The series converges: ' + sum[3] + ' at ' + sum[2]
            var cEl = gProgress.rElementQML(elements.value)
            curElText.text = cEl[3] + ' = \n' + cEl[0] + "/" + cEl[1] + "  at [" + cEl[2] + "]"
        }
        else{
            state.text = 'The series summ is infinite.'
        }
    }

    Button{
        y: 120
        text: "Calculate elements"
        onClicked: {
            fRepeater.model = 50
            for (var i = 0; i < 50; ++i){
                fRepeater.itemAt(i).opacity = 0
                fRepeater.itemAt(i).clear()
            }
            gProgress.set(firstStep.text,rise.text,fall.text)
            timer2.count = 0
            timer2.start()
        }
    }

    Timer{
        id:timer2
        interval: 100
        property int count: 0
        repeat: true
        running: false
        onTriggered: {
            var currentCount = count
            count = currentCount +1
            if (count > elements.value) timer2.repeat = false;
            var cEl = gProgress.reducedElementQML(currentCount) //and + one
            var str = '$$\\frac{'+cEl[0]+'}{'+cEl[1]+'}$$'
            fRepeater.itemAt(currentCount).raw(str)
            fRepeater.itemAt(currentCount).appear()
        }
    }



    Button{
        y: 220
        text:"Octave f()"
        onClicked: {
            fRepeater.model = 50
            for (var i = 0; i < 50; ++i){
                fRepeater.itemAt(i).opacity = 0
                fRepeater.itemAt(i).clear()
            }
            timer.count = 0
            timer.start()
        }
    }



    Timer{
        id:timer
        interval: 100
        property int count: 0
        repeat: true
        running: false
        onTriggered: {
            var currentCount = count
            count = currentCount +1
            if (count > 49) timer.repeat = false;
            gProgress.set(currentCount+1,rise.text,fall.text)
            var sum = gProgress.rSumQML()
            fRepeater.itemAt(currentCount).sum(currentCount+1,'{'+rise.text+'}^{n}','{'+fall.text+'}^{n+1}','{'+sum[0]+'}','{'+sum[1]+'}')
            fRepeater.itemAt(currentCount).appear()
        }
    }

    Button{
        y: 530
        text: "picture"
        property int count: 0
        onPressed: {
            var fname = "formuls" + count + ".png"
            formulasHome.grabToImage(function(result) {
                                     result.saveToFile(fname);
                                     //clipboard.copyImageSrc(result.image)
                                     console.log("Image saved to ",fname)
                                 });
        }
    }


}
