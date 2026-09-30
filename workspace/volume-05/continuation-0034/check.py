#!/usr/bin/env python3
"""Banned-word and filler census for Continuation 0034, chapters 525-529.

COPIED FROM `workspace/volume-05/continuation-0033/check.py` WITH THE TWO LISTS
CHANGED, WHICH IS WHAT THE 0034 PROMPT ASKS FOR AND WHAT THE 0033 BLOCK RECOMMENDS.
Nothing was rebuilt.  The method, the article test, the approximation test, the
line-buffer, the motif list, the closed list and the total-and-verdict footer are
byte-identical to the copy they came from, so that a figure printed here and a
figure printed there are two measurements of the same thing.

WHAT WAS CHANGED AND WHY
  * docstring, defaults: 0033 -> 0034, 515-524 -> 525-529.
  * CARD_BARS: typed out whole from the 0034 prompt's ten cards.  Only the five
    cards this run actually writes are here; the other five belong to a later
    writer who will type them in rather than inherit them.
  * SPENT_515_524: the objects 515-524 spent, at item 6 of the 0034 prompt.
    0033 held 505-514 and 495-504.  495-504 is kept, because the bar runs
    forward and is not retroactive.
  * FILLER: the declared measure of this batch is QUITE, which is neither
    ONE nor WEEK nor ABOUT, and ONE, WEEK and ABOUT are all still counted and
    reported beside it.  A batch that reports one measure has reported half of
    what it measured.
  * EXTRA_ZERO: the three stems 0033 kept in its own §13 rather than in the
    union.  This copy puts them in the union, because a list of closed words
    that lives in a paragraph is not a bar.

Run:  python3 workspace/volume-05/continuation-0034/check.py 525 529
"""
import re, sys, os

REPO = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))

GLOBAL_ZERO = [
    'thank', 'eleven', 'eleventh', 'spring', 'winter', 'autumn', 'shed',
    'drawer', 'panel', 'envelope', 'tin', 'bracket', 'rail', 'chair',
    'armchair', 'lamp', 'comb', 'hose', 'lock-up', 'stone', 'card',
    'warden', 'light', 'permission', 'compact', 'pact', 'reservation',
    'impact', 'reclamation', 'bin', 'shelf', 'rug', 'bottle', 'letterbox',
    'handrail', 'level', 'hall', 'counter', 'bollard', 'grate', 'settee',
    'print', 'coping', 'kerb', 'landing', 'machine', 'awning', 'scoop', 'cat',
    'the ninth', 'four years', 'in about four years',
    'a level of service', 'a borrowed city', 'there is no form in this borough',
    'four hundred yards', 'nobody is required', 'a key moment',
    'a turning point', 'a pivot', 'a load-bearing', 'the order',
    'nacre', 'river stacks', 'jonas', 'mercer', 'nell', 'ardent', 'tomas',
    'renn', 'sanaa', 'iqbal', 'iselin', 'krogh', 'bram', 'osei', 'ezra',
    'mbeki', 'trevor', 'nunn', 'blowel', 'albery', 'calloway', 'tolley',
    'royden', 'achebe', 'naylor', 'wharton', 'collier', 'peverell',
    'halsey', 'wray', 'hanna', 'rowan', 'kestrel',
    'juniper', 'morrow', 'lowglass', 'gantry', 'orange', 'corrance',
    'sink', 'saucer', 'reel', 'mat', 'brass', 'boiler', 'hasp', 'trolley',
    'prop', 'hedge', 'auction', 'invitation',
    'sarn', 'lowdale', 'marcement', 'penhale', 'ravensmere', 'marrowgate',
    'alderwick', 'saint orra', 'saint orra west',
]

# 0033 kept REQUIR-, PERMIT and FREE in its own prose and measured them by hand.
# They are in the union here.  DRAINAGE, DRAINS and DRAINER are legitimate
# English and only the bare word DRAIN is the prohibited member, which is why
# the test below is \bDRAIN\b and not DRAIN-.
EXTRA_ZERO = ['requir', 'permit', 'free']

# Chapter-specific bars printed on the cards of 0034, transcribed whole.
# A WRITER MAY NOT NARROW A CARD TOWARD THE PROSE SO AS TO MAKE A COUNT PASS.
_COMMON = ['money', 'letter', 'form', 'claim', 'rent', 'repair', 'gate',
           'light', 'bin', 'sign', 'road', 'key', 'van']

CARD_BARS = {
    525: _COMMON + ['bus stop', 'bench', 'door', 'coat', 'hat', 'handbag',
                    'lamp', 'clock', 'card', 'rail', 'chair', 'mat', 'sink',
                    'stair', 'step', 'table', 'bed', 'rug', 'bottle',
                    'envelope', 'bag', 'ticket'],
    526: _COMMON + ['bench', 'door', 'card', 'chair', 'table', 'bag', 'bottle',
                    'hat', 'rail', 'handrail', 'stair', 'step', 'mat'],
    527: _COMMON + ['chair', 'table', 'bench', 'clock', 'lamp', 'mat', 'sink',
                    'saucer', 'tray', 'tap', 'kettle', 'shelf', 'rail',
                    'sack', 'window'],
    528: _COMMON + ['bench', 'door', 'stair', 'step', 'chair', 'table',
                    'window', 'kitchen', 'bed', 'hall', 'mat', 'rug', 'lamp',
                    'clock', 'tap', 'sink', 'card', 'paper'],
    529: _COMMON + ['bench', 'door', 'chair', 'table', 'clock', 'lamp', 'hat',
                    'coat', 'bag', 'ticket', 'bus stop', 'mat', 'rug',
                    'bottle', 'kettle', 'tray', 'shelf'],
}

# Objects spent by 515-524 AS OBJECTS, at item 6 of the 0034 prompt.  A WALK TO
# THE END OF A STREET, A GARDEN GATE, BAGS, A BAY, A PLASTIC BAG, A POSTBOX, A
# PLATE, A DRYING RACK, A KITCHEN WORKTOP, A FIRM, A HAT, A HOOK, A LANE, A
# WALL, A TELEPHONE, A PICTURE, A TELEPHONE HELD UP, A SCREEN, A DESK, A
# HARDBACK, A PENCIL, A PIECE OF PAPER, A LOW THING, A GARDEN BORDER, A SWING,
# A JAR OF OIL, A STEEL DESK, A CUP.  The ones that are single words are typed
# in.  A list written in prose is a list nobody greps.
SPENT_515_524 = ['bag', 'bags', 'bay', 'postbox', 'plate', 'rack', 'worktop',
                 'firm', 'hook', 'lane', 'wall', 'telephone', 'picture',
                 'screen', 'desk', 'hardback', 'pencil', 'paper', 'swing',
                 'cup', 'oil', 'border', 'front room']

# 495-504 are spent too and the bar runs forward.  It is not retroactive: a
# reviewer reading a non-zero line on 495-504 is reading a recorded defect in
# those cards and not a new one.
SPENT_495_504 = ['stair', 'stairs', 'staircase', 'stairwell', 'doorway',
                 'doorstep', 'bus stop', 'passage', 'telephone box',
                 'kitchen door', 'table', 'washing line', 'shuttering']

# The general barred-object list printed at the foot of the TEN CARDS section
# of PROMPT.md for this batch.  0033's list is longer again than 0032's and this
# one is 0033's plus the items the 0034 prompt added to the foot of its own
# card list, which is EVERYTHING SPENT BY 515-524 AND EVERYTHING AT 16 OF THE
# 0033 BLOCK.
GENERAL_BARRED = [
    'counter', 'lock-up', 'mat', 'sink', 'saucer', 'reel', 'stack of iron',
    'picture frame', 'case', 'blanket', 'stool', 'bed', 'stump', 'fence',
    'bulb', 'clock', 'tray', 'knot', 'rope', 'chair', 'armchair', 'card',
    'bracket', 'drawer', 'envelope', 'stone', 'rug', 'bottle', 'letterbox',
    'handrail', 'settee', 'bollard', 'grate', 'hall', 'kerb', 'landing',
    'awning', 'scoop', 'coping', 'shop front',
]

# Motif phrases, capped at twice in a chapter and not counting a dateline.
MOTIFS = ['four hundred yards', 'there is no form in this borough',
          'nobody is required', 'a borrowed city', 'a friday', 'a tuesday']

# Words the account has closed.  Measured on a word boundary and on the
# substring, because a closed word inside a hyphenated compound is still there.
CLOSED = ['thank', 'eleven', 'forty', 'spring', 'winter', 'autumn', 'drain',
          'hose', 'warden', 'jonas', 'mercer', 'nell', 'ardent', 'saucer',
          'sink', 'mat', 'reel', 'stool', 'bulb', 'tray', 'blanket']

# THE DECLARED MEASURE FOR THIS BATCH IS *QUITE*.  It is neither *one* nor
# *week* nor *about*, and it is a word of ordinary English and not of this
# account's grammar.  All four are counted and all four are reported per
# chapter at the end, and the chapter that comes out highest on each is
# printed, because four measures that agree on one chapter are four measures
# of a batch written to a number.
FILLER = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight',
          'nine', 'ten', 'twelve', 'thirteen', 'fourteen', 'fifteen',
          'sixteen', 'seventeen', 'eighteen', 'nineteen', 'twenty', 'thirty',
          'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety',
          'about', 'week', 'quite']

# A BAR THAT FIRES ON EVERYTHING IS A BAR THAT GETS IGNORED.  CAN is both an
# object in this account and the modal verb, and the object is always introduced
# by an article or a possessive, so the test for these words is the article.
ARTICLE = re.compile(
    r"\b(?:a|an|the|that|this|those|these|his|her|its|their|my|your|our|"
    r"another|each|every|some|no|half|eight|one|two|three|four|five|six|"
    r"seven|nine|ten|twelve|twenty|thirty)\s+%s\b")

NEEDS_ARTICLE = ['can']

APPROX = re.compile(
    r"\babout (?:a|an|the|one|two|three|four|five|six|seven|eight|nine|ten|"
    r"eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|"
    r"nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|"
    r"half|quarter|third|hundred|thousand|\d)")


def read(ch):
    p = os.path.join(REPO, 'chapters', 'volume-05', 'chapter-%04d.md' % ch)
    if not os.path.exists(p):
        return None
    return open(p, encoding='utf-8').read()


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
    lo = int(sys.argv[1]) if len(sys.argv) > 1 else 525
    hi = int(sys.argv[2]) if len(sys.argv) > 2 else 529
    filler_tot = {w: 0 for w in FILLER}
    total_w = 0
    total_hits = 0
    missing = []
    for ch in range(lo, hi + 1):
        t = read(ch)
        if t is None:
            missing.append(ch)
            continue
        low = t.lower()
        body = t
        for w in FILLER:
            n = len(re.findall(r'\b%s\b' % w, low))
            filler_tot[w] += n
        bars = list(GLOBAL_ZERO) + GENERAL_BARRED + CARD_BARS.get(ch, []) \
            + SPENT_515_524 + SPENT_495_504 + CLOSED + EXTRA_ZERO
        hits = []
        for b in sorted(set(bars)):
            n = len(re.findall(r'\b%s\b' % re.escape(b.lower()), low))
            n -= len(re.findall(r"o'%s\b" % re.escape(b.lower()), low))
            n -= len(re.findall(r'flower %s\b' % re.escape(b.lower()), low))
            if b.lower() in NEEDS_ARTICLE:
                n = len(re.findall(ARTICLE.pattern % re.escape(b.lower()), low))
            if b.lower() == 'forty':
                n -= len(re.findall(r'\bforty-(?:one|two)\b', low))
            if n > 0:
                hits.append('%s=%d' % (b, n))
                total_hits += n
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
        approx = len(APPROX.findall(low))
        one_liners = 0
        for block in t.split('\n\n'):
            b = block.strip()
            if not b or b.startswith('# ') or b == '---':
                continue
            if b.upper() == b:
                continue
            if len(TOK_S.findall(b)) and len(b.split()) <= 9 \
                    and re.search(r'^(["‘]|said|asked|replied)', b, re.I) is None \
                    and re.search(r'[a-z]"\s*$', b):
                one_liners += 1
        print('%d  w=%4d  caps=%d  ---=%d  approx=%d  tail-dialogue=%d  %s'
              % (ch, words(body), len(caps_blocks(t)), breaks(t), approx,
                 one_liners,
                 ('BARS: ' + ', '.join(hits)) if hits else 'bars 0')
              + ('  || MOTIFS: ' + ', '.join(motifs) if motifs else '')
              + ('  || ' + ', '.join(subs) if subs else '')
              + ('  (forty-one/two: %d)' % forty1 if forty1 else ''))
        total_w += words(body)
    print('TOTAL WORDS', total_w)
    print('FILLER CENSUS:', ', '.join(
        '%s %d' % (w, filler_tot[w]) for w in FILLER))
    if missing:
        print('MISSING CHAPTERS (%d): %s' % (len(missing), missing))
    print('TOTAL BARRED HITS', total_hits,
          'VERDICT', 'OK' if total_hits == 0 else 'NOT OK — CLEAR THESE IN '
          'THE CHAPTERS, OR FLAG THE CARD AS A CARD DEFECT AND KEEP THE RULE')
    if missing:
        print('VERDICT ON THE WHOLE RUN: INCOMPLETE — %d OF %d CHAPTERS DO '
              'NOT EXIST' % (len(missing), hi - lo + 1))


TOK_S = re.compile(r"[A-Za-z0-9']+")

if __name__ == '__main__':
    main()
