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
SPENT_495_504 = ['stair', 'doorway', 'doorstep', 'bus stop', 'passage',
                 'telephone box', 'kitchen door', 'table', 'washing line',
                 'shuttering']

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
        bars = list(GLOBAL_ZERO) + CARD_BARS.get(ch, []) + SPENT_495_504
        hits = []
        for b in sorted(set(bars)):
            n = len(re.findall(r'\b%s\b' % re.escape(b.lower()), low))
            if n:
                hits.append('%s=%d' % (b, n))
        subs = []
        for b in ('thank', 'forty', 'eleven'):
            n = len(re.findall(b, low))
            if n:
                subs.append('%s substring=%d' % (b, n))
        forty1 = len(re.findall(r'\bforty-one\b|\bforty-two\b', low))
        print('%d  w=%4d  caps=%d  ---=%d  %s'
              % (ch, words(body), len(caps_blocks(t)), breaks(t),
                 ('BARS: ' + ', '.join(hits)) if hits else 'bars 0')
              + ('  || ' + ', '.join(subs) if subs else '')
              + ('  (forty-one/two: %d)' % forty1 if forty1 else ''))
        total_w += words(body)
    print('TOTAL WORDS', total_w)
    print('FILLER CENSUS:', ', '.join(
        '%s %d' % (w, filler_tot[w]) for w in FILLER))


if __name__ == '__main__':
    main()
