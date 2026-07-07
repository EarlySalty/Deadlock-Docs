---
title: "Website Doku Bericht"
tags: [website, intern, bericht]
stand: 2026-07-07
quelle: "Website"
---
# Bericht

## Dateiliste

| Datei | Inhalt | Beleg |
|---|---|---|
| `uebersicht.md` | Portale, Binaries, systemd-Namen und Ports. | `/home/naniadm/Documents/Caddy/conf/Caddyfile`, `/home/naniadm/.config/systemd/user/deadlock-website-backend.service`, `/home/naniadm/Documents/Website/*/vite.config.*` |
| `architektur.md` | Frontend-Struktur, Rust-Backend und Router-Gruppen. | `/home/naniadm/Documents/Website/builds/backend-rust/src/app.rs`, `/home/naniadm/Documents/Website/dl-coaching/src/App.tsx`, `/home/naniadm/Documents/Website/builds/frontend/src/App.tsx` |
| `datenmodell.md` | Tabellen nach Core, Coaching, Scrims, Meta und Patchnotes. | `/home/naniadm/Documents/Website/builds/backend-rust/src/routes/*.rs`, `/home/naniadm/Documents/Deadlock-Bots/rust/crates/dl-central-db/migrations` |
| `betrieb.md` | Build, Deploy, Caddy-Zusammenspiel, Env-Var-Namen und Fallen. | `/home/naniadm/Documents/Website/scripts/run_builds_backend.sh`, `/home/naniadm/Documents/Website/builds/backend-rust/src/config.rs`, `/home/naniadm/Documents/Caddy/conf/Caddyfile` |
| `integrationen.md` | Bot-APIs, Coaching-Flow, Discord Linked Role und Turnier-Portal. | `/home/naniadm/Documents/Deadlock-Bots/rust/crates/dl-community/src/coaching.rs`, `/home/naniadm/Documents/Deadlock-Bots/service/website_client.py`, `/home/naniadm/Documents/Website/builds/backend-rust/src/routes/platform.rs` |
| `website-portale-technik.md` | Altdatei markiert als eingearbeitet. | `/home/naniadm/Documents/Deadlock-Docs/internal/website/website-portale-technik.md` |

## Veraltete Alt-Doku-Funde

`/home/naniadm/Documents/Website/docs/internal/deployment.md` nennt die `builds`-App noch als FastAPI-Anwendung; der aktuelle Wrapper startet bei Default `WEBSITE_BACKEND_IMPL=rust` das Rust-Binary `ddc-website-backend` (`/home/naniadm/Documents/Website/docs/internal/deployment.md`, `/home/naniadm/Documents/Website/scripts/run_builds_backend.sh`, `/home/naniadm/Documents/Website/builds/backend-rust/README.md`).

`/home/naniadm/Documents/Website/dl-tierlist/API-CONTRACT.md` beschreibt alte Singular-Endpunkte wie `/api/tierlist`; der Rust-Router definiert pluralisierte Meta-Endpunkte wie `/api/tierlists`, und Caddy leitet `/builds/api/*` produktiv nach `127.0.0.1:8771` (`/home/naniadm/Documents/Website/dl-tierlist/API-CONTRACT.md`, `/home/naniadm/Documents/Website/builds/backend-rust/src/app.rs`, `/home/naniadm/Documents/Caddy/conf/Caddyfile`).

`/home/naniadm/Documents/Website/dl-landing/setup.md` beschreibt IIS-Deployment und das Stoppen von Caddy; die aktive lokale Caddy-Konfiguration liefert Website-Pfade direkt aus Linux-Pfaden unter `/home/naniadm/Documents/Website` (`/home/naniadm/Documents/Website/dl-landing/setup.md`, `/home/naniadm/Documents/Caddy/conf/Caddyfile`).

`/home/naniadm/Documents/Website/docs/redesign-2026-07-website-vereinheitlichung.md` ist ein Redesign-/Rollout-Plan und wurde nicht als Betriebsquelle verwendet; die aktive Routenwahrheit steht in Caddy und Vite-Konfigurationen (`/home/naniadm/Documents/Website/docs/redesign-2026-07-website-vereinheitlichung.md`, `/home/naniadm/Documents/Caddy/conf/Caddyfile`, `/home/naniadm/Documents/Website/*/vite.config.*`).

## UNSICHER

UNSICHER: Das Website-Rust-Backend enthält Meta-Routen für `/api/builds`, `/api/tierlists` und weitere Meta-Pfade, aber Caddy routet produktiv `/builds/api/*` nach `127.0.0.1:8771`; die genaue Aufgabenteilung zwischen `8771` und `8772` ist nur über Caddy klar, nicht über eine zentrale Repo-Doku (`/home/naniadm/Documents/Website/builds/backend-rust/src/app.rs`, `/home/naniadm/Documents/Caddy/conf/Caddyfile`).

UNSICHER: Das Datenmodell für `/aktivitaet` liegt nicht im Website-Repo; das Frontend ruft `/aktivitaet/api/*` auf, und Caddy proxyt zum externen `8768`-Dienst aus `deadlock-web-rust.service` (`/home/naniadm/Documents/Website/dl-activity/src/activity.js`, `/home/naniadm/Documents/Caddy/conf/Caddyfile`, `/home/naniadm/.config/systemd/user/deadlock-web-rust.service`).

UNSICHER: Ein zentrales Linux-Deploy-Skript für alle Caddy-Roots liegt im Website-Repo nicht vor; gefunden wurden Paket-Builds, der Rust-Startwrapper und ein IIS-Deploy-Skript für `dl-landing` (`/home/naniadm/Documents/Website/*/package.json`, `/home/naniadm/Documents/Website/scripts/run_builds_backend.sh`, `/home/naniadm/Documents/Website/dl-landing/deploy_iis.ps1`).
