---
title: "onboarding-und-invites — Dev-Notizen"
tags: [deadlock-bots, technik]
stand: 2026-07-07
quelle: "public/discord-server/onboarding-und-invites.md (Für-Devs-Sektion)"
---
## Für Devs (knapp)
- Rust: `dl-community/src/onboarding.rs` (+ `onboarding_steps.json`), `ai_onboarding.rs`, `tags_ui.rs`, `reaction_roles.rs`, Invite-Lounge-Watcher in `dl-community`; automatisierter Invite-Pfad im Steam-Bot: `steam-flows/src/betainvite/`
- Der User-Slash-Command `/betainvite` wurde entfernt; der Funnel ist nur noch über den Panel-Button (`betainvite:panel:start`, Admin: `/publish_betainvite_panel`) erreichbar
- Kanalnamen live: <#1464736918951432222>, <#1398021105339334666> (Server-as-Code-Renames)
