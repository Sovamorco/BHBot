from utils import *

level_bbox = 975, 143, 1060, 198
font_color = (254, 254, 254)
single_digit_diff = 21
second_digit_diff = 43

bar_bbox = 1082, 148, 1656, 149
bar_colors = ((158, 158, 177), (128, 128, 153), (30, 60, 126))

rewards_bar_bbox = 786, 331, 1365, 332
rewards_bar_colors = ((35, 120), (190, 255), (40, 165))

locked_pixel = 1163, 875
locked_color = (110, 200, 211)

first_digit_dict = {
    '1': ((10, 17), (15, 45), (17, 4), (20, 15), (27, 45), (29, 4), (19, 32)),
    '2': ((5, 11), (6, 5), (9, 3), (30, 4), (34, 45), (36, 12)),
    '3': ((3, 37), (7, 10), (8, 3), (9, 23), (33, 6), (36, 34)),
    '4': ((2, 25), (2, 34), (19, 45), (30, 45), (32, 3), (37, 27)),
    '5': ((4, 37), (5, 26), (7, 4), (23, 20), (34, 4), (36, 32)),
    '6': ((2, 28), (3, 37), (16, 3), (25, 46), (29, 3), (37, 27)),
    '7': ((4, 3), (4, 11), (5, 45), (19, 45), (36, 3), (36, 12)),
    '8': ((2, 38), (5, 12), (19, 27), (20, 3), (36, 11), (37, 35)),
    '9': ((10, 45), (15, 3), (15, 30), (19, 23), (22, 28), (24, 45)),
    '0': ((1, 30), (9, 6), (15, 13), (23, 46), (24, 34), (37, 17))
}

second_digit_dict = dict(((key, tuple(((x + second_digit_diff, y) for x, y in value))) for key, value in first_digit_dict.items()))

single_digit_dict = dict(((key, tuple(((x + single_digit_diff, y) for x, y in value))) for key, value in first_digit_dict.items()))

level_hundred_conditions = ((0, 9), (0, 15), (10, 42), (11, 8), (27, 14), (49, 39), (62, 37), (84, 9), (84, 40))

levels_xp = [
    0,  # infinite xp if lvl 0 (undefined)
    210, 368, 455, 542, 628, 737, 867, 997, 1127, 1278, 1430, 1582, 1733, 1907, 2080, 2253, 2427, 2622, 2817, 3012, 3207, 3402, 3618, 3813, 4030, 4247, 4463, 4680,
    4918, 5135, 5373, 5612, 5850, 6088, 6372, 6565, 6803, 7063, 7302, 7562, 7800, 8060, 8320, 8580, 8840, 9122, 9382, 9642, 9923, 10183, 10465, 10747, 11007, 11288, 11570,
    11852, 12113, 12415, 12718, 13000, 13282, 13585, 13867, 14170, 14473, 14755, 15058, 15362, 15665, 15968, 16272, 16575, 16878, 17182, 17507, 17810, 18113, 18438, 18742,
    19067, 19370, 19695, 20020, 20323, 20648, 20973, 21298, 21623, 21948, 22273, 22598, 22923, 23270, 23595, 23920, 24267, 24592, 24917, 25263,
    float('inf')  # infinite xp if lvl 100 (max lvl)
]

gold_levels = list(range(7, 20, 2)) + list(range(21, 101))


def get_duration_xp(duration):
    return int(40.91 * duration)


def get_duration_gold(duration):
    return 10 * duration


class LevelNotDetected(Exception):
    pass


class LevelDefiner:
    def __init__(self, brawlhalla):
        self.brawlhalla = brawlhalla

    def _get_single_digit_level(self, image):
        return int(self.get_single_digit(image))

    def _get_double_digit_level(self, image):
        return int(self.get_first_digit(image) + self.get_second_digit(image))

    @staticmethod
    def _get_level_hundred(image):
        if all(image.getpixel(pos) == font_color for pos in level_hundred_conditions):
            return 100
        raise TypeError

    def get_level(self):
        screenshot = self.brawlhalla.make_screenshot()
        level = screenshot.crop(level_bbox)
        for f in [self._get_single_digit_level, self._get_double_digit_level, self._get_level_hundred]:
            try:
                # noinspection PyArgumentList
                return f(level)
            except TypeError:
                pass
        logger.error('level_error')
        raise LevelNotDetected

    def get_percentage(self):
        count = -3
        screenshot = self.brawlhalla.make_screenshot()
        bar = screenshot.crop(bar_bbox)
        for i in range(bar.width):
            if bar.getpixel((i, 0)) in bar_colors:
                break
            count += 1
        perc = count / bar.width
        return perc

    def get_reward_percentage(self):
        count = 1
        screenshot = self.brawlhalla.make_screenshot()
        bar = screenshot.crop(rewards_bar_bbox)
        for i in range(bar.width):
            pixel = bar.getpixel((i, 0))
            if all(rewards_bar_colors[i][1] > pixel[i] > rewards_bar_colors[i][0] for i in range(len(pixel))):
                count += 1
        perc = count / bar.width
        return perc

    def get_xp(self, level, reward=False):
        if level == 100:
            return 0
        return int((self.get_reward_percentage() if reward else self.get_percentage()) * levels_xp[level])

    def get_unlocked(self):
        screenshot = self.brawlhalla.make_screenshot()
        return screenshot.getpixel(locked_pixel) != locked_color

    @staticmethod
    def get_digit(conditions, image):
        for digit in conditions:
            if all(image.getpixel(pos) == font_color for pos in conditions[digit]):
                return digit

    def get_first_digit(self, image):
        return self.get_digit(first_digit_dict, image)

    def get_second_digit(self, image):
        return self.get_digit(second_digit_dict, image)

    def get_single_digit(self, image):
        return self.get_digit(single_digit_dict, image)
