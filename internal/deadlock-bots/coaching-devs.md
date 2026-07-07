---
title: "coaching — Dev-Notizen"
tags: [deadlock-bots, technik]
stand: 2026-07-07
quelle: "public/discord-server/coaching.md (Für-Devs-Sektion)"
---
eingearbeitet in integrationen.md

## Für Devs (knapp)
- Rust live: `dl-community/src/coaching_requests.rs` (Spiegelung, Claim/Release/Abort, Status, Survey, Sperren), `coaching.rs` (Coach-Rollen-Sync + Notification-Polling)
- Website: `builds/backend-rust/src/routes/coaching.rs` + `platform.rs` (Coach-Plattform), Frontend `dl-coaching/` (Anfrage-Seite `/anfrage`, Scrim-Anmeldung)
- Wichtige DB-Tabellen: Coaching-Anfragen/Sessions/Sperren zentral in Postgres; Anfragen entstehen auf der Website, nicht mehr im Discord-Modal
