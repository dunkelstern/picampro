import QtQuick 2.11
import QtQuick.Controls 2.4

SideButtonBar {
    id: wb

    signal setValue(string key, int value)

    property IconSlider slider
    property var currentValues
    property var ranges
    property string activeValue

    anchors.top: parent.top
    anchors.bottom: parent.bottom
    height: parent.height
    width: parent.width
    x: parent.width

    buttonTitles: [
        "Sharpness",
        "Contrast",
        "Brightness",
        "Saturation",
        "WB Red",
        "WB Blue",
        "DRC"
    ]

    buttonIcons: [
        "../icons/image-sharpness.svg",
        "../icons/image-contrast.svg",
        "../icons/image-brightness.svg",
        "../icons/image-saturation.svg",
        "../icons/image-awb-gain-red.svg",
        "../icons/image-awb-gain-blue.svg",
        "../icons/image-drc.svg",
    ]

    function makeButtonColors(num) {
        var result = Array(num)
        for (var i = 0; i < num; i++) {
            result[i] = Constants.accentBlue
        }
        return result
    }

    buttonColors: makeButtonColors(buttonTitles.length)

    function sliderMoved() {
        setValue(activeValue, slider.value)
        currentValues[activeValue] = slider.value
    }

    onSideButtonClicked: {
        var buttonMapping = [
            'sharpness',
            'contrast',
            'brightness',
            'saturation',
            'awb_gain_red',
            'awb_gain_blue',
            'drc'
        ]

        activeValue = buttonMapping[buttonID]

        // Show and setup slider
        slider.from = ranges[activeValue][0]
        slider.to = ranges[activeValue][1]
        slider.value = currentValues[activeValue]
        slider.iconSource = '../icons/image-' + activeValue.replace(/_/g, "-") +  '.svg'
        slider.visible = true

        slider.onMoved.disconnect(sliderMoved)
        slider.onMoved.connect(sliderMoved)
    }
}
