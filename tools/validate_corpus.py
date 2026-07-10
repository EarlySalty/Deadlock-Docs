#!/usr/bin/env python3
"""Korpus-Validator für die HTML-Wissensbasis (nur Standardbibliothek).

Prüft jede HTML-Wissensseite unter ``public/`` und ``internal/`` gegen den
Repository-Vertrag und meldet jeden Verstoß:

* fehlende oder falsch verschachtelte kanonische Hülle (Doctype, genau ein
  ``html`` mit ``lang="de"``, genau ein ``head``/``body`` direkt unter ``html``,
  genau ein ``<meta charset="utf-8">``),
* fehlende oder mehrfache Metadaten (genau ein ``title``, je genau ein
  ``tags``/``stand``/``quelle`` mit echtem Inhalt),
* nicht genau ein ``main`` bzw. ``h1``, ``h1`` nicht direkt unter ``main``,
  direkte ``section`` in ``main`` ohne ``id`` oder ``h2``,
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
# Runtime liefert ausschließlich .html; .htm gilt als Vertragsverstoß.
HTML_SUFFIXES = (".html",)
EMBED_TAGS = {"iframe", "object", "embed"}
# URL-tragende Attribute; srcset/imagesrcset werden gesondert (Liste) behandelt
URL_ATTRS = ("src", "href", "poster", "data", "xlink:href", "action", "formaction", "ping")
# responsive Bildquellen (Komma-Liste mit Deskriptoren) – wie <img>, so <link preload>
SRCSET_ATTRS = ("srcset", "imagesrcset")
NAV_TAGS = {"a", "area"}
ACTIVE_SCHEMES = ("javascript", "vbscript")
# Sichere externe Navigation exakt wie im Docstring: http(s)/mailto/tel (kein ftp).
NAV_EXTERNAL_SCHEMES = ("http", "https", "mailto", "tel")
# Void-Elemente werden nie auf den Verschachtelungs-Stack gelegt.
VOID_ELEMENTS = {
    "area", "base", "br", "col", "embed", "hr", "img",
    "input", "link", "meta", "param", "source", "track", "wbr",
}
# HTML5 repariert Block-/Heading-Elemente aus <h1> heraus. Nur passives Inline-
# Text-Formatting darf als Nachfahre eines <h1> auftreten; Block-/Heading-Nachfahren
# würden die Rust-Runtime umbauen (h1 verliert Text) und werden abgelehnt.
H1_PHRASING = {
    "a", "abbr", "b", "bdi", "bdo", "br", "cite", "code", "data", "del",
    "dfn", "em", "i", "ins", "kbd", "mark", "q", "rp", "rt", "ruby", "s",
    "samp", "small", "span", "strong", "sub", "sup", "time", "u", "var", "wbr",
}
# Browser entfernen Tab/Zeilenumbruch/CR überall aus URLs …
_URL_REMOVE_MAP = {ord("\t"): None, ord("\n"): None, ord("\r"): None}
# … und schneiden führende/abschließende C0-Steuerzeichen (0x00–0x1F) samt
# Leerzeichen ab. str.strip() lässt die meisten C0-Zeichen stehen – deshalb hier
# explizit der volle Bereich, sonst fällt „\x01//host" fälschlich als lokal durch.
_URL_STRIP_CHARS = "".join(chr(c) for c in range(0x21))

_CSS_URL = re.compile(r"url\(\s*(['\"]?)([^'\")]*)\1\s*\)", re.IGNORECASE)


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tag_counts = {}
        self.ids = []
        self.metas = {}
        # wie oft ein <meta name="..."> vorkam (Eindeutigkeit der Pflicht-Metas)
        self.meta_counts = {}
        self.charset_count = 0
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
        # (tag, attr, value) für Asset-/Link-Prüfung
        self.assets = []
        # CSS-Quellen (Style-Blöcke + Inline-style-Attribute)
        self.styles = []
        # Verschachtelungs-Stack aus Knoten-Dicts für Eltern-/Direktkind-Verträge
        self._stack = []
        # True, sobald ein schließendes Tag nicht das oberste offene Element
        # schließt (unmatched/misnested). Kanonische Seiten sind wohl-verschachtelt.
        self.malformed = False
        self.h1_parents = []
        # h1-Knoten (Sichttext-Prüfung wie in der Runtime)
        self.h1_nodes = []
        self.head_parents = []
        self.body_parents = []
        # direkte <section>-Kinder von <main> (Knoten, damit Kind-Tags erfasst sind)
        self.main_sections = []
        # (tag, attr) je doppeltem Attributnamen pro Element
        self.dup_attrs = []

    def handle_decl(self, decl):
        if decl.strip().lower().startswith("doctype html"):
            self.has_doctype = True

    def _open(self, tag, attrs, self_closing):
        # Doppelte Attributnamen vor der Dict-Bildung erfassen: HTML5 behält das
        # erste Attribut, ein Dict das letzte – sonst umgehen Duplikate Vertrag
        # und Runtime. Nur Name+Tag melden, nie den (evtl. sensiblen) Wert.
        seen_attrs = set()
        for key, _ in attrs:
            if key in seen_attrs:
                self.dup_attrs.append((tag, key))
            else:
                seen_attrs.add(key)
        d = {k: (v if v is not None else "") for k, v in attrs}
        self.tag_counts[tag] = self.tag_counts.get(tag, 0) + 1

        parent = self._stack[-1] if self._stack else None
        parent_tag = parent["tag"] if parent else None
        node = {"tag": tag, "id": d.get("id", ""), "child_tags": set(),
                "children": [], "text": []}
        if parent is not None:
            parent["child_tags"].add(tag)
            parent["children"].append(node)

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
        if tag == "h1":
            self.h1_parents.append(parent_tag)
            self.h1_nodes.append(node)
        if tag == "head":
            self.head_parents.append(parent_tag)
        if tag == "body":
            self.body_parents.append(parent_tag)
        if tag == "section" and parent_tag == "main":
            self.main_sections.append(node)
        if tag == "meta":
            if "charset" in d:
                self.charset_count += 1
                self.charset = d.get("charset", "")
            if d.get("http-equiv", "").strip().lower() == "refresh":
                self.meta_refresh = True
            name = d.get("name")
            if name:
                self.meta_counts[name] = self.meta_counts.get(name, 0) + 1
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
        for attr in SRCSET_ATTRS:
            if d.get(attr, "") != "":
                for url in _srcset_urls(d[attr]):
                    self.assets.append((tag, attr, url))

        if not self_closing and tag not in VOID_ELEMENTS:
            self._stack.append(node)

    def handle_starttag(self, tag, attrs):
        self._open(tag, attrs, False)

    def handle_startendtag(self, tag, attrs):
        # Slash-Selbstschluss (<tag/>) ist in HTML5 nur für Void-Elemente gültig.
        # Bei jedem anderen Tag ignoriert der HTML5-Scraper den Slash und hält das
        # Element offen (schluckt den Folgeinhalt), während Python-HTMLParser es
        # sofort schließt – eine Paritätslücke. Fail-closed als fehlerhafte
        # Verschachtelung ablehnen.
        if tag not in VOID_ELEMENTS:
            self.malformed = True
        self._open(tag, attrs, True)

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        if tag == "style":
            self._in_style = False
        # Strikte Wohlgeformtheit: das schließende Tag muss das oberste offene
        # Element schließen. Kanonische Seiten sind explizit wohl-verschachtelt;
        # tolerantes Reparieren würde Runtime-Abweichungen (z. B. leeres <h1>
        # nach </h2>) verdecken. Alles andere (unmatched/misnested) ist ein Fund.
        if not self._stack or self._stack[-1]["tag"] != tag:
            self.malformed = True
        # danach dennoch bis zum passenden offenen Element zurückrollen, damit der
        # Stack für die Eltern-/Direktkind-Prüfungen konsistent bleibt
        for i in range(len(self._stack) - 1, -1, -1):
            if self._stack[i]["tag"] == tag:
                del self._stack[i:]
                break

    def handle_data(self, data):
        if self._in_title:
            self.title_parts.append(data)
        if self._in_style:
            self.styles.append(data)
        if self._stack:
            self._stack[-1]["text"].append(data)


def _srcset_urls(value):
    urls = []
    for part in value.split(","):
        part = part.strip()
        if part:
            urls.append(part.split()[0])
    return urls


def _browser_normalize(value):
    """Bildet die URL-Vorverarbeitung von Browsern für die Klassifikation nach:
    Tab/Zeilenumbruch/CR werden überall entfernt, führende/abschließende
    C0-Steuerzeichen und Leerzeichen abgeschnitten und Backslashes wie
    Vorwärts-Schrägstriche behandelt. So kann keine extern ladende URL über
    Backslash-, C0- oder eingebettete-Whitespace-Varianten als lokal durchfallen."""
    v = value.translate(_URL_REMOVE_MAP)
    v = v.strip(_URL_STRIP_CHARS)
    return v.replace("\\", "/")


def _classify_url(value):
    """Klassifiziert eine URL browsernah und liefert (Kategorie, Scheme, normiert).
    Kategorie ist eine von ``active`` (javascript/vbscript), ``data``, ``external``
    (jedes Scheme oder protokoll-relativ/Netzwerk-Pfad ``//``), ``local``
    (schemefreies relatives Ziel) oder ``invalid`` (Parser lehnt die URL ab, z. B.
    NFKC-invalide netloc). Zentral, damit gewöhnliche Assets, srcset/imagesrcset
    und CSS-``url()`` dieselbe Einstufung nutzen. Wirft nie und spiegelt den Wert
    nie in eine Meldung – ``invalid`` ist eine stabile, wertfreie Kategorie."""
    norm = _browser_normalize(value)
    try:
        scheme = urlparse(norm).scheme.lower()
    except ValueError:
        # urlparse lehnt manche netlocs ab (NFKC-invalide Zeichen, kaputte
        # Bracket-Hosts). Fail-closed als eigene Kategorie, ohne Wert/Exception-Text.
        return "invalid", "", norm
    if scheme in ACTIVE_SCHEMES:
        return "active", scheme, norm
    if scheme == "data" or norm.lower().startswith("data:"):
        return "data", scheme, norm
    if scheme or norm.startswith("//"):
        return "external", scheme, norm
    return "local", scheme, norm


def _descendant_tags(node):
    """Alle Tag-Namen im Teilbaum unter ``node`` (ohne den Knoten selbst)."""
    tags = set()
    for child in node["children"]:
        tags.add(child["tag"])
        tags |= _descendant_tags(child)
    return tags


def _has_visible_text(node):
    """True, sobald irgendein Textknoten im Teilbaum nichtleeren Sichttext hat.
    Spiegelt die Leerheitsprüfung von ``html_text`` in der Runtime."""
    if any(part.strip() for part in node["text"]):
        return True
    return any(_has_visible_text(child) for child in node["children"])


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
    # Werte (Pfad/Query) nie in die Meldung spiegeln – sie können Tokens/Secrets
    # tragen; die Datei (rel) genügt zur Lokalisierung.
    if not _within(target, kdir):
        errors.append(f"{rel}: Pfadflucht, Ziel außerhalb des Korpus-Roots")
    elif not target.exists():
        errors.append(f"{rel}: toter relativer Link")


def validate_page(page_path, root, kdir, rel):
    errors = []
    try:
        source = page_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        return [f"{rel}: nicht als UTF-8 lesbar ({exc})"]

    parser = PageParser()
    parser.feed(source)
    parser.close()

    # Fehlerhafte Verschachtelung generisch ablehnen: entweder ein schließendes Tag
    # schloss nicht das oberste offene Element (unmatched/misnested) oder am Ende
    # blieben Elemente offen (unclosed). Kanonische Seiten sind wohl-verschachtelt.
    if parser.malformed or parser._stack:
        errors.append(f"{rel}: fehlerhafte HTML-Verschachtelung nicht erlaubt")

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
    # Hülle korrekt verschachtelt: head/body müssen direkt unter <html> liegen
    if any(p != "html" for p in parser.head_parents):
        errors.append(f"{rel}: <head> muss direktes Kind von <html> sein")
    if any(p != "html" for p in parser.body_parents):
        errors.append(f"{rel}: <body> muss direktes Kind von <html> sein")

    if parser.charset_count == 0:
        errors.append(f'{rel}: <meta charset="utf-8"> erwartet')
    elif parser.charset_count > 1:
        errors.append(f"{rel}: genau ein <meta charset> erwartet (gefunden {parser.charset_count})")
    elif parser.charset.strip().lower() != "utf-8":
        errors.append(f'{rel}: <meta charset="utf-8"> erwartet')

    title_count = parser.tag_counts.get("title", 0)
    title = "".join(parser.title_parts).strip()
    if title_count == 0:
        errors.append(f"{rel}: fehlender <title>")
    elif title_count > 1:
        errors.append(f"{rel}: genau ein <title> erwartet (gefunden {title_count})")
    elif not title:
        errors.append(f"{rel}: leerer <title>")

    for name in REQUIRED_META:
        count = parser.meta_counts.get(name, 0)
        content = parser.metas.get(name, "").strip()
        if count == 0 or not content:
            errors.append(f"{rel}: fehlendes Metadatum '{name}'")
        elif count > 1:
            errors.append(f"{rel}: Metadatum '{name}' mehrfach vorhanden ({count})")
    # tags müssen mindestens einen echten (nichtleeren) Eintrag enthalten
    tags_raw = parser.metas.get("tags", "")
    if parser.meta_counts.get("tags", 0) >= 1 and tags_raw.strip():
        if not [t for t in tags_raw.split(",") if t.strip()]:
            errors.append(f"{rel}: Metadatum 'tags' enthält keine gültigen Einträge")

    main_count = parser.tag_counts.get("main", 0)
    if main_count != 1:
        errors.append(f"{rel}: genau ein <main> erwartet (gefunden {main_count})")
    h1_count = parser.tag_counts.get("h1", 0)
    if h1_count != 1:
        errors.append(f"{rel}: genau ein <h1> erwartet (gefunden {h1_count})")
    if any(p != "main" for p in parser.h1_parents):
        errors.append(f"{rel}: <h1> muss direktes Kind von <main> sein")
    # Runtime verlangt nach Sichttext-Normalisierung ein nichtleeres <h1>
    if h1_count == 1 and parser.h1_nodes and not _has_visible_text(parser.h1_nodes[0]):
        errors.append(f"{rel}: <h1> ohne sichtbaren Text")
    # <h1> darf nur Inline-Phrasing enthalten (a/span/code/em/strong/br). HTML5/
    # Rust reparieren Block-/Heading-Nachfahren aus dem h1 heraus – der Text
    # landet dann außerhalb und die Runtime verwirft die dann leere Überschrift.
    if h1_count == 1 and parser.h1_nodes:
        bad = sorted(_descendant_tags(parser.h1_nodes[0]) - H1_PHRASING)
        if bad:
            errors.append(
                f"{rel}: <h1> darf nur Inline-Inhalt enthalten "
                f"(unerlaubte Nachfahren: {', '.join(bad)})"
            )

    # direkte <section>-Kinder von <main> brauchen eine id und eine <h2>-Überschrift
    # und dürfen nicht leer sein (die Runtime verwirft Sektionen ohne Sichttext)
    for node in parser.main_sections:
        if not node["id"].strip():
            errors.append(f"{rel}: <section> in <main> braucht eine id")
        if "h2" not in node["child_tags"]:
            errors.append(f"{rel}: <section> in <main> braucht eine direkte <h2>-Überschrift")
        if not _has_visible_text(node):
            errors.append(f"{rel}: <section> in <main> ohne sichtbaren Inhalt")

    seen = set()
    dups = []
    for value in parser.ids:
        if value in seen and value not in dups:
            dups.append(value)
        seen.add(value)
    if dups:
        errors.append(f"{rel}: doppelte id(s): {', '.join(sorted(dups))}")

    reported_dup_attrs = set()
    for dtag, dattr in parser.dup_attrs:
        if (dtag, dattr) not in reported_dup_attrs:
            reported_dup_attrs.add((dtag, dattr))
            errors.append(f"{rel}: doppeltes Attribut '{dattr}' an <{dtag}>")

    if parser.scripts:
        errors.append(f"{rel}: <script> ist nicht erlaubt")
    if parser.event_handlers:
        errors.append(f"{rel}: Inline-Event-Handler (JavaScript) nicht erlaubt")
    if parser.embeds:
        errors.append(f"{rel}: eingebettete externe Inhalte (iframe/object/embed) nicht erlaubt")
    if parser.meta_refresh:
        errors.append(f"{rel}: meta-refresh (aktive Weiterleitung) nicht erlaubt")

    for tag, attr, value in parser.assets:
        if not value.strip():
            continue
        # ping ist reine Beacon-Telemetrie (Whitespace-Liste von Zielen); aktive
        # Analytics sind unnötig. Jedes nichtleere ping-Attribut wird rundheraus
        # abgelehnt – ohne Klassifikation, damit kein Ziel als lokal durchfällt.
        if attr == "ping":
            errors.append(f"{rel}: ping-Attribut (Telemetrie) nicht erlaubt ({tag})")
            continue
        category, scheme, norm = _classify_url(value)
        # Wertfreie stabile Kategorie: nie den (evtl. sensiblen) URL-/netloc-Wert
        # spiegeln, nur Fundort (tag/attr) melden.
        if category == "invalid":
            errors.append(f"{rel}: ungültige URL ({tag} {attr})")
            continue
        if category == "active":
            errors.append(f"{rel}: aktives Schema nicht erlaubt ({tag} {attr})")
            continue
        if category == "data":
            errors.append(f"{rel}: data:-URI nicht erlaubt ({tag} {attr})")
            continue
        if tag in NAV_TAGS and attr == "href":
            # Sichere externe Navigation ausschließlich über die vier erlaubten
            # Schemes. Protokoll-relativ/Netzwerk-Pfad (``//``) navigiert der
            # Browser extern und wird abgelehnt, ebenso jedes andere Scheme
            # (ftp/file/…) – auch wenn zufällig ein lokaler Pfad gleich heißt.
            # Der Scheme-Wert wird nicht gespiegelt (Leak-Schutz).
            if scheme in NAV_EXTERNAL_SCHEMES:
                continue
            if scheme:
                errors.append(f"{rel}: unerlaubtes Schema in Navigation ({tag} {attr})")
                continue
            if category == "external":
                errors.append(f"{rel}: protokoll-relative Navigation nicht erlaubt ({tag} {attr})")
                continue
            _check_local_target(page_path, kdir, norm, rel, errors)
            continue
        # Ladende Ressource: jedes Scheme (auch protokoll-relativ) ist extern und
        # verboten; nur schemefreie lokale Ziele werden gegen das Dateisystem geprüft.
        if category == "external":
            errors.append(f"{rel}: externes Asset nicht erlaubt ({tag} {attr})")
            continue
        _check_local_target(page_path, kdir, norm, rel, errors)

    # CSS aus Style-Blöcken und Inline-style-Attributen prüfen
    for css in parser.styles:
        # Kanonischer Vertrag: kein Backslash in CSS. CSS-Escapes (u\72l(...),
        # url(http\00003a//...)) verstecken sonst Funktionsnamen/Doppelpunkte vor
        # der Regex-Klassifikation und würden extern ladende Ziele durchlassen.
        if "\\" in css:
            errors.append(f"{rel}: Backslash-Escape in CSS/Style nicht erlaubt")
            continue
        if "@import" in css.lower():
            errors.append(f"{rel}: CSS @import nicht erlaubt")
        for match in _CSS_URL.finditer(css):
            if not match.group(2).strip():
                continue
            category, _css_scheme, norm = _classify_url(match.group(2))
            if category == "invalid":
                errors.append(f"{rel}: ungültige URL in CSS nicht erlaubt")
            elif category in ("active", "data"):
                errors.append(f"{rel}: aktive/data-URL in CSS nicht erlaubt")
            elif category == "external":
                errors.append(f"{rel}: externes Asset in CSS nicht erlaubt")
            else:
                # lokale CSS-URL derselben Root-/Existenzprüfung unterwerfen
                _check_local_target(page_path, kdir, norm, rel, errors)

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
            raw_suffix = path.suffix
            low_suffix = raw_suffix.lower()
            if low_suffix == ".md":
                errors.append(f"{rel}: Markdown-Wissensseite (nur HTML erlaubt)")
            elif raw_suffix in HTML_SUFFIXES:
                errors.extend(validate_page(path, root, kdir, rel))
            elif low_suffix == ".html":
                # Runtime-Collector nimmt nur exakt .html; .HTML würde stumm
                # nicht indexiert – als Vertragsverstoß ablehnen
                errors.append(
                    f"{rel}: Wissensseiten-Endung muss exakt .html (kleingeschrieben) "
                    "sein – wird sonst nicht indexiert"
                )
            elif low_suffix == ".htm":
                errors.append(f"{rel}: .htm nicht erlaubt – Wissensseiten nur als .html")
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
