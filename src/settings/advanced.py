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
        if 'exposure_mode' in self.dirty_values[self.__class__.__name__]:
            if self.exposure_mode not in AdvancedSettings.EXPOSURE_MODES:
                raise ValueError(
                    "Invalid exposure mode {}, valid are {}".format(
                        self.exposure_mode,
                        ', '.join(AdvancedSettings.EXPOSURE_MODES)
                    )
                )
        if 'metering_mode' in self.dirty_values[self.__class__.__name__]:
            if self.metering_mode not in AdvancedSettings.METERING_MODES:
                raise ValueError(
                    "Invalid metering mode {}, valid are {}".format(
                        self.metering_mode,
                        ', '.join(AdvancedSettings.METERING_MODES)
                    )
                )

        self.dirty_values[self.__class__.__name__] = {}
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
