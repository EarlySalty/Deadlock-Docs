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

# Lokale Replace-Refs sowie System- und globale Attribute dürfen den
# committeten Export nicht verändern.
export GIT_NO_REPLACE_OBJECTS=1
export GIT_ATTR_NOSYSTEM=1
SHA="$(git -c core.attributesFile=/dev/null -C "$REPO_ROOT" rev-parse --verify "${REF}^{commit}")"
ORIGINAL_OBJECT_DIR="$(git -C "$REPO_ROOT" rev-parse --path-format=absolute --git-path objects)"
OBJECT_FORMAT="$(git -c core.attributesFile=/dev/null -C "$REPO_ROOT" rev-parse --show-object-format)"
DEST="$BASE/$SHA"

mkdir -p "$BASE"

# Den Soll-Snapshot bei jedem Deploy frisch aus Git erzeugen. Auch ein bereits
# vorhandenes SHA-Verzeichnis ist erst vertrauenswürdig, wenn es erneut den
# Korpusvertrag erfüllt und baumgleich mit genau diesem Commit ist.
STAGING="$(mktemp -d "$BASE/.staging.XXXXXX")"

# Ein leeres Bare-Control-Gitdir trennt den Export von lokalen Repository-
# Attributen und Refs; nur die originalen Commit-Objekte bleiben zugänglich.
CONTROL_GIT_DIR="$STAGING/.control.git"
git init --bare -q --template= --object-format="$OBJECT_FORMAT" "$CONTROL_GIT_DIR"
GIT_OBJECT_DIRECTORY="$ORIGINAL_OBJECT_DIR" \
  git -c core.attributesFile=/dev/null --git-dir="$CONTROL_GIT_DIR" archive "$SHA" public \
  | tar -x -C "$STAGING"
rm -rf "$CONTROL_GIT_DIR"

# Ohne öffentliche HTML-Seite gibt es nichts zu deployen.
html_count="$(find "$STAGING/public" -type f -name '*.html' 2>/dev/null | wc -l)"
if [ "$html_count" -eq 0 ]; then
  echo "deploy: kein öffentliches HTML in $SHA" >&2
  exit 1
fi

# Soll-Export prüfen, bevor irgendein current-Link verändert wird.
python3 "$SCRIPT_DIR/validate_corpus.py" "$STAGING"

verify_existing_snapshot() {
  if [ -L "$DEST" ] || [ ! -d "$DEST" ]; then
    echo "deploy: vorhandenes Snapshot-Ziel ist kein echtes Verzeichnis: $SHA" >&2
    return 1
  fi
  python3 "$SCRIPT_DIR/validate_corpus.py" "$DEST" >/dev/null
  if ! diff -qr --no-dereference "$STAGING" "$DEST" >/dev/null; then
    echo "deploy: vorhandener Snapshot stimmt nicht mit Commit $SHA überein" >&2
    return 1
  fi
}

if [ -e "$DEST" ] || [ -L "$DEST" ]; then
  verify_existing_snapshot
elif mv -T "$STAGING" "$DEST" 2>/dev/null; then
  # Staging ist jetzt der unveränderliche SHA-Snapshot; Cleanup darf ihn nicht
  # mehr als temporäres Verzeichnis behandeln.
  STAGING=""
else
  # Ein paralleler Deploy derselben SHA kann den Zielnamen gewonnen haben.
  # Nur dessen vollständig geprüften, identischen Snapshot übernehmen.
  verify_existing_snapshot
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
