# This Python file uses the following encoding: utf-8
import sys
import os

from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine

import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject

# gst-launch-1.0 rpicamsrc preview=1 inline-headers=1 bitrate=1500000 ! 'video/x-h264, width=1920, height=1080, framerate=30/1,profile=high' ! h264parse ! tcpserversink host=0.0.0.0 port=8000

player = None

def on_message(bus, message):
    t = message.type
    if t == Gst.MessageType.EOS:
        player.set_state(Gst.State.NULL)
    elif t == Gst.MessageType.ERROR:
        err, debug = message.parse_error()
        print("Error: %s" % err, debug)
        player.set_state(Gst.State.NULL)

def on_sync_message(bus, message):
    struct = message.get_structure()
    if not struct:
        return
    message_name = struct.get_name()
    # if message_name == "prepare-xwindow-id":
    #     # Assign the viewport
    #     imagesink = message.src
    #     imagesink.set_property("force-aspect-ratio", True)
    #     imagesink.set_xwindow_id(self.movie_window.window.xid)

if __name__ == "__main__":
    Gst.init(None)

    # Set up the gstreamer pipeline
    player = Gst.parse_launch("rpicamsrc preview=1 rotation=180 fullscreen=0 preview-x=0 preview-y=0 preview-w=904 preview-h=508 inline-headers=1 bitrate=150000 ! video/x-h264, width=1920, height=1080, framerate=30/1,profile=high ! h264parse ! fakesink")
    bus = player.get_bus()
    bus.add_signal_watch()
    bus.enable_sync_message_emission()
    bus.connect("message", on_message)
    bus.connect("sync-message::element", on_sync_message)
    player.set_state(Gst.State.PLAYING)

    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    engine.load(os.path.join(os.path.dirname(__file__), "../resources/qml/main.qml"))

    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec_())
