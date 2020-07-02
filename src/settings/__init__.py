import sys
from PySide2.QtCore import QSettings

from .proto import SettingsProto
from .advanced import AdvancedSettings
from .image import ImageSettings
from .encoder import EncoderSettings
from .streaming import StreamingSettings
from .recording import RecordingSettings
from .audio import AudioSettings


class Settings(AdvancedSettings, ImageSettings, EncoderSettings, StreamingSettings, RecordingSettings, AudioSettings):
   
    def __init__(self):
        super().__init__()
        organization = "de.dunkelstern" if sys.platform.startswith('darwin') else "dunkelstern"
        self.settings_instance = QSettings(organization, "PiCamPro")
        self.load()
    
    def save(self) -> None:
        """
        Save the settings to permanent storage
        """
        self.validate()

        for key, value in self.__dict__.items():
            if key.startswith('_') or callable(value) or key in ('settings_instance', 'dirty_values', 'value_ranges'):
                continue
            section = 'unknown'
            for klass in self.__class__.__mro__:
                if issubclass(klass, SettingsProto):
                    if key in klass.__dict__:
                        section = klass.__name__.replace('Settings', '').lower()
            self.settings_instance.setValue('{}/{}'.format(section, key), value)
    
    def load(self) -> None:
        """
        Load settings from permanent storage, usually will be performed on
        initialization.
        """
        for key in self.settings_instance.allKeys():
            value = self.settings_instance.value(key)
            klass, prop = key.split('/')
            klass = klass.title() + 'Settings'
            for c in Settings.__mro__:
                if c.__name__ == klass:
                    klass = c
                    break
            if klass.__dict__[prop] is True or klass.__dict__[prop] is False:
                value = bool(value)
            elif isinstance(klass.__dict__[prop], int):
                value = int(value)
            setattr(self, prop, value)
        self.dirty_values = {}
