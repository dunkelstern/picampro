from typing import TYPE_CHECKING
from contextlib import contextmanager

import sys

import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject

if TYPE_CHECKING:
    from settings import Settings

Gst.init(None)


class Pipeline:
    
    pipeline = None
    video_source = None
    video_caps = None
    video_caps_filter = None
    video_queue = None
    audio_source = None       # TODO: audio source
    audio_caps = None         # TODO: audio caps
    audio_caps_filter = None  # TODO: audio caps filter
    h264_parser = None
    muxer = None              # TODO: muxer
    video_sink = None
    audio_sink = None         # TODO: audio sink
    bus = None

    def __init__(self, settings: 'Settings'):
        self.settings = settings
        self.re_init()

    def re_init(self):
        # Set up the gstreamer pipeline
        self.pipeline = Gst.Pipeline.new("pipeline")

        # video
        self.video_source = Gst.ElementFactory.make("rpicamsrc", "videosource")

        self.video_caps = Gst.Caps.from_string("video/x-h264, width=1920, height=1080, framerate=30/1,profile=high")
        self.video_caps_filter = Gst.ElementFactory.make("capsfilter", "filter")
        self.video_caps_filter.set_property("caps", self.video_caps)
        self.video_queue = Gst.ElementFactory.make("queue", "videoqueue")
        self.h264_parser = Gst.ElementFactory.make("h264parse", "videoparse")
        self.video_sink = Gst.ElementFactory.make("fakesink", "videosink") # FIXME: only fakesink

        self.video_source.set_property("preview", 1)
        #video_source.set_property("rotation", 180)
        self.video_source.set_property("fullscreen", 0)
        self.video_source.set_property("preview-x", 0)
        self.video_source.set_property("preview-y", 0)
        self.video_source.set_property("preview-w", 904)  # FIXME: make dependend on screen size
        self.video_source.set_property("preview-h", 508)  # FIXME: make dependend on screen size
        self.video_source.set_property("inline-headers", 1)
        #video_source.set_property("bitrate", 150000)

        self.video_queue.set_property('max-size-bytes', 0)
        self.video_queue.set_property('max-size-buffers', 0)

        # TODO: audio

        if not self.pipeline or not self.video_source or not self.video_caps or not self.video_caps_filter or not self.h264_parser or not self.video_sink: 
            print("ERROR: Not all gstreamer elements could be created") 
            sys.exit(1)
        
        # assemble pipeline
        self.pipeline.add(self.video_source, self.video_caps_filter, self.video_queue, self.h264_parser, self.video_sink)
        self.video_source.link(self.video_caps_filter)
        self.video_caps_filter.link(self.video_queue)
        self.video_queue.link(self.h264_parser)
        self.h264_parser.link(self.video_sink)
        
        self.bus = self.pipeline.get_bus()
        self.bus.add_signal_watch()
        self.bus.enable_sync_message_emission()
        self.bus.connect("message", self._on_message)
        self.bus.connect("sync-message::element", self._on_sync_message)

        self.settings.apply(self)

    def preview(self):
        """
        Start the video preview, calling this while recording or streaming will
        switch to preview mode only and stop the encoder
        """
        # FIXME: add fake sink when starting preview and disconnect recorders and streamers
        if self.pipeline is None:
            self.re_init()
        self.pipeline.set_state(Gst.State.PLAYING)
    
    def start_recording(self):
        """
        Start recording to disk, keeps the preview and streaming running
        """
        # TODO: start recording
        pass
    
    def start_streaming(self):
        """
        Start streaming to a streaming server, keeps preview and recording running
        """
        # TODO: start streaming
        pass

    def stop(self):
        """
        Stop the pipeline.
        This will disable the preview
        """
        self.pipeline.set_state(Gst.State.NULL)
        self.pipeline = None
        self.settings.remove_state()

    @contextmanager
    def offline_edit(self):
        """
        This is the context manager to change things on the pipeline that can not be done
        while the pipeline is running. On entering it saves the pipeline state and stops the
        pipeline. Then it calls the context with two parameters:
        - ``self``, reference to the pipeline
        - ``Gst``, reference to the GStreamer module (so you do not have to re-import it)

        On exiting the context the pipeline state is restored to the state it was in before.
        """
        changing, state, pending = self.pipeline.get_state(1000)
        self.pipeline.set_state(Gst.State.NULL)
        try:
            yield (self, Gst)
        finally:
            self.pipeline.set_state(state)

    def _on_message(self, bus, message):
        """
        GStreamer message handler
        """
        t = message.type
        if t == Gst.MessageType.EOS:
            self.pipeline.set_state(Gst.State.NULL)
        elif t == Gst.MessageType.ERROR:
            err, debug = message.parse_error()
            print("Error: %s" % err, debug)
            self.pipeline.set_state(Gst.State.NULL)

    def _on_sync_message(self, bus, message):
        """
        Gstreamer sync message handler
        """
        struct = message.get_structure()
        if not struct:
            return
        message_name = struct.get_name()
        # if message_name == "prepare-xwindow-id":
        #     # Assign the viewport
        #     imagesink = message.src
        #     imagesink.set_property("force-aspect-ratio", True)
        #     imagesink.set_xwindow_id(self.movie_window.window.xid)