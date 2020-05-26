import QtQuick 2.11

Item {
    id: container

    signal bottomButtonClicked(int buttonID)

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

    Row {
        spacing: 2
        anchors.top: parent.top
        anchors.right: parent.right
        width: parent.height * buttonTitles.length
        height: parent.height

        Repeater {
            id: buttons
            model: buttonTitles
            BottomButton {
                width: height - 2
                height: parent.height                
                colorbarColor: buttonColors[index]
                titleText: modelData
                iconSource: buttonIcons[index]
                onActivated: bottomButtonClicked(index)
            }
        }
    }

    states: [
        State {
            name: "hidden"
            PropertyChanges {
                target: container
                y: parent.height
            }
        },
        State {
            name: "visible"
            PropertyChanges {
                target: container
                y: parent.height - height
            }
        }
    ]

    transitions: [
        Transition {
            NumberAnimation {
                properties: "y"
            }
        }
    ]

    Component.onCompleted: state = 'hidden'
}