from .proto import SettingsProto
from pipeline import Pipeline


class BaseSettings(SettingsProto):
    RESOLUTIONS = [
        '1920x1080',
        '1280x720',
        '1280x960',
        '640x360',
        '640x480'
    ]

    FPS = {
        '1920x1080': [            30, 25, 24, 15, 12, 10, 5, 2, 1],
        '1280x720':  [        40, 30, 25, 24, 15, 12, 10, 5, 2, 1],
        '1280x960':  [        40, 30, 25, 24, 15, 12, 10, 5, 2, 1],
        '640x360':   [90, 60, 40, 30, 25, 24, 15, 12, 10, 5, 2, 1],
        '640x480':   [90, 60, 40, 30, 25, 24, 15, 12, 10, 5, 2, 1],
    }

    ORIENTATIONS = {
        'normal': 0,
        '90r': 1,
        '180': 2,
        '90l': 3,
        'hflip': 4,
        'vflip': 5,
        'ul-lr': 6,
        'ur-ll': 7,
    }

    resolution = '1920x1080'
    fps = 30
    orientation = 'normal'

    def validate(self):
        if self.__class__.__name__ not in self.dirty_values:
            return super().validate()

        if 'fps' in self.dirty_values[self.__class__.__name__] or 'resolution' in self.dirty_values[self.__class__.__name__]:
            # check if the selected resolution can do the fps
            if self.resolution not in BaseSettings.RESOLUTIONS:
                raise ValueError(
                    "Unsupported resolution {}, valid are {}".format(
                        self.resolution,
                        ", ".join(BaseSettings.RESOLUTIONS)
                    )
                )
            if self.fps not in BaseSettings.FPS[self.resolution]:
                raise ValueError(
                    "Unsupported fps {} for resolution {}, valid are {}".format(
                        self.fps,
                        self.resolution,
                        ', '.join(BaseSettings.FPS[self.resolution])
                    )
                )

        self.dirty_values[self.__class__.__name__]
        return super().validate()

    def parse(self, key: str, value: str):
        if key == 'basic:resolution':
            self.resolution = value
        elif key == 'basic:fps':
            self.fps = int(value)
        elif key == 'basic:orientation':
            self.orientation = value
        super().parse(key, value)
    
    def can_apply_live(self):
        # Base settings always stop the pipeline if any parameter changes
        if len(self.state_changes(BaseSettings)) == 0:
            return super.can_apply_live()
        return False
        
    def apply(self, gst_state: Pipeline):
        w, h = self.resolution.split('x')

        # only kill the pipeline if we actually have changes
        if len(self.state_changes(BaseSettings)) == 0:
            super().apply(gst_state)
            return
        
        self.store_state(BaseSettings)

        with gst_state.offline_edit() as (handle, Gst):
            handle.video_caps = Gst.Caps.from_string(
                "video/x-h264, width={w}, height={h}, framerate={fps}/1,profile=high".format(
                    w=w, h=h, fps=self.fps
                )
            )
            handle.video_caps_filter.set_property("caps", handle.video_caps)
            handle.video_source.set_property('video-direction', BaseSettings.ORIENTATIONS[self.orientation])
        super().apply(gst_state)