import QtQuick 2.10
import QtQuick.Window 2.10
import QtQuick.Controls 2.5
import QtQuick.Layouts 1.3

import 'components'
//https://doc.qt.io/qt-5/qtqml-syntax-directoryimports.html

ApplicationWindow {
//Item {
    id: mainWindow
    visible: true
    width: 1280 //fullscreen please
    height: 720

    ListModel{
        id: openedTabsList
    }

    //ony use with web gl!!
    property int webGLCounter : 0 //don't use not for web gl - need qml notifier if its so! parse args..
    onClosing: {
        if (athenumInfo.isWebGl()){
            if (webGLCounter){
                console.log("CLOSED") //FIRST IT GETS CLOSED, then it gets opened, and next time it closed we can kill it
                Qt.quit()}
            ++webGLCounter
        }
        //another strategy is to reinit on open, so when new suer comes - nothing was saved there
    }


    Component.onCompleted: { 
        openedTabsList.append({"pageName":".","pageURL":"/pages/pageFullReptendPrime.qml","ls":"","prevInd":""})
        openedTabsList.append({"pageName":".","pageURL":"/pages/pagePrimeScales.qml","ls":"","prevInd":""}) //TODO wipe the pageName
        //vmainRepeater.model = openedTabsList.count
        initPages()
    }

    Popup{
        id: newWindowPopup

        ComboBox{ //Replace with combobox and load here list of files from all pages
            id:newWindowName
            width: 490
            //placeholderText: "URL"
            model: ["/pages/test2.qml","/pages/pagePrime.qml", "/pages/pageCyclicPrimes.qml", "/pages/pageScaleOfNotation.qml"]

            Component.onCompleted: {
                var list = athenumInfo.loadQmlFilesList()
                //LATER EXTEND THIS FUNCTION TO PARSE NEEDED PROPERTY FROM PYTHON ITSELF

                var subList = list

                for (var i = 0; i < list.length; ++i){
                    var element = list[i]
                    ////console.log("PRELoading page ",element)
                    hiddenComboLoader.setSource("file:///home/constcut/dev/athenum/qml" + element)
                    if (hiddenComboLoader.item !== null) {

                        var pageName = "..."
                        if (hiddenComboLoader.item.athName !== undefined)
                            pageName = hiddenComboLoader.item.athName
                        list[i] = pageName
                    }
                }
                newWindowName.model = list
            }
            Loader{
                visible: false
                id: hiddenComboLoader
            }

            onCurrentTextChanged: {
                var list = athenumInfo.loadQmlFilesList()
                //LATER EXTEND THIS FUNCTION TO PARSE NEEDED PROPERTY FROM PYTHON ITSELF
                hiddenLoader.setSource("file:///home/constcut/dev/athenum/qml" + list[currentIndex])
                if (hiddenLoader.item !== null) {
                    if (hiddenLoader.item.descriptionText !== undefined)
                        descriptionArea.text = hiddenLoader.item.descriptionText
                }
            }
        }

        width: 750
        height: 270
        x:100
        y:100

        Button{
            text: "open"
            y: 0
            x: 500
            onPressed: {
                var saveIndex = tabBar.currentIndex

                var list = athenumInfo.loadQmlFilesList()
                //LATER EXTEND THIS FUNCTION TO PARSE NEEDED PROPERTY FROM PYTHON ITSELF
                //later could be done also a requset to open by page name, yet it goes by url only

                //JSON OBJECT
                /*var jsonString = '{"key": "value"}'
                console.log(jsonString)
                var JsonObject = JSON.parse(jsonString);
                console.log(JsonObject.key, " j o")*/

                var jsonOb

                if (startParams.text.length > 0)
                    jsonOb = JSON.parse(startParams.text);


                openedTabsList.append({"pageName":"New page","pageURL":list[newWindowName.currentIndex],"jObj":jsonOb,"ls":"","prevInd":""}) //also test saved as idea is interesting //emptyPage.qml - later make it

                tabsRepeater.model = openedTabsList.count
                tabBar.currentIndex = tabsRepeater.model-1
                newWindowPopup.close()
                initPages()
            }
        }
        Button{
            text: "close"
            y: 0
            x: 615
            onPressed: {
               newWindowPopup.close()
            }
        }

        TextArea{
            id: descriptionArea
            y: 70
            x: 0
            placeholderText: "Description would be there if its implemented in qml file"
            width: parent.width
            height: 100
        }
        TextArea{
            id: startParams
            y: 175
            x:0
            height: 120
            width: parent.width
            placeholderText: "{initialParams:values,...}"
        }
        Loader{
            visible: false
            id: hiddenLoader
        }
    }

    Button {
        text: ":" //TODO later replace the function
        width: 25
        x: 0
        onClicked: { 
            var url = mainRepeater.itemAt(tabBar.currentIndex).url
            mainRepeater.itemAt(tabBar.currentIndex).loadNewUrl(url)
        }
    }

    Button { //maybe later shift the x depending on size of TabBar to the end of last tab
         //will need to calc full tabbar size
        x: tabBar.width + 25
        text: "+"
        width: 25
        onClicked: {
             //saveIndex if need old position before add use save index
            //MUST OPEN POP UP HERE
            //with list of qml pages items
            //and description so it could be just chosen
            newWindowPopup.open()
        }
        id: outerAdd
        //visible: innerAdd.visible == false
    }

    Button {
        x: parent.width - width - 5
        text: "[h?]"
        onClicked: {
            console.log("help presseed")
            //access athenum page on focus
            //call help functions that sets all the tooltips on
            //and shows tooltip that to turn this off need press help button again
            //if (mainRepeater.itemAt(tabBar.currentIndex).helpPressed !== undefined)
            mainRepeater.itemAt(tabBar.currentIndex).helpPressed()
        }
    }

    TabBar {
        id: tabBar
        width: (parent.width-50) > tabBar.contentWidth ? tabBar.contentWidth : parent.width - 50
        x: 25
        Repeater{
            id: tabsRepeater
            model: openedTabsList.count
            TabButton{
                text: openedTabsList.get(index).pageName
                width: implicitWidth
                onDoubleClicked: {
                    console.log("CLOSE TAB " + index) //later should add it to history so we can return it back
                    openedTabsList.remove(index)
                    tabsRepeater.model = openedTabsList.count
                    //TODO compare prev index
                }
            }
        } //or on double click on empty area - makes a new tab - later should make it more usable
    }

    function loadNewPage(pageName){
        //console.log("On a top level we ready to open page",pageName)

        //NEED TO SEARCH TO FIND URL
        var list = athenumInfo.loadQmlFilesList()
        //LATER EXTEND THIS FUNCTION TO PARSE NEEDED PROPERTY FROM PYTHON ITSELF
        var pageUrl = '...'
        for (var i = 0; i < list.length; ++i)
            if (newWindowName.model[i] === pageName) {
                pageUrl = list[i]
            }

        openedTabsList.append({"pageName":"New page","pageURL":pageUrl,"ls":"","prevInd":""}) //also test saved as idea is interesting //emptyPage.qml - later make it
        tabsRepeater.model = openedTabsList.count
        tabBar.currentIndex = tabsRepeater.model-1
        initPages()
    }

    function loadNewUrl(pageUrl){
        //console.log("On a top level we ready to open url",pageUrl)
        openedTabsList.append({"pageName":"New page","pageURL":pageUrl,"ls":"","prevInd":""}) //also test saved as idea is interesting //emptyPage.qml - later make it
        tabsRepeater.model = openedTabsList.count
        tabBar.currentIndex = tabsRepeater.model-1
        initPages()
    }

    function loadNewUrlInit(pageUrl, jStr){
        var jsonOb = null
        if (jStr.length > 0)
            jsonOb = JSON.parse(jStr);

        openedTabsList.append({"pageName":"New page","pageURL":pageUrl,"ls":"","prevInd":"","jObj":jsonOb}) //also test saved as idea is interesting //emptyPage.qml - later make it
        tabsRepeater.model = openedTabsList.count
        tabBar.currentIndex = tabsRepeater.model-1
        initPages()
    }

    Timer{
        interval: 500; running: true; repeat: true
        onTriggered: {
            //Todo improve:
            //console.log(mainWindow.width, mainWindow.height, " current mainWindow.w .h ")
            mainRepeater.itemAt(tabBar.currentIndex).resizePage(pagesLayout.width, pagesLayout.height)
        }
    }

    function initPages(){
        for (var i = 0; i < openedTabsList.count; ++i){

            if (openedTabsList.get(i).ls === "loaded")
                continue

            var pageURL = "file://" + athenumInfo.getQMLPath() + openedTabsList.get(i).pageURL
            var emptyJson = openedTabsList.get(i).jObj
            mainRepeater.itemAt(i).loadNewUrl(pageURL, emptyJson)
            openedTabsList.get(i).ls = "loaded";
            openedTabsList.get(i).prevInd = i //TODO establish change for loaded ones
        }
        tabBar.currentIndex = openedTabsList.count - 1
    }

    StackLayout {
        y: 5
        //width: parent.width
        //height: parent.height - y
        anchors.fill: parent
        id: pagesLayout

        currentIndex: tabBar.currentIndex

        Repeater {
            id: mainRepeater
            model: 64


            AthenumPage{id: athenumPageObject

                //anchors.fill: pagesLayout

                Component.onCompleted: {
                    /*
                    var filePath = "file://" + athenumInfo.getQMLPath() + openedTabsList.get(index).pageURL
                    var emptyJson = openedTabsList.get(index).jObj
                    athenumPageObject.loadNewUrl(filePath, emptyJson)
                    */
                }
                onUrlWasEdited: {
                    openedTabsList.get(index).pageURL = athenumInfo.cutAppPath(athenumPageObject.url)
                }
                onChangeTabTitle: {
                    if (newTitle){
                        openedTabsList.get(index).pageName = newTitle

                        if (tabsRepeater.itemAt(index))
                            tabsRepeater.itemAt(index).text = openedTabsList.get(index).pageName //warning
                    }
                }
                onRequestToOpenPage:{
                   console.log("App open page",pageName)
                   mainWindow.loadNewPage(pageName)
                   //IT OPENS URL ACTUALLY
                }
                onRequestToOpenUrl:{
                   console.log("App open url",pageUrl)
                   console.log(typeof jsonObject)
                   if (typeof jsonObject !== undefined) {
                       console.log("request with json", jsonObject)
                       mainWindow.loadNewUrlInit(pageUrl, jsonObject)
                   }
                   else
                    mainWindow.loadNewUrl(pageUrl)
                }
            }
            onModelChanged: { //future: serialize pages states.. or StackView as solution for reloading issue on adding new
            }
        }
    }
}
