import QtQuick 2.11
import QtQuick.Window 2.11
import QtQuick.VirtualKeyboard 2.1
import QtQuick.Controls 2.4

Window {
    id: main

    property var modelData: {}
    property var histogramData: []
    property var vuMeterData: []

    property Item activeSideBar: sideBar
    property Item activeBottomBar: bottomBar
    property alias slider: slider

    signal setValue(string area, string key, string value)
    signal buttonPressed(string key)
    signal stopVideo()
    signal startVideo()

    title: "PiCamPro"
    width: 1024
    height: 600
    color: "black"
    visible: true

    function showSettings() {
        console.log("Show settings")
        main.stopVideo()
    }

    onModelDataChanged: {
        if (main.modelData === undefined) {
            return
        }
        sideBar.stateChanged(null)
    }

    onHistogramDataChanged: {
        if (main.histogramData === undefined) {
            return
        }
        histogram.histogramData = main.histogramData
    }

    onVuMeterDataChanged: {
        if (main.vuMeterData === undefined) {
            return
        }
        vuMeter.vuLeft = main.vuMeterData[0]
        vuMeter.peakLeft = main.vuMeterData[1]
        vuMeter.vuRight = main.vuMeterData[2]
        vuMeter.peakRight = main.vuMeterData[3]
    }

    SideButtonBar {
        id: sideBar
        objectName: "main"

        anchors.top: parent.top
        anchors.bottom: parent.bottom
        width: parent.height / 5
        height: parent.height
        x: parent.width - width

        buttonTitles: [
            "Auto",
            "0 EV",
            "Auto",
            "Image",
            "Settings"
        ]

        buttonIcons: [
            "../icons/ISO.svg",
            "../icons/EV.svg",
            "../icons/wb-auto.svg",
            "../icons/settings-image.svg",
            "../icons/settings-technical.svg"
        ]

        onSideButtonClicked: {
            switch (buttonID) {
                case 0:
                    // Show ISO selection overlay
                    main.activeSideBar = iso
                    main.activeBottomBar = okDialogBar
                    break;
                case 1:
                    // Show EV selection overlay
                    main.activeSideBar = ev
                    main.activeBottomBar = okDialogBar
                    break;
                case 2:
                    // Show WB selection overlay
                    main.activeSideBar = wb
                    main.activeBottomBar = scrollableDialogBar
                    break;
                case 3:
                    // Show image settings overlay
                    main.activeSideBar = image
                    main.activeBottomBar = scrollableDialogBar
                    break;
                case 4:
                    // Stop Video preview
                    main.activeSideBar = sideBar
                    main.activeBottomBar = bottomBar
                    main.buttonPressed("settings")
                    // TODO: Show settings screen
                    break;
                default:
                    break;
            }

            if (main.activeSideBar != sideBar) {
                main.activeSideBar.state = "visible"
                main.activeBottomBar.state = "visible"
                sideBar.state = "hidden"
                bottomBar.state = "hidden"
            }
        }

        onStateChanged: {
            if (main.modelData === undefined) {
                return
            }
            sideBar.buttons.itemAt(0).titleText = modelData.image.iso.replace(/\b(\w)/g, function(s) { return s.toUpperCase() })
            sideBar.buttons.itemAt(1).titleText = (modelData.image.ev > 0 ? "+" : "") + modelData.image.ev.toString() + ' EV'
            sideBar.buttons.itemAt(2).titleText = modelData.image.wb.replace(/\b(\w)/g, function(s) { return s.toUpperCase() })
            sideBar.buttons.itemAt(2).iconSource = "../icons/wb-" + modelData.image.wb.toLowerCase() + '.svg'
        }
    }

    Rectangle {
        id: videoWindow
        color: Constants.bgColor
        anchors.left: parent.left
        anchors.top: parent.top
        width: parent.width - sideBar.width
        height: width / 16 * 9
    }

    BottomButtonBar {
        id: bottomBar

        x: parent.width - sideBar.width - height * buttonTitles.length
        y: parent.height - height
        width: height * buttonTitles.length
        height: parent.height - videoWindow.height

        buttonTitles: [
            "Rec",
            "Stop",
            "Stream",
            "Mic"
        ]

        buttonIcons: [
            "../icons/rec.svg",
            "../icons/stop.svg",
            "../icons/stream.svg",
            "../icons/mic.svg"
        ]

        onBottomButtonClicked: {
            switch(buttonID) {
                case 0:
                    main.buttonPressed("rec")
                    break;
                case 1:
                    main.buttonPressed("stop")
                    break;
                case 2:
                    main.buttonPressed("stream")
                    break;
                case 3:
                    main.buttonPressed("mic")
                    break;
                default:
                    break;
            }
        }
    }

    BottomButtonBar {
        id: okDialogBar

        x: parent.width - sideBar.width - height * buttonTitles.length
        y: parent.height - height
        width: height * buttonTitles.length
        height: parent.height - videoWindow.height

        buttonTitles: [
            "Ok"
        ]

        buttonIcons: [
            "../icons/ok.svg"
        ]

        onBottomButtonClicked: {
            main.activeSideBar.state = "hidden"
            main.activeBottomBar.state = "hidden"
            main.activeSideBar = sideBar
            main.activeBottomBar = bottomBar
            bottomBar.state = "visible"
            sideBar.state = "visible"
            slider.visible = false
        }
    }

    BottomButtonBar {
        id: scrollableDialogBar

        x: parent.width - sideBar.width - height * buttonTitles.length
        y: parent.height - height
        width: height * buttonTitles.length
        height: parent.height - videoWindow.height

        buttonTitles: [
            "Up",
            "Down",
            "Ok"
        ]

        buttonIcons: [
            "../icons/up.svg",
            "../icons/down.svg",
            "../icons/ok.svg"
        ]

        onBottomButtonClicked: {
            switch(buttonID) {
                case 0: // up
                    main.activeSideBar.contentY -= parent.height / 5
                    if (main.activeSideBar.contentY < 0) {
                        main.activeSideBar.contentY = 0
                    }
                    break;
                case 1: // down
                    main.activeSideBar.contentY += parent.height / 5
                    if (main.activeSideBar.contentY > parent.height / 5 * main.activeSideBar.buttonTitles.length - parent.height) {
                        main.activeSideBar.contentY = parent.height / 5 * main.activeSideBar.buttonTitles.length - parent.height
                    }
                    break;
                case 2: // ok
                    main.activeSideBar.state = "hidden"
                    main.activeBottomBar.state = "hidden"
                    main.activeSideBar = sideBar
                    main.activeBottomBar = bottomBar
                    bottomBar.state = "visible"
                    sideBar.state = "visible"
                    slider.visible = false
                    break;
                default:
                    break;
            }
        }
    }

    ISOOverlay {
        id: iso
        objectName: "iso"
        width: sideBar.width

        onSetISO: {
            if (value == 0) {
                main.setValue("image", "iso", "auto")
            } else {
                main.setValue("image", "iso", value.toString())
            }
        }
    }

    EVOverlay {
        id: ev
        objectName: "ev"
        width: sideBar.width

        onSetEV: {
            main.setValue("image", "ev", value.toString())
        }
    }

    WBOverlay {
        id: wb
        objectName: "wb"
        width: sideBar.width

        onSetWB: {
            main.setValue("image", "wb", value.toLowerCase())
        }
    }

    ImageOverlay {
        id: image
        objectName: "image"
        width: sideBar.width

        onSetValue: {
            main.setValue("image", key, value.toString())
        }

        onStateChanged: {
            image.slider = main.slider
            currentValues = main.modelData.image
            ranges = main.modelData.image._ranges
        }
    }

    IconSlider {
        id: slider
        x: 0
        y: parent.height - height
        width: parent.width - main.activeBottomBar.width - sideBar.width
        height: parent.height - videoWindow.height
        visible: false
        onVisibleChanged: {
            histogram.visible = !slider.visible
            vuMeter.visible = !slider.visible
        }
    }

    Histogram {
        id: histogram
        x: vuMeter.x + vuMeter.width
        y: parent.height - height
        width: 160
        height: parent.height - videoWindow.height
        visible: true
    }

    VUMeter {
        id: vuMeter
        x: 0
        y: parent.height - height
        height: parent.height - videoWindow.height
        width: 250
        visible: true
    }

    Timer {
        id: timer
        function setTimeout(cb, delayTime) {
            timer.interval = delayTime;
            timer.repeat = false;
            timer.triggered.connect(cb);
            timer.triggered.connect(function release () {
                timer.triggered.disconnect(cb); // This is important
                timer.triggered.disconnect(release); // This is important as well
            });
            timer.start();
        }
    }

    function updateState(area, key, value) {
        main.modelData[area][key] = value
    }

    Component.onCompleted: {
        // Delay starting of video preview a bit as the event handler may not be attached
        // at load time yet
        timer.setTimeout(function() {
            main.startVideo()
            bottomBar.state = 'visible'
            sideBar.state = 'visible'
        }, 500)

        main.setValue.connect(updateState)
    }
}
