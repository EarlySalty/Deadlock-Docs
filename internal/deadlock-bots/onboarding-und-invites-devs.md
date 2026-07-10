---
title: "onboarding-und-invites — Dev-Notizen"
tags: [deadlock-bots, technik]
stand: 2026-07-10
quelle: "public/discord-server/onboarding-und-invites.md (Für-Devs-Sektion)"
---
eingearbeitet in architektur.md

## Für Devs (knapp)
- Rust: `dl-community/src/onboarding.rs` (+ `onboarding_steps.json`), `ai_onboarding.rs`, `tags_ui.rs`, `reaction_roles.rs`, Invite-Lounge-Watcher in `dl-community`; automatisierter Invite-Pfad im Steam-Bot: `steam-flows/src/betainvite/`
- Der Slash-Command `/betainvite` existiert weiter im Rust-Event-Ingress und routet auf `betainvite:panel:start`. Operativ nutzen wir ihn nicht als automatischen Bot-Invite-Weg; der Community-Weg bleibt Frag-Kanal plus veröffentlichtes Panel. (`steam-web/src/routes/events.rs`)
- Kanalnamen live: <#1464736918951432222>, <#1398021105339334666> (Server-as-Code-Renames)

## Invite-Lounge-Watcher — wann der Freundescode-Tipp feuert

Der Watcher (`rust/crates/dl-community/src/invite_lounge.rs`) hört auf jede Nachricht im Kanal `1426220702054355077` und antwortet als reine Text-Reply mit `INVITE_LOUNGE_HINT_TEXT`. Kein Panel, kein Button, kein Slash-Command. Gespawnt wird er in `rust/bin/dl-bot/src/main.rs` über `invite_lounge::spawn`.

Geantwortet wird nur, wenn alle vier Bedingungen zugleich gelten (`should_reply`):

1. Nachricht kommt aus einer Guild und aus genau diesem Kanal.
2. Der Autor ist neu auf dem Server: `author_joined_at` liegt weniger als `NEWCOMER_MAX_JOIN_SECONDS` (7 Tage) zurück. Das Beitrittsdatum stammt aus dem Gateway-Member-Objekt der Nachricht (`dl-discord/src/gateway.rs`), kein zusätzlicher API-Call. Ist es unbekannt (`None`), wird nicht geantwortet — fail-closed.
3. Der Text sieht nach Invite-Frage aus: enthält "invite", "einlad", "playtest" oder "beta" (umlautgefaltet) **und** ein Fragesignal ("?" oder eines von wer/mag/kann/könnte/jemand/würde/hätte).
4. Der Text enthält noch keinen Freundescode: keine 6- bis 12-stellige Zahl, kein Link auf `steamcommunity.com` oder `s.team/p/`.

Danach greift ein Cooldown von 24 h pro Autor, gespeichert in `bot.kv_store` unter der Namespace `invite_lounge:cooldown`, Key `user:<id>`.

Das 7-Tage-Fenster ist bewusst dasselbe wie `NEW_MEMBER_MAX_JOIN_HOURS = 168` in `dl-moderation/src/behavior_detector.rs`, aber als eigene Konstante geführt: `dl-community` hängt nicht von `dl-moderation` ab.

**Warum die Neu-Prüfung existiert (2026-07-10):** Vorher entschied allein der Text. Dadurch antwortete der Bot auch Stammmitgliedern, die einem Neuling halfen ("Ich kann dich gerne im Laufe des Tages einladen" enthält "einlad" + "kann"). Genau dieser Satz liegt jetzt als Regressionstest `veteran_mit_invite_frage_triggert_nicht` in der Datei.
