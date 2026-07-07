---
title: "Deadlock-Bots Betrieb"
tags: [deadlock-bots, intern, betrieb]
stand: 2026-07-07
quelle: Deadlock-Bots
---
# Betrieb

Build und Checks laufen über `rust/scripts/check.sh`: `cargo fmt --all --check`, `cargo clippy --workspace --all-targets -- -D warnings` und `cargo test --workspace`. Zentrale DB-Integrationstests laufen über `rust/scripts/central_test_db.sh`; das Skript startet einen Timescale-Testcontainer, setzt `CENTRAL_TEST_DSN`, spiegelt ihn nach `DEADLOCK_CENTRAL_DSN` und führt `dl-central-migrate` aus (`rust/scripts/check.sh`, `rust/scripts/central_test_db.sh`).

## Startpfade

`scripts/run_dl_bot_service.sh` lädt nicht-geheime Infisical-Verbindungsparameter aus `$HOME/.config/deadlock-bots/infisical.conf`, liest den Bootstrap-Token aus systemd-Credentials und injiziert Secrets über `scripts/export_infisical_env.py`. Danach setzt es unter anderem `DL_BOT_GATEWAY`, `DL_ENABLE_PRESENCE_INTENT`, `DL_BOT_COMMAND_SYNC`, `WEBSITE_API_BASE`, `AI_MODERATOR_ENABLE`, `MODERATION_ENFORCE`, LFG-Forum-Variablen und startet `rust/target/release/dl-bot` (`scripts/run_dl_bot_service.sh`).

`scripts/run_dl_web_service.sh` nutzt denselben Infisical-Ladepfad und startet `rust/target/release/dl-web`. Der Code bindet Dashboard, Public-Stats und Tierlist; er bindet keinen Turnier-Server (`scripts/run_dl_web_service.sh`, `rust/bin/dl-web/src/main.rs`).

`scripts/run_twitch_invite_sync.sh` lädt Infisical, setzt `TWITCH_BOT_API_BASE` auf `http://127.0.0.1:8776` und startet `rust/target/release/dl-twitch-invite-sync`. Das Binary braucht zusätzlich `TWITCH_INTERNAL_API_TOKEN` und `DEADLOCK_CENTRAL_DSN` (`scripts/run_twitch_invite_sync.sh`, `rust/bin/dl-twitch-invite-sync/src/main.rs`, `rust/crates/dl-central-db/src/pool.rs`).

`deadlock-twitch-invite-sync.timer` startet alle 15 Minuten den Oneshot-Service `deadlock-twitch-invite-sync.service`. Der Service nutzt WorkingDirectory `/home/naniadm/Documents/Deadlock-Bots`, lädt Infisical und startet `rust/target/release/dl-twitch-invite-sync` (`/home/naniadm/.config/systemd/user/deadlock-twitch-invite-sync.timer`, `/home/naniadm/.config/systemd/user/deadlock-twitch-invite-sync.service`, `scripts/run_twitch_invite_sync.sh`).

`dl-repostats.timer` startet `dl-repostats.service` 3 Minuten nach Boot und danach alle 2 Stunden. Die Live-Unit führt direkt `rust/target/release/dl-repostats` im WorkingDirectory `/home/naniadm/Documents/Deadlock-Bots` aus (`/home/naniadm/.config/systemd/user/dl-repostats.timer`, `/home/naniadm/.config/systemd/user/dl-repostats.service`).

## Restart und Logs

User-Services werden mit `systemctl --user restart <service-name>` neu gestartet. Die gelesenen Live-Units für diesen Satz heißen `deadlock-bot-rust.service`, `deadlock-web-rust.service`, `deadlock-twitch-invite-sync.service` und `dl-repostats.service` (`/home/naniadm/.config/systemd/user/deadlock-bot-rust.service`, `/home/naniadm/.config/systemd/user/deadlock-web-rust.service`, `/home/naniadm/.config/systemd/user/deadlock-twitch-invite-sync.service`, `/home/naniadm/.config/systemd/user/dl-repostats.service`).

`scripts/set_infisical_token.sh` schreibt Credential-Dateien und ruft danach `systemctl --user try-restart` auf den betroffenen Diensten auf, außer `--no-restart` ist gesetzt. Das Skript zeigt anschließend `is-active` je Dienst (`scripts/set_infisical_token.sh`).

Log-Zugriff ist nicht als Repo-Skript gekapselt. Für systemd-User-Services ist der belegte Betriebsweg deshalb `journalctl --user -u <service-name>`; die Repo-Codebasis nennt selbst nur `systemctl --user`-Restart-Aufrufe (`scripts/set_infisical_token.sh`, `scripts/migrate_to_systemd_creds.sh`).

## Env-Variablen

Zentrale DB: `DEADLOCK_CENTRAL_DSN` ist Pflicht für Migration, Web, Bot, ETL und Twitch-Invite-Sync (`rust/crates/dl-central-db/src/pool.rs`, `rust/bin/dl-central-migrate/src/main.rs`, `rust/bin/dl-web/src/main.rs`, `rust/bin/dl-twitch-invite-sync/src/main.rs`).

Lokaler SQLite-Pfad: `DEADLOCK_DB_PATH` schlägt `DEADLOCK_DB_DIR`, sonst nutzt `dl-core` `data/deadlock.sqlite3`. Zentrale Live-Daten laufen über `DEADLOCK_CENTRAL_DSN` und Postgres (`rust/crates/dl-core/src/config.rs`, `rust/crates/dl-central-db/src/pool.rs`).

Ports: `DASHBOARD_PORT`, `PUBLIC_STATS_PORT`, `MASTER_BROKER_PORT`, `TIERLIST_PUBLIC_PORT` und `CHANGELOG_API_PORT` setzen die Default-Ports `8766`, `8768`, `8770`, `8771` und `8899` außer Kraft (`rust/crates/dl-core/src/config.rs`).

Web: `PUBLIC_STATS_SESSION_SECRET`, `SESSIONS_ENCRYPTION_KEY`, `PUBLIC_STATS_INSECURE_COOKIE`, `PUBLIC_STATS_COOKIE_SECURE`, `PUBLIC_STATS_CORS_ORIGINS`, `DASHBOARD_INTERNAL_API_BASE`, `PUBLIC_STATS_CALLBACK_URL`, `PUBLIC_STATS_HOST`, `TIERLIST_PUBLIC_HOST`, `DL_STATIC_DIR` und `DL_TIERLIST_REFRESH` steuern Stats, Cookies, CORS, Static-Pfad und Tierlist-Refresh (`rust/crates/dl-webcore/src/config.rs`).

Dashboard: `DISCORD_OAUTH_CLIENT_ID`, `DISCORD_OAUTH_CLIENT_SECRET`, `MASTER_DASHBOARD_DISCORD_REDIRECT_URI`, `MASTER_DASHBOARD_OWNER_USER_ID`, `MASTER_DASHBOARD_MODERATOR_ROLE_ID`, `MASTER_DASHBOARD_AUTH_GUILD_IDS`, `MASTER_DASHBOARD_SESSION_TTL_SEC`, `MASTER_DASHBOARD_OAUTH_STATE_TTL_SEC`, `DEADLOCK_OAUTH_STATE_TTL_SECONDS`, `MASTER_DASHBOARD_PUBLIC_URL`, `MASTER_DASHBOARD_LISTEN_URL`, `MASTER_DASHBOARD_ALLOWED_ORIGINS`, `DISCORD_API_BASE` und `MASTER_BROKER_BASE_URL` steuern Auth und interne Broker-Lookups (`rust/crates/dl-dashboard/src/config.rs`).

Broker und Server-Sync: `MASTER_BROKER_TOKEN`, `MAIN_BOT_INTERNAL_TOKEN`, `TWITCH_INTERNAL_API_TOKEN`, `MASTER_BROKER_HOST`, `MASTER_BROKER_ALLOWED_CHANNEL_IDS`, `MASTER_BROKER_ALLOWED_ROLE_IDS`, `SERVERSYNC_INTERNAL_TOKEN` und die Alias-Namen in `dl-broker` steuern Auth, Bindung und Allowlisten (`rust/bin/dl-bot/src/main.rs`, `rust/crates/dl-broker/src/lib.rs`).

MCP: Der integrierte Bot-Connector nutzt `MCP_CONNECTOR_HOST`, `MCP_CONNECTOR_PORT`, `MCP_CONNECTOR_TOKEN`, `MCP_DEFAULT_GUILD_ID` und `MCP_EXPORT_DIR`. Das Standalone-Binary `dl-mcp` nutzt dagegen `DISCORD_TOKEN` oder `BOT_TOKEN`, `DL_MCP_HOST`, `DL_MCP_PORT`, `DL_MCP_AUTH_TOKEN`, `DL_MCP_GUILD_ID` und `DL_MCP_EXPORT_DIR` (`rust/bin/dl-bot/src/mcp.rs`, `rust/bin/dl-mcp/src/main.rs`).

AI und Moderation: `OPENAI_API_KEY`, `DEADLOCK_OPENAI_KEY`, `OPENAI_BASE_URL`, `AI_MODERATOR_ENABLE`, `MODERATION_ENFORCE`, `MOD_ENFORCE`, `SECURITY_GUARD_ENFORCE`, `MOD_ANALYZE_FLAG_THRESHOLD`, `MOD_AUTO_VERIFY_THRESHOLD`, `MOD_PROPOSE_VERIFY_THRESHOLD`, `MOD_TIMEOUT_MINUTES` und `MOD_BEHAVIOR_PROPOSAL_TIMEOUT_MINUTES` steuern Modellzugriff, Scanner, Shadow-Modus und Policy-Schwellen (`rust/bin/dl-bot/src/main.rs`, `rust/crates/dl-ai/src/lib.rs`, `rust/crates/dl-moderation/src/action_policy.rs`).

## Fallen

`DL_BOT_GATEWAY=1` macht `dl-bot` zum Gateway-Owner. Ohne diese Variable bleiben Gateway-Subscriber aus, aber Broker, Changelog, Server-Sync und MCP binden trotzdem. Zwei aktive Gateway-Sessions mit demselben Bot-Token sind laut Wrapper nicht erlaubt (`rust/bin/dl-bot/src/main.rs`, `scripts/run_dl_bot_service.sh`).

`DL_ENABLE_PRESENCE_INTENT=1` fordert den privilegierten Presence-Intent an. Der Wrapper setzt ihn auf `1`; der Code nutzt ihn nur im Gateway-Zweig (`scripts/run_dl_bot_service.sh`, `rust/bin/dl-bot/src/main.rs`).

`DL_TIERLIST_REFRESH=0` ist der Schalter, um den Tierlist-Refresh-Loop auszuschalten. Sonst startet `dl-web` den Refresh-Loop nach dem Bind der Tierlist (`rust/bin/dl-web/src/main.rs`, `rust/crates/dl-webcore/src/config.rs`).

`dl-mcp` liegt unter `rust/bin/`, fehlt aber in `rust/Cargo.toml` unter `members`. `cargo build --workspace` baut es deshalb nicht als Workspace-Paket (`rust/Cargo.toml`, `rust/bin/dl-mcp/Cargo.toml`).

Der Kommentar in `scripts/run_twitch_invite_sync.sh` nennt SQLite und setzt `DEADLOCK_DB_PATH`; der Rust-Code schreibt aber `bot.twitch_streamer_invites` und `activity.member_events` über `DEADLOCK_CENTRAL_DSN` in Postgres (`scripts/run_twitch_invite_sync.sh`, `rust/bin/dl-twitch-invite-sync/src/main.rs`, `rust/crates/dl-central-db/src/pool.rs`).
