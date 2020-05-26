import QtQuick 2.11

BottomButtonBar {
    id: container

    signal buttonClicked(int buttonID)

    property string buttonIcon: ""
    property color buttonColor: Constants.accentRed
    property alias buttonTitles: container.buttonTitles
    property alias buttons: container.buttons

    buttonIcons: [
        buttonIcon,
        buttonIcon,
        buttonIcon,
        buttonIcon,
        buttonIcon
    ]

    buttonColors: [
        buttonColor,
        buttonColor,
        buttonColor,
        buttonColor,
        buttonColor
    ]


    onSideButtonClicked: buttonClicked(buttonID)
}