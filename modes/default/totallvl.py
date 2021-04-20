from abstract_mode import Mode


class TotalLvl(Mode):
    name = {
        'default': 'Leveling up characters with lowest level',
        'Русский': 'Повышение низкоуровневых персонажей',
        'English': 'Leveling up characters with lowest level',
    }
    character_selection_enabled = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def next_duration(self):
        return self.bot.config.duration

    @property
    def next_character(self):
        return sorted(self.bot.characters, key=lambda char: char.total_xp)[0]
