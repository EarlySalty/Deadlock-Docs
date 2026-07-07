---
title: Deadlock Twitch Bot Knowledge und FAQ
tags: [internal, deadlock-twitch-bot, knowledge, faq]
stand: 2026-07-07
quelle: Deadlock-Twitch-Bot
---

## Quelle

- Kuratierte Bot-Inhalte liegen als Markdown unter `rust/knowledge/bot/*.md`. (rust/knowledge/bot/faq-einstieg.md; rust/knowledge/bot/faq-funktionen.md; rust/knowledge/bot/faq-raids.md)
- `tb-knowledge` lädt Markdown-Dateien aus Namespaces, liest Frontmatter und baut daraus deterministische Treffer für Grounding. (rust/crates/tb-knowledge/src/lib.rs)
- Der Code beschreibt den Ansatz ausdrücklich als kuratierte Auswahl und nicht als RAG. (rust/crates/tb-knowledge/src/lib.rs)

## Bot-Nutzung

- `tb-bot` lädt die Knowledge-Base aus `KNOWLEDGE_DIR` oder aus `rust/knowledge`, wenn `KNOWLEDGE_DIR` fehlt. (rust/bin/tb-bot/src/chat_wiring.rs)
- Die Knowledge-Base fließt in Tips, Go-Live-Tipps und Engagement-Antworten ein. (rust/bin/tb-bot/src/chat_wiring.rs; rust/crates/tb-tips/src/lib.rs; rust/crates/tb-engagement/src/lib.rs)

## Website-Nutzung

- Die Website importiert `rust/knowledge/bot/*.md` beim Build und extrahiert daraus Titel, Abschnitte und Listen. (website/src/v2/lib/knowledge.ts)
- Die FAQ-Reihenfolge ist im Website-Code fest verdrahtet und umfasst Einstieg, Funktionen, Raids, Stats-Overlay, Analytics, Community, Werbung, Pläne, Affiliate und Support. (website/src/v2/lib/knowledge.ts)
- `website/vite.config.ts` erlaubt dem Build den Zugriff auf den Repo-Root, damit diese Knowledge-Dateien gelesen werden können. (website/vite.config.ts)

## Pflegegrenze

- Änderungen an FAQ-Inhalten gehören in `rust/knowledge/bot/*.md`, weil Bot und Website diese Quelle lesen. (rust/crates/tb-knowledge/src/lib.rs; website/src/v2/lib/knowledge.ts)
- Alte Markdown-Dokumente unter `docs/` oder `rust/docs/` sind keine Laufzeitquelle für Bot-Knowledge. (rust/crates/tb-knowledge/src/lib.rs; website/src/v2/lib/knowledge.ts)
