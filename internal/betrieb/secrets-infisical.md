---
title: "Cross-System-Betrieb - Secrets und Infisical"
tags: [internal, betrieb, secrets, infisical]
stand: 2026-07-07
quelle: "systemd-User-Units und Service-Wrapper"
---
# Cross-System-Betrieb - Secrets und Infisical

Secrets laufen über Infisical und systemd-Credentials, nicht über Klartextdateien im Repo.
Diese Datei nennt nur Variablennamen und Pfade, nie Werte.
Secret-Dateien bleiben beim Debugging tabu.

## Startmuster

| Schritt | Mechanismus | Beleg |
|---|---|---|
| Infisical-Verfügbarkeit | `wait_for_infisical.sh` pollt `http://127.0.0.1:8080/api/status` mit Timeout und Intervall aus Env-Namen. | `Deadlock-Bots/scripts/wait_for_infisical.sh` |
| Bootstrap-Token | systemd lädt `LoadCredential=infisical-token:...`; Wrapper lesen nur `CREDENTIALS_DIRECTORY/infisical-token`. | `systemctl --user cat deadlock-bot-rust.service`; `systemctl --user cat steam-core.service`; `Deadlock-Bots/scripts/run_dl_bot_service.sh`; `Deadlock-Steam-Bot/rust/deploy/run-steam-core.sh` |
| Infisical-Config | Wrapper sourcen nur Verbindungsparameter aus `INFISICAL_CONFIG_FILE`; der Service-Token kommt bevorzugt aus systemd-Credentials. | `Deadlock-Bots/scripts/run_bot_with_infisical.sh`; `Deadlock-Twitch-Bot/rust/scripts/run_tb_bot_service.sh`; `Website/scripts/run_builds_backend.sh` |
| Export | `export_infisical_env.py` liest `INFISICAL_API_URL`, `INFISICAL_PROJECT_ID`, `INFISICAL_ENV`, `INFISICAL_SERVICE_TOKEN`, optional `INFISICAL_SECRET_PATH` und `INFISICAL_HTTP_TIMEOUT`; Ausgabeformat ist `export NAME=...`. | `Deadlock-Bots/scripts/export_infisical_env.py` |
| Prozessstart | Wrapper führen nach dem Export `exec` auf das Ziel-Binary aus; dadurch zeigt systemd am Ende auf den Dienstprozess, nicht auf eine dauerhafte Shell. | `Deadlock-Bots/scripts/run_dl_web_service.sh`; `Deadlock-Steam-Bot/rust/deploy/run-steam-bot.sh`; `Deadlock-Turniere/scripts/run_turniere_backend_rust.sh` |

## Dienst-spezifische Abweichungen

| Dienstfamilie | Besonderheit | Beleg |
|---|---|---|
| Deadlock-Bots | `run_dl_bot_service.sh`, `run_dl_web_service.sh`, `run_dl_knowledge_service.sh` und `run_twitch_invite_sync.sh` verwenden denselben Exporter aus `Deadlock-Bots/scripts`. | `Deadlock-Bots/scripts/run_dl_bot_service.sh`; `Deadlock-Bots/scripts/run_dl_web_service.sh`; `Deadlock-Bots/scripts/run_dl_knowledge_service.sh`; `Deadlock-Bots/scripts/run_twitch_invite_sync.sh` |
| Steam | `run-steam-core.sh` und `run-steam-bot.sh` teilen sich die Deadlock-Bots-Infisical-Konfiguration und den Deadlock-Bots-Exporter. | `Deadlock-Steam-Bot/rust/deploy/run-steam-core.sh`; `Deadlock-Steam-Bot/rust/deploy/run-steam-bot.sh` |
| Twitch | Rust-Worker und Rust-Dashboard lesen `~/.config/deadlock-twitch-bot/infisical.conf` über `INFISICAL_CONFIG_FILE` und starten `tb-bot` oder `tb-dashboard`. | `Deadlock-Twitch-Bot/rust/scripts/run_tb_bot_service.sh`; `Deadlock-Twitch-Bot/rust/scripts/run_tb_dashboard_service.sh` |
| Turniere | Der Rust-Launcher sourced `TURNIERE_CONFIG_FILE` und danach die Infisical-Konfiguration; `DEADLOCK_CENTRAL_DSN` ist Pflicht, der Wert wird nicht ausgegeben. | `Deadlock-Turniere/scripts/run_turniere_backend_rust.sh` |
| Patchnotes | Der Wrapper akzeptiert `DISCORD_TOKEN_PATCHNOTES` oder `PATCHNOTES_BOT_TOKEN` als Namen und verweigert den generischen Token-Pfad. | `Deadlock--Patchnotes-Bot/scripts/run_patchnotes_bot.sh` |
| Website | `run_builds_backend.sh` lädt Infisical, verlangt im Rust-Pfad `DEADLOCK_CENTRAL_DSN` und startet `ddc-website-backend`. | `Website/scripts/run_builds_backend.sh` |

## Dateien, die nicht gelesen werden

`~/.config/deadlock-bots/infisical.conf`, `~/.config/deadlock-twitch-bot/infisical.conf`, `~/.config/deadlock-turniere/turniere.env`, `~/.config/deadlock-patchnotes/patchnotes.env` und alles unter `CREDENTIALS_DIRECTORY` sind Secret- oder Secret-nahe Laufzeitdateien. Betriebsaussagen dürfen daraus nur Namen ableiten, wenn ein Wrapper diese Namen im Code nennt. (`Deadlock-Bots/scripts/run_bot_with_infisical.sh`; `Deadlock-Turniere/scripts/run_turniere_backend_rust.sh`; `Deadlock--Patchnotes-Bot/scripts/run_patchnotes_bot.sh`)

Die Repos ignorieren Env-Dateien, lokale Datenbanken, Logs und lokale Worktree-/Run-Artefakte. Neue lokale Run-Skripte gehören in die bestehenden `scripts/`-Muster, aber ohne Secret-Werte und ohne Klartext-Token. (`Deadlock-Bots/.gitignore`; `Deadlock-Twitch-Bot/.gitignore`; `Deadlock-Turniere/.gitignore`; `Website/.gitignore`)

