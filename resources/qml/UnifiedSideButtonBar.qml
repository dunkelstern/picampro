import QtQuick 2.11

SideButtonBar {
    id: container

    signal buttonClicked(int buttonID)

    property string buttonIcon: ""
    property color buttonColor: Constants.accentRed
    property alias buttonTitles: container.buttonTitles

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