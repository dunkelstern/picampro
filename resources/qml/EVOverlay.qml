
import QtQuick 2.11

UnifiedSideButtonBar {
    id: container

    signal setEV(int value)

    anchors.top: parent.top
    anchors.bottom: parent.bottom
    height: parent.height
    x: parent.width

    buttonTitles: [
        "-10 EV",
        "-5 EV",
        "0 EV",
        "+5 EV",
        "+10 EV"
    ]

    buttonIcon:  "../icons/EV.svg"
    buttonColor: Constants.accentYellow

    onButtonClicked: {
        switch (buttonID) {
            case 0:
                setEV(-10)
                break;
            case 1:
                setEV(-5)
                break;
            case 2:
                setEV(0)
                break;
            case 3:
                setEV(5)
                break;
            case 4:
                setEV(10)
                break;        
            default:
                break;
        }
    }

    states: [
        State {
            name: "hidden"
            PropertyChanges {
                target: ev
                x: parent.width
            }
        },
        State {
            name: "visible"
            PropertyChanges {
                target: ev
                x: parent.width - width
            }
        }
    ]

    transitions: [
        Transition {
            NumberAnimation {
                properties: "x"
            }
        }
    ]
}