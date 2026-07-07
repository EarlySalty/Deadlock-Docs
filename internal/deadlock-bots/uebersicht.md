---
title: "Deadlock-Bots Übersicht"
tags: [deadlock-bots, intern, rust]
stand: 2026-07-07
quelle: Deadlock-Bots
---
# Deadlock-Bots Übersicht

`Deadlock-Bots` bündelt Discord-Gateway-Arbeit, interne Discord-REST-Aktionen, öffentliche Web-APIs, Dashboard-Routen, zentrale Postgres-Migrationen und kleine Sync-Collector. Der Rust-Teil liegt unter `rust/` und nutzt einen Workspace mit Domain-Crates und Binaries unter `rust/bin/` (`rust/Cargo.toml`, `rust/bin/dl-bot/src/main.rs`, `rust/bin/dl-web/src/main.rs`).

Der Prozess `dl-bot` startet auch ohne Gateway mehrere lokale HTTP-Server: Master-Broker, Changelog-Empfänger, Server-Sync und MCP-Connector. Discord-Gateway-Arbeit läuft erst, wenn `DL_BOT_GATEWAY=1` gesetzt ist (`rust/bin/dl-bot/src/main.rs`, `scripts/run_dl_bot_service.sh`).

## Binaries

| Binary | Aufgabe | Beleg |
|---|---|---|
| `dl-bot` | Discord-Prozess mit Broker, Changelog-API, Server-Sync, MCP-Connector und optionalem Gateway. | `rust/bin/dl-bot/Cargo.toml`, `rust/bin/dl-bot/src/main.rs` |
| `dl-web` | Ein Prozess für Dashboard, Public-Stats und Tierlist; alle drei binden eigene Ports. | `rust/bin/dl-web/Cargo.toml`, `rust/bin/dl-web/src/main.rs` |
| `dl-central-migrate` | Wendet `rust/crates/dl-central-db/migrations` auf die zentrale Postgres-DB an. | `rust/bin/dl-central-migrate/src/main.rs` |
| `dl-central-sync` | Snapshotet bekannte SQLite-Quellen, lädt ETL-Ledger und schreibt in die zentrale Postgres-DB. | `rust/bin/dl-central-sync/src/main.rs`, `rust/crates/dl-central-etl/src/lib.rs` |
| `dl-twitch-invite-sync` | Holt Streamer-Invite-Zuordnungen aus der internen Twitch-API und korrigiert Join-Metadaten auf Bucket `twitch`. | `rust/bin/dl-twitch-invite-sync/src/main.rs` |
| `dl-repostats` | Sammelt Repo-Aktivität in ein JSON-Artefakt für das Dashboard. | `rust/bin/dl-repostats/src/main.rs`, `service/systemd/dl-repostats.service` |
| `dl-mcp` | Eigenständiger MCP-Server für Discord-REST-Tools. Er liegt unter `rust/bin/`, ist aber nicht in den Workspace-`members` eingetragen. | `rust/bin/dl-mcp/src/main.rs`, `rust/bin/dl-mcp/Cargo.toml`, `rust/Cargo.toml` |

`dl-bot` enthält zusätzlich das Cargo-Nebenbinary `seed_scrim`; es importiert ein Seed-Roster-JSON in die zentrale DB. Es ist kein eigener Ordner unter `rust/bin/` (`rust/bin/dl-bot/src/bin/seed_scrim.rs`).

## Ports

| Port | Prozess | Bindung | Beleg |
|---|---|---|---|
| `8766` | `dl-web` | Dashboard, Host aus `DASHBOARD_HOST`, Default `127.0.0.1`. | `rust/crates/dl-core/src/config.rs`, `rust/bin/dl-web/src/main.rs` |
| `8768` | `dl-web` | Public-Stats, Host aus `PUBLIC_STATS_HOST`, Default `127.0.0.1`. | `rust/crates/dl-core/src/config.rs`, `rust/crates/dl-webcore/src/config.rs`, `rust/bin/dl-web/src/main.rs` |
| `8770` | `dl-bot` | Master-Broker, Host aus `MASTER_BROKER_HOST`, Default `127.0.0.1`. | `rust/crates/dl-core/src/config.rs`, `rust/bin/dl-bot/src/main.rs` |
| `8771` | `dl-web` | Tierlist, Host aus `TIERLIST_PUBLIC_HOST`, Default `127.0.0.1`. | `rust/crates/dl-core/src/config.rs`, `rust/crates/dl-webcore/src/config.rs`, `rust/bin/dl-web/src/main.rs` |
| `8890` | `dl-bot` oder `dl-mcp` | MCP-Connector im Bot nutzt `MCP_CONNECTOR_PORT`; Standalone-`dl-mcp` nutzt `DL_MCP_PORT`. | `rust/bin/dl-bot/src/mcp.rs`, `rust/bin/dl-mcp/src/main.rs` |
| `8899` | `dl-bot` | Changelog-Empfänger, immer loopback. | `rust/crates/dl-core/src/config.rs`, `rust/bin/dl-bot/src/main.rs` |
| `8901` | `dl-bot` | Server-Sync-Orchestrator, loopback plus interner Token. | `rust/bin/dl-bot/src/serversync.rs`, `rust/bin/dl-bot/src/main.rs` |
| `8776` | Schwester-Bot | Default-Basis der Twitch-internen API. | `rust/crates/dl-bridges/src/twitch.rs`, `rust/bin/dl-twitch-invite-sync/src/main.rs` |
| `8783` | Schwester-Bot | Default-Basis der Steam-Bot-API. | `rust/crates/dl-bridges/src/steam.rs` |
| `8772` | Website-Backend | Wrapper setzt `WEBSITE_API_BASE` auf den lokalen `/api`-Pfad. | `scripts/run_dl_bot_service.sh`, `rust/crates/dl-community/src/coaching.rs` |

## Live-User-Services

`deadlock-bot-rust.service` startet im WorkingDirectory `/home/naniadm/Documents/Deadlock-Bots` den Wrapper `scripts/run_dl_bot_service.sh`; die gelesene Unit hat `Conflicts=deadlock-bot.service` und ein Drop-in für `OWNER_ID` (`/home/naniadm/.config/systemd/user/deadlock-bot-rust.service`, `/home/naniadm/.config/systemd/user/deadlock-bot-rust.service.d/owner.conf`, `scripts/run_dl_bot_service.sh`).

`deadlock-web-rust.service` startet im selben WorkingDirectory den Wrapper `scripts/run_dl_web_service.sh` und bindet darüber Dashboard, Public-Stats und Tierlist (`/home/naniadm/.config/systemd/user/deadlock-web-rust.service`, `scripts/run_dl_web_service.sh`, `rust/bin/dl-web/src/main.rs`).

`deadlock-twitch-invite-sync.timer` startet alle 15 Minuten den Oneshot-Service `deadlock-twitch-invite-sync.service`; der Service ruft `scripts/run_twitch_invite_sync.sh` auf und führt danach `rust/target/release/dl-twitch-invite-sync` aus (`/home/naniadm/.config/systemd/user/deadlock-twitch-invite-sync.timer`, `/home/naniadm/.config/systemd/user/deadlock-twitch-invite-sync.service`, `scripts/run_twitch_invite_sync.sh`).

`dl-repostats.timer` startet `dl-repostats.service` 3 Minuten nach Boot und danach alle 2 Stunden. Die Live-Unit führt direkt `rust/target/release/dl-repostats` aus (`/home/naniadm/.config/systemd/user/dl-repostats.timer`, `/home/naniadm/.config/systemd/user/dl-repostats.service`).
