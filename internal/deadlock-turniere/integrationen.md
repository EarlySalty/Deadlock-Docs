---
title: "Turniere — Integrationen"
tags: [internal, deadlock-turniere, integrationen]
stand: 2026-07-07
quelle: Deadlock-Turniere
---
# Turniere — Integrationen

Der Rust-Dienst integriert drei externe Pfade: delegierten Discord-OAuth, Discord-Effekte über den Master-Broker und Steam-Lobby-Aktionen über die Steam-Bridge-Queue. Rangdaten kommen aus `turnier.rank_cache`, Steam-Bridge und Discord-Rollen. (`rust/crates/turnier-auth/src/oauth.rs`, `rust/crates/turnier-discord/src/broker.rs`, `rust/crates/turnier-steam/src/resolver.rs`)

## Discord-OAuth

Der OAuth-Flow wird an Deadlock-Bots delegiert. `OAuthClient` ruft `POST /internal/v1/discord/initiate` und `POST /internal/v1/discord/consume-result` mit Header `X-Internal-Token` auf; Scope ist `identify guilds.members.read`, `requesting_service` ist `turnier`. (`rust/crates/turnier-auth/src/oauth.rs`)

`/auth/discord/login` holt die Authorize-URL und leitet den Browser weiter. `/auth/discord/complete` löst `state_id` ein, erstellt eine Session in `turnier.sessions`, setzt `session_token` und leitet zur konfigurierten Frontend-URL. `/auth/discord/logout` löscht Session und Cookie. (`rust/crates/turnier-api/src/auth.rs`, `rust/crates/turnier-auth/src/session.rs`)

Authentifizierte Requests lesen zuerst `Authorization: Bearer <token>`, danach das Cookie `session_token`. `AuthUser` verlangt eine gültige Session, `ModUser` und `AdminUser` prüfen die aus Config-Rollen berechneten Flags. (`rust/crates/turnier-api/src/extract.rs`, `rust/crates/turnier-auth/src/roles.rs`)

## Discord-Broker

Der Discord-Broker-Client hält einen wiederverwendeten `reqwest::Client`, normalisiert die Base-URL, nutzt `X-Internal-Token` und mappt Broker-Fehler aus JSON-Feldern `error` oder `detail`. (`rust/crates/turnier-discord/src/broker.rs`)

Der Notifier nutzt interne Broker-Pfade für Channel anlegen, Rich Message senden, Plain Message senden, Channel löschen, Voice Move, Voice-Member-Liste und Rollenmitglieder. Die Pfade stehen zentral im `path`-Modul. (`rust/crates/turnier-discord/src/notifier.rs`)

Discord-Effekte werden in `turnier.discord_tasks` protokolliert. Rust legt eine Zeile direkt mit `status='RUNNING'` an und markiert danach `DONE` oder `FAILED` mit Result-Payload oder Fehlertext. (`rust/crates/turnier-discord/src/tasks.rs`)

DM-Versand respektiert `turnier.user_profiles` und `turnier.tournament_dm_optout`. Der Notifier lädt nur die eventrelevanten Profilspalten und schreibt pro Empfänger ein Ergebnis in `sent`, `skipped` oder `failed`. (`rust/crates/turnier-discord/src/notifier.rs`)

## Steam-Bridge

Die Steam-Bridge ist ein separater SQLite-Pool auf `STEAM_BRIDGE_DB_PATH`. `SteamBridge::open()` legt die Datei nicht an; leerer Pfad oder fehlende Datei führen zu `Ok(None)` und damit zu deaktivierten Steam-Tasks im MatchManager. (`rust/crates/turnier-match/src/steam_bridge.rs`, `rust/crates/turnier-api/src/state.rs`)

Steam-Aufträge werden in `steam_tasks` geschrieben. Rust erzeugt Tasks mit Typ, JSON-Payload und `PENDING`, markiert hängende `RUNNING`-Tasks nach 120 Sekunden als `FAILED` und pollt alle 500 ms bis `DONE`, `FAILED` oder Timeout. (`rust/crates/turnier-match/src/steam_bridge.rs`)

Lobby-Erstellung erzeugt `GC_CREATE_CUSTOM_LOBBY` mit `tournament_id`, `match_id`, `match_type`, `game_mode`, `region_mode` und optionalen ConVars. Danach schreibt Rust Lobby-Daten ins Match, lädt eindeutige Steam-IDs ein und erstellt Discord-Channel und Announcement best-effort. (`rust/crates/turnier-match/src/lobby.rs`, `rust/crates/turnier-match/src/repo.rs`)

Spieler-Einladungen nutzen `GC_LOBBY_INVITE_PLAYER` pro eindeutiger Steam-ID. Vorher prüft Rust aktive Tasks mit gleicher `party_id` und `steam_id`; aktive Einladungen landen im `skipped`-Bucket. (`rust/crates/turnier-match/src/steam_bridge.rs`, `rust/crates/turnier-match/src/lobby.rs`)

Match-Start setzt erst Spectator und Ready über `GC_LOBBY_SET_SPECTATOR` und `GC_LOBBY_READY`, startet dann `GC_LOBBY_START_MATCH` und setzt das Match auf `in_progress`. Lobby verlassen nutzt `GC_LOBBY_LEAVE` und schreibt keine neuen Lobby-Daten zurück. (`rust/crates/turnier-match/src/lobby.rs`, `rust/crates/turnier-match/src/repo.rs`)

## Rangdaten

Der Rang-Resolver liest zuerst den prozesslokalen und persistenten Cache, danach Steam-Bridge und danach Discord-Rollen. Treffer aus Steam-Bridge oder Discord-Rollen schreibt er per UPSERT nach `turnier.rank_cache`. (`rust/crates/turnier-steam/src/resolver.rs`, `rust/crates/turnier-steam/src/cache.rs`)

Der Cache nutzt 24 Stunden TTL. L2 liest `turnier.rank_cache` mit `cached_at > now() - interval '24 hours'`, L1 nutzt dieselbe Dauer im Prozess. (`rust/crates/turnier-steam/src/cache.rs`)
