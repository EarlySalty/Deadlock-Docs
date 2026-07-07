---
title: "tierlist-und-builds — Dev-Notizen"
tags: [deadlock-bots, technik]
stand: 2026-07-07
quelle: "public/discord-server/tierlist-und-builds.md (Für-Devs-Sektion)"
---
## Für Devs (knapp)
- Rust live: `dl-tierlist` (Public-API: Heroes/Tierlist/History/Votes + Admin-Routes inkl. Refresh; Settings: 8h-Intervall, min_matches 500, Buckets `all`/`phantom_plus`/`eternus`; Sortierung `(sort_order, votes)` in `data.rs`)
- Der alte Steam-Build-Sync (`MAINTAIN_BUILD_CATALOG`/Build-Publisher-Worker) ist nicht nach Rust portiert; Upsert/Delete halten nur die DB konsistent (`dl-dashboard/src/deadlock.rs`)
- Wichtige DB-Tabellen: Schema `tierlist.*` (Settings, Snapshots, Votes, Streamer, Hero-Meta); `steam.steam_tasks` gehört zum Steam-Schema
