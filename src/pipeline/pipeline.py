from typing import TYPE_CHECKING
from contextlib import contextmanager

import sys

from PySide2.QtCore import QTimer
from rpi_display_histogram import ScreenHistogram

import gi
gi.require_version('Gst', '1.0')
gi.require_version('GstBase', '1.0')

from gi.repository import Gst, GObject, GstBase

if TYPE_CHECKING:
    from settings import Settings

Gst.init(None)


class Pipeline:
    audio_source = None       # TODO: audio source
    audio_caps = None         # TODO: audio caps
    audio_caps_filter = None  # TODO: audio caps filter
    muxer = None              # TODO: muxer
    audio_sink = None         # TODO: audio sink

    def __init__(self, settings: 'Settings'):
        self.settings = settings
        self.histogram_timer = None
        self.histogram = None
        self.histogram_update_callback = None
        self.vu_update_callback = None
        self.vuLeft = 0
        self.peakLeft = 0
        self.vuRight = 0
        self.peakRight = 0
        self.re_init()

    def re_init(self):
        pipeline_items = []

        # Set up the gstreamer pipeline
        self.pipeline = Gst.Pipeline.new("pipeline")

        # video
        self.video_source = Gst.ElementFactory.make("rpicamsrc", "videosource")
        pipeline_items.append(self.video_source)

        self.video_caps = Gst.Caps.from_string("video/x-h264, width=1920, height=1080, framerate=30/1,profile=high")
        pipeline_items.append(self.video_caps)

        self.video_caps_filter = Gst.ElementFactory.make("capsfilter", "filter")
        pipeline_items.append(self.video_caps_filter)

        self.h264_parser = Gst.ElementFactory.make("h264parse", "videoparse")
        pipeline_items.append(self.h264_parser)

        self.video_tee  = Gst.ElementFactory.make('tee', 'video_tee')
        pipeline_items.append(self.video_tee)

        self.video_fake_queue = Gst.ElementFactory.make("queue", "videoqueue")
        pipeline_items.append(self.video_fake_queue)

        self.video_fake_sink = Gst.ElementFactory.make("fakesink", "videofakesink")
        pipeline_items.append(self.video_fake_sink)

        if None in pipeline_items:
            print("ERROR: Not all gstreamer elements could be created")
            sys.exit(1)

        # TODO: add queue -> flvmux -> rtmpsink
        # TODO: add queue -> matroskamux -> filesink

        # Set video caps (frame size, etc.)
        self.video_caps_filter.set_property("caps", self.video_caps)

        # Video source properties
        self.video_source.set_property("preview", 1)
        self.video_source.set_property("fullscreen", 0)
        self.video_source.set_property("preview-x", 0)
        self.video_source.set_property("preview-y", 0)
        self.video_source.set_property("preview-w", 904)  # FIXME: make dependend on screen size
        self.video_source.set_property("preview-h", 508)  # FIXME: make dependend on screen size
        self.video_source.set_property("inline-headers", 1)

        # Make sure the video pipeline always runs sync
        self.video_fake_sink.set_property('sync', True)

        # TODO: audio
        # Encoder: voaacenc
        # Audio levels: level

        # assemble pipeline
        self.pipeline.add(
            self.video_source,
            self.video_caps_filter,
            self.h264_parser,
            self.video_tee,
            self.video_fake_queue,
            self.video_fake_sink
        )
        self.video_source.link(self.video_caps_filter)
        self.video_caps_filter.link(self.h264_parser)
        self.h264_parser.link(self.video_tee)

        # Tee has dynamic pads, so request one for the fake sink
        self.video_src_pad_template = Gst.PadTemplate.new_with_gtype(
            "src_%u",
            Gst.PadDirection.SRC,
            Gst.PadPresence.REQUEST,
            Gst.Caps.from_string('video/x-h264'),
            GstBase.AggregatorPad.__gtype__
        )
        fake_video_src_pad = self.video_tee.request_pad(self.video_src_pad_template)
        fake_queue_sink_pad = self.video_fake_sink.get_static_pad('sink')
        fake_video_src_pad.link(fake_queue_sink_pad)
        self.video_fake_sink.link(self.video_fake_queue)

        # get the bus and connect signals
        self.bus = self.pipeline.get_bus()
        self.bus.add_signal_watch()
        self.bus.enable_sync_message_emission()
        self.bus.connect("message", self._on_message)
        self.bus.connect("sync-message::element", self._on_sync_message)

        # now apply all settings to the stream
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

        if self.histogram_timer:
            self.histogram_timer.start()
        else:
            self.histogram_timer = QTimer()
            self.histogram_timer.timeout.connect(self.update_histogram)
            self.histogram_timer.start(100)


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
        if self.histogram_timer:
            self.histogram_timer.stop()

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

    def update_histogram(self):
        if self.histogram is None:
            self.histogram = ScreenHistogram()
            self.histogram.scaled_width = int(self.histogram.screen_width / 6)
            self.histogram.scaled_height = int(self.histogram.screen_height / 6)
            self.histogram.roi = (0, 0, int(904 / 6) - 1, int(508 / 6) - 1)  # FIXME: make dependent on screen size
        self.histogram.capture()
        data = self.histogram.fast_luminance_histogram(num_bins=32)
        if self.histogram_update_callback and callable(self.histogram_update_callback):
            self.histogram_update_callback(data)
        if self.vu_update_callback and callable(self.vu_update_callback):
            self.vu_update_callback([self.vuLeft / 100.0, self.peakLeft / 100.0, self.vuRight / 100.0, self.peakRight / 100.0])


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
