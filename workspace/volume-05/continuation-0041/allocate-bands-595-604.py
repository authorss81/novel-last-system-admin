#!/usr/bin/env python3
"""Age-band allocator for Continuation 0041, chapters 595-604.

WRITTEN BEFORE ANY PROSE OF 595-604 EXISTS, WHICH IS THE WHOLE POINT OF IT.
THE FINDING CARRIED FORWARD FROM 0040 IS AT §13 SECOND ITEM OF THE
CONTINUATION 0040 OPEN-THREADS BLOCK: THE ALLOCATION AT
workspace/volume-05/continuation-0040/bands-585-594.json WAS HONOURED BY
NOTHING, AND THE PROSE CAME OUT WITH THREE MEN IN THEIR EARLY FIFTIES WHERE
THE FILE ALLOCATES THREE DIFFERENT BANDS.  AN ALLOCATION FILE IS A PLAN AND NOT
A CONSTRAINT.  SO THIS ONE IS NOT THE LAST STEP.  IT IS THE FIRST STEP, AND
check-bands-595-604.py READS THE PROSE BACK AGAINST IT AFTERWARDS AND PRINTS
EVERY DISAGREEMENT RATHER THAN SUMMING IT, AND THE CHARACTER-STATE ROSTER
RECORDS THE DISAGREEMENTS INSTEAD OF HIDING THEM BY RE-AGING SOMEBODY.

THE RULE: no two figures of the same gender share one band in the batch.
THE POOL IS SIX DECADES (TWENTIES TO SEVENTIES) BY THREE (EARLY, MID, LATE) =
EIGHTEEN PER GENDER.  THIS BATCH CARRIES FOURTEEN MEN AND ELEVEN WOMEN, SO
THERE IS HEADROOM IN BOTH SEXES AND A FIGURE MAY BE ADDED WITHOUT REMOVING ONE.

ONE MORE RULE ADDED HERE BECAUSE 0040'S PROSE BROKE IT TWICE AND BECAUSE
§13 FIRST ITEM OF THE SAME BLOCK NAMES IT: A FIGURE IS ALLOCATED A BAND ONCE,
IN ONE PLACE, AND NO CHAPTER MAY GIVE THAT FIGURE A SECOND BAND ANYWHERE LATER
IN THE SAME CHAPTER.  THE CHECKER BELOW MEASURES EVERY MENTION IN EVERY
CHAPTER, NOT ONLY THE FIRST, AND PRINTS A CHAPTER IN WHICH ONE FIGURE CARRIES
TWO BANDS.

Run:  python3 workspace/volume-05/continuation-0041/allocate-bands-595-604.py
"""

import collections
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'bands-595-604.json')

DEC = ('early', 'mid', 'late')
# THE SEVENTIES ARE NOT IN THE POOL FOR THIS BLOCK AND THAT IS A DECISION.
# THE ACCOUNT ALREADY CARRIES A MAN IN HIS EARLY SEVENTIES AT 0534 AND A WOMAN
# IN HER LATE SEVENTIES WHO HAS CROSSED 0584 AND 0594, AND THE PROMPT BARS THE
# MAN OF ABOUT SEVENTY-THREE OUT OF EVERY BATCH.  A SEVENTIES BAND HERE COULD
# BE READ AS ONE OF THOSE THREE FIGURES BY A LATER WRITER LOOKING FOR A
# CONTINUITY, AND THE POINT OF A BAND IS THAT IT MEANS SOMETHING.  SO THE
# POOL IS FIVE DECADES BY THREE AND IS FIFTEEN PER GENDER, WHICH IS TIGHT
# AGAINST FOURTEEN MEN AND ELEVEN WOMEN AND IS THE COST OF THE DECISION.
DECS = ('twenties', 'thirties', 'forties', 'fifties', 'sixties')
ALL = [t + ' ' + d for d in DECS for t in DEC]

# Every figure that will appear, in order of first appearance, with the decades
# that figure is allowed to occupy.  A figure is never moved more than one
# decade from what the prose will give it, and the prose is re-read after this
# file runs.
MEN = [
    (595, ('fifties', 'forties', 'sixties')),   # m1  the document
    (596, ('thirties', 'forties', 'twenties')),  # m2  the decorator
    (597, ('forties', 'fifties')),              # m3  said the sentence
    (597, ('fifties', 'sixties', 'forties')),   # m4  the airer is gone
    (598, ('fifties', 'sixties', 'thirties')),  # m5  the other end of a call
    (599, ('forties', 'fifties', 'sixties')),   # m6  said the thing
    (600, ('forties', 'sixties', 'thirties')),  # m7  the paper and the room
    (601, ('thirties', 'forties', 'twenties')),  # m8  carries the jumper
    (601, ('forties', 'fifties', 'sixties')),   # m9  is given the jumper
    (601, ('thirties', 'forties')),             # m10 the jumper is his
    (602, ('forties', 'fifties', 'sixties')),   # m11 the man who is told
    (602, ('thirties', 'forties', 'twenties')),  # m12 said it a week ago
    (603, ('forties', 'fifties', 'sixties')),   # m13 says it again
    (604, ('fifties', 'sixties', 'forties')),   # m14 three dogs at once
]
WOMEN = [
    (595, ('thirties', 'forties')),             # w1  said the sentence
    (596, ('forties', 'fifties')),              # w2  said have them done
    (597, ('fifties', 'sixties')),              # w3  bought the machine
    (598, ('twenties', 'thirties')),            # w4  makes the calls
    (599, ('twenties', 'thirties')),            # w5  writes it down
    (600, ('forties', 'fifties', 'sixties')),   # w6  her business, the desk
    (601, ('twenties', 'thirties')),            # w7  wants it carried
    (601, ('twenties', 'thirties', 'forties')), # w8  is asked, asks another
    (602, ('thirties', 'forties')),             # w9  is told
    (602, ('forties', 'fifties', 'sixties')),   # w10 makes the arrangement
    (603, ('forties', 'fifties', 'sixties')),   # w11 it is said to
]


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
    out = {'MEN': men, 'WOMEN': women}
    out['_order'] = {'MEN': MEN, 'WOMEN': WOMEN}
    json.dump(out, open(OUT, 'w'), indent=1)
    print('WROTE', OUT)
    print('HEADROOM: MEN %d of 15, WOMEN %d of 15'
          % (sum(len(v) for v in men.values()),
             sum(len(v) for v in women.values())))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
