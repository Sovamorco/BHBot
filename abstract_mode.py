from abc import ABCMeta, abstractmethod
from utils import *


class Mode(metaclass=ABCMeta):
    name = None
    character_selection_enabled = True
    duration_selection_enabled = True
    parse_character_levels = True

    def __init__(self, bot):
        self.bot = bot

    @property
    @abstractmethod
    def next_character(self):
        pass

    @property
    @abstractmethod
    def next_duration(self):
        pass

    @classmethod
    def get_name(cls):
        if isinstance(cls.name, str):
            return cls.name  # Shouldn't be used, here for backwards compatibility
        elif isinstance(cls.name, dict):
            return cls.name.get(global_settings.language_name, cls.name.get('default', cls.__name__))
        return cls.__name__
