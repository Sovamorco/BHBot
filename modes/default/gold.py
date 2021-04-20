from abstract_mode import Mode


class Gold(Mode):
    name = {
        'default': 'Gold farming',
        'Русский': 'Фарм голды',
        'English': 'Gold farming',
    }
    character_selection_enabled = False
    duration_selection_enabled = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def next_duration(self):
        return self.next_character.duration_to_next_gold

    @property
    def next_character(self):
        return sorted(self.bot.unlocked_characters, key=lambda char: char.xp_to_next_gold)[0]
