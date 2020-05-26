import QtQuick 2.11

UnifiedSideButtonBar {
    id: wb

    signal setWB(string value)

    anchors.top: parent.top
    anchors.bottom: parent.bottom
    height: parent.height
    width: parent.width
    x: parent.width

    buttonTitles: [
        "Manual",
        "Auto",
        "Sunlight",
        "Cloudy",
        "Shade",
        "Tungsten",
        "Fluorescent",
        "Incandescent",
        "Flash",
        "Horizon"
    ]

    buttonIcon:  "../icons/wb-shade.svg"
    buttonColor: Constants.accentGreen

    onButtonClicked: {
        setWB(buttonTitles[buttonID])
    }
}