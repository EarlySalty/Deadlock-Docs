---
title: "onboarding-und-invites — Dev-Notizen"
tags: [deadlock-bots, technik]
stand: 2026-07-08
quelle: "public/discord-server/onboarding-und-invites.md (Für-Devs-Sektion)"
---
eingearbeitet in architektur.md

## Für Devs (knapp)
- Rust: `dl-community/src/onboarding.rs` (+ `onboarding_steps.json`), `ai_onboarding.rs`, `tags_ui.rs`, `reaction_roles.rs`, Invite-Lounge-Watcher in `dl-community`; automatisierter Invite-Pfad im Steam-Bot: `steam-flows/src/betainvite/`
- Der Slash-Command `/betainvite` existiert weiter im Rust-Event-Ingress und routet auf `betainvite:panel:start`. Operativ nutzen wir ihn nicht als automatischen Bot-Invite-Weg; der Community-Weg bleibt Frag-Kanal plus veröffentlichtes Panel. (`steam-web/src/routes/events.rs`)
- Kanalnamen live: <#1464736918951432222>, <#1398021105339334666> (Server-as-Code-Renames)
