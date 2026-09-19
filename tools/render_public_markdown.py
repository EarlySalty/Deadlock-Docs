#!/usr/bin/env python3
"""Redaktionshilfe für neue HTML-Entwürfe, ausdrücklich kein Refresh-Schritt.

Benötigt markdown-it-py. Bestehende Dateien werden nie überschrieben.
Eine Ausgabe ist ein Entwurf, keine fachliche Freigabe.
"""
from __future__ import annotations

import argparse
import html
import re
from pathlib import Path

from markdown_it import MarkdownIt

from import_public_sources import frontmatter

STYLE = """body { font-family: system-ui, sans-serif; line-height: 1.6;
max-width: 46rem; margin: 2rem auto; padding: 0 1rem; color: #1b1b1b; }
h1, h2, h3 { line-height: 1.25; }
code { background: #f2f2f2; padding: .1rem .3rem; border-radius: .2rem;
overflow-wrap: anywhere; }
pre { overflow-x: auto; padding: 1rem; background: #f2f2f2; }
table { border-collapse: collapse; width: 100%; }
th, td { border: 1px solid #ccc; padding: .4rem .6rem; text-align: left;
vertical-align: top; overflow-wrap: anywhere; }
nav a { margin-right: .8rem; }
a:focus-visible { outline: 3px solid #805400; outline-offset: 3px; }
"""


def render_markdown(raw: str, *, title: str | None = None) -> str:
    meta, body = frontmatter(raw)
    parser = MarkdownIt("commonmark", {"html": False}).enable("table")
    tokens = parser.parse(body)
    title = title or meta.get("title")
    if not title:
        raise ValueError("Expliziter Seitentitel erforderlich")
    # Die flachste Überschrift unterhalb des Seitentitels bildet Abschnitte;
    # tiefere Überschriften bleiben darin, ebenso Listen, Tabellen und Code.
    levels = [int(t.tag[1:]) for t in tokens if t.type == "heading_open" and t.tag != "h1"]
    level = min(levels, default=2)
    result = []
    active = False
    identifiers: set[str] = set()
    index = 0
    while index < len(tokens):
        token = tokens[index]
        if token.type == "heading_open" and token.tag == "h1":
            index += 3
            continue
        if token.type == "heading_open" and int(token.tag[1:]) == level:
            if active:
                result.append("</section>\n")
            heading = tokens[index + 1]
            slug = re.sub(r"[^\w-]+", "-", heading.content.lower()).strip("-") or "abschnitt"
            candidate, counter = slug, 2
            while candidate in identifiers:
                candidate = f"{slug}-{counter}"
                counter += 1
            identifiers.add(candidate)
            result.append(f'<section id="{html.escape(candidate)}">\n')
            tokens[index].tag = "h2"
            tokens[index + 2].tag = "h2"
            active = True
            result.append(parser.renderer.render(tokens[index:index + 3], parser.options, {}))
            index += 3
            continue
        elif token.type in {"heading_open", "heading_close"}:
            token.tag = f"h{min(6, int(token.tag[1:]) - level + 2)}"
        result.append(parser.renderer.render([token], parser.options, {}))
        index += 1
    if active:
        result.append("</section>\n")
    escaped = html.escape(title)
    return (f'<!doctype html>\n<html lang="de"><head><meta charset="utf-8">\n'
            f'<title>{escaped}</title><meta name="tags" content="hilfe, nutzerwissen">\n'
            '<meta name="stand" content="Redaktionsentwurf – fachlich ungeprüft">\n'
            '<meta name="quelle" content="Redaktionelle Nutzerhilfe">\n'
            f'<style>{STYLE}</style></head><body><main><h1>{escaped}</h1>\n'
            + "".join(result) + "</main></body></html>\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--title")
    args = parser.parse_args()
    rendered = render_markdown(args.source.read_text(encoding="utf-8"), title=args.title)
    with args.output.open("x", encoding="utf-8") as output:
        output.write(rendered)


if __name__ == "__main__":
    main()
