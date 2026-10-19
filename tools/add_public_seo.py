#!/usr/bin/env python3
"""Ergaenzt SEO-Metadaten fuer alle oeffentlichen Wissensseiten.

Der Korpus bleibt statisches HTML. Fuer Suchmaschinen werden pro Seite eine
knappe Description und ein explizites index/follow gesetzt. Die Description
wird deterministisch aus dem ersten sichtbaren Absatz erzeugt.
"""

from __future__ import annotations

import argparse
import html
import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
MAX_DESCRIPTION = 160


class TextCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.in_p = False
        self.parts: list[str] = []
        self.done = False

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag == "p" and not self.done:
            self.in_p = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "p" and self.in_p:
            self.in_p = False
            self.done = True

    def handle_data(self, data: str) -> None:
        if self.in_p and not self.done:
            self.parts.append(data)


def first_paragraph(source: str) -> str:
    parser = TextCollector()
    parser.feed(source)
    text = " ".join(" ".join(parser.parts).split())
    if text.lower().startswith("überblick."):
        text = text[len("Überblick."):].strip()
    return text


def shorten(text: str, limit: int = MAX_DESCRIPTION) -> str:
    if len(text) <= limit:
        return text
    cut = text[: limit + 1].rsplit(" ", 1)[0].rstrip(" ,;:")
    return cut + "…"


def upsert_meta(source: str, name: str, content: str) -> str:
    pattern = re.compile(
        rf'<meta\s+name=["\']{re.escape(name)}["\']\s+content=["\'][^"\']*["\']\s*/?>',
        re.IGNORECASE,
    )
    tag = f'<meta name="{name}" content="{html.escape(content, quote=True)}">'
    if pattern.search(source):
        return pattern.sub(tag, source, count=1)
    title_end = re.search(r"</title\s*>", source, re.IGNORECASE)
    if not title_end:
        raise ValueError("title fehlt")
    pos = title_end.end()
    return source[:pos] + "\n  " + tag + source[pos:]


def process(path: Path, write: bool) -> bool:
    source = path.read_text(encoding="utf-8")
    description = shorten(first_paragraph(source))
    if not description:
        raise ValueError(f"{path}: erster Absatz fehlt")
    updated = upsert_meta(source, "description", description)
    updated = upsert_meta(updated, "robots", "index, follow")
    if updated == source:
        return False
    if write:
        path.write_text(updated, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    changed = 0
    for path in sorted(PUBLIC.rglob("*.html")):
        if process(path, args.write):
            changed += 1
            print(path.relative_to(ROOT))
    print(f"[public-seo] {changed} Seiten {'aktualisiert' if args.write else 'würden aktualisiert'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
