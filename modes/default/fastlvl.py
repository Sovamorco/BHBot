from abstract_mode import Mode


class FastLvl(Mode):
    name = {
        'default': 'Leveling up characters closest to next level',
        'Русский': 'Повышение общего уровня',
        'English': 'Leveling up characters closest to next level',
    }
    character_selection_enabled = False
    duration_selection_enabled = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def next_duration(self):
        return self.next_character.duration_to_next_level

    @property
    def next_character(self):
        return sorted(self.bot.characters, key=lambda char: char.xp_to_next_level)[0]
