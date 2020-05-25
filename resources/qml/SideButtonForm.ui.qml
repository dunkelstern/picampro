import QtQuick 2.0
import QtGraphicalEffects 1.0

Item {
    width: 120
    height: 120
    property alias iconSource: icon.source
    property alias titleText: buttonText.text
    property alias colorbarColor: colorbar.color
    property alias buttonFlashOpacity: backgroundFlash.opacity

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
                    color: "#171717"
                }
                GradientStop {
                    id: gradientEnd
                    position: 1
                    color: "#2e2e2e"
                }
            }
            Rectangle {
                id: backgroundFlash
                color: "#2e2e2e"
                anchors.fill: parent
                opacity: 0
            }

            Rectangle {
                id: iconBackground
                width: parent.width * 0.6
                height: parent.height * 0.3
                color: "#5c5c5c"
                radius: 0.25 * height
                anchors.verticalCenterOffset: -height / 2
                anchors.verticalCenter: parent.verticalCenter
                anchors.horizontalCenter: parent.horizontalCenter
                border.color: "#00000000"

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
                color: "#5c5c5c"
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
        color: "#ff0000"
        anchors.top: parent.top
        anchors.topMargin: 0
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 0
        anchors.right: parent.right
        anchors.rightMargin: 0
    }
}
