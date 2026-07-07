---
title: "Deadlock-Bots Integrationen"
tags: [deadlock-bots, intern, integrationen]
stand: 2026-07-07
quelle: Deadlock-Bots
---
# Integrationen

## Master-Broker

Der Master-Broker bietet `/internal/master/v1/*` als localhost-IPC für Discord-Aktionen. Routen decken Rollen, Member, Channel-Info, Name-Resolution, Guild-Stats, Nachrichten, Channels, Rollen, Voice-Move, Invite und DM ab (`rust/crates/dl-broker/src/lib.rs`).

Der Broker verlangt `X-Internal-Token`, erzeugt oder übernimmt `X-Request-Id` und nutzt `X-Idempotency-Key` für idempotente Schreibaufrufe. Allowlisten für Channel, Guild und Rollen kommen aus `MASTER_BROKER_ALLOWED_*`-Env-Namen und Alias-Namen (`rust/crates/dl-broker/src/lib.rs`).

## MCP

Der integrierte MCP-Connector läuft im `dl-bot`-Prozess auf `/mcp` und `/healthz`, default `127.0.0.1:8890`. Er nutzt den Bot-Token aus dem laufenden Prozess, optional `MCP_CONNECTOR_TOKEN`, und schreibt große Exporte nach `MCP_EXPORT_DIR` (`rust/bin/dl-bot/src/mcp.rs`, `rust/bin/dl-bot/src/main.rs`).

Das Standalone-Binary `dl-mcp` bietet dieselben HTTP-Pfade, nutzt aber eigene Env-Namen mit `DL_MCP_*` und akzeptiert `DISCORD_TOKEN` oder `BOT_TOKEN`. Es ruft Discord REST v10 direkt und kennt Tools wie `server_overview`, `list_channels`, `read_messages`, `list_threads`, `export_category`, `send_message`, `search_members` und `api_call` (`rust/bin/dl-mcp/src/main.rs`).

## Twitch-Bridge

`TwitchApiClient` nutzt `TWITCH_INTERNAL_API_TOKEN` und baut die Basis aus `TWITCH_INTERNAL_API_BASE_URL` oder `TWITCH_INTERNAL_API_HOST` plus `TWITCH_INTERNAL_API_PORT`, Default `127.0.0.1:8776`. Nicht-loopback ist nur mit `TWITCH_INTERNAL_API_ALLOW_NON_LOOPBACK` erlaubt (`rust/crates/dl-bridges/src/twitch.rs`).

Die Bridge rehydriert aktive Live-Ankündigungen über `GET /internal/twitch/v1/live/active-announcements`, trackt Button-Klicks über `POST /internal/twitch/v1/live/link-click` und nutzt `Idempotency-Key` bei Klicks. Ticket-FAQ darf Twitch-Diagnose nur für den fragenden User ausführen (`rust/crates/dl-bridges/src/twitch.rs`, `rust/crates/dl-community/src/faq.rs`).

`dl-twitch-invite-sync` ruft `/internal/twitch/v1/streamer-invites`, schreibt `bot.twitch_streamer_invites` und klassifiziert passende `activity.member_events` von anderen Buckets nach `twitch` um. Website-Invite-Codes aus `bot.kv_store` haben Vorrang vor Twitch (`rust/bin/dl-twitch-invite-sync/src/main.rs`).

## Steam

`SteamBotClient` sendet Discord-Ereignisse an `POST {STEAM_BOT_API_URL}/events/discord`, Default `http://127.0.0.1:8783`. Der Token kommt aus `TWITCH_INTERNAL_API_TOKEN`, danach `MASTER_BROKER_TOKEN`, danach `MAIN_BOT_INTERNAL_TOKEN` (`rust/crates/dl-bridges/src/steam.rs`).

Die lokale Steam-Bridge enthält keine Steam-Business-Logik. Sie rendert Antworten des Steam-Bots als Discord-Antwort und öffnet nur das Freundescode-Modal lokal; Panel-Custom-IDs und Beta-Invite-Panel werden im Bridge-Code registriert (`rust/crates/dl-bridges/src/steam.rs`, `rust/bin/dl-bot/src/main.rs`).

## Website-APIs

Der Coaching-Website-Client nutzt `TWITCH_INTERNAL_API_TOKEN`, danach `MASTER_BROKER_TOKEN`, danach `COACHING_BOT_TOKEN`. Die Basis ist `WEBSITE_API_BASE`, im Bot-Wrapper default `http://127.0.0.1:8772/api`; der Code-Default wäre die öffentliche `/api`-URL (`rust/crates/dl-community/src/coaching.rs`, `scripts/run_dl_bot_service.sh`).

Der Client schreibt Coaching-Snapshots nach `POST /coaching/platform/sync`, Coach-Roster nach `POST /coaching/platform/coaches/sync`, liest fällige Benachrichtigungen über `GET /coaching/platform/notifications/due` und bestätigt sie über `POST /coaching/platform/notifications/ack` (`rust/crates/dl-community/src/coaching.rs`).

Public-Stats und Tierlist delegieren Auth an das Dashboard über `DashboardClient`. Dieser ruft unter anderem `/internal/v1/discord/initiate`, `/internal/v1/discord/consume-result` und `/internal/twitch/v1/discord/validate-session` am Dashboard auf (`rust/crates/dl-webcore/src/dashboard.rs`, `rust/bin/dl-web/src/main.rs`).

## Clips

Der belegte Rust-Pfad für Clips ist die Discord-Einsendung: Button `clip_submit_btn_v1`, Modal, URL-Prüfung, 60-Sekunden-Cooldown, Wochenfenster Sonntag 00:00 bis Samstag 23:00 Europe/Berlin und ein TXT-Dump an den Kurator nach Ablauf. Die Persistenz liegt in `clips.clip_submissions`, `clips.clip_windows` und `clips.clip_window_submissions` (`rust/crates/dl-community/src/clips.rs`, `rust/crates/dl-central-db/migrations/0008_clips.sql`).

## Discord-REST

`dl-bot` nutzt Discord über `dl-discord` und direkte REST-Clients für Server-Sync, Vanity-Attribution, Member-Directory und MCP. Vanity pollt `/guilds/{id}/vanity-url`, Member-Directory paginiert Guild-Members und MCP ruft Pfade relativ zu `/api/v10` auf (`rust/bin/dl-bot/src/vanity.rs`, `rust/bin/dl-bot/src/mcp.rs`, `rust/bin/dl-mcp/src/main.rs`, `rust/bin/dl-bot/src/serversync.rs`).
