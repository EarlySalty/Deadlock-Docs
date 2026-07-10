---
title: "Website Betrieb"
tags: [website, intern, betrieb]
stand: 2026-07-10
quelle: "Website"
---
# Betrieb

## Build

| Teil | Build-Befehl | Ergebnis | Beleg |
|---|---|---|---|
| `dl-landing` | `npm run build` | Vite schreibt `dist`; `scripts.build` ist `vite build`. | `/home/naniadm/Documents/Website/dl-landing/package.json`, `/home/naniadm/Documents/Website/dl-landing/vite.config.js` |
| `dl-activity` | `npm run build` | Vite schreibt `dist`; die App hängt auf `base: "/aktivitaet/"`. | `/home/naniadm/Documents/Website/dl-activity/package.json`, `/home/naniadm/Documents/Website/dl-activity/vite.config.js` |
| `dl-patch` | `npm run build` | Vite schreibt `dist`; die App hängt auf `base: "/patch/"`. | `/home/naniadm/Documents/Website/dl-patch/package.json`, `/home/naniadm/Documents/Website/dl-patch/vite.config.js` |
| `dl-tierlist` | `npm run build` | Vite schreibt `dist`; die App hängt auf `base: "/builds/"`. | `/home/naniadm/Documents/Website/dl-tierlist/package.json`, `/home/naniadm/Documents/Website/dl-tierlist/vite.config.js` |
| `dl-coaching` | `npm run build` | `tsc && vite build`; die App hängt auf `base: "/coaching/"`. | `/home/naniadm/Documents/Website/dl-coaching/package.json`, `/home/naniadm/Documents/Website/dl-coaching/vite.config.ts` |
| `builds/frontend` | (Legacy, nicht deployt) | Baut zwar auf `base: "/builds/"`, wird aber nicht ausgeliefert — live `/builds/` ist `dl-tierlist/dist`. | `/home/naniadm/Documents/Website/builds/frontend/package.json`, `/home/naniadm/Documents/Caddy/conf/Caddyfile` |
| `builds/backend-rust` | `cargo build --release` | Release-Binary `target/release/ddc-website-backend`; der Startwrapper erwartet dieses Binary. | `/home/naniadm/Documents/Website/builds/backend-rust/README.md`, `/home/naniadm/Documents/Website/scripts/run_builds_backend.sh` |

## Deploy und Prozessstart

Caddy liest die produktiven statischen Dateien direkt aus dem Website-Repo. Die Root-Landing `/` kommt aus `deco-elevator-new` (kein Vite-Build, statisch); die weiteren Caddy-Roots zeigen auf `dl-landing/dist` (Landing-Unterseiten), `dl-activity/dist`, `dl-patch/dist`, `dl-tierlist/dist` (live unter `/builds/`) und `dl-coaching/dist` (`/home/naniadm/Documents/Caddy/conf/Caddyfile`).

`deadlock-website-backend.service` startet im Working Directory `/home/naniadm/Documents/Website` und ruft `scripts/run_builds_backend.sh` auf (`/home/naniadm/.config/systemd/user/deadlock-website-backend.service`).

`scripts/run_builds_backend.sh` lädt Infisical-Env, setzt OAuth-Callback-URLs für `/coaching/api/...`, nutzt `WEBSITE_BACKEND_IMPL=rust` als Default und startet `builds/backend-rust/target/release/ddc-website-backend` (`/home/naniadm/Documents/Website/scripts/run_builds_backend.sh`).

Der Rust-Start bricht ab, wenn das Release-Binary fehlt oder `DEADLOCK_CENTRAL_DSN` nach dem Infisical-Export nicht gesetzt ist; der Wrapper gibt dabei nur aus, ob die DSN vorhanden ist, nicht den Wert (`/home/naniadm/Documents/Website/scripts/run_builds_backend.sh`).

## Caddy-Zusammenspiel

| Pfad | Caddy-Ziel | Betriebsfolge | Beleg |
|---|---|---|---|
| `/coaching/api/*` | `127.0.0.1:8772` | Caddy entfernt `/coaching`; das Backend sieht `/api/...`. | `/home/naniadm/Documents/Caddy/conf/Caddyfile`, `/home/naniadm/Documents/Website/builds/backend-rust/src/app.rs` |
| `/api/public/patch-timeline`, `/api/public/patch-notes` | `127.0.0.1:8772` | Patch-Public-Daten laufen zum Website-Backend, obwohl das Portal unter `/patch` liegt. | `/home/naniadm/Documents/Caddy/conf/Caddyfile`, `/home/naniadm/Documents/Website/dl-patch/src/patch.js` |
| `/aktivitaet/api/*`, `/aktivitaet/auth/*`, `/aktivitaet/health` | `127.0.0.1:8768` | Caddy entfernt `/aktivitaet`; der Stats-Service muss `/api/*`, `/auth/*` und `/health` bedienen. | `/home/naniadm/Documents/Caddy/conf/Caddyfile`, `/home/naniadm/Documents/Website/dl-activity/src/activity.js` |
| `/builds/api/*`, `/builds/auth/*` | `127.0.0.1:8771` | Caddy entfernt `/builds`; der Dienst auf `8771` bedient Builds-/Auth-Pfade. | `/home/naniadm/Documents/Caddy/conf/Caddyfile`, `/home/naniadm/.config/systemd/user/deadlock-web-rust.service` |
| `/api/public/*` | `127.0.0.1:8766` | Generische Public-API geht zum Dashboard, außer die Patch-Spezialrouten greifen vorher. | `/home/naniadm/Documents/Caddy/conf/Caddyfile` |

## Env-Var-Namen

| Gruppe | Namen | Beleg |
|---|---|---|
| Backend-Bind | `WEBSITE_BACKEND_HOST`, `WEBSITE_BACKEND_PORT` | `/home/naniadm/Documents/Website/builds/backend-rust/src/config.rs` |
| Rust-Backend-Start | `WEBSITE_BACKEND_IMPL`, `RUST_BACKEND_BIN` | `/home/naniadm/Documents/Website/scripts/run_builds_backend.sh` |
| Infisical | `INFISICAL_CONFIG_FILE`, `INFISICAL_EXPORT_SCRIPT`, `INFISICAL_SERVICE_TOKEN`, `INFISICAL_RETRY_DELAY`, `INFISICAL_MAX_ATTEMPTS` | `/home/naniadm/Documents/Website/scripts/run_builds_backend.sh` |
| Datenbank | `DEADLOCK_CENTRAL_DSN`, `DB_MASTER_KEY_V1` | `/home/naniadm/Documents/Website/builds/backend-rust/src/db.rs`, `/home/naniadm/Documents/Website/builds/backend-rust/src/config.rs` |
| Sessions | `AUTH_COOKIE_NAME`, `AUTH_PRE_AUTH_COOKIE_NAME`, `AUTH_SESSION_TTL_SECONDS`, `AUTH_PRE_AUTH_TTL_SECONDS`, `AUTH_SESSION_AUDIENCE`, `AUTH_SESSION_ISSUER`, `AUTH_COOKIE_DOMAIN`, `AUTH_DDC_COOKIE_DOMAIN`, `AUTH_COOKIE_PATH`, `AUTH_COOKIE_SAMESITE`, `AUTH_SESSION_SECRET`, `JWT_SECRET`, `SESSIONS_ENCRYPTION_KEY` | `/home/naniadm/Documents/Website/builds/backend-rust/src/config.rs` |
| OAuth und Discord | `AUTH_PUBLIC_CALLBACK_URL`, `DISCORD_ROLE_CONNECTION_CALLBACK_URL`, `DISCORD_API_BASE`, `DISCORD_OAUTH_AUTHORIZE_BASE`, `DISCORD_AUTHORIZE_BASE`, `DISCORD_OAUTH_CLIENT_ID`, `DISCORD_CLIENT_ID`, `DISCORD_OAUTH_CLIENT_SECRET`, `DISCORD_CLIENT_SECRET`, `DISCORD_APPLICATION_ID`, `DISCORD_ROLE_CONNECTION_BOT_TOKEN`, `DISCORD_BOT_TOKEN`, `DISCORD_TOKEN`, `BOT_TOKEN`, `DISCORD_ROLE_CONNECTION_STATE_COOKIE_NAME`, `DISCORD_ROLE_CONNECTION_SYNC_WORKER_ENABLED`, `DISCORD_ROLE_CONNECTION_SYNC_INTERVAL_SECONDS` | `/home/naniadm/Documents/Website/builds/backend-rust/src/config.rs`, `/home/naniadm/Documents/Website/scripts/run_builds_backend.sh` |
| Interne APIs | `DASHBOARD_INTERNAL_API_BASE`, `MASTER_BROKER_BASE`, `MASTER_BROKER_TOKEN`, `MAIN_BOT_INTERNAL_TOKEN`, `TWITCH_INTERNAL_API_TOKEN`, `WEBSITE_INTERNAL_API_TOKEN`, `TURNIER_INTERNAL_API_TOKEN`, `COACHING_BOT_TOKEN` | `/home/naniadm/Documents/Website/builds/backend-rust/src/config.rs`, `/home/naniadm/Documents/Website/builds/backend-rust/src/routes/auth.rs`, `/home/naniadm/Documents/Website/builds/backend-rust/src/routes/coaching.rs` |
| Scrims | `SCRIM_GUILD_ID`, `SCRIM_RESERVE_ROLE_ID` | `/home/naniadm/Documents/Website/builds/backend-rust/src/config.rs`, `/home/naniadm/Documents/Website/builds/backend-rust/src/routes/scrim.rs` |
| Activity-Frontend | `VITE_API_BASE`, `VITE_AUTH_BASE` | `/home/naniadm/Documents/Website/dl-activity/src/activity.js` |

## Fallen

`/aktivitaet` hat einen Routing-Vertrag: das Frontend baut API- und Auth-URLs aus `VITE_API_BASE` oder `import.meta.env.BASE_URL`, hängt danach `/api/...` oder `/auth/...` an, und Caddy strippt `/aktivitaet`; Base-Änderungen müssen deshalb mit Caddy und dem `8768`-Dienst zusammen geändert werden (`/home/naniadm/Documents/Website/dl-activity/src/activity.js`, `/home/naniadm/Documents/Caddy/conf/Caddyfile`).

`/coaching` hat einen Callback-Vertrag: der Startwrapper setzt `AUTH_PUBLIC_CALLBACK_URL` und `DISCORD_ROLE_CONNECTION_CALLBACK_URL` auf URLs mit `/coaching/api/...`, weil Caddy den Prefix entfernt, bevor das Backend die Callback-Route sieht (`/home/naniadm/Documents/Website/scripts/run_builds_backend.sh`, `/home/naniadm/Documents/Caddy/conf/Caddyfile`).

`dl-patch` nutzt absolute `/api/public/*`-URLs; ein Proxy unter `/patch/api` hilft diesem Portal nicht, solange `dl-patch/src/patch.js` unverändert bleibt (`/home/naniadm/Documents/Website/dl-patch/src/patch.js`, `/home/naniadm/Documents/Caddy/conf/Caddyfile`).
