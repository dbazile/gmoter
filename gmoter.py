#!/usr/bin/python
# ~ encoding: utf-8 ~
#
# gmoter.py
#
# Written in Python 2 since CentOS and Fedora install pygtk2 by default
# (my attempt to keep this script dependency-free).
#

from __future__ import print_function

import logging

import gtk


__version__ = '1.0'

COLUMNS = 12
CELL_SIZE = 60

EMOTICONS = (
    ('👆', 'WHITE UP POINTING BACKHAND INDEX'),
    ('👇', 'WHITE DOWN POINTING BACKHAND INDEX'),
    ('👈', 'WHITE LEFT POINTING BACKHAND INDEX'),
    ('👉', 'WHITE RIGHT POINTING BACKHAND INDEX'),
    ('👊', 'FISTED HAND SIGN'),
    ('👋', 'WAVING HAND SIGN'),
    ('👌', 'OK HAND SIGN'),
    ('👍', 'THUMBS UP SIGN'),
    ('👎', 'THUMBS DOWN SIGN'),
    ('👏', 'CLAPPING HANDS SIGN'),
    ('👐', 'OPEN HANDS SIGN'),

    ('😀', 'GRINNING FACE'),
    ('😁', 'GRINNING FACE WITH SMILING EYES'),
    ('😂', 'FACE WITH TEARS OF JOY'),
    ('😃', 'SMILING FACE WITH OPEN MOUTH'),
    ('😄', 'SMILING FACE WITH OPEN MOUTH AND SMILING EYES'),
    ('😅', 'SMILING FACE WITH OPEN MOUTH AND COLD SWEAT'),
    ('😆', 'SMILING FACE WITH OPEN MOUTH AND TIGHTLY-CLOSED EYES'),
    ('😇', 'SMILING FACE WITH HALO'),
    ('😈', 'SMILING FACE WITH HORNS'),
    ('😉', 'WINKING FACE'),
    ('😊', 'SMILING FACE WITH SMILING EYES'),
    ('😋', 'FACE SAVOURING DELICIOUS FOOD'),
    ('😌', 'RELIEVED FACE'),
    ('😍', 'SMILING FACE WITH HEART-SHAPED EYES'),
    ('😎', 'SMILING FACE WITH SUNGLASSES'),
    ('😏', 'SMIRKING FACE'),
    ('😐', 'NEUTRAL FACE'),
    ('😑', 'EXPRESSIONLESS FACE'),
    ('😒', 'UNAMUSED FACE'),
    ('😓', 'FACE WITH COLD SWEAT'),
    ('😔', 'PENSIVE FACE'),
    ('😕', 'CONFUSED FACE'),
    ('😖', 'CONFOUNDED FACE'),
    ('😗', 'KISSING FACE'),
    ('😘', 'FACE THROWING A KISS'),
    ('😙', 'KISSING FACE WITH SMILING EYES'),
    ('😚', 'KISSING FACE WITH CLOSED EYES'),
    ('😛', 'FACE WITH STUCK-OUT TONGUE'),
    ('😜', 'FACE WITH STUCK-OUT TONGUE AND WINKING EYE'),
    ('😝', 'FACE WITH STUCK-OUT TONGUE AND TIGHTLY-CLOSED EYES'),
    ('😞', 'DISAPPOINTED FACE'),
    ('😟', 'WORRIED FACE'),
    ('😠', 'ANGRY FACE'),
    ('😡', 'POUTING FACE'),
    ('😢', 'CRYING FACE'),
    ('😣', 'PERSEVERING FACE'),
    ('😤', 'FACE WITH LOOK OF TRIUMPH'),
    ('😥', 'DISAPPOINTED BUT RELIEVED FACE'),
    ('😦', 'FROWNING FACE WITH OPEN MOUTH'),
    ('😧', 'ANGUISHED FACE'),
    ('😨', 'FEARFUL FACE'),
    ('😩', 'WEARY FACE'),
    ('😪', 'SLEEPY FACE'),
    ('😫', 'TIRED FACE'),
    ('😬', 'GRIMACING FACE'),
    ('😭', 'LOUDLY CRYING FACE'),
    ('😮', 'FACE WITH OPEN MOUTH'),
    ('😯', 'HUSHED FACE'),
    ('😰', 'FACE WITH OPEN MOUTH AND COLD SWEAT'),
    ('😱', 'FACE SCREAMING IN FEAR'),
    ('😲', 'ASTONISHED FACE'),
    ('😳', 'FLUSHED FACE'),
    ('😴', 'SLEEPING FACE'),
    ('😵', 'DIZZY FACE'),
    ('😶', 'FACE WITHOUT MOUTH'),
    ('😷', 'FACE WITH MEDICAL MASK'),
    ('😸', 'GRINNING CAT FACE WITH SMILING EYES'),
    ('😹', 'CAT FACE WITH TEARS OF JOY'),
    ('😺', 'SMILING CAT FACE WITH OPEN MOUTH'),
    ('😻', 'SMILING CAT FACE WITH HEART-SHAPED EYES'),
    ('😼', 'CAT FACE WITH WRY SMILE'),
    ('😽', 'KISSING CAT FACE WITH CLOSED EYES'),
    ('😾', 'POUTING CAT FACE'),
    ('😿', 'CRYING CAT FACE'),
    ('🙀', 'WEARY CAT FACE'),
    ('🙁', 'SLIGHTLY FROWNING FACE'),
)

LOG = logging.getLogger('gmoter')


def main():
    # TODO -- type name to filter
    # TODO -- onfocus, change colors

    logging.basicConfig(level=logging.DEBUG,
                        format='[%(levelname)s] [%(funcName)s] %(message)s')

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
    win.connect('key-press-event', on_keypress)

    rows = gtk.VBox()
    win.add(rows)

    clipboard = gtk.Clipboard()

    row = None  # type: gtk.HButtonBox
    for i, (emoticon, name) in enumerate(EMOTICONS):
        if i % COLUMNS == 0:
            row = gtk.HBox()
            rows.pack_start(row)

        def ebhover(button, event):
            button.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color('#ff0'))

        def ebblur(button, event):
            button.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color('#fff'))

        eb = gtk.EventBox()
        eb.connect('button_press_event', on_button_click, clipboard, emoticon)
        eb.connect('enter_notify_event', ebhover)
        eb.connect('leave_notify_event', ebblur)
        eb.add(gtk.Label(emoticon))
        row.add(eb)
        # button = gtk.Button(emoticon)
        # button.connect('clicked', on_button_click, clipboard, emoticon)
        # button.set_border_width(-1)
        # row.pack_start(button)

    win.show_all()

    try:
        gtk.main()
    except KeyboardInterrupt:
        exit(1)


def on_button_click(btn, event, clipboard, emoticon):
    LOG.info('Copy: %s', emoticon)
    clipboard.set_text(emoticon)
    clipboard.store()
    gtk.main_quit()


def on_keypress(window, event):
    key_name = gtk.gdk.keyval_name(event.keyval)
    LOG.info('Key press: %s', key_name)
    if key_name == 'Escape':
        LOG.info('Exiting')
        gtk.main_quit()


if __name__ == '__main__':
    main()
