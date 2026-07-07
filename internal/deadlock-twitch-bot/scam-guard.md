---
title: Deadlock Twitch Bot Scam Guard
tags: [internal, deadlock-twitch-bot, scam-guard]
stand: 2026-07-07
quelle: Deadlock-Twitch-Bot
---

## Laufzeit

- Conversation Scam Guard hängt in der Chat-Pipeline nach Globalban und vor Spam-Autoban. (rust/crates/tb-chat/src/pipeline.rs)
- Der Guard bewertet Gesprächsverläufe mit einem MiniMax-basierten Judge und kennt die Modi `auto_ban`, `timeout` und `alert_only`. (rust/crates/tb-chat/src/conversation_scam.rs)
- Defaultwerte sind aktiv, Modus `auto_ban`, Schwelle `0.90`, Vorschlagsgrenze `0.70` und Timeout `600` Sekunden. (rust/crates/tb-chat/src/conversation_scam.rs)
- Der Guard bewertet Einzel-Pitches sofort und sonst erst, wenn ein Gespräch mindestens drei substanzielle Nachrichten enthält. (rust/crates/tb-chat/src/conversation_scam.rs)

## Daten

- `twitch_scam_guard_settings` hält Einstellungen pro Channel. (rust/migrations/20260618010000_conversation_scam_guard.sql)
- `twitch_scam_guard_verdicts` hält Urteil, Confidence, Kategorie, Begründung, Transcript-Snapshot, Aktion und Zeitstempel. (rust/migrations/20260618010000_conversation_scam_guard.sql)

## Dashboard

- Partner lesen und ändern die eigenen Einstellungen über `/twitch/api/v2/streamer/scam-guard/settings`; Admins können einen `streamer`-Parameter setzen. (rust/crates/tb-dashboard-api/src/handlers/scam_guard_settings.rs; rust/crates/tb-dashboard-api/src/lib.rs)
- Der Settings-Handler akzeptiert nur `auto_ban`, `timeout` und `alert_only` und validiert `0 <= suggestion_floor <= threshold <= 1`. (rust/crates/tb-dashboard-api/src/handlers/scam_guard_settings.rs)
- Die Queue zeigt eigene Verdicts mit `action_taken` in `suggested`, `banned` oder `timed_out` und liefert Details channelgebunden aus. (rust/crates/tb-dashboard-api/src/handlers/scam_guard_queue.rs)
- Enforce und Revoke laufen im Dashboard als Proxy zur internen API. (rust/crates/tb-dashboard-api/src/handlers/scam_guard_enforce.rs)

## Interne API

- Interne Scam-Guard-Routen liegen unter `/internal/twitch/v1/scam-guard/enforce` und `/internal/twitch/v1/scam-guard/revoke`. (rust/crates/tb-internal-api/src/lib.rs; rust/crates/tb-internal-api/src/handlers/scam_guard.rs)
- Die internen Handler verlangen privilegierte interne Authentifizierung und geben ohne passenden Port einen Service-Fehler zurück. (rust/crates/tb-internal-api/src/handlers/scam_guard.rs)
- `tb-bot` baut den Enforce-Port nur aus dem aktiven Chat-API-Port. (rust/bin/tb-bot/src/main.rs; rust/bin/tb-bot/src/scam_enforce_impl.rs)
- UNSICHER: Wenn `TB_CHAT_ENABLED=0` ist, ist Enforce wahrscheinlich nicht verfügbar, weil dann kein Chat-API-Port in `build_scam_enforce_port` eingeht. (rust/bin/tb-bot/src/chat_wiring.rs; rust/bin/tb-bot/src/main.rs; rust/bin/tb-bot/src/scam_enforce_impl.rs)
