import QtQuick 2.11

SideButtonBar {
    id: wb

    signal setValue(int value)

    anchors.top: parent.top
    anchors.bottom: parent.bottom
    height: parent.height
    width: parent.width
    x: parent.width

    buttonTitles: [
        "Sharpness",
        "Contrast",
        "Brightness",
        "Saturation",
        "WB Red",
        "WB Blue",
        "DRC"
    ]

    buttonIcons: [ // TODO: Icons
        "../icons/stop.svg",
        "../icons/stop.svg",
        "../icons/stop.svg",
        "../icons/stop.svg",
        "../icons/stop.svg",
        "../icons/stop.svg",
        "../icons/stop.svg",
    ]

    function makeButtonColors(num) {
        var result = Array(num)
        for (var i = 0; i < num; i++) {
            result[i] = Constants.accentBlue
        }
        return result
    }

    buttonColors: makeButtonColors(buttonTitles.length)

    onSideButtonClicked: {
        // TODO: Show slider
    }
}