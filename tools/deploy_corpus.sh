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
# Deployt wird immer das Repository des Skripts (SCRIPT_DIR/..), unabhängig vom
# Aufruf-CWD – sonst könnte ein fremdes Repo als Deadlock-Korpus erscheinen.
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
BASE="${DL_KNOWLEDGE_HOME:-$HOME/.local/share/dl-knowledge}"

STAGING=""
LINKDIR=""
cleanup() {
  if [ -n "$STAGING" ]; then rm -rf "$STAGING"; fi
  if [ -n "$LINKDIR" ]; then rm -rf "$LINKDIR"; fi
}
trap cleanup EXIT

# Vollen SHA auflösen (schlägt bei unbekanntem Ref fehl).
SHA="$(git -C "$REPO_ROOT" rev-parse --verify "${REF}^{commit}")"
DEST="$BASE/$SHA"

mkdir -p "$BASE"

# Snapshot nur bauen, wenn er noch nicht existiert (unveränderlich).
if [ ! -d "$DEST" ]; then
  STAGING="$(mktemp -d "$BASE/.staging.XXXXXX")"

  # Nur den committeten public/-Baum exportieren; scheitert, wenn public/ fehlt.
  git -C "$REPO_ROOT" archive "$SHA" public | tar -x -C "$STAGING"

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

# current-Symlink atomar auf den SHA schalten. Der Link entsteht in einem per
# mktemp -d reservierten privaten Verzeichnis (mode 0700) – kein 'mktemp -u',
# dessen unreservierter Name sonst von einem parallelen Prozess/Symlink belegt
# werden könnte. mv -T ersetzt current atomar und löscht nie das Live-Ziel.
LINKDIR="$(mktemp -d "$BASE/.linkdir.XXXXXX")"
ln -s "$SHA" "$LINKDIR/current"
mv -T "$LINKDIR/current" "$BASE/current"
rmdir "$LINKDIR"
LINKDIR=""

echo "deploy: current -> $SHA"
