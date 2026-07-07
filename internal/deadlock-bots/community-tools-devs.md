---
title: "community-tools — Dev-Notizen"
tags: [deadlock-bots, technik]
stand: 2026-07-07
quelle: "public/discord-server/community-tools.md (Für-Devs-Sektion)"
---
eingearbeitet in architektur.md

## Für Devs (knapp)
- Rust live: `dl-community/src/tags_ui.rs` + `tags.rs` (User-/Mod-Tags), `feedback_hub.rs`, `clips.rs`, `leave_survey.rs`, `faq.rs` (FAQ-Chat + Ticket-Auto-Help), `dm_assistant.rs` (DM-Hilfe), `dl-activity/src/lfg.rs` (Intent, Cooldown, Co-Player, Decision-Log)
- Player-Finder (`dl-activity/src/player_finder.rs`) existiert im Code, ist aber per Default deaktiviert (`PLAYER_FINDER_ENABLED=false`)
- Bug-Reporter (`cogs/bug_reporter.py`) wurde beim Rust-Cutover bewusst nicht portiert
