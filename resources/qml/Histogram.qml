import QtQuick 2.11

Item {
    id: histogram
    property var histogramData

    Row {
        spacing: 1
        anchors.top: parent.top
        anchors.topMargin: 5
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        width: 5 * histogramData.length

        Repeater {
            id: histogram_lines
            model: histogramData
            Rectangle {
                width: 4
                height: parent.height / 100.0 * modelData
                y: parent.height - (parent.height / 100.0 * modelData)
                border.width: 0
                color: "#ffffff"
            }
        }
    }
}
