from typing import TYPE_CHECKING
from contextlib import contextmanager

from time import sleep

import sys
import random

from PySide2.QtCore import QTimer
from rpi_display_histogram import ScreenHistogram

import gi
gi.require_version('Gst', '1.0')
gi.require_version('GstBase', '1.0')

from gi.repository import Gst, GObject, GstBase

if TYPE_CHECKING:
    from settings import Settings

Gst.init(None)

from .record_bin import RecordingBin


class Pipeline:
    audio_source = None       # TODO: audio source
    audio_caps = None         # TODO: audio caps
    audio_caps_filter = None  # TODO: audio caps filter
    muxer = None              # TODO: muxer
    audio_sink = None         # TODO: audio sink

    def __init__(self, settings: 'Settings'):
        self.settings = settings
        # Status
        self.recording = False
        self.streaming = False
        self.previewing = False
        self.muted = True

        # Histogram
        self.histogram_timer = None
        self.histogram = None
        self.histogram_update_callback = None

        # VU Meter
        self.vu_update_callback = None
        self.vuLeft = 0
        self.peakLeft = 0
        self.vuRight = 0
        self.peakRight = 0

        # build pipeline
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

        self.video_caps_filter = Gst.ElementFactory.make("capsfilter", "video_filter")
        pipeline_items.append(self.video_caps_filter)

        self.h264_parser = Gst.ElementFactory.make("h264parse", "videoparse")
        pipeline_items.append(self.h264_parser)

        self.h264_caps = Gst.Caps.from_string("video/x-h264, stream-format=avc, alignment=au, framerate=30/1")
        pipeline_items.append(self.h264_caps)

        self.h264_caps_filter = Gst.ElementFactory.make("capsfilter", "h264_filter")
        pipeline_items.append(self.h264_caps_filter)

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

        # Set video caps (frame size, etc.)
        self.video_caps_filter.set_property("caps", self.video_caps)
        self.h264_caps_filter.set_property("caps", self.h264_caps)

        # Video source properties
        self.video_source.set_property("preview", 1)
        self.previewing = True
        self.video_source.set_property("fullscreen", 0)
        self.video_source.set_property("preview-x", 0)
        self.video_source.set_property("preview-y", 0)
        self.video_source.set_property("preview-w", 904)  # FIXME: make dependend on screen size
        self.video_source.set_property("preview-h", 508)  # FIXME: make dependend on screen size
        self.video_source.set_property("inline-headers", 1)
        self.video_source.set_property("use-stc", True)
        self.video_source.set_property("bitrate", 10000000) # FIXME: Remove this

        # Make sure the video pipeline always runs sync
        self.video_fake_sink.set_property('sync', True)
        self.pipeline.set_property("message-forward", True)

        # TODO: audio
        # Encoder: voaacenc
        # Audio levels: level

        # assemble pipeline
        self.pipeline.add(
            self.video_source,
            self.video_caps_filter,
            self.h264_parser,
            self.h264_caps_filter,
            self.video_tee,
            self.video_fake_queue,
            self.video_fake_sink
        )
        self.video_source.link(self.video_caps_filter)
        self.video_caps_filter.link(self.h264_parser)
        self.h264_parser.link(self.h264_caps_filter)
        self.h264_caps_filter.link(self.video_tee)

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

    def start_recording(self):
        """
        Start recording to disk, keeps the preview and streaming running
        """
        if self.recording is True:
            return

        # New recording bin
        self.record_bin = RecordingBin()
        self.pipeline.add(self.record_bin)
        self.record_bin.sync_state_with_parent()

        # Tee has dynamic pads, so request one for the recording sink
        video_record_src_pad = self.video_tee.request_pad(self.video_src_pad_template)
        video_record_src_pad.link(self.record_bin.get_static_pad('sink'))

        self.recording = True


    def stop_recording(self):
        """
        Stop recording to disk
        """
        if self.recording is False:
            return
        
        self.record_bin.get_static_pad('sink').get_peer().add_probe(Gst.PadProbeType.BLOCK, self._stop_recording_cb, None)

    def _stop_recording_cb(self, pad, info, data):
        # unlink the pad
        peer = pad.get_peer()
        if peer is None:
            return Gst.PadProbeReturn.REMOVE # Already unlinked
        pad.unlink(peer)
 
        self.video_tee.release_request_pad(pad)

        # send EOS downstream
        self.record_bin.stop()

        # add event listener to destroy the dangling part of the pipeline on EOS
        return Gst.PadProbeReturn.REMOVE

    def _remove_recorder(self):
        if self.record_bin is None:
            return
        self.record_bin.set_state(Gst.State.NULL)

        self.pipeline.remove(self.record_bin)
        self.record_bin = None
        self.recording = False

    def start_streaming(self):
        """
        Start streaming to a streaming server, keeps preview and recording running
        """
        # TODO: start streaming
        pass

    def stop_streaming(self):
        """
        Stop streaming
        """
        pass

    def start_pipeline(self):
        if self.pipeline is None:
            self.re_init()

        self.pipeline.set_state(Gst.State.PLAYING)

        if self.histogram_timer:
            self.histogram_timer.start()
        else:
            self.histogram_timer = QTimer()
            self.histogram_timer.timeout.connect(self.update_histogram)
            self.histogram_timer.start(100)

    def stop_pipeline(self):
        """
        Stop the pipeline.
        This will disable the preview
        """
        if self.histogram_timer:
            self.histogram_timer.stop()

        self.stop_recording()
        self.stop_streaming()

        self.pipeline.set_state(Gst.State.NULL)
        self.pipeline = None
        self.settings.remove_state()

    def mute_audio(self):
        """
        Mute audio channels
        """
        pass

    def unmute_audio(self):
        """
        Un-Mute audio channels
        """
        pass

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
            self.vuLeft += random.randint(-15, 15)
            self.vuRight += random.randint(-15, 15)
            if self.vuLeft > 100:
                self.vuLeft = 100
            elif self.vuLeft < 0:
                self.vuLeft = 0
            if self.vuRight > 100:
                self.vuRight = 100
            elif self.vuRight < 0:
                self.vuRight = 0
            if self.vuLeft >= self.peakLeft:
                self.peakLeft = self.vuLeft
            else:
                self.peakLeft -= 2
            if self.vuRight >= self.peakRight:
                self.peakRight = self.vuRight
            else:
                self.peakRight -= 2
            self.vu_update_callback([self.vuLeft / 100.0, self.peakLeft / 100.0, self.vuRight / 100.0, self.peakRight / 100.0])


    def _on_message(self, bus, message):
        """
        GStreamer message handler
        """
        t = message.type
        # print('message', t)
        if t == Gst.MessageType.EOS:
            self.pipeline.set_state(Gst.State.NULL)
        elif t == Gst.MessageType.ERROR:
            err, debug = message.parse_error()
            print("Error: %s" % err, debug)
            self.pipeline.set_state(Gst.State.NULL)
        elif t == Gst.MessageType.ELEMENT:
            data = message.get_structure()
            if data.has_name("GstBinForwarded"):
                forwarded_message = data.get_value("message")
                if forwarded_message.type == Gst.MessageType.EOS:
                    self._remove_recorder()  # FIXME: Check if we have to remove recorder or streamer
                # print('forwarded', forwarded_message.type)

    def _on_sync_message(self, bus, message):
        """
        Gstreamer sync message handler
        """
        # print('sync message', message.type)
        struct = message.get_structure()
        if not struct:
            return
        if struct.has_name("GstBinForwarded"):
            forwarded_message = struct.get_value("message")
            # print('sync forwarded', forwarded_message.type)
        # if message_name == "prepare-xwindow-id":
        #     # Assign the viewport
        #     imagesink = message.src
        #     imagesink.set_property("force-aspect-ratio", True)
        #     imagesink.set_xwindow_id(self.movie_window.window.xid)
