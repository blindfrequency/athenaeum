import QtQuick 2.0

Item {
    id: latexFormulaItem

    property string filename: "someFormula" // + random number for example

    function sum(first, mult, divs, num, den){
        formulaImage.source = ''
        QMLLatex.plotSum(first, mult, divs, num, den, athenumInfo.getPath() + '/../temp/' + latexFormulaItem.filename)
        formulaImage.source = "file:///" + athenumInfo.getPath() + '/../temp/' + latexFormulaItem.filename
        ///console.log("ATTEMPT TO LOAD ",formulaImage.source)
        ///console.log("JUST PATH",athenumInfo.getPath())
    } //same way we can make stupid version of librosa and matplot lib - its slow works, but its fast to work with it:) later we can update things we really need

    function raw(latext){
        formulaImage.source = ''
        ///console.log("Try latex formulas ", latext, latexFormulaItem.filename)
        QMLLatex.plotRawTex(latext, athenumInfo.getPath() + '/../temp/' + latexFormulaItem.filename)
        formulaImage.source = "file:///" + athenumInfo.getPath() + '/../temp/' + latexFormulaItem.filename
    }

    function clear(){
        formulaImage.source = ''
    }

    property int imageWidth: formulaImage.width

    Image{
        id: formulaImage
        cache: false //something like this
    }

    Component.onCompleted: {
        formulaImage.source = "file:///" + athenumInfo.getPath() + '/../temp/' + latexFormulaItem.filename
    }
}
