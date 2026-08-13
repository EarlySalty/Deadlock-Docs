#!/usr/bin/env bash
# Woechentlicher Frische-Lauf: prueft, was die Quell-Repos seit der letzten
# Pruefung ueberholt haben, und committet den Bericht nur bei echter Aenderung.
#
# Bewusst ohne LLM: der Lauf ist reines git und kostet kein Budget. Die
# inhaltliche Nacharbeit der gemeldeten Seiten bleibt ein eigener Schritt.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
BERICHT="berichte/frische.md"

cd "$REPO_ROOT"

# Der Dienst teilt sich den Arbeitsbaum mit Menschen. Laeuft er, waehrend ein
# Feature-Branch ausgecheckt ist, landet der Bericht per `push` still dort statt
# auf main. Lieber laut abbrechen als am falschen Ort committen.
ZWEIG="$(git rev-parse --abbrev-ref HEAD)"
if [ "$ZWEIG" != "main" ]; then
  echo "Arbeitsbaum steht auf '$ZWEIG', nicht auf main – Lauf abgebrochen." >&2
  exit 1
fi

# Der Bericht beschreibt den committeten Stand der Quell-Repos. Ein schmutziger
# Arbeitsbaum wuerde ihn mit halbfertigen Aenderungen vermischen.
if [ -n "$(git status --porcelain -- "$BERICHT")" ]; then
  echo "Bericht ist lokal veraendert – Lauf abgebrochen, bitte erst aufraeumen." >&2
  exit 1
fi

python3 "$SCRIPT_DIR/check_freshness.py" --schreiben

if git diff --quiet -- "$BERICHT"; then
  echo "Keine Aenderung an $BERICHT – nichts zu committen."
  exit 0
fi

VERALTET="$(python3 "$SCRIPT_DIR/check_freshness.py" --json | python3 -c '
import json, sys
seiten = json.load(sys.stdin)["seiten"]
print(sum(1 for s in seiten if s["status"] == "veraltet"))
')"

git add -- "$BERICHT"
git commit -q -m "docs(frische): woechentlicher Quellabgleich, ${VERALTET} Seiten ungeprueft"
git push -q origin main
echo "Bericht aktualisiert und gepusht (${VERALTET} veraltete Seiten)."
