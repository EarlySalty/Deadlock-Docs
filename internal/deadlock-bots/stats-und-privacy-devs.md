---
title: "stats-und-privacy — Dev-Notizen"
tags: [deadlock-bots, technik]
stand: 2026-07-07
quelle: "public/discord-server/stats-und-privacy.md (Für-Devs-Sektion)"
---
## Für Devs (knapp)
- Rust live: Public-Stats-Service `dl-stats` (Web-API inkl. `/api/public/me/*` + Discord-OAuth), Prefix-Stats in `dl-activity/src/stats_cmd.rs` + `text_stats.rs`, Privacy in `dl-community/src/privacy_ui.rs` + `privacy.rs` (Export mit Schwärzung, Erasure inkl. Turnier-Scope, Opt-out-Tombstone `core.user_privacy`), Retention in `dl-community/src/retention.rs`
- Voice- und Steam-Systeme respektieren das Privacy-Opt-out beim Schreiben (`dl-voice/src/tracker.rs`, Steam-Leave-Cleanup)
