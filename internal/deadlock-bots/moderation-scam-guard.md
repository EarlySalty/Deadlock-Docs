---
title: "Moderation und Scam-Guard"
tags: [deadlock-bots, intern, moderation, scam]
stand: 2026-07-07
quelle: Deadlock-Bots
---
# Moderation und Scam-Guard

Moderation besteht aus Content-Analyse, Verifikation, Verhaltensdetektor, Action-Policy und Case-Store. `dl-bot` verdrahtet Textanalyse, Bildanalyse und Verifikation, baut daraus `ModerationSystem` und registriert Review-Buttons mit Prefix `aimod:` (`rust/bin/dl-bot/src/main.rs`, `rust/crates/dl-moderation/src/lib.rs`, `rust/crates/dl-moderation/src/moderation_system.rs`).

Der Scanner läuft nur bei `AI_MODERATOR_ENABLE=1`. Auto-Vollzug hängt an `MODERATION_ENFORCE`, danach `MOD_ENFORCE`, danach `SECURITY_GUARD_ENFORCE`; ohne explizit wahre Variable läuft die Policy im Shadow-Modus (`rust/bin/dl-bot/src/main.rs`, `rust/crates/dl-moderation/src/moderation_system.rs`).

Content-Analyse nutzt Text und optional Vision. Text nutzt den Fireworks-Default aus `dl-ai`, Bildanalyse den OpenAI-Default; die Analyse wählt die schwerere Kategorie aus Text und Bild (`rust/crates/dl-ai/src/lib.rs`, `rust/crates/dl-moderation/src/content_analyzer.rs`).

High-Damage-Kategorien können bei bestätigter Verifikation und ausreichender Confidence automatisch Timeout auslösen. Account-Takeover-Signale können automatisch Timeout oder Bann auslösen; andere Verhaltenssignale brauchen Content-Bestätigung oder werden als Proposal behandelt (`rust/crates/dl-moderation/src/action_policy.rs`, `rust/crates/dl-moderation/src/behavior_detector.rs`).

Der Verhaltensdetektor arbeitet ohne LLM. Er erkennt Account-Takeover, Burst-Rate, junge Accounts mit Burst, Bildverteilung über mehrere Kanäle, fremde Invites und Scam-Keywords wie `telegram`, `100k`, `usdt`, `profit`, `promo code` und `earning $` (`rust/crates/dl-moderation/src/behavior_detector.rs`).

Staff wird fail-closed behandelt: Wenn der Staff-Status nicht bekannt ist, scannt der Bot die Nachricht nicht. Bekannte Staff-, Admin- oder `manage_messages`-Autoren werden ebenfalls übersprungen (`rust/crates/dl-moderation/src/moderation_system.rs`).

Ein Case muss zuerst in `moderation.ai_moderation_cases` persistieren. Erst danach löscht der Bot Nachrichten, setzt Timeout oder Bann, spiegelt Evidence-Bilder und postet den Review-Case in den Moderationskanal (`rust/crates/dl-moderation/src/store.rs`, `rust/crates/dl-moderation/src/moderation_system.rs`).

Review-Buttons können Cases akzeptieren, bannen, verwerfen, Timeout aufheben oder Bann aufheben. Diese Pfade lesen den Case aus der DB, prüfen, ob er schon behandelt ist, führen die Discord-Aktion aus und schreiben das Ergebnis zurück (`rust/crates/dl-moderation/src/moderation_system.rs`, `rust/crates/dl-moderation/src/store.rs`).

Moderationsinhalte werden nach 90 Tagen anonymisiert oder geleert. Der Privacy-Retention-Worker läuft alle 24 Stunden und bearbeitet `moderation.ai_moderation_cases`, `moderation.ai_moderation_ragebait_hits` und `moderation.security_guard_incidents` (`rust/crates/dl-community/src/privacy.rs`).
