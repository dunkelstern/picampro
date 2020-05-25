import QtQuick 2.11

UnifiedSideButtonBar {
    id: iso

    signal setISO(int value)

    anchors.top: parent.top
    anchors.bottom: parent.bottom
    height: parent.height
    x: parent.width

    buttonTitles: [
        "100",
        "200",
        "400",
        "800",
        "Auto"
    ]

    buttonIcon:  "../icons/ISO.svg"
    buttonColor: Constants.accentRed

    onButtonClicked: {
        switch (buttonID) {
            case 0:
                setISO(100)
                break;
            case 1:
                setISO(200)
                break;
            case 2:
                setISO(400)
                break;
            case 3:
                setISO(800)
                break;
            case 4:
                setISO(0)
                break;        
            default:
                break;
        }
    }

    states: [
        State {
            name: "hidden"
            PropertyChanges {
                target: iso
                x: parent.width
            }
        },
        State {
            name: "visible"
            PropertyChanges {
                target: iso
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