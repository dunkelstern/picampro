
# Inverts a grayscale image in place, requires numpy.
#
# gst-launch-1.0 videotestsrc ! ExampleTransform ! videoconvert ! xvimagesink

import gi
gi.require_version('Gst', '1.0')
gi.require_version('GstBase', '1.0')
gi.require_version('GstVideo', '1.0')

from gi.repository import Gst, GObject, GstBase, GstVideo

Gst.init(None)
FIXED_CAPS = Gst.Caps.from_string('ANY')

class PTSRetime(GstBase.BaseTransform):
    __gstmetadata__ = ('Buffer re-timer','Transform',
                      'Overwrites the presentation timestamps of a buffer, one buffer needs to be one frame', 'Johannes Schriewer')

    __gsttemplates__ = (Gst.PadTemplate.new("src",
                                           Gst.PadDirection.SRC,
                                           Gst.PadPresence.ALWAYS,
                                           FIXED_CAPS),
                       Gst.PadTemplate.new("sink",
                                           Gst.PadDirection.SINK,
                                           Gst.PadPresence.ALWAYS,
                                           FIXED_CAPS))

    def do_set_caps(self, incaps, outcaps):
        struct = incaps.get_structure(0)
        self.fps = struct.get_float("fps").value
        print(fps)
        return True

    def do_transform_ip(self, buf):
        try:
            with buf.map(Gst.MapFlags.READ | Gst.MapFlags.WRITE) as info:
                print(info)
                return Gst.FlowReturn.OK
        except Gst.MapError as e:
            Gst.error("Mapping error: %s" % e)
            return Gst.FlowReturn.ERROR

GObject.type_register(PTSRetime)
__gstelementfactory__ = ("pts_retime", Gst.Rank.NONE, PTSRetime)