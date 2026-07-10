#!/usr/bin/env python3
"""Korpus-Validator für die HTML-Wissensbasis (nur Standardbibliothek).

Prüft jede HTML-Wissensseite unter ``public/`` und ``internal/`` gegen den
Repository-Vertrag und meldet jeden Verstoß:

* fehlende kanonische Hülle (Doctype, genau ein ``html`` mit ``lang="de"``,
  genau ein ``head``/``body``, ``<meta charset="utf-8">``),
* fehlende Metadaten (``title``, ``tags``, ``stand``, ``quelle``),
* nicht genau ein ``main`` bzw. ``h1``, ``h1`` außerhalb von ``main``,
* doppelte ``id``-Attribute,
* Skripte, Inline-Event-Handler, Meta-Refresh, aktive/externe Assets,
  ``data:``-URIs, CSS-``@import``/``url()`` sowie ``srcset``/``xlink:href``,
* tote relative Links und Pfadflucht aus dem Korpus-Root,
* Symlinks (dürfen im public-only-Artefakt nicht verbleiben),
* Markdown-Wissensseiten (nur HTML ist erlaubt),
* öffentliche Referenzen auf ``internal/``.

Sichere externe Navigation (``<a>``/``<area>`` mit ``http(s)``/``mailto``/
``tel``) ist erlaubt; ladende Ressourcen dürfen nur lokal sein. Root-Dateien
wie README/PLAN/CHANGELOG bleiben Markdown und werden nicht geprüft. Binäre
Beweis-Assets (z. B. PDF) sind erlaubt und werden nicht indexiert.
"""
import html
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

REQUIRED_META = ("tags", "stand", "quelle")
KNOWLEDGE_DIRS = ("public", "internal")
HTML_SUFFIXES = (".html", ".htm")
EMBED_TAGS = {"iframe", "object", "embed"}
# URL-tragende Attribute; srcset wird gesondert (Liste) behandelt
URL_ATTRS = ("src", "href", "poster", "data", "xlink:href")
NAV_TAGS = {"a", "area"}
ACTIVE_SCHEMES = ("javascript", "vbscript")
NAV_EXTERNAL_SCHEMES = ("http", "https", "ftp", "mailto", "tel")

_CSS_URL = re.compile(r"url\(\s*(['\"]?)([^'\")]*)\1\s*\)", re.IGNORECASE)


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tag_counts = {}
        self.ids = []
        self.metas = {}
        self.title_parts = []
        self._in_title = False
        self._in_style = False
        self.scripts = 0
        self.event_handlers = 0
        self.embeds = 0
        self.meta_refresh = False
        self.has_doctype = False
        self.html_lang = ""
        self.charset = ""
        self._main_depth = 0
        self.h1_outside_main = False
        # (tag, attr, value) für Asset-/Link-Prüfung
        self.assets = []
        # CSS-Quellen (Style-Blöcke + Inline-style-Attribute)
        self.styles = []

    def handle_decl(self, decl):
        if decl.strip().lower().startswith("doctype html"):
            self.has_doctype = True

    def handle_starttag(self, tag, attrs):
        d = {k: (v if v is not None else "") for k, v in attrs}
        self.tag_counts[tag] = self.tag_counts.get(tag, 0) + 1

        if "id" in d and d["id"] != "":
            self.ids.append(d["id"])
        if tag == "script":
            self.scripts += 1
        if tag == "title":
            self._in_title = True
        if tag == "style":
            self._in_style = True
        if tag == "html":
            self.html_lang = d.get("lang", "")
        if tag == "main":
            self._main_depth += 1
        if tag == "h1" and self._main_depth <= 0:
            self.h1_outside_main = True
        if tag == "meta":
            if "charset" in d:
                self.charset = d.get("charset", "")
            if d.get("http-equiv", "").strip().lower() == "refresh":
                self.meta_refresh = True
            name = d.get("name")
            if name:
                self.metas[name] = d.get("content", "")
        if tag in EMBED_TAGS:
            self.embeds += 1
        for key in d:
            if key.startswith("on"):
                self.event_handlers += 1
        if d.get("style"):
            self.styles.append(d["style"])
        for attr in URL_ATTRS:
            if d.get(attr, "") != "":
                self.assets.append((tag, attr, d[attr]))
        if d.get("srcset", "") != "":
            for url in _srcset_urls(d["srcset"]):
                self.assets.append((tag, "srcset", url))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        if tag == "style":
            self._in_style = False
        if tag == "main" and self._main_depth > 0:
            self._main_depth -= 1

    def handle_data(self, data):
        if self._in_title:
            self.title_parts.append(data)
        if self._in_style:
            self.styles.append(data)


def _srcset_urls(value):
    urls = []
    for part in value.split(","):
        part = part.strip()
        if part:
            urls.append(part.split()[0])
    return urls


def _scheme(value):
    return urlparse(value).scheme.lower()


def _is_external(value):
    if value.startswith("//"):
        return True
    return _scheme(value) in ("http", "https", "ftp")


def _within(path, root):
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def _relative_target(page_path, value):
    """Löst einen relativen Link auf einen (aufgelösten) Pfad auf oder gibt
    None zurück, wenn er nicht gegen das Dateisystem geprüft werden soll."""
    if value.startswith("#"):
        return None
    path_part = value.split("#", 1)[0].split("?", 1)[0]
    if not path_part:
        return None
    return (page_path.parent / path_part).resolve()


def _check_local_target(page_path, kdir, value, rel, errors):
    target = _relative_target(page_path, value)
    if target is None:
        return
    if not _within(target, kdir):
        errors.append(f"{rel}: Pfadflucht, Ziel außerhalb des Korpus-Roots: {value}")
    elif not target.exists():
        errors.append(f"{rel}: toter relativer Link: {value}")


def validate_page(page_path, root, kdir, rel):
    errors = []
    try:
        source = page_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        return [f"{rel}: nicht als UTF-8 lesbar ({exc})"]

    parser = PageParser()
    parser.feed(source)
    parser.close()

    # kanonische Hülle
    if not parser.has_doctype:
        errors.append(f"{rel}: fehlendes <!doctype html>")
    html_count = parser.tag_counts.get("html", 0)
    if html_count != 1:
        errors.append(f"{rel}: genau ein <html> erwartet (gefunden {html_count})")
    if parser.html_lang.strip().lower() != "de":
        errors.append(f'{rel}: <html lang="de"> erwartet (gefunden "{parser.html_lang}")')
    head_count = parser.tag_counts.get("head", 0)
    if head_count != 1:
        errors.append(f"{rel}: genau ein <head> erwartet (gefunden {head_count})")
    body_count = parser.tag_counts.get("body", 0)
    if body_count != 1:
        errors.append(f"{rel}: genau ein <body> erwartet (gefunden {body_count})")
    if parser.charset.strip().lower() != "utf-8":
        errors.append(f'{rel}: <meta charset="utf-8"> erwartet')

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
    if parser.h1_outside_main:
        errors.append(f"{rel}: <h1> muss innerhalb von <main> liegen")

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
    if parser.meta_refresh:
        errors.append(f"{rel}: meta-refresh (aktive Weiterleitung) nicht erlaubt")

    for tag, attr, value in parser.assets:
        v = value.strip()
        if not v:
            continue
        scheme = _scheme(v)
        if scheme in ACTIVE_SCHEMES:
            errors.append(f"{rel}: aktives Schema ({scheme}:) nicht erlaubt ({tag} {attr})")
            continue
        if scheme == "data" or v.lower().startswith("data:"):
            errors.append(f"{rel}: data:-URI nicht erlaubt ({tag} {attr})")
            continue
        if tag in NAV_TAGS and attr == "href":
            # sichere externe Navigation ist erlaubt
            if scheme in NAV_EXTERNAL_SCHEMES or v.startswith("//"):
                continue
            _check_local_target(page_path, kdir, v, rel, errors)
            continue
        # ladende Ressource: extern verboten, sonst lokal prüfen
        if _is_external(v):
            errors.append(f"{rel}: externes Asset nicht erlaubt: {v}")
            continue
        _check_local_target(page_path, kdir, v, rel, errors)

    # CSS aus Style-Blöcken und Inline-style-Attributen prüfen
    for css in parser.styles:
        if "@import" in css.lower():
            errors.append(f"{rel}: CSS @import nicht erlaubt")
        for match in _CSS_URL.finditer(css):
            url = match.group(2).strip()
            if not url:
                continue
            scheme = _scheme(url)
            if scheme in ACTIVE_SCHEMES or scheme == "data" or url.lower().startswith("data:"):
                errors.append(f"{rel}: aktive/data-URL in CSS nicht erlaubt: {url}")
            elif _is_external(url):
                errors.append(f"{rel}: externes Asset in CSS nicht erlaubt: {url}")

    # öffentliche Seiten dürfen internal/ nicht referenzieren
    # (entitäten-dekodiert und case-insensitiv, damit INTERNAL/ oder internal&#47; greifen)
    if "public" in page_path.relative_to(root).parts:
        if "internal/" in html.unescape(source).lower():
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
            # Symlinks vor is_dir() prüfen: dürfen im public-only-Artefakt nicht
            # verbleiben und könnten sonst auf internal/ oder Host-Dateien zeigen
            if path.is_symlink():
                errors.append(f"{path.relative_to(root).as_posix()}: Symlink nicht erlaubt")
                continue
            if path.is_dir():
                continue
            rel = path.relative_to(root).as_posix()
            suffix = path.suffix.lower()
            if suffix == ".md":
                errors.append(f"{rel}: Markdown-Wissensseite (nur HTML erlaubt)")
            elif suffix in HTML_SUFFIXES:
                errors.extend(validate_page(path, root, kdir, rel))
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
