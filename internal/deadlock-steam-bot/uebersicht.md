---
title: "Deadlock Steam-Bot Übersicht"
tags: [internal, steam, bot]
stand: 2026-07-07
quelle: "Deadlock-Steam-Bot"
---
# Deadlock Steam-Bot Übersicht

Der Steam-Bot läuft als Rust-Workspace mit zwei Service-Binaries. `steam-core` hält die Steam-Session, verbindet den Deadlock-Game-Coordinator, bedient die interne Task-API und verarbeitet `steam.steam_tasks`. `steam-bot` öffnet dieselbe zentrale Postgres-DB, startet Discord-Transport, Flow-Scheduler und die Web-Routen für Link, Rang, Ko-fi und Events. (`rust/crates/steam-core/src/main.rs`, `rust/crates/steam-bot/src/main.rs`)

Der Workspace bindet `deadlock-proto`, `steam-domain`, `api-contract`, `steam-persistence`, `steam-gc`, `steam-core`, `steam-discord`, `steam-web`, `steam-flows` und `steam-bot` ein. `dl-central-db` kommt als Workspace-Abhängigkeit aus dem Schwester-Repo und liefert DSN, Pool und Migrationen. (`rust/Cargo.toml`)

## Binaries

| Binary | Aufgabe | Beleg |
|---|---|---|
| `steam-core` | Steam-Login, GC-Verbindung, Task-Loop, HTTP-API, Presence-Listener und Heartbeat. | `rust/crates/steam-core/Cargo.toml`, `rust/crates/steam-core/src/main.rs` |
| `steam-bot` | Discord-Flows, Web-Routen, Scheduler, Ko-fi-Webhook und Broker-Calls. | `rust/crates/steam-bot/Cargo.toml`, `rust/crates/steam-bot/src/main.rs` |

## systemd

`steam-core.service` startet `rust/deploy/run-steam-core.sh` im WorkingDirectory `~/Documents/Deadlock-Steam-Bot/rust`. Die Live-Unit nutzt `Restart=on-failure`, `RestartSec=5`, `TimeoutStopSec=20`, lädt `infisical-token` per Drop-in und setzt `STEAM_PRESENCE_ENABLED=1` per Drop-in (`/home/naniadm/.config/systemd/user/steam-core.service`, `/home/naniadm/.config/systemd/user/steam-core.service.d/20-creds.conf`, `/home/naniadm/.config/systemd/user/steam-core.service.d/30-presence.conf`).

`steam-bot.service` startet `rust/deploy/run-steam-bot.sh`, hat `After=network-online.target steam-core.service`, setzt `STEAM_BOT_API_ADDR=127.0.0.1:8783` und `STEAM_BOT_DISCORD=broker`, lädt `infisical-token` per Drop-in und setzt Friend-Limit-Reservierung per Drop-in (`/home/naniadm/.config/systemd/user/steam-bot.service`, `/home/naniadm/.config/systemd/user/steam-bot.service.d/20-creds.conf`, `/home/naniadm/.config/systemd/user/steam-bot.service.d/phase0-friend-limit.conf`).

Beide Wrapper lesen Infisical-Verbindungsdaten, übernehmen optional `CREDENTIALS_DIRECTORY/infisical-token`, laden Secrets per `Deadlock-Bots/scripts/export_infisical_env.py --format shell` und ersetzen die Shell per `exec` durch das Rust-Binary. (`rust/deploy/run-steam-core.sh`, `rust/deploy/run-steam-bot.sh`)

## Ports

| Port | Dienst | Mechanismus | Beleg |
|---|---|---|---|
| `127.0.0.1:8782` | `steam-core` | Default für `STEAM_CORE_API_ADDR`; die API bietet `/health`, `/status`, `/friends`, `POST /tasks` und `GET /tasks/{id}`. | `rust/crates/steam-core/src/config.rs`, `rust/crates/steam-core/src/api/mod.rs` |
| `127.0.0.1:8783` | `steam-bot` | Default für `STEAM_BOT_API_ADDR`; der Web-Layer bietet `/health`, `/link/*`, `/rank`, `/player-*`, `/kofi/*` und `/events/discord`. | `rust/crates/steam-bot/src/main.rs`, `rust/crates/steam-web/src/lib.rs`, `rust/crates/steam-web/src/routes/mod.rs` |
| `127.0.0.1:8770` | Master-Broker | `steam-bot` nutzt diesen Default für Discord-Aktionen, wenn `STEAM_BROKER_URL` fehlt. | `rust/crates/steam-discord/src/broker.rs` |
| `127.0.0.1:8766` | Discord-OAuth-API des Master-Bots | Der Link-Flow delegiert Discord-OAuth an diese interne API, wenn `DISCORD_OAUTH_INTERNAL_API_BASE_URL` fehlt. | `rust/crates/steam-flows/src/link.rs` |

## Funktionsumfang

Der Account-Link-Flow erzeugt Launch-Tokens, baut Steam-OpenID-Redirects, verifiziert den Steam-Callback, schreibt `core.steam_links` und reiht `AUTH_SEND_FRIEND_REQUEST` ein. (`rust/crates/steam-flows/src/link.rs`, `rust/crates/steam-web/src/routes/link.rs`)

Der Friend-Sync pflegt Freundschaftsanfragen, Rollen-Cleanup und Reconcile-Zustand über `steam.steam_friend_requests`, `steam.steam_friend_check_cache`, `steam.steam_friendship_miss_tracker` und `steam.steam_cleanup_poll_state`. (`rust/crates/steam-flows/src/friend_sync.rs`, `rust/crates/steam-persistence/src/friends.rs`, `rust/crates/steam-persistence/src/friend_cache.rs`, `rust/crates/steam-persistence/src/miss_tracker.rs`)

Der Rank-Flow liest verifizierte Steam-Links, fragt Profilkarten und Account-Stats über GC-Tasks ab, schreibt Snapshots und aktualisiert Discord-Rollen über den Broker. (`rust/crates/steam-flows/src/rank.rs`, `rust/crates/steam-web/src/routes/rank.rs`, `rust/crates/steam-persistence/src/rank.rs`)

Der Playtest-Invite-Funnel nutzt `steam.steam_beta_invites`, Ticket-Tabellen, Friendship-Auto-Poll und Ko-fi-Zahlungen; `steam-bot` startet dafür Dispatcher, Friendship-Poller und Ticket-Cleanup. (`rust/crates/steam-bot/src/main.rs`, `rust/crates/steam-flows/src/betainvite.rs`, `rust/crates/steam-flows/src/supporter.rs`)

Der Lobby-Flow läuft über `steam.steam_tasks` und die GC-Task-Typen `GC_CREATE_CUSTOM_LOBBY`, `GC_LOBBY_*` und `GC_GET_MATCH_RESULT`. (`rust/crates/steam-core/src/task/handlers/lobby.rs`, `rust/crates/steam-core/src/task/lanes.rs`)
