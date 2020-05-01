import QtQuick 2.0
import IdeasLib 1.0
import QtQuick.Controls 2.2

Item {

    id: octavizerItem
    property int octInited : 0

    TextEdit{
        y: 10; x:10; width: 75
        id: baseNumberOct1
        text: "14"
    }
    ComboBox{
        y:10; x:10+5+baseNumberOct1.width; width: 75
        id: multiplyByOct1
        model: ["2","3"]
        currentIndex: 0
    }
    TextEdit{
        y:10; x:10+5*2+baseNumberOct1.width+multiplyByOct1.width; width: 75
        id: groubByOtc1
        text: "7"
    }
    TextEdit{
        y:10; x:10+5*3+baseNumberOct1.width+multiplyByOct1.width+groubByOtc1.width; width: 75
        id:elementsToCountOtc1
        text:"1000"
    }
    Button{
        id: firstButton
        text: "calc 1"
        y:10; x:100+5*3+baseNumberOct1.width+multiplyByOct1.width+groubByOtc1.width; width: 75
        onClicked: {
            textArea.text = firstOct.calculate(baseNumberOct1.text,multiplyByOct1.currentText,
                               groubByOtc1.text,elementsToCountOtc1.text);
            firstOct.update();
        }
    }
    Button{
        text: "calc 2"
        y:10; x:100+10+5*3+baseNumberOct1.width+multiplyByOct1.width+groubByOtc1.width+firstButton.width; width: 75
        onClicked: {
            textArea.text = secondOct.calculate(baseNumberOct2.text,multiplyByOct2.currentText,
                               groubByOtc2.text,elementsToCountOtc2.text);
            secondOct.update();
        }
    }

    Octavizer
    {
        x: 10
        y: 10 + baseNumberOct1.height + 10
        width: 1000
        height: 250
        id: firstOct
        Component.onCompleted: {
            firstOct.calculate(14,2,7,1000)
            firstOct.update()
            if (++octavizerItem.octInited == 2)
                octavizerItem.refillScalesCombobox()
        }
    }

    TextEdit{
        y: 275; x:10; width: 75
        id: baseNumberOct2
        text: "23"
    }
    ComboBox{
        y:275; x:10+5+baseNumberOct2.width; width: 75
        id: multiplyByOct2
        model: ["3","2"]
        currentIndex: 0
    }
    TextEdit{
        y:275; x:10+5*2+baseNumberOct2.width+multiplyByOct2.width; width: 75
        id: groubByOtc2
        text: "5"
    }
    TextEdit{
        y:275; x:10+5*3+baseNumberOct2.width+multiplyByOct2.width+groubByOtc2.width; width: 75
        id:elementsToCountOtc2
        text:"1000"
    }
    Button{
        text: "calc"
        visible: false
        y:275; x:parent.width-200; width: 75
        onClicked: {
            textArea.text = secondOct.calculate(baseNumberOct2.text,multiplyByOct2.currentText,
                                groubByOtc2.text,elementsToCountOtc2.text);
            secondOct.update();
        }
    }
    TextArea
    {
        text: " "
        id:textArea
        y:10; x:parent.width-400; width: 390
    }

    Octavizer
    {
        id: secondOct
        x: 10
        y: 10 + 10 + baseNumberOct1.height*2 + 10 + firstOct.height;
        width: 1000
        height: 250

        Component.onCompleted: {
            secondOct.calculate(23,3,5,1000)
            secondOct.update()
            if (++octavizerItem.octInited == 2)
                octavizerItem.refillScalesCombobox()
        }
    }


    ListModel{
        id: scalesList
    }

    ComboBox{
        y:275;x:10+5*4+baseNumberOct2.width+multiplyByOct2.width+groubByOtc2.width+elementsToCountOtc2.width
        width: 250
        id: checkScale
        model:scalesList
        onCurrentIndexChanged: {
            var scale; var result
            if (currentIndex >= firstOct.getListOfScalesSize())
            {
                var subIndex = currentIndex - firstOct.getListOfScalesSize() //check up -1
                //scale = secondOct.getListOfScales()[subIndex]
                //console.log("Scale of search " + scale+ " by index " + subIndex)
                firstOct.removeSelections()
                result = firstOct.findFitScale(secondOct,subIndex,false)
                firstOct.update()
                secondOct.setSingleSelection(subIndex)
                secondOct.update()
                //console.log("Result5 "+result)
            }
            else
            {
                //scale = firstOct.getListOfScales()[currentIndex]
                //console.log("Scale of search " + scale + " by index " + currentIndex)
                secondOct.removeSelections()
                result = secondOct.findFitScale(firstOct,currentIndex,true)
                firstOct.setSingleSelection(currentIndex)
                firstOct.update()
                secondOct.update()
                //console.log("Result7 "+result)
            }

        }
    }

    function refillScalesCombobox() {
        scalesList.clear()
        var scalesStringlist = firstOct.getListOfScalesNames()
        for (var i = 0; i < scalesStringlist.length; ++i)
            scalesList.append({"text":scalesStringlist[i]});
        var scalesStringlistSecond = secondOct.getListOfScalesNames()
        for (i = 0; i < scalesStringlistSecond.length; ++i)
            scalesList.append({"text":scalesStringlistSecond[i]});
    }
}
