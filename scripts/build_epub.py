#!/usr/bin/env python3
"""Build two EPUBs for a finished novel.

    <book>-volumes.epub   volume title pages, then the chapters of each volume
    <book>-flat.epub      every chapter in order, no volume divisions

Chapter numbers are dropped: a chapter's title is its name only. Written
against the standard library so it cannot fail on a missing package.
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import os
import re
import sys
import xml.etree.ElementTree as ET
import zipfile

import book_metadata

CHAPTER_RE = re.compile(r"^chapters/volume-(\d+)/chapter-(\d+)\.md$", re.M)
NUMBER_PREFIX = re.compile(
    r"^\s*(?:chapter|ch)\s*[0-9ivxlcdm]+\s*(?:[-–—:.]|\s)\s*", re.I
)
VOLUME_DIR_RE = re.compile(r"^volume-(\d+)$")

# XML 1.0 forbids most control characters, and a single stray one (a manuscript
# once contained a literal backspace) makes an otherwise valid document
# unparseable. Strip them at the point where text becomes markup.
XML_FORBIDDEN = re.compile(
    "[^\x09\x0A\x0D\x20-퟿-�\U00010000-\U0010FFFF]"
)


def xml_safe(text: str) -> str:
    return XML_FORBIDDEN.sub("", text)


# ---------------------------------------------------------------- discovery


def find_chapters(root: str) -> list[tuple[int, int, str]]:
    """Return (volume, number, path) for every chapter file, in reading order."""
    found: list[tuple[int, int, str]] = []
    chapters_root = os.path.join(root, "chapters")
    if not os.path.isdir(chapters_root):
        return found
    for entry in sorted(os.listdir(chapters_root)):
        match = VOLUME_DIR_RE.match(entry)
        if not match:
            continue
        volume = int(match.group(1))
        vdir = os.path.join(chapters_root, entry)
        for name in os.listdir(vdir):
            m = re.match(r"^chapter-(\d+)\.md$", name)
            if m:
                found.append((volume, int(m.group(1)), os.path.join(vdir, name)))
    found.sort(key=lambda item: (item[0], item[1]))
    return found


def tidy(text: str) -> str:
    """Strip emphasis, replacement characters and stray punctuation."""
    text = xml_safe(text)
    text = text.replace("�", " ")
    text = re.sub(r"\*+", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip(" \t-_`*#,;:.–—·()[]")


def field_value(text: str) -> str | None:
    """A '**Title:** x' or 'Title: x' field, which is the reliable source."""
    m = re.search(r"^\**\s*Title\**\s*:\s*(.+?)\s*$", text, re.M | re.I)
    return tidy(m.group(1)) if m else None


def book_title(root: str, fallback: str, override: str | None = None) -> str:
    if override:
        return tidy(override)
    spec = os.path.join(root, "NOVEL_SPEC.md")
    if os.path.isfile(spec):
        with open(spec, encoding="utf-8", errors="replace") as handle:
            text = handle.read()
        found = field_value(text)
        if found:
            return found
    return fallback.replace("novel-", "").replace("-", " ").title()


def series_volume_titles(root: str) -> dict[int, str]:
    """Volume names from '### Volume 05: The City Below the Weather' headings."""
    path = os.path.join(root, "outline", "series.md")
    titles: dict[int, str] = {}
    if not os.path.isfile(path):
        return titles
    with open(path, encoding="utf-8", errors="replace") as handle:
        for line in handle:
            m = re.match(r"^#{2,4}\s*volume\s+(\d+)\s*[:\-–]\s*(.+?)\s*$", line.strip(), re.I)
            if m:
                name = re.split(r"\(|—|–|\s-\s", tidy(m.group(2)))[0].strip()
                if name:
                    titles[int(m.group(1))] = name
    return titles


def volume_titles(root: str, volumes: set[int]) -> dict[int, str]:
    from_series = series_volume_titles(root)
    titles: dict[int, str] = {}
    for volume in sorted(volumes):
        path = os.path.join(root, "outline", f"volume-{volume:02d}.md")
        if not os.path.isfile(path):
            path = os.path.join(root, "outline", f"volume-{volume}.md")
        title = ""
        if os.path.isfile(path):
            with open(path, encoding="utf-8", errors="replace") as handle:
                text = handle.read()
            title = field_value(text) or ""
            if not title:
                heading = ""
                for line in text.splitlines():
                    m = re.match(r"^#\s+(.+?)\s*$", line)
                    if m:
                        heading = m.group(1)
                        break
                # "*The First Turn*" inside the heading is the volume name.
                emph = re.search(r"\*([^*]{2,120})\*", heading)
                if emph:
                    title = tidy(emph.group(1))
                else:
                    title = tidy(heading)
                    title = re.sub(
                        r"\b(chapters?\s+.*|plan of record|outline|volume\s+\d+)\b.*$",
                        "",
                        title,
                        flags=re.I,
                    ).strip(" -–—:")
        if not title or re.fullmatch(r"volume\s*\d*", title, re.I):
            title = from_series.get(volume) or f"Volume {volume}"
        titles[volume] = title
    return titles


def clean_title(raw: str) -> str:
    title = raw.strip().strip("*_` ")
    title = re.sub(r"^\s*volume\s+[0-9ivxlcdm]+\s*[-–—:]?\s*", "", title, flags=re.I)
    title = re.sub(r"\s+outline\b.*$", "", title, flags=re.I)
    title = title.strip(" *_`#-–—:·,.")
    return NUMBER_PREFIX.sub("", title).strip()


# ------------------------------------------------------------- markdown->xhtml


def _markup(text: str) -> str:
    out = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    out = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", out)
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", out)


def _well_formed(fragment: str) -> bool:
    try:
        ET.fromstring(f"<p>{fragment}</p>")
    except Exception:
        return False
    return True


def inline(text: str) -> str:
    """Escape, then apply inline markup. Prose with a stray '*' or '` can
    produce unbalanced or mis-nested tags, so the result is parsed and the
    plain escaped text is used whenever it is not well-formed."""
    plain = html.escape(text, quote=False)
    if "*" not in plain and "`" not in plain:
        return plain
    out = _markup(plain)
    return out if _well_formed(out) else plain


def markdown_to_xhtml(body: str, heading: str | None = None) -> str:
    parts: list[str] = []
    if heading:
        parts.append(f"<h1>{html.escape(heading)}</h1>")

    lines = body.splitlines()
    index = 0
    while index < len(lines):
        line = lines[index]
        stripped = line.strip()
        if not stripped:
            index += 1
            continue
        if re.match(r"^(-{3,}|\*{3,}|_{3,})$", stripped):
            parts.append("<hr/>")
            index += 1
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if m:
            level = min(len(m.group(1)) + 1, 6)
            parts.append(f"<h{level}>{inline(m.group(2).strip())}</h{level}>")
            index += 1
            continue
        if stripped.startswith(">"):
            quote: list[str] = []
            while index < len(lines) and lines[index].strip().startswith(">"):
                quote.append(lines[index].strip().lstrip(">").strip())
                index += 1
            parts.append(f"<blockquote><p>{inline(' '.join(quote))}</p></blockquote>")
            continue
        if re.match(r"^([-*+]|\d+[.)])\s+", stripped):
            items: list[str] = []
            while index < len(lines) and re.match(r"^\s*([-*+]|\d+[.)])\s+", lines[index]):
                items.append(re.sub(r"^\s*([-*+]|\d+[.)])\s+", "", lines[index]).strip())
                index += 1
            body_html = "".join(f"<li>{inline(item)}</li>" for item in items)
            parts.append(f"<ul>{body_html}</ul>")
            continue
        paragraph: list[str] = []
        while index < len(lines) and lines[index].strip():
            nxt = lines[index].strip()
            if re.match(r"^(#{1,6}\s|>|(-{3,}|\*{3,}|_{3,})$)", nxt):
                break
            paragraph.append(nxt)
            index += 1
        if paragraph:
            parts.append(f"<p>{inline(' '.join(paragraph))}</p>")
    return "\n".join(parts)


def split_title(text: str) -> tuple[str | None, str]:
    """Return (chapter name without its number, body without the title line)."""
    lines = text.splitlines()
    for position, line in enumerate(lines):
        m = re.match(r"^#\s+(.+?)\s*$", line)
        if m:
            title = clean_title(m.group(1))
            return (title or None), "\n".join(lines[:position] + lines[position + 1 :])
    return None, text


# ------------------------------------------------------------------ epub glue

CONTAINER = """<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>
"""

STYLE = """body{font-family:serif;line-height:1.5;margin:1.2em;}
h1,h2,h3{line-height:1.25;}blockquote{margin-left:1.5em;font-style:italic;}
hr{margin:1.5em 0;border:0;border-top:1px solid #999;}
"""

CONTAINER_ITEM = ("text/html", "chapters.xhtml")


def document(title: str, body: str, epub_ns: bool = False) -> str:
    ops = ' xmlns:epub="http://www.idpf.org/2007/ops"' if epub_ns else ""
    title = xml_safe(title)
    body = xml_safe(body)
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<!DOCTYPE html>\n'
        '<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en"'
        f"{ops}>\n"
        f"<head><title>{html.escape(title)}</title>"
        '<meta charset="utf-8"/></head>\n'
        f"<body>\n{body}\n</body>\n</html>\n"
    )


def read_sections(path: str) -> dict[str, str]:
    """Split a markdown file into '## Heading' -> body."""
    sections: dict[str, str] = {}
    if not os.path.isfile(path):
        return sections
    with open(path, encoding="utf-8", errors="replace") as handle:
        text = handle.read()
    current = ""
    buffer: list[str] = []
    for line in text.splitlines():
        m = re.match(r"^#{1,3}\s+(.+?)\s*$", line)
        if m:
            if current:
                sections[current] = "\n".join(buffer).strip()
            current = tidy(m.group(1)).lower()
            buffer = []
        else:
            buffer.append(line)
    if current:
        sections[current] = "\n".join(buffer).strip()
    return sections


def spec_field(root: str, label: str) -> str:
    path = os.path.join(root, "NOVEL_SPEC.md")
    if not os.path.isfile(path):
        return ""
    with open(path, encoding="utf-8", errors="replace") as handle:
        for line in handle:
            m = re.match(rf"^\s*{label}\s*:\s*(.+?)\s*$", line, re.I)
            if m:
                return tidy(m.group(1))
    return ""


MAX_TITLE_WORDS = 14
MAX_TITLE_CHARS = 90


def tighten_title(title: str) -> str:
    """Force a title back to something that reads in a table of contents.

    A model asked for a chapter name will sometimes hand back the scene: the
    place, the hour, the weather, the ages of everyone present. One generated
    novel put 167 such titles in its final third and every one was unreadable
    in the nav. Clamp the length and fall back to the number when a title
    cannot be rescued.
    """
    # Prefer a natural clause break over a mid-phrase cut.
    if len(title) > MAX_TITLE_CHARS or len(title.split()) > MAX_TITLE_WORDS:
        clause = re.split(
            r"\s+(?:And|But|While|After|Because|Since|On|At|With|The Second|"
            r"Then|So|Yet|When|Which|Who|That)\s+",
            title,
            maxsplit=1,
        )[0].strip(" ,;:-—")
        # A comma is also a reasonable place to stop, if the first half stands.
        if len(clause) >= 15 and clause.count(",") == 0 and len(clause) <= MAX_TITLE_CHARS:
            return clause
        words = title.split()
        trimmed = " ".join(words[:MAX_TITLE_WORDS])
        if len(trimmed) > MAX_TITLE_CHARS:
            trimmed = trimmed[:MAX_TITLE_CHARS].rsplit(" ", 1)[0]
        return (trimmed or title[:MAX_TITLE_CHARS]).strip(" ,;:-—")
    return title.strip(" ,;:-—")


def unique_titles(entries: list[tuple[int, int, str, str]]) -> list[tuple[int, int, str, str]]:
    """Clamp titles and disambiguate repeats by appending the chapter number."""
    seen: dict[str, int] = {}
    out: list[tuple[int, int, str, str]] = []
    for volume, number, name, body in entries:
        name = tighten_title(name) or f"Chapter {number}"
        key = name.casefold()
        if key in seen:
            seen[key] += 1
            name = f"{name} ({seen[key] + 1})"
        else:
            seen[key] = 0
        out.append((volume, number, name, body))
    return out


def front_matter(root: str) -> dict[str, str]:
    """Blurb and synopsis, written by state/synopsis.md when the pipeline has
    produced one, otherwise the premise from NOVEL_SPEC.md."""
    written = read_sections(os.path.join(root, "state", "synopsis.md"))
    spec = read_sections(os.path.join(root, "NOVEL_SPEC.md"))
    blurb = written.get("back cover") or written.get("back-cover") or written.get("blurb", "")
    synopsis = written.get("synopsis") or spec.get("premise") or ""
    return {
        "blurb": blurb,
        "synopsis": synopsis,
        "genre": spec_field(root, "Genre"),
        "logline": spec.get("premise", ""),
    }


def build(
    out_path: str,
    book: str,
    sections: list[tuple[str, str, str]],
    author: str,
    stamp: dt.datetime,
    meta: dict,
    cover_path: str = "",
) -> None:
    """sections: list of (document filename, document title, xhtml body).

    Entries carry a fixed timestamp so an unchanged manuscript rebuilds to a
    byte-identical file and the commit step can skip it."""
    """sections: list of (document filename, document title, xhtml body)."""
    identifier = f"urn:uuid:{re.sub(r'[^0-9a-f]', '', book)[:32] or 'novel'}"
    now = stamp.strftime("%Y-%m-%dT%H:%M:%SZ")
    zip_date = (
        max(stamp.year, 1980),
        stamp.month,
        stamp.day,
        stamp.hour,
        stamp.minute,
        stamp.second,
    )

    manifest = [
        '<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>',
        '<item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>',
        '<item id="style" href="style.css" media-type="text/css"/>',
    ]
    if cover_path:
        manifest.append(
            '<item id="cover-image" href="cover.png" media-type="image/png" '
            'properties="cover-image"/>'
        )
    spine: list[str] = []
    nav_points: list[str] = []
    ncx_points: list[str] = []

    for order, (name, doc_title, _body) in enumerate(sections, start=1):
        manifest.append(
            f'<item id="d{order}" href="{name}" media-type="application/xhtml+xml"/>'
        )
        spine.append(f'<itemref idref="d{order}"/>')
        nav_points.append(
            f'<li><a href="{name}">{html.escape(doc_title)}</a></li>'
        )
        ncx_points.append(
            f'<navPoint id="np{order}" playOrder="{order}">'
            f"<navLabel><text>{html.escape(doc_title)}</text></navLabel>"
            f'<content src="{name}"/></navPoint>'
        )

    meta_lines = [
        f'<dc:identifier id="bookid">{identifier}</dc:identifier>',
        f'<dc:title>{html.escape(meta["title"])}</dc:title>',
    ]
    if meta["description"]:
        meta_lines.append(f'<dc:description>{xml_safe(meta["description"])}</dc:description>')
    meta_lines.append(f'<dc:language>{html.escape(meta["language"])}</dc:language>')
    if meta["creator"]:
        meta_lines.append(f'<dc:creator>{html.escape(meta["creator"])}</dc:creator>')
    for _category, tag in meta["tags"]:
        meta_lines.append(f'<dc:subject>{html.escape(tag)}</dc:subject>')
    meta_lines.append(f'<meta property="dcterms:modified">{now}</meta>')
    # Inkstone records these as closed numeric lists, so the values are ids.
    meta_lines.append(f'<meta property="inkstone:genre">{meta["genre"]}</meta>')
    meta_lines.append(f'<meta property="inkstone:gender">{html.escape(meta["gender"])}</meta>')
    meta_lines.append(f'<meta property="inkstone:length">{html.escape(meta["length"])}</meta>')
    meta_lines.append(f'<meta property="inkstone:warning">{html.escape(meta["warning"])}</meta>')
    meta_lines.append(
        f'<meta property="inkstone:relationship">{html.escape(meta["relationship"])}</meta>'
    )
    if meta["abbreviation"]:
        meta_lines.append(
            f'<meta property="inkstone:abbreviation">{html.escape(meta["abbreviation"])}</meta>'
        )
    if cover_path:
        meta_lines.append('<meta name="cover" content="cover-image"/>')

    opf = f"""<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="bookid">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    {chr(10).join("    " + line for line in meta_lines)}
  </metadata>
  <manifest>
    {chr(10).join("    " + item for item in manifest)}
  </manifest>
  <spine>
    {chr(10).join("    " + item for item in spine)}
  </spine>
</package>
"""

    nav = document(
        "Contents",
        f"<h1>Contents</h1><nav epub:type=\"toc\" id=\"toc\"><ol>"
        + "".join(nav_points)
        + "</ol></nav>",
        epub_ns=True,
    )
    ncx = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">\n'
        f'  <head><meta name="dtb:uid" content="{identifier}"/></head>\n'
        f'  <docTitle><text>{html.escape(book)}</text></docTitle>\n'
        "  <navMap>\n    "
        + "\n    ".join(ncx_points)
        + "\n  </navMap>\n</ncx>\n"
    )

    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)

    def entry(name: str, data: str, stored: bool = False) -> zipfile.ZipInfo:
        info = zipfile.ZipInfo(name, date_time=zip_date)
        info.compress_type = zipfile.ZIP_STORED if stored else zipfile.ZIP_DEFLATED
        info.external_attr = 0o644 << 16
        return info

    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as zf:
        # The mimetype entry must be first and stored uncompressed.
        zf.writestr(entry("mimetype", "", stored=True), "application/epub+zip")
        for name, text in (
            ("META-INF/container.xml", CONTAINER),
            ("OEBPS/style.css", STYLE),
            ("OEBPS/content.opf", opf),
            ("OEBPS/nav.xhtml", nav),
            ("OEBPS/toc.ncx", ncx),
        ):
            zf.writestr(entry(name, text), text)
        for name, _doc_title, body in sections:
            zf.writestr(entry(f"OEBPS/{name}", body), body)
        if cover_path and os.path.isfile(cover_path):
            with open(cover_path, "rb") as handle:
                zf.writestr(entry("OEBPS/cover.png", ""), handle.read())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--out-dir", default="dist")
    parser.add_argument("--author", default="authorss81")
    parser.add_argument("--title", default=None)
    args = parser.parse_args()

    root = os.path.abspath(args.root)
    chapters = find_chapters(root)
    if not chapters:
        print("no chapters found", file=sys.stderr)
        return 1

    title = book_title(root, os.path.basename(root), args.title)
    volumes = {volume for volume, _, _ in chapters}
    vol_titles = volume_titles(root, volumes)

    # Read once, keep both renderings. The newest chapter decides the archive
    # timestamp so a rebuild of unchanged prose is byte-identical.
    rendered: list[tuple[int, int, str, str]] = []  # volume, number, name, body
    newest = 0.0
    for volume, number, path in chapters:
        with open(path, encoding="utf-8", errors="replace") as handle:
            raw = handle.read()
        newest = max(newest, os.path.getmtime(path))
        name, body = split_title(raw)
        if not name:
            name = f"Chapter {number}"
        rendered.append((volume, number, name, body))

    rendered = unique_titles(rendered)

    stamp = (
        dt.datetime.fromtimestamp(newest, dt.timezone.utc)
        if newest
        else dt.datetime(1980, 1, 1, tzinfo=dt.timezone.utc)
    )
    matter = front_matter(root)
    meta = book_metadata.build_metadata(
        root, title=title, author=args.author, description=matter["synopsis"]
    )
    cover_path = book_metadata.cover_path(root)

    def title_page(count: str) -> str:
        bits = [f"<h1>{html.escape(title)}</h1>", f"<p>{html.escape(args.author)}</p>", f"<p>{count}</p>"]
        if matter["genre"]:
            bits.append(f"<p>{html.escape(matter['genre'])}</p>")
        if matter["blurb"]:
            bits.append("<hr/>" + markdown_to_xhtml(matter["blurb"]))
        return document(title, "\n".join(bits))

    def synopsis_page() -> str:
        body = matter["synopsis"] or matter["logline"]
        if not body:
            return ""
        return document("Synopsis", f"<h1>Synopsis</h1>\n{markdown_to_xhtml(body)}")

    # Flat edition: title page, synopsis, then every chapter in order.
    flat_sections: list[tuple[str, str, str]] = [
        ("title.xhtml", title, title_page(f"{len(rendered)} chapters")),
    ]
    page = synopsis_page()
    if page:
        flat_sections.append(("synopsis.xhtml", "Synopsis", page))
    for volume, number, name, body in rendered:
        flat_sections.append(
            (f"ch-{volume:02d}-{number:04d}.xhtml", name, document(name, markdown_to_xhtml(body, name)))
        )
    flat_path = os.path.join(args.out_dir, f"{os.path.basename(root)}-flat.epub")
    build(flat_path, title, flat_sections, args.author, stamp, meta, cover_path)
    print(f"wrote {flat_path} ({len(rendered)} chapters)")

    # Volume edition: a title page per volume, then its chapters.
    vol_sections: list[tuple[str, str, str]] = [
        (
            "title.xhtml",
            title,
            title_page(f"{len(rendered)} chapters in {len(volumes)} volumes"),
        ),
    ]
    page = synopsis_page()
    if page:
        vol_sections.append(("synopsis.xhtml", "Synopsis", page))
    for volume in sorted(volumes):
        heading = vol_titles.get(volume, f"Volume {volume}")
        vol_sections.append(
            (f"volume-{volume:02d}.xhtml", heading, document(heading, f"<h1>{html.escape(heading)}</h1>"))
        )
        for vol, number, name, body in rendered:
            if vol == volume:
                vol_sections.append(
                    (
                        f"ch-{vol:02d}-{number:04d}.xhtml",
                        name,
                        document(name, markdown_to_xhtml(body, name)),
                    )
                )
    vol_path = os.path.join(args.out_dir, f"{os.path.basename(root)}-volumes.epub")
    build(vol_path, title, vol_sections, args.author, stamp, meta, cover_path)
    print(f"wrote {vol_path} ({len(vol_sections)} sections)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
