#!/usr/bin/env python3
"""Measure the shared ten-token spans in a block of chapters, WITH THE DATELINE IN.

Usage: measure_runs.py 0785 0794
Body text = everything except the title line and the ALL-CAPS block.
The dateline paragraph IS counted, which is the change the review of 0059 asked for.
"""
import re
import sys
import itertools
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CH = ROOT / "chapters" / "volume-05"

BANNED = """hold holds held holding claim claims counter counters seal seals seam seams
term terms notice notices lens margin system panel permission bearer lattice civicore
goal resistance change beat changes changed changing goals beats household threshold
encounter determine noticed exchange""".split()

WATCHED = "steady plain counted breathed wrote nodded".split()

ORDINARY_BANNED = """not usually anyway like just enough still kind quite small round one week
almost anything and then nearly away count garden shoulder work""".split()


def load(n):
    p = CH / f"chapter-{n}.md"
    raw = p.read_text()
    lines = raw.split("\n")
    body = []
    for ln in lines:
        if ln.startswith("# Chapter "):
            continue
        if ln.startswith("---"):
            continue
        if ln.strip() and ln.strip() == ln.strip().upper() and re.search(r"[A-Z]{3}", ln):
            continue
        body.append(ln)
    text = "\n".join(body)
    return raw, text


def toks(text):
    return re.findall(r"[a-z0-9']+", text.lower())


def main():
    lo, hi = sys.argv[1], sys.argv[2]
    nums = [f"{i:04d}" for i in range(int(lo), int(hi) + 1)]
    docs = {}
    for n in nums:
        _, t = load(n)
        docs[n] = toks(t)

    N = 10
    spans = {}
    for n, tk in docs.items():
        seen = set()
        for i in range(len(tk) - N + 1):
            seen.add(tuple(tk[i:i + N]))
        spans[n] = seen

    intra = {n: [] for n in nums}
    for n in nums:
        tk = docs[n]
        counts = {}
        for i in range(len(tk) - N + 1):
            s = tuple(tk[i:i + N])
            counts[s] = counts.get(s, 0) + 1
        for s, c in counts.items():
            if c > 1:
                intra[n].append((c, " ".join(s)))

    cross = []
    for a, b in itertools.combinations(nums, 2):
        shared = spans[a] & spans[b]
        for s in shared:
            cross.append((a, b, " ".join(s)))

    print("=== INTRA-CHAPTER repeated 10-token spans ===")
    tot_intra = 0
    for n in nums:
        tot_intra += len(intra[n])
        for c, s in intra[n]:
            print(f"  {n} x{c}: {s}")
    print(f"total intra-chapter spans: {tot_intra}")

    print("\n=== CROSS-CHAPTER shared 10-token spans (dateline included) ===")
    tally = {}
    for a, b, s in cross:
        tally[s] = tally.get(s, 0) + 1
    for s, c in sorted(tally.items(), key=lambda x: -x[1]):
        where = [f"{a}/{b}" for a, b, t in cross if t == s]
        print(f"  x{c}: {s}   [{', '.join(where)}]")
    print(f"total shared spans: {len(cross)}; distinct: {len(tally)}")
    over2 = {s: c for s, c in tally.items() if c > 2}
    print(f"spans standing in more than 2 chapters: {len(over2)}")
    for s, c in sorted(over2.items(), key=lambda x: -x[1]):
        print(f"   x{c}: {s}")

    print("\n=== BANNED / WATCHED / ORDINARY / said / numerals ===")
    for n in nums:
        raw, t = load(n)
        low = re.findall(r"[a-z']+", t.lower())
        bad = sorted({w for w in BANNED if w in low})
        wat = sorted({w for w in WATCHED if w in low})
        said = low.count("said")
        wedge = low.count("wedge")
        digs = [d for d in raw if d.isdigit()]
        print(f"  {n}: banned={bad} watched={wat} said={said} wedge={wedge} digits={sorted(set(digs))}")

    print("\n=== per-chapter stats ===")
    tot = 0
    for n in nums:
        raw = (CH / f"chapter-{n}.md").read_text()
        w = len(raw.split())
        sb = raw.count("\n---\n")
        caps = sum(
            1 for p in raw.split("\n\n")
            if p.strip() and p.strip() == p.strip().upper() and re.search(r"[A-Z]{3}", p)
        )
        tot += w
        print(f"  {n}: words={w} scene_breaks={sb} allcaps_paragraphs={caps}")
    print(f"total words: {tot}")

    print("\n=== ordinary filler words (should be sparse) ===")
    for n in nums:
        _, t = load(n)
        low = re.findall(r"[a-z']+", t.lower())
        hits = {w: low.count(w) for w in ORDINARY_BANNED if low.count(w)}
        print(f"  {n}: {hits}")


if __name__ == "__main__":
    main()