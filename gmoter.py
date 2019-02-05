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
    (128070, '👆', 'WHITE UP POINTING BACKHAND INDEX'),
    (128071, '👇', 'WHITE DOWN POINTING BACKHAND INDEX'),
    (128072, '👈', 'WHITE LEFT POINTING BACKHAND INDEX'),
    (128073, '👉', 'WHITE RIGHT POINTING BACKHAND INDEX'),
    (128074, '👊', 'FISTED HAND SIGN'),
    (128075, '👋', 'WAVING HAND SIGN'),
    (128076, '👌', 'OK HAND SIGN'),
    (128077, '👍', 'THUMBS UP SIGN'),
    (128078, '👎', 'THUMBS DOWN SIGN'),
    (128079, '👏', 'CLAPPING HANDS SIGN'),
    (128080, '👐', 'OPEN HANDS SIGN'),

    (128512, '😀', 'GRINNING FACE'),
    (128513, '😁', 'GRINNING FACE WITH SMILING EYES'),
    (128514, '😂', 'FACE WITH TEARS OF JOY'),
    (128515, '😃', 'SMILING FACE WITH OPEN MOUTH'),
    (128516, '😄', 'SMILING FACE WITH OPEN MOUTH AND SMILING EYES'),
    (128517, '😅', 'SMILING FACE WITH OPEN MOUTH AND COLD SWEAT'),
    (128518, '😆', 'SMILING FACE WITH OPEN MOUTH AND TIGHTLY-CLOSED EYES'),
    (128519, '😇', 'SMILING FACE WITH HALO'),
    (128520, '😈', 'SMILING FACE WITH HORNS'),
    (128521, '😉', 'WINKING FACE'),
    (128522, '😊', 'SMILING FACE WITH SMILING EYES'),
    (128523, '😋', 'FACE SAVOURING DELICIOUS FOOD'),
    (128524, '😌', 'RELIEVED FACE'),
    (128525, '😍', 'SMILING FACE WITH HEART-SHAPED EYES'),
    (128526, '😎', 'SMILING FACE WITH SUNGLASSES'),
    (128527, '😏', 'SMIRKING FACE'),
    (128528, '😐', 'NEUTRAL FACE'),
    (128529, '😑', 'EXPRESSIONLESS FACE'),
    (128530, '😒', 'UNAMUSED FACE'),
    (128531, '😓', 'FACE WITH COLD SWEAT'),
    (128532, '😔', 'PENSIVE FACE'),
    (128533, '😕', 'CONFUSED FACE'),
    (128534, '😖', 'CONFOUNDED FACE'),
    (128535, '😗', 'KISSING FACE'),
    (128536, '😘', 'FACE THROWING A KISS'),
    (128537, '😙', 'KISSING FACE WITH SMILING EYES'),
    (128538, '😚', 'KISSING FACE WITH CLOSED EYES'),
    (128539, '😛', 'FACE WITH STUCK-OUT TONGUE'),
    (128540, '😜', 'FACE WITH STUCK-OUT TONGUE AND WINKING EYE'),
    (128541, '😝', 'FACE WITH STUCK-OUT TONGUE AND TIGHTLY-CLOSED EYES'),
    (128542, '😞', 'DISAPPOINTED FACE'),
    (128543, '😟', 'WORRIED FACE'),
    (128544, '😠', 'ANGRY FACE'),
    (128545, '😡', 'POUTING FACE'),
    (128546, '😢', 'CRYING FACE'),
    (128547, '😣', 'PERSEVERING FACE'),
    (128548, '😤', 'FACE WITH LOOK OF TRIUMPH'),
    (128549, '😥', 'DISAPPOINTED BUT RELIEVED FACE'),
    (128550, '😦', 'FROWNING FACE WITH OPEN MOUTH'),
    (128551, '😧', 'ANGUISHED FACE'),
    (128552, '😨', 'FEARFUL FACE'),
    (128553, '😩', 'WEARY FACE'),
    (128554, '😪', 'SLEEPY FACE'),
    (128555, '😫', 'TIRED FACE'),
    (128556, '😬', 'GRIMACING FACE'),
    (128557, '😭', 'LOUDLY CRYING FACE'),
    (128558, '😮', 'FACE WITH OPEN MOUTH'),
    (128559, '😯', 'HUSHED FACE'),
    (128560, '😰', 'FACE WITH OPEN MOUTH AND COLD SWEAT'),
    (128561, '😱', 'FACE SCREAMING IN FEAR'),
    (128562, '😲', 'ASTONISHED FACE'),
    (128563, '😳', 'FLUSHED FACE'),
    (128564, '😴', 'SLEEPING FACE'),
    (128565, '😵', 'DIZZY FACE'),
    (128566, '😶', 'FACE WITHOUT MOUTH'),
    (128567, '😷', 'FACE WITH MEDICAL MASK'),
    (128568, '😸', 'GRINNING CAT FACE WITH SMILING EYES'),
    (128569, '😹', 'CAT FACE WITH TEARS OF JOY'),
    (128570, '😺', 'SMILING CAT FACE WITH OPEN MOUTH'),
    (128571, '😻', 'SMILING CAT FACE WITH HEART-SHAPED EYES'),
    (128572, '😼', 'CAT FACE WITH WRY SMILE'),
    (128573, '😽', 'KISSING CAT FACE WITH CLOSED EYES'),
    (128574, '😾', 'POUTING CAT FACE'),
    (128575, '😿', 'CRYING CAT FACE'),
    (128576, '🙀', 'WEARY CAT FACE'),
    (128577, '🙁', 'SLIGHTLY FROWNING FACE'),
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
    win.connect('destroy', gtk.main_quit)
    win.set_title('emoticons v%s' % __version__)
    win.set_keep_above(True)
    win.set_position(gtk.WIN_POS_MOUSE)
    win.set_geometry_hints(min_width=width, min_height=height)

    win.connect('key-press-event', on_keypress)

    rows = gtk.VBox()

    clipboard = gtk.Clipboard()

    row = None  # type: gtk.HButtonBox
    for i, (_, emoticon, name) in enumerate(EMOTICONS):
        if i % COLUMNS == 0:
            row = gtk.HBox()
            rows.add(row)

        button = gtk.Button(emoticon)
        button.connect('clicked', on_button_click, clipboard, emoticon)
        row.pack_start(button)

    win.set_resizable(False)
    win.add(rows)
    win.show_all()

    try:
        gtk.main()
    except KeyboardInterrupt:
        exit(1)


def on_button_click(btn, clipboard, emoticon):
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
