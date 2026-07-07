---
title: "Patchnotes-Bot Betrieb"
tags: [internal, patchnotes-bot, betrieb]
stand: 2026-07-07
quelle: "Deadlock--Patchnotes-Bot"
---
# Patchnotes-Bot Betrieb

Start und Neustart laufen über den User-Service `deadlock-patchnotes.service`. Die Unit startet `/usr/bin/bash -lc '/home/naniadm/Documents/Deadlock--Patchnotes-Bot/scripts/run_patchnotes_bot.sh'`. (`/home/naniadm/.config/systemd/user/deadlock-patchnotes.service`)

```bash
systemctl --user start deadlock-patchnotes.service
systemctl --user restart deadlock-patchnotes.service
systemctl --user status deadlock-patchnotes.service
```

Die Unit setzt `Restart=always`, `RestartSec=5`, `TimeoutStopSec=20` und `KillMode=mixed`. Ein Prozess-Crash wird damit von systemd neu gestartet. (`/home/naniadm/.config/systemd/user/deadlock-patchnotes.service`)

Der Wrapper nimmt zuerst `$DEADLOCK_HOME/.venv/bin/python`, wenn diese Datei ausführbar ist, sonst `python3`. Danach führt er im Bot-Repo `main.py` aus. (`scripts/run_patchnotes_bot.sh`)

Der Wrapper hält eine exklusive `flock` auf `PATCHNOTES_LOCK_FILE`; ohne Lock beendet er den Start mit Hinweis auf den laufenden Bot. (`scripts/run_patchnotes_bot.sh`)

## Env-Variablen

Start und Secrets lesen `INFISICAL_CONFIG_FILE`, `PATCHNOTES_ENV_FILE`, `CREDENTIALS_DIRECTORY`, `INFISICAL_SERVICE_TOKEN`, `DEADLOCK_HOME`, `PYTHON_BIN`, `INFISICAL_RETRY_DELAY`, `INFISICAL_MAX_ATTEMPTS` und `PATCHNOTES_LOCK_FILE`. (`scripts/run_patchnotes_bot.sh`)

Discord und DB nutzen `DEADLOCK_CENTRAL_DSN`, `DISCORD_TOKEN_PATCHNOTES`, `PATCHNOTES_BOT_TOKEN`, `BOT_TOKEN`, `PATCH_CHANNEL_ID` und `PATCH_LOGS_CHANNEL_ID`. (`scripts/run_patchnotes_bot.sh`, `main.py`, `patchnotes_db.py`)

Polling und Steam nutzen `CHECK_INTERVAL_SECONDS`, `PATCH_STEAM_NEWS_TRIGGER_ENABLED`, `PATCH_STEAM_NEWS_TRIGGER_INTERVAL_SECONDS`, `PATCH_STEAM_VERSION_BURST_ENABLED`, `PATCH_STEAM_VERSION_TRIGGER_FILE`, `PATCH_STEAM_VERSION_TRIGGER_CHECK_SECONDS`, `PATCH_STEAM_VERSION_BURST_DURATION_SECONDS`, `PATCH_STEAM_VERSION_BURST_INTERVAL_SECONDS`, `PATCH_SIGNAL_HISTORY_FILE`, `PATCH_SIGNAL_HISTORY_MAX_ENTRIES`, `PATCH_MAX_AUTO_POST_AGE_DAYS` und `PATCH_MAX_CATCHUP_POSTS`. (`main.py`)

Ausgabe und Formatierung nutzen `PATCH_OUTPUT_DIR`, `BOT_DRY_RUN`, `PATCH_CHUNK_LIMIT`, `PATCH_TIMING_LEVEL`, `PATCH_SCAN_VERBOSE`, `PATCH_EMBED_V2`, `PATCH_AUTO_INCLUDE_PING`, `PATCH_FORCE_POST_LATEST_ON_START`, `PATCH_TRANSLATE_SPLIT_THRESHOLD` und `PATCH_TRANSLATE_CHUNK_TARGET`. (`main.py`)

Prepared-Patch nutzt `PATCH_PREPARED_FILE`, `PATCH_PREPARED_POST_ON_START`, `PATCH_PREPARED_INCLUDE_PING`, `PATCH_PREPARED_TRANSLATE`, `PATCH_PREPARED_USE_LOGS_CHANNEL` und `PATCH_PREPARED_ONLY_MODE`. Das One-shot-Skript setzt zusätzlich `PATCH_FILE`, `PATCH_TARGET`, `PATCH_PING` und `PATCH_TRANSLATE`. (`main.py`, `scripts/run_prepared_patch_once.sh`)

KI und Brain-Sync nutzen `PERPLEXITY_API_KEY`, `PERPLEXITY_MODEL`, `PERPLEXITY_MAX_TOKENS`, `BRAIN_PATCHNOTES_SYNC_ENABLED` und `BRAIN_PATCHNOTES_SYNC_SERVICE`. (`perplexity_requests.py`, `main.py`)

## Fallen

`main.py` hat keinen eigenen Default für `PATCH_CHANNEL_ID`; der Wrapper setzt den Default. Ein direkter Start von `main.py` ohne `PATCH_CHANNEL_ID` scheitert beim `int(os.getenv("PATCH_CHANNEL_ID"))`. (`main.py`, `scripts/run_patchnotes_bot.sh`)

Der Wrapper akzeptiert nicht einfach ein vorhandenes `BOT_TOKEN`. Er bildet den Token aus `DISCORD_TOKEN_PATCHNOTES` oder `PATCHNOTES_BOT_TOKEN` und überschreibt ein abweichendes `BOT_TOKEN`. (`scripts/run_patchnotes_bot.sh`)

`DEADLOCK_CENTRAL_DSN` ist Pflicht. Der Wrapper beendet ohne DSN, und der DB-Layer wirft ohne DSN `CentralDBError`. (`scripts/run_patchnotes_bot.sh`, `patchnotes_db.py`)

`DEADLOCK_DB_PATH` und `DEADLOCK_DB_DIR` werden im Wrapper entfernt. Alte SQLite-Umgebung hat im Runtime-Pfad keine Wirkung. (`scripts/run_patchnotes_bot.sh`)

Wenn `PATCH_OUTPUT_DIR` gesetzt ist und `BOT_DRY_RUN` fehlt, setzt `main.py` `BOT_DRY_RUN=True`; der `__main__`-Block startet den Discord-Client dann nicht. Für Datei-Ausgabe mit laufendem Client muss `BOT_DRY_RUN` ausdrücklich anders gesetzt werden. (`main.py`)

`PATCH_PREPARED_ONLY_MODE` schließt den Client nach `maybe_post_prepared_patch_once()`. Der normale Scan-Loop startet in diesem Modus nicht. (`main.py`)

Ein unerwarteter Fehler in `_scan_loop()` wird geloggt und erneut geworfen. Innerhalb desselben Prozesses baut `main.py` keinen neuen Scan-Task; die Prozessaufsicht kommt aus `Restart=always`. (`main.py`, `/home/naniadm/.config/systemd/user/deadlock-patchnotes.service`)
