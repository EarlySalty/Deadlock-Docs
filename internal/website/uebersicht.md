---
title: "Website Übersicht"
tags: [website, intern, übersicht]
stand: 2026-07-07
quelle: "Website"
---
# Übersicht

Die öffentliche Domain wird aus statischen Roots und lokalen Reverse-Proxys zusammengesetzt; die Zuordnung steht in Caddy, die Frontend-Basen stehen in den Vite-Konfigurationen (`/home/naniadm/Documents/Caddy/conf/Caddyfile`, `/home/naniadm/Documents/Website/*/vite.config.*`).

## Portale

| Pfad | Code/Root | Mechanismus | Beleg |
|---|---|---|---|
| `/` | `deco-elevator-new` | Caddy matcht nur `/` und liefert `deco-elevator-new/index.html`; Assets für diese Landing kommen über `/new/*`. | `/home/naniadm/Documents/Caddy/conf/Caddyfile`, `/home/naniadm/Documents/Website/deco-elevator-new/index.html` |
| `/new/*` | `deco-elevator-new` | Caddy strippt `/new` und sucht `{path}`, `{path}/index.html`, dann `/index.html`. | `/home/naniadm/Documents/Caddy/conf/Caddyfile` |
| `/mitspieler/*`, `/survey/*`, `/guides/*`, `/helden/*`, `/beitreten/*` | `dl-landing/dist` | Caddy matcht diese Pfade in `@landing`; Vite baut mehrere HTML-Einstiege mit `rollupOptions.input`. | `/home/naniadm/Documents/Caddy/conf/Caddyfile`, `/home/naniadm/Documents/Website/dl-landing/vite.config.js` |
| `/patch/*` | `dl-patch/dist` | Caddy strippt `/patch`, liefert Assets direkt und fällt sonst auf `/index.html` zurück; das Portal ruft `/api/public/patch-timeline` und `/api/public/patch-notes`. | `/home/naniadm/Documents/Caddy/conf/Caddyfile`, `/home/naniadm/Documents/Website/dl-patch/src/patch.js` |
| `/aktivitaet/*` | `dl-activity/dist` | Caddy liefert statische Dateien aus `dl-activity/dist`; `/aktivitaet/api/*`, `/aktivitaet/auth/*` und `/aktivitaet/health` gehen nach `127.0.0.1:8768`. | `/home/naniadm/Documents/Caddy/conf/Caddyfile`, `/home/naniadm/Documents/Website/dl-activity/vite.config.js` |
| `/builds/*` | `dl-tierlist/dist` | Caddy liefert `dl-tierlist/dist`; `/builds/api/*` und `/builds/auth/*` gehen nach `127.0.0.1:8771`. | `/home/naniadm/Documents/Caddy/conf/Caddyfile`, `/home/naniadm/Documents/Website/dl-tierlist/vite.config.js` |
| `/coaching/*` | `dl-coaching/dist` | Caddy liefert `dl-coaching/dist`; `/coaching/api/*` geht nach `127.0.0.1:8772` und Caddy entfernt vorher `/coaching`. | `/home/naniadm/Documents/Caddy/conf/Caddyfile`, `/home/naniadm/Documents/Website/dl-coaching/vite.config.ts` |
| `/brand/*` | `dl-brand` | Caddy strippt `/brand` und liefert gemeinsame Brand-Dateien; `dl-brand/nav.js` enthält die sichtbaren Portal-Links. | `/home/naniadm/Documents/Caddy/conf/Caddyfile`, `/home/naniadm/Documents/Website/dl-brand/nav.js` |
| `/turnier/*` | `Deadlock-Turniere` | Caddy liefert das Turnier-Frontend aus einem anderen Repo und proxyt `/turnier/api/*` sowie `/turnier/auth/*` nach `127.0.0.1:8900`. | `/home/naniadm/Documents/Caddy/conf/Caddyfile`, `/home/naniadm/.config/systemd/user/deadlock-turniere.service` |

## Binaries und Dienste

| Name | Rolle | Beleg |
|---|---|---|
| `ddc-website-backend` | Rust-Binary für Website-Backend, Meta-API, Coaching-Plattform, Auth, Scrims und Patch-Public-Endpunkte. | `/home/naniadm/Documents/Website/builds/backend-rust/Cargo.toml`, `/home/naniadm/Documents/Website/builds/backend-rust/src/app.rs` |
| `deadlock-website-backend.service` | systemd-User-Service für `scripts/run_builds_backend.sh`; der Wrapper startet standardmäßig das Rust-Binary. | `/home/naniadm/.config/systemd/user/deadlock-website-backend.service`, `/home/naniadm/Documents/Website/scripts/run_builds_backend.sh` |
| `deadlock-web-rust.service` | systemd-User-Service für Dashboard `8766`, Stats `8768` und Tierlist `8771` aus `Deadlock-Bots`. | `/home/naniadm/.config/systemd/user/deadlock-web-rust.service` |
| `deadlock-turniere.service` | systemd-User-Service für das externe Turnier-Backend. | `/home/naniadm/.config/systemd/user/deadlock-turniere.service`, `/home/naniadm/.config/systemd/user/deadlock-turniere.service.d/30-rust-cutover.conf` |
| `run_dl_bot_service.sh` | Der aktive Rust-Bot-Wrapper setzt `WEBSITE_API_BASE` standardmäßig auf das lokale Website-Backend unter `127.0.0.1:8772/api`. | `/home/naniadm/Documents/Deadlock-Bots/scripts/run_dl_bot_service.sh` |

## Ports

| Port | Nutzung | Beleg |
|---:|---|---|
| `8772` | lokales Website-Backend für `/coaching/api/*` und Patch-Public-API; Default kommt aus `WEBSITE_BACKEND_PORT`. | `/home/naniadm/Documents/Caddy/conf/Caddyfile`, `/home/naniadm/Documents/Website/builds/backend-rust/src/config.rs` |
| `8768` | Activity-/Stats-Service hinter `/aktivitaet/api/*`, `/aktivitaet/auth/*` und `/aktivitaet/health`. | `/home/naniadm/Documents/Caddy/conf/Caddyfile`, `/home/naniadm/.config/systemd/user/deadlock-web-rust.service` |
| `8771` | Builds-/Tierlist-Backend hinter `/builds/api/*` und `/builds/auth/*`. | `/home/naniadm/Documents/Caddy/conf/Caddyfile`, `/home/naniadm/.config/systemd/user/deadlock-web-rust.service` |
| `8766` | Dashboard/Auth-Broker für zentrale Callbacks und generisches `/api/public/*` außerhalb der Patch-Spezialrouten. | `/home/naniadm/Documents/Caddy/conf/Caddyfile`, `/home/naniadm/Documents/Website/builds/backend-rust/src/config.rs` |
| `8900` | externes Turnier-Backend für `/turnier/api/*` und `/turnier/auth/*`. | `/home/naniadm/Documents/Caddy/conf/Caddyfile`, `/home/naniadm/.config/systemd/user/deadlock-turniere.service` |
| `5173`, `5174`, `5175`, `3000`, `3001` | lokale Vite-Dev-Ports für `dl-landing`, `dl-tierlist`, `dl-activity`, `builds/frontend` und `dl-coaching`. | `/home/naniadm/Documents/Website/dl-landing/vite.config.js`, `/home/naniadm/Documents/Website/dl-tierlist/vite.config.js`, `/home/naniadm/Documents/Website/dl-activity/vite.config.js`, `/home/naniadm/Documents/Website/builds/frontend/vite.config.ts`, `/home/naniadm/Documents/Website/dl-coaching/vite.config.ts` |
