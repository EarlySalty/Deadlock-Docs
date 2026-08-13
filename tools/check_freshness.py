#!/usr/bin/env python3
"""Meldet, welche internen Wissensseiten von ihren Quellen ueberholt wurden.

Jede Seite unter `internal/` ist in `quellen.json` an einen oder mehrere
Quell-Repos gebunden, zusammen mit dem Commit, gegen den sie zuletzt geprueft
wurde. Dieses Werkzeug fragt fuer jede Bindung, was sich seither in den
gebundenen Pfaden geaendert hat.

    check_freshness.py                 # Bericht nach stdout
    check_freshness.py --json          # maschinenlesbar
    check_freshness.py --schreiben     # Bericht nach berichte/frische.md
    check_freshness.py --strict        # Exit 1, sobald eine Seite veraltet ist

Die Quell-Repos werden unter `$DL_REPO_HOME` gesucht (Vorgabe: das
Elternverzeichnis dieses Repos). Es wird nur gelesen; kein Repo wird
veraendert und kein Netzzugriff ausgeloest.
"""
import argparse
import json
import subprocess
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST = REPO_ROOT / "quellen.json"

AKTUELL = "aktuell"
VERALTET = "veraltet"
UNBEKANNT = "unbekannt"
NICHT_VERFOLGT = "nicht-verfolgt"
UNGEBUNDEN = "ohne-eintrag"

# Reihenfolge fuer die Berichts-Gruppierung: Dringendes zuerst.
RANG = {UNGEBUNDEN: 0, VERALTET: 1, UNBEKANNT: 2, AKTUELL: 3, NICHT_VERFOLGT: 4}

GENAU = "genau"
GROB = "grob"


class GitFehler(RuntimeError):
    pass


def git(repo_dir, *args):
    proc = subprocess.run(
        ["git", "-C", str(repo_dir), *args],
        capture_output=True, text=True,
    )
    if proc.returncode != 0:
        raise GitFehler(proc.stderr.strip() or f"git {' '.join(args)} fehlgeschlagen")
    return proc.stdout.strip()


def lade_manifest(pfad=MANIFEST):
    with open(pfad, encoding="utf-8") as fh:
        return json.load(fh)


def repo_basis(manifest, override=None):
    if override:
        return Path(override).expanduser().resolve()
    import os
    env = manifest.get("repo_basis_env", "DL_REPO_HOME")
    wert = os.environ.get(env)
    if wert:
        return Path(wert).expanduser().resolve()
    return REPO_ROOT.parent


def praezision(pfade):
    """Wie eng eine Bindung gefasst ist.

    Eine Bindung auf `rust/crates/dl-community/src/concierge.rs` sagt etwas
    ueber genau diese Seite aus. Eine Bindung auf `rust` oder `.` faengt jeden
    Commit des Repos ein; ihre Commit-Zahl ist nur eine Obergrenze. Der
    Unterschied entscheidet, wie ernst eine Meldung zu nehmen ist, deshalb
    wird er im Bericht ausgewiesen statt versteckt.
    """
    return GENAU if all("/" in p for p in pfade) else GROB


def pathspec(pfade, ausschluss):
    """Git-Pathspec aus gebundenen Pfaden plus globalen Ausschluessen."""
    spec = [p for p in pfade if p != "."]
    for muster in ausschluss:
        # Ein Ausschluss muss sowohl den Eintrag selbst (WORKFLOW.md) als auch
        # alles darunter (logs/lauf.txt) treffen, auf jeder Verschachtelungstiefe.
        spec.extend((
            f":(exclude,glob){muster}",
            f":(exclude,glob){muster}/**",
            f":(exclude,glob)**/{muster}",
            f":(exclude,glob)**/{muster}/**",
        ))
    return spec


def pruefe_bindung(bindung, manifest, basis):
    """Ein (repo, pfade, geprueft)-Tripel gegen den aktuellen Branch-Stand."""
    name = bindung["repo"]
    repo_info = manifest["repos"].get(name)
    ergebnis = {
        "repo": name,
        "pfade": bindung["pfade"],
        "geprueft": bindung["geprueft"],
        "herkunft": bindung.get("herkunft"),
        "praezision": praezision(bindung["pfade"]),
        "commits": 0,
        "dateien": [],
        "status": UNBEKANNT,
        "hinweis": None,
    }
    if repo_info is None:
        ergebnis["hinweis"] = f"Repo {name} fehlt im Manifest"
        return ergebnis

    repo_dir = basis / repo_info["verzeichnis"]
    if not (repo_dir / ".git").exists():
        ergebnis["hinweis"] = f"Repo nicht gefunden: {repo_dir}"
        return ergebnis

    branch = repo_info.get("branch", "HEAD")
    try:
        basis_sha = git(repo_dir, "rev-parse", "--verify", f"{bindung['geprueft']}^{{commit}}")
        kopf = git(repo_dir, "rev-parse", "--verify", f"{branch}^{{commit}}")
    except GitFehler as e:
        ergebnis["hinweis"] = str(e)
        return ergebnis

    # Ein geprueft-Commit von einem Feature-Branch liegt nicht zwingend auf dem
    # Hauptbranch. Dann ist der gemeinsame Vorfahr der ehrlichste Vergleichspunkt.
    ahne = subprocess.run(
        ["git", "-C", str(repo_dir), "merge-base", "--is-ancestor", basis_sha, kopf],
        capture_output=True, text=True,
    ).returncode == 0
    if not ahne:
        try:
            basis_sha = git(repo_dir, "merge-base", basis_sha, kopf)
            ergebnis["hinweis"] = (
                f"geprueft liegt nicht auf {branch}; verglichen ab gemeinsamem "
                f"Vorfahr {basis_sha[:8]} (meldet eher zu viel als zu wenig)"
            )
        except GitFehler as e:
            ergebnis["hinweis"] = str(e)
            return ergebnis

    spec = pathspec(bindung["pfade"], manifest.get("ausschluss", []))
    spanne = f"{basis_sha}..{kopf}"
    try:
        roh = git(repo_dir, "log", "--format=%H", spanne, "--", *spec)
        dateien = git(repo_dir, "diff", "--name-only", spanne, "--", *spec)
    except GitFehler as e:
        ergebnis["hinweis"] = str(e)
        return ergebnis

    ergebnis["commits"] = len([z for z in roh.split("\n") if z])
    ergebnis["dateien"] = [z for z in dateien.split("\n") if z]
    ergebnis["status"] = VERALTET if ergebnis["commits"] else AKTUELL
    return ergebnis


def ohne_eintrag(manifest, docs_root):
    """Interne Seiten, die es auf der Platte, aber nicht im Manifest gibt.

    Ohne diese Pruefung entzieht sich jede neu angelegte Seite still der
    Frische-Verfolgung - also genau der Verfall, den das Manifest verhindern
    soll.
    """
    verzeichnis = Path(docs_root) / "internal"
    if not verzeichnis.is_dir():
        return []
    vorhanden = {
        p.relative_to(docs_root).as_posix()
        for p in verzeichnis.rglob("*.html")
    }
    return sorted(vorhanden - set(manifest["seiten"]))


def pruefe(manifest, basis, docs_root=REPO_ROOT):
    seiten = [
        {
            "seite": rel, "stand": None, "grund": None,
            "status": UNGEBUNDEN, "praezision": GROB, "commits": 0, "bindungen": [],
        }
        for rel in ohne_eintrag(manifest, docs_root)
    ]
    for rel, eintrag in sorted(manifest["seiten"].items()):
        bindungen = [pruefe_bindung(b, manifest, basis) for b in eintrag["bindungen"]]
        if not bindungen:
            status = NICHT_VERFOLGT
        elif any(b["status"] == VERALTET for b in bindungen):
            status = VERALTET
        elif any(b["status"] == UNBEKANNT for b in bindungen):
            status = UNBEKANNT
        else:
            status = AKTUELL
        # Fuer die Dringlichkeit zaehlt, wie genau die *meldende* Bindung ist:
        # 8 Commits auf concierge.rs sind ein Befund, 482 auf `rust` ein Verdacht.
        melder = [b for b in bindungen if b["status"] == VERALTET] or bindungen
        seiten.append({
            "seite": rel,
            "stand": eintrag.get("stand"),
            "grund": eintrag.get("grund"),
            "status": status,
            "praezision": GENAU if any(b["praezision"] == GENAU for b in melder) else GROB,
            "commits": sum(b["commits"] for b in bindungen),
            "bindungen": bindungen,
        })
    return seiten


def bericht(seiten, heute=None):
    heute = heute or date.today().isoformat()
    zaehler = {s: 0 for s in RANG}
    for e in seiten:
        zaehler[e["status"]] += 1
    veraltet_genau = sum(1 for e in seiten if e["status"] == VERALTET and e["praezision"] == GENAU)
    grob = sum(1 for e in seiten if e["praezision"] == GROB and e["bindungen"])

    zeilen = [
        "# Frische der internen Wissensseiten",
        "",
        f"Erzeugt: {heute} von `tools/check_freshness.py` aus `quellen.json`.",
        "",
        f"- ohne Eintrag in `quellen.json`: **{zaehler[UNGEBUNDEN]}**",
        f"- veraltet: **{zaehler[VERALTET]}**, davon {veraltet_genau} mit genauer Bindung",
        f"- aktuell: {zaehler[AKTUELL]}",
        f"- unbekannt: {zaehler[UNBEKANNT]}",
        f"- nicht verfolgt: {zaehler[NICHT_VERFOLGT]}",
        "",
        "`veraltet` heisst: seit dem geprueften Commit wurde in den gebundenen",
        "Quellpfaden weitergearbeitet. Es heisst nicht, dass die Seite falsch ist,",
        "sondern dass sie ungeprueft ist.",
        "",
        f"{grob} Seiten haengen noch an groben Pfaden (ganze Repo-Verzeichnisse).",
        "Ihre Commit-Zahlen sind Obergrenzen, kein Befund. Wer eine solche Seite",
        "ueberarbeitet, traegt in `quellen.json` gleich die genauen Pfade nach;",
        "danach meldet der Bericht fuer sie nur noch echte Treffer.",
        "",
    ]

    geordnet = sorted(seiten, key=lambda e: (
        RANG[e["status"]],
        0 if e["praezision"] == GENAU else 1,
        -e["commits"],
        e["seite"],
    ))
    for status in (UNGEBUNDEN, VERALTET, UNBEKANNT, AKTUELL, NICHT_VERFOLGT):
        gruppe = [e for e in geordnet if e["status"] == status]
        if not gruppe:
            continue
        zeilen.append(f"## {status} ({len(gruppe)})")
        zeilen.append("")
        for e in gruppe:
            kopf = f"### {e['seite']}"
            if e["commits"]:
                kopf += f" ({e['praezision']}, {e['commits']} Commits seit Pruefung)"
            zeilen.append(kopf)
            zeilen.append("")
            zeilen.append(f"Stand der Seite: {e['stand'] or 'unbekannt'}")
            if e["grund"]:
                zeilen.append(f"Grund: {e['grund']}")
            for b in e["bindungen"]:
                pfade = ", ".join(b["pfade"])
                zeilen.append(
                    f"- `{b['repo']}` ({pfade}) ab `{b['geprueft'][:8]}`"
                    f" [{b['herkunft']}, {b['praezision']}]: {b['commits']} Commits,"
                    f" {len(b['dateien'])} Dateien"
                )
                if b["hinweis"]:
                    zeilen.append(f"  - Hinweis: {b['hinweis']}")
                for d in b["dateien"][:8]:
                    zeilen.append(f"  - `{d}`")
                if len(b["dateien"]) > 8:
                    zeilen.append(f"  - … {len(b['dateien']) - 8} weitere")
            zeilen.append("")
    return "\n".join(zeilen).rstrip() + "\n"


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--manifest", default=str(MANIFEST))
    p.add_argument("--repo-basis", default=None, help="Elternverzeichnis der Quell-Repos")
    p.add_argument("--docs-root", default=str(REPO_ROOT), help="Wurzel dieses Doku-Repos")
    p.add_argument("--json", action="store_true", help="Rohdaten statt Bericht")
    p.add_argument("--schreiben", action="store_true", help="Bericht nach berichte/frische.md")
    p.add_argument("--strict", action="store_true", help="Exit 1, wenn Seiten veraltet sind")
    args = p.parse_args(argv)

    manifest = lade_manifest(args.manifest)
    basis = repo_basis(manifest, args.repo_basis)
    seiten = pruefe(manifest, basis, Path(args.docs_root).resolve())

    if args.json:
        print(json.dumps({"repo_basis": str(basis), "seiten": seiten}, indent=2, ensure_ascii=False))
    else:
        text = bericht(seiten)
        if args.schreiben:
            ziel = REPO_ROOT / "berichte" / "frische.md"
            ziel.parent.mkdir(parents=True, exist_ok=True)
            ziel.write_text(text, encoding="utf-8")
            print(f"Bericht geschrieben: {ziel.relative_to(REPO_ROOT)}")
        else:
            print(text, end="")

    veraltet = sum(1 for e in seiten if e["status"] == VERALTET)
    unbekannt = sum(1 for e in seiten if e["status"] == UNBEKANNT)
    ungebunden = sum(1 for e in seiten if e["status"] == UNGEBUNDEN)
    if unbekannt:
        print(f"{unbekannt} Seite(n) nicht pruefbar", file=sys.stderr)
    # Eine Seite ohne Manifest-Eintrag ist immer ein Fehler, kein Zustand: sie
    # entzieht sich der Verfolgung. Deshalb schlaegt sie auch ohne --strict fehl.
    if ungebunden:
        print(f"{ungebunden} Seite(n) ohne Eintrag in quellen.json", file=sys.stderr)
        return 1
    if args.strict and veraltet:
        print(f"{veraltet} Seite(n) veraltet", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
