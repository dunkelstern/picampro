from .proto import SettingsProto
from pipeline import Pipeline


class ImageSettings(SettingsProto):
    WHITEBALANCES = {
        "manual": 0,
        "auto": 1,
        "sunlight": 2,
        "cloudy": 3,
        "shade": 4,
        "tungsten": 5,
        "fluorescent": 6,
        "incandescent": 7,
        "flash": 8,
        "horizon": 9
    }

    ISOS = {
        'auto': 0,
        '100': 100,
        '200': 200,
        '400': 400,
        '800': 800
    }

    iso = 'auto'
    ev = 0
    wb = 'auto'
    sharpness = 0
    contrast = 0
    brightness = 50
    saturation = 0
    awb_gain_red = 0
    awb_gain_blue = 0
    drc = 0

    def validate(self):
        return super().validate()
    
    def parse(self, key: str, value: str):
        if key == 'iso':
            self.iso = value
        elif key == 'ev':
            self.ev = int(value)
        elif key == 'wb':
            self.wb = value
        elif key == 'sharpness':
            self.sharpness = int(value)
        elif key == 'contrast':
            self.contrast = int(value)
        elif key == 'brightness':
            self.brightness = int(value)
        elif key == 'saturation':
            self.saturation = int(value)
        elif key == 'wb red':
            self.awb_gain_red = int(value)
        elif key == 'wb blue':
            self.awb_gain_blue = int(value)
        elif key == 'drc':
            self.drc = int(value)
        super().parse(key, value)
    
    def can_apply_live(self):
        return super().can_apply_live()
        
    def apply(self, gst_state: Pipeline):
        changes = self.state_changes(ImageSettings)

        if 'iso' in changes:
            gst_state.video_source.set_property('iso', ImageSettings.ISOS[self.iso])
        if 'ev' in changes:
            gst_state.video_source.set_property('exposure-compensation', self.ev)
        if 'wb' in changes:
            gst_state.video_source.set_property('awb-mode', ImageSettings.WHITEBALANCES[self.wb])
        if 'sharpness' in changes:
            gst_state.video_source.set_property('sharpness', self.sharpness)
        if 'contrast' in changes:
            gst_state.video_source.set_property('contrast', self.contrast)
        if 'brightness' in changes:
            gst_state.video_source.set_property('brightness', self.brightness)
        if 'saturation' in changes:
            gst_state.video_source.set_property('saturation', self.saturation)
        if 'awb_gain_red' in changes:
            gst_state.video_source.set_property('awb-gain-red', self.awb_gain_red)
        if 'awb_gain_blue' in changes:
            gst_state.video_source.set_property('awb-gain-blue', self.awb_gain_blue)
        if 'drc' in changes:
            gst_state.video_source.set_property('drc', self.drc)

        self.store_state(ImageSettings)
        super().apply(gst_state)