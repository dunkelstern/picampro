import QtQuick 2.11

UnifiedSideButtonBar {
    id: iso

    signal setISO(int value)

    anchors.top: parent.top
    anchors.bottom: parent.bottom
    height: parent.height
    x: parent.width

    buttonTitles: [  // FIXME: get button titles from model state
        "Auto",
        "100",
        "200",
        "400",
        "800",
        "1600",
        "3200",
    ]

    buttonIcon:  "../icons/ISO.svg"
    buttonColor: Constants.accentRed

    onButtonClicked: {
        switch (buttonID) {
            case 0:
                setISO(0)
                break;        
            case 1:
                setISO(100)
                break;
            case 2:
                setISO(200)
                break;
            case 3:
                setISO(400)
                break;
            case 4:
                setISO(800)
                break;
            case 5:
                setISO(1600)
                break;
            case 6:
                setISO(3200)
                break;
            default:
                break;
        }
    }
}