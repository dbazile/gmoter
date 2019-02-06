#!/usr/bin/python
# ~ encoding: utf-8 ~

from __future__ import print_function

import logging

import gtk
import pango


__version__ = '1.0'

COLUMNS   = 12
CELL_SIZE = 50

EMOTICONS = (
    ('👍', 'THUMBS UP SIGN'),  # 0x1F44D
    ('👎', 'THUMBS DOWN SIGN'),  # 0x1F44E
    ('👏', 'CLAPPING HANDS SIGN'),  # 0x1F44F
    ('🤞', 'HAND WITH INDEX AND MIDDLE FINGERS CROSSED'),  # 0x1F91E
    ('🚩', 'TRIANGULAR FLAG ON POST'),  # 0x1F6A9
    ('🤖', 'ROBOT FACE'),  # 0x1F916
    ('😀', 'GRINNING FACE'),  # 0x1F600
    ('😂', 'FACE WITH TEARS OF JOY'),  # 0x1F602
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
)

LOG = logging.getLogger('gmoter')  # type: logging.Logger


def main():
    # TODO -- type name to filter

    logging.basicConfig(level=logging.DEBUG,
                        format='[%(levelname)-5s] [%(funcName)16s] %(message)s')

    width = CELL_SIZE * COLUMNS
    height = CELL_SIZE * int(round(len(EMOTICONS) / COLUMNS))

    LOG.info('Dimensions: %dx%d', width, height)

    win = gtk.Window()
    win.set_title('emoticons v%s' % __version__)
    win.set_keep_above(True)
    win.set_position(gtk.WIN_POS_MOUSE)
    win.set_geometry_hints(min_width=width, min_height=height)
    win.set_resizable(False)

    win.connect('destroy', gtk.main_quit)

    rows = gtk.VBox()
    win.add(rows)

    colors = get_colors()

    row = None  # type: gtk.HButtonBox
    for i, (emoticon, name) in enumerate(EMOTICONS):
        if i % COLUMNS == 0:
            row = gtk.HBox()
            rows.pack_start(row)

        button = Button(emoticon, name, colors)

        row.pack_start(button)

    win.show_all()

    try:
        gtk.main()
    except KeyboardInterrupt:
        exit(1)


def get_colors():
    settings = gtk.settings_get_default()  # type: gtk.Settings
    raw = settings.get_property('gtk-color-scheme').strip()  # type: str
    LOG.debug('gtk-color-scheme:\n'
              '---\n'
              '%s\n'
              '---',
              raw)

    items = {}
    for line in raw.split('\n'):
        k, v = line.lower().split(':')
        items[k.strip()] = gtk.gdk.Color(v.strip())
    return items


class Button(gtk.EventBox):
    def __init__(self, emoticon, description, colors):
        super(Button, self).__init__()
        self.emoticon = emoticon
        self.description = description
        self.colors = colors

        self.set_bgcolor()
        self.set_can_focus(True)
        self.set_activate_signal

        label = gtk.Label(emoticon)
        label.modify_font(pango.FontDescription('16'))
        self.add(label)

        self.connect('button_press_event', self.on_click)
        self.connect('enter_notify_event', self.on_hover_in)
        # self.connect('leave_notify_event', self.on_hover_out)
        self.connect('key-press-event', self.on_keypress)
        self.connect('focus-in-event', self.on_focus)
        self.connect('focus-out-event', self.on_blur)

    def on_blur(self, *args):
        LOG.info('[%s] blur', self.emoticon)
        self.set_bgcolor()

    def on_click(self, *args):
        LOG.info('Copy: %s', self.emoticon)
        clipboard = gtk.Clipboard()
        clipboard.set_text(self.emoticon)
        clipboard.store()
        gtk.main_quit()

    def on_focus(self, *args):
        LOG.info('[%s] focus', self.emoticon)
        self.set_bgcolor('selected_bg_color')

    def on_hover_in(self, *args):
        LOG.info('[%s] hover in', self.emoticon)
        self.grab_focus()

    def on_keypress(self, _, event):
        key_name = gtk.gdk.keyval_name(event.keyval)
        LOG.info('[%s] keypress: %s', self.emoticon, key_name)

        if key_name in ('space', 'Return'):
            self.on_click()
        elif key_name == 'Escape':
            LOG.info('Exiting')
            gtk.main_quit()

    def set_bgcolor(self, name='base_color'):
        self.modify_bg(gtk.STATE_NORMAL, self.colors.get(name))


if __name__ == '__main__':
    main()
