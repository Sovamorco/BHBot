import importlib.util
import json
import logging
import os
import sys
from copy import copy
from datetime import datetime, timedelta
from math import floor, ceil
from pathlib import Path

import PySimpleGUI as Sg
import requests
# noinspection PyProtectedMember
from pyupdater import rfh, log
from pyupdater.client import Client

from client_config import ClientConfig
from font_loader import get_font_name, load_font

rfh.close()
log.removeHandler(rfh)


def get_text(element):
    if isinstance(element, Sg.Text):
        return element.get()
    elif isinstance(element, Sg.Button):
        return element.get_text()
    return f'Unsupported element type {type(element)}'


def set_text(element, value):
    if isinstance(element, Sg.Text):
        element.set_size((len(value), 1))
        element.update(value)
    if isinstance(element, Sg.Button):
        element.update(value)


def my_emit(superclass, record):
    record = copy(record)
    if isinstance(record.msg, str) and record.msg.count('%s') < len(record.args):
        record.msg += ' ' + ' '.join(['%s' for _ in range(len(record.args) - record.msg.count('%s'))])
    superclass.emit(record)


class MyStreamHandler(logging.StreamHandler):
    def emit(self, record):
        my_emit(super(), record)


class MyFileHandler(logging.FileHandler):
    def emit(self, record):
        my_emit(super(), record)


class MyFormatter(logging.Formatter):
    def format(self, record):
        # noinspection PyProtectedMember
        format_orig = self._style._fmt
        if record.levelno == logging.DEBUG:
            self._style._fmt = '%(asctime)s %(levelname)s %(message)s'
        elif record.levelno == logging.INFO:
            self._style._fmt = '%(message)s'
        result = super().format(record)
        self._style._fmt = format_orig
        return result


logger = logging.getLogger('main_bot_logger')
logger.setLevel(logging.DEBUG)
hdlr = MyStreamHandler()
hdlr.setLevel(logging.DEBUG)
hdlr.setFormatter(MyFormatter())
logger.addHandler(hdlr)


def excepthook(type_, value, traceback):
    logger.exception(value)
    sys.__excepthook__(type_, value, traceback)


sys.excepthook = excepthook


class Settings:
    installation_folder = Path.cwd()
    logs_folder = Path(os.getenv('LOCALAPPDATA')) / 'BHBot' / 'logs'
    installation_info_location = Path(os.getenv('LOCALAPPDATA')) / 'BHBot' / 'installation.data'
    settings_location = Path(os.getenv('LOCALAPPDATA')) / 'BHBot' / 'settings.cfg'
    config_location = Path(os.getenv('LOCALAPPDATA')) / 'BHBot' / 'bhbot.cfg'
    hotkeys_location = Path(os.getenv('LOCALAPPDATA')) / 'BHBot' / 'hotkeys.cfg'
    stats_location = Path(os.getenv('LOCALAPPDATA')) / 'BHBot' / 'stats.json'

    def __init__(self, settings):
        self.APP_NAME = 'BHBot'
        self.APP_VERSION = '3.3.18-beta'
        self.APP_CHANGELOGS = {
            'English': [f'Updated to {self.APP_VERSION} \\o/',
                        'If it\'s your first time using the bot or seeing this message, please click "Instructions" and read them carefully',
                        '- Made bot slower but safer and it\'s weird now'],
            'Русский': [f'Обновился до {self.APP_VERSION} \\o/',
                        'Если вы используете бота или видите это сообщение впервые, пожалуйста, нажмите на "Инструкции" и тщательно их прочтите',
                        '- Сделал бота более медленным но более безопасным и очень странным']
        }

        self.compiled = getattr(sys, 'frozen', False)

        self.load_installation_info()
        self.clear_old_logs()
        self.add_file_handlers()
        self.load_fonts()

        pyupdater_client = Client(ClientConfig(), refresh=True, progress_hooks=[self.print_update_status])

        self.branch = settings.get('branch', 'stable')

        self.new_version = pyupdater_client.update_check(self.APP_NAME, self.APP_VERSION, channel=self.branch, strict=self.branch != 'beta')

        self.languages = self.get_languages()
        if not self.languages:
            logger.error('No languages found. Program will not function with empty languages directory.')
        self.language_name = settings.get('language_name', 'English')

        self.APP_CHANGELOG = self.APP_CHANGELOGS.get(self.language_name, self.APP_CHANGELOGS.get('English'))

        self.fonts = self.get_fonts()
        self.font = settings.get('font', 'Cousine Regular')

        self.autostart = settings.get('autostart', False)

        self.icon = self.installation_folder / 'icon.ico'

        self.debug = settings.get('debug', False)
        self.gui_handler = None
        self.loaded_modes = {}

    @staticmethod
    def print_update_status(info):
        if info['status'] == 'downloading':
            logger.info('downloading', info["percent_complete"])
        elif info['status'] == 'finished':
            logger.info('downloaded', info["time"])

    @classmethod
    def load(cls):
        try:
            return cls(json.load(cls.settings_location.open('r')))
        except FileNotFoundError:
            return cls({})

    # noinspection PyUnresolvedReferences
    def get_languages(self):
        languages = []
        for language in self.languages_folder.glob('*.py'):
            spec = importlib.util.spec_from_file_location('module.name', language)
            language_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(language_module)
            languages.append(language_module)
        return languages

    def get_fonts(self):
        fonts = ['Courier']
        for font in self.fonts_folder.glob('**/*.ttf'):
            fonts.append(get_font_name(font.open('rb')))
        return fonts

    def get_language(self, name):
        return next(filter(lambda x: x.LANGUAGE == name, self.languages))

    @property
    def language(self):
        return self.get_language(self.language_name)

    @property
    def not_save(self):
        return ['fonts', 'languages', 'gui_handler', 'loaded_modes', 'new_version', 'compiled', 'APP_CHANGELOG', 'APP_CHANGELOGS', 'icon']

    def set_debug_state(self):
        if self.gui_handler:
            self.gui_handler.setLevel(logging.DEBUG if self.debug else logging.INFO)

    def get_save_vars(self):
        return {k: v for k, v in vars(self).items() if k not in self.not_save}

    def save(self):
        self.set_debug_state()
        try:
            self.settings_location.parent.mkdir(parents=True, exist_ok=True)
            json.dump(self.get_save_vars(), self.settings_location.open('w+'))
        except Exception as e:
            logger.error(f'Could not save settings. Exception: {e}')

    # noinspection PyUnresolvedReferences
    @property
    def messages(self):
        return self.language.MESSAGES

    # noinspection PyUnresolvedReferences
    def update_window(self, window):
        for key in window.AllKeysDict:
            font = window[key].Font
            if font and font[0] != global_settings.font:
                window[key].Font = (global_settings.font, font[1])
                window[key].Widget.config(font=window[key].Font)
            if key in self.language.LAYOUT_MAPPING:
                value = self.language.LAYOUT_MAPPING.get(key)
                res_text = value[window[key].metadata].format(self) if window[key].metadata is not None else value.format(self)
                if res_text != get_text(window[key]):
                    set_text(window[key], res_text)
            tooltip_text = None
            if hasattr(self.language, 'TOOLTIPS') and key in self.language.TOOLTIPS:  # First condition is for backwards-compatibility
                tooltip_value = self.language.TOOLTIPS.get(key)
                tooltip_text = tooltip_value[window[key].metadata].format(self) if window[key].metadata is not None else tooltip_value.format(self)
            if tooltip_text != window[key].Tooltip:
                window[key].Tooltip = tooltip_text
                window[key].set_tooltip(tooltip_text)

        if window.Title != self.language.LAYOUT_MAPPING.get(window.metadata):
            window.Title = self.language.LAYOUT_MAPPING.get(window.metadata)
            window.set_title(window.Title)

    def load_installation_info(self):
        logger.debug('Loading installation info')
        if not self.compiled:
            return
        if all(Path(folder).exists() for folder in ['fonts', 'languages', 'modes']):
            logger.debug('Writing installation info')
            return self.write_installation_info()
        if not self.installation_info_location.exists():
            logger.error('Corrupted installation. Exiting.')
            sys.exit()
        installation_info = json.load(self.installation_info_location.open('r'))
        for path in installation_info:
            setattr(type(self), path, Path(installation_info[path]))

    def write_installation_info(self):
        logger.debug('Writing installation info')
        self.installation_info_location.parent.mkdir(parents=True, exist_ok=True)
        obj = {
            'installation_folder': Path.cwd(),
            'logs_folder': self.logs_folder,
            'settings_location': self.settings_location,
            'config_location': self.config_location,
            'hotkeys_location': self.hotkeys_location,
            'stats_location': self.stats_location,
        }
        obj = {k: str(v) for k, v in obj.items()}
        json.dump(obj, self.installation_info_location.open('w+'))

    def clear_old_logs(self):
        for _log in self.logs_folder.glob('????????-??????.log'):
            dt = _log.name[:-4]
            dt = datetime.strptime(dt, '%Y%m%d-%H%M%S')
            if datetime.now() - dt > timedelta(days=3):
                _log.unlink()

    def add_file_handlers(self):
        self.logs_folder.mkdir(parents=True, exist_ok=True)
        file_hdlr = MyFileHandler(self.logs_folder / f'{datetime.now().strftime("%Y%m%d-%H%M%S")}.log', encoding='utf-8')
        file_hdlr.setFormatter(logging.Formatter('[%(asctime)s] [%(threadName)s:THREAD%(thread)d] %(levelname)-8s %(message)s'))
        file_hdlr.setLevel(logging.DEBUG)
        logger.addHandler(file_hdlr)
        error_hdlr = MyFileHandler(self.logs_folder / 'exceptions.log', encoding='utf-8')
        error_hdlr.setFormatter(logging.Formatter('[%(asctime)s] [%(threadName)s:THREAD%(thread)d] %(levelname)-8s %(message)s'))
        error_hdlr.setLevel(logging.WARNING)
        logger.addHandler(error_hdlr)

    @property
    def fonts_folder(self):
        return self.installation_folder / 'fonts'

    @property
    def languages_folder(self):
        return self.installation_folder / 'languages'

    @property
    def modes_folder(self):
        return self.installation_folder / 'modes'

    def load_fonts(self):
        for font in self.fonts_folder.glob('**/*.ttf'):
            load_font(str(font))

    def update_stats(self, **kwargs):
        current = self.get_stats()
        for key in kwargs:
            current[key] = current.get(key, 0) + kwargs[key]
        json.dump(current, self.stats_location.open('w+'))

    def get_stats(self):
        if not self.stats_location.exists():
            return {}
        return json.load(self.stats_location.open('r'))

    def __str__(self):
        return self.messages.get('settings', 'Missing "settings" entry in language').format(self)


global_settings = Settings.load()


def box(text, startmargin=True, endmargin=True):
    lines = text.split('\n')
    longest_line = sorted(lines, key=lambda x: len(x), reverse=True)[0]
    length = len(longest_line) + 6
    if startmargin:
        logger.info('\n\n')
    logger.info('#' * length)
    for line in lines:
        spaces = (length - len(line) - 2) / 2
        logger.info('#' + ' ' * ceil(spaces) + line + ' ' * floor(spaces) + '#')
    logger.info('#' * length)
    if endmargin:
        logger.info('\n\n')


def format_time(seconds):
    seconds = int(seconds)
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return f'{h:d}:{m:02d}:{s:02d}'


def get_rotation():
    try:
        res = requests.get('https://sovamor.co/bhbot/rotation').json()
        return [character.lower() for character in res.get('rotation')]
    except Exception as e:
        logger.warning('rotation_error', e)
        return []


def chunks(input_list, n):
    """
    Yield n number of sequential chunks from input_list.
    https://stackoverflow.com/a/54802737
    """
    d, r = divmod(len(input_list), n)
    for i in range(n):
        si = (d + 1) * (i if i < r else r) + d * (0 if i < r else i - r)
        yield input_list[si:si + (d + 1 if i < r else d)]


def compare(fst, snd):
    return sum(fst[i] != snd[i] for i in range(min(len(fst), len(snd))))
