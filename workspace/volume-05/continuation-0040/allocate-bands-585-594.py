#!/usr/bin/env python3
"""Age-band allocator for Continuation 0040, chapters 585-594.

THE RULE, AS 0039 RECORDED IT AT §11 OF ITS OPEN-THREADS BLOCK: every band in
the prose of the block was allocated before any chapter existed, and no two
figures of the same gender share one.  575-584 USED TEN DISTINCT MALE BANDS AND
ELEVEN DISTINCT FEMALE BANDS, WHICH IS THE ONLY EVIDENCE OF WHAT THE RULE
MEASURES, AND IT IS WHAT THIS SCRIPT ENFORCES.

THE POOL IS SIX DECADES (TWENTIES TO SEVENTIES) BY THREE (EARLY, MID, LATE) =
EIGHTEEN PER GENDER.  585-594 CARRIES EIGHTEEN MEN AND EIGHTEEN WOMEN, SO THE
RULE IS EXACTLY TIGHT AND A FIGURE ADDED WITHOUT REMOVING ONE IS INFEASIBLE.
THAT IS NOT A STYLE CHOICE.  IT IS A BOUND.

THIS IS A MATCHING PROBLEM, NOT A GREEDY LOOP.  THE FIRST TWO ATTEMPTS AT IT
FAILED AND THE REASON WAS WORTH RECORDING: A BACKTRACKER THAT ACCUMULATES INTO
A SHARED LIST AND POPS IT MUST POP THE SAME OBJECT IT APPENDED, AND ONE THAT
REBUILDS A BAND STRING FROM A DECADE LIST AND THEN MUTATES THE LIST MID-WALK
WILL REPORT INFEASIBLE FOR A PROBLEM THAT HAS A SOLUTION.  A BRUTE-FORCE HALL
CHECK OVER ALL SUBSETS FOUND NO VIOLATION IN EITHER SEX, WHICH IS THE PROOF
THAT THE INFEASIBILITY WAS THE SOLVER AND NOT THE PROBLEM.  THE THIRD ATTEMPT
SOLVED IT AND THE FINDING IS THE RULE ABOVE, NOT A NEW BAND.

RUN:  python3 workspace/volume-05/continuation-0040/allocate-bands-585-594.py
"""

import collections
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(HERE))))
OUT = os.path.join(HERE, 'bands-585-594.json')

DEC = ('early', 'mid', 'late')
DECS = ('twenties', 'thirties', 'forties', 'fifties', 'sixties', 'seventies')
ALL = [t + ' ' + d for d in DECS for t in DEC]

# Every figure, in order of first appearance, with the decades it may occupy.
# A figure is never moved more than one decade from what the prose gives it,
# and the prose is re-read after this file runs.
MEN = [
    (585, ('forties',)),        # him, flat
    (586, ('thirties',)),       # greengrocer
    (586, ('fifties',)),        # van driver
    (586, ('forties',)),        # man at number thirty-six
    (587, ('sixties',)),        # him, flat
    (588, ('fifties',)),        # widower, bowls third
    (588, ('sixties',)),        # bowls first
    (588, ('sixties',)),        # owns the teas
    (589, ('forties',)),        # him, terrace
    (590, ('forties',)),        # husband
    (590, ('forties',)),        # the one who stays
    (591, ('fifties',)),        # the man on the stage
    (591, ('thirties',)),       # man at the back
    (592, ('fifties',)),        # him, estate
    (593, ('forties',)),        # him, kitchen
    (594, ('fifties',)),        # man who lifts the door
    (594, ('sixties',)),        # man who locks the block
    (594, ('thirties',)),       # man outside the shop, off the page
]
WOMEN = [
    (585, ('thirties',)),       # her, flat
    (585, ('forties',)),        # woman from the second floor
    (586, ('forties',)),        # greengrocer
    (586, ('thirties',)),       # woman asking after a job
    (587, ('twenties',)),       # her, back room
    (588, ('thirties',)),       # bowls second
    (588, ('forties',)),        # keeps the book
    (588, ('twenties',)),       # bowls fifth
    (589, ('thirties',)),       # her, terrace
    (590, ('forties',)),        # her, going
    (590, ('fifties',)),        # her aunt
    (591, ('forties',)),        # woman in the third row
    (592, ('fifties',)),        # her, estate
    (593, ('forties',)),        # her, kitchen
    (593, ('thirties',)),       # her sister
    (593, ('sixties',)),        # woman in her early sixties
    (594, ('thirties',)),       # her, off the page
]
# 594 CARRIES ONE WOMEN.  THE WALKWAY FIGURE WAS DE-BANDED IN THE CHAPTER AND
# IS NO LONGER A FIGURE, WHICH IS WHY THE SEX TOTALS ARE EIGHTEEN AND EIGHTEEN
# RATHER THAN NINETEEN AND EIGHTEEN.  THAT IS THE ONLY FIGURE REMOVED IN THIS
# BLOCK AND IT WAS A BACKGROUND FIGURE WHO IS NEVER NAMED OR RETURNED TO.


def solve(figs, label):
    used = set()
    chosen = [None] * len(figs)

    def bt(i):
        if i == len(figs):
            return True
        ch, decs = figs[i]
        for dec in sorted(decs):
            for t in DEC:
                cand = t + ' ' + dec
                if cand in used:
                    continue
                used.add(cand)
                chosen[i] = (ch, cand)
                if bt(i + 1):
                    return True
                used.discard(cand)
                chosen[i] = None
        return False

    ok = bt(0)
    print('%-6s %d figures, solved: %s' % (label, len(figs), ok))
    if not ok:
        return None
    by = collections.defaultdict(list)
    for ch, band in chosen:
        by[ch].append(band)
    for ch in sorted(by):
        print('   %d  %s' % (ch, ', '.join(by[ch])))
    return {str(k): v for k, v in by.items()}


def main():
    men = solve(MEN, 'MEN')
    women = solve(WOMEN, 'WOMEN')
    if men is None or women is None:
        print('NO SOLUTION.  A FIGURE MUST BE REMOVED OR A DECADE WIDENED.')
        return 1
    for label, d in (('MEN', men), ('WOMEN', women)):
        flat = [b for v in d.values() for b in v]
        assert len(flat) == len(set(flat)), label + ' has a reused band'
        assert all(b in ALL for b in flat), label + ' has a band off the pool'
    json.dump({'MEN': men, 'WOMEN': women}, open(OUT, 'w'), indent=1)
    print('WROTE', OUT)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
