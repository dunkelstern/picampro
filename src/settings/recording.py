from .proto import SettingsProto
from pipeline import Pipeline


class RecordingSettings(SettingsProto):

    def validate(self):
        return super().validate()
    
    def parse(self, key: str, value: str):
        if key == 'recording:location':
            # TODO: implement recording location change
            pass
        elif key == 'recording:split':
            # TODO: implement recording filesplitting change
            pass
        elif key == 'recording:split-size':
            # TODO: implement recording split size change
            pass
        super().parse(key, value)
    
    def can_apply_live(self):
        return super().can_apply_live()
        
    def apply(self, gst_state: Pipeline):
        super().apply(gst_state)