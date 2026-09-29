#!/usr/bin/env python3
"""Closed-vocabulary, cap and calendar check for Continuation 0030.

Every figure is taken from the chapter files on the day it is printed and is
never carried forward from a summary. Word boundaries for the closed list,
and the substring as well for *thank*.
"""
import re, sys, glob, os, datetime as dt

CH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))), 'chapters', 'volume-05')

CLOSED = ['eleven', 'eleventh', 'forty', 'spring', 'winter', 'autumn', 'shed',
          'drawer', 'panel', 'envelope', 'tin', 'bracket', 'rail', 'chair',
          'armchair', 'lamp', 'level', 'comb', 'hose', 'lock-up', 'stone',
          'card', 'warden', 'light', 'permission', 'compact', 'pact',
          'reservation', 'impact', 'reclamation', 'drain', 'bin', 'shelf',
          'rug', 'bottle', 'letterbox', 'handrail']
PHRASES = ['a friday', 'a tuesday', 'four hundred yards', 'a level of service',
           'there is no form in this borough', 'a borrowed city', 'the ninth',
           'nobody is required', 'a load-bearing', 'a key moment',
           'a turning point', 'a pivot', 'in about four years', 'four years',
           'a borough form', 'a boroughed city']
NAMES = ['nacre', 'river stacks', 'halsey cross', 'halse cross', 'jonas',
         'mercer', 'nell', 'ardent', 'tomas', 'renn', 'hanna', 'wray', 'ama',
         'boateng', 'obrero', 'frances', 'tolley', 'royden', 'achebe',
         'naylor', 'wharton', 'calder', 'marcus', 'edin',
         'mcbride', 'krogh', 'albery', 'sallow', 'bram', 'osei',
         'muthoni', 'ezra', 'mbeki', 'trevor', 'nunn', 'evan', 'sparrowhawk']
STEMS = [r'\bdrain', r'\brequir', r'\bthank', r'\bfree\b', r'\bpermit']

BANNED_DAYS = {9, 11}


def caps_count(path):
    raw = open(path, encoding='utf-8').read()
    out = []
    for b in raw.split('\n\n'):
        b = b.strip()
        if not b or b.startswith('# '):
            continue
        if b.upper() == b and re.search(r'[A-Z]', b):
            out.append(b)
    return out


def breaks(path):
    return sum(1 for l in open(path, encoding='utf-8') if l.strip() == '---')


def words(path):
    return len(open(path, encoding='utf-8').read().split())


def dateline(path):
    raw = open(path, encoding='utf-8').read()
    for b in raw.split('\n\n'):
        b = b.strip()
        if re.match(r'^(the\s+)?(monday|tuesday|wednesday|thursday|friday|'
                    r'saturday|sunday)\b', b, re.I) or \
           re.match(r'^\d{1,2}\s+(january|february|march|april|may|june|july|'
                    r'august|september|october|november|december)\b', b, re.I):
            return b
    return None


def main(lo, hi):
    bad = 0
    for i in range(lo, hi + 1):
        p = os.path.join(CH, 'chapter-%04d.md' % i)
        raw = open(p, encoding='utf-8').read()
        low = raw.lower()
        line = '04%d w=%4d caps=%d breaks=%d' % (i, words(p), len(caps_count(p)),
                                                 breaks(p))
        dl = dateline(p)
        line += ' dl=' + (' '.join(dl.split())[:44] if dl else 'NONE')
        print(line)
        if dl is None:
            print('   !! NO DATELINE DETECTED')
            bad += 1
        if len(caps_count(p)) > 5:
            print('   !! CAPS OVER FIVE')
            bad += 1
        if breaks(p) > 2:
            print('   !! SCENE BREAKS OVER CAP OF TWO')
            bad += 1
        for w in CLOSED:
            n = len(re.findall(r'\b' + w + r'\b', low))
            if n:
                print('   !! %s x%d' % (w, n))
                bad += 1
        for w in PHRASES:
            n = low.count(w)
            if n:
                print('   !! phrase %r x%d' % (w, n))
                bad += 1
        for w in NAMES:
            n = len(re.findall(r'\b' + w + r'\b', low))
            if n:
                print('   !! NAME/FLAG %r x%d' % (w, n))
                bad += 1
        for w in STEMS:
            n = len(re.findall(w, low))
            if n:
                print('   !! stem %s x%d' % (w, n))
                bad += 1
        if low.count('tideglass') != 1:
            print('   !! tideglass x%d' % low.count('tideglass'))
            bad += 1
        # day-counts in the body
        for m in re.finditer(r'(one thousand|seven hundred|one thousand five '
                             r'hundred)[^.]{0,80}days', low):
            print('   (day-count?) ...%s...' % m.group(0)[:90])
    print('\nPROBLEMS:', bad)


if __name__ == '__main__':
    main(int(sys.argv[1]), int(sys.argv[2]))
