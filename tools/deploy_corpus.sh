#!/usr/bin/env bash
# Deployt den committeten public/-Korpus als versionierten Snapshot und
# schaltet den current-Symlink atomar um.
#
#   deploy_corpus.sh <git-ref>
#
# Es wird ausschließlich der committete public/-Baum des angeforderten Refs
# exportiert (git archive, nicht die Arbeitskopie). internal/ wird nie kopiert.
# Ältere Snapshots bleiben erhalten.
set -euo pipefail

REF="${1:?usage: deploy_corpus.sh <git-ref>}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE="${DL_KNOWLEDGE_HOME:-$HOME/.local/share/dl-knowledge}"

# Vollen SHA auflösen (schlägt bei unbekanntem Ref fehl).
SHA="$(git rev-parse --verify "${REF}^{commit}")"
DEST="$BASE/$SHA"
STAGING="$BASE/.staging-$SHA"

mkdir -p "$BASE"
rm -rf "$STAGING"
mkdir -p "$STAGING"
trap 'rm -rf "$STAGING"' EXIT

# Nur den committeten public/-Baum exportieren; scheitert, wenn public/ am Ref fehlt.
git archive "$SHA" public | tar -x -C "$STAGING"

# Ohne öffentliche HTML-Seite gibt es nichts zu deployen.
html_count="$(find "$STAGING/public" -type f -name '*.html' 2>/dev/null | wc -l)"
if [ "$html_count" -eq 0 ]; then
  echo "deploy: kein öffentliches HTML in $SHA" >&2
  exit 1
fi

# Snapshot gegen den Korpusvertrag prüfen, bevor er live geht.
python3 "$SCRIPT_DIR/validate_corpus.py" "$STAGING"

# Snapshot veröffentlichen (idempotent für denselben SHA, ohne andere zu löschen).
rm -rf "$DEST"
mv "$STAGING" "$DEST"

# current-Symlink atomar umschalten (relativer Ziel-Name innerhalb von BASE).
ln -sfn "$SHA" "$BASE/.current.tmp"
mv -T "$BASE/.current.tmp" "$BASE/current"

echo "deploy: current -> $SHA"
