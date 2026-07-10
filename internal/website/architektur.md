---
title: "Website Architektur"
tags: [website, intern, architektur]
stand: 2026-07-10
quelle: "Website"
---
# Architektur

## Frontend-Struktur

Die Website ist kein einzelnes Frontend; Caddy hängt mehrere Vite-Builds und statische Roots unter feste Pfade (`/home/naniadm/Documents/Caddy/conf/Caddyfile`, `/home/naniadm/Documents/Website/*/vite.config.*`).

| Teil | Struktur | Beleg |
|---|---|---|
| `deco-elevator-new` | Statische Aufzug-Landing ohne Vite-Konfig im Projektwurzelbereich. | `/home/naniadm/Documents/Website/deco-elevator-new/index.html`, `/home/naniadm/Documents/Caddy/conf/Caddyfile` |
| `dl-landing` | Vite-Multi-Page-Build mit `home`, `mitspieler`, `survey`, `coaching`, `streamer`, `helden`, `guideAnfaenger` und `beitreten` als Inputs. | `/home/naniadm/Documents/Website/dl-landing/vite.config.js` |
| `dl-activity` | Vite-App mit `base: "/aktivitaet/"`, eigener Brand-Asset-Middleware und Chart.js. | `/home/naniadm/Documents/Website/dl-activity/vite.config.js`, `/home/naniadm/Documents/Website/dl-activity/package.json`, `/home/naniadm/Documents/Website/dl-activity/src/activity.js` |
| `dl-patch` | Vite-App mit `base: "/patch/"`; das Frontend lädt Patchdaten über absolute `/api/public/*`-Pfade. | `/home/naniadm/Documents/Website/dl-patch/vite.config.js`, `/home/naniadm/Documents/Website/dl-patch/src/patch.js` |
| `dl-tierlist` | Vite-Multi-Page-Build mit `home`, `history` und `admin`, ausgeliefert unter `/builds/`. | `/home/naniadm/Documents/Website/dl-tierlist/vite.config.js` |
| `dl-coaching` | React/Vite-App unter `/coaching/`; `App.tsx` definiert Routen für Coaches, Anfrage, Dashboard, Coachees, Spieleransicht und Scrims. | `/home/naniadm/Documents/Website/dl-coaching/vite.config.ts`, `/home/naniadm/Documents/Website/dl-coaching/src/App.tsx` |
| `builds/frontend` | **Legacy / nicht live geroutet.** Ältere React/Vite-App; Caddy liefert `/builds/` in Wirklichkeit aus `dl-tierlist/dist`, nicht von hier. Nur noch dev-preview. | `/home/naniadm/Documents/Website/builds/frontend/vite.config.ts`, `/home/naniadm/Documents/Caddy/conf/Caddyfile` |
| `dl-brand` | Gemeinsame Navigation und Tokens; `nav.js` baut Links zu Empfang, Mitspieler, Coaching, Aktivität, Patchnotes, Helden, Streamer und Beitreten. | `/home/naniadm/Documents/Website/dl-brand/nav.js`, `/home/naniadm/Documents/Caddy/conf/Caddyfile` |

## API-Basis im Browser

`dl-coaching` baut seine API-Basis aus `import.meta.env.BASE_URL` plus `/api`; bei `base: "/coaching/"` wird daraus `/coaching/api` (`/home/naniadm/Documents/Website/dl-coaching/src/api/client.ts`). Die live unter `/builds/` ausgelieferte Tierlist-App (`dl-tierlist`) spricht ihr Backend entsprechend unter `/builds/api` an (`/home/naniadm/Documents/Website/dl-tierlist/src/shared.js`).

`dl-activity` nutzt `VITE_API_BASE` oder die Vite-Base als Prefix und ruft darunter `/api/...` sowie `/auth/...` auf; Caddy entfernt bei `/aktivitaet/api/*` und `/aktivitaet/auth/*` den Prefix, bevor der Stats-Service auf `8768` die Anfrage sieht (`/home/naniadm/Documents/Website/dl-activity/src/activity.js`, `/home/naniadm/Documents/Caddy/conf/Caddyfile`).

`dl-patch` ruft `/api/public/patch-timeline` und `/api/public/patch-notes` ohne `/patch`-Prefix; Caddy mappt genau diese beiden Public-Endpunkte auf `127.0.0.1:8772` (`/home/naniadm/Documents/Website/dl-patch/src/patch.js`, `/home/naniadm/Documents/Caddy/conf/Caddyfile`).

## Rust-Backend

Das Rust-Backend heißt `ddc-website-backend`, nutzt Axum, Sqlx/Postgres, Reqwest und Tokio; die Cargo-Datei bindet `dl-central-db` per lokalem Pfad ein (`/home/naniadm/Documents/Website/builds/backend-rust/Cargo.toml`).

`main.rs` lädt `Config::from_env()`, baut `AppState`, erstellt den Router und bindet auf `WEBSITE_BACKEND_HOST:WEBSITE_BACKEND_PORT`, Default `127.0.0.1:8772` (`/home/naniadm/Documents/Website/builds/backend-rust/src/main.rs`, `/home/naniadm/Documents/Website/builds/backend-rust/src/config.rs`).

`AppState::new` öffnet den zentralen Postgres-Pool, führt `db::init` als Smoke-Check aus, erstellt einen Reqwest-Client, Auth-Helfer und Discord-Role-Clients; danach startet der Discord-Role-Sync-Worker (`/home/naniadm/Documents/Website/builds/backend-rust/src/app.rs`, `/home/naniadm/Documents/Website/builds/backend-rust/src/db.rs`).

## Router-Gruppen

| Gruppe | Pfade | Handler-Datei | Beleg |
|---|---|---|---|
| Health und Patch-Public | `/api/health`, `/api/public/patch-timeline`, `/api/public/patch-notes` | `routes/mod.rs`, `routes/public.rs` | `/home/naniadm/Documents/Website/builds/backend-rust/src/app.rs`, `/home/naniadm/Documents/Website/builds/backend-rust/src/routes/public.rs` |
| Auth | `/api/auth/discord/login`, `/api/auth/discord/callback`, `/api/auth/me`, `/api/auth/logout` | `routes/auth.rs` | `/home/naniadm/Documents/Website/builds/backend-rust/src/app.rs`, `/home/naniadm/Documents/Website/builds/backend-rust/src/routes/auth.rs` |
| Discord Linked Role | `/api/auth/discord/linked-role/*`, `/api/admin/discord-role-connections/metadata`, `/api/internal/discord-role-connections/sync` | `routes/linked_role.rs` | `/home/naniadm/Documents/Website/builds/backend-rust/src/app.rs`, `/home/naniadm/Documents/Website/builds/backend-rust/src/routes/linked_role.rs` |
| Meta | `/api/heroes`, `/api/builds`, `/api/items`, `/api/tierlists`, `/api/patchnotes`, `/api/history`, `/api/admin/*` | `routes/meta.rs` | `/home/naniadm/Documents/Website/builds/backend-rust/src/app.rs`, `/home/naniadm/Documents/Website/builds/backend-rust/src/routes/meta.rs` |
| Coaching | `/api/coaching/coaches`, `/api/coaching/requests`, `/api/coaching/surveys`, `/api/coaching/dashboard`, `/api/coaching/sessions/*` | `routes/coaching.rs` | `/home/naniadm/Documents/Website/builds/backend-rust/src/app.rs`, `/home/naniadm/Documents/Website/builds/backend-rust/src/routes/coaching.rs` |
| Coaching-Plattform | `/api/coaching/platform/*` | `routes/platform.rs` | `/home/naniadm/Documents/Website/builds/backend-rust/src/app.rs`, `/home/naniadm/Documents/Website/builds/backend-rust/src/routes/platform.rs` |
| Scrims | `/api/scrim/*` | `routes/scrim.rs` | `/home/naniadm/Documents/Website/builds/backend-rust/src/app.rs`, `/home/naniadm/Documents/Website/builds/backend-rust/src/routes/scrim.rs` |

## Legacy

Legacy: Der Wrapper enthält noch einen Python-Zweig für `WEBSITE_BACKEND_IMPL=python`, aber die gelesene Live-Unit startet `scripts/run_builds_backend.sh` mit Default `rust` und der Rust-Zweig verlangt `builds/backend-rust/target/release/ddc-website-backend`. Die Website-Doku beschreibt deshalb das Rust-Backend als Laufzeitpfad (`/home/naniadm/.config/systemd/user/deadlock-website-backend.service`, `/home/naniadm/Documents/Website/scripts/run_builds_backend.sh`, `/home/naniadm/Documents/Website/builds/backend-rust/src/main.rs`).
