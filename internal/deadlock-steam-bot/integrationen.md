---
title: "Deadlock Steam-Bot Integrationen"
tags: [internal, steam, integrationen]
stand: 2026-07-07
quelle: "Deadlock-Steam-Bot"
---
# Integrationen

## Discord-Bot

`steam-bot` nutzt `BrokerClient`, wenn `STEAM_BOT_DISCORD` nicht `noop` ist. Der Client sendet an `{STEAM_BROKER_URL}/internal/master/v1/...`, nutzt `X-Internal-Token` und setzt pro Request `X-Idempotency-Key`. (`rust/crates/steam-bot/src/main.rs`, `rust/crates/steam-discord/src/broker.rs`)

`/events/discord` nimmt Discord-Events von der Rust-Bridge im Hauptbot an. Der Handler unterstützt `interaction`, `slash_command`, `member_remove` und `admin_command`. (`/home/naniadm/Documents/Deadlock-Bots/rust/crates/dl-bridges/src/steam.rs`, `rust/crates/steam-web/src/routes/events.rs`)

Der Event-Ingress prüft `X-Internal-Token` gegen `TWITCH_INTERNAL_API_TOKEN`, `STEAM_INTERNAL_API_TOKEN` oder `INTERNAL_API_TOKEN`; fehlt ein erwarteter Token, läuft der Endpoint im Dev-Modus ohne Auth. (`rust/crates/steam-web/src/routes/events.rs`)

Link-Panel-Interaktionen laufen über Prefixe `steam_link_panel:`, `steamlink:`, `steam_link:` und `linkpanel_`. Playtest-Invite-Interaktionen laufen über `betainvite:`. (`rust/crates/steam-web/src/routes/events.rs`)

Slash-Commands werden im Event-Ingress auf Flow-Funktionen gemappt. Dazu gehören `account_verknüpfen`, `steam_links`, `steam_whoami`, `steam_setprimary`, `steam_unlink`, `steam_rank`, `checkrank`, `steam_rank_sync`, `subrank_sync`, `sync_steam_friends` und Beta-Invite-Commands. (`rust/crates/steam-web/src/routes/events.rs`, `rust/crates/steam-flows/src/link_commands.rs`, `rust/crates/steam-flows/src/rank.rs`)

## Account-Link und Discord-OAuth

Der Browser-Link-Flow bietet `/link/steam/start`, `/link/steam/callback`, `/link/callback/steam`, `/link/steam/return`, `/link/discord/login`, `/link/discord/complete` und Legacy-Alias `/link/steam/login`. (`rust/crates/steam-web/src/routes/link.rs`)

Steam-OpenID nutzt fest `https://steamcommunity.com/openid/login`. Der Callback prüft `openid.mode`, lädt den State, sendet `check_authentication` an Steam, extrahiert `openid.claimed_id` und konsumiert den State atomar. (`rust/crates/steam-flows/src/link.rs`)

Discord-OAuth läuft nicht im Steam-Bot. Der Steam-Bot delegiert Start und Consume an die interne Master-Bot-API `/internal/v1/discord/initiate` und `/internal/v1/discord/consume-result`. (`rust/crates/steam-flows/src/link.rs`)

Steam-Vanity und Persona-Namen nutzt der Bot über `https://api.steampowered.com` mit `STEAM_API_KEY`. Ohne Key geben die Resolver `None` zurück. (`rust/crates/steam-flows/src/steam_web_api.rs`)

## Turniere und Lobby

Admin-Lobby-Commands kommen als `admin_command`-Events und werden an `steam_flows::admin::handle_admin_command()` delegiert. `steam_lobby_events` und `steam_status` laufen synchron; andere Admin-Commands laufen im Hintergrund und posten das Ergebnis in den Admin-Log-Kanal. (`rust/crates/steam-web/src/routes/events.rs`, `rust/crates/steam-flows/src/admin.rs`)

Die Admin-Commands `steam_lobby_convar`, `steam_lobby_apply`, `steam_lobby_events` und `steam_lobby_event` erzeugen `GC_LOBBY_SET_CONVAR` oder `GC_LOBBY_APPLY_CONVARS` in `steam-core`. (`rust/crates/steam-flows/src/admin.rs`)

`steam-core` verarbeitet Lobby-Tasks in der Lane `lobby` mit Parallelität 1. Die Lane enthält `GC_CREATE_CUSTOM_LOBBY`, `GC_LOBBY_SET_CONVAR`, `GC_LOBBY_APPLY_CONVARS`, `GC_LOBBY_INVITE_PLAYER`, `GC_LOBBY_SET_SPECTATOR`, `GC_LOBBY_READY`, `GC_LOBBY_START_MATCH`, `GC_LOBBY_LEAVE` und `GC_GET_MATCH_RESULT`. (`rust/crates/steam-core/src/task/lanes.rs`)

`GC_CREATE_CUSTOM_LOBBY` sendet `CMsgClientToGcPartyCreate`, wartet bis zu 20 Sekunden auf den Join-Code aus dem CSO-Party-Cache und gibt `party_id`, `join_code`, `party_code_display` und angewendete ConVars zurück. (`rust/crates/steam-core/src/task/handlers/lobby.rs`, `rust/crates/steam-core/src/steam/cso.rs`)

`GC_LOBBY_START_MATCH` sendet `CMsgClientToGcPartyStartMatch`, löst danach `match_id` über `GetActiveMatches` auf und versucht nach 3 Sekunden einmal erneut, wenn der GC die Match-ID noch nicht zeigt. (`rust/crates/steam-core/src/task/handlers/lobby.rs`)

`GC_GET_MATCH_RESULT` akzeptiert `match_id` oder `party_id`, liest aktive Matches und fällt auf `GetMatchMetaData` zurück, wenn kein Snapshot verfügbar ist. (`rust/crates/steam-core/src/task/handlers/lobby.rs`)

## Steam und GC

`steam-core` nutzt `steam-vent` für Login, Friends-Listen, Persona-State und GC-Verbindung. (`rust/Cargo.toml`, `rust/crates/steam-core/src/steam/session.rs`, `rust/crates/steam-core/src/steam/friends.rs`)

Der GC-Handshake läuft nach dem Steam-Login. Wenn der initiale GC-Connect fehlschlägt, startet der Supervisor einen Hintergrund-Reconnect und der Service läuft mit Task-Queue, API und Heartbeat weiter. (`rust/crates/steam-core/src/main.rs`, `rust/crates/steam-core/src/steam/supervisor.rs`)

Die GC-Task-Handler nutzen `round_trip()` und Deadlock-Protobuf-Typen für Profilkarten, Account-Stats, Match-History, Build-Katalog, Playtest-Invite und Lobby-Operationen. (`rust/crates/steam-core/src/task/handlers/mod.rs`, `rust/crates/steam-core/src/task/handlers/gc.rs`, `rust/crates/steam-core/src/task/handlers/builds/mod.rs`, `rust/crates/steam-core/src/task/handlers/playtest.rs`, `rust/crates/steam-core/src/task/handlers/lobby.rs`)

Der Presence-Listener verarbeitet `CMsgClientPersonaState`, fragt Friend-Data alle 60 Sekunden in Chunks neu an und schreibt `activity.live_player_state` sowie `voice.deadlock_party_members`. (`rust/crates/steam-core/src/steam/presence.rs`, `rust/crates/steam-persistence/src/presence.rs`)

## Ko-fi

`steam-bot` baut den Router mit `KofiWebhookState::from_env()` und warnt beim Start, wenn `KOFI_VERIFICATION_TOKEN` fehlt. (`rust/crates/steam-bot/src/main.rs`)

`POST /kofi/webhook` erwartet form-urlencodetes `data` mit JSON, prüft `verification_token` constant-time gegen `KOFI_VERIFICATION_TOKEN` und delegiert danach an `handle_kofi_payment()`. (`rust/crates/steam-web/src/routes/kofi.rs`, `rust/crates/steam-flows/src/supporter.rs`)

`GET /kofi/health` liefert nur `{"ok": true}`. (`rust/crates/steam-web/src/routes/kofi.rs`)
