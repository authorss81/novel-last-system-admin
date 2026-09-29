#!/usr/bin/env python3
"""Shape and closed-figure pass for Continuation 0028, chapters 465-474.

Counts standalone all-caps paragraphs, `---` scene breaks, datelines, word
counts, and every closed or to-be-measured figure. Every figure is taken
from the chapter files on the day it is printed.
"""
import re
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
CH = [os.path.join(REPO, 'chapters', 'volume-05', 'chapter-%04d.md' % i)
      for i in range(465, 475)]

# Words to be measured on word boundaries, plus the substring check on thank.
BOUNDARY = ['eleven', 'eleventh', 'forty', 'spring', 'winter', 'autumn', 'shed',
            'drawer', 'panel', 'envelope', 'tin', 'bracket', 'rail', 'chair',
            'lamp', 'level', 'hall', 'comb', 'hose', 'lock-up', 'stone', 'card',
            'permission', 'compact', 'pact', 'reservation', 'impact',
            'reclamation', 'warden', 'light', 'drain-', 'supervise', 'ticket']
PHRASES = ['a friday', 'a tuesday', 'four hundred yards',
           'there is no form in this borough', 'a level of service',
           'a borrowed city', 'eleven feet by nine', 'a key moment',
           'a turning point', 'a pivot', 'in about four years', 'four years',
           'a load-bearing', 'a form in this borough', 'nacre', 'river stacks',
           'the ninth', '£1,812', 'a grade', 'a department', 'a rota row']
SUBSTR = ['thank', 'nobody is required', 'nothing is required of',
          "nobody's required", 'nobody has to do']


def blocks(raw):
    out = []
    for b in raw.split('\n\n'):
        b = b.strip()
        if b:
            out.append(b)
    return out


def is_caps(b):
    return (not b.startswith('# ')) and b.upper() == b and \
        bool(re.search(r'[A-Z]', b))


def is_dateline(b):
    t = b.lstrip()
    if re.match(r'^(the\s+)?(monday|tuesday|wednesday|thursday|friday|saturday|'
                r'sunday)\b', t, re.I):
        return True
    if re.match(r'^\d{1,2}\s+(january|february|march|april|may|june|july|august|'
                r'september|october|november|december|mon|tue|wed|thu|fri|sat|sun)\b',
                t, re.I):
        return True
    if re.match(r'^(january|february|march|april|may|june|july|august|september|'
                r'october|november|december)\s+\d{1,2}\b', t, re.I):
        return True
    return False


def main():
    tot_words = 0
    print('%-6s %6s %4s %4s %4s %4s' % ('ch', 'words', 'caps', '---', 'dl',
                                         'paras'))
    for p in CH:
        raw = open(p, encoding='utf-8').read()
        bs = blocks(raw)
        caps = sum(1 for b in bs if is_caps(b))
        brk = sum(1 for b in bs if b == '---')
        dl = sum(1 for b in bs if is_dateline(b))
        w = len(raw.split())
        tot_words += w
        print('%-6s %6d %4d %4d %4d %4d' % (p[-8:-3], w, caps, brk, dl,
                                             len(bs)))
    print('TOTAL WORDS (wc -w equivalent, whole file, title included): %d'
          % tot_words)
    print()
    allraw = '\n'.join(open(p, encoding='utf-8').read() for p in CH)
    low = allraw.lower()
    print('-- word boundaries, whole file, datelines included')
    bad = []
    for w in BOUNDARY:
        if w.endswith('-'):
            n = low.count(w)
        else:
            n = len(re.findall(r'\b' + re.escape(w) + r'\b', low))
        if n:
            bad.append((w, n))
    print('  NON-ZERO:', bad if bad else 'none')
    print('-- phrases')
    bad = [(p, low.count(p)) for p in PHRASES if low.count(p)]
    print('  NON-ZERO:', bad if bad else 'none')
    print('-- substrings')
    bad = [(s, low.count(s)) for s in SUBSTR if low.count(s)]
    print('  NON-ZERO:', bad if bad else 'none')
    print('-- per-chapter non-zero, for the ones that are not zero')
    for p in CH:
        t = open(p, encoding='utf-8').read().lower()
        nz = [w for w in BOUNDARY
              if (t.count(w) if w.endswith('-')
                  else len(re.findall(r'\b' + re.escape(w) + r'\b', t)))]
        nzp = [s for s in PHRASES if s in t]
        nzs = [s for s in SUBSTR if s in t]
        if nz or nzp or nzs:
            print('  %s: %s %s %s' % (p[-8:-3], nz, nzp, nzs))
    print()
    print('-- tideglass per chapter (dateline only)')
    for p in CH:
        t = open(p, encoding='utf-8').read().lower()
        n = t.count('tideglass')
        where = 'dateline' if n == 1 and is_dateline(
            [b for b in blocks(open(p, encoding='utf-8').read())
             if 'tideglass' in b.lower()][0]) else 'CHECK'
        print('  %s: %d (%s)' % (p[-8:-3], n, where))


if __name__ == '__main__':
    main()
