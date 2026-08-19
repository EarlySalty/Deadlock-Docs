#!/usr/bin/env python3
"""Generiert die oeffentliche FAQ-/Themen-Seite (site/index.html) aus dem
kompletten public/-Korpus. Kuratierte Top-Fragen bleiben handgepflegt (mit
FAQPage-JSON-LD), der Rest wird vollstaendig aus den Korpus-Seiten erzeugt,
damit nichts fehlt und die Seite synchron zum Korpus bleibt.

Aufruf:  python3 tools/build_faq.py
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"
OUT = ROOT / "site" / "index.html"

# Reihenfolge + Anzeigenamen der Bereiche (top-level Ordner in public/)
AREAS = [
    ("discord-server", "Discord &amp; Community", "Beitritt, Rollen, Voice-Lanes, Mitspielersuche, Coaching, Moderation, Datenschutz."),
    ("steam-bot", "Steam-Bot", "Steam verknuepfen, Rang pruefen, Playtest-Einladung, Build-Katalog."),
    ("twitch-bot", "Twitch-Bot fuer Streamer", "Kanal verbinden, Auto-Raid, Dashboard, Overlay, Plaene, Werbefrei, Datenschutz."),
    ("turniere", "Turniere", "Anmeldung, Team, Check-in, Bracket und Rangliste ueber das Turnierportal."),
    ("patchnotes-bot", "Patchnotes", "Offizielle Deadlock-Patchnotes auf Deutsch, plus durchsuchbares Archiv."),
    ("website", "Website-Portale", "Coaching, Scrims, Builds, Patch-Archiv, Aktivitaet und Turniere im Web."),
    ("dokus", "Anleitungen", "Schritt-fuer-Schritt-Abläufe fuer Mitglieder und Orga."),
    ("deadlock-helden", "Helden-Guides", "Spielweise, Build, Staerken und Schwaechen aller Helden."),
]

STRIP_TAGS = re.compile(r"<[^>]+>")


def normalize_dashes(s: str) -> str:
    # Nutzersichtbarer Text kommt ohne Em-Dashes raus (Projektregel). Korpus-
    # Titel/Leads enthalten teils "—"/"–"; hier sauber ersetzen.
    s = s.replace(" — ", ", ").replace(" – ", ", ")
    s = s.replace("—", ", ").replace("–", "-")
    return re.sub(r"\s+,", ",", s)


def text_of(fragment: str) -> str:
    return normalize_dashes(html.unescape(STRIP_TAGS.sub("", fragment)).strip())


def extract(path: Path):
    raw = path.read_text(encoding="utf-8")
    m = re.search(r"<title>(.*?)</title>", raw, re.S)
    title = text_of(m.group(1)) if m else path.stem
    lead = ""
    for pm in re.finditer(r"<p[^>]*>(.*?)</p>", raw, re.S):
        t = text_of(pm.group(1))
        t = re.sub(r"\s+", " ", t)
        if len(t) >= 40:
            lead = t[:240]
            break
    # Unterthemen: h2 und summary (keine h1)
    subs = []
    for hm in re.finditer(r"<(h2|h3|summary)[^>]*>(.*?)</\1>", raw, re.S):
        s = re.sub(r"\s+", " ", text_of(hm.group(2)))
        if s and s.lower() not in (x.lower() for x in subs):
            subs.append(s)
    return title, lead, subs


def hero_title(title: str) -> str:
    # "Abrams (Spielweise, Build, ...)" -> "Abrams"
    return re.sub(r"\s*\(.*$", "", title).strip()


pages = {}
for p in sorted(PUBLIC.rglob("*.html")):
    rel = p.relative_to(PUBLIC).as_posix()
    if rel == "index.html":
        continue
    area = rel.split("/", 1)[0]
    pages.setdefault(area, []).append((rel, *extract(p)))

# ---- Alle-Themen-HTML bauen ----
sections = []
for area_key, area_name, area_desc in AREAS:
    items = pages.get(area_key, [])
    if not items:
        continue
    sections.append(f'\n<section class="topic" id="t-{area_key}">')
    sections.append(f'  <h2>{area_name}</h2>')
    sections.append(f'  <p class="section-note">{area_desc}</p>')

    if area_key == "deadlock-helden":
        # kompakte Grid-Liste, ein Link je Held
        sections.append('  <div class="hero-grid">')
        for rel, title, lead, subs in sorted(items, key=lambda x: hero_title(x[1]).lower()):
            name = html.escape(hero_title(title))
            sections.append(f'    <a href="/docs/{rel}">{name}</a>')
        sections.append('  </div>')
    else:
        for rel, title, lead, subs in items:
            t = html.escape(title)
            sections.append('  <details>')
            sections.append(f'    <summary>{t}</summary>')
            sections.append('    <div class="answer">')
            if lead:
                sections.append(f'      <p>{html.escape(lead)}</p>')
            shown = [s for s in subs if s.lower() != title.lower()][:8]
            if shown:
                sections.append('      <ul class="subs">')
                for s in shown:
                    sections.append(f'        <li>{html.escape(s)}</li>')
                sections.append('      </ul>')
            sections.append(f'      <p class="more"><a href="/docs/{rel}">Ganze Seite oeffnen</a></p>')
            sections.append('    </div>')
            sections.append('  </details>')
    sections.append('</section>')

ALL_TOPICS = "\n".join(sections)
total_pages = sum(len(v) for v in pages.values())

# ---- Template zusammensetzen ----
TEMPLATE = Path(__file__).parent / "faq_template.html"
tpl = TEMPLATE.read_text(encoding="utf-8")
out = tpl.replace("<!--ALL_TOPICS-->", ALL_TOPICS).replace("{{TOTAL_PAGES}}", str(total_pages))
OUT.write_text(out, encoding="utf-8")
print(f"OK: {OUT} geschrieben. Bereiche: {len([k for k in pages])}, Seiten gesamt: {total_pages}")
