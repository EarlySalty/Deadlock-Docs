---
title: "faq-bot-selbst — Dev-Notizen"
tags: [deadlock-bots, technik]
stand: 2026-07-07
quelle: "public/discord-server/faq-bot-selbst.md (Für-Devs-Sektion)"
---
## Für Devs (knapp)
- Rust live: `dl-community/src/faq.rs` — Panel (`/faqpanel`, idempotentes Panel-Healing), `/faq`, Button `faq_chat:start`, Close-Button `faq_chat:close:{session}`, Ticket-Auto-Help (Kategorie-Check + KEIN_TREFFER-Protokoll), Twitch-Diagnose-Tool
- Grounding: flacher Loader für `docs/*.md` (`load_docs`), Verlauf = letzte 10 Nachrichten
- Wichtige DB-Tabellen: `bot.faq_chat_sessions`, `bot.faq_chat_messages`, Panel-ID im KV (`faq_chat:panel`)
- Python `cogs/faq_chat.py`/`server_faq.py` sind Legacy (dort lebte `/faqclose` + `server_faq_logs`)
