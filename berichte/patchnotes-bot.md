---
title: "Patchnotes-Bot Bericht"
tags: [internal, patchnotes-bot, bericht]
stand: 2026-07-07
quelle: "Deadlock--Patchnotes-Bot"
---
# Patchnotes-Bot Bericht

## Dateiliste

- `internal/patchnotes-bot/uebersicht.md`
- `internal/patchnotes-bot/architektur.md`
- `internal/patchnotes-bot/betrieb.md`
- `internal/patchnotes-bot/integrationen.md`
- `internal/patchnotes-bot/bericht.md`

## Veraltete Alt-Doku-Funde

`docs/plans/2026-07-01-patchnotes-central-db.md` enthält im Abschnitt "Aktueller Befund" noch die alte Aussage zu `service.db` und SQLite. Der Runtime-Code importiert heute `patchnotes_db`, der Wrapper entfernt `DEADLOCK_DB_PATH` und `DEADLOCK_DB_DIR`, und `patchnotes_db.py` nutzt `DEADLOCK_CENTRAL_DSN`. (`docs/plans/2026-07-01-patchnotes-central-db.md`, `main.py`, `scripts/run_patchnotes_bot.sh`, `patchnotes_db.py`)

`README.md` verweist auf einen `prompt`-String. Der aktuelle Prompt entsteht in `_build_system_prompt()`, wird als `system_prompt` zusammen mit `user_prompt` gebaut und danach an Perplexity übergeben. (`README.md`, `perplexity_requests.py`)

`docs/internal/perplexity-summarization.md` und `docs/internal/scheduler.md` haben kein Frontmatter. Der aktuelle Styleguide verlangt `title`, `tags`, `stand` und `quelle`. (`docs/internal/perplexity-summarization.md`, `docs/internal/scheduler.md`, `/home/naniadm/Documents/Deadlock-Docs/internal/STYLEGUIDE.md`)

Mehrere alte Doku-Dateien nutzen Umlaut-Ersatzschreibungen. Der aktuelle Styleguide verlangt echte UTF-8-Umlaute und Eszett. (`docs/plans/2026-07-01-patchnotes-central-db.md`, `WORKFLOW.md`, `/home/naniadm/Documents/Deadlock-Docs/internal/STYLEGUIDE.md`)

## UNSICHER

UNSICHER: Die Discord-Channel-Namen stehen nicht im gelesenen Code. Belegt sind nur die IDs aus `PATCH_CHANNEL_ID` und `PATCH_LOGS_CHANNEL_ID`. (`scripts/run_patchnotes_bot.sh`, `main.py`)

UNSICHER: Der Live-Status von `deadlock-patchnotes.service` wurde nicht geprüft. Belegt sind Unit, Wrapper und Codepfad, nicht der aktuell laufende Prozess. (`/home/naniadm/.config/systemd/user/deadlock-patchnotes.service`, `scripts/run_patchnotes_bot.sh`, `main.py`)

UNSICHER: Der zentrale Postgres-Inhalt wurde nicht abgefragt. Belegt sind SQL-Ziele und DSN-Pflicht im Code, nicht der Live-Datenbestand. (`patchnotes_db.py`, `scripts/run_patchnotes_bot.sh`)

## Codepoint-Check

Der geforderte Codepoint-Check über das Zielverzeichnis lief ohne Treffer.
