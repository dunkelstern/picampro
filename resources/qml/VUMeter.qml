import QtQuick 2.11

Item {
    id: vumeter
    property var vuLeft;
    property var peakLeft;
    property var vuRight;
    property var peakRight;

    Item {
        anchors.left: parent.left
        anchors.top: parent.top
        anchors.topMargin: 5
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 5
        anchors.rightMargin: 10

        Rectangle {
            id: leftBackground
            width: parent.width
            height: parent.height / 2 - 5
            x: 0
            y: 0
            color: Constants.bgColor
        }
        Rectangle {
            id: leftLow
            width: Math.min(vuLeft, 0.8) * parent.width
            height: parent.height / 2 - 5
            y: 0
            x: 0
            border.width: 0
            color: Constants.accentGreen
        }
        Rectangle {
            id: leftMid
            width: (Math.min(vuLeft, 0.9) - 0.8) * parent.width
            height: parent.height / 2 - 5
            y: 0
            x: parent.width * 0.8
            visible: vuLeft > 0.8
            border.width: 0
            color: Constants.accentYellow
        }
        Rectangle {
            id: leftHigh
            width: (vuLeft - 0.9) * parent.width
            height: parent.height / 2 - 5
            y: 0
            x: parent.width * 0.9
            visible: vuLeft > 0.9
            border.width: 0
            color: Constants.accentRed
        }
        Rectangle {
            id: leftPeak
            width: 2
            height: parent.height / 2 - 5
            y: 0
            x: parent.width * peakLeft
            visible: peakLeft > 0.0
            border.width: 0
            color: Constants.iconColor
        }

        Rectangle {
            id: rightBackground
            width: parent.width
            height: parent.height / 2 - 5
            x: 0
            y: parent.height / 2 + 5
            color: Constants.bgColor
        }
        Rectangle {
            id: rightLow
            width: Math.min(vuRight, 0.8) * parent.width
            height: parent.height / 2 - 5
            y: parent.height / 2 + 5
            x: 0
            border.width: 0
            color: Constants.accentGreen
        }
        Rectangle {
            id: rightMid
            width: (Math.min(vuRight, 0.9) - 0.8) * parent.width
            height: parent.height / 2 - 5
            y: parent.height / 2 + 5
            x: parent.width * 0.8
            visible: vuRight > 0.8
            border.width: 0
            color: Constants.accentYellow
        }
        Rectangle {
            id: rightHigh
            width: (vuRight - 0.9) * parent.width
            height: parent.height / 2 - 5
            y: parent.height / 2 + 5
            x: parent.width * 0.9
            visible: vuRight > 0.9
            border.width: 0
            color: Constants.accentRed
        }
        Rectangle {
            id: rightPeak
            width: 2
            height: parent.height / 2 - 5
            y: parent.height / 2 + 5
            x: parent.width * peakRight
            visible: peakRight > 0.0
            border.width: 0
            color: Constants.iconColor
        }

    }
}
