---
title: "tierlist-und-builds — Dev-Notizen"
tags: [deadlock-bots, technik]
stand: 2026-07-08
quelle: "public/discord-server/tierlist-und-builds.md (Für-Devs-Sektion)"
---
eingearbeitet in architektur.md

## Für Devs (knapp)
- Rust live: `dl-tierlist` (Public-API: Heroes/Tierlist/History/Votes + Admin-Routes inkl. Refresh; Settings: 8h-Intervall, min_matches 500, Buckets `all`/`phantom_plus`/`eternus`; Sortierung `(sort_order, votes)` in `data.rs`)
- Der Steam-Build-Sync ist in Rust aktiv: `steam-core` registriert `BUILD_PUBLISH`, `BUILD_DELETE`, `MAINTAIN_BUILD_CATALOG` und `BUILD_CATALOG_CYCLE`; der Catalog-Scheduler plant `MAINTAIN_BUILD_CATALOG`. Details stehen in `internal/deadlock-steam-bot/uebersicht.md` und `internal/deadlock-steam-bot/task-queue.md`. (`steam-core/src/task/handlers/builds/`, `steam-core/src/main.rs`)
- Wichtige DB-Tabellen: Schema `tierlist.*` (Settings, Snapshots, Votes, Streamer, Hero-Meta); `steam.steam_tasks` gehört zum Steam-Schema
