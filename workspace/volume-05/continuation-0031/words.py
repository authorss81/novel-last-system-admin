#!/usr/bin/env python3
"""Barred-object list and the batch filler measure for Continuation 0031.

Two things this repository has no script for, done the cheapest way:
  1. the objects barred from every card and every chapter of this batch
  2. ONE ordinary word counted across all ten chapters at the end, with
     every place reported, because a word spread across ten chapters is
     not a span and no 9-gram run in this repository can see it.
"""
import re, sys, os

CH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))), 'chapters', 'volume-05')

# The barred objects, from the prompt's own list.
BARRED = ['counter', 'lock-up', 'mat', 'sink', 'saucer', 'reel', 'stack of iron',
          'picture frame', 'case', 'blanket', 'stool', 'bed', 'stump', 'fence',
          'bulb', 'clock', 'tray', 'knot', 'rope', 'chair', 'armchair', 'card',
          'bracket', 'drawer', 'envelope', 'stone', 'rug', 'bottle',
          'letterbox', 'handrail']

FILLER = 'twelve'


def main(lo, hi):
    total = 0
    print('== barred objects ==')
    for i in range(lo, hi + 1):
        p = os.path.join(CH, 'chapter-%04d.md' % i)
        if not os.path.exists(p):
            continue
        low = open(p, encoding='utf-8').read().lower()
        for w in BARRED:
            n = len(re.findall(r"(?<![a-z0-9'])" + w + r"(?![a-z0-9'])", low))
            if n:
                print('  04%d  %s x%d' % (i, w, n))
    print('== filler measure: %r ==' % FILLER)
    for i in range(lo, hi + 1):
        p = os.path.join(CH, 'chapter-%04d.md' % i)
        if not os.path.exists(p):
            continue
        raw = open(p, encoding='utf-8').read()
        n = len(re.findall(r"(?<![a-z0-9'])" + FILLER + r"(?![a-z0-9'])", raw.lower()))
        total += n
        print('  04%d  %d' % (i, n))
    print('  TOTAL across the ten: %d' % total)


if __name__ == '__main__':
    main(int(sys.argv[1]), int(sys.argv[2]))
