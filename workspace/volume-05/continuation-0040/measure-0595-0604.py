#!/usr/bin/env python3
"""Verbatim-span measuring pass for Continuation 0038, chapters 565-574.

Threshold NINE tokens. Tokenised comparison, paragraph sentinels, three excluded
classes recorded as a count and not chased.

COPIED FROM workspace/volume-05/continuation-0037/measure-0555-0564.py WITH THE
BATCH, THE FOUR NAMED RUN THREE WINDOWS, CONTROL 2 AND THE PLANT CHAPTER
CHANGED, AND WITH NOTHING ELSE TOUCHED, so that a figure printed here and a
figure printed in the second half of Continuation 0034 are two measurements of
the same method by the same tokeniser at the same threshold and the two are
comparable.  THE FOUR NAMED WINDOWS FOR THIS RUN ARE 545-549, 545-554,
555-564 AND 385-394, AND THE CONTROL PAIR IS 565-574 AGAINST 555-564, WHICH
IS THE PAIR THAT PROVES THE COPY WAS MADE CORRECTLY RATHER THAN BY SEARCH AND
REPLACE.

THE PLANT MUST COME FROM A CHAPTER INSIDE THE SET BEING MEASURED.  0029's driver
took its plant from outside the set and got nil for the wrong reason, 0032's
took it from 0505 while measuring 515-524, and 0033's took it from 0525 while
measuring 525-529.  THIS ONE TAKES ITS PLANT FROM 0585, WHICH IS THE FIRST
CHAPTER OF THE SET BEING MEASURED.  THIS DRIVER PRINTS WHICH CHAPTER IT TOOK IT FROM AND THAT
PRINT STAYS.
"""


import os, re, sys, glob

N = 9
SENT = '\x00PARA\x00'
TOK = re.compile(r"[a-z0-9']+")

FIG_HEAD = {'man','woman','boy','girl','lad','child','children','person','people',
            'figure','doctor','nurse','student','teacher','driver','worker','staff',
            'porter','officer','clerk','keeper','widow','couple','pair','father',
            'mother','brother','sister','son','daughter','baby','youth','ladder'}
DETS = {'the','a','an','that','this','some','any','every','each','one','two'}
PREPS = {'of','in','on','at','from','with','behind','under','over','about','by',
         'for','to','into','onto','across','beside','near','against','between',
         'along','through','off','out','up','down','who','which','whose','where'}
VERBISH = {'is','was','were','are','am','be','been','being','has','have','had',
           'do','does','did','done','go','goes','went','gone','come','comes','came',
           'say','says','said','tell','tells','told','make','makes','made','put',
           'puts','get','gets','got','take','takes','took','give','gives','gave',
           'stand','stands','stood','sit','sits','sat','look','looks','looked',
           'work','works','worked','hold','holds','held','walk','walks','walked',
           'keep','keeps','kept','carry','carries','carried','carry','wear','wears',
           'wore','live','lives','lived','know','knows','knew','think','thinks',
           'thought','want','wants','wanted','ask','asks','asked','turn','turns',
           'turned','leave','leaves','left','put','set','sets','find','finds',
           'found','see','sees','saw','hear','hears','heard','feel','feels','felt',
           'watch','watches','watched','notice','notices','noticed','remember',
           'remembers','remembered','use','uses','used','need','needs','needed'}

PLACE_TOKENS = {'parade','street','road','lane','yard','shop','counter','gate',
                'stairs','stair','room','building','corner','pavement','flags'}


def strip_md(path):
    raw = open(path, encoding='utf-8').read()
    out = []
    for block in raw.split('\n\n'):
        b = block.strip()
        if not b:
            continue
        if b.startswith('# '):
            continue
        if b == '---' or set(b) <= set('-'):
            continue
        if b.upper() == b and re.search(r'[A-Z]', b):
            continue
        out.append(b)
    return out


def dateline(block):
    """Structural dateline: paragraph BEGINNING with a day of the week, or with
    a number and a day / a month name immediately after it."""
    t = block.lstrip()
    if re.match(r'^(the\s+)?(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b', t, re.I):
        return True
    if re.match(r'^\d{1,2}\s+(january|february|march|april|may|june|july|august|'
                r'september|october|november|december|mon|tue|wed|thu|fri|sat|sun)\b',
                t, re.I):
        return True
    if re.match(r'^(january|february|march|april|may|june|july|august|september|'
                r'october|november|december)\s+\d{1,2}\b', t, re.I):
        return True
    return False


def is_caps(block):
    b = block.strip()
    if b.startswith('# '):
        return False
    return b.upper() == b and bool(re.search(r'[A-Z]', b))


def blocks_with_kinds(path, caps_too=False):
    raw = open(path, encoding='utf-8').read()
    res = []
    for block in raw.split('\n\n'):
        b = block.strip()
        if not b:
            continue
        if b.startswith('# '):
            continue
        if b == '---':
            continue
        if is_caps(b) and not caps_too:
            continue
        res.append((b, dateline(b)))
    return res


def tokens_of(blocks):
    """Return flat token list with a sentinel at every paragraph boundary."""
    toks = []
    for i, (b, isdl) in enumerate(blocks):
        if i:
            toks.append(SENT)
        ts = TOK.findall(b.lower())
        ts = [t for t in ts if not re.fullmatch(r"['’]+", t)]
        toks.extend(ts)
    return toks


def byname_spans(toks):
    """Indices of tokens inside a figure's own by-name noun phrase:
    determiner, modifiers, head noun, then a chain of preposition phrases.
    Refused the moment a verb appears inside it."""
    inside = [False] * len(toks)
    i = 0
    n = len(toks)
    while i < n:
        if toks[i] in DETS:
            j = i + 1
            mods = []
            while j < n and toks[j] not in FIG_HEAD and toks[j] not in PREPS \
                    and toks[j] not in VERBISH and toks[j] != SENT and toks[j] not in DETS:
                mods.append(j); j += 1
            if j < n and toks[j] in FIG_HEAD:
                k = j + 1
                # chain of preposition phrases
                while k < n:
                    if toks[k] in VERBISH or toks[k] == SENT:
                        break
                    if toks[k] in PREPS:
                        m = k + 1
                        while m < n and toks[m] not in VERBISH and toks[m] != SENT \
                                and toks[m] not in DETS and toks[m] not in FIG_HEAD \
                                and toks[m] not in PREPS:
                            m += 1
                        for z in range(k, m):
                            inside[z] = True
                        k = m
                        continue
                    if toks[k] in DETS:
                        break
                    # bare modifier tail
                    inside[k] = True
                    k += 1
                for z in range(i, j + 1):
                    inside[z] = True
                i = k
                continue
        i += 1
    return inside


def place_spans(toks):
    """A borough's own recurring place noun: a determiner-led noun phrase whose
    head is a place noun, with no verb inside."""
    inside = [False] * len(toks)
    for i, t in enumerate(toks):
        if t in DETS:
            j = i + 1
            while j < len(toks) and toks[j] not in PLACE_TOKENS and toks[j] not in PREPS \
                    and toks[j] not in VERBISH and toks[j] != SENT:
                j += 1
            if j < len(toks) and toks[j] in PLACE_TOKENS:
                k = j + 1
                while k < len(toks) and toks[k] not in VERBISH and toks[k] != SENT \
                        and toks[k] not in DETS:
                    for z in range(i, k + 1):
                        inside[z] = True
                    k += 1
    return inside


def load_set(paths, caps_too=False):
    """set index: ngram -> list of (file, start_index_in_that_file's_token_stream)

    An entry of `paths` is either a path or a list of (name, [(block, is_dl)])
    tuples, which is how RUN SEVEN puts a dateline in the set."""
    index = {}
    per_file = {}
    for k, p in enumerate(paths):
        if isinstance(p, list):
            blocks = [b for _name, bs in p for b in bs]
        else:
            blocks = blocks_with_kinds(p, caps_too=caps_too)
        toks = tokens_of(blocks)
        per_file[k] = toks
        for i in range(len(toks) - N + 1):
            if SENT in toks[i:i + N]:
                continue
            g = tuple(toks[i:i + N])
            index.setdefault(g, []).append((k, i))
    return index, per_file


def scan(target_paths, set_paths, caps_too=False, exclusions=True, label=''):
    index, per_file = load_set(set_paths, caps_too=caps_too)
    raw = excl_byname = excl_place = 0
    hits = []
    for tp in target_paths:
        blocks = blocks_with_kinds(tp, caps_too=caps_too)
        toks = tokens_of(blocks)
        dl = [False] * len(toks)
        pos = 0
        for b, isdl in blocks:
            ts = TOK.findall(b.lower())
            ts = [t for t in ts if not re.fullmatch(r"['’]+", t)]
            for t in ts:
                dl[pos] = isdl
                pos += 1
            pos += 1  # sentinel
        bn = byname_spans(toks) if exclusions else [False] * len(toks)
        pl = place_spans(toks) if exclusions else [False] * len(toks)
        i = 0
        while i <= len(toks) - N:
            if toks[i] == SENT:
                i += 1
                continue
            g = tuple(toks[i:i + N])
            if SENT in g:
                i += 1
                continue
            if g in index:
                # extend from EVERY real position
                best = None
                for (fp, si) in index[g]:
                    stoks = per_file[fp]
                    L = 0
                    while (i - L - 1 >= 0 and si - L - 1 >= 0
                           and toks[i - L - 1] != SENT
                           and stoks[si - L - 1] != SENT
                           and toks[i - L - 1] == stoks[si - L - 1]):
                        L += 1
                    R = N
                    while (i + R < len(toks) and si + R < len(stoks)
                           and toks[i + R] != SENT
                           and stoks[si + R] != SENT
                           and toks[i + R] == stoks[si + R]):
                        R += 1
                    span = (i - L, i + R)
                    if best is None or (span[1] - span[0]) > (best[1] - best[0]):
                        best = span
                raw += 1
                a, b = best
                seg = toks[a:b]
                if exclusions and all(dl[x] for x in range(a, b)):
                    excl_byname += 0
                    i = b
                    continue
                if exclusions and all(x or toks[x] == SENT for x in bn[a:b]) \
                        and all(toks[x] != SENT for x in range(a, b)):
                    excl_byname += 1
                    i = b
                    continue
                if exclusions and all(toks[x] in PLACE_TOKENS for x in range(a, b) if toks[x] != SENT):
                    excl_place += 1
                    i = b
                    continue
                hits.append((os.path.basename(tp),
                             os.path.basename(set_paths[index[g][0][0]]),
                             ' '.join(x for x in seg if x != SENT), b - a))
                i = b
                continue
            i += 1
    longest = max([h[3] for h in hits], default=0)
    if label:
        print(f'{label}: {raw} RAW, {len(hits)} REUSES, LONGEST {longest}'
              f'  [byname {excl_byname}, place {excl_place}]')
        for h in hits:
            if len(h) == 4:
                print(f'    HIT {h[0]} vs {h[1]} [{h[3]}] {" ".join(h[2].split())}')
            else:
                print(f'    HIT {h[0]} [{h[2]}] {" ".join(h[1].split())}')
    return raw, hits, longest


def dateline_texts(paths):
    out = []
    for p in paths:
        raw = open(p, encoding='utf-8').read()
        for block in raw.split('\n\n'):
            b = block.strip()
            if b and dateline(b):
                out.append((p, b))
    return out


def as_targets(texts):
    """[(path, block)] -> [(name, [(block, is_dateline)])] for scan_blocks."""
    return [(os.path.basename(p), [(b, False)]) for p, b in texts]


def caps_texts(paths):
    """The standalone all-caps paragraphs, as a run of their own."""
    out = []
    for p in paths:
        raw = open(p, encoding='utf-8').read()
        for block in raw.split('\n\n'):
            b = block.strip()
            if b and is_caps(b):
                out.append((p, b))
    return out


# ---------------------------------------------------------------------------
# Driver. Everything the continuity block cites is produced here. Nothing
# below is carried forward from a summary; every figure is taken from the
# files on the day it is printed.
# ---------------------------------------------------------------------------

REPO = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))


def batch_chapters(lo, hi):
    """The chapter files of a run, and a loud notice when they are not there.

    A detector that raises FileNotFoundError on a batch nobody has written
    yet gets skipped, and a detector that skips is not a detector.  The
    missing ones are named at the top so that a figure read off a partial
    run cannot be mistaken for a figure read off the whole of it.
    """
    out, gone = [], []
    for i in range(lo, hi + 1):
        p = os.path.join(REPO, 'chapters', 'volume-05', 'chapter-%04d.md' % i)
        if os.path.exists(p):
            out.append(p)
        else:
            gone.append(i)
    if gone:
        print('!! %d OF %d CHAPTERS IN %d-%d DO NOT EXIST: %s'
              '  ANY FIGURE BELOW IS A FIGURE ON THE PART OF THE RUN THAT'
              ' EXISTS AND NOT ON THE WHOLE OF IT.'
              % (len(gone), hi - lo + 1, lo, hi, gone))
    return out


def non_chapter_markdown():
    """Every markdown file outside chapters/ and outside .git/."""
    out = []
    for root, dirs, files in os.walk(REPO):
        dirs[:] = [d for d in dirs if d not in ('.git', 'chapters')]
        for f in sorted(files):
            if f.endswith('.md'):
                out.append(os.path.join(root, f))
    return sorted(out)


def scan_blocks(targets, set_paths, caps_too=False, exclusions=True, label=''):
    """Same pass as scan(), but the target is a list of (name, blocks) so that
    a run can be taken over caps blocks alone or over datelines alone."""
    index, per_file = load_set(set_paths, caps_too=caps_too)
    raw = excl_byname = excl_place = 0
    hits = []
    for name, blocks in targets:
        toks = tokens_of(blocks)
        dl = [False] * len(toks)
        pos = 0
        for b, isdl in blocks:
            ts = TOK.findall(b.lower())
            ts = [t for t in ts if not re.fullmatch(r"['’]+", t)]
            for _t in ts:
                dl[pos] = isdl
                pos += 1
            pos += 1
        bn = byname_spans(toks) if exclusions else [False] * len(toks)
        i = 0
        while i <= len(toks) - N:
            if toks[i] == SENT or SENT in toks[i:i + N]:
                i += 1
                continue
            g = tuple(toks[i:i + N])
            if g in index:
                best = None
                for (fp, si) in index[g]:
                    stoks = per_file[fp]
                    L = 0
                    while (i - L - 1 >= 0 and si - L - 1 >= 0
                           and toks[i - L - 1] != SENT
                           and stoks[si - L - 1] != SENT
                           and toks[i - L - 1] == stoks[si - L - 1]):
                        L += 1
                    R = N
                    while (i + R < len(toks) and si + R < len(stoks)
                           and toks[i + R] != SENT
                           and stoks[si + R] != SENT
                           and toks[i + R] == stoks[si + R]):
                        R += 1
                    span = (i - L, i + R)
                    if best is None or (span[1] - span[0]) > (best[1] - best[0]):
                        best = span
                raw += 1
                a, b = best
                if exclusions and all(dl[x] for x in range(a, b)):
                    i = b
                    continue
                if (exclusions and all(x or toks[x] == SENT for x in bn[a:b])
                        and all(toks[x] != SENT for x in range(a, b))):
                    excl_byname += 1
                    i = b
                    continue
                seg = toks[a:b]
                if exclusions and all(toks[x] in PLACE_TOKENS
                                      for x in range(a, b) if toks[x] != SENT):
                    excl_place += 1
                    i = b
                    continue
                hits.append((name, ' '.join(x for x in seg if x != SENT), b - a))
                i = b
                continue
            i += 1
    longest = max([h[2] for h in hits], default=0)
    if label:
        print(f'{label}: {raw} RAW, {len(hits)} REUSES, LONGEST {longest}'
              f'  [byname {excl_byname}, place {excl_place}]')
        for h in hits:
            if len(h) == 4:
                print(f'    HIT {h[0]} vs {h[1]} [{h[3]}] {" ".join(h[2].split())}')
            else:
                print(f'    HIT {h[0]} [{h[2]}] {" ".join(h[1].split())}')
    return raw, hits, longest


def against_each_other(paths, label, caps_too=False, exclusions=True):
    """RUN TWO. Every file is compared with the other N-1 and NEVER with itself,
    which is the fault §12A item seven exists to stop."""
    texts = {p: [(os.path.basename(p), blocks_with_kinds(p, caps_too=caps_too))]
             for p in paths}
    return _pairwise(list(paths), texts, label, caps_too, exclusions)


def datelines_against_each_other(paths, label):
    """RUN SEVEN, and it is the SEVENTH and not a whole-chapter pass.

    The target is the DATELINE of each file and the set is the datelines of the
    other nine. The exclusions are off, because the whole point is that the
    dateline carries its own FRAME, which the dateline excluded class does not
    cover. Each file is compared with the other nine and never with itself, and
    the target block and the set block are never taken from the same file."""
    dts = {p: [(os.path.basename(p), [(b, False)])
               for _q, b in dateline_texts([p])] for p in paths}
    return _pairwise(list(paths), dts, label, caps_too=False, exclusions=False)


def _pairwise(paths, texts, label, caps_too=False, exclusions=True, key=None):
    """Compare each file in `paths` against the text of the OTHER files only.

    `texts` maps a path to that path's list of (name, [(block, is_dateline)])
    tuples. Every file is walked as a target once, with the other N-1 in the
    set, and no file is ever its own set, which is the fault item seven exists
    to stop and the fault Run Seven tripped over on its first telling."""
    tot_raw = tot_hits = 0
    longest = 0
    for p in paths:
        others = [t for q, t in texts.items() if q != p]
        raw, hits, lg = scan_blocks(texts[p], others, caps_too=caps_too,
                                    exclusions=exclusions)
        tot_raw += raw
        tot_hits += len(hits)
        longest = max(longest, lg)
        for h in hits:
            print(f'    hit {h[0]} [{h[2]}] {" ".join(h[1].split())[:100]}')
    print(f'{label}: {tot_raw} RAW, {tot_hits} REUSES, LONGEST {longest}')
    return tot_raw, tot_hits, longest


def _blocks_of(p, caps_too=False):
    return blocks_with_kinds(p, caps_too=caps_too)


if __name__ == '__main__':
    print('method: N=%d, tokenised, paragraph sentinel, three excluded classes '
          'recorded as a count' % N)
    ch = batch_chapters(585, 594)
    nonmd = non_chapter_markdown()
    state_six = [os.path.join(REPO, 'state', f) for f in
                 ('current.md', 'continuity.md', 'open-threads.md',
                  'character-state.md', 'chapter-summaries.md',
                  'batch-summaries.md')]

    print('\n-- RUN ONE: the caps blocks of the ten against every non-chapter '
          'markdown file (%d files)' % len(nonmd))
    scan_blocks(as_targets(caps_texts(ch)), nonmd, caps_too=True,
                label='RUN ONE')

    print('\n-- RUN TWO: the ten against each other, none against itself')
    against_each_other(ch, 'RUN TWO')

    print('\n-- RUN THREE: the ten against four named windows')
    # 585-594 IS ITSELF AND IS NOT A WINDOW.  THE FOUR NAMED WINDOWS FOR THIS
    # RUN ARE 575-584, 565-574, 555-564 AND 385-394.
    for lo, hi in ((575, 584), (565, 574), (555, 564), (385, 394)):
        scan(ch, batch_chapters(lo, hi), label='RUN THREE vs %d-%d' % (lo, hi))

    print('\n-- RUN FOUR: the ten against the six state files this batch wrote')
    scan(ch, state_six, label='RUN FOUR')

    print('\n-- RUN FIVE: the whole text of the ten against every non-chapter '
          'markdown file (%d files)' % len(nonmd))
    scan(ch, nonmd, label='RUN FIVE')

    print('\n-- RUN SEVEN: the ten DATELINES against each other as a run of '
          'their own, exclusions OFF, none against itself')
    # CONFIRM WHAT THIS FUNCTION READS BEFORE BELIEVING IT. §12C item 3 of the
    # 0027 block: a run-seven function that scans the chapter instead of the
    # dateline reports reuses between two bodies under a heading that says it
    # is measuring datelines. Print the datelines themselves.
    for _p in ch:
        _d = dateline_texts([_p])
        assert len(_d) == 1, f'{_p} has {len(_d)} dateline paragraphs, not 1'
        print('    dateline read: %s' % ' '.join(_d[0][1].split())[:100])
    datelines_against_each_other(ch, 'RUN SEVEN')

    print('\n-- CONTROLS')
    scan([os.path.join(REPO, 'state', 'continuity.md')],
         [os.path.join(REPO, 'state', 'open-threads.md')],
         label='CONTROL 1: continuity.md against open-threads.md')
    scan(batch_chapters(585, 594), batch_chapters(575, 584),
         label='CONTROL 2: the ten against the ten immediately above')
    import tempfile
    # THE PLANT MUST COME FROM A CHAPTER IN THIS BATCH, OR THE CONTROL
    # MEASURES A CHAPTER AGAINST A SET IT IS NOT IN AND COMES BACK NIL FOR
    # THE WRONG REASON. 0029's driver took it from 0482 and got zero,
    # 0032's took it from 0505 while measuring 515-524, and 0033's took it
    # from 0525 while measuring 525-529, which is the same fault under a
    # later name.
    plant_src = ch[0] if ch else None
    if plant_src is None or not os.path.exists(plant_src):
        print('CONTROL 3 SKIPPED: the batch is unwritten, so there is no '
              'prose paragraph inside the set being measured to plant. THIS '
              'CONTROL MUST BE TAKEN AFTER 0525 EXISTS AND NOT BEFORE.')
    else:
        src = blocks_with_kinds(plant_src)
        # A DATELINE IS NOT A PLANT.  The method excludes dateline paragraphs
        # from the index (that is what RUN SEVEN exists to measure), so a
        # plant taken from one is measured against a set it is not in and
        # comes back nil for the wrong reason.  Take prose.
        para = [b for b, d in src if not d and len(TOK.findall(b.lower())) > 40][0]
        ptoks = TOK.findall(para.lower())[:14]
        with tempfile.NamedTemporaryFile('w', suffix='.md',
                                         delete=False) as fh:
            fh.write(' '.join(ptoks) + '\n')
            plant = fh.name
        print(f'    plant taken from {os.path.basename(plant_src)}: '
              f'{" ".join(ptoks)}')
        scan([plant], ch,
             label='CONTROL 3: a fourteen-token plant against the ten')
        os.unlink(plant)
