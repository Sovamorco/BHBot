from random import choice
from time import sleep

import keyboard
import win32api
import win32con
import win32gui

from utils import *

MAP_VSC_TO_VK = 1
MAP_VK_TO_CHAR = 2


# noinspection PyPep8Naming
class VirtualInput:
    def __init__(self, brawlhalla, hotkeys):
        self.brawlhalla = brawlhalla
        self.hotkeys = hotkeys

    @property
    def keys(self):
        return vars(self.hotkeys)

    def PressKey(self, hexCode):
        win32gui.SendMessage(self.brawlhalla.window, win32con.WM_KEYDOWN, hexCode)

    def ReleaseKey(self, hexCode):
        win32gui.SendMessage(self.brawlhalla.window, win32con.WM_KEYUP, hexCode)

    def press_key(self, *key_codes, delay=.05):
        for key_code in key_codes:
            self.PressKey(key_code)
        sleep(delay)
        for key_code in key_codes:
            self.ReleaseKey(key_code)

    def release_keys(self):
        for key in self.keys:
            self.ReleaseKey(self.keys[key])
            sleep(.05)

    def up(self, *args, **kwargs):
        self.press_key(self.hotkeys.up, *args, **kwargs)

    def down(self, *args, **kwargs):
        self.press_key(self.hotkeys.down, *args, **kwargs)

    def left(self, *args, **kwargs):
        self.press_key(self.hotkeys.left, *args, **kwargs)

    def right(self, *args, **kwargs):
        self.press_key(self.hotkeys.right, *args, **kwargs)

    def throw(self, *args, **kwargs):
        self.press_key(self.hotkeys.throw, *args, **kwargs)

    def quick(self, *args, **kwargs):
        self.press_key(self.hotkeys.quick, *args, **kwargs)

    def heavy(self, *args, **kwargs):
        self.press_key(self.hotkeys.heavy, *args, **kwargs)

    def dodge(self, *args, **kwargs):
        self.press_key(self.hotkeys.dodge, *args, **kwargs)

    def rbr(self, *args, **kwargs):
        self.press_key(self.hotkeys.rbr, *args, **kwargs)

    def esc(self, *args, **kwargs):
        self.press_key(self.hotkeys.esc, *args, **kwargs)

    def enter(self, *args, **kwargs):
        self.press_key(self.hotkeys.enter, *args, **kwargs)

    def fight(self):
        move_keys = [self.hotkeys.left, self.hotkeys.up, self.hotkeys.down, self.hotkeys.right]
        fight_keys = [self.hotkeys.throw, self.hotkeys.quick, self.hotkeys.heavy, self.hotkeys.dodge]
        self.press_key(choice(move_keys), choice(fight_keys), delay=.2)


class Hotkeys:
    def __init__(self, hotkeys):
        self.up = hotkeys.get('up', win32con.VK_UP)
        self.down = hotkeys.get('down', win32con.VK_DOWN)
        self.left = hotkeys.get('left', win32con.VK_LEFT)
        self.right = hotkeys.get('right', win32con.VK_RIGHT)
        self.throw = hotkeys.get('throw', 0x48)
        self.quick = hotkeys.get('quick', 0x4A)
        self.heavy = hotkeys.get('heavy', 0x4B)
        self.dodge = hotkeys.get('dodge', 0x4C)
        self.rbr = 0xDD
        self.esc = win32con.VK_ESCAPE
        self.enter = win32con.VK_RETURN

    @classmethod
    def load(cls):
        try:
            res = json.load(global_settings.hotkeys_location.open('r'))
            return cls(res)
        except FileNotFoundError:
            return cls({})

    def save(self):
        try:
            global_settings.hotkeys_location.parent.mkdir(parents=True, exist_ok=True)
            json.dump(vars(self), global_settings.hotkeys_location.open('w+'))
        except Exception as e:
            logger.error('cant_save_hotkeys', e)


class GUIHotkeys:
    def __init__(self):
        self.hotkeys = Hotkeys.load()
        self.window = self.create_window()
        self.hook = None
        self.last_keyboard_event = None
        self.converter = {}

    def hook_keyboard(self):
        def inner_hook(event):
            self.last_keyboard_event = event

        if not self.hook:
            self.hook = keyboard.hook(inner_hook)

    def unhook_keyboard(self):
        if self.hook:
            keyboard.unhook(self.hook)
            self.hook = None

    @staticmethod
    def text_column(*keys):
        return Sg.Column(
            [[Sg.Text(' ', size=(1, 1), key=f'{key}_text', font=(global_settings.font, 12))] for key in keys]
        )

    def input_column(self, *keys):
        return Sg.Column(
            [[Sg.Input(size=(3, 1), key=key, enable_events=True, font=(global_settings.font, '12'), default_text=self.vk_to_char(vars(self.hotkeys)[key]))] for key in keys]
        )

    def combined_column(self, *keys):
        return [self.text_column(*keys), self.input_column(*keys)]

    def create_window(self):
        layout = [
            [Sg.Text(' ', size=(1, 1), key='hotkeys_title', font=(global_settings.font, 20))],
            [
                *self.combined_column('up', 'left', 'throw', 'quick'),
                *self.combined_column('down', 'right', 'dodge', 'heavy')
            ],
            [Sg.Button('', key='save', font=(global_settings.font, 12)), Sg.Button('', key='back', font=(global_settings.font, 12))],
        ]
        window = Sg.Window('', layout, size=(600, 350), keep_on_top=True, icon=global_settings.icon, metadata='hotkeys_window_title').Finalize()
        global_settings.update_window(window)
        return window

    @staticmethod
    def vsc_to_vk(code):
        return win32api.MapVirtualKey(code, MAP_VSC_TO_VK)

    @staticmethod
    def vk_to_char(code):
        direct = {
            win32con.VK_LEFT: '◁',
            win32con.VK_UP: '△',
            win32con.VK_RIGHT: '▷',
            win32con.VK_DOWN: '▽',
        }
        if code in direct:
            return direct[code]
        return chr(win32api.MapVirtualKey(code, MAP_VK_TO_CHAR))

    def save(self):
        for key in self.converter:
            vars(self.hotkeys)[key] = self.converter[key]
        self.hotkeys.save()

    def start_loop(self):
        self.hook_keyboard()
        while True:
            event, values = self.window.read(timeout=50)
            if self.last_keyboard_event:
                if event in ['up', 'down', 'left', 'right', 'quick', 'heavy', 'dodge', 'throw']:
                    vk = self.vsc_to_vk(self.last_keyboard_event.scan_code)
                    self.window[event].Update(self.vk_to_char(vk))
                    self.converter[event] = vk
            if event in (Sg.WINDOW_CLOSED, 'back'):
                break
            elif event == 'save':
                self.save()
                break
            global_settings.update_window(self.window)
        self.unhook_keyboard()
        self.window.close()
