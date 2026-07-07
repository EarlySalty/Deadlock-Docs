---
title: "Cross-System-Betrieb - Übersicht"
tags: [internal, betrieb, systemd]
stand: 2026-07-07
quelle: "systemd-User-Units, Deadlock-Repos, Caddy"
---
# Cross-System-Betrieb - Übersicht

Welche Deadlock-Dienste systemd startet, wo ihr Code liegt und welche lokalen Ports sie belegen.
Die Tabelle beschreibt den Rust-Zielpfad; Legacy-Python steht nur dort, wo der Service noch als Fallback existiert.
Ausgeschlossene Repos und Dienste stehen nicht in der Landkarte.

## Dienst-Landkarte

| systemd-User-Service | Repo | Startpfad | Binary oder Prozess | Lokale Ports | Beleg |
|---|---|---|---|---|---|
| `deadlock-bot-rust.service` | `Deadlock-Bots` | `scripts/run_dl_bot_service.sh` | `rust/target/release/dl-bot` | `8770` Master-Broker, `8899` Changelog, `8901` Server-Sync, `8890` MCP | `systemctl --user cat deadlock-bot-rust.service`; `Deadlock-Bots/scripts/run_dl_bot_service.sh`; `Deadlock-Bots/rust/bin/dl-bot/src/main.rs` |
| `deadlock-web-rust.service` | `Deadlock-Bots` | `scripts/run_dl_web_service.sh` | `rust/target/release/dl-web` | `8766` Dashboard, `8768` Aktivität, `8771` Builds/Tierlist | `systemctl --user cat deadlock-web-rust.service`; `Deadlock-Bots/scripts/run_dl_web_service.sh`; `Deadlock-Bots/rust/bin/dl-web/src/main.rs` |
| `dl-knowledge.service` | `Deadlock-Bots` | `scripts/run_dl_knowledge_service.sh` | `rust/target/release/dl-knowledge` | `8896` FAQ-Wissensdienst | `systemctl --user cat dl-knowledge.service`; `Deadlock-Bots/scripts/run_dl_knowledge_service.sh`; `Deadlock-Bots/rust/bin/dl-knowledge/src/main.rs` |
| `deadlock-twitch-invite-sync.service` | `Deadlock-Bots` | `scripts/run_twitch_invite_sync.sh` | `rust/target/release/dl-twitch-invite-sync` | kein Listener; nutzt `127.0.0.1:8776` als Upstream | `systemctl --user cat deadlock-twitch-invite-sync.service`; `Deadlock-Bots/scripts/run_twitch_invite_sync.sh` |
| `dl-repostats.service` | `Deadlock-Bots` | direkte Unit | `rust/target/release/dl-repostats` | kein Listener; schreibt `data/repo_activity.json` | `systemctl --user cat dl-repostats.service`; `Deadlock-Bots/rust/Cargo.toml` |
| `steam-core.service` | `Deadlock-Steam-Bot` | `rust/deploy/run-steam-core.sh` | `rust/target/release/steam-core` | `8782` Steam-Core-API | `systemctl --user cat steam-core.service`; `Deadlock-Steam-Bot/rust/deploy/run-steam-core.sh`; `Deadlock-Steam-Bot/rust/crates/steam-core/src/main.rs` |
| `steam-bot.service` | `Deadlock-Steam-Bot` | `rust/deploy/run-steam-bot.sh` | `rust/target/release/steam-bot` | `8783` Steam-Link/API | `systemctl --user cat steam-bot.service`; `Deadlock-Steam-Bot/rust/deploy/run-steam-bot.sh`; `Deadlock-Steam-Bot/rust/crates/steam-bot/src/main.rs` |
| `deadlock-twitch-bot-rust.service` | `Deadlock-Twitch-Bot` | `rust/scripts/run_tb_bot_service.sh` | `rust/target/release/tb-bot` | `8776` interne API, `8786` EventSub-Webhook | `systemctl --user cat deadlock-twitch-bot-rust.service`; `Deadlock-Twitch-Bot/rust/scripts/run_tb_bot_service.sh`; `Deadlock-Twitch-Bot/rust/bin/tb-bot/src/main.rs` |
| `deadlock-twitch-dashboard-rust.service` | `Deadlock-Twitch-Bot` | `rust/scripts/run_tb_dashboard_service.sh` | `rust/target/release/tb-dashboard` | `8769` Dashboard/API/Legal | `systemctl --user cat deadlock-twitch-dashboard-rust.service`; `Deadlock-Twitch-Bot/rust/scripts/run_tb_dashboard_service.sh`; `Deadlock-Twitch-Bot/rust/bin/tb-dashboard/src/main.rs` |
| `deadlock-twitch-stream-coaching-watch.service` | `Deadlock-Twitch-Bot` | `scripts/run_stream_coaching_watch.sh` | Script-Prozess | kein dokumentierter HTTP-Listener | `systemctl --user cat deadlock-twitch-stream-coaching-watch.service`; `Deadlock-Twitch-Bot/scripts/run_stream_coaching_watch.sh` |
| `deadlock-turniere.service` | `Deadlock-Turniere` | `scripts/run_turniere_backend_rust.sh` | `rust/target/release/turnier-bot` | `8900` Turnier-API | `systemctl --user cat deadlock-turniere.service`; `Deadlock-Turniere/scripts/run_turniere_backend_rust.sh`; `Deadlock-Turniere/rust/crates/turnier-bot/src/main.rs` |
| `deadlock-patchnotes.service` | `Deadlock--Patchnotes-Bot` | `scripts/run_patchnotes_bot.sh` | `main.py` | kein eigener öffentlicher Port | `systemctl --user cat deadlock-patchnotes.service`; `Deadlock--Patchnotes-Bot/scripts/run_patchnotes_bot.sh` |
| `deadlock-website-backend.service` | `Website` | `scripts/run_builds_backend.sh` | `builds/backend-rust/target/release/ddc-website-backend` | `8772` Website-/Coaching-/Patch-API | `systemctl --user cat deadlock-website-backend.service`; `Website/scripts/run_builds_backend.sh`; `Website/builds/backend-rust/src/config.rs` |

## Legacy-Fallbacks

`deadlock-bot.service`, `deadlock-twitch-bot.service` und `deadlock-twitch-dashboard.service` sind Python-Legacy-Units. Sie werden hier nicht als Zielpfad beschrieben: Die Rust-Units und Caddy-Routen belegen die aktuelle Betriebsrichtung, Patchnotes bleibt die bekannte Ausnahme mit Python-Prozess. (`systemctl --user cat deadlock-bot.service`; `systemctl --user cat deadlock-twitch-bot.service`; `systemctl --user cat deadlock-twitch-dashboard.service`)

