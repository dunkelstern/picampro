import QtQuick 2.4

SideButtonForm {
    signal activated

    MouseArea {
        anchors.fill: parent
        onClicked: {
            clickNotify.running = true
            parent.activated()
        }
    }

    SequentialAnimation on buttonFlashOpacity {
        id: clickNotify
        running: false

        NumberAnimation {
            from: 0.0
            to: 1.0
            duration: 100
        }

        NumberAnimation {
            from: 1.0
            to: 0.0
            duration: 300
        }
    }
}
