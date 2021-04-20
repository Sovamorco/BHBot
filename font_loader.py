import ctypes

from fontTools.ttLib import TTFont

FONT_SPECIFIER_NAME_ID = 4


def get_font_name(file):
    font = TTFont(file)
    name = ''
    for record in font['name'].names:
        if b'\x00' in record.string:
            name_str = record.string.decode('utf-16-be')
        else:
            name_str = record.string.decode('utf-8')
        if record.nameID == FONT_SPECIFIER_NAME_ID and not name:
            return name_str
    return ''


def load_font(fontpath):
    flags = 0x10 | 0x20
    num_fonts_added = ctypes.windll.gdi32.AddFontResourceExW(ctypes.byref(ctypes.create_unicode_buffer(fontpath)), flags, 0)
    return bool(num_fonts_added)
