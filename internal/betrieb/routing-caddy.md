---
title: "Cross-System-Betrieb - Caddy-Routing"
tags: [internal, betrieb, caddy, routing]
stand: 2026-07-07
quelle: "Caddy Docker Compose und Caddyfile"
---
# Cross-System-Betrieb - Caddy-Routing

Caddy läuft als Docker-Container mit Host-Netzwerk.
Die aktive Konfiguration liegt unter `/home/naniadm/Documents/Caddy/conf/Caddyfile`.
Öffentliche Pfade werden fast immer auf Loopback-Ports oder statische `dist`-Verzeichnisse gemappt.

## Caddy-Laufzeit

| Baustein | Wert | Beleg |
|---|---|---|
| Container | `caddy:2.10-alpine` mit `container_name: caddy` | `Caddy/docker-compose.yml` |
| Netzwerk | `network_mode: host` | `Caddy/docker-compose.yml` |
| Konfiguration | `./conf` wird read-only nach `/etc/caddy` gemountet. | `Caddy/docker-compose.yml` |
| Website-Mounts | `Website`, `Deadlock-Twitch-Bot` und `Deadlock-Turniere/frontend/dist` werden read-only eingebunden. | `Caddy/docker-compose.yml` |

## Öffentliche Routen

| Route | Ziel | Beleg |
|---|---|---|
| `/callback/discord` | `127.0.0.1:8766` | `Caddy/conf/Caddyfile` |
| `/callback/twitch` | `127.0.0.1:8769` | `Caddy/conf/Caddyfile` |
| `/callback/steam` | Rewrite auf `/link/callback/steam`, dann `127.0.0.1:8783` | `Caddy/conf/Caddyfile` |
| `/twitch/eventsub/callback` | `127.0.0.1:8786` | `Caddy/conf/Caddyfile`; `Deadlock-Twitch-Bot/rust/bin/tb-bot/src/main.rs` |
| `/twitch/*`, `/analyse/*`, `/social-media/*`, `/demo/*`, `/raid/*` | Rust Twitch-Dashboard auf `127.0.0.1:8769`; nicht portierte Routen fallen intern auf Legacy-Fallback, wenn gesetzt. | `Caddy/conf/Caddyfile`; `Deadlock-Twitch-Bot/rust/scripts/run_tb_dashboard_service.sh` |
| `/link/*` | Rust Steam-Bot auf `127.0.0.1:8783`; `/link/health` wird zu `/health` umgeschrieben. | `Caddy/conf/Caddyfile`; `Deadlock-Steam-Bot/rust/crates/steam-bot/src/main.rs` |
| `/turnier/api/*`, `/turnier/auth/*` | Prefix `/turnier` wird entfernt, dann `127.0.0.1:8900`. | `Caddy/conf/Caddyfile`; `Deadlock-Turniere/rust/crates/turnier-config/src/lib.rs` |
| `/turnier*` | statisches Frontend aus `Deadlock-Turniere/frontend/dist` | `Caddy/conf/Caddyfile`; `Caddy/docker-compose.yml` |
| `/patch*` | statisches Frontend aus `Website/dl-patch/dist` | `Caddy/conf/Caddyfile` |
| `/api/public/patch-timeline`, `/api/public/patch-notes` | Website-Backend auf `127.0.0.1:8772` | `Caddy/conf/Caddyfile`; `Website/builds/backend-rust/src/config.rs` |
| `/api/public/*` | Master-Dashboard/API auf `127.0.0.1:8766` | `Caddy/conf/Caddyfile`; `Deadlock-Bots/rust/bin/dl-web/src/main.rs` |
| `/aktivitaet/api/*`, `/aktivitaet/auth/*`, `/aktivitaet/health` | Public-Stats auf `127.0.0.1:8768`; die restliche App kommt aus `Website/dl-activity/dist`. | `Caddy/conf/Caddyfile`; `Deadlock-Bots/rust/bin/dl-web/src/main.rs` |
| `/builds/api/*`, `/builds/auth/*` | Tierlist auf `127.0.0.1:8771`; die App kommt aus `Website/dl-tierlist/dist`. | `Caddy/conf/Caddyfile`; `Deadlock-Bots/rust/bin/dl-web/src/main.rs` |
| `/coaching/api/*` | Website-Backend auf `127.0.0.1:8772`; die App kommt aus `Website/dl-coaching/dist`. | `Caddy/conf/Caddyfile`; `Website/scripts/run_builds_backend.sh` |

## Admin-Subdomain

`admin.deutsche-deadlock-community.de` leitet Twitch-Admin-Auth, Panel und Admin-Support auf `127.0.0.1:8769`; generische Admin- und Fallback-Routen gehen auf `127.0.0.1:8766`. Öffentliche Twitch-, Analyse-, Social- und Demo-Pfade werden auf der Admin-Subdomain hart mit `404` beantwortet. (`Caddy/conf/Caddyfile`)

