import contextlib
from typing import Tuple, Optional

import colour

try:
    from .terminalsize import get_terminal_size
except (ModuleNotFoundError, ImportError):
    from terminalsize import get_terminal_size

import colorama
colorama.init()

ESC = '\033'
CLEARFORE = ESC + '[39m'
CLEARBACK = ESC + '[49m'


def color(text, clr: colour.Color, fore=True):
    r, g, b = map(lambda x: int(x * 255), clr.rgb)
    return ESC + '[{fore};2;{r};{g};{b}m{text}'.format(
        r=r, g=g, b=b,
        fore=38 if fore else 48,
        text=text
    )


class VirtualScreenWrap:
    def __enter__(self):
        print(ESC + '[?1049h', end='')

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(ESC + '[?1049l', end='')


class HideCursorFuncWrap:

    def __call__(self, *args, **kwargs):
        print(ESC + '[?25l', end='')

    def __enter__(self):
        self()

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(ESC + '[?25h', end='')


class MoveFuncWrap:
    def __call__(self, row, col):
        print(ESC + '[%d;%dH' % (row, col), end='')

    def __enter__(self):
        print(ESC + '[s', end='')

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(ESC + '[u', end='')


class ColorFuncWrap:
    def __init__(self, fore: Optional[colour.Color], back: Optional[colour.Color]):
        self.fore = fore
        self.back = back

    def __call__(self, *args, end=True):

        string = ' '.join([str(arg) for arg in args])

        if self.fore:
            string = color(string, self.fore, True) + (CLEARFORE if end else '')
        if self.back:
            string = color(string, self.back, False) + (CLEARBACK if end else '')
        return string

    def __enter__(self):
        if self.fore:
            print(color('', self.fore, True), end='')
        if self.back:
            print(color('', self.back, False), end='')

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.fore:
            print(CLEARFORE, end='')
        if self.back:
            print(CLEARBACK, end='')


class Terminal:
    @property
    def width(self):
        return get_terminal_size()[0]

    @property
    def height(self):
        return get_terminal_size()[1]

    @property
    def size(self):
        return get_terminal_size()

    def __getattr__(self, clr: str):

        fore, _, back, = clr.partition('on_')
        fore = fore.strip(' _')
        back = back.strip(' _')

        try:
            if fore:
                fore = colour.Color(fore)
            if back:
                back = colour.Color(back)
        except ValueError:
            raise AttributeError

        wrap = ColorFuncWrap(fore, back)

        setattr(self, clr, wrap)

        return wrap

    def rgb(self, r, g, b):
        color = '#' + ''.join(map(lambda x: hex(x)[2:], (r, g, b)))
        return ColorFuncWrap(colour.Color(color), None)

    def on_rgb(self, r, g, b):
        color = '#{}{}{}'.format(*map(lambda x: ('0' if x < 16 else '') + hex(x)[2:], (r, g, b))).replace(' ', '0')
        return ColorFuncWrap(None, colour.Color(color))

    def scroll(self, row):
        """
        A posive number will move the text up and create space at the bottom.
        A negative will do the opposite.
        """
        if row > 0:
            print(ESC + '[%sS' % row, end='')
        if row < 0:
            print(ESC + '[%sT' % -row, end='')

    move = MoveFuncWrap()

    virtual_screen = VirtualScreenWrap()

    hide_cursor = HideCursorFuncWrap()

    @contextlib.contextmanager
    def mvh(self):
        """Save the cursor location, enter virtual screen and hide the cursor"""
        with self.move:
            with self.virtual_screen:
                with self.hide_cursor:
                    yield
