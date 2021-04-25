import ctypes
import subprocess
from time import sleep

import psutil
import pywintypes
import win32con
import win32gui
import win32process
import winxpgui
from PIL import Image

from utils import *


class NotRespondingError(Exception):
    pass


def get_window(title):
    def window_enumeration_handler(hwnd, response):
        if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            proc = psutil.Process(pid)
            if proc.name() == title:
                response.append((hwnd, proc))

    res = []
    win32gui.EnumWindows(window_enumeration_handler, res)
    return res[0] if res else None


class BrawlhallaProcess:
    def __init__(self, hwnd, proc):
        self.window = hwnd
        self.process = proc

    @classmethod
    def find(cls):
        res = get_window('Brawlhalla.exe')
        if not res:
            return None
        return cls(*res)

    @property
    def responding(self):
        cmd = f'tasklist /FI "PID eq {self.process.pid}" /FI "STATUS eq running"'
        status = subprocess.check_output(cmd, creationflags=subprocess.DETACHED_PROCESS)
        return str(self.process.pid) in str(status)

    def kill(self):
        while self.process.is_running():
            self.process.kill()
            sleep(.5)

    def get_window_rect(self):
        return win32gui.GetWindowRect(self.window)

    def get_window_size(self):
        left, top, right, bot = self.get_window_rect()
        return right - left, bot - top

    def get_client_size(self):
        left, top, right, bot = win32gui.GetClientRect(self.window)
        return right - left, bot - top

    @property
    def fullscreen(self):
        return self.get_client_size() == self.get_window_size()

    def resize(self):
        window_size = self.get_window_size()
        client_size = self.get_client_size()
        w_border = window_size[0] - client_size[0]
        h_border = window_size[1] - client_size[1]
        while self.get_client_size() != (1920, 1080):  # getwindowsize or getclientsize or setwindowpos or something else is weird so it sometimes doesnt work first try
            win32gui.SetWindowPos(self.window, 0, 0, 0, 1920 + w_border, 1080 + h_border, win32con.SWP_NOMOVE | win32con.SWP_NOZORDER)

    def move_off_screen(self):
        logger.debug('move_offscreen')
        w, h = Sg.Window.get_screen_size()
        win32gui.SetWindowPos(self.window, 0, w * 4, h * 4, 0, 0, win32con.SWP_NOSIZE | win32con.SWP_NOZORDER)

    def make_transparent(self):
        style = win32gui.GetWindowLong(self.window, win32con.GWL_EXSTYLE)
        win32gui.ShowWindow(self.window, win32con.SW_HIDE)
        style |= win32con.WS_EX_COMPOSITED | win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT | win32con.WS_EX_TOOLWINDOW | win32con.WS_EX_NOACTIVATE
        style &= ~win32con.WS_EX_APPWINDOW
        win32gui.SetWindowLong(self.window, win32con.GWL_EXSTYLE, style)
        sleep(1)
        win32gui.ShowWindow(self.window, win32con.SW_SHOW)
        winxpgui.SetLayeredWindowAttributes(self.window, 0, 0, win32con.LWA_ALPHA)

    def hide(self):
        self.move_off_screen()
        self.make_transparent()

    def make_screenshot(self):
        import win32ui
        w, h = self.get_client_size()

        window_dc = win32gui.GetWindowDC(self.window)
        mfc_dc = win32ui.CreateDCFromHandle(window_dc)
        save_dc = mfc_dc.CreateCompatibleDC()

        save_bit_map = win32ui.CreateBitmap()
        save_bit_map.CreateCompatibleBitmap(mfc_dc, w, h)

        save_dc.SelectObject(save_bit_map)

        ctypes.windll.user32.PrintWindow(self.window, save_dc.GetSafeHdc(), 1)

        bmpinfo = save_bit_map.GetInfo()
        bmpstr = save_bit_map.GetBitmapBits(True)

        im = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)

        win32gui.DeleteObject(save_bit_map.GetHandle())
        save_dc.DeleteDC()
        mfc_dc.DeleteDC()
        win32gui.ReleaseDC(self.window, window_dc)
        return im


class Singleton:
    def __init__(self):
        res = get_window('BHBot.exe')
        if res:
            window, _ = res
            self.set_focus(window)
            sys.exit()

    @staticmethod
    def set_focus(window):
        try:
            win32gui.SetForegroundWindow(window)
        except pywintypes.error:
            pass
