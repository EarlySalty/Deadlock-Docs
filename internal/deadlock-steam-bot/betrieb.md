---
title: "Deadlock Steam-Bot Betrieb"
tags: [internal, steam, betrieb]
stand: 2026-07-07
quelle: "Deadlock-Steam-Bot"
---
# Betrieb

## Build

Die Release-Binaries heißen `steam-core` und `steam-bot`. Beide liegen nach dem Build unter `rust/target/release/`, weil die Wrapper genau diese Pfade prüfen. (`rust/crates/steam-core/Cargo.toml`, `rust/crates/steam-bot/Cargo.toml`, `rust/deploy/run-steam-core.sh`, `rust/deploy/run-steam-bot.sh`)

Der minimale Build-Befehl ist:

```bash
cargo build --manifest-path rust/Cargo.toml --release -p steam-core -p steam-bot
```

Der Workspace nutzt Rust stable mit `rustfmt` und `clippy`. (`rust/rust-toolchain.toml`, `rust/Cargo.toml`)

## Deploy und Restart

Die systemd-User-Units heißen `steam-core.service` und `steam-bot.service`. `steam-bot.service` hat `After=network-online.target steam-core.service` und startet den Wrapper `run-steam-bot.sh`. Beide Live-Units liegen unter `/home/naniadm/.config/systemd/user/` und haben Drop-ins für `LoadCredential`; `steam-core` hat zusätzlich `STEAM_PRESENCE_ENABLED=1`, `steam-bot` Friend-Limit-Reservierung (`/home/naniadm/.config/systemd/user/steam-core.service`, `/home/naniadm/.config/systemd/user/steam-bot.service`, `/home/naniadm/.config/systemd/user/steam-core.service.d/30-presence.conf`, `/home/naniadm/.config/systemd/user/steam-bot.service.d/phase0-friend-limit.conf`).

Der sichere Restart läuft zuerst über Core, dann Bot:

```bash
systemctl --user restart steam-core.service
systemctl --user restart steam-bot.service
```

`steam-bot` wartet im Wrapper auf `STEAM_CORE_WAIT_URL` und nutzt `STEAM_CORE_WAIT_MAX` als Obergrenze; danach startet er auch ohne erfolgreiche Core-Readiness und verlässt sich auf eigene Retries. (`rust/deploy/run-steam-bot.sh`)

Die Drop-ins `steam-core.service.d/20-creds.conf` und `steam-bot.service.d/20-creds.conf` reichen `infisical-token` über `LoadCredential` in `$CREDENTIALS_DIRECTORY`. `steam-core.service.d/30-presence.conf` setzt `STEAM_PRESENCE_ENABLED=1`. (`rust/deploy/dropins/steam-core.service.d/20-creds.conf`, `rust/deploy/dropins/steam-bot.service.d/20-creds.conf`, `rust/deploy/dropins/steam-core.service.d/30-presence.conf`, `rust/deploy/dropins/README.md`)

## Logs

Beide Binaries initialisieren `tracing_subscriber::fmt()` und schreiben über stdout/stderr in den systemd-User-Journalpfad. (`rust/crates/steam-core/src/main.rs`, `rust/crates/steam-bot/src/main.rs`, `rust/deploy/steam-core.service`, `rust/deploy/steam-bot.service`)

Die Live-Logs kommen aus dem User-Journal:

```bash
journalctl --user -u steam-core.service -f
journalctl --user -u steam-bot.service -f
```

## Env-Variablen

Core-Start: `DEADLOCK_CENTRAL_DSN`, `STEAM_CORE_API_ADDR`, `RUST_LOG`, `STEAM_CORE_API_TOKEN`, `STEAM_BOT_USERNAME`, `STEAM_LOGIN`, `STEAM_BOT_PASSWORD`, `STEAM_PASSWORD`, `STEAM_TOTP_SECRET`, `STEAM_REFRESH_TOKEN`, `STEAM_DATA_DIR`. (`rust/crates/steam-core/src/config.rs`, `rust/crates/steam-core/src/main.rs`, `/home/naniadm/Documents/Deadlock-Bots/rust/crates/dl-central-db/src/pool.rs`)

Core-Betrieb: `STEAM_PRESENCE_ENABLED`, `CATALOG_MAINTENANCE_INTERVAL_MS`, `STEAM_COMMAND_POLL_MS`, `STEAM_TASKS_MAX_ROWS`, `STEAM_TOKEN_REFRESH_LEAD_DAYS`, `STEAM_TOKEN_AUTO_REFRESH`, `STEAM_TOKEN_UPDATER_SCRIPT`. (`rust/crates/steam-core/src/main.rs`, `rust/crates/steam-core/src/command_loop.rs`, `rust/crates/steam-persistence/src/tasks.rs`, `rust/crates/steam-core/src/token_refresh.rs`, `rust/crates/steam-core/src/steam/token_sync.rs`)

Steam-Guard-Mailpfad: `STEAM_GUARD_EMAIL`, `STEAM_EMAIL_ACCOUNT_PASSWORD`, `STEAM_GUARD_IMAP_SERVER`, `STEAM_GUARD_IMAP_PORT`, `STEAM_GUARD_MAX_EMAIL_AGE`, `STEAM_GUARD_POLL_INTERVAL`. (`rust/crates/steam-core/src/steam/email_guard.rs`)

Bot-Start und Core-Client: `STEAM_BOT_API_ADDR`, `STEAM_BOT_DISCORD`, `RUST_LOG`, `STEAM_CORE_URL`, `STEAM_CORE_API_TOKEN`. (`rust/crates/steam-bot/src/main.rs`, `rust/crates/steam-flows/src/shared.rs`)

Discord-Broker: `STEAM_BROKER_URL`, `TWITCH_INTERNAL_API_TOKEN`, `STEAM_INTERNAL_API_TOKEN`, `INTERNAL_API_TOKEN`. (`rust/crates/steam-discord/src/broker.rs`, `rust/crates/steam-web/src/routes/events.rs`)

Link/OAuth: `PUBLIC_BASE_URL`, `STEAM_LINK_PUBLIC_BASE_URL`, `STEAM_RETURN_PATH`, `DISCORD_OAUTH_REDIRECT`, `DISCORD_OAUTH_INTERNAL_API_BASE_URL`, `TURNIER_INTERNAL_API_TOKEN`, `MASTER_BROKER_TOKEN`, `MAIN_BOT_INTERNAL_TOKEN`, `STEAM_API_KEY`, `STEAM_FIELD_CRYPTO_KEY`, `FRIEND_CODE_LINKING_ENABLED`, `STEAM_LOGIN_LAUNCH_TTL_SEC`, `STEAM_TRUST_X_FORWARDED_FOR`. (`rust/crates/steam-flows/src/link.rs`, `rust/crates/steam-flows/src/field_crypto.rs`, `rust/crates/steam-web/src/routes/link.rs`, `rust/crates/steam-flows/src/steam_web_api.rs`)

Guild, Rollen und Scheduler: `STEAM_GUILD_ID`, `STEAM_VERIFIED_ROLE_ID`, `STEAM_FRIEND_SYNC_INTERVAL_HOURS`, `STEAM_POLL_MIN_INTERVAL_SEC`, `STEAM_UNFOLLOW_MISS_THRESHOLD`, `STEAM_POLL_BATCH_SIZE`, `STEAM_FRIEND_REQUEST_RECONCILE_INTERVAL_SEC`, `STEAM_FRIEND_REQUEST_RECONCILE_BATCH_SIZE`, `AUTO_SYNC_INTERVAL_MINUTES`, `STEAM_FRIEND_LIMIT`, `STEAM_FRIEND_RESERVE`, `STEAM_INACTIVE_PURGE_DAYS`. (`rust/crates/steam-flows/src/friend_sync.rs`, `rust/crates/steam-flows/src/rank.rs`, `rust/crates/steam-flows/src/purge.rs`, `rust/crates/steam-flows/src/leave_cleanup.rs`)

Beta-Invite und Ko-fi: `STEAM_BOT_FRIEND_CODE`, `BETA_INVITE_COMMUNITY_DISPATCH_INTERVAL_SECONDS`, `BETA_INVITE_COMMUNITY_DISPATCH_MAX_RETRYABLE_FAILURES`, `BETA_INVITE_COMMUNITY_DISPATCH_MIN_SECONDS`, `BETA_INVITE_COMMUNITY_DISPATCH_MAX_SECONDS`, `MAIN_GUILD_ID`, `KOFI_VERIFICATION_TOKEN`. (`rust/crates/steam-flows/src/betainvite.rs`, `rust/crates/steam-flows/src/supporter.rs`, `rust/crates/steam-web/src/routes/kofi.rs`)

Wrapper: `INFISICAL_CONFIG_FILE`, `INFISICAL_EXPORT_SCRIPT`, `STEAM_CORE_BIN`, `STEAM_BOT_BIN`, `INFISICAL_SERVICE_TOKEN`, `CREDENTIALS_DIRECTORY`, `INFISICAL_RETRY_DELAY`, `INFISICAL_MAX_ATTEMPTS`, `STEAM_CORE_WAIT_URL`, `STEAM_CORE_WAIT_MAX`. (`rust/deploy/run-steam-core.sh`, `rust/deploy/run-steam-bot.sh`)

## Fallen

Falle: Alte Deploy-Vorlagen und Betriebsnotizen können noch `DEADLOCK_DB_PATH` nennen, aber die gelesenen Live-Units setzen diesen Wert nicht. Der aktuelle Rust-Code liest die zentrale Postgres-DSN `DEADLOCK_CENTRAL_DSN`; SQLite-Anweisungen zeigen daher nicht auf den produktiven Pfad (`/home/naniadm/.config/systemd/user/steam-core.service`, `/home/naniadm/.config/systemd/user/steam-bot.service`, `rust/crates/steam-core/src/main.rs`, `rust/crates/steam-bot/src/main.rs`, `rust/crates/steam-persistence/src/lib.rs`).

Falle: Der Primary-Race ist nur geschlossen, wenn Migration `0015_steam_links_one_primary.sql` gelaufen ist und der Codepfad `upsert_link()` genutzt wird. Die Migration legt `uq_steam_links_one_primary` an, und `upsert_link()` nimmt zusätzlich einen Advisory-Lock pro User. (`/home/naniadm/Documents/Deadlock-Bots/rust/crates/dl-central-db/migrations/0015_steam_links_one_primary.sql`, `rust/crates/steam-persistence/src/links.rs`)

Falle: Wenn `STEAM_CORE_API_TOKEN` fehlt, lässt `steam-core` alle geschützten Endpunkte außer `/health` im Loopback-Modus ohne Token durch. (`rust/crates/steam-core/src/api/mod.rs`)

Falle: Wenn `KOFI_VERIFICATION_TOKEN` fehlt, antwortet `/kofi/webhook` mit 503 und verarbeitet keine Zahlungen. (`rust/crates/steam-bot/src/main.rs`, `rust/crates/steam-web/src/routes/kofi.rs`)

Falle: Der Token-Auto-Refresh-Pfad ruft bei `STEAM_TOKEN_AUTO_REFRESH` und vorhandenem Passwort `std::process::exit(0)` auf. Die Unit nutzt `Restart=on-failure`; Exit 0 löst dort keinen on-failure-Neustart aus. (`rust/crates/steam-core/src/token_refresh.rs`, `rust/deploy/steam-core.service`)

Falle: `STEAM_BOT_DISCORD=noop` ersetzt den Broker durch `NoopDiscord`; Discord-Seiteneffekte werden dann nicht beim Master-Bot ausgeführt. (`rust/crates/steam-bot/src/main.rs`)
