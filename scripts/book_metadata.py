"""Inkstone / WebNovel EPUB metadata.

Reads `state/book-metadata.md` if the manuscript has one, and otherwise falls back
to what can be derived, so the OPF always carries the required fields.

Fields, and what Inkstone makes of them:

    dc:title                      bookTitle            required, max 70 chars
    dc:description                synopsis             required
    dc:language                   language             required
    dc:creator                    author               optional
    dc:subject (repeatable)       tags                 optional
    inkstone:genre                categoryId           required
    inkstone:gender               leading gender       required
    inkstone:length               novels/short/super-short   optional
    inkstone:warning              general audiences    optional
    inkstone:abbreviation         max 15 chars         optional

Source syntax is a plain `Key: value` block, tags comma-separated:

    Title: The Ninth Furnace
    Author: authorss81
    Language: en
    Genre: fantasy
    Gender: male
    Length: novels
    Warning: general audiences
    Abbreviation: T9F
    Tags: industrial fantasy, progression, system

An unknown key is ignored rather than fatal, so a manuscript may keep extra notes
in the same file.
"""

from __future__ import annotations

import os
import re

MAX_TITLE = 70
MAX_ABBREVIATION = 15
VALID_LENGTHS = ("novels", "short", "super-short")
VALID_WARNINGS = (
    "general audiences",
    "teen audiences",
    "mature audiences",
    "adults only",
)
VALID_GENDERS = ("male", "female", "other")

# Genre words mapped to Inkstone's category vocabulary.
GENRE_CATEGORIES = {
    "fantasy": "fantasy",
    "high fantasy": "fantasy",
    "low fantasy": "fantasy",
    "urban fantasy": "fantasy",
    "sword and sorcery": "fantasy",
    "progression": "xianxia",
    "cultivation": "xianxia",
    "martial arts": "martial-arts",
    "mystery": "mystery",
    "detective": "mystery",
    "crime": "mystery",
    "thriller": "thriller",
    "suspense": "thriller",
    "science fiction": "scifi",
    "sci-fi": "scifi",
    "system": "xianxia",
    "adventure": "adventure",
    "action": "action",
    "horror": "horror",
    "romance": "romance",
    "historical": "history",
    "military": "military",
    "western": "western",
    "sports": "sports",
    "game": "games",
    "games": "games",
    "isekai": "isekai",
    "slice of life": "slice-of-life",
    "drama": "drama",
    "cyberpunk": "scifi",
    "steampunk": "scifi",
    "dystopian": "scifi",
    "apocalypse": "scifi",
    "industrial fantasy": "fantasy",
    "procedural": "mystery",
    "financial": "urban",
    "urban": "urban",
}


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


def normalise_length(value: str) -> str:
    lowered = value.strip().lower().replace(" ", "-")
    for candidate in VALID_LENGTHS:
        if candidate in lowered:
            return candidate
    return "novels"


def normalise_warning(value: str) -> str:
    lowered = value.strip().lower()
    if "general" in lowered:
        return "general audiences"
    if "teen" in lowered:
        return "teen audiences"
    if "adult" in lowered and "general" not in lowered:
        return "adults only"
    if "mature" in lowered:
        return "mature audiences"
    return "general audiences"


def normalise_gender(value: str) -> str:
    lowered = value.strip().lower()
    if "female" in lowered or "woman" in lowered or "women" in lowered:
        return "female"
    if lowered in ("other", "nonbinary", "non-binary"):
        return "other"
    return "male"


def normalise_genre(value: str) -> str:
    """Map a free-text genre onto an Inkstone category id."""
    if not value:
        return "fantasy"
    lowered = value.lower()
    for needle, category in GENRE_CATEGORIES.items():
        if needle in lowered:
            return category
    slug = re.sub(r"[^a-z0-9]+", "-", lowered.split(",")[0].strip()).strip("-")
    return slug or "fantasy"


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
    """Resolve every field the OPF needs, preferring the manuscript's own file."""
    fields = parse_metadata_file(root)

    resolved_title = clamp_title(_first(fields, "title", "booktitle") or title)
    resolved_description = (_first(fields, "description", "synopsis") or description).strip()

    tags: list[str] = []
    raw_tags = _first(fields, "tags", "subjects", "keywords")
    if raw_tags:
        tags = [t.strip() for t in re.split(r"[,;]", raw_tags) if t.strip()]

    genre_raw = _first(fields, "genre", "categoryid", "category", "inkstone genre")
    if not genre_raw:
        spec = ""
        spec_path = os.path.join(root, "NOVEL_SPEC.md")
        if os.path.isfile(spec_path):
            with open(spec_path, encoding="utf-8", errors="replace") as handle:
                spec = handle.read()
            genre_raw = re.search(r"(?im)^\s*Genre:\s*(.+)$", spec)
            genre_raw = genre_raw.group(1) if genre_raw else ""

    length_raw = _first(fields, "length", "inkstone length")
    if not length_raw:
        length_raw = "novels"
        spec_path = os.path.join(root, "NOVEL_SPEC.md")
        if os.path.isfile(spec_path):
            with open(spec_path, encoding="utf-8", errors="replace") as handle:
                text = handle.read()
            m = re.search(r"(?im)^\s*Length target:\s*(\d+)", text)
            if m and int(m.group(1)) < 100:
                length_raw = "short"

    return {
        "title": resolved_title,
        "description": resolved_description,
        "language": (_first(fields, "language") or "en").strip(),
        "creator": (_first(fields, "author", "creator") or author).strip(),
        "subjects": tags,
        "genre": normalise_genre(genre_raw),
        "gender": normalise_gender(_first(fields, "gender", "leading gender")),
        "length": normalise_length(length_raw),
        "warning": normalise_warning(_first(fields, "warning", "content warning")),
        "abbreviation": clamp_abbreviation(_first(fields, "abbreviation", "abbrev")),
    }


def cover_info(root: str) -> tuple[str, int | None]:
    """Return (relative path, declared id) for a cover image, if the repo has one."""
    for relative in ("cover.png", "state/cover.png", "dist/cover.png", "assets/cover.png"):
        if os.path.isfile(os.path.join(root, relative)):
            return relative, None
    return "", None