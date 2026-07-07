---
title: "Cross-System-Betrieb - Datenbank"
tags: [internal, betrieb, datenbank, postgres]
stand: 2026-07-07
quelle: "Deadlock-Bots zentrale DB, Rust-Wrapper, Service-Units"
---
# Cross-System-Betrieb - Datenbank

Die zentrale Deadlock-Datenbank ist Postgres/TimescaleDB auf Loopback.
Der gemeinsame Rust-Pfad liest die DSN über `DEADLOCK_CENTRAL_DSN`.
Migrationen gehören dem Deadlock-Bots-Workspace.

## Zentrale Postgres

| Baustein | Wert | Beleg |
|---|---|---|
| Container | `deadlock-central-postgres` aus `timescale/timescaledb:2.17.2-pg16` | `Deadlock-Bots/rust/infra/central-db/docker-compose.yml` |
| Bind | `127.0.0.1:5434` auf Container-Port `5432` | `Deadlock-Bots/rust/infra/central-db/docker-compose.yml` |
| Datenbankname | `deadlock` | `Deadlock-Bots/rust/infra/central-db/docker-compose.yml` |
| Startskript | `up.sh` verlangt `DEADLOCK_CENTRAL_DSN`, leitet daraus nur `POSTGRES_PASSWORD` für Docker ab und startet Compose. | `Deadlock-Bots/rust/infra/central-db/up.sh` |
| optionale System-Unit-Vorlage | `deadlock-central-db.service` startet und stoppt denselben Compose-Stack; Klartext-Secrets sind dort ausdrücklich nicht vorgesehen. | `Deadlock-Bots/rust/infra/central-db/deadlock-central-db.service` |

## DSN und Migrationen

`dl-central-db` definiert `DEADLOCK_CENTRAL_DSN` als einzige zentrale DSN-Env und baut daraus den `PgPool`. `dl-central-migrate` ruft `sqlx::migrate!` auf dem Migrationsverzeichnis `crates/dl-central-db/migrations` auf. (`Deadlock-Bots/rust/crates/dl-central-db/src/pool.rs`; `Deadlock-Bots/rust/bin/dl-central-migrate/src/main.rs`)

Der Migrationsweg ist:

```bash
cd /home/naniadm/Documents/Deadlock-Bots/rust
cargo run -p dl-central-migrate
```

`central_test_db.sh` nutzt denselben Binary-Pfad gegen einen Wegwerfcontainer und setzt dort `DEADLOCK_CENTRAL_DSN` nur für den Testprozess. (`Deadlock-Bots/rust/scripts/central_test_db.sh`)

## Schemata

| Schema | Zweck im Betrieb | Beleg |
|---|---|---|
| `core` | Benutzer und Steam-Links als gemeinsame Identitätsschicht. | `Deadlock-Bots/rust/crates/dl-central-db/migrations/0001_core_and_schemas.sql` |
| `coaching` | Coaching-Plattform und Website-Coaching. | `Deadlock-Bots/rust/crates/dl-central-db/migrations/0001_core_and_schemas.sql`; `Website/builds/backend-rust/src/routes/platform.rs` |
| `scrim` | Scrim-/Match-Orchestrierung und Website-Scrim-Routen. | `Deadlock-Bots/rust/crates/dl-central-db/migrations/0001_core_and_schemas.sql`; `Website/builds/backend-rust/src/routes/scrim.rs` |
| `steam` | Steam-Links, Ränge, Friend-Requests und Steam-Tasks. | `Deadlock-Bots/rust/crates/dl-central-db/migrations/0001_core_and_schemas.sql`; `Deadlock-Bots/rust/crates/dl-central-db/migrations/0003_steam.sql`; `Deadlock-Steam-Bot/rust/crates/steam-bot/src/main.rs` |
| `turnier` | Turnier-Backend und Match-Automatik. | `Deadlock-Bots/rust/crates/dl-central-db/migrations/0001_core_and_schemas.sql`; `Deadlock-Bots/rust/crates/dl-central-db/migrations/0009_turnier.sql`; `Deadlock-Turniere/rust/crates/turnier-bot/src/main.rs` |
| `patchnotes` | Patchnotes-Identitäten und Patchnotes-Daten. | `Deadlock-Bots/rust/crates/dl-central-db/migrations/0001_core_and_schemas.sql`; `Deadlock-Bots/rust/crates/dl-central-db/migrations/0014_patchnotes_identity_sequences.sql`; `Deadlock--Patchnotes-Bot/scripts/run_patchnotes_bot.sh` |
| `activity` | Aktivitätsdaten, Journey und Live-Player-State. | `Deadlock-Bots/rust/crates/dl-central-db/migrations/0001_core_and_schemas.sql`; `Deadlock-Bots/rust/crates/dl-central-db/migrations/0010_activity_moderation_content_patchnotes.sql` |
| `voice`, `tierlist`, `moderation`, `bot`, `clips`, `content` | Bot-Funktionen, Voice, Tierlist, Moderation, Clips und Content. | `Deadlock-Bots/rust/crates/dl-central-db/migrations/0002_sp1_schemas_and_core.sql`; `Deadlock-Bots/rust/crates/dl-central-db/migrations/0008_clips.sql` |
| `server_config` | Server-Konfiguration aus dem Rust-Bot. | `Deadlock-Bots/rust/crates/dl-central-db/migrations/2026070210_server_config_schema.sql` |

## Dienstbindung

Deadlock-Bots, Steam, Turniere, Patchnotes und Website starten nicht sinnvoll ohne zentrale DSN im jeweiligen Rust- oder Wrapper-Pfad. Twitch hat einen separaten Analytics-Postgres-Pfad über `TWITCH_ANALYTICS_DSN` und eigene Rust-Migrationen; das ist kein `DEADLOCK_CENTRAL_DSN`-Pfad. (`Deadlock-Bots/rust/bin/dl-web/src/main.rs`; `Deadlock-Steam-Bot/rust/crates/steam-core/src/main.rs`; `Deadlock-Turniere/scripts/run_turniere_backend_rust.sh`; `Website/scripts/run_builds_backend.sh`; `Deadlock-Twitch-Bot/rust/bin/tb-dashboard/src/main.rs`)

