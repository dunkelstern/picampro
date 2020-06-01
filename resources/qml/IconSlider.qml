import QtQuick 2.11
import QtQuick.Controls 2.4

Item {
    id: container

    signal moved()

    property alias from: slider.from
    property alias to: slider.to
    property alias value: slider.value
    property alias iconSource: icon.source

    Image {
        id: icon
        sourceSize.height: 0.3 * parent.height
        sourceSize.width: 0.3 * parent.height
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.topMargin: 0.35 * parent.height
        anchors.leftMargin: 0.35 * parent.height

        width: 0.3 * parent.height
        height: 0.3 * parent.height
        fillMode: Image.PreserveAspectFit
    }

    Slider {
        id: slider
        anchors.left: icon.right
        anchors.leftMargin: 0.35 * parent.height
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        anchors.right: parent.right

        snapMode: Slider.SnapAlways
        stepSize: 1.0
        from: 1
        to: 100
        value: 25

        onMoved: container.moved()
    }
}
