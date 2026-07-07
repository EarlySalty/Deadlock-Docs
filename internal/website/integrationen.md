---
title: "Website Integrationen"
tags: [website, intern, integrationen]
stand: 2026-07-07
quelle: "Website"
---
# Integrationen

## Bot-APIs

Interne Bot-Endpunkte im Website-Backend akzeptieren `X-Internal-Token` oder `X-Bot-Token`; der Vergleich nutzt `constant_time_eq` gegen `TWITCH_INTERNAL_API_TOKEN`, `MASTER_BROKER_TOKEN` oder `COACHING_BOT_TOKEN` (`/home/naniadm/Documents/Website/builds/backend-rust/src/routes/coaching.rs`).

Der Rust-Bot-Client baut `WEBSITE_API_BASE`, Default `https://deutsche-deadlock-community.de/api`, und sendet beide Header bei `POST /coaching/platform/sync`, `POST /coaching/platform/coaches/sync`, `GET /coaching/platform/notifications/due` und `POST /coaching/platform/notifications/ack` (`/home/naniadm/Documents/Deadlock-Bots/rust/crates/dl-community/src/coaching.rs`).

Der aktive Rust-Bot-Wrapper setzt `WEBSITE_API_BASE=http://127.0.0.1:8772/api`, wenn die Variable nicht schon gesetzt ist; damit laufen Bot-Calls lokal gegen das Website-Backend statt über die öffentliche Domain (`/home/naniadm/Documents/Deadlock-Bots/scripts/run_dl_bot_service.sh`).

Auth im Website-Backend delegiert Discord-Login-Daten an `DASHBOARD_INTERNAL_API_BASE`, Default `http://127.0.0.1:8766`, und sendet `X-Internal-Token` mit einem Token aus `WEBSITE_INTERNAL_API_TOKEN`, `TURNIER_INTERNAL_API_TOKEN`, `MAIN_BOT_INTERNAL_TOKEN` oder `TWITCH_INTERNAL_API_TOKEN` (`/home/naniadm/Documents/Website/builds/backend-rust/src/routes/auth.rs`, `/home/naniadm/Documents/Website/builds/backend-rust/src/config.rs`).

Der Coaching-No-Show-Check ruft `{DASHBOARD_INTERNAL_API_BASE}/internal/coaching/v1/no-show-ban` auf und nutzt `TURNIER_INTERNAL_API_TOKEN`, `MAIN_BOT_INTERNAL_TOKEN`, `TWITCH_INTERNAL_API_TOKEN` oder `MASTER_BROKER_TOKEN` (`/home/naniadm/Documents/Website/builds/backend-rust/src/routes/coaching.rs`).

## Coaching-Flow

`dl-coaching` routet `/anfrage` auf `CoachingRequestPage`, `/dashboard` auf `CoachDashboardPage`, `/overview` auf `CoachOverviewPage`, `/coachees/:id` auf `CoacheeDetailPage`, `/me` auf `MyCoachingPage` und Scrim-Seiten unter `/scrims` (`/home/naniadm/Documents/Website/dl-coaching/src/App.tsx`).

Der Coaching-API-Client postet neue Website-Anfragen an `/coaching/requests`, liest Coaches über `/coaching/coaches`, lädt Plattform-Queue über `/coaching/platform/queue` und verwaltet Ziele, Meilensteine, Notizen und Termine über `/coaching/platform/*` (`/home/naniadm/Documents/Website/dl-coaching/src/api/client.ts`).

`POST /api/coaching/requests` schreibt `coaching.requests`, prüft vorher den No-Show-Ban über die interne Dashboard-API und speichert optionale Website- und Bot-IDs für idempotentes Matching (`/home/naniadm/Documents/Website/builds/backend-rust/src/routes/coaching.rs`).

`POST /api/coaching/platform/sync` ist der Bot-Spiegel-Endpunkt; er verlangt Bot-Token, verlangt `website_request_id`, `bot_request_id` oder `request_uid`, upsertet `coaching.coachees`, aktualisiert oder erstellt `coaching.requests` und kann Sessions in `coaching.sessions` mitschreiben (`/home/naniadm/Documents/Website/builds/backend-rust/src/routes/platform.rs`).

`GET /api/coaching/platform/notifications/due` liefert Termin-Events und `request_created`-Events; `POST /api/coaching/platform/notifications/ack` setzt `notify_*_at` auf Terminen oder `notify_discord_at` auf Requests (`/home/naniadm/Documents/Website/builds/backend-rust/src/routes/platform.rs`).

## Discord Linked Role

Linked-Role-Login und Callback hängen unter `/api/auth/discord/linked-role/*`; Caddy macht daraus öffentlich `/coaching/api/auth/discord/linked-role/*` und der Startwrapper setzt die öffentliche Callback-URL entsprechend (`/home/naniadm/Documents/Website/builds/backend-rust/src/app.rs`, `/home/naniadm/Documents/Website/scripts/run_builds_backend.sh`, `/home/naniadm/Documents/Caddy/conf/Caddyfile`).

Discord-Role-Tokens liegen in `core.discord_role_connection_tokens`; der Sync-State liegt in `core.discord_role_connection_sync_state` und wird per Migration angelegt (`/home/naniadm/Documents/Deadlock-Bots/rust/crates/dl-central-db/migrations/2026070330_discord_role_connections.sql`, `/home/naniadm/Documents/Website/builds/backend-rust/src/routes/linked_role.rs`).

## Turnier-Portal

Das Website-Repo verlinkt `/turnier/` in Navigation und Sitemap, aber die aktive Auslieferung kommt laut Caddy aus `/home/naniadm/Documents/Deadlock-Turniere/frontend/dist` und nicht aus dem Website-Repo (`/home/naniadm/Documents/Website/dl-brand/nav.js`, `/home/naniadm/Documents/Website/scripts/build-sitemap.mjs`, `/home/naniadm/Documents/Caddy/conf/Caddyfile`).

Caddy proxyt `/turnier/api/*` und `/turnier/auth/*` nach `127.0.0.1:8900`; `deadlock-turniere.service` arbeitet im Verzeichnis `/home/naniadm/Documents/Deadlock-Turniere` (`/home/naniadm/Documents/Caddy/conf/Caddyfile`, `/home/naniadm/.config/systemd/user/deadlock-turniere.service`).
