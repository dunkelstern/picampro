import QtQuick 2.11

SideButtonBar {
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

    buttonIcons:  [
        "../icons/wb-manual.svg",
        "../icons/wb-auto.svg",
        "../icons/wb-sunlight.svg",
        "../icons/wb-cloudy.svg",
        "../icons/wb-shade.svg",
        "../icons/wb-tungsten.svg",
        "../icons/wb-fluorescent.svg",
        "../icons/wb-incandescent.svg",
        "../icons/wb-flash.svg",
        "../icons/wb-horizon.svg"
    ]
    buttonColors: [
        Constants.accentGreen,
        Constants.accentGreen,
        Constants.accentGreen,
        Constants.accentGreen,
        Constants.accentGreen,
        Constants.accentGreen,
        Constants.accentGreen,
        Constants.accentGreen,
        Constants.accentGreen,
        Constants.accentGreen
    ]

    onSideButtonClicked: {
        setWB(buttonTitles[buttonID])
    }
}