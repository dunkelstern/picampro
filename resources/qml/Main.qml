import QtQuick 2.11
import QtQuick.Window 2.11
import QtQuick.VirtualKeyboard 2.1

Window {
    id: main

    property Item activeSideBar
    property Item activeBottomBar

    signal setValue(string key, string value)
    signal stopVideoPreview()
    signal startVideoPreview()

    // FIXME: Add button titles as properties to initialize at program start

    title: qsTr("PiCamPro")
    width: 1024
    height: 600
    color: "black"
    visible: true

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
            "Shade",
            "Image",
            "Settings"
        ]

        buttonIcons: [
            "../icons/ISO.svg",
            "../icons/EV.svg",
            "../icons/wb-shade.svg",
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
                    main.stopVideoPreview()
                    // TODO: Show settings screen
                    break;        
                default:
                    break;
            }

            main.activeSideBar.state = "visible"
            main.activeBottomBar.state = "visible"
            sideBar.state = "hidden"
            bottomBar.state = "hidden"
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
                    main.setValue("rec", "true")
                    break;
                case 1:
                    main.setValue("stop", "true")
                    break;
                case 2:
                    main.setValue("stream", "true")
                    break;
                case 3:
                    main.setValue("mic", "true")
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
            "../icons/rec.svg" // FIXME: Ok icon
        ]

        onBottomButtonClicked: {
            main.activeSideBar.state = "hidden"
            main.activeBottomBar.state = "hidden"
            bottomBar.state = "visible"
            sideBar.state = "visible"
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
            "../icons/rec.svg", // FIXME: Up icon
            "../icons/rec.svg", // FIXME: Down icon
            "../icons/rec.svg"  // FIXME: Ok icon
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
                    bottomBar.state = "visible"
                    sideBar.state = "visible"
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
                main.setValue("iso", "auto")
                sideBar.buttons.itemAt(0).titleText = qsTr("Auto")
            } else {
                main.setValue("iso", value.toString())
                sideBar.buttons.itemAt(0).titleText = value.toString()
            }
        }
    }

    EVOverlay {
        id: ev
        objectName: "ev"
        width: sideBar.width

        onSetEV: {
            main.setValue("ev", value.toString())
            sideBar.buttons.itemAt(1).titleText = (value > 0 ? "+" : "") + value.toString() + ' EV'
        }
    }

    WBOverlay {
        id: wb
        objectName: "wb"
        width: sideBar.width

        onSetWB: {
            main.setValue('wb', value.toLowerCase())
            sideBar.buttons.itemAt(2).titleText = value
            sideBar.buttons.itemAt(2).iconSource = "../icons/wb-" + value.toLowerCase() + '.svg'
        }
    }

    ImageOverlay {
        id: image
        objectName: "image"
        width: sideBar.width

        onSetValue: {
            console.log(key, value)
            main.setValue(key, value.toString())
        }
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

    Component.onCompleted: {
        // Delay starting of video preview a bit as the event handler may not be attached
        // at load time yet
        timer.setTimeout(function() {
            main.startVideoPreview()
            bottomBar.state = 'visible'
            sideBar.state = 'visible'
        }, 500)
    }
}
