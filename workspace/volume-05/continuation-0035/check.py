#!/usr/bin/env python3
"""Banned-word and filler census for Continuation 0035, chapters 535-544.

COPIED FROM workspace/volume-05/continuation-0035/check-0530-0534.py WITH THE
DOCSTRING, THE DEFAULTS, THE SPENT LISTS AND THE DECLARED MEASURE CHANGED.  The
method, the article test, the approximation test, the line buffer, the motif
list, the closed list and the total-and-verdict footer are byte-identical, so
that a figure printed here and a figure printed there are two measurements of
the same thing.

WHAT A WRITER OF 0535 MUST DO TO THIS FILE BEFORE IT BELIEVES ANYTHING IT PRINTS
  * TYPE THE FIVE CARD BARS OF CHAPTERS 535 TO 539 IN WHOLE, AND GIVE 540 TO 544
    AN EMPTY LIST EACH, WHICH IS WHAT A CARD THAT BARS NOTHING GETS.  A CARD MAY
    NOT BE NARROWED TOWARD THE PROSE SO AS TO MAKE A COUNT PASS.
  * ADD TO SPENT_525_529 THE OBJECTS CHAPTERS 530 TO 534 SPENT, WHICH ARE AT
    1 TO 10 OF THE 0034 OPEN-THREADS BLOCK AND ARE NOT ALL IN THE LIST BELOW.
    SPENT_530_534 IS TYPED IN ALREADY AND IS IN THE UNION.
  * **AND THEN CHECK THE UNION.**  The copy built for the second half of 0034
    listed SPENT_525_529 and then did not put it into the union at the point
    where the bars are assembled, and it did not fire once for four chapters,
    and three genuine hits were sitting in the prose the whole time.  FIND THE
    LINE THAT BEGINS `bars = list(GLOBAL_ZERO)` AND CONFIRM THAT EVERY SPENT
    LIST IS IN IT BEFORE YOU TRUST A NIL.
  * CHANGE THE DECLARED MEASURE.  ALMOST CAME OUT AT NIL ACROSS 530-534 AND THAT
    IS THE FINDING, AND ALL SIX MEASURES ARE COUNTED AND REPORTED REGARDLESS.

Run:  python3 workspace/volume-05/continuation-0035/check.py 535 544
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

# 0033 kept REQUIR-.*?
# They are in the union here.  DRAINAGE, DRAINS and DRAINER are legitimate
# English and only the bare word DRAIN is the prohibited member, which is why
# the test below is \bDRAIN\b and not DRAIN-.
EXTRA_ZERO = ['requir', 'permit', 'free']

# Chapter-specific bars printed on the cards of 0034, transcribed whole.
# A WRITER MAY NOT NARROW A CARD TOWARD THE PROSE SO AS TO MAKE A COUNT PASS.
_COMMON = ['money', 'letter', 'form', 'claim', 'rent', 'repair', 'gate',
           'light', 'bin', 'sign', 'road', 'key', 'van']

_COMMON = ['money', 'letter', 'form', 'claim', 'rent', 'repair', 'gate',
           'light', 'bin', 'sign', 'road', 'key', 'van']

CARD_BARS = {
    # TYPE THE FIVE CARD BARS OF 535-539 IN WHOLE, AND GIVE 540-544 AN EMPTY
    # LIST EACH, WHICH IS WHAT A CARD THAT BARS NOTHING GETS.  A CARD MAY NOT BE
    # NARROWED TOWARD THE PROSE SO AS TO MAKE A COUNT PASS.
}

# The objects 525-529 spent AS OBJECTS, taken from 1 to 10 of the 0034
# OPEN-THREADS BLOCK, which is the list of record.  A word that is furniture of
# the prose rather than the object of a chapter is NOT in here, because a bar
# that fires on every chapter is a bar that gets ignored.  525-529 spent: THE
# SCARF, THE CORNER, THE TREE, THE YARD, THE LORRY, THE CAR PARK, THE
# ARCHWAY, THE LAY-BY, THE ROOM, THE COAT, THE INTERVAL, THE PORCH, THE BRICK,
# THE BOY ON THE BICYCLE, THE HOLDALL, THE RADIATOR, THE BUS, THE POCKET, THE
# FRONT PATH AND THE WORD AT THE ENTRANCE.
SPENT_525_529 = ['scarf', 'corner', 'tree', 'yard', 'lorry', 'car park',
                 'archway', 'lay-by', 'room', 'coat', 'interval', 'porch',
                 'brick', 'bicycle', 'holdall', 'radiator', 'bus', 'pocket',
                 'front path', 'green coat', 'pavement', 'collar']

# THE OBJECTS 530-534 SPENT, AND A WRITER OF 0535 MUST ADD TO THIS LIST AND NOT
# REPLACE IT.  FROM 1 TO 10 OF THE 0034 OPEN-THREADS BLOCK: THE MIRROR, THE CHALK,
# THE BED, THE BASIN, THE TILES, THE LEDGE, THE SILL, THE CISTERN, THE AIRING
# CUPBOARD, THE LONG SEAT, THE GLASS, THE GREEN, THE HUT, THE MALLLETS, THE HOOPS,
# THE PEG, THE JACK, THE DITCH, THE JUG, THE SHOES, THE SPECTACLES, THE FOLD, THE
# THREE STEPS, THE ICE, THE RAMP, THE DIP, THE SHAFT, THE SHOVEL, THE GRIT, THE
# FRAME, THE SHOP END, THE PIECE OF GROUND, THE WASHING, THE RAIN.
SPENT_530_534 = ['mirror', 'chalk', 'basin', 'tiles', 'ledge', 'sill',
                 'cistern', 'airing cupboard', 'spectacles', 'green', 'hut',
                 'mallets', 'hoop', 'peg', 'ditch', 'jug', 'shoes', 'steps',
                 'ice', 'ramp', 'dip', 'shovel', 'grit', 'frame', 'washing',
                 'rain', 'peg', 'jack']

# The objects spent by 515-524 AS OBJECTS, at item 6 of the 0034 prompt.  A
# list written in prose is a list nobody greps, so the single words are typed in.
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

# THE DECLARED MEASURE FOR THIS BATCH IS CHOSEN BY THE WRITER AND IS NOT ONE OF  It is neither *one*
# nor *week* nor *about* nor *quite*, and it is a word of ordinary English and
# nor *about* nor *quite*, and it is a word of ordinary English and not of this
# account's grammar.  All six are counted and all six are reported per chapter at
# the end, and the chapter that comes out highest on each is printed, because six
# measures that agree on one chapter are six measures of a batch written to a number.
FILLER = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight',
          'nine', 'ten', 'twelve', 'thirteen', 'fourteen', 'fifteen',
          'sixteen', 'seventeen', 'eighteen', 'nineteen', 'twenty', 'thirty',
          'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety',
          'about', 'week', 'quite', 'almost']

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
    lo = int(sys.argv[1]) if len(sys.argv) > 1 else 535
    hi = int(sys.argv[2]) if len(sys.argv) > 2 else 544
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
            + SPENT_530_534 + SPENT_525_529 + SPENT_515_524 \
            + SPENT_495_504 + CLOSED + EXTRA_ZERO
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
