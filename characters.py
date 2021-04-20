from levels import *

character_matrix = [
    ['bödvar', 'cassidy', 'orion', 'lord vraxx', 'gnash', 'queen nai', 'hattori', 'sir roland', 'scarlet', 'thatch', 'ada', 'sentinel', 'lucien', 'teros'],
    ['brynn', 'asuri', 'barraza', 'ember', 'azoth', 'koji', 'ulgrim', 'diana', 'jhala', 'kor', 'wu shang', 'val', 'ragnir', 'cross'],
    ['mirage', 'nix', 'mordex', 'yumiko', 'artemis', 'caspian', 'sidra', 'xull', 'kaya', 'isaiah', 'jiro', 'lin fei', 'zariel', 'rayman'],
    ['dusk', 'fait', 'thor', 'petra', 'vector', 'volkov', 'onyx', 'jaeyun', 'mako', 'magyar', 'reno', 'random']
]

flat_characters = sum(character_matrix, [])

no_random = flat_characters[:-1]
level_character_matrix = list([no_random[i:i+14] for i in range(0, len(no_random), 14)])


def find_char(name):
    for i, row in enumerate(character_matrix):
        try:
            return i + 1, row.index(name) + 1
        except ValueError:
            pass


def map_to_char(row, col):
    return ['down'] * (row - 1) + ['right'] * (col - 1)


def parse_pos(inp):
    try:
        pos = tuple(map(int, inp.split()))
    except ValueError:
        pos = find_char(inp.lower())
    if not pos:
        return None
    return map_to_char(*pos)


class Character:
    def __init__(self, name, level=0, xp=0):
        self.name = name
        self.level = level
        self.xp = xp

    def add_xp(self, xp):
        gold = 0
        self.xp += xp
        if self.level:
            while self.xp > levels_xp[self.level]:
                self.xp -= levels_xp[self.level]
                self.level += 1
                if self.level in gold_levels:
                    gold += 120
        return gold

    def get_xp_to_level(self, level):
        return max(sum((levels_xp[level]) for level in range(self.level, level)) - self.xp, 1)

    @property
    def xp_to_next_level(self):
        return self.get_xp_to_level(self.level + 1)

    @property
    def total_xp(self):
        return sum(levels_xp[i] for i in range(self.level)) + self.xp

    @property
    def next_gold_level(self):
        for i in range(self.level + 1, 101):
            if i in gold_levels:
                return i
        return 100

    @property
    def xp_to_next_gold(self):
        return self.get_xp_to_level(self.next_gold_level)

    def get_path_to(self, name):
        orow, opos = find_char(self.name)
        trow, tpos = find_char(name)
        if orow == 4:
            return (trow - orow) * ['down'] + (orow - trow) * ['up'] + (tpos - opos) * ['right'] + (opos - tpos) * ['left']
        return (tpos - opos) * ['right'] + (opos - tpos) * ['left'] + (trow - orow) * ['down'] + (orow - trow) * ['up']

    @staticmethod
    def get_duration_for_xp(xp, maximum=15):
        return min(ceil((xp + 1) / 41), maximum)

    @property
    def duration_to_next_level(self):
        return self.get_duration_for_xp(self.xp_to_next_level)

    @property
    def duration_to_next_gold(self):
        return self.get_duration_for_xp(self.xp_to_next_gold)

    def __str__(self):
        return f'<{self.name.capitalize()} (lvl: {self.level}, xp: {self.xp})>'

    def __repr__(self):
        return str(self)
