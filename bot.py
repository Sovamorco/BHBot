import queue
from time import time

from config import *
from direct_input import *
from menu import find_element, regenerate_layout
from windows import *


class QueuedRecalculation(Exception):
    pass


class ResizedError(Exception):
    pass


class DangerZoneError(Exception):
    pass


class InvalidStateError(Exception):
    pass


class BrawlhallaBot:
    def __init__(self, config, hotkeys, bot_queue):
        self.config = config
        self.hotkeys = hotkeys
        self.queue = bot_queue

        self.mode = self.config.mode(bot=self)

        self.characters = []
        self.unlocked_characters = []
        self.character = None
        self.duration = None

        self.brawlhalla = None
        self.virtual_input = None
        self.level_definer = None

        self.last_pause = time()
        self.games_completed = 0
        self.total_xp = 0
        self.total_gold = 0
        self.crashes = 0
        self.time_started = time()
        self._time_started = self.time_started

        self.last_states = set()

        self.state_detection_pixels = get_menu_pixels()

        self.current_menu_element = None

    def find_brawlhalla(self):
        brawlhalla = BrawlhallaProcess.find()
        if brawlhalla:
            self.brawlhalla = brawlhalla
            return True
        return False

    def ensure_brawlhalla(self):
        if self.find_brawlhalla():
            self.brawlhalla.kill()
            sleep(5)

        try:
            steam = SteamClient()
        except SteamExeNotFound:
            logger.error('no_steam_exe')
            return self.on_exit()
        count = 10000
        while not self.find_brawlhalla():
            logger.debug('waiting_for_bh_window')
            self.process_queue()
            count += 1
            if count >= 10000:
                steam.run_brawlhalla()
                count = 0

        self.virtual_input = VirtualInput(self.brawlhalla, self.hotkeys)
        self.level_definer = LevelDefiner(self.brawlhalla)

        logger.info('found_bh')
        self.virtual_input.esc()  # idk why but it puts bh into windowed
        sleep(1)
        self.get_states()
        if self.brawlhalla.fullscreen:
            logger.info('not_windowed_mode')
            raise NotRespondingError
        self.brawlhalla.resize()
        if self.config.stealth:
            logger.info('stealth_mode')
            self.brawlhalla.hide()
            self.brawlhalla.set_low_priority()

    def initialize(self):
        self.ensure_brawlhalla()
        self.duration = 15

        self.go_to_menu(True)
        regenerate_layout()
        self.current_menu_element = find_element('first_column').current_element
        sleep(2)

        if self.config.mute:
            self.mute()

        if not self.characters:
            if self.mode.parse_character_levels:
                self.characters = self.get_characters()
                self.unlocked_characters = [character for character in self.characters if character.unlocked]
            else:
                self.characters = [Character(name) for name in characters]
                self.unlocked_characters = self.characters

        self.character = self.unlocked_characters[0]
        logger.debug('initialized')

    def on_exit(self):
        if self.virtual_input:
            self.virtual_input.release_keys()
        if self.config.stealth and self.brawlhalla:
            self.brawlhalla.kill()
        text = global_settings.messages.get('initial_on_exit', 'initial_on_exit') % (format_time(time() - self.time_started), self.games_completed, self.crashes, self.total_xp)
        if self.mode.parse_character_levels:
            text += global_settings.messages.get('on_exit_has_rewards', 'on_exit_has_rewards') % (self.total_gold,)
        else:
            text += global_settings.messages.get('on_exit_no_rewards', 'on_exit_no_rewards') % (self.total_gold,)
        box(text, endmargin=False)
        global_settings.update_stats(time=time() - self._time_started)
        stats = global_settings.get_stats()
        total = global_settings.messages.get('total_stats', 'total_stats') % (stats.get('games', 0), stats.get('xp', 0), stats.get('gold', 0), format_time(stats.get('time', 0)))
        box(total, endmargin=False)
        sys.exit()

    def process_queue(self, stop_delayed=False):
        put_back = []
        while not self.queue.empty():
            try:
                msg = self.queue.get_nowait()
            except queue.Empty:
                continue
            self.queue.task_done()
            if msg == 'STOP':
                raise KeyboardInterrupt
            elif msg == 'DELAYED_STOP':
                if stop_delayed:
                    raise KeyboardInterrupt
                put_back.append(msg)  # cycle it in queue waiting for delayed_stop check
        for item in put_back:
            self.queue.put_nowait(item)

    def check_stuff(self):
        self.process_queue()
        if self.brawlhalla and not self.brawlhalla.responding:
            self.brawlhalla.kill()
            sleep(1)
            raise NotRespondingError

    @property
    def state_conditions(self):
        conn_x = 1772 - ceil(98.5 * (self.config.bots // 2))
        low_conn_x = conn_x - 27

        _new_menu = {
            'pixels': ((1890, 70),),
            'colors': ((255, 255, 255),)
        }

        res = {
            'ingame': {
                'pixels': ((conn_x, 46),),
                'colors': ((0, 204, 51),),
            },
            'low_connection': {
                'pixels': ((low_conn_x, 64),),
                'colors': ((255, 255, 51), (255, 153, 0), (255, 0, 0)),
            },
            'menu': self.state_detection_pixels.get('menu') or _new_menu,
            'loading': {
                'pixels': ((899, 85),),
                'colors': ((227, 248, 255),),
            },
            'bonus': {
                'pixels': ((930, 320),),
                'colors': ((109, 198, 211),),
            },
            'offline': {
                'pixels': ((1674, 26),),
                'colors': ((55, 66, 100), (57, 67, 101)),
            },
            'sorted_by_date': {
                'pixels': ((410, 768),),
                'colors': ((254, 254, 255),),
            },
            'lobby': {
                'pixels': ((1325, 22),),
                'colors': ((255, 255, 255),),
            },
            'game_in_progress': {
                'pixels': ((960, 395),),
                'colors': ((111, 200, 211),),
            },
            'settings_open': {
                'pixels': ((1221, 106),),
                'colors': ((220, 220, 222),),
            },
            'disconnected': {
                'pixels': ((934, 623),),
                'colors': ((247, 248, 249),),
            },
            'system_settings_selected': {
                'pixels': ((1607, 195),),
                'colors': ((39, 85, 136),),
            },
            'on_rewards_screen': {
                'pixels': ((1035, 121),),
                'colors': ((255, 255, 255),),
            },
            'level_up': {
                'pixels': ((1363, 320),),
                'colors': ((19, 133, 51),),
            },
            'popup': {
                'pixels': ((940, 790),),
                'colors': ((247, 248, 249),),
            },
            'in_mallhalla': {
                'pixels': ((578, 135),),
                'colors': ((255, 255, 255),),
            },
            'in_battle_pass': {
                'pixels': ((160, 40),),
                'colors': ((255, 255, 255),),
            },
        }

        for key in res.keys():
            if key != 'menu' and key in self.state_detection_pixels:
                res[key] = self.state_detection_pixels[key]

        return res

    @property
    def duration_setting(self):
        return [self.open_settings, 1] + \
            [self.virtual_input.down] * 2 + \
            (self.mode.next_duration - self.duration) * [self.virtual_input.right] + \
               (self.duration - self.mode.next_duration) * [self.virtual_input.left] + \
               [self.virtual_input.quick]

    @property
    def danger_zone(self):
        return {'in_mallhalla', 'in_battle_pass'}

    @property
    def safe_states(self):
        return {'ingame', 'low_connection'}

    @staticmethod
    def is_color(screenshot, pixels, colors):
        return any(screenshot.getpixel(pixel) in colors for pixel in pixels)

    def execute_steps(self, *steps, delay=.1):
        self.get_states()
        for step in steps:
            if isinstance(step, (int, float)):
                sleep(step)
            elif isinstance(step, str):
                if step in self.virtual_input.keys:
                    self.virtual_input.press_key(self.virtual_input.keys[step])
                else:
                    logger.info(step)
            else:
                step()
            self.get_states()
            sleep(delay)

    def main_sequence(self):
        try:
            self.initialize()
            self.initial_setup()

            while True:
                self.execute_steps(self.before_fight, self.go_to_fight)

                logger.info('started_fighting')
                last, ig = True, True  # To avoid failing ingame detection on low connection bc of "Double kill" popup covering first connection column for 1 frame
                while last or ig:
                    self.get_states()
                    last, ig = ig, self.has_state('ingame', 'low_connection')
                    self.virtual_input.fight()

                self.execute_steps('ended_fighting', 5, self.after_fight)

        except NotRespondingError:
            self.crashes += 1
            sleep(5)
            logger.info('reinitializing')
        except QueuedRecalculation:
            sleep(5)
            logger.info('queued_recalc')
        except ResizedError:
            logger.warning('resized_warning')
            sleep(5)
        except DangerZoneError:
            logger.warning('danger_zone_warning')
            sleep(5)
        except InvalidStateError:
            self.crashes += 1
            logger.warning('invalid_state_warning')
            sleep(5)

    def main_loop(self):
        while True:
            try:
                self.main_sequence()
            except KeyboardInterrupt:
                self.on_exit()
            except Exception as e:
                logger.exception(e)
                self.crashes += 1
                self.on_exit()

    def get_states(self):
        self.check_stuff()
        states = set()
        screenshot = self.brawlhalla.make_screenshot()
        if screenshot.size != (1920, 1080):
            raise ResizedError
        for state in self.state_conditions:
            if self.is_color(screenshot, **self.state_conditions[state]):
                states.add(state)
        logger.debug(states)
        if self.danger_zone & states and not self.safe_states & states:
            raise DangerZoneError
        self.last_states = states

    def has_state(self, *states):
        return self.last_states & set(states)

    def go_to_menu(self, initial=False):
        iters = 0
        self.get_states()
        while not self.has_state('menu'):
            iters += 1
            logger.debug('not_in_menu')
            self.virtual_input.esc()
            sleep(1)
            if self.has_state('bonus'):
                logger.info('collecting_bonus')
                self.virtual_input.quick()
            if self.has_state('popup'):
                logger.info('accepting_event_popup')
                self.virtual_input.quick()
            if not initial and self.has_state('offline'):
                logger.info('offline')
                self.select_menu_item('custom_game_room')
                self.go_to_lobby(100)
                logger.info('reconnected')
                self.go_to_menu()
            if iters > 100:
                raise NotRespondingError
            self.get_states()

    def select_item(self, item, *steps):
        while not self.has_state(f'{item}_selected'):
            logger.debug('item_not_selected', item)
            self.execute_steps(*steps, delay=.05)
            if self.has_state('game_in_progress'):
                self.virtual_input.dodge()

    def select_menu_item(self, name):
        target = find_element(name)
        keys = self.current_menu_element.move_to(target, self.virtual_input)
        self.current_menu_element = target
        self.execute_steps(*keys)

    def mute(self):
        logger.info('muting')
        self.select_menu_item('system_settings')
        self.get_states()
        if not self.has_state('system_settings_selected'):
            raise InvalidStateError
        self.execute_steps(self.virtual_input.quick, *([self.virtual_input.left] * 10), self.virtual_input.down, *([self.virtual_input.left] * 10), self.virtual_input.dodge)

    def sort_by_date(self):
        counter = 0
        while not self.has_state('sorted_by_date'):
            logger.debug('sorting_by_date')
            self.virtual_input.enter()
            sleep(.5)
            self.get_states()
            if counter > 10:
                raise InvalidStateError
            counter += 1

    def get_characters(self):
        _characters = []
        rotation = get_rotation()
        self.select_menu_item('meet_the_legends')
        self.execute_steps(self.virtual_input.quick, .5, self.sort_by_date)
        logger.info('collecting_character_data')
        for line in level_character_matrix:
            for character in line:
                self.get_states()
                level = self.level_definer.get_level()
                xp = self.level_definer.get_xp(level)
                unlocked = character in rotation or self.level_definer.get_unlocked()
                _characters.append(Character(character, level, xp, unlocked))
                logger.debug(_characters[-1])
                self.virtual_input.right()
                sleep(.15)
            self.virtual_input.down()
            sleep(.15)
        unlocked_characters = [character.name for character in _characters if character.unlocked]
        locked_characters = [character.name for character in _characters if not character.unlocked]
        fixed_characters = unlocked_characters + ['random'] + locked_characters
        build_character_matrix(fixed_characters)
        self.go_to_menu()
        return _characters

    def go_to_lobby(self, max_iters=10):
        iters = 0
        while not self.has_state('lobby'):
            self.virtual_input.quick()
            sleep(2)
            if iters > max_iters:
                raise InvalidStateError
            self.get_states()
            iters += 1

    def validate_level(self):
        self.go_to_rewards_screen()
        if self.duration < 3 or self.has_state('level_up'):
            logger.debug('skip_lvl_valid')
            return True
        xp = self.level_definer.get_xp(self.character.level, True)
        calculated_xp = get_duration_xp(self.duration)
        logger.debug('calc_xp', calculated_xp)
        logger.debug('pixel_xp', xp)
        if (self.character.level < 40 and abs(xp - calculated_xp) > calculated_xp / 3) or abs(xp - calculated_xp) > calculated_xp / 1.5:
            logger.info('xp_discrep')
            return False
        return True

    def go_to_rewards_screen(self):
        while not self.has_state('on_rewards_screen'):
            self.virtual_input.quick()
            sleep(5)
            self.get_states()

    def open_settings(self):
        while not self.has_state('settings_open'):
            self.virtual_input.heavy()
            sleep(2)
            self.get_states()

    def wait_for_loading(self):
        iters = 0
        while not self.has_state('loading'):
            logger.debug('waiting_for_loading')
            iters += 1
            self.virtual_input.quick()
            sleep(2)
            if iters > self.duration * 60:
                raise NotRespondingError
            self.get_states()

    def wait_for_loaded(self):
        iters = 0
        while self.has_state('loading'):
            logger.debug('loading')
            iters += 1
            sleep(1)
            if iters > 100:
                raise InvalidStateError
            self.get_states()

    def pick_character(self):
        logger.info('pick_char', self.mode.next_character)
        if self.character != self.mode.next_character:
            self.execute_steps(*self.character.get_path_to(self.mode.next_character.name))
            self.character = self.mode.next_character

    def set_duration(self):
        logger.info('setting_dur', self.mode.next_duration)
        if self.duration != self.mode.next_duration:
            self.execute_steps(*self.duration_setting)
            self.duration = self.mode.next_duration

    def reset_xp(self):
        self.execute_steps(self.virtual_input.dodge, self.virtual_input.dodge, self.go_to_menu)
        waiting_start = time()
        logger.info('wait_for_xp_reset', self.config.auto_stop_duration)
        while time() - waiting_start < self.config.auto_stop_duration * 60:
            logger.debug('wait_remaining', int(waiting_start + self.config.auto_stop_duration * 60 - time()))
            self.check_stuff()
            sleep(1)
        self.last_pause = time()
        self.characters = []
        self.unlocked_characters = []
        raise QueuedRecalculation

    def setup_lobby(self):
        # noinspection PyTypeChecker
        steps = [self.open_settings] + \
                [self.virtual_input.right] * 6 + \
                [self.virtual_input.down] + \
                [self.virtual_input.left] * 3 + \
                [self.virtual_input.down] + \
                [self.virtual_input.left] * (15 - self.duration) + \
                [self.virtual_input.down] + \
                [self.virtual_input.left] * 6 + \
                [self.virtual_input.rbr] + \
                [self.virtual_input.down] * 3 + \
                [self.virtual_input.left, self.virtual_input.down] * 3 + \
                [self.virtual_input.left, self.virtual_input.quick]
        self.execute_steps(*steps)

    def add_bots(self):
        steps = [self.virtual_input.throw, 1, self.virtual_input.quick, self.virtual_input.throw]
        self.execute_steps(*steps)

    def initial_setup(self):
        self.execute_steps('creating_lobby', 1, 1)
        self.select_menu_item('custom_game_room')
        self.execute_steps(self.go_to_lobby, 'setting_lobby', self.setup_lobby, 4, self.add_bots)

    def before_fight(self):
        self.execute_steps(2, self.pick_character, 1, self.set_duration, 1)

    def go_to_fight(self):
        self.process_queue(True)
        self.execute_steps('starting_game', self.wait_for_loading, self.wait_for_loaded, 'loaded', 5)

    def after_fight(self):
        self.get_states()
        if self.has_state('disconnected', 'game_in_progress', 'offline'):
            logger.info('disconnected')
            raise NotRespondingError
        self.games_completed += 1
        calc_xp = get_duration_xp(self.duration)
        time_to_sleep = self.config.auto_stop and (
                (not self.config.auto_detect_auto_stop and time() - self.last_pause > self.config.auto_stop_frequency * 3600)
                or (self.config.auto_detect_auto_stop and not self.validate_level()))
        gold_for_level_up = self.character.add_xp(calc_xp)
        calc_gold = get_duration_gold(self.duration) + gold_for_level_up
        self.total_xp += calc_xp
        self.total_gold += calc_gold
        logger.debug('update_total_stats')
        global_settings.update_stats(games=1, time=time() - self._time_started, gold=calc_gold, xp=calc_xp)
        self._time_started = time()
        logger.info('return_to_lobby')
        self.go_to_lobby()
        sleep(2)
        self.process_queue(True)
        if time_to_sleep:
            self.reset_xp()
