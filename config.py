import importlib.util

from abstract_mode import Mode
from characters import *
from direct_input import *
from utils import *


def display_changelog():
    changelog_path = Path(os.getenv('LOCALAPPDATA')) / 'BHBot' / 'changelog'
    if global_settings.compiled and (not changelog_path.exists() or changelog_path.read_text('utf-8') != global_settings.APP_VERSION):
        Sg.popup(*global_settings.APP_CHANGELOG, font=(global_settings.font, 13), title=global_settings.language.LAYOUT_MAPPING.get('changelog_popup_title', 'Changelog'), icon=global_settings.icon)
        changelog_path.parent.mkdir(parents=True, exist_ok=True)
        changelog_path.write_text(global_settings.APP_VERSION, 'utf-8')


class Config:
    def __init__(self, config):
        self.character = config.get('character', 'Random')
        self.duration = config.get('duration', 8)
        self.auto_stop = config.get('auto_stop', True)
        self.auto_detect_auto_stop = config.get('auto_detect_auto_stop', False)
        self.auto_stop_frequency = config.get('auto_stop_frequency', 5)
        self.auto_stop_duration = config.get('auto_stop_duration', 30)
        # self.bots = config.get('bots', 2)
        self.bots = 2
        self.mute = config.get('mute', False)
        self.stealth = config.get('stealth', False)
        self.modes = self.get_modes()
        if not self.modes:
            logger.error('no_modes')
        else:
            self.mode_name = config.get('mode_name', self.modes[0].get_name())
        self.version = global_settings.APP_VERSION

    @classmethod
    def load(cls):
        try:
            res = json.load(global_settings.config_location.open('r'))
            if res.get('version') != global_settings.APP_VERSION:
                logger.warning('old_config')
            return cls(res)
        except FileNotFoundError:
            return cls({})

    # noinspection PyUnresolvedReferences
    @staticmethod
    def get_modes():
        for mode in global_settings.modes_folder.glob('**/*.py'):
            if mode in global_settings.loaded_modes:
                continue
            spec = importlib.util.spec_from_file_location('module.name', mode)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            global_settings.loaded_modes[mode] = module
        return Mode.__subclasses__()

    def get_mode(self, name):
        try:
            return next(filter(lambda x: x.get_name() == name, self.modes))
        except StopIteration:
            return self.modes[0]

    @property
    def mode(self):
        return self.get_mode(self.mode_name)

    @property
    def not_save(self):
        return ['modes']

    def get_save_vars(self):
        return {k: v for k, v in vars(self).items() if k not in self.not_save}

    def save(self):
        try:
            global_settings.config_location.parent.mkdir(parents=True, exist_ok=True)
            json.dump(self.get_save_vars(), global_settings.config_location.open('w+'))
        except Exception as e:
            logger.error('cant_save_config', e)

    def __str__(self):
        return global_settings.messages.get('config', 'Missing "config" entry in language').format(self)


# noinspection PyUnresolvedReferences
class GUIConfig:
    def __init__(self):
        self.config = Config.load()
        self.window = self.create_window()

    @property
    def characters(self):
        res = [character.capitalize() for character in sorted(characters)]
        if hasattr(self, 'window') and not self.get_mode().parse_character_levels:
            res.insert(0, 'Random')
        return res

    @property
    def mode_names(self):
        return [mode.get_name() for mode in self.config.modes]

    @property
    def language_names(self):
        return [language.LANGUAGE for language in global_settings.languages]

    def get_mode(self):
        return self.config.get_mode(self.window['mode_name'].get())

    def update_layout(self):
        if self.window['mode_name'].Values != self.mode_names:
            self.window['mode_name'].Update(self.mode_names[0], values=self.mode_names)
        if self.window['character'].Values != self.characters:
            char = self.window['character'].get() if self.window['character'].get() in self.characters else self.characters[0]
            self.window['character'].Update(char, values=self.characters)
        mode = self.get_mode()
        if mode.character_selection_enabled:
            self.window['character'].update(disabled=False, readonly=True)
        else:
            self.window['character'].update(disabled=True, readonly=True)
        if not mode.parse_character_levels:
            self.window['auto_detect_auto_stop'].update(False, disabled=True)
        if mode.duration_selection_enabled:
            self.window['duration'].update(disabled=False)
        else:
            self.window['duration'].update(disabled=True)
        if self.window['auto_stop'].get():
            self.window['auto_stop_duration'].update(disabled=False)
            if mode.parse_character_levels:
                self.window['auto_detect_auto_stop'].update(disabled=False)
            if self.window['auto_detect_auto_stop'].get():
                self.window['auto_stop_frequency'].update(disabled=True)
            else:
                self.window['auto_stop_frequency'].update(disabled=False)
        else:
            self.window['auto_detect_auto_stop'].update(disabled=True)
            self.window['auto_stop_frequency'].update(disabled=True)
            self.window['auto_stop_duration'].update(disabled=True)
        if self.window['stealth'].get():
            self.window['mute'].update(True, disabled=True)
        else:
            self.window['mute'].update(disabled=False)

    def save(self, values):
        for key in values:
            if isinstance(values[key], float) and values[key].is_integer():
                values[key] = int(values[key])
        for k, v in values.items():
            if hasattr(self.config, k):
                setattr(self.config, k, v)
            if hasattr(global_settings, k):
                setattr(global_settings, k, v)
        self.config.save()
        global_settings.save()

    @staticmethod
    def row(key, input_element):
        input_element.Key = key
        text = Sg.Text(' ', size=(1, 1), key=f'{key}_text', font=(global_settings.font, 12))
        if isinstance(input_element, Sg.Slider):
            text.Pad = ((5, 0), (20, 0))
        layout = [
            [text, input_element]
        ]
        return Sg.Column(layout, key=f'{key}_column', element_justification='left')

    def create_window(self):
        layout = [
            [Sg.Text(' ', size=(1, 1), key='settings_title', font=(global_settings.font, 20))],
            [Sg.Text(' ', size=(1, 1), key='settings_help', font=(global_settings.font, 16))],
            [self.row('language_name', Sg.Combo(self.language_names, enable_events=True, readonly=True, default_value=global_settings.language_name, font=(global_settings.font, 12)))],
            [self.row('font', Sg.Combo(global_settings.fonts, enable_events=True, readonly=True, default_value=global_settings.font, font=(global_settings.font, 12)))],
            [self.row('autostart', Sg.Checkbox('', default=global_settings.autostart))],
            [self.row('branch', Sg.Combo(['stable', 'beta'], readonly=True, default_value=global_settings.branch, font=(global_settings.font, 12)))],
            [self.row('debug', Sg.Checkbox('', default=global_settings.debug))],
            [self.row('mode_name', Sg.Combo(self.mode_names, readonly=True, default_value=self.config.mode_name, font=(global_settings.font, 12)))],
            [self.row('character', Sg.Combo(self.characters, readonly=True, default_value=self.config.character, font=(global_settings.font, 12)))],
            [self.row('duration', Sg.Slider(range=(1, 15), orientation='horizontal', default_value=self.config.duration, font=(global_settings.font, 12)))],
            [self.row('auto_stop', Sg.Checkbox('', default=self.config.auto_stop))],
            [self.row('auto_detect_auto_stop', Sg.Checkbox('', default=self.config.auto_detect_auto_stop))],
            [self.row('auto_stop_frequency',
                      Sg.Slider(range=(1, 20), resolution=.5, orientation='horizontal', default_value=self.config.auto_stop_frequency, font=(global_settings.font, 12)))],
            [self.row('auto_stop_duration',
                      Sg.Slider(range=(5, 240), resolution=5, orientation='horizontal', default_value=self.config.auto_stop_duration, font=(global_settings.font, 12)))],
            # [self.row('bots', Sg.Combo(list(range(1, 8)), readonly=True, default_value=self.config.bots, font=(global_settings.font, 12)))],
            [self.row('stealth', Sg.Checkbox('', default=self.config.stealth))],
            [self.row('mute', Sg.Checkbox('', default=self.config.mute))],
            [Sg.Button('', font=(global_settings.font, 12), key='hotkey_settings')],
            [Sg.Button('', font=(global_settings.font, 12), key='save'), Sg.Button('', font=(global_settings.font, 12), key='back')]
        ]
        window = Sg.Window('', layout, size=(800, 800), keep_on_top=True, icon=global_settings.icon, metadata='settings_window_title').Finalize()
        global_settings.update_window(window)
        return window

    def start_loop(self):
        while True:
            event, values = self.window.read(timeout=50)
            if event in (Sg.WINDOW_CLOSED, 'back'):
                break
            elif event == 'save':
                self.save(values)
                break
            elif event == 'hotkey_settings':
                hotkeys = GUIHotkeys()
                self.window.disable()
                self.window.hide()
                hotkeys.start_loop()
                self.window.enable()
                self.window.un_hide()
            elif event == 'language_name':
                global_settings.language_name = values['language_name']
                global_settings.save()
            elif event == 'font':
                global_settings.font = values['font']
                global_settings.save()
            self.update_layout()
            global_settings.update_window(self.window)
        self.window.close()
