import QtQuick 2.11

SideButtonBar {
    id: container

    signal buttonClicked(int buttonID)

    property string buttonIcon: ""
    property color buttonColor: Constants.accentRed
    property alias buttonTitles: container.buttonTitles
    property alias buttons: container.buttons

    function makeButtonIcons(num) {
        var result = Array(num)
        for (var i = 0; i < num; i++) {
            result[i] = buttonIcon
        }
        return result
    }

    function makeButtonColors(num) {
        var result = Array(num)
        for (var i = 0; i < num; i++) {
            result[i] = buttonColor
        }
        return result
    }

    buttonIcons: makeButtonIcons(buttonTitles.length)
    buttonColors: makeButtonColors(buttonTitles.length)

    onSideButtonClicked: buttonClicked(buttonID)
}