#!/usr/bin/env python3
"""Korpus-Validator für die HTML-Wissensbasis (nur Standardbibliothek).

Prüft jede HTML-Wissensseite unter ``public/`` und ``internal/`` gegen den
Repository-Vertrag und meldet jeden Verstoß:

* fehlende Metadaten (``title``, ``tags``, ``stand``, ``quelle``),
* nicht genau ein ``main`` bzw. ``h1``,
* doppelte ``id``-Attribute,
* Skripte oder externe Assets (CDN/JS/externe Fonts),
* tote relative Links,
* Markdown-Wissensseiten (nur HTML ist erlaubt),
* öffentliche Referenzen auf ``internal/``.

Root-Dateien wie README/PLAN/CHANGELOG bleiben Markdown und werden nicht
geprüft. Binäre Beweis-Assets (z. B. PDF) sind erlaubt und werden nicht
indexiert.
"""
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

REQUIRED_META = ("tags", "stand", "quelle")
KNOWLEDGE_DIRS = ("public", "internal")
HTML_SUFFIXES = (".html", ".htm")
EMBED_TAGS = {"iframe", "object", "embed"}
ASSET_ATTRS = ("src", "href", "poster", "data")


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tag_counts = {}
        self.ids = []
        self.metas = {}
        self.title_parts = []
        self._in_title = False
        self.scripts = 0
        self.event_handlers = 0
        self.embeds = 0
        # (tag, attr, value) für Asset-/Link-Prüfung
        self.assets = []

    def handle_starttag(self, tag, attrs):
        d = {k: (v if v is not None else "") for k, v in attrs}
        self.tag_counts[tag] = self.tag_counts.get(tag, 0) + 1

        if "id" in d and d["id"] != "":
            self.ids.append(d["id"])
        if tag == "script":
            self.scripts += 1
        if tag == "title":
            self._in_title = True
        if tag == "meta":
            name = d.get("name")
            if name:
                self.metas[name] = d.get("content", "")
        if tag in EMBED_TAGS:
            self.embeds += 1
        for key in d:
            if key.startswith("on"):
                self.event_handlers += 1
        for attr in ASSET_ATTRS:
            if attr in d and d[attr] != "":
                self.assets.append((tag, attr, d[attr]))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False

    def handle_data(self, data):
        if self._in_title:
            self.title_parts.append(data)


def _is_external(value):
    if value.startswith("//"):
        return True
    scheme = urlparse(value).scheme.lower()
    return scheme in ("http", "https", "ftp")


def _relative_target(page_path, value):
    """Löst einen relativen Link auf einen Pfad auf oder gibt None zurück,
    wenn er nicht gegen das Dateisystem geprüft werden soll."""
    low = value.lower()
    if value.startswith("#"):
        return None
    if low.startswith(("mailto:", "tel:", "data:", "javascript:")):
        return None
    path_part = value.split("#", 1)[0].split("?", 1)[0]
    if not path_part:
        return None
    return (page_path.parent / path_part).resolve()


def validate_page(page_path, root, rel):
    errors = []
    try:
        source = page_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        return [f"{rel}: nicht als UTF-8 lesbar ({exc})"]

    parser = PageParser()
    parser.feed(source)
    parser.close()

    title = "".join(parser.title_parts).strip()
    if not title:
        errors.append(f"{rel}: fehlender oder leerer <title>")
    for name in REQUIRED_META:
        if not parser.metas.get(name, "").strip():
            errors.append(f"{rel}: fehlendes Metadatum '{name}'")

    main_count = parser.tag_counts.get("main", 0)
    if main_count != 1:
        errors.append(f"{rel}: genau ein <main> erwartet (gefunden {main_count})")
    h1_count = parser.tag_counts.get("h1", 0)
    if h1_count != 1:
        errors.append(f"{rel}: genau ein <h1> erwartet (gefunden {h1_count})")

    seen = set()
    dups = []
    for value in parser.ids:
        if value in seen and value not in dups:
            dups.append(value)
        seen.add(value)
    if dups:
        errors.append(f"{rel}: doppelte id(s): {', '.join(sorted(dups))}")

    if parser.scripts:
        errors.append(f"{rel}: <script> ist nicht erlaubt")
    if parser.event_handlers:
        errors.append(f"{rel}: Inline-Event-Handler (JavaScript) nicht erlaubt")
    if parser.embeds:
        errors.append(f"{rel}: eingebettete externe Inhalte (iframe/object/embed) nicht erlaubt")

    for tag, attr, value in parser.assets:
        v = value.strip()
        if not v:
            continue
        if v.lower().startswith("javascript:"):
            errors.append(f"{rel}: javascript:-URL nicht erlaubt ({tag} {attr})")
            continue
        if _is_external(v):
            errors.append(f"{rel}: externes Asset/Link nicht erlaubt: {v}")
            continue
        target = _relative_target(page_path, v)
        if target is not None and not target.exists():
            errors.append(f"{rel}: toter relativer Link: {v}")

    # öffentliche Seiten dürfen internal/ nicht referenzieren
    if "public" in page_path.relative_to(root).parts and "internal/" in source:
        errors.append(f"{rel}: öffentliche Referenz auf internal/")

    return errors


def _knowledge_dirs(root):
    dirs = [root / name for name in KNOWLEDGE_DIRS if (root / name).is_dir()]
    return dirs or [root]


def validate_root(root):
    root = Path(root).resolve()
    errors = []
    for kdir in _knowledge_dirs(root):
        for path in sorted(kdir.rglob("*")):
            if path.is_dir():
                continue
            rel = path.relative_to(root).as_posix()
            suffix = path.suffix.lower()
            if suffix == ".md":
                errors.append(f"{rel}: Markdown-Wissensseite (nur HTML erlaubt)")
            elif suffix in HTML_SUFFIXES:
                errors.extend(validate_page(path, root, rel))
            # andere Endungen (PDF/Bilder) sind erlaubte Beweis-Assets
    return errors


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if len(argv) != 1:
        print("usage: validate_corpus.py <root>", file=sys.stderr)
        return 2
    errors = validate_root(argv[0])
    for err in errors:
        print(err, file=sys.stderr)
    if errors:
        print(f"{len(errors)} Verstoß/Verstöße gefunden", file=sys.stderr)
        return 1
    print("Korpus gültig")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
