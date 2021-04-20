from abstract_mode import Mode


class PowerLvl(Mode):
    name = {
        'default': 'Leveling up one character',
        'Русский': 'Повышение персонажа',
        'English': 'Leveling up one character',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def next_duration(self):
        return self.bot.config.duration

    @property
    def next_character(self):
        return next(filter(lambda x: x.name == self.bot.config.character.lower(), self.bot.characters))
