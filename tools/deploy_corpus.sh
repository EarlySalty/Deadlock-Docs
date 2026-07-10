#!/usr/bin/env bash
# Deployt den committeten public/-Korpus als versionierten Snapshot und
# schaltet den current-Symlink atomar um.
#
#   deploy_corpus.sh <git-ref>
#
# Es wird ausschließlich der committete public/-Baum des angeforderten Refs
# exportiert (git archive, nicht die Arbeitskopie). internal/ wird nie kopiert.
# SHA-Snapshots sind nach der ersten Veröffentlichung unveränderlich; ältere
# Snapshots bleiben erhalten. Deploys sind race-sicher (eindeutige Temp-Namen)
# und lassen bei Fehlern das laufende current unangetastet.
set -euo pipefail

REF="${1:?usage: deploy_corpus.sh <git-ref>}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE="${DL_KNOWLEDGE_HOME:-$HOME/.local/share/dl-knowledge}"

STAGING=""
TMPLINK=""
cleanup() {
  if [ -n "$STAGING" ]; then rm -rf "$STAGING"; fi
  if [ -n "$TMPLINK" ]; then rm -f "$TMPLINK"; fi
}
trap cleanup EXIT

# Vollen SHA auflösen (schlägt bei unbekanntem Ref fehl).
SHA="$(git rev-parse --verify "${REF}^{commit}")"
DEST="$BASE/$SHA"

mkdir -p "$BASE"

# Snapshot nur bauen, wenn er noch nicht existiert (unveränderlich).
if [ ! -d "$DEST" ]; then
  STAGING="$(mktemp -d "$BASE/.staging.XXXXXX")"

  # Nur den committeten public/-Baum exportieren; scheitert, wenn public/ fehlt.
  git archive "$SHA" public | tar -x -C "$STAGING"

  # Ohne öffentliche HTML-Seite gibt es nichts zu deployen.
  html_count="$(find "$STAGING/public" -type f -name '*.html' 2>/dev/null | wc -l)"
  if [ "$html_count" -eq 0 ]; then
    echo "deploy: kein öffentliches HTML in $SHA" >&2
    exit 1
  fi

  # Snapshot gegen den Korpusvertrag prüfen, bevor er live geht.
  python3 "$SCRIPT_DIR/validate_corpus.py" "$STAGING"

  # Atomar veröffentlichen; bei parallelem Sieger dessen Snapshot behalten.
  mv -T "$STAGING" "$DEST" 2>/dev/null || [ -d "$DEST" ]
fi

# current-Symlink atomar auf den SHA schalten. Eindeutiger Temp-Name pro Lauf
# verhindert Kollisionen paralleler Deploys; mv -T ersetzt current atomar und
# löscht dabei nie das Live-Ziel.
TMPLINK="$(mktemp -u "$BASE/.current.XXXXXX")"
ln -s "$SHA" "$TMPLINK"
mv -T "$TMPLINK" "$BASE/current"
TMPLINK=""

echo "deploy: current -> $SHA"
