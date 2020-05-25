import QtQuick 2.11
import QtQuick.Window 2.11
import QtQuick.VirtualKeyboard 2.1

Window {
    id: window
    title: qsTr("PiCamPro")
    width: 1024
    height: 600
    color: "#000000"
    visible: true

    SideButton {
        id: button1
        width: parent.height / 5
        height: (parent.height / 5) - 2
        anchors.top: parent.top
        anchors.topMargin: 0
        anchors.right: parent.right
        anchors.rightMargin: 0
        colorbarColor: "#FF595E"
        titleText: qsTr("Auto")
        iconSource: "../icons/ISO.svg"
    }

    SideButton {
        id: button2
        width: parent.height / 5
        height: (parent.height / 5) - 2
        anchors.top: button1.bottom
        anchors.right: parent.right
        anchors.rightMargin: 0
        anchors.topMargin: 2
        colorbarColor: "#FFCA3A"
        titleText: qsTr("+ 0 EV")
        iconSource: "../icons/EV.svg"
    }
    SideButton {
        id: button3
        width: parent.height / 5
        height: (parent.height / 5) - 2
        anchors.top: button2.bottom
        anchors.right: parent.right
        anchors.rightMargin: 0
        anchors.topMargin: 2
        colorbarColor: "#8AC926"
        titleText: qsTr("Shade")
        iconSource: "../icons/wb-shade.svg"
    }
    SideButton {
        id: button4
        width: parent.height / 5
        height: (parent.height / 5) - 2
        anchors.top: button3.bottom
        anchors.right: parent.right
        anchors.rightMargin: 0
        anchors.topMargin: 2
        colorbarColor: "#1982C4"
        titleText: qsTr("Image")
        iconSource: "../icons/settings-image.svg"
    }
    SideButton {
        id: button5
        width: parent.height / 5
        height: (parent.height / 5) - 2
        anchors.top: button4.bottom
        anchors.right: parent.right
        anchors.rightMargin: 0
        anchors.topMargin: 2
        colorbarColor: "#6A4C93"
        titleText: qsTr("Settings")
        iconSource: "../icons/settings-technical.svg"
    }

    Rectangle {
        id: videoWindow
        color: "#2e2e2e"
        anchors.right: button1.left
        anchors.left: parent.left
        anchors.top: parent.top
        height: width / 16 * 9
    }
}

/*##^##
Designer {
    D{i:0;formeditorZoom:0.5}D{i:1;anchors_y:236}D{i:2;anchors_y:236}D{i:6;anchors_width:200;anchors_x:387;anchors_y:187}
}
##^##*/
