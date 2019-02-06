#!/usr/bin/python3

import argparse
import unicodedata


ap = argparse.ArgumentParser()
ap.add_argument('--start', default='0x1F900')
ap.add_argument('--stop', default='0x1FBFF')
params = ap.parse_args()


start = int(params.start, 16 if 'x' in params.start else 10)
stop = int(params.stop, 16 if 'x' in params.stop else 10)

for n in range(start, stop + 1):
    c    = chr(n)
    name = unicodedata.name(c, '??')

    print("    ('{}', '{}'),  # 0x{:X}".format(c, name, n))
