---
title: "Turniere — Übersicht"
tags: [internal, deadlock-turniere, übersicht]
stand: 2026-07-07
quelle: Deadlock-Turniere
---
# Turniere — Übersicht

Der Live-Dienst `deadlock-turniere.service` läuft über das Rust-Binary `rust/target/release/turnier-bot`. Die Fachdaten liegen in der zentralen Postgres-DB aus `DEADLOCK_CENTRAL_DSN` und werden im Schema `turnier.*` gelesen und geschrieben. API, Scheduler, Match-Flow, Discord, Steam-Bridge und Automatik kommen aus `rust/crates/*`. (`/home/naniadm/.config/systemd/user/deadlock-turniere.service.d/30-rust-cutover.conf`, `scripts/run_turniere_backend_rust.sh`, `rust/crates/turnier-db/src/pool.rs`)

## Laufzeit

Die komplette User-Unit ersetzt die ursprüngliche `ExecStart`-Zeile im Drop-in `30-rust-cutover.conf`: erst `ExecStart=` leeren, dann `scripts/run_turniere_backend_rust.sh` starten. Der Drop-in liegt unter der User-Unit und ist damit der wirksame Startpfad für `deadlock-turniere.service`. (`/home/naniadm/.config/systemd/user/deadlock-turniere.service`, `/home/naniadm/.config/systemd/user/deadlock-turniere.service.d/30-rust-cutover.conf`)

Der Rust-Launcher lädt die lokale Turniere-Config, optional die Infisical-Config und bei systemd-Credentials die Datei `infisical-token`. Danach exportiert er Secrets über den Infisical-Helfer, verlangt `DEADLOCK_CENTRAL_DSN`, setzt `DISCORD_BOT_TOKEN` aus `DISCORD_TOKEN` nach und exec't `rust/target/release/turnier-bot`. (`scripts/run_turniere_backend_rust.sh`)

`turnier-bot` lädt `Config`, legt das Avatar-Verzeichnis an, öffnet den zentralen Pool, baut `AppState`, erzeugt den Scheduler und merged den axum-Router. Ohne `--check` bindet es auf `BACKEND_HOST:BACKEND_PORT`; mit `--check` baut es State, Scheduler und Router und beendet sich ohne Listener. (`rust/crates/turnier-bot/src/main.rs`, `rust/crates/turnier-config/src/lib.rs`)

## Aufbau

Der Rust-Code ist ein Cargo-Workspace mit `members = ["crates/*"]`. Das Binary-Paket heißt `turnier-bot`; sein Manifest hängt die Crates `turnier-config`, `turnier-db`, `turnier-discord`, `turnier-match`, `turnier-scheduler` und `turnier-api` an die Composition-Root. (`rust/Cargo.toml`, `rust/crates/turnier-bot/Cargo.toml`)

`AppState` hält den Postgres-Pool, Config, Rollen-Sets, OAuth-Client, MatchManager, RankResolver und DiscordNotifier. Beim Start öffnet er die Steam-Bridge optional; fehlt die Bridge-DB, läuft der Dienst weiter und Steam-Tasks sind deaktiviert. (`rust/crates/turnier-api/src/state.rs`, `rust/crates/turnier-match/src/steam_bridge.rs`)

Der HTTP-Router liefert direkt `/api/health` und `/api/me` und merged Auth, Account, Public, Admin, Operations, Consent, Leaderboard, Draft und Test-Modus. CORS kommt aus `Config::cors_allowed_origins()`, der Host-Guard aus `Config::allowed_hosts()`. (`rust/crates/turnier-api/src/app.rs`, `rust/crates/turnier-config/src/lib.rs`)

## Daten und Effekte

`turnier_db::connect_central()` baut den Pool aus `DEADLOCK_CENTRAL_DSN`. Produktive Migrationen laufen nicht im Turnier-Dienst; `run_migrations()` ist absichtlich ein No-op und verweist auf zentrale Migrationen. (`rust/crates/turnier-db/src/pool.rs`)

Rust-SQL nutzt voll qualifizierte Tabellen im Schema `turnier`, zum Beispiel `turnier.tournaments`, `turnier.bracket_matches`, `turnier.group_matches`, `turnier.sessions`, `turnier.rank_cache` und `turnier.tournament_presets`. (`rust/crates/turnier-match/src/repo.rs`, `rust/crates/turnier-auth/src/session.rs`, `rust/crates/turnier-automatik/src/presets.rs`)

Discord läuft über den Master-Broker mit `X-Internal-Token`. Steam-Lobbys laufen über die externe SQLite-Queue `steam_tasks` in `STEAM_BRIDGE_DB_PATH`; diese Queue gehört dem Steam-Worker, nicht der Turnier-Fachdatenbank. (`rust/crates/turnier-discord/src/broker.rs`, `rust/crates/turnier-match/src/steam_bridge.rs`)
