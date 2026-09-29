#!/usr/bin/env python3
"""Banned-word and filler census for Continuation 0033, chapters 515-524.

Every list here is printed from the cards and from the closed vocabulary.
Run:  python3 workspace/volume-05/continuation-0033/check.py 515 524

CHANGED FROM THE 0032 COPY, WHICH WAS BYTE-IDENTICAL AND THEREFORE MEASURED
THE PREVIOUS TEN WHILE BEING CALLED THE NEXT TEN.  Five things were wrong and
all five are fixed here: the docstring, the two defaults, CARD_BARS, the spent
list, and the filler measure.  The prompt asks for this at its own line 105 and
the ask had not been carried out.
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
    'handrail', 'level', 'hall', 'counter', 'bisland', 'bollard', 'grate',
    'settee', 'print', 'coping', 'kerb', 'landing', 'machine', 'awning',
    'scoop', 'cat', 'the ninth', 'four years', 'in about four years',
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

# Chapter-specific bars printed on the ten cards of 0033, transcribed whole
# and in order.  A WRITER MAY NOT NARROW A CARD TOWARD THE PROSE SO AS TO
# MAKE A COUNT PASS; THAT IS THE FINDING OF THE REVIEW OF 0031 AND IT IS THE
# REASON THIS LIST IS TYPED OUT RATHER THAN DERIVED.
_COMMON = ['money', 'letter', 'form', 'claim', 'rent', 'repair', 'gate',
           'light', 'bin', 'sign', 'road', 'key', 'van']

CARD_BARS = {
    515: _COMMON + ['kettle', 'chair', 'window', 'bench', 'hill', 'towel'],
    516: _COMMON + ['car', 'bench', 'door'],
    517: _COMMON + ['queue', 'shop', 'bus', 'ticket', 'number', 'handbag',
                    'umbrella'],
    518: _COMMON + ['church', 'grave', 'name'],
    519: _COMMON + ['bell', 'can', 'ceiling', 'fish', 'rope', 'ladder'],
    520: _COMMON + ['chair', 'kettle', 'blanket', 'towel', 'bench', 'stair'],
    521: _COMMON + ['car', 'frame', 'room', 'picture frame', 'wall'],
    522: _COMMON + ['lift', 'stair', 'window', 'name board', 'bench', 'floor'],
    523: _COMMON + ['diary', 'notebook', 'pen', 'chair', 'table', 'room',
                    'bed'],
    524: [],
}

# Objects spent by 505-514 as objects, not only as chapters, at item 6 of the
# 0033 prompt.  0032's checker held the 495-504 list under the name
# SPENT_495_504 and measured it against the wrong ten.
SPENT_505_514 = ['hill', 'bath sheet', 'nail', 'bench', 'flask', 'seat',
                 'tap', 'ledge', 'can', 'umbrella', 'shoe rack', 'ceiling',
                 'broom', 'step', 'steps', 'front room']

# The ten before those are spent as objects too and stay spent.  0032's prompt
# barred A STAIR, A DOORWAY A MAN STANDS IN, A DOORSTEP, A BUS STOP, A PASSAGE,
# A TELEPHONE BOX, A KITCHEN DOOR, A TABLE, A WASHING LINE AND A LENGTH OF
# SHUTTERING, and 0509 AND 0514 WERE BUILT ON STEPS ANYWAY, WHICH IS §12D ITEM
# 8 AND §12G ITEM 9 OF THE 0032 BLOCK.  THE BAR RUNS FORWARD.  IT IS NOT
# RETROACTIVE, AND A REVIEWER READING A NON-ZERO LINE ON CHAPTERS 505-514 IS
# READING A KNOWN AND RECORDED DEFECT IN THOSE CARDS AND NOT A NEW ONE.
SPENT_495_504 = ['stair', 'stairs', 'staircase', 'stairwell', 'doorway',
                 'doorstep', 'bus stop', 'passage', 'telephone box',
                 'kitchen door', 'table', 'washing line', 'shuttering']

# 0032 could not see a flight of STEPS because the list held only STAIR.
# A bar that is only tested at the end is a bar that has already been broken.

# The general barred-object list printed at the foot of the TEN CARDS section
# of PROMPT.md, transcribed whole and in order.  0032 held it THIRTEEN ITEMS
# SHORT, which is how TRAY SURVIVED ELEVEN USES IN 0507 AND BED SURVIVED THREE
# IN 0505.  THE 0033 LIST IS LONGER AGAIN AND ENDS AT A SHOP FRONT.
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
# This list was documentation and was never added to the bars, which is how
# FORTY and the bare stem DRAIN- went unchecked.  It is in the union now.
# \bDRAIN\b does not match DRAINAGE or DRAINS, which are legitimate English;
# only the bare word is the prohibited member of the stem.
CLOSED = ['thank', 'eleven', 'forty', 'spring', 'winter', 'autumn', 'drain',
          'hose', 'warden', 'jonas', 'mercer', 'nell', 'ardent', 'saucer',
          'sink', 'mat', 'reel', 'stool', 'bulb', 'tray', 'blanket']

# The declared filler measure of 0032 was the number words and that was the
# WRONG WORD.  §13 AND §12G ITEM 10 OF THE 0032 BLOCK record *about* at 381
# across the ten, of which 207 are the approximation use, against 328 in
# 495-504.  A NUMBER-WORD CENSUS CANNOT SEE THAT, AND THIS FILE COULD NOT
# SEE IT EITHER UNTIL NOW.  ABOUT IS IN THE CENSUS AND THE APPROXIMATION
# USE IS COUNTED BESIDE IT, DEFINED IN THE FILE SO THAT IT CAN BE REPRODUCED.
# §13's NARROWER HAND COUNT OF 207 IS NOT REPRODUCED HERE AND IS NOT
# REPLACED BY THE FIGURE BELOW; THE TWO ARE DIFFERENT MEASURES.
FILLER = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight',
          'nine', 'ten', 'twelve', 'thirteen', 'fourteen', 'fifteen',
          'sixteen', 'seventeen', 'eighteen', 'nineteen', 'twenty', 'thirty',
          'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety',
          'about']

# A BAR THAT FIRES ON EVERYTHING IS A BAR THAT GETS IGNORED, AND 0032's WAS
# IGNORED WITH 48 HITS ON THE SCREEN AND NO TOTAL ANYWHERE.  CAN IS BOTH THE
# OBJECT IN 0505, 0508, 0509, 0512 AND 0514 AND THE MODAL VERB, AND A BARE \b
# TEST ON IT REPORTED THE MODAL AS THE OBJECT AND MADE THE LINE UNREADABLE.
# THE OBJECT IN THIS ACCOUNT IS ALWAYS INTRODUCED BY AN ARTICLE OR A
# POSSESSIVE, SO THE TEST FOR THESE WORDS IS THE ARTICLE AND NOT THE BARE
# WORD.  0509 ON THE BARE TEST READS can=18; ON THIS ONE IT READS can=11, AND
# THE SEVEN THAT LEAVE ARE "CAN SEE", "CAN TELL" AND FIVE MORE.
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
    lo = int(sys.argv[1]) if len(sys.argv) > 1 else 515
    hi = int(sys.argv[2]) if len(sys.argv) > 2 else 524
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
        # count filler on word boundaries in the whole file
        for w in FILLER:
            n = len(re.findall(r'\b%s\b' % w, low))
            filler_tot[w] += n
        bars = list(GLOBAL_ZERO) + GENERAL_BARRED + CARD_BARS.get(ch, []) \
            + SPENT_505_514 + SPENT_495_504 + CLOSED
        hits = []
        for b in sorted(set(bars)):
            n = len(re.findall(r'\b%s\b' % re.escape(b.lower()), low))
            # "o'clock" is an hour, not the barred object.  Same for
            # "flower bed", which is a border and not the barred furniture.
            n -= len(re.findall(r"o'%s\b" % re.escape(b.lower()), low))
            n -= len(re.findall(r'flower %s\b' % re.escape(b.lower()), low))
            if b.lower() in NEEDS_ARTICLE:
                n = len(re.findall(ARTICLE.pattern % re.escape(b.lower()), low))
            # FORTY-ONE is the address at the low end of Peverell Street and
            # FORTY-TWO is an occupied age.  Neither is the closed word.
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
        print('%d  w=%4d  caps=%d  ---=%d  approx=%d  %s'
              % (ch, words(body), len(caps_blocks(t)), breaks(t), approx,
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
    # 0032 CLOSED WITH 48 HITS ON FIVE CHAPTERS AND NOTHING PRINTED A TOTAL,
    # WHICH IS WHY THE OUTPUT WAS NOT ENFORCED.  A TOTAL IS THE LAST LINE ON
    # PURPOSE.  A CHECKER THAT REPORTS A NON-ZERO AND IS NOT READ IS NOT A
    # CHECKER, AND A LINE THAT SCROLLS PAST IS THE SAME THING AS NO LINE.
    print('TOTAL BARRED HITS', total_hits,
          'VERDICT', 'OK' if total_hits == 0 else 'NOT OK — CLEAR THESE IN '
          'THE CHAPTERS, OR FLAG THE CARD AS §12D ITEM 1 AND KEEP THE RULE')
    if missing:
        print('VERDICT ON THE WHOLE RUN: INCOMPLETE — %d OF %d CHAPTERS DO '
              'NOT EXIST' % (len(missing), hi - lo + 1))


if __name__ == '__main__':
    main()
