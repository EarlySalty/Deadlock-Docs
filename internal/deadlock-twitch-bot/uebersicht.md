---
title: Deadlock Twitch Bot Überblick
tags: [internal, deadlock-twitch-bot, übersicht]
stand: 2026-07-07
quelle: Deadlock-Twitch-Bot
---

## Dienste

- `deadlock-twitch-bot-rust.service` startet `rust/scripts/run_tb_bot_service.sh` im Repo-Root und führt danach `rust/target/release/tb-bot` aus. (/home/naniadm/.config/systemd/user/deadlock-twitch-bot-rust.service; rust/scripts/run_tb_bot_service.sh)
- `tb-bot` bindet die interne API auf `127.0.0.1` und nutzt Port `8776`, wenn `PORT` nicht gesetzt ist. (rust/bin/tb-bot/src/main.rs; rust/crates/tb-config/src/lib.rs)
- `deadlock-twitch-dashboard-rust.service` startet `rust/scripts/run_tb_dashboard_service.sh` und führt danach `rust/target/release/tb-dashboard` aus. (/home/naniadm/.config/systemd/user/deadlock-twitch-dashboard-rust.service; rust/scripts/run_tb_dashboard_service.sh)
- Das Dashboard-Skript setzt `DASHBOARD_PORT=8769`, obwohl der Code ohne Env-Wert auf `8765` fällt. (rust/scripts/run_tb_dashboard_service.sh; rust/bin/tb-dashboard/src/main.rs)

## Hauptpfade

- EventSub erreicht den Rust-Bot über `/twitch/eventsub/callback`; der Receiver prüft die Twitch-HMAC-Signatur vor der Verarbeitung. (rust/crates/tb-monitoring/src/webhook_receiver.rs)
- Die interne API liegt unter `/internal/twitch/v1` und verlangt `X-Internal-Token` plus Loopback-Zugriff. (rust/crates/tb-internal-api/src/lib.rs)
- Das Dashboard liefert `/analyse`, `/twitch/dashboard`, `/twitch/verwaltung`, `/twitch/pricing` und Assets unter `/twitch/dashboard-v2/*`. (rust/crates/tb-dashboard-api/src/lib.rs; rust/crates/tb-dashboard-api/src/handlers/spa.rs)
- Die öffentliche Website liegt unter `/streamer`; `/website` leitet auf `/streamer` um. (rust/crates/tb-dashboard-api/src/handlers/website.rs)

## Zuständigkeiten

- `tb-bot` baut Helix, EventSub, Monitoring, Chat, Raid, Knowledge, Social-Media, Analytics und die interne API zusammen. (rust/bin/tb-bot/src/main.rs; rust/bin/tb-bot/Cargo.toml)
- `tb-dashboard` baut die Dashboard-API, Auth-Flüsse, Affiliate-Flüsse, Billing, Legal-Seiten, Website-Auslieferung und die SPA-Auslieferung zusammen. (rust/bin/tb-dashboard/src/main.rs; rust/bin/tb-dashboard/Cargo.toml; rust/crates/tb-dashboard-api/src/lib.rs)
- Beide Rust-Dienste nutzen PostgreSQL über `TWITCH_ANALYTICS_DSN`; die Pool-Konfiguration kommt aus `tb-config` und `tb-db`. (rust/crates/tb-config/src/lib.rs; rust/crates/tb-db/src/pool.rs)
- Das Dashboard führt die eingebetteten Rust-Migrationen beim Start aus, wenn `TB_DB_MIGRATE` nicht deaktiviert ist. (rust/bin/tb-dashboard/src/main.rs; rust/crates/tb-db/src/migrate.rs)
