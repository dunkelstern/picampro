import QtQuick 2.11

UnifiedSideButtonBar {
    id: ev

    signal setEV(int value)

    anchors.top: parent.top
    anchors.bottom: parent.bottom
    height: parent.height
    x: parent.width

    buttonTitles: [  // FIXME: Get buttons from model state
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
}