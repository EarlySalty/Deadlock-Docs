#!/usr/bin/env python3
"""Prueft, ob die von internen Seiten genannten Quellpfade noch existieren.

Nennt eine Betriebsseite ein Skript, das es nicht mehr gibt, ist die Seite
falsch - unabhaengig davon, wie viele Commits seit der letzten Pruefung
gelaufen sind. Das ist deterministisch feststellbar, kostet nichts und
erzeugt keine Fehlalarme, deshalb laeuft diese Pruefung vor der Frische-
Pruefung und nicht nach ihr.

    check_referenzen.py                 # Bericht nach stdout
    check_referenzen.py --json          # maschinenlesbar
    check_referenzen.py --schreiben     # Bericht nach berichte/referenzen.md
    check_referenzen.py --strict        # Exit 1, sobald ein Pfad fehlt

Geprueft wird gegen das *Dateisystem*, nicht gegen `git ls-files`: mehrere
Repos ignorieren ihr `scripts/`-Verzeichnis bewusst, die Dateien existieren
aber und werden von systemd gestartet. Eine Git-Pruefung meldet genau diese
als fehlend.
"""
import argparse
import json
import os
import re
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST = REPO_ROOT / "quellen.json"

# Verzeichnisse, die kein Quellcode sind und den Baumlauf nur verlangsamen.
UEBERSPRINGEN = {
    ".git", "target", "node_modules", "dist", "build", ".venv",
    "__pycache__", "graphify-out", "logs", ".next", "vendor",
}

# Kandidaten sind Pfade, die mit einem dieser Verzeichnisse beginnen. Ein
# freies Muster wuerde jeden Schraegstrich im Fliesstext einfangen.
WURZELN = (
    "rust", "src", "bot", "features", "ops", "scripts", "backend",
    "frontend", "builds", "crates", "bin", "cogs", "migrations", "docs",
)
# Die Doku schreibt Pfade mal repo-relativ (`rust/bin/...`), mal mit
# Repo-Namen davor (`Deadlock-Bots/scripts/...`). Beide Formen gehoeren
# erkannt, das Praefix wird vor der Pruefung abgeschnitten.
REPO_PRAEFIX = r"(?:Deadlock-[A-Za-z-]+|Website|Caddy|TradingBot)/"

# Kein \b davor: das greift auch nach einem Bindestrich und macht aus
# `dl-bot/src/vanity.rs` ein vermeintlich fehlendes `bot/src/vanity.rs`.
# Auch ein Schraegstrich davor ist verboten, sonst meldet jeder lange Pfad
# zusaetzlich sein eigenes Suffix. Das Repo-Praefix steht deshalb im Muster
# und nicht im Lookbehind.
MUSTER = re.compile(
    r"(?<![\w/.-])(?:" + REPO_PRAEFIX + r")?(?:" + "|".join(WURZELN)
    + r")/[A-Za-z0-9_./-]{3,}")
OHNE_PRAEFIX = re.compile(r"^" + REPO_PRAEFIX)

# Kein Quellcode, sondern Bauergebnis, Laufzeitdatei oder Interpreterpfad.
# Diese Treffer waeren immer falsch, deshalb gar nicht erst melden.
AUSNAHMEN = re.compile(
    r"(^|/)(target|dist|build|node_modules)(/|$)"   # Bauergebnisse
    r"|\.html$"                                      # Verweise auf andere Doku-Seiten
    r"|^bin/(bash|sh|python[0-9.]*|env)$"            # Shebang-Zeilen
    r"|\.conf$"                                      # Laufzeit-Konfiguration ausserhalb der Repos
)


def quellbaum(manifest, basis):
    """Alle Dateien und Verzeichnisse der Quell-Repos, repo-relativ."""
    eintraege = set()
    for repo in manifest["repos"].values():
        wurzel = basis / repo["verzeichnis"]
        if not wurzel.is_dir():
            continue
        for pfad, verzeichnisse, dateien in os.walk(wurzel):
            verzeichnisse[:] = [d for d in verzeichnisse if d not in UEBERSPRINGEN]
            rel = os.path.relpath(pfad, wurzel)
            if rel != ".":
                eintraege.add(rel)
            for datei in dateien:
                eintraege.add(datei if rel == "." else os.path.join(rel, datei))
    return eintraege


def existiert(pfad, eintraege):
    """Auch als Suffix: die Doku kuerzt Pfade oft auf den sprechenden Teil."""
    if pfad in eintraege:
        return True
    endung = "/" + pfad
    return any(e == pfad or e.endswith(endung) for e in eintraege)


def kandidaten(text):
    """(gemeldeter Pfad, repo-relativer Pfad) je Fundstelle."""
    for roh in set(MUSTER.findall(text)):
        gemeldet = roh.rstrip(".,);:")
        relativ = OHNE_PRAEFIX.sub("", gemeldet)
        if relativ.endswith("/") or ".." in relativ or AUSNAHMEN.search(relativ):
            continue
        yield gemeldet, relativ


def pruefe(manifest, basis, docs_root=REPO_ROOT):
    eintraege = quellbaum(manifest, basis)
    fehlend = defaultdict(list)
    verzeichnis = Path(docs_root) / "internal"
    for seite in sorted(verzeichnis.rglob("*.html")) if verzeichnis.is_dir() else []:
        rel = seite.relative_to(docs_root).as_posix()
        text = re.sub(r"<[^>]+>", " ", seite.read_text(encoding="utf-8"))
        for gemeldet, relativ in sorted(kandidaten(text)):
            if not existiert(relativ, eintraege):
                fehlend[rel].append(gemeldet)
    return dict(fehlend), len(eintraege)


def bericht(fehlend, geprueft, heute=None):
    heute = heute or date.today().isoformat()
    anzahl = sum(len(v) for v in fehlend.values())
    zeilen = [
        "# Nicht auffindbare Quellpfade",
        "",
        f"Erzeugt: {heute} von `tools/check_referenzen.py`.",
        "",
        f"- fehlende Pfade: **{anzahl}** auf {len(fehlend)} Seiten",
        f"- abgeglichen gegen {geprueft} Dateien und Verzeichnisse der Quell-Repos",
        "",
        "Ein hier gelisteter Pfad steht in der Doku, existiert aber nirgends.",
        "Anders als der Frische-Bericht ist das kein Verdacht, sondern ein Fehler:",
        "wer der Seite folgt, laeuft ins Leere.",
        "",
    ]
    for seite in sorted(fehlend, key=lambda s: (-len(fehlend[s]), s)):
        zeilen.append(f"## {seite} ({len(fehlend[seite])})")
        zeilen.append("")
        zeilen += [f"- `{p}`" for p in fehlend[seite]]
        zeilen.append("")
    if not fehlend:
        zeilen.append("Keine Treffer. Alle genannten Pfade existieren.")
        zeilen.append("")
    return "\n".join(zeilen).rstrip() + "\n"


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--manifest", default=str(MANIFEST))
    p.add_argument("--repo-basis", default=None)
    p.add_argument("--docs-root", default=str(REPO_ROOT))
    p.add_argument("--json", action="store_true")
    p.add_argument("--schreiben", action="store_true")
    p.add_argument("--strict", action="store_true")
    args = p.parse_args(argv)

    with open(args.manifest, encoding="utf-8") as fh:
        manifest = json.load(fh)
    if args.repo_basis:
        basis = Path(args.repo_basis).expanduser().resolve()
    else:
        basis = Path(os.environ.get(manifest.get("repo_basis_env", "DL_REPO_HOME")
                                    or "DL_REPO_HOME", REPO_ROOT.parent)).resolve()

    fehlend, geprueft = pruefe(manifest, basis, Path(args.docs_root).resolve())
    anzahl = sum(len(v) for v in fehlend.values())

    if args.json:
        print(json.dumps({"fehlend": fehlend, "geprueft": geprueft},
                         indent=2, ensure_ascii=False))
    else:
        text = bericht(fehlend, geprueft)
        if args.schreiben:
            ziel = REPO_ROOT / "berichte" / "referenzen.md"
            ziel.parent.mkdir(parents=True, exist_ok=True)
            ziel.write_text(text, encoding="utf-8")
            print(f"Bericht geschrieben: {ziel.relative_to(REPO_ROOT)}")
        else:
            print(text, end="")

    if args.strict and anzahl:
        print(f"{anzahl} nicht auffindbare Pfad(e)", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
