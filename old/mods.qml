import QtQuick 2.10
import QtQuick.Window 2.10
import QtQuick.Controls 2.2
import QtQuick.Dialogs 1.3

Item {
    id: pageProcess

    property string athName: "Modules"

    width: 1000 //anchors
    height: 600

    ComboBox{
        x:10
        y:10
        id: modulesList
        width: 600
        onCurrentIndexChanged: {
            qmlTypesList.model = athenumModules.getQMLTypes(currentIndex)
        }
    }
    ComboBox{
        x:10
        y:100
        width: 600
        id: qmlTypesList
    }


    ComboBox{
        x:10
        y:200
        id: qmlPluginsList
        width: 600

        onCurrentIndexChanged: {
            var list = athenumModules.getPluginsFiles()
            pluginDesk.text = list[currentIndex]
        }
    }
    Text{
        x:10
        y: 250
        id: pluginDesk
        text: "black pre"
    }

    FileDialog {
        id: fileDialogModule //for modules
        title: "Please choose a file"
        folder: athenumInfo.getPath() + '/..'
        onAccepted: {
            var pathString = fileDialogModule.fileUrls[0]
            var cuttenPath = athenumInfo.cutAppPath(pathString)
            athenumModules.load(cuttenPath)
            modulesList.model = athenumModules.getModulesNames()
        }
    }

    Button{
        x: 620
        y: 10
        text: "Add module"
        onClicked:{
            fileDialogModule.open()
        }
    }

    FileDialog {
        id: fileDialogPlugin //for plugins
        title: "Please choose a file"
        folder: athenumInfo.getPath() + '/..'
        onAccepted: {
            var pathString = fileDialogPlugin.fileUrls[0]
            var cuttenPath = athenumInfo.cutAppPath(pathString)
            var importName = "TimeExample" //just an example, need imput it too :(
            athenumModules.loadQMLPlugin(cuttenPath,importName)
            qmlPluginsList.model = athenumModules.getPluginsNames()
        }
    }

    Button{
        x: 620
        y: 200
        text: "Add plugin"
        onClicked:{
            fileDialogPlugin.open()
        }
    }

    Component.onCompleted: {
        modulesList.model = athenumModules.getModulesNames()
        qmlTypesList.model = athenumModules.getQMLTypes(0)
        qmlPluginsList.model = athenumModules.getPluginsNames()
    }
}
