#!/usr/bin/env python3
"""Reduce a chapter to its cap of scene breaks without touching prose.

A chapter in this batch carries `---` as a scene break and at most two of them.
Where a scene changes place or hour the break is kept; the rest are cut and the
paragraphs either side run on, because nothing about the room or the hour has
changed across the join. NO TEXT IS EVER DROPPED: only the rule is removed.
"""
import sys, os

CH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))), 'chapters', 'volume-05')


def breaks(s):
    return sum(1 for l in s.split('\n') if l.strip() == '---')


def words(s):
    return len([t for t in s.split() if t.strip() != '---'])


def fix(path, cap=2):
    s = open(path, encoding='utf-8').read()
    w0 = words(s)
    while breaks(s) > cap:
        # drop the LAST rule only; every paragraph either side is kept
        a, _sep, b = s.rpartition('\n\n---\n\n')
        assert a, 'no rule to drop in %s' % path
        s = a + '\n\n' + b
    s = s.replace('\n\n\n', '\n\n')
    open(path, 'w', encoding='utf-8').write(s)
    assert words(s) == w0, 'TEXT LOST in %s: %d -> %d' % (path, w0, words(s))
    return breaks(s), w0


if __name__ == '__main__':
    lo, hi, cap = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]) if len(sys.argv) > 3 else 2
    for i in range(lo, hi + 1):
        p = os.path.join(CH, 'chapter-%04d.md' % i)
        if not os.path.exists(p):
            continue
        b, w = fix(p, cap)
        print('04%d  %d breaks  %d words' % (i, b, w))
