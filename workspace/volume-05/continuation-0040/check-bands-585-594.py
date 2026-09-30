#!/usr/bin/env python3
"""Age-band allocator and verifier for Continuation 0040, chapters 585-594.

COPIED IN METHOD FROM 0039's practice, WHICH IS DESCRIBED AT §11 OF THE 0039
OPEN-THREADS BLOCK: every band in the prose of the block was allocated before
any chapter existed and no two figures of the same gender shared one.  575-584
USED TEN DISTINCT MALE BANDS AND ELEVEN DISTINCT FEMALE BANDS, WHICH IS THE
ONLY EVIDENCE OF WHAT THE RULE MEASURES AND IS WHAT THIS SCRIPT CHECKS.

THE POOL IS SIX DECADES (TWENTIES TO SEVENTIES) BY THREE (EARLY, MID, LATE)
= EIGHTEEN PER GENDER.  THE BATCH CARRIES EIGHTEEN MEN AND EIGHTEEN WOMEN, SO
THE RULE IS TIGHT AND A FIGURE ADDED WITHOUT REMOVING ONE IS INFEASIBLE.

RUN:  python3 workspace/volume-05/continuation-0040/check-bands-585-594.py
"""

import json
import os
import re
import sys
import collections

HERE = os.path.dirname(os.path.abspath(__file__))
# HERE IS ALREADY A DIRECTORY (continuation-0040).  THREE dirnames WALK
# continuation-0040 -> volume-05 -> workspace -> REPO ROOT.  THE 0039 COPY OF
# THIS SCRIPT APPLIED FOUR AND LANDED ON THE REPO'S PARENT, WHICH IS WHY IT
# FOUND NO CHAPTERS AND PRINTED OK.  FIXED 0040.
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
BANDS_JSON = os.path.join(HERE, 'bands-585-594.json')
LO, HI = 585, 594

# The forms a band takes in this account's prose.  Every one of these was found
# in 575-584 and none of them is new here.
BAND_RE = re.compile(
    r'\b(?:[Tt]he |a )?(man|woman)\b'
    r'[^.\n]{0,24}?\b(?:in|of) (?:his|her) '
    r'(early|mid|late) (twenties|thirties|forties|fifties|sixties|seventies)\b')


def read(ch):
    p = os.path.join(REPO, 'chapters', 'volume-05',
                     'chapter-%04d.md' % ch)
    if not os.path.exists(p):
        return None
    return open(p, encoding='utf-8').read()


def bands_in(text):
    """Return {'M': [band...], 'F': [band...]} in order of first appearance."""
    out = {'M': [], 'F': []}
    for m in BAND_RE.finditer(text):
        g = 'M' if m.group(1) == 'man' else 'F'
        b = '%s %s' % (m.group(2), m.group(3))
        if b not in out[g]:
            out[g].append(b)
    return out


def main():
    plan = json.load(open(BANDS_JSON))
    ok = True

    print('-- THE ALLOCATION AS A TABLE (allocated before the prose)')
    for g, label in (('MEN', 'MEN'), ('WOMEN', 'WOMEN')):
        n = sum(len(v) for v in plan[g].values())
        print('  %s: %d figures' % (label, n))
        for ch in sorted(plan[g], key=int):
            print('    %s  %s' % (ch, ', '.join(plan[g][ch])))

    # 1. THE PLAN ITSELF: no band used twice in the same gender.
    print('\n-- CHECK ONE: the plan has no band twice, per gender')
    for g, label in (('MEN', 'MEN'), ('WOMEN', 'WOMEN')):
        seen = collections.Counter()
        for ch, bs in plan[g].items():
            for b in bs:
                seen[b] += 1
        dupes = {b: c for b, c in seen.items() if c > 1}
        if dupes:
            ok = False
            print('  %s: REUSED %s' % (label, dupes))
        else:
            print('  %s: %d distinct bands, none reused' % (label, len(seen)))

    # 2. THE CHAPTERS AGAINST THE PLAN.
    print('\n-- CHECK TWO: the chapters carry exactly the planned bands')
    missing = []
    for ch in range(LO, HI + 1):
        t = read(ch)
        if t is None:
            missing.append(ch)
            continue
        found = bands_in(t)
        for g, label in (('M', 'MEN'), ('F', 'WOMEN')):
            want = list(plan[label][str(ch)])
            got = found[g]
            if want != got:
                ok = False
                print('  %d %s: PLANNED %s  ON THE PAGE %s'
                      % (ch, label, want, got))
    if not missing:
        print('  all ten present and, where they agree, silent; '
              'any disagreement is printed above')

    # 3. THE TOTALS AGAINST THE POOL.
    print('\n-- CHECK THREE: the figures fit the pool of eighteen per gender')
    for g, label in (('MEN', 'MEN'), ('WOMEN', 'WOMEN')):
        n = sum(len(v) for v in plan[g].values())
        print('  %s: %d figures against 18 bands, headroom %d'
              % (label, n, 18 - n))
        if n > 18:
            ok = False

    # 4. THE BANNED-WORD LIST IS NOT A BAND LIST.  A BAND MAY NOT BE SPELLED
    #    WITH A FIGURE HEAD THAT READS AS A NARRATOR.
    print('\n-- CHECK FOUR: no figure is given a personal name in this batch')
    name_re = re.compile(r'\b(?:Mr|Mrs|Ms|Miss|Dr)\.? [A-Z]')
    named = 0
    for ch in range(LO, HI + 1):
        t = read(ch)
        if t and name_re.search(t):
            ok = False
            named += 1
            print('  %d: a titled personal name' % ch)
    print('  titled names across the ten: %d' % named)

    if missing:
        ok = False
        print('MISSING CHAPTERS (%d): %s' % (len(missing), missing))

    print('\nVERDICT', 'OK' if ok else 'NOT OK — RECHECK THE TABLE')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
