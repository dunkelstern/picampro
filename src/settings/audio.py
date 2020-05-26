from .proto import SettingsProto
from pipeline import Pipeline


class AudioSettings(SettingsProto):

    def validate(self):
        return super().validate()
    
    def parse(self, key: str, value: str):
        if key == 'audio:enabled':
            # TODO: implement audio enabled change
            pass
        elif key == 'audio:codec':
            # TODO: implement audio codec change
            pass
        elif key == 'audio:bitrate':
            # TODO: implement audio bitrate change
            pass
        elif key == 'audio:channels':
            # TODO: implement audio channels change
            pass
        super().parse(key, value)
    
    def can_apply_live(self):
        return super().can_apply_live()
        
    def apply(self, gst_state: Pipeline):
        super().apply(gst_state)