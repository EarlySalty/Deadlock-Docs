---
title: "steam-integration — Dev-Notizen"
tags: [deadlock-bots, technik]
stand: 2026-07-07
quelle: "public/discord-server/steam-integration.md (Für-Devs-Sektion)"
---
eingearbeitet in integrationen.md

## Für Devs
Rust live: Panel/Commands in `Deadlock-Bots/rust/crates/dl-bridges/src/steam.rs`; Link-, Rank- und Invite-Flows im Steam-Bot (`steam-flows/src/link.rs`, `rank.rs`, `friend_sync.rs`, `betainvite/`), Web-Routen in `steam-web/src/routes/link.rs`. Verifizierung = OpenID-Link + bestätigte Bot-Freundschaft. Rank- und Invite-Funktionen greifen auf dieselbe Steam-Bridge zu, damit nicht mehrere Dienste direkt gegen Steam sprechen.
