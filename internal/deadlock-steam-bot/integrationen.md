---
title: "Deadlock Steam-Bot Integrationen"
tags: [internal, steam, integrationen]
stand: 2026-07-08
quelle: "Deadlock-Steam-Bot"
---
# Integrationen

## Discord-Bot

`steam-bot` nutzt `BrokerClient`, wenn `STEAM_BOT_DISCORD` nicht `noop` ist. Der Client sendet an `{STEAM_BROKER_URL}/internal/master/v1/...`, nutzt `X-Internal-Token` und setzt pro Request `X-Idempotency-Key`. (`rust/crates/steam-bot/src/main.rs`, `rust/crates/steam-discord/src/broker.rs`)

POST-Brokerpfade sind `discord/send-message`, `discord/send-rich-message`, `discord/edit-rich-message`, `discord/member/add-role`, `discord/member/remove-role`, `discord/create-channel`, `discord/delete-channel` und `discord/create-invite`. GET-Pfade sind `discord/role-members`, `discord/member-present`, `discord/channel-info` und `discord/roles`. POSTs behalten denselben UUIDv4-Idempotency-Key und wiederholen 5xx-Antworten bis zu zwei Mal nach 200 ms. (`rust/crates/steam-discord/src/broker.rs`)

`/events/discord` nimmt Discord-Events von der Rust-Bridge im Hauptbot an. Der Handler unterstützt `interaction`, `slash_command`, `member_remove` und `admin_command`. (`/home/naniadm/Documents/Deadlock-Bots/rust/crates/dl-bridges/src/steam.rs`, `rust/crates/steam-web/src/routes/events.rs`)

Der Event-Ingress prüft `X-Internal-Token` gegen `TWITCH_INTERNAL_API_TOKEN`, `STEAM_INTERNAL_API_TOKEN` oder `INTERNAL_API_TOKEN`; fehlt ein erwarteter Token, läuft der Endpoint im Dev-Modus ohne Auth. (`rust/crates/steam-web/src/routes/events.rs`)

Link-Panel-Interaktionen laufen über Prefixe `steam_link_panel:`, `steamlink:`, `steam_link:` und `linkpanel_`. Playtest-Invite-Interaktionen laufen über `betainvite:`. (`rust/crates/steam-web/src/routes/events.rs`)

Slash-Commands werden im Event-Ingress auf Flow-Funktionen gemappt. Dazu gehören `account_verknüpfen`, `steam_links`, `steam_whoami`, `steam_setprimary`, `steam_unlink`, `steam_rank`, `checkrank`, `steam_rank_sync`, `subrank_sync`, `sync_steam_friends` und Beta-Invite-Commands. (`rust/crates/steam-web/src/routes/events.rs`, `rust/crates/steam-flows/src/link_commands.rs`, `rust/crates/steam-flows/src/rank.rs`)

## Account-Link und Discord-OAuth

Der Browser-Link-Flow bietet `/link/steam/start`, `/link/steam/callback`, `/link/callback/steam`, `/link/steam/return`, `/link/discord/login`, `/link/discord/complete` und Legacy-Alias `/link/steam/login`. (`rust/crates/steam-web/src/routes/link.rs`)

Steam-OpenID nutzt fest `https://steamcommunity.com/openid/login`. Der Callback prüft `openid.mode`, lädt den State, sendet `check_authentication` an Steam, extrahiert `openid.claimed_id` und konsumiert den State atomar. (`rust/crates/steam-flows/src/link.rs`)

Discord-OAuth läuft nicht im Steam-Bot. Der Steam-Bot delegiert Start und Consume an die interne Master-Bot-API `/internal/v1/discord/initiate` und `/internal/v1/discord/consume-result`. (`rust/crates/steam-flows/src/link.rs`)

Steam-Vanity und Persona-Namen nutzt der Bot über `https://api.steampowered.com` mit `STEAM_API_KEY`. Ohne Key geben die Resolver `None` zurück. (`rust/crates/steam-flows/src/steam_web_api.rs`)

## Rank-Web-API

`GET /rank` liefert den Link-/Rank-Status für einen Discord-User. `GET /player-matches` lädt Match-History über den bevorzugten Steam-Link und akzeptiert ein Limit. `GET /player-live` liest `activity.live_player_state` und gibt `linked`, `in_deadlock`, `live`, Hero, Minuten, Stage und Zeitstempel zurück. `GET /player-mmr-trend` liest sichtbare Rank-History für den Trend. (`rust/crates/steam-web/src/routes/rank.rs`)

## Beta-Invite, Friends und Builds

`/betainvite` routet aktiv auf `betainvite:panel:start`; `publish_betainvite_panel` baut nur das Panel. Der Funnel erstellt oder nutzt `beta-invite-{user_id}`-Tickets, prüft Link und Steam-Freundschaft, reiht `AUTH_SEND_PLAYTEST_INVITE` ein, schreibt Audit und plant Self-Heal je nach GC-/Steam-Fehlerklasse. Der Ko-fi-Absprung hängt am Pending-Payment-Token im Format `DDL-XXXXXXXX`. (`rust/crates/steam-web/src/routes/events.rs`, `rust/crates/steam-flows/src/betainvite.rs`, `rust/crates/steam-flows/src/betainvite/interactions.rs`)

Der Steam-Friends-Listener akzeptiert eingehende Steam-Friend-Requests automatisch. Der Friend-Sync markiert bekannte Links als verifiziert, entfernt unbekannte Steam-Freunde aus der Bot-Freundesliste und queue't Rollen-Cleanup, wenn ein verknüpfter Account nach Miss-Schwelle nicht mehr befreundet ist. (`rust/crates/steam-core/src/steam/friends.rs`, `rust/crates/steam-flows/src/friend_sync.rs`)

Der Build-Publisher arbeitet über `BUILD_PUBLISH`, `BUILD_DELETE`, `MAINTAIN_BUILD_CATALOG` und `BUILD_CATALOG_CYCLE`. Er liest Dashboard-Konfiguration aus `tierlist.deadlock_hero_builds`, Quellen aus `tierlist.hero_build_sources`, schreibt Clones nach `tierlist.hero_build_clones` und nutzt GC-Build-Nachrichten zum Publizieren und Löschen. (`rust/crates/steam-core/src/task/handlers/builds/mod.rs`, `rust/crates/steam-persistence/src/builds.rs`)

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

Statusmapping: `missing_data_field`, `invalid_encoding`, `invalid_json` und `missing_message` liefern 400; `invalid_verification_token` liefert 401; `token_not_found` und `user_not_found` liefern 409; `webhook_disabled`, `guild_unavailable` und `payment_confirm_failed` liefern 503. Unbekannte Gründe werden 500. (`rust/crates/steam-web/src/routes/kofi.rs`, `rust/crates/steam-flows/src/supporter.rs`)

Ein Support-Klick erzeugt ein Pending-Payment mit Token `DDL-XXXXXXXX`; der Webhook consumed den Token, setzt oder verlängert den Grant für 30 Tage und setzt die Supporter-Rolle defensiv. Der Supporter-Scheduler läuft alle 10 Minuten und entfernt abgelaufene Grants per Broker. (`rust/crates/steam-flows/src/betainvite/interactions.rs`, `rust/crates/steam-flows/src/supporter.rs`, `rust/crates/steam-persistence/src/supporter.rs`)

`GET /kofi/health` liefert nur `{"ok": true}`. (`rust/crates/steam-web/src/routes/kofi.rs`)
