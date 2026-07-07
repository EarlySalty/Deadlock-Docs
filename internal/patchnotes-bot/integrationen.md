---
title: "Patchnotes-Bot Integrationen"
tags: [internal, patchnotes-bot, integrationen]
stand: 2026-07-07
quelle: "Deadlock--Patchnotes-Bot"
---
# Patchnotes-Bot Integrationen

## Discord

Der Patch-Channel kommt aus `PATCH_CHANNEL_ID`. Der Wrapper setzt als Default `1326973956825284628`, und `main.py` löst diesen Channel über Cache oder `fetch_channel()` auf. (`scripts/run_patchnotes_bot.sh`, `main.py`)

Der Logs-Channel kommt aus `PATCH_LOGS_CHANNEL_ID`. Der Wrapper setzt als Default `1374364800817303632`, und `main.py` nutzt ihn für Logs-Nachrichten und optional für Prepared-Patches. (`scripts/run_patchnotes_bot.sh`, `main.py`)

Der Bot aktiviert `message_content` und `guilds` in den Discord-Intents. Ohne `message_content` kann `on_message()` die Team-Befehle nicht lesen. (`main.py`)

`patch_response()` sendet Text in Chunks unter `PATCH_CHUNK_LIMIT`. Wenn `PATCH_EMBED_V2` aktiv ist, versucht der Bot Components V2; Renderfehler fallen auf Text zurück. (`main.py`, `patch_view.py`)

Der Rollen-Ping steht als `ROLE_PING` in `perplexity_requests.py`. `patch_response()` hängt ihn als eigene Nachricht an, wenn `include_ping=True` ist. (`perplexity_requests.py`, `main.py`)

## Team-Befehle

`!tpatch` triggert die Neuübersetzung des zuletzt gespeicherten Patches ohne Ping. `_get_retranslate_mode()` gibt dafür `False` zurück. (`main.py`)

`!ppatch` triggert dieselbe Neuübersetzung mit Ping. `_get_retranslate_mode()` gibt dafür `True` zurück. (`main.py`)

Beide Befehle haben einen Cooldown von `60` Sekunden pro Channel. `on_message()` speichert den letzten Zeitpunkt in `_retranslate_cooldowns`. (`main.py`)

Die Retranslation lädt den neuesten DB-Eintrag, fällt bei fehlendem Rohtext auf erneutes Content-Fetching über die URL zurück, übersetzt neu und schreibt den Datensatz wieder. (`main.py`, `patchnotes_db.py`, `changelog_content_fetcher.py`)

## Brain-Wissens-Sync

Nach jedem erfolgreichen `upsert_changelog()` ruft `save_changelog_to_db()` `trigger_brain_patchnotes_sync(url)` auf. Der Sync-Start liegt damit nach dem DB-Schreiben und vor dem Discord-Versand in `update_patch()`. (`main.py`, `patchnotes_db.py`)

Der Sync ist per `BRAIN_PATCHNOTES_SYNC_ENABLED` abschaltbar. Der Servicename kommt aus `BRAIN_PATCHNOTES_SYNC_SERVICE` und fällt auf `deadlock-brain-patchnotes-sync.service` zurück. (`main.py`)

Der Bot startet den Sync mit `systemctl --user start <service>`. Fehler beim Start werden geloggt und nicht in den Patchpost zurückgeworfen. (`main.py`)

`deadlock-brain-patchnotes-sync.service` ist ein `oneshot`-Service. Die Unit setzt `DEADLOCK_BRAIN_ROOT=/home/naniadm/Documents/Deadlock-Brain`, `LOAD_INFISICAL=1` und startet `/home/naniadm/.local/bin/deadlock-brain-patchnotes-sync.sh`. (`/home/naniadm/.config/systemd/user/deadlock-brain-patchnotes-sync.service`)

Das Brain-Sync-Skript vergleicht zuerst die neueste `patchnotes.changelog_posts`-ID mit `brain.entity_snapshots`. Bei neuen Patchnotes zieht es Deadlock-Daten, Assets, Patchnotes, Parser- und Enrichment-Schritte und schreibt einen Qualitätsbericht nach `data/last_patchnotes_sync_quality.json`. (`/home/naniadm/.local/bin/deadlock-brain-patchnotes-sync.sh`)
