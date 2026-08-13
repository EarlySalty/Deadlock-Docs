#!/usr/bin/env bash
# Taeglicher Frische-Lauf: prueft, was die Quell-Repos seit der letzten
# Pruefung ueberholt haben, und committet den Bericht nur bei echter Aenderung.
#
# Bewusst ohne LLM: der Lauf ist reines git und kostet kein Budget. Die
# inhaltliche Nacharbeit der gemeldeten Seiten bleibt ein eigener Schritt.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
BERICHTE=("berichte/frische.md" "berichte/referenzen.md")

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
if [ -n "$(git status --porcelain -- "${BERICHTE[@]}")" ]; then
  echo "Bericht ist lokal veraendert – Lauf abgebrochen, bitte erst aufraeumen." >&2
  exit 1
fi

# Erst die Referenzen: ein nicht existierender Pfad ist ein Fehler, keine
# Frage der Commit-Zahl. Der Lauf bricht daran nicht ab, damit der
# Frische-Bericht trotzdem erneuert wird.
python3 "$SCRIPT_DIR/check_referenzen.py" --schreiben || true

python3 "$SCRIPT_DIR/check_freshness.py" --schreiben

if git diff --quiet -- "${BERICHTE[@]}"; then
  echo "Keine Aenderung an den Berichten – nichts zu committen."
  exit 0
fi

VERALTET="$(python3 "$SCRIPT_DIR/check_freshness.py" --json | python3 -c '
import json, sys
seiten = json.load(sys.stdin)["seiten"]
print(sum(1 for s in seiten if s["status"] == "veraltet"))
')"

git add -- "${BERICHTE[@]}"
git commit -q -m "docs(frische): woechentlicher Quellabgleich, ${VERALTET} Seiten ungeprueft"
git push -q origin main
echo "Bericht aktualisiert und gepusht (${VERALTET} veraltete Seiten)."
