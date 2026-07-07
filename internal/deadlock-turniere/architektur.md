---
title: "Turniere — Architektur"
tags: [internal, deadlock-turniere, architektur]
stand: 2026-07-07
quelle: Deadlock-Turniere
---
# Turniere — Architektur

Der Dienst ist Rust-first: systemd startet den Rust-Launcher, der `turnier-bot` exec't. `turnier-bot` ist die Composition-Root für Config, zentrale Postgres-DB, AppState, Scheduler und axum-API. (`/home/naniadm/.config/systemd/user/deadlock-turniere.service.d/30-rust-cutover.conf`, `scripts/run_turniere_backend_rust.sh`, `rust/crates/turnier-bot/src/main.rs`)

## Live-Pfad

Die wirksame User-Unit muss komplett gelesen werden: die Basisdatei enthält eine frühere `ExecStart`-Zeile, aber das Drop-in `30-rust-cutover.conf` leert `ExecStart` und setzt den Start auf `scripts/run_turniere_backend_rust.sh`. Damit ist der belegte Live-Pfad am 2026-07-07 der Rust-Launcher. (`/home/naniadm/.config/systemd/user/deadlock-turniere.service`, `/home/naniadm/.config/systemd/user/deadlock-turniere.service.d/30-rust-cutover.conf`)

Der Launcher lädt lokale Config und Infisical-Werte, verlangt `INFISICAL_SERVICE_TOKEN` und `DEADLOCK_CENTRAL_DSN` und startet dann `rust/target/release/turnier-bot`. Der Launcher schreibt keine Secrets aus und beendet sich vor dem Start, wenn die zentrale DSN fehlt. (`scripts/run_turniere_backend_rust.sh`)

`turnier-bot` initialisiert Tracing, lädt `Config::from_env()`, ruft `ensure_dirs()`, öffnet `turnier_db::connect_central()`, baut `AppState::build()`, erzeugt `Scheduler::new()` und merged `build_router(state)`. Danach startet es den Scheduler per `tokio::spawn(start_scheduler(...))` und serviert axum über einen `TcpListener`. (`rust/crates/turnier-bot/src/main.rs`)

## Crates

Der Workspace hängt alle Crates unter `rust/crates/*` ein. Die fachliche Aufteilung liegt in `turnier-api`, `turnier-auth`, `turnier-automatik`, `turnier-config`, `turnier-core`, `turnier-db`, `turnier-discord`, `turnier-draft`, `turnier-engine`, `turnier-match`, `turnier-scheduler` und `turnier-steam`. (`rust/Cargo.toml`, `rust/crates/turnier-bot/Cargo.toml`)

`turnier-config` löst Env und Secret-Dateien auf und hält die zur Laufzeit verwendeten Werte. `DEADLOCK_CENTRAL_DSN` wird nicht in `Config` gespeichert, sondern von `turnier_db::connect_central()` direkt gelesen. (`rust/crates/turnier-config/src/lib.rs`, `rust/crates/turnier-db/src/pool.rs`)

`turnier-api` hält den axum-Router und den `AppState`. Der State bündelt Pool, Config, RBAC, OAuth, MatchManager, RankResolver und DiscordNotifier; diese Handles werden pro Request billig geklont. (`rust/crates/turnier-api/src/app.rs`, `rust/crates/turnier-api/src/state.rs`)

## Request- und Job-Flow

Die API merged öffentliche Turnier- und Team-Routen, Admin-Routen, Operations, Consent/Profile, Leaderboard, Draft, Auth, Account und optional Test-Modus. Der Host-Guard prüft den `Host`-Header gegen `Config::allowed_hosts()`, CORS erlaubt den lokalen Vite-Origin und die konfigurierte Frontend-URL. (`rust/crates/turnier-api/src/app.rs`, `rust/crates/turnier-config/src/lib.rs`)

Auth läuft über delegierten Discord-OAuth beim Deadlock-Bots-Service. `/auth/discord/login` holt eine Authorize-URL, `/auth/discord/complete` löst `state_id` ein, legt eine opake Session in `turnier.sessions` an und setzt `session_token`; Requests lesen zuerst `Authorization: Bearer`, danach das Cookie. (`rust/crates/turnier-api/src/auth.rs`, `rust/crates/turnier-auth/src/oauth.rs`, `rust/crates/turnier-api/src/extract.rs`)

Der Scheduler lebt im selben Prozess. Er läuft einmal sofort und danach alle 60 Sekunden; pro Tick laufen Phasenwechsel, Registrierungs-Reminder, Start-Reminder und Match-Reminder jeweils fehlertolerant. (`rust/crates/turnier-bot/src/main.rs`, `rust/crates/turnier-scheduler/src/loop_runner.rs`)

Der MatchManager orchestriert Bracket- und Group-Matches. Er schreibt Fachdaten in `turnier.*`, nutzt die Steam-Bridge nur für `steam_tasks`, erstellt Discord-Match-Channels über den Broker und behandelt Discord-Fehler best-effort. (`rust/crates/turnier-match/src/lib.rs`, `rust/crates/turnier-match/src/repo.rs`, `rust/crates/turnier-discord/src/notifier.rs`)

Legacy: der alte Python-Pfad unter `backend/` ist abgelöst, Code liegt noch im Repo. (`/home/naniadm/.config/systemd/user/deadlock-turniere.service.d/30-rust-cutover.conf`, `scripts/run_turniere_backend_rust.sh`)
