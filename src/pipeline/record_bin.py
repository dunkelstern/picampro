import gi
gi.require_version('Gst', '1.0')
gi.require_version('GstBase', '1.0')

from gi.repository import Gst, GObject, GstBase

from .pts_retimer import PTSRetime

class RecordingBin(Gst.Bin):

    def __init__(self):
        super().__init__()
        self.pts = 0
        self.fps = None

        self.set_property("message-forward", True)

        # add queue -> matroskamux -> filesink
        pipeline_items = []

        self.video_record_queue = Gst.ElementFactory.make("queue", "recording_queue")
        pipeline_items.append(self.video_record_queue)

        self.retimer = Gst.ElementFactory.make("identity", "retimer")
        pipeline_items.append(self.retimer)

        self.video_record_mux = Gst.ElementFactory.make("matroskamux", "recording_mux")
        pipeline_items.append(self.video_record_mux)

        self.video_record_sink = Gst.ElementFactory.make("filesink", "recording_sink")
        pipeline_items.append(self.video_record_sink)
        
        self.h264_caps = Gst.Caps.from_string("video/x-h264, stream-format=avc, alignment=au")

        if None in pipeline_items:
            print("ERROR: Not all gstreamer recording elements could be created")
            return

        self.video_record_sink.set_property("sync", False)
        self.video_record_sink.set_property("location", "/home/pi/test.mkv")
        self.retimer.set_property("signal-handoffs", True)
        self.retimer.connect("handoff", self._handoff_cb, None)

        self.add(*pipeline_items)

        self.video_record_queue.link(self.retimer)
        self.retimer.link_filtered(self.video_record_mux, self.h264_caps)
        self.video_record_mux.link(self.video_record_sink)

        record_queue_sink_pad = self.video_record_queue.get_static_pad('sink')
        self.sink_pad = Gst.GhostPad.new('sink', record_queue_sink_pad)
        self.add_pad(self.sink_pad)


    def stop(self):
        Gst.Element.send_event(self.video_record_mux, Gst.Event.new_eos())

    def _handoff_cb(self, element, buffer, data):
        if self.fps is None:
            self.fps = 30  # FIXME: read from caps

        self.pts += 1.0/self.fps * 1000 * 1000 * 1000

        buffer.pts = self.pts
        buffer.duration = 1.0/self.fps * 1000 * 1000 * 1000
