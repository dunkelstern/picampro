import QtQuick 2.11
import QtGraphicalEffects 1.0

Item {
    width: 120
    height: 120
    
    property alias iconSource: icon.source
    property alias titleText: buttonText.text
    property alias colorbarColor: colorbar.color
    property alias buttonFlashOpacity: backgroundFlash.opacity

    signal activated

    Rectangle {
        id: background
        anchors.fill: parent
        border.width: 0
        LinearGradient {
            id: linearGradient
            anchors.fill: parent
            start: Qt.point(0, 0)
            end: Qt.point(width, 0)
            gradient: Gradient {
                GradientStop {
                    id: gradientStart
                    position: 0
                    color: Constants.btnBackgroundColor
                }
                GradientStop {
                    id: gradientEnd
                    position: 1
                    color: Constants.bgColor
                }
            }
            Rectangle {
                id: backgroundFlash
                color: Constants.bgColor
                anchors.fill: parent
                opacity: 0
            }

            Rectangle {
                id: iconBackground
                width: parent.width * 0.6
                height: parent.height * 0.3
                color: Constants.btnTextColor
                radius: 0.25 * height
                anchors.verticalCenterOffset: -height / 2
                anchors.verticalCenter: parent.verticalCenter
                anchors.horizontalCenter: parent.horizontalCenter

                Image {
                    id: icon
                    sourceSize.height: 0.6 * parent.height
                    sourceSize.width: 0.6 * parent.width
                    anchors.topMargin: 0.2 * parent.height
                    anchors.bottomMargin: 0.2 * parent.height
                    anchors.leftMargin: 0.2 * parent.width
                    anchors.rightMargin: 0.2 * parent.width
                    anchors.fill: parent
                    fillMode: Image.PreserveAspectFit
                }
            }

            Text {
                id: buttonText
                color: Constants.btnTextColor
                text: qsTr("Text")
                anchors.verticalCenterOffset: height * 1.5
                anchors.verticalCenter: parent.verticalCenter
                anchors.horizontalCenter: parent.horizontalCenter
                horizontalAlignment: Text.AlignHCenter
                font.pixelSize: parent.height / 7
            }
        }
    }

    Rectangle {
        id: colorbar
        width: parent.width / 24
        color: Constants.accentRed
        anchors.top: parent.top
        anchors.topMargin: 0
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 0
        anchors.right: parent.right
        anchors.rightMargin: 0
    }

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
