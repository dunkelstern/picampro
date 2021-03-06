import QtQuick 2.11

Flickable {
    id: container

    signal sideButtonClicked(int buttonID)

    property alias buttons: buttons

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

    property var buttonColors: Constants.accentColors

    contentHeight: width * buttonTitles.length
    contentWidth: width
    width: parent.width
    height: parent.height
    clip: true

    Column {
        spacing: 2
        anchors.top: parent.top
        anchors.right: parent.right
        width: container.height / 5 // fixed height to allow for use in flickable

        Repeater {
            id: buttons
            model: buttonTitles
            SideButton {
                width: parent.width
                height: width - 2
                colorbarColor: buttonColors[index]
                titleText: modelData
                iconSource: buttonIcons[index]
                onActivated: sideButtonClicked(index)
            }
        }
    }

    states: [
        State {
            name: "hidden"
            PropertyChanges {
                target: container
                x: parent.width
            }
        },
        State {
            name: "visible"
            PropertyChanges {
                target: container
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

    Component.onCompleted: state = 'hidden'
}