from typing import List, Dict, Any, Tuple, Union

from pipeline import Pipeline


class SettingsProto:
    dirty_values = {}
    _state = {}

    def __init__(self):
        super().__init__()
        for klass in self.__class__.__mro__:
            if issubclass(klass, SettingsProto):
                for key, value in klass.__dict__.items():
                    if key.startswith('_') or callable(value) or key == key.upper():
                        continue
                    setattr(self, key, value)
        self.dirty_values = {}

    def __setattr__(self, attr, value):
        """
        This has been overridden to allow marking changed values as dirty so
        in case we call ``validate()`` we do not have to check everything
        """
        if self.__class__.__name__ not in self.dirty_values:
            self.dirty_values[self.__class__.__name__] = set()
        self.dirty_values[self.__class__.__name__].add(attr)
        super().__setattr__(attr, value)

    def store_state(self, cls) -> None:
        """
        Store a snapshot of the current state of instance variables to avoid re-setting
        values that have not been changed between calls to ``apply()``

        :param class cls: The sub-class to query
        """
        self._state[cls.__name__] = {}
        for key, value in cls.__dict__.items():
            if key.startswith('_') or callable(value) or key == key.upper():
                continue
            self._state[cls.__name__][key] = self.__dict__[key]

    def remove_state(self) -> None:
        """
        Remove all stored state, used when the pipeline has to be restarted so we get all
        settings again
        """
        self._state = {}

    def state_changes(self, cls) -> List[str]:
        """
        Return a list of changed instance variables since last call to ``store_state()``

        :param class cls: The sub-class to query
        :returns: List of changed parameters
        """
        result: List[str] = []
        if cls.__name__ not in self._state:
            self._state[cls.__name__] = {}
        for key, value in cls.__dict__.items():
            if key.startswith('_') or callable(value) or key == key.upper():
                continue
            if key not in self._state[cls.__name__]:
                result.append(key)
                continue
            if self._state[cls.__name__][key] != self.__dict__[key]:
                result.append(key)
        return result

    def serialize(self) -> Dict[str, Any]:
        """
        Serialize settings into a dict.

        This is used primarily to send the settings over to the UI

        :returns: Dictionary with all settings serialized
        """
        result: Dict[str, Dict[str, Any]] = {}
        for key, value in self.__dict__.items():
            if key.startswith('_') or callable(value) or key == key.upper() or key in ('settings_instance', 'dirty_values', 'value_ranges'):
                continue
            classes = list(self.__class__.__mro__)
            classes.reverse()
            for c in classes:
                if c.__name__ in ('Settings', 'object', 'SettingsProto'):
                    continue
                if hasattr(c, key):
                    cls = c.__name__.replace('Settings', '').lower()
                    rng = c.value_ranges()
                    break;
            if cls == 'proto':
                continue
            if cls not in result:
                result[cls] = {}
                for rng_key, rng_value in rng.items():
                    if isinstance(rng_value, tuple):
                        rng[rng_key] = list(rng_value)
                result[cls]['_ranges'] = rng
            print(cls, key, self.__dict__[key])
            result[cls][key] = self.__dict__[key]
        return result

    @classmethod
    def value_ranges(cls) -> Dict[str, Union[Tuple[float, float], List[str]]]:
        """
        Returns the allowed ranges for each attribute that has to be
        range-checked.
        """
        return {}

    def validate(self) -> bool:
        """
        Validate the parameters set. Returns true if everything is alright and
        throws ``ValueError`` exceptions if a parameter mismatch has been detected.

        Attention: always call ``super().validate()`` !
        """
        return True
    
    def parse(self, key: str, value: str) -> None:
        """
        Parse a parameter update from the QML layer

        Attention: always call ``super().parse(key, value)`` !
        """
        pass
    
    def can_apply_live(self) -> bool:
        """
        Returns if the changed parameters can be changed while the pipeline is running.
        Used to query parameter changes while streaming or recording to avoid stopping
        the pipeline by accident.

        :returns: ``True`` if the settings can be applied without stopping the pipeline
        """
        return True
        
    def apply(self, gst_state: Pipeline) -> None:
        """
        Apply changed parameters to the pipeline. The pipeline state will be restored
        if it has to be stopped temporarily to change settings.

        :param Pipeline gst_state: the gstreamer management class to apply parameters to
        """
        pass