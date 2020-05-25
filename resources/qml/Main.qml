import QtQuick 2.11
import QtQuick.Window 2.11
import QtQuick.VirtualKeyboard 2.1

Window {
    id: main

    signal buttonPressed(string buttonID)
    signal stopVideoPreview()
    signal startVideoPreview()

    title: qsTr("PiCamPro")
    width: 1024
    height: 600
    color: "black"
    visible: true

    property alias micButton: micButton
    property alias streamButton: streamButton
    property alias stopButton: stopButton
    property alias recButton: recButton
    property alias videoWindow: videoWindow

    SideButtonBar {
        id: sideBar

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

        buttonColors: [
            Constants.accentRed,
            Constants.accentYellow,
            Constants.accentGreen,
            Constants.accentBlue,
            Constants.accentViolet
        ]

        onSideButtonClicked: {
            switch (buttonID) {
                case 0:
                    // Show ISO selection overlay
                    iso.state = "visible"
                    break;
                case 1:
                    // Show EV selection overlay
                    ev.state = "visible"
                    break;
                case 2:
                    // TODO: Show WB selection overlay
                    break;
                case 3:
                    // TODO: Show image settings overlay
                    break;
                case 4:
                    // Stop Video preview
                    main.stopVideoPreview()
                    // TODO: Show settings screen
                    break;        
                default:
                    break;
            }
        }
    }

    Rectangle {
        id: videoWindow
        color: Constants.bgColor
        anchors.right: sideBar.left
        anchors.left: parent.left
        anchors.top: parent.top
        height: width / 16 * 9
    }

    BottomButton {
        id: micButton
        anchors.top: videoWindow.bottom
        anchors.right: sideBar.left
        anchors.rightMargin: 2
        anchors.bottom: parent.bottom
        width: height
        colorbarColor: Constants.accentBlue
        titleText: qsTr("Mic")
        iconSource: "../icons/mic.svg"
        onActivated: main.buttonPressed("mic")
    }

    BottomButton {
        id: streamButton
        anchors.top: videoWindow.bottom
        anchors.right: micButton.left
        anchors.rightMargin: 2
        anchors.bottom: parent.bottom
        width: height
        colorbarColor: Constants.accentGreen
        titleText: qsTr("Stream")
        iconSource: "../icons/stream.svg"
        onActivated: main.buttonPressed("stream")
    }

    BottomButton {
        id: stopButton
        anchors.top: videoWindow.bottom
        anchors.right: streamButton.left
        anchors.rightMargin: 2
        anchors.bottom: parent.bottom
        width: height
        colorbarColor: Constants.accentYellow
        titleText: qsTr("Stop")
        iconSource: "../icons/stop.svg"
        onActivated: main.buttonPressed("stop")
    }

    BottomButton {
        id: recButton
        anchors.top: videoWindow.bottom
        anchors.right: stopButton.left
        anchors.rightMargin: 2
        anchors.bottom: parent.bottom
        width: height
        colorbarColor: Constants.accentRed
        titleText: qsTr("Record")
        iconSource: "../icons/rec.svg"
        onActivated: main.buttonPressed("rec")
    }

    ISOOverlay {
        id: iso
        width: sideBar.width

        onSetISO: {
            if (value == 0) {
                main.buttonPressed("iso_auto")
                sideBar.button1.titleText = qsTr("Auto")
            } else {
                main.buttonPressed("iso_" + value.toString())
                sideBar.button1.titleText = value.toString()
            }
            iso.state = "hidden"
        }
    }

    EVOverlay {
        id: ev
        width: sideBar.width

        onSetEV: {
            main.buttonPressed("ev_" + value.toString())
            sideBar.button2.titleText = (value > 0 ? "+" : "") + value.toString() + ' EV'
            ev.state = "hidden"
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
        iso.state = 'hidden'
        ev.state = 'hidden'
        timer.setTimeout(main.startVideoPreview, 500)
    }
}
