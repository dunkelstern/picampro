import QtQuick 2.11

Item {
    id: container

    signal sideButtonClicked(int buttonID)

    property alias button1: button1
    property alias button2: button2
    property alias button3: button3
    property alias button4: button4
    property alias button5: button5

    property var buttonTitles: [
        "Button1",
        "Button2",
        "Button3",
        "Button4",
        "Button5"
    ]

    property var buttonIcons: [
        "",
        "",
        "",
        "",
        ""
    ]

    property var buttonColors: [
        Constants.accentRed,
        Constants.accentRed,
        Constants.accentRed,
        Constants.accentRed,
        Constants.accentRed
    ]

    SideButton {
        id: button1
        width: parent.height / 5
        height: (parent.height / 5) - 2
        anchors.top: parent.top
        anchors.topMargin: 0
        anchors.right: parent.right
        anchors.rightMargin: 0
        colorbarColor: buttonColors[0]
        titleText: buttonTitles[0]
        iconSource: buttonIcons[0]
        onActivated: sideButtonClicked(0)
    }

    SideButton {
        id: button2
        width: parent.height / 5
        height: (parent.height / 5) - 2
        anchors.top: button1.bottom
        anchors.right: parent.right
        anchors.rightMargin: 0
        anchors.topMargin: 2
        colorbarColor: buttonColors[1]
        titleText: buttonTitles[1]
        iconSource: buttonIcons[1]
        onActivated: sideButtonClicked(1)
    }
    SideButton {
        id: button3
        width: parent.height / 5
        height: (parent.height / 5) - 2
        anchors.top: button2.bottom
        anchors.right: parent.right
        anchors.rightMargin: 0
        anchors.topMargin: 2
        colorbarColor: buttonColors[2]
        titleText: buttonTitles[2]
        iconSource: buttonIcons[2]
        onActivated: sideButtonClicked(2)
    }
    SideButton {
        id: button4
        width: parent.height / 5
        height: (parent.height / 5) - 2
        anchors.top: button3.bottom
        anchors.right: parent.right
        anchors.rightMargin: 0
        anchors.topMargin: 2
        colorbarColor: buttonColors[3]
        titleText: buttonTitles[3]
        iconSource: buttonIcons[3]
        onActivated: sideButtonClicked(3)
    }
    SideButton {
        id: button5
        width: parent.height / 5
        height: (parent.height / 5) - 2
        anchors.top: button4.bottom
        anchors.right: parent.right
        anchors.rightMargin: 0
        anchors.topMargin: 2
        colorbarColor: buttonColors[4]
        titleText: buttonTitles[4]
        iconSource: buttonIcons[4]
        onActivated: sideButtonClicked(4)
    }
}