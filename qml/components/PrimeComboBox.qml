import QtQuick 2.0
import Athenum 1.0 //well, when we release we would make it 0.1 instead, everywhere
import QtQuick.Controls 2.2 //go for 2.5?

//later we need to update for Qt 5.13, it would support Python nativly finally

Item {
    id: primesCombo

    ListModel{
        id: primeModel
    }
    ComboBox{
        id: innerCombo
        model: primeModel
    }
    property string text: innerCombo.currentText
    //Later nice to make small button after the ComboBox
    //And let to chose range of primes from popup
    //yet 1-50 is ok

    ///WHEN REVISION IS DONE REPLACE ON INPUTS OF TEXTFIELD TO THAT ONE
    function setPrime(primeNum){
        var p = primes.getPrimesList(1,100)
        for (var i = 0; i < p.length; ++i){
            if (p[i] === primeNum){
                innerCombo.currentIndex = i
                console.log("Prime combo set to ",i)
                break;     
            }
        }
        console.log("Failed to find?", primeNum)
    }

    Component.onCompleted: {
        primeModel.clear()
        var p = primes.getPrimesList(1,100)
        for (var i = 0; i < p.length; ++i){
            primeModel.append({text:p[i]})
        }
        //innerCombo.currentIndex = 3 //we set 7 as default
    }
    Primes{
        id: primes
        Component.onCompleted: {
            //console.log("Primes created")
        }
    }
}


