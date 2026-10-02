"""Inkstone / WebNovel EPUB metadata.

Every field Inkstone accepts is a **closed list**. Values outside a list are
rejected on their platform, so this module maps free-text manuscript metadata
onto the permitted values and reports anything it had to correct rather than
silently emitting something invalid.

Values, as published by Inkstone:

    dc:title                bookTitle                  max 70 chars
    dc:description          synopsis                   required
    dc:language             language                   required, numeric id
    dc:creator              author
    dc:subject (repeatable) tags                       max 10, restricted catalogue
    inkstone:genre          categoryId                 required, 11 values
    inkstone:gender         leading gender             required, 3 values
    inkstone:length         length                     3 values
    inkstone:warning        warning notice             5 values
    inkstone:abbreviation   abbreviation               max 15 chars

Plus relationship, which Inkstone also records.

Source of values is `state/book-metadata.md`, a plain `Key: value` block:

    Title: The Ninth Furnace
    Genre: Fantasy
    Gender: Male
    Length: Novels
    Warning: General Audiences
    Relationship: F/M
    Language: English
    Abbreviation: T9F
    Tags: system, magic, genius, antihero

Unrecognised tags are dropped with a note, because the catalogue is restricted
and an invented tag will not resolve. Note that there is no "detective",
"procedural" or "water" tag; use mystery or thriller for the first two.
"""

from __future__ import annotations

import os
import re
import sys

MAX_TITLE = 70
MAX_ABBREVIATION = 15
MAX_TAGS = 10

# 70005 and 70011 do not exist: the ids are not contiguous.
GENRES = {
    "urban": 70001,
    "fantasy": 70002,
    "history": 70003,
    "historical": 70003,
    "horror": 70004,
    "scifi": 70006,
    "science fiction": 70006,
    "sci-fi": 70006,
    "sports": 70007,
    "games": 70008,
    "game": 70008,
    "eastern": 70009,
    "xianxia": 70009,
    "cultivation": 70009,
    "wuxia": 70009,
    "realistic": 70010,
    "contemporary": 70010,
    "action": 70012,
    "war": 70013,
    "military": 70013,
}

LENGTHS = {
    "novels": "3",
    "novel": "3",
    "short stories": "2",
    "short story": "2",
    "short": "2",
    "super-short-stories": "1",
    "super short stories": "1",
    "supershort": "1",
}

WARNINGS = {
    "general audiences": "1",
    "general audience": "1",
    "parental guidance suggested": "2",
    "parents strongly cautioned": "3",
    "restricted": "4",
    "no one 17 and under admitted": "5",
}

GENDERS = {
    "male": "1",
    "female": "2",
    "common": "3",
}

RELATIONSHIPS = {
    "m/m": "M/M",
    "f/f": "F/F",
    "f/m": "F/M",
    "m/f": "F/M",
    "gen": "Gen",
    "multi": "Multi",
    "other": "other",
}

LANGUAGES = {
    "english": "1",
    "spanish": "2",
    "bahasa indonesia": "3",
    "indonesian": "3",
    "filipino": "4",
    "melayu": "5",
    "korean": "6",
    "vietnamese": "7",
    "portuguese": "8",
    "french": "9",
    "hindi": "10",
    "russian": "11",
    "swahili": "12",
}

# The published catalogue is 144 tags in five categories. These are the
# documented ones per category; anything outside is treated as unknown.
TAG_CATEGORIES = {
    "character": 100001,
    "plot": 100002,
    "setting": 100003,
    "tone": 100004,
    "fanfic": 100005,
}

CHARACTER_TAGS = {
    "harem", "villain", "genius", "antihero", "werewolf", "beauty", "ceo",
    "vampire", "devil", "killer", "dragon", "highiq",
    "possessive", "strongfemalelead", "alpha", "abandoned", "princess",
}
PLOT_TAGS = {
    "action", "adventure", "romance", "reincarnation", "revenge", "betrayal",
    "kingdombuilding", "levelup", "academy", "rebirth",
    "loveatfirstsight", "suspense", "pregnancy", "thriller",
}
SETTING_TAGS = {
    "system", "magic", "superpowers", "cultivation", "urban", "apocalypse",
    "historical", "royalfamily", "mafia", "future", "myth", "horror",
    "campus", "family", "sweetlove", "teen", "lovetriangle", "richfamily",
}
TONE_TAGS = {
    "comedy", "dark", "mystery", "tragedy", "scary", "serious", "dramatic",
    "angst", "fastpaced", "healing", "sliceoflife", "detailed", "twisted",
}
FANFIC_TAGS = {
    "isekai", "anime", "supernatural", "crossover", "marvel", "dc", "yuri",
    "yaoi", "smut", "omegaverse",
}

CATEGORY_TAGS = {
    "character": CHARACTER_TAGS,
    "plot": PLOT_TAGS,
    "setting": SETTING_TAGS,
    "tone": TONE_TAGS,
    "fanfic": FANFIC_TAGS,
}


def warn(message: str) -> None:
    print(f"book_metadata: {message}", file=sys.stderr)


def parse_metadata_file(root: str) -> dict[str, str]:
    path = os.path.join(root, "state", "book-metadata.md")
    if not os.path.isfile(path):
        return {}
    fields: dict[str, str] = {}
    with open(path, encoding="utf-8", errors="replace") as handle:
        for line in handle:
            m = re.match(r"^\s*[-*]?\s*([A-Za-z][A-Za-z ]{1,24}?)\s*:\s*(.+?)\s*$", line)
            if m:
                fields[m.group(1).strip().lower()] = m.group(2).strip()
    return fields


def _first(fields: dict[str, str], *names: str) -> str:
    for name in names:
        value = fields.get(name, "").strip()
        if value:
            return value
    return ""


def _from_spec(root: str, label: str) -> str:
    path = os.path.join(root, "NOVEL_SPEC.md")
    if not os.path.isfile(path):
        return ""
    with open(path, encoding="utf-8", errors="replace") as handle:
        text = handle.read()
    m = re.search(rf"(?im)^\s*{label}:\s*(.+)$", text)
    return m.group(1).strip() if m else ""


def _lookup(table: dict, value: str, fallback_key: str, field: str) -> str:
    """Resolve free text against a closed list, correcting and reporting."""
    if not value:
        return table[fallback_key]
    cleaned = re.sub(r"\s+", " ", value.strip().lower())
    if cleaned in table:
        return table[cleaned]
    # A spec genre line often reads like "urban fantasy mystery / procedural".
    # Prefer the most specific single term it contains rather than whichever
    # happens to appear first in the table, so "urban fantasy" resolves to
    # Fantasy rather than Urban.
    parts = [p.strip() for p in re.split(r"[/,;|]| and | or ", cleaned) if p.strip()]
    matches: list[tuple[int, int, str, str]] = []
    for order, part in enumerate(parts):
        for term, mapped in table.items():
            if part == term:
                specificity = 0
                break
            if term in part:
                specificity = len(part.split())
                break
        else:
            continue
        matches.append((specificity, order, term, mapped))
    if matches:
        # Most specific wins; ties broken by order of appearance.
        matches.sort(key=lambda item: (-item[0], item[1]))
        _, _, term, mapped = matches[0]
        warn(f"{field} '{value}' is not a permitted value; using '{term}'")
        return mapped
    warn(f"{field} '{value}' is not a permitted value; using '{fallback_key}'")
    return table[fallback_key]


def resolve_genre(value: str) -> str:
    return _lookup(GENRES, value, "fantasy", "genre")


def resolve_length(value: str) -> str:
    return _lookup(LENGTHS, value, "novels", "length")


def resolve_warning(value: str) -> str:
    return _lookup(WARNINGS, value, "general audiences", "warning")


def resolve_gender(value: str) -> str:
    if not value:
        return GENDERS["male"]
    cleaned = value.strip().lower()
    if cleaned in GENDERS:
        return GENDERS[cleaned]
    for term, mapped in GENDERS.items():
        if term in cleaned:
            warn(f"gender '{value}' is not a permitted value; using '{term}'")
            return mapped
    warn(f"gender '{value}' is not a permitted value; using 'male'")
    return GENDERS["male"]


def resolve_relationship(value: str) -> str:
    if not value:
        return RELATIONSHIPS["other"]
    cleaned = value.strip().lower().replace(" ", "")
    if cleaned in RELATIONSHIPS:
        return RELATIONSHIPS[cleaned]
    warn(f"relationship '{value}' is not a permitted value; using 'other'")
    return RELATIONSHIPS["other"]


def resolve_language(value: str) -> str:
    return _lookup(LANGUAGES, value, "english", "language")


def resolve_tags(value: str) -> list[tuple[int, str]]:
    """Return [(category id, tag)] for recognised tags only, max 10."""
    known = {tag: cat for cat, tags in CATEGORY_TAGS.items() for tag in tags}
    out: list[tuple[int, str]] = []
    for raw in re.split(r"[,;]", value or ""):
        tag = re.sub(r"[^a-z0-9]", "", raw.strip().lower())
        if not tag:
            continue
        if tag in known:
            if all(t != tag for _, t in out):
                out.append((TAG_CATEGORIES[known[tag]], tag))
        else:
            warn(f"tag '{raw.strip()}' is not in the catalogue; dropped")
    if len(out) > MAX_TAGS:
        warn(f"{len(out)} tags given; keeping the first {MAX_TAGS}")
        out = out[:MAX_TAGS]
    return out


def clamp_title(value: str) -> str:
    value = value.strip()
    if len(value) <= MAX_TITLE:
        return value
    clipped = value[:MAX_TITLE].rsplit(" ", 1)[0]
    return (clipped or value[:MAX_TITLE]).strip(" ,;:-—")


def clamp_abbreviation(value: str) -> str:
    value = re.sub(r"\s+", " ", value.strip())
    if len(value) <= MAX_ABBREVIATION:
        return value
    return value[:MAX_ABBREVIATION].strip()


def build_metadata(root: str, *, title: str, author: str, description: str) -> dict:
    fields = parse_metadata_file(root)

    genre_raw = _first(fields, "genre", "category", "categoryid", "inkstone genre")
    if not genre_raw:
        genre_raw = _from_spec(root, "Genre")

    length_raw = _first(fields, "length", "inkstone length")
    if not length_raw:
        length_raw = _from_spec(root, "Length target")
        if length_raw:
            count = re.search(r"(\d+)", length_raw)
            length_raw = "short" if count and int(count.group(1)) < 100 else "novels"
        else:
            length_raw = "novels"

    tags_raw = _first(fields, "tags", "subjects", "keywords")
    tags = resolve_tags(tags_raw) if tags_raw else []

    return {
        "title": clamp_title(_first(fields, "title", "booktitle") or title),
        "description": (_first(fields, "description", "synopsis") or description).strip(),
        "language": resolve_language(_first(fields, "language")),
        "creator": (_first(fields, "author", "creator") or author).strip(),
        "tags": tags,
        "genre": resolve_genre(genre_raw),
        "gender": resolve_gender(_first(fields, "gender", "leading gender")),
        "length": resolve_length(length_raw),
        "warning": resolve_warning(_first(fields, "warning", "content warning")),
        "relationship": resolve_relationship(_first(fields, "relationship", "romance")),
        "abbreviation": clamp_abbreviation(_first(fields, "abbreviation", "abbrev")),
    }


def cover_path(root: str) -> str:
    """Return the repo-relative path of a cover image, or an empty string."""
    for relative in ("cover.png", "state/cover.png", "dist/cover.png", "assets/cover.png"):
        if os.path.isfile(os.path.join(root, relative)):
            return relative
    return ""