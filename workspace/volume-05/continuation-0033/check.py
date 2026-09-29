#!/usr/bin/env python3
"""Banned-word and filler census for Continuation 0032, chapters 505-514.

Every list here is printed from the cards and from the closed vocabulary.
Run:  python3 workspace/volume-05/continuation-0032/check.py 505 514
"""
import re, sys, os, glob

REPO = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))

GLOBAL_ZERO = [
    'thank', 'eleven', 'eleventh', 'spring', 'winter', 'autumn', 'shed',
    'drawer', 'panel', 'envelope', 'tin', 'bracket', 'rail', 'chair',
    'armchair', 'lamp', 'comb', 'hose', 'lock-up', 'stone', 'card',
    'warden', 'light', 'permission', 'compact', 'pact', 'reservation',
    'impact', 'reclamation', 'bin', 'shelf', 'rug', 'bottle', 'letterbox',
    'handrail', 'level', 'hall', 'counter', 'bisland', 'bollard', 'grate',
    'settee', 'print', 'coping', 'kerb', 'landing', 'machine', 'awning',
    'scoop', 'cat', 'the ninth', 'four years', 'in about four years',
    'a level of service', 'a borrowed city', 'there is no form in this borough',
    'four hundred yards', 'nobody is required', 'a key moment',
    'a turning point', 'a pivot', 'a load-bearing', 'the order',
    'nacre', 'river stacks', 'jonas', 'mercer', 'nell', 'ardent', 'tomas',
    'renn', 'sanaa', 'iqbal', 'iselin', 'krogh', 'bram', 'osei', 'ezra',
    'mbeki', 'trevor', 'nunn', 'blowel', 'albery', 'calloway', 'toll ey',
    'tolley', 'royden', 'achebe', 'naylor', 'wharton', 'collier', 'peverell',
    'hal sey', 'halse', 'halsey', 'wray', 'hanna', 'rowan', 'kestrel',
    'juniper', 'morrow', 'lowglass', 'gantry', 'orange', 'corrance',
    'sink', 'saucer', 'reel', 'mat', 'brass', 'boiler', 'hasp', 'trolley',
    'prop', 'machine', 'coping', 'kerb', 'awning', 'hedge', 'counter',
    'auction', 'invitation', 'saucer',
    'sarn', 'lowdale', 'marcement', 'penhale', 'ravensmere', 'marrowgate',
    'alderwick', 'saint orra', 'saint orra west', 'warden', 'compact',
]

# Chapter-specific bars printed on the ten cards of 0032.
CARD_BARS = {
    505: ['money', 'letter', 'form', 'claim', 'rent', 'repair', 'gate',
          'light', 'bin', 'sign', 'road', 'key', 'van', 'kettle', 'chair',
          'window'],
    506: ['money', 'letter', 'form', 'claim', 'rent', 'repair', 'gate',
          'light', 'bin', 'sign', 'road', 'key', 'van', 'church', 'grave',
          'name'],
    507: ['money', 'letter', 'form', 'claim', 'rent', 'repair', 'gate',
          'light', 'bin', 'sign', 'road', 'key', 'van', 'will', 'death',
          'funeral'],
    508: ['money', 'letter', 'form', 'claim', 'rent', 'repair', 'gate',
          'light', 'bin', 'sign', 'road', 'key', 'van', 'death', 'funeral',
          'will', 'inheritance'],
    509: ['money', 'letter', 'form', 'claim', 'rent', 'repair', 'gate',
          'light', 'bin', 'sign', 'road', 'key', 'van', 'stair', 'landing',
          'banister', 'lift'],
    510: ['money', 'letter', 'form', 'claim', 'rent', 'repair', 'gate',
          'light', 'bin', 'sign', 'road', 'key', 'van', 'queue', 'shop',
          'bus', 'ticket', 'number'],
    511: ['money', 'letter', 'form', 'claim', 'rent', 'repair', 'gate',
          'light', 'bin', 'sign', 'road', 'key', 'van', 'car', 'hedge',
          'wall', 'tree'],
    512: ['money', 'letter', 'form', 'claim', 'rent', 'repair', 'gate',
          'light', 'bin', 'sign', 'road', 'key', 'van', 'lift', 'stair',
          'window', 'name board'],
    513: ['money', 'letter', 'form', 'claim', 'rent', 'repair', 'gate',
          'light', 'bin', 'sign', 'road', 'key', 'van', 'room', 'bed',
          'sofa', 'table', 'a set of keys'],
    514: [],
}

# Objects spent by 495-504 as objects, not only as chapters.
SPENT_495_504 = ['stair', 'stairs', 'staircase', 'stairwell', 'step', 'steps',
                 'doorway', 'doorstep', 'bus stop', 'passage',
                 'telephone box', 'kitchen door', 'table', 'washing line',
                 'shuttering']

# 0032 could not see a flight of STEPS because the list held only STAIR.
# A bar that is only tested at the end is a bar that has already been broken.

# The general barred-object list printed at the foot of the TEN CARDS section
# of PROMPT.md, transcribed whole and in order.  0032 left thirteen of these
# out of the list above, which is how TRAY survived eleven uses in 0507 and
# BED survived three in 0505.  A WRITER OF 0033 COPIES THIS BLOCK RATHER THAN
# SHORTENING IT, AND A CARD MAY NOT BE NARROWED TOWARD THE PROSE AFTERWARDS
# SO AS TO MAKE THE COUNT PASS.
GENERAL_BARRED = [
    'counter', 'lock-up', 'mat', 'sink', 'saucer', 'reel', 'stack of iron',
    'picture frame', 'case', 'blanket', 'stool', 'bed', 'stump', 'fence',
    'bulb', 'clock', 'tray', 'knot', 'rope', 'chair', 'armchair', 'card',
    'bracket', 'drawer', 'envelope', 'stone', 'rug', 'bottle', 'letterbox',
    'handrail',
]

# Motif phrases, capped at twice in a chapter and not counting a dateline.
MOTIFS = ['four hundred yards', 'there is no form in this borough',
          'nobody is required', 'a borrowed city', 'a friday', 'a tuesday']

# Words the account has closed.  Measured on a word boundary and on the
# substring, because a closed word inside a hyphenated compound is still there.
CLOSED = ['thank', 'eleven', 'forty', 'spring', 'winter', 'autumn', 'drain',
          'hose', 'warden', 'jonas', 'mercer', 'nell', 'ardent', 'saucer',
          'sink', 'mat', 'reel', 'stool', 'bulb', 'tray', 'blanket']

FILLER = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight',
          'nine', 'ten', 'twelve', 'twenty', 'thirty', 'forty', 'fifty',
          'sixty', 'seventy', 'eighty', 'ninety']


def read(ch):
    return open(os.path.join(REPO, 'chapters', 'volume-05',
                             'chapter-%04d.md' % ch), encoding='utf-8').read()


def caps_blocks(text):
    out = []
    for block in text.split('\n\n'):
        b = block.strip()
        if b and not b.startswith('# ') and b.upper() == b \
                and re.search(r'[A-Z]', b):
            out.append(b)
    return out


def breaks(text):
    return sum(1 for line in text.splitlines() if line.strip() == '---')


def words(text):
    return len(text.split())


def main():
    lo = int(sys.argv[1]) if len(sys.argv) > 1 else 505
    hi = int(sys.argv[2]) if len(sys.argv) > 2 else 514
    filler_tot = {w: 0 for w in FILLER}
    total_w = 0
    for ch in range(lo, hi + 1):
        t = read(ch)
        low = t.lower()
        body = t
        # count filler on word boundaries in the whole file
        for w in FILLER:
            n = len(re.findall(r'\b%s\b' % w, low))
            filler_tot[w] += n
        bars = list(GLOBAL_ZERO) + GENERAL_BARRED + CARD_BARS.get(ch, []) \
            + SPENT_495_504
        hits = []
        for b in sorted(set(bars)):
            n = len(re.findall(r'\b%s\b' % re.escape(b.lower()), low))
            # "o'clock" is an hour, not the barred object.  Same for
            # "flower bed", which is a border and not the barred furniture.
            n -= len(re.findall(r"o'%s\b" % re.escape(b.lower()), low))
            n -= len(re.findall(r'flower %s\b' % re.escape(b.lower()), low))
            if n > 0:
                hits.append('%s=%d' % (b, n))
        motifs = []
        for m in MOTIFS:
            n = len(re.findall(re.escape(m), low))
            if n:
                motifs.append('%s=%d' % (m, n))
        subs = []
        for b in ('thank', 'forty', 'eleven'):
            n = len(re.findall(b, low))
            if n:
                subs.append('%s substring=%d' % (b, n))
        forty1 = len(re.findall(r'\bforty-one\b|\bforty-two\b', low))
        print('%d  w=%4d  caps=%d  ---=%d  %s'
              % (ch, words(body), len(caps_blocks(t)), breaks(t),
                 ('BARS: ' + ', '.join(hits)) if hits else 'bars 0')
              + ('  || MOTIFS: ' + ', '.join(motifs) if motifs else '')
              + ('  || ' + ', '.join(subs) if subs else '')
              + ('  (forty-one/two: %d)' % forty1 if forty1 else ''))
        total_w += words(body)
    print('TOTAL WORDS', total_w)
    print('FILLER CENSUS:', ', '.join(
        '%s %d' % (w, filler_tot[w]) for w in FILLER))


if __name__ == '__main__':
    main()
