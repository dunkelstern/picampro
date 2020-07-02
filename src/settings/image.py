from typing import Dict, Tuple, Union, List

from .proto import SettingsProto
from pipeline import Pipeline


class ImageSettings(SettingsProto):
    WHITEBALANCES: Dict[str, int] = {
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

    ISOS: Dict[str, int] = {
        'auto': 0,
        '100': 100,
        '200': 200,
        '400': 400,
        '800': 800,
        '1600': 1600,
        '3200': 3200
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

    @classmethod
    def value_ranges(cls) -> Dict[str, Union[Tuple[float, float], List[str]]]:
        return {
            'iso':           list(ImageSettings.ISOS.keys()),
            'ev':            ( -10.0,  10.0),
            'wb':            list(ImageSettings.WHITEBALANCES.keys()),
            'sharpness':     (-100.0, 100.0),
            'contrast':      (-100.0, 100.0),
            'brightness':    (   0.0, 100.0),
            'saturation':    (-100.0, 100.0),
            'awb_gain_red':  (   0.0,   8.0),
            'awb_gain_blue': (   0.0,   8.0),
            'drc':           (   0.0,   3.0)
        }

    def validate(self):
        for attr, rng in ImageSettings.value_ranges().items():
            value = getattr(self, attr)
            if isinstance(rng, tuple):
                rng_min, rng_max = rng
                if value > rng_max or value < rng_min:
                    raise ValueError('Attribute {} out of range: {} < {} < {}'.format(attr, rng_min, value, rng_max))
            elif isinstance(rng, list):
                if value not in rng:
                    raise ValueError('Attribute {} has invalid value {}, possible: {}'.format(attr, value, ', '.join(rng)))
        return super().validate()
    
    def parse(self, key: str, value: str):
        if key == 'image:iso':
            self.iso = value
        elif key == 'image:ev':
            self.ev = int(value)
        elif key == 'image:wb':
            self.wb = value
        elif key == 'image:sharpness':
            self.sharpness = int(value)
        elif key == 'image:contrast':
            self.contrast = int(value)
        elif key == 'image:brightness':
            self.brightness = int(value)
        elif key == 'image:saturation':
            self.saturation = int(value)
        elif key == 'image:awb_gain_red':
            self.awb_gain_red = int(value)
        elif key == 'image:awb_gain_blue':
            self.awb_gain_blue = int(value)
        elif key == 'image:drc':
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