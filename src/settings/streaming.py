from .proto import SettingsProto
from pipeline import Pipeline


class StreamingSettings(SettingsProto):

    def validate(self):
        return super().validate()
    
    def parse(self, key: str, value: str):
        if key == 'streaming:protocol':
            # TODO: implement streaming protocol change
            pass
        elif key == 'streaming:target':
            # TODO: implement streaming target change
            pass
        elif key == 'streaming:key':
            # TODO: implement stream key change
            pass
        super().parse(key, value)
    
    def can_apply_live(self):
        return super().can_apply_live()
        
    def apply(self, gst_state: Pipeline):
        super().apply(gst_state)