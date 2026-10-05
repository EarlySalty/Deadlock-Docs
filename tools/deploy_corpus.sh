#!/usr/bin/env bash
# Deployt den committeten public/-Korpus als versionierten Snapshot und
# schaltet den current-Symlink atomar um.
#
#   deploy_corpus.sh <git-ref> [zielverzeichnis]
#
# Es wird ausschließlich der committete public/-Baum des angeforderten Refs
# exportiert (git archive, nicht die Arbeitskopie). internal/ wird nie kopiert.
# SHA-Snapshots sind nach der ersten Veröffentlichung unveränderlich; ältere
# Snapshots bleiben erhalten. Deploys sind race-sicher (eindeutige Temp-Namen)
# und lassen bei Fehlern das laufende current unangetastet.
set -euo pipefail

if [ "${1:-}" = "--config" ]; then
  CONFIG="${2:?usage: deploy_corpus.sh --config <refresh.json>}"
  exec python3 "$(dirname "${BASH_SOURCE[0]}")/refresh_public_corpus.py" --config "$CONFIG"
fi

REF="${1:?usage: deploy_corpus.sh <git-ref>}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Deployt wird immer das Repository des Skripts (SCRIPT_DIR/..), unabhängig vom
# Aufruf-CWD – sonst könnte ein fremdes Repo als Deadlock-Korpus erscheinen.
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
if [ -f "$REPO_ROOT/public-sources.json" ] && [ "$REF" != "--web-source" ]; then
  echo "deploy: Dieser Korpus braucht die Quellen-/Frischeprüfung. Nutze deploy_corpus.sh --config <refresh.json>." >&2
  exit 1
fi
BASE="${2:-${DL_KNOWLEDGE_HOME:-$HOME/.local/share/dl-knowledge}}"
WEB_SOURCE=""
if [ "$REF" = "--web-source" ]; then
  WEB_SOURCE="$(realpath "${2:?Snapshot erforderlich}")"
  BASE="${3:?Web-Zielverzeichnis erforderlich}"
  SOURCE_BASE="$(jq -er '.base' "$REPO_ROOT/ops/public-corpus-refresh.json")"
  if [ "$(dirname "$WEB_SOURCE")" != "$SOURCE_BASE" ] || [ "$(realpath "$SOURCE_BASE/current")" != "$WEB_SOURCE" ]; then
    echo "deploy: Webquelle ist nicht der aktive öffentliche Snapshot" >&2
    exit 1
  fi
  SOURCE_NAME="$(basename "$WEB_SOURCE")"
  jq -e --arg snapshot "$SOURCE_NAME" '.refresh_status == "ok" and .active_snapshot == $snapshot' "$SOURCE_BASE/status-summary.json" >/dev/null
  SOURCE_DATE="$(jq -er '.generated_at' "$SOURCE_BASE/status-summary.json")"
  SOURCE_AGE="$(( $(date +%s) - $(date -d "$SOURCE_DATE" +%s) ))"
  if [ "$SOURCE_AGE" -lt 0 ] || [ "$SOURCE_AGE" -gt 86400 ]; then
    echo "deploy: Quellenprüfung ist nicht aktuell" >&2
    exit 1
  fi
  SOURCE_IDENTITY="$(jq -er '.identity' "$WEB_SOURCE/source-manifest.json")"
  case "$SOURCE_NAME" in *-"$SOURCE_IDENTITY"-*) ;; *) echo "deploy: Quellenmanifest passt nicht zum Snapshot" >&2; exit 1 ;; esac
  if [ -L "$WEB_SOURCE/public" ] || [ ! -d "$WEB_SOURCE/public" ] || [ -n "$(find "$WEB_SOURCE/public" -mindepth 1 ! -type d ! -type f -print -quit)" ]; then
    echo "deploy: Webquelle enthält nichtreguläre Dateien" >&2
    exit 1
  fi
  # Identität nach dem bestehenden corpus_digest-Vertrag, nur HTML im public-Baum.
  SOURCE_DIGEST="$(
    while IFS= read -r -d '' page; do
      page_hash="$(sha256sum "$WEB_SOURCE/public/$page" | cut -c1-64)"
      printf '%s\0%s\n' "$page" "$page_hash"
    done < <(find "$WEB_SOURCE/public" -type f -name '*.html' -printf '%P\0' | LC_ALL=C sort -z) | sha256sum | cut -c1-64)"
  jq -e --arg generation "$SOURCE_DIGEST" '.generation == $generation' "$SOURCE_BASE/status-summary.json" >/dev/null
fi

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
if [ -n "$WEB_SOURCE" ]; then
  SHA="$SOURCE_NAME"
else
SHA="$(git -c core.attributesFile=/dev/null -C "$REPO_ROOT" rev-parse --verify "${REF}^{commit}")"
ORIGINAL_OBJECT_DIR="$(git -C "$REPO_ROOT" rev-parse --path-format=absolute --git-path objects)"
OBJECT_FORMAT="$(git -c core.attributesFile=/dev/null -C "$REPO_ROOT" rev-parse --show-object-format)"
fi
DEST="$BASE/$SHA"

mkdir -p "$BASE"

# Den Soll-Snapshot bei jedem Deploy frisch aus Git erzeugen. Auch ein bereits
# vorhandenes SHA-Verzeichnis ist erst vertrauenswürdig, wenn es erneut den
# Korpusvertrag erfüllt und baumgleich mit genau diesem Commit ist.
STAGING="$(mktemp -d "$BASE/.staging.XXXXXX")"

# Ein leeres Bare-Control-Gitdir trennt den Export von lokalen Repository-
# Attributen und Refs; nur die originalen Commit-Objekte bleiben zugänglich.
if [ -n "$WEB_SOURCE" ]; then
  cp -a "$WEB_SOURCE/public" "$STAGING/public"
else
CONTROL_GIT_DIR="$STAGING/.control.git"
git init --bare -q --template= --object-format="$OBJECT_FORMAT" "$CONTROL_GIT_DIR"
GIT_OBJECT_DIRECTORY="$ORIGINAL_OBJECT_DIR" \
  git -c core.attributesFile=/dev/null --git-dir="$CONTROL_GIT_DIR" archive "$SHA" public \
  | tar -x -C "$STAGING"
rm -rf "$CONTROL_GIT_DIR"
fi

# Ohne öffentliche HTML-Seite gibt es nichts zu deployen.
html_count="$(find "$STAGING/public" -type f -name '*.html' 2>/dev/null | wc -l)"
if [ "$html_count" -eq 0 ]; then
  echo "deploy: kein öffentliches HTML in $SHA" >&2
  exit 1
fi

# Soll-Export prüfen, bevor irgendein current-Link verändert wird.
if [ -z "$WEB_SOURCE" ]; then
  python3 "$SCRIPT_DIR/validate_corpus.py" "$STAGING"
else
  # Die aktive Pipeline hat Struktur, Quellen und Fachgültigkeit bereits geprüft.
  diff -qr --no-dereference "$WEB_SOURCE/public" "$STAGING/public" >/dev/null
fi

# Nur der validierte öffentliche Export bekommt Webserver-Leserechte.
# mktemp erzeugt sonst 0700, das Caddy den Zugang zum gesamten Snapshot sperrt.
chmod 0755 "$STAGING"
find "$STAGING/public" -type d -exec chmod 0755 {} +
find "$STAGING/public" -type f -exec chmod 0644 {} +

verify_existing_snapshot() {
  if [ -L "$DEST" ] || [ ! -d "$DEST" ]; then
    echo "deploy: vorhandenes Snapshot-Ziel ist kein echtes Verzeichnis: $SHA" >&2
    return 1
  fi
  if [ -z "$WEB_SOURCE" ]; then
    python3 "$SCRIPT_DIR/validate_corpus.py" "$DEST" >/dev/null
  fi
  if ! diff -qr --no-dereference "$STAGING" "$DEST" >/dev/null; then
    echo "deploy: vorhandener Snapshot stimmt nicht mit Commit $SHA überein" >&2
    return 1
  fi
  # Erst nach Vertragsprüfung und Baumgleichheit alte 0700-Snapshots freigeben.
  chmod 0755 "$DEST"
  find "$DEST/public" -type d -exec chmod 0755 {} +
  find "$DEST/public" -type f -exec chmod 0644 {} +
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
