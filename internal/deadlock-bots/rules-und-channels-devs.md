---
title: "rules-und-channels — Dev-Notizen"
tags: [deadlock-bots, technik]
stand: 2026-07-07
quelle: "public/discord-server/rules-und-channels.md (Für-Devs-Sektion)"
---
## Für Devs (knapp)
- Rust live: `dl-community/src/onboarding.rs` (Panel + Threads + Screening-Autostart), `reaction_roles.rs`, `tags_ui.rs`, `privacy_ui.rs`, `retention.rs`; Ranked-Voice: `dl-voice/src/rank.rs` (Anker + Subrang-Fenster ±9 + Overwrites)
- Kanal-Renames aus Server-as-Code (`dl-server-as-code/src/rules.rs`) sind GEPLANT, aktuell aber zurückgerollt (Rechte-Incident 2026-07-03): `beta-zugang` → `deadlock-invite`, `rang-auswahl` → `deadlock-rang`, `lag-kompensator` → `server-support`, `hier-starten-regelwerk` → `regelwerk`; kommen mit der nächsten Struktur-Welle wieder
- Doku-Konvention: Kanäle IMMER als `<#ID>` schreiben (rename-fest), nie als Klartext-`#name`; neue Kanäle in die Register-Tabelle oben eintragen
- Wichtige DB-Tabellen: keine eigene Fach-Tabelle; Persistenz läuft über Onboarding- und KV-Mechaniken
