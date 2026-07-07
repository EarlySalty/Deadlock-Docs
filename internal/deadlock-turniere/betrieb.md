---
title: "Turniere — Betrieb"
tags: [internal, deadlock-turniere, betrieb]
stand: 2026-07-07
quelle: Deadlock-Turniere
---
# Turniere — Betrieb

Der Betriebspfad ist der systemd-User-Service `deadlock-turniere.service` mit Rust-Cutover-Drop-in. Neustarts laufen als User-Service, nicht über Root. Die zentrale Pflicht-Variable für Fachdaten ist `DEADLOCK_CENTRAL_DSN`. (`/home/naniadm/.config/systemd/user/deadlock-turniere.service.d/30-rust-cutover.conf`, `scripts/run_turniere_backend_rust.sh`, `rust/crates/turnier-db/src/pool.rs`)

## Service

Neustart: `systemctl --user restart deadlock-turniere.service`. Für Laufzeitprüfung immer `systemctl --user cat deadlock-turniere.service` verwenden, weil die Basisdatei und die Drop-ins zusammen den wirksamen Start ergeben. (`/home/naniadm/.config/systemd/user/deadlock-turniere.service`, `/etc/systemd/user/deadlock-turniere.service.d/10-infisical-gate.conf`, `/home/naniadm/.config/systemd/user/deadlock-turniere.service.d/30-rust-cutover.conf`)

Vor dem Start wartet das globale Drop-in auf Infisical, das Credential-Drop-in lädt `infisical-token`, und das Rust-Cutover-Drop-in ersetzt `ExecStart` durch `scripts/run_turniere_backend_rust.sh`. Diese Reihenfolge ist Teil der kompletten Unit. (`/etc/systemd/user/deadlock-turniere.service.d/10-infisical-gate.conf`, `/home/naniadm/.config/systemd/user/deadlock-turniere.service.d/20-creds.conf`, `/home/naniadm/.config/systemd/user/deadlock-turniere.service.d/30-rust-cutover.conf`)

Der Rust-Launcher liest `TURNIERE_CONFIG_FILE` oder `$HOME/.config/deadlock-turniere/turniere.env`, optional `INFISICAL_CONFIG_FILE` oder `$HOME/.config/deadlock-bots/infisical.conf`, und bei gesetztem `CREDENTIALS_DIRECTORY` die Datei `infisical-token`. Fehlt `INFISICAL_SERVICE_TOKEN`, beendet er den Start. (`scripts/run_turniere_backend_rust.sh`)

## Konfiguration

Die Rust-Config liest zuerst `NAME_FILE`, danach Secret-Dateien in `CREDENTIALS_DIRECTORY`, `SECRETS_DIRECTORY` oder `VAULT_SECRETS_DIR`, danach Env-Werte, danach Defaults. Der Resolver trimmt Datei- und Env-Werte und ignoriert leere Werte. (`rust/crates/turnier-config/src/secrets.rs`)

| Name | Bedeutung |
| --- | --- |
| `DEADLOCK_CENTRAL_DSN` | Pflicht-DSN für die zentrale Postgres-DB |
| `BACKEND_HOST`, `BACKEND_PORT` | Listener-Adresse für `turnier-bot` |
| `BACKEND_ALLOWED_HOSTS` | Zusatzhosts für den Host-Guard |
| `FRONTEND_URL`, `TURNIER_PUBLIC_URL` | CORS, Redirects und öffentliche Links |
| `DISCORD_OAUTH_INTERNAL_API_BASE_URL` | Interne OAuth-Basis-URL |
| `TURNIER_INTERNAL_API_TOKEN`, `MASTER_BROKER_TOKEN`, `MAIN_BOT_INTERNAL_TOKEN`, `TWITCH_INTERNAL_API_TOKEN` | Token-Aliase für OAuth/Broker |
| `DISCORD_MASTER_BROKER_BASE_URL`, `DISCORD_MASTER_BROKER_TOKEN` | Master-Broker für Discord-Effekte |
| `DISCORD_BOT_TOKEN`, `DISCORD_TOKEN`, `BOT_TOKEN` | Token-Aliase für Discord-Client-Fallbacks |
| `STEAM_BRIDGE_DB_PATH` | SQLite-Queue des Steam-Workers |
| `AVATAR_DIR` | Profilavatar-Verzeichnis |
| `TURNIER_ENABLE_TEST_MODE` | Schalter für Test-Routen |
| `CENTRAL_TEST_DSN`, `TURNIER_TEST_DB_CONFIRM` | Schutzwerte für Test-Wipe |

`Config::from_env()` definiert die aktiven Server-, Discord-, OAuth-, Broker-, Rollen-, Avatar- und Steam-Bridge-Namen. `turnier-api::test_mode` hängt Test-Routen nur an, wenn `TURNIER_ENABLE_TEST_MODE` aktiv ist, und schützt den Wipe zusätzlich über `CENTRAL_TEST_DSN` und `TURNIER_TEST_DB_CONFIRM=throwaway-only`. (`rust/crates/turnier-config/src/lib.rs`, `rust/crates/turnier-api/src/test_mode.rs`)

## Prüfungen

Smoke-Check ohne Listener: `rust/target/release/turnier-bot --check`. Dieser Pfad lädt Config, öffnet die zentrale DB, baut `AppState`, Scheduler und Router und beendet sich vor `TcpListener::bind()`. (`rust/crates/turnier-bot/src/main.rs`)

Der Launcher prüft vor dem Exec, ob `DEADLOCK_CENTRAL_DSN` gesetzt ist. Fehlt die Variable, beendet der Start mit einem Fehler, bevor `turnier-bot` läuft. (`scripts/run_turniere_backend_rust.sh`)

## Fallstricke

Die erste `ExecStart`-Zeile in der Basisdatei ist nicht die Laufzeit-Wahrheit. Das Drop-in `30-rust-cutover.conf` löscht sie und setzt den Rust-Launcher als neuen Start. (`/home/naniadm/.config/systemd/user/deadlock-turniere.service`, `/home/naniadm/.config/systemd/user/deadlock-turniere.service.d/30-rust-cutover.conf`)

`STEAM_BRIDGE_DB_PATH` zeigt auf eine externe SQLite-Datei des Steam-Workers. Wenn der Pfad leer ist oder die Datei fehlt, liefert `SteamBridge::open()` `Ok(None)` und der MatchManager läuft ohne Steam-Tasks weiter. (`rust/crates/turnier-config/src/lib.rs`, `rust/crates/turnier-match/src/steam_bridge.rs`, `rust/crates/turnier-api/src/state.rs`)

Das verzögerte Löschen von Discord-Match-Channels lebt im Prozess. Ein Neustart während der Wartezeit verliert diesen geplanten Löschvorgang. (`rust/crates/turnier-discord/src/notifier.rs`, `rust/crates/turnier-match/src/result.rs`)

Reminder nutzen ein 5-Minuten-Fenster und Dedupe-Tabellen. Verpasste Fenster nach längerem Ausfall werden nicht nachgeholt. (`rust/crates/turnier-scheduler/src/reminders.rs`)
