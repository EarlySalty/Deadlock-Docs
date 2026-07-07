---
title: "voice-features — Dev-Notizen"
tags: [deadlock-bots, technik]
stand: 2026-07-07
quelle: "public/discord-server/voice-features.md (Für-Devs-Sektion)"
---
## Für Devs (knapp)
- Rust live: `dl-voice/src/tempvoice/` (engine + interface: Staging, Buttons, Presets, Tag-Filter, Owner-Claim-Regeln), `router.rs` (Router-VC, Smart-Routing), `adaptive.rs` (New-Player-/Off-Topic-/Sortier-Automatik), `rank.rs` (Anker, Subrang-Fenster ±9, Overwrites), `status.rs` (Kanalstatus), `stats.rs` (`!vstats`, Leaderboards, Admin-Debug), `feedback.rs` (Feedback-DM + Modal), `nudge.rs` (Steam-Link-DM), `tracker.rs` (Sessions, respektiert Privacy-Opt-out)
- Admin: Panel-Post per `!tvpanel`/`!tempvoicepanel`/`!tvinterface`
