import QtQuick 2.12
import QtQuick.Controls 2.5
import '../components'
import Athenum 1.0

Item {
    id: pageCyclicPrime

    property string athName: "Cyclic primes"
    property int requestedWidth: width
    property int requestedHeight: 500
    property string descriptionText: "Some special prime numbers generated from full reptend"

    property int prime: 0

    CyclicPrime{
        anchors.fill: parent
    }


    //There may be formulas to generate cyclic numbers from the geo progression, so they are ever rising,
    //And there is a place for 7*5
}
