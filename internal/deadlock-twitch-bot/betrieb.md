---
title: Deadlock Twitch Bot Betrieb
tags: [internal, deadlock-twitch-bot, betrieb]
stand: 2026-07-07
quelle: Deadlock-Twitch-Bot
---

## Build

- Die Rust-Binaries heißen `tb-bot` und `tb-dashboard`; die systemd-Skripte erwarten sie unter `rust/target/release/`. (rust/bin/tb-bot/Cargo.toml; rust/bin/tb-dashboard/Cargo.toml; rust/scripts/run_tb_bot_service.sh; rust/scripts/run_tb_dashboard_service.sh)
- Der passende Release-Build ist `cargo build --release -p tb-bot -p tb-dashboard` im Rust-Workspace. (rust/Cargo.toml; rust/bin/tb-bot/Cargo.toml; rust/bin/tb-dashboard/Cargo.toml)
- Das Dashboard-Frontend baut mit `npm run build` in `bot/dashboard_v2` nach `bot/analytics/dashboard_v2/dist`. (bot/dashboard_v2/package.json; bot/dashboard_v2/vite.config.ts)
- Die Website baut mit `npm run build` in `website` nach `website/dist`. (website/package.json; website/vite.config.ts; website/scripts/vite-build.mjs)

## Deploy

- `deadlock-twitch-bot-rust.service` nutzt `rust/scripts/run_tb_bot_service.sh` und startet `tb-bot`. (/home/naniadm/.config/systemd/user/deadlock-twitch-bot-rust.service; rust/scripts/run_tb_bot_service.sh)
- `deadlock-twitch-dashboard-rust.service` nutzt `rust/scripts/run_tb_dashboard_service.sh` und startet `tb-dashboard`. (/home/naniadm/.config/systemd/user/deadlock-twitch-dashboard-rust.service; rust/scripts/run_tb_dashboard_service.sh)
- Der Neustart läuft als User-Service über `systemctl --user restart deadlock-twitch-bot-rust.service deadlock-twitch-dashboard-rust.service`. (/home/naniadm/.config/systemd/user/deadlock-twitch-bot-rust.service; /home/naniadm/.config/systemd/user/deadlock-twitch-dashboard-rust.service)
- Beide Rust-Skripte laden Infisical-Konfiguration aus `$HOME/.config/deadlock-twitch-bot/infisical.conf` und bevorzugen Token aus `CREDENTIALS_DIRECTORY`. (rust/scripts/run_tb_bot_service.sh; rust/scripts/run_tb_dashboard_service.sh)
- `tb-dashboard` führt Migrationen aus, wenn `TB_DB_MIGRATE` nicht auf einen deaktivierenden Wert gesetzt ist. (rust/bin/tb-dashboard/src/main.rs)

## Env-Namen

- Datenbank und interne API: `TWITCH_ANALYTICS_DSN`, `TWITCH_ANALYTICS_POOL_MAXSIZE`, `TWITCH_ANALYTICS_POOL_TIMEOUT_SECONDS`, `TWITCH_ANALYTICS_CONNECT_TIMEOUT_SECONDS`, `TWITCH_INTERNAL_API_TOKEN`, `TWITCH_INTERNAL_API_HOST`, `TWITCH_INTERNAL_API_PORT`. (rust/crates/tb-config/src/lib.rs)
- Bot-Port: `PORT`. (rust/bin/tb-bot/src/main.rs; rust/scripts/run_tb_bot_service.sh)
- Dashboard-Port: `DASHBOARD_PORT`, `TWITCH_DASHBOARD_PORT`. (rust/bin/tb-dashboard/src/main.rs; rust/scripts/run_tb_dashboard_service.sh)
- Twitch und EventSub: `TWITCH_CLIENT_ID`, `TWITCH_CLIENT_SECRET`, `TWITCH_WEBHOOK_SECRET`, `TWITCH_EVENTSUB_CALLBACK_URL`, `TWITCH_TARGET_GAME_NAME`, `TWITCH_NOTIFY_CHANNEL_ID`, `TWITCH_ALERT_MENTION`, `TWITCH_LANGUAGE_FILTERS`. (rust/bin/tb-bot/src/main.rs; rust/scripts/run_tb_bot_service.sh)
- Chat und IRC: `TB_CHAT_ENABLED`, `TWITCH_BOT_USER_ID`, `TWITCH_BOT_TOKEN`, `TWITCH_BOT_REFRESH_TOKEN`, `TB_IRC_LURKER_ENABLED`, `TB_CHAT_REVIEW_LOG_DIR`. (rust/bin/tb-bot/src/chat_wiring.rs; rust/bin/tb-bot/src/irc_lurker_wiring.rs; rust/scripts/run_tb_bot_service.sh)
- Verschlüsselung, Sessions und Billing: `DB_MASTER_KEY_V1`, `SESSIONS_ENCRYPTION_KEY`, `STRIPE_WEBHOOK_SECRET`, `STRIPE_SECRET_KEY`, `TWITCH_BILLING_STRIPE_SECRET_KEY`. (rust/bin/tb-bot/src/main.rs; rust/bin/tb-dashboard/src/main.rs; rust/crates/tb-dashboard-api/src/handlers/stripe_webhook.rs)
- Discord und Broker: `MASTER_BROKER_BASE_URL`, `MASTER_BROKER_HOST`, `MASTER_BROKER_PORT`, `MASTER_BROKER_TOKEN`, `MAIN_BOT_INTERNAL_TOKEN`, `STREAMER_GUILD_ID`, `MAIN_GUILD_ID`, `STREAMER_ROLE_ID`. (rust/crates/tb-config/src/lib.rs; rust/bin/tb-bot/src/oauth_followups.rs)
- Frontend- und Content-Pfade: `DASHBOARD_V2_DIST_PATH`, `WEBSITE_DIST_PATH`, `TB_LEGAL_PAGES_PATH`. (rust/crates/tb-dashboard-api/src/handlers/spa.rs; rust/crates/tb-dashboard-api/src/handlers/website.rs; rust/scripts/run_tb_dashboard_service.sh)

## Fallen

- Live läuft das Dashboard auf `8769`, aber der Code-Default bleibt `8765`; das Skript deaktiviert die Split-Runtime-Erzwingung, weil die Härtung sonst noch eine alte Portannahme erzwingt. (rust/scripts/run_tb_dashboard_service.sh; rust/bin/tb-dashboard/src/main.rs)
- `tb-bot` darf nur loopback für die interne API binden; der Router prüft zusätzlich `X-Internal-Token`. (rust/bin/tb-bot/src/main.rs; rust/crates/tb-internal-api/src/lib.rs)
- Der Dashboard-Asset-Vertrag ist `/twitch/dashboard-v2/`, weil Vite diese Base setzt und der Rust-Handler diese Asset-Pfade ausliefert. (bot/dashboard_v2/vite.config.ts; rust/crates/tb-dashboard-api/src/handlers/spa.rs)
- `/analyse` lädt dieselbe SPA wie `/twitch/dashboard-v2/*`, aber der Handler erzwingt Auth und Host-Gate vor der Auslieferung. (rust/crates/tb-dashboard-api/src/handlers/spa.rs)
- UNSICHER: Der Reverse-Proxy-Vertrag ist im gelesenen Code nicht als Caddy- oder Nginx-Datei belegt; codebelegt sind nur die App-Pfade `/twitch/eventsub/callback`, `/internal/twitch/v1`, `/analyse`, `/twitch/dashboard-v2/*` und `/streamer`. (rust/crates/tb-monitoring/src/webhook_receiver.rs; rust/crates/tb-internal-api/src/lib.rs; rust/crates/tb-dashboard-api/src/handlers/spa.rs; rust/crates/tb-dashboard-api/src/handlers/website.rs)
