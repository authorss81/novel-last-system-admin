#!/usr/bin/env python3
"""Verbatim-span measuring pass for Continuation 0026, chapters 445-454.

Threshold NINE tokens. Tokenised comparison, paragraph sentinels, three
excluded classes recorded as a count and not chased.
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
    """set index: ngram -> list of (file, start_index_in_that_file's_token_stream)"""
    index = {}
    per_file = {}
    for p in paths:
        blocks = blocks_with_kinds(p, caps_too=caps_too)
        toks = tokens_of(blocks)
        per_file[p] = toks
        for i in range(len(toks) - N + 1):
            if SENT in toks[i:i + N]:
                continue
            g = tuple(toks[i:i + N])
            index.setdefault(g, []).append((p, i))
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
                hits.append((os.path.basename(tp), os.path.basename(index[g][0][0]),
                             ' '.join(x for x in seg if x != SENT), b - a))
                i = b
                continue
            i += 1
    longest = max([h[3] for h in hits], default=0)
    if label:
        print(f'{label}: {raw} RAW, {len(hits)} REUSES, LONGEST {longest}'
              f'  [byname {excl_byname}, place {excl_place}]')
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


if __name__ == '__main__':
    print('method: N=%d, tokenised, paragraph sentinel, three excluded classes recorded' % N)
