# This Python file uses the following encoding: utf-8
import sys
import os

from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine
from PySide2.QtCore import Slot

import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject

# gst-launch-1.0 rpicamsrc preview=1 inline-headers=1 bitrate=1500000 ! 'video/x-h264, width=1920, height=1080, framerate=30/1,profile=high' ! h264parse ! tcpserversink host=0.0.0.0 port=8000

pipeline = None
video_source = None
h264_parser = None
video_sink = None

def on_message(bus, message):
    t = message.type
    if t == Gst.MessageType.EOS:
        pipeline.set_state(Gst.State.NULL)
    elif t == Gst.MessageType.ERROR:
        err, debug = message.parse_error()
        print("Error: %s" % err, debug)
        pipeline.set_state(Gst.State.NULL)

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

@Slot(str)
def button_pressed(button):
    print(button)
    if button.startswith('iso'):
        # change iso of source
        _, iso = button.split('_')
        if iso == 'auto':
            video_source.set_property('iso', 0)
        else:
            video_source.set_property('iso', int(iso))
    if button.startswith('ev'):
        # change EV compensation of source
        _, ev = button.split('_')
        video_source.set_property('exposure-compensation', int(ev))

@Slot()
def start_preview():
    print('start preview')
    pipeline.set_state(Gst.State.PLAYING)


@Slot()
def stop_preview():
    print('stop preview')
    pipeline.set_state(Gst.State.NULL)


if __name__ == "__main__":
    Gst.init(None)

    # Set up the gstreamer pipeline
    video_source = Gst.ElementFactory.make("rpicamsrc", "videosource")

    caps = Gst.Caps.from_string("video/x-h264, width=1920, height=1080, framerate=30/1,profile=high")
    caps_filter = Gst.ElementFactory.make("capsfilter", "filter")
    caps_filter.set_property("caps", caps)
    h264_parser = Gst.ElementFactory.make("h264parse", "videoparse")
    video_sink = Gst.ElementFactory.make("fakesink", "videosink")

    video_source.set_property("preview", 1)
    video_source.set_property("rotation", 180)
    video_source.set_property("fullscreen", 0)
    video_source.set_property("preview-x", 0)
    video_source.set_property("preview-y", 0)
    video_source.set_property("preview-w", 904)
    video_source.set_property("preview-h", 508)
    video_source.set_property("inline-headers", 1)
    video_source.set_property("bitrate", 150000)

    pipeline = Gst.Pipeline.new("pipeline")

    if not pipeline or not video_source or not h264_parser or not video_sink: 
        print("ERROR: Not all gstreamer elements could be created") 
        sys.exit(1)  
    
    pipeline.add(video_source, caps_filter, h264_parser, video_sink)
    video_source.link(caps_filter)
    caps_filter.link(h264_parser)
    h264_parser.link(video_sink)
    
    bus = pipeline.get_bus()
    bus.add_signal_watch()
    bus.enable_sync_message_emission()
    bus.connect("message", on_message)
    bus.connect("sync-message::element", on_sync_message)

    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    engine.load(os.path.join(os.path.dirname(__file__), "../resources/qml/Main.qml"))
    
    if not engine.rootObjects():
        sys.exit(-1)

    engine.rootObjects()[0].buttonPressed.connect(button_pressed)
    engine.rootObjects()[0].stopVideoPreview.connect(stop_preview)
    engine.rootObjects()[0].startVideoPreview.connect(start_preview)

    sys.exit(app.exec_())
