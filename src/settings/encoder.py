from .proto import SettingsProto
from pipeline import Pipeline


class EncoderSettings(SettingsProto):

    def validate(self):
        return super().validate()
    
    def parse(self, key: str, value: str):
        if key == 'encoder:keyframe-interval':
            # TODO: implement keyframe interval change
            pass
        elif key == 'encoder:bitrate':
            # TODO: implement bitrate change
            pass
        elif key == 'encoder:qp':
            # TODO: implement qp change
            pass
        elif key == 'encoder:preview-encoded':
            # TODO: implement encoded preview change
            pass
        super().parse(key, value)
    
    def can_apply_live(self):
        return super().can_apply_live()
        
    def apply(self, gst_state: Pipeline):
        super().apply(gst_state)