#!/usr/bin/python
# ~ encoding: utf-8 ~

from __future__ import print_function

import argparse
import logging

from gi import require_version
require_version('Gdk', '3.0')
require_version('Gtk', '3.0')
from gi.repository import Gdk, Gtk, GLib


__version__ = '2.0'

COLUMNS   = 12

EMOTICONS = (
    ('👍', 'THUMBS UP SIGN'),  # 0x1F44D
    ('👎', 'THUMBS DOWN SIGN'),  # 0x1F44E
    ('👏', 'CLAPPING HANDS SIGN'),  # 0x1F44F
    ('🤞', 'HAND WITH INDEX AND MIDDLE FINGERS CROSSED'),  # 0x1F91E
    ('🚩', 'TRIANGULAR FLAG ON POST'),  # 0x1F6A9
    ('🤖', 'ROBOT FACE'),  # 0x1F916
    ('😬', 'GRIMACING FACE'),  # 0x1F62C
    ('😀', 'GRINNING FACE'),  # 0x1F600
    ('😂', 'FACE WITH TEARS OF JOY'),  # 0x1F602
    ('😭', 'LOUDLY CRYING FACE'),  # 0x1F62D
    ('😅', 'SMILING FACE WITH OPEN MOUTH AND COLD SWEAT'),  # 0x1F605
    ('😆', 'SMILING FACE WITH OPEN MOUTH AND TIGHTLY-CLOSED EYES'),  # 0x1F606
    ('😉', 'WINKING FACE'),  # 0x1F609
    ('😎', 'SMILING FACE WITH SUNGLASSES'),  # 0x1F60E
    ('🤔', 'THINKING FACE'),  # 0x1F914
    ('🧐', 'FACE WITH MONOCLE'),  # 0x1F9D0
    ('😐', 'NEUTRAL FACE'),  # 0x1F610
    ('🤐', 'ZIPPER-MOUTH FACE'),  # 0x1F910
    ('😕', 'CONFUSED FACE'),  # 0x1F615
    ('😶', 'FACE WITHOUT MOUTH'),  # 0x1F636
    ('🙃', 'UPSIDE-DOWN FACE'),  # 0x1F643
    ('🤕', 'FACE WITH HEAD-BANDAGE'),  # 0x1F915
    ('🤤', 'DROOLING FACE'),  # 0x1F924
    ('🤯', 'SHOCKED FACE WITH EXPLODING HEAD'),  # 0x1F92F
    ('🙁', 'SLIGHTLY FROWNING FACE'),  # 0x1F641
    ('😮', 'FACE WITH OPEN MOUTH'),  # 0x1F62E
    ('😟', 'WORRIED FACE'),  # 0x1F61F
    ('😳', 'FLUSHED FACE'),  # 0x1F633
    ('😖', 'CONFOUNDED FACE'),  # 0x1F616
    ('😢', 'CRYING FACE'),  # 0x1F622
    ('😥', 'DISAPPOINTED BUT RELIEVED FACE'),  # 0x1F625
    ('😴', 'SLEEPING FACE'),  # 0x1F634
    (r'¯\_(ツ)_/¯', 'shrug'),  # yum install google-noto-sans-japanese-fonts
    (r'ಠ_ಠ', 'look of disapproval'),    # yum install google-noto-sans-kannada-fonts
)

CSS = '''
    .gmoter-window.gmother-window--isPopup {
        border: 1px solid @borders;
    }

    .gmoter-button {
        font-size: 20px;
    }

    .gmoter-button label {
        padding: 10px;
    }

    .gmoter-button:focus,
    .gmoter-button:hover {
        background-color: @theme_selected_bg_color;
        color: @theme_selected_fg_color;
    }
'''

LOG = logging.getLogger('gmoter')  # type: logging.Logger


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--debug', action='store_true', default=True)
    ap.add_argument('--persistent', action='store_true')
    params = ap.parse_args()

    logging.basicConfig(level=logging.DEBUG if params.debug else logging.INFO,
                        format='[%(levelname)-5s] [%(funcName)16s] %(message)s')

    apply_styles()

    win = Window(not params.persistent)

    row = None  # type: Gtk.Box
    for i, (emoticon, name) in enumerate(EMOTICONS):
        if i % COLUMNS == 0:
            row = win.create_row()
        row.add(Button(emoticon, name))

    win.show_all()

    try:
        Gtk.main()
    except KeyboardInterrupt:
        return 0


def apply_styles():
    LOG.debug('Applying CSS styles:\n---\n%s\n---\n', CSS)

    provider = Gtk.CssProvider()
    provider.load_from_data(CSS.encode())

    Gtk.StyleContext.add_provider_for_screen(
        Gdk.Screen.get_default(),
        provider,
        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
    )


def shutdown(*args):
    """
    Dispatches an alternate-thread invocation of main_quit.

    Added because GTK seems to have a problem persisting clipboard data
    if main_quit() is invoked on the same thread as the call to
    Gtk.Clipboard.store(), as seen with PyGObject 3.34.0.
    """

    LOG.info('Shutting down')

    GLib.timeout_add(100, Gtk.main_quit)


class Button(Gtk.EventBox):
    def __init__(self, emoticon, description):
        super(Button, self).__init__()
        self.emoticon = emoticon
        self.description = description

        self.get_style_context().add_class('gmoter-button')
        self.set_can_focus(True)

        label = Gtk.Label(label=emoticon)
        self.add(label)

        self.connect('button_press_event', self.on_click)
        self.connect('enter_notify_event', self.on_hover_in)
        self.connect('key-press-event', self.on_keypress)

    def on_click(self, *args):
        LOG.info('[%s] COPY', self.emoticon)

        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        clipboard.set_text(self.emoticon, -1)
        clipboard.store()

        # Note: Same-thread call to main_quit drops clipboard contents
        shutdown()

    def on_hover_in(self, *args):
        LOG.debug('[%s] hover in', self.emoticon)
        self.grab_focus()

    def on_keypress(self, _, event):
        key_name = Gdk.keyval_name(event.keyval)

        LOG.debug('[%s] keypress: %s', self.emoticon, key_name)

        if key_name in ('space', 'Return'):
            self.on_click()
        elif key_name == 'Escape':
            LOG.info('Exiting')
            shutdown()


class Window(Gtk.Window):
    def __init__(self, popup=True):
        super(Window, self).__init__()

        self.get_style_context().add_class('gmoter-window')

        self.set_title('emoticons v%s' % __version__)
        self.set_keep_above(True)
        self.set_position(Gtk.WindowPosition.CENTER)  # not sure why I even bother... maybe this will work again one day
        self.set_resizable(False)

        self.rows = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(self.rows)

        self.connect('destroy', shutdown)
        self.connect('key-press-event', self.on_keypress)

        if popup:
            self.get_style_context().add_class('gmother-window--isPopup')
            self.set_border_width(1)
            self.set_decorated(False)
            self.connect('focus-out-event', shutdown)

    def create_row(self):
        row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.rows.add(row)
        return row

    def on_keypress(self, _, event):
        key_name = Gdk.keyval_name(event.keyval)
        LOG.debug('[window] keypress: %s', key_name)

        if key_name == 'Escape':
            shutdown()


if __name__ == '__main__':
    exit(main())
