from typing import Dict, Tuple, Union, List

from .base import BaseSettings
from pipeline import Pipeline


class AdvancedSettings(BaseSettings):
    EXPOSURE_MODES = {
        'off': 0,
        'auto': 1,
        'night': 2,
        'nightpreview': 3,
        'backlight': 4,
        'spotlight': 5,
        'sports': 6,
        'snow': 7,
        'beach': 8,
        'verylong': 9,
        'fixedfps': 10,
        'antishake': 11,
        'fireworks': 12
    }

    METERING_MODES = {
        'average': 0,
        'spot': 1,
        'backlit': 2,
        'matrix': 3
    }

    stabilisation = False
    shutter_speed = 0
    exposure_mode = 'auto'
    metering_mode = 'average' 

    @classmethod
    def value_ranges(cls) -> Dict[str, Union[Tuple[float, float], List[str]]]:
        return {
            'shutter_speed': (0.0, 6000000.0),
            'exposure_mode': list(AdvancedSettings.EXPOSURE_MODES.keys()),
            'metering_mode': list(AdvancedSettings.METERING_MODES.keys())
        }

    def validate(self):
        if self.__class__.__name__ not in self.dirty_values:
            return super().validate()

        super().validate()
        if 'shutter_speed' in self.dirty_values[self.__class__.__name__]:
            if self.shutter_speed > 1.0 / self.fps * 1000000:
                raise ValueError(
                    "Shutter speed {} too big for selected fps of {}, max is {}".format(
                        self.shutter_speed,
                        self.fps,
                        1.0 / self.fps * 1000000
                    )
                )

        for attr, rng in AdvancedSettings.value_ranges().items():
            value = getattr(self, attr)
            if isinstance(rng, tuple):
                rng_min, rng_max = rng
                if value > rng_max or value < rng_min:
                    raise ValueError('Attribute {} out of range: {} < {} < {}'.format(attr, rng_min, value, rng_max))
            elif isinstance(rng, list):
                if value not in rng:
                    raise ValueError('Attribute {} has invalid value {}, possible: {}'.format(attr, value, ', '.join(rng)))

        self.dirty_values[self.__class__.__name__] = set()
        return True

    def parse(self, key: str, value: str):
        if key == 'advanced:stabilisation':
            self.stabilisation = value.upper() in ('TRUE', 'YES', 'ON', 'ENABLED', '1')
        elif key == 'advanced:shutter-speed':
            self.shutter_speed = int(value)
        elif key == 'advanced:exposure-mode':
            self.exposure_mode = value
        elif key == 'advanced:metering-mode':
            self.metering_mode = value
        super().parse(key, value)
    
    def can_apply_live(self):
        return super().can_apply_live()
        
    def apply(self, gst_state: Pipeline):
        super().apply(gst_state)
        # TODO: implement video stabilisation change
        # TODO: implement shutter speed change
        # TODO: implement exposure mode change
        # TODO: implement metering mode change
