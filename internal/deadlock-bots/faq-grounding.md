---
title: "FAQ-Grounding"
tags: [deadlock-bots, intern, faq, grounding]
stand: 2026-07-07
quelle: Deadlock-Bots
---
# FAQ-Grounding

Der FAQ-Chat ist in `dl-community` implementiert und wird im Bot-Prozess registriert. Der Panel-Button `faq_chat:start` öffnet einen privaten FAQ-Kanal, der Close-Button `faq_chat:close:{session}` schließt die Session, und Sessions laufen nach 24 Stunden ab (`rust/crates/dl-community/src/faq.rs`, `rust/bin/dl-bot/src/main.rs`).

Das Grounding lädt flach alle `*.md` aus `FAQ_DOCS_PATH`; ohne Env nutzt der Bot `docs`. Die Dateien werden sortiert, mit `=== Dokument: <name> ===` getrennt und als Wissensbasis in den Prompt geschrieben (`rust/bin/dl-bot/src/main.rs`, `rust/crates/dl-community/src/faq.rs`).

Der Chat speichert Sessions in `bot.faq_chat_sessions` und Nachrichten in `bot.faq_chat_messages`. Für den Kontext liest der Code die letzten 10 Nachrichten einer Session und sortiert sie wieder chronologisch (`rust/crates/dl-central-db/migrations/0007_bot.sql`, `rust/crates/dl-community/src/faq.rs`).

Der System-Prompt verbietet interne Pfade, Tokens, Secrets, Datenbank-URLs und erfundene Serverstrukturen. Sonderregeln überschreiben veraltete Invite- und Coaching-Aussagen: Invite läuft über Freundescode, Community-Einladung und Steam-Verknüpfung; Coaching läuft über den Coaching-Channel und die Website (`rust/crates/dl-community/src/faq.rs`).

Ticket-Auto-Help läuft auf die erste Nachricht in Ticket-Kanälen der Ticket-Kategorie. Der Bot antwortet nur bei dokumentierten Sach- und How-to-Fragen; bei Moderation, Konflikten, Sonderfällen oder unsicherem Status gibt er intern `KEIN_TREFFER` zurück und schweigt (`rust/crates/dl-community/src/faq.rs`).

Die Ticket-Diagnose kennt zwei Tools: `twitch_diagnose` und `log_lookup`. Beide sind auf den fragenden User begrenzt; Log-Zeilen werden auf den fragenden Discord-ID- oder Twitch-Login-Bezug gefiltert und danach redigiert (`rust/crates/dl-community/src/faq.rs`).

Vor einer Ticket-Antwort läuft ein Guard. Er blockiert deterministisch auf Secret-Muster, fremde Discord-IDs und lange gemischte Tokens; danach kann ein Textmodell mit `FREIGABE` oder `BLOCK` prüfen (`rust/crates/dl-community/src/faq.rs`).

Die FAQ-Panel-ID liegt im KV-Store unter Namespace `faq_chat:panel` und Schlüssel `panel_msg_id`, damit Rust ein bestehendes Panel übernehmen kann. Der Schlüsselname ist bewusst stabil gehalten (`rust/crates/dl-community/src/faq.rs`, `rust/crates/dl-central-db/migrations/0007_bot.sql`).

UNSICHER: Patchnote-Anreicherung ist im Rust-Kommentar als Lücke genannt. Der aktuelle FAQ-Pfad lädt Markdown-Dokus und Ticket-Tools, aber keine Patchnote-Anreicherung (`rust/crates/dl-community/src/faq.rs`).
