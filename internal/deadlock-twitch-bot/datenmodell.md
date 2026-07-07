---
title: Deadlock Twitch Bot Datenmodell
tags: [internal, deadlock-twitch-bot, datenmodell]
stand: 2026-07-07
quelle: Deadlock-Twitch-Bot
---

## Migrationen

- Die Rust-Migrationen sind die aktive Schemaquelle, weil `tb-db` `../../migrations` einbettet und `tb-dashboard` sie beim Start ausführt. (rust/crates/tb-db/src/migrate.rs; rust/bin/tb-dashboard/src/main.rs)
- `tb_schema_ownership` markiert `analytics_schema` als `rust`. (rust/crates/tb-db/src/migrate.rs; rust/migrations/20260702090000_schema_ownership.sql)

## Identität und Partner

- `twitch_streamers` hält Streamer-Logins und Twitch-User-IDs; spätere Migrationen entfernen die alte numerische ID und nutzen `twitch_login` als Schlüssel. (rust/migrations/20260601000000_baseline_schema.sql; rust/migrations/20260630140000_streamers_drop_legacy_id.sql)
- `twitch_partners` hält Partnerstatus, manuelle Flags, Raid-Bot-Flags, Live-Ping-Rollen und technische Pausen. (rust/migrations/20260601000000_baseline_schema.sql)
- `twitch_streamer_identities` verbindet Twitch-User mit Discord-Usern und Discord-Anzeigenamen. (rust/migrations/20260601000000_baseline_schema.sql)
- `twitch_partners_all_state` und `twitch_streamers_partner_state` materialisieren Partner- und Streamer-Zustände für Dashboard und Bot. (rust/migrations/20260601000000_baseline_schema.sql; rust/migrations/20260622130000_partner_state_keystone.sql; rust/migrations/20260623150000_drop_manual_verified_columns.sql)

## Live-Sessions

- `twitch_live_state` hält den aktuellen Live-Status, Stream-ID, Session-ID und Deadlock-Erkennung je Kanal. (rust/migrations/20260601000000_baseline_schema.sql)
- `twitch_stream_sessions` hält abgeschlossene und laufende Sessions mit Start, Ende, Viewern, Chatter-Zahlen, Titel, Sprache und Statusflags. (rust/migrations/20260601000000_baseline_schema.sql)
- `twitch_session_viewers` hält Zeitreihenpunkte pro Session und wird als Hypertable geführt. (rust/migrations/20260601000000_baseline_schema.sql; rust/migrations/20260630130000_reconcile_event_hypertables.sql)
- `twitch_session_chatters` hält Chatter-Präsenz und Zähler pro Session. (rust/migrations/20260601000000_baseline_schema.sql)

## EventSub

- `eventsub_guard_state` speichert Dedupe-Schlüssel mit Ablaufzeit. (rust/migrations/20260601000000_baseline_schema.sql; rust/crates/tb-monitoring/src/dispatch.rs)
- `twitch_eventsub_processing_inbox` hält Core-Events für asynchrone Verarbeitung. (rust/migrations/20260601000000_baseline_schema.sql; rust/crates/tb-monitoring/src/dispatch.rs)
- `twitch_eventsub_bridge_outbox`, `twitch_eventsub_bridge_dead_letter` und `twitch_eventsub_capacity_snapshot` bilden die Bridge- und Kapazitätsseite ab. (rust/migrations/20260601000000_baseline_schema.sql)

## Chat und Moderation

- `twitch_chat_messages` und `twitch_chatter_rollup` halten Chat-Verlauf und aggregierte Chatter-Daten. (rust/migrations/20260601000000_baseline_schema.sql)
- `twitch_chatter_global_ban` und `twitch_chatter_global_ban_applied` halten globale Ban-Regeln und deren Anwendung. (rust/migrations/20260601000000_baseline_schema.sql)
- `tb_chat_autoban_log`, `twitch_outbound_chat_suppressions`, `twitch_auto_learned_safe_patterns` und `twitch_auto_learned_spam_patterns` gehören zur Runtime-Moderation. (rust/migrations/20260630141000_chat_moderation_runtime_tables.sql)
- `twitch_scam_guard_settings` und `twitch_scam_guard_verdicts` halten Scam-Guard-Konfiguration und Urteile. (rust/migrations/20260618010000_conversation_scam_guard.sql)

## Raids

- `twitch_raid_auth` hält Raid-OAuth-Daten, Scopes, Status, Reauth-Flags und verschlüsselte Token-Spalten. (rust/migrations/20260601000000_baseline_schema.sql)
- `twitch_raid_history`, `twitch_raid_arrival_tracking`, `twitch_raid_retention`, `twitch_raid_blacklist` und `twitch_raid_disabled_strikes` halten Raid-Ausführung, Ankunft, Retention, Sperren und Strike-Status. (rust/migrations/20260601000000_baseline_schema.sql)
- `twitch_auto_raid_pause` steht in der Baseline, wird aber später als Legacy-Backup-Tabelle gelöscht. (rust/migrations/20260601000000_baseline_schema.sql; rust/migrations/20260630120000_drop_legacy_backup_tables.sql)

## Telemetrie und Features

- `20260630130000_reconcile_event_hypertables.sql` legt Hypertables für Ads, Bans, Bits, Channel-Points, Clips, EventSub-Kapazität, Follows, Hype-Trains, Link-Klicks, Raids, Sessions, Shoutouts, Statistik-Kategorien, Subscriptions und Viewers an. (rust/migrations/20260630130000_reconcile_event_hypertables.sql)
- Engagement nutzt Tabellen für Settings, Conversation, Logs, Stream-Transkripte, Sender-Auth und Self-Explainer. (rust/migrations/20260601000000_baseline_schema.sql; rust/migrations/20260628130000_engagement_sender_auth.sql; rust/migrations/20260617040000_self_explainer_feedback.sql)
- Social-Media-Features nutzen Tabellen für Clips, Upload-Queue, Analytics, Approval, Enrichment, Plattform-Auth, Settings, Templates und Reports. (rust/migrations/20260601000000_baseline_schema.sql)
- Billing nutzt `twitch_billing_subscriptions`, `twitch_billing_profiles` und `twitch_billing_events`. (rust/migrations/20260601000000_baseline_schema.sql; rust/migrations/20260617010000_billing_profiles.sql; rust/migrations/20260630144000_billing_events.sql)
- Affiliate nutzt `affiliate_accounts`, `affiliate_pii`, `affiliate_streamer_claims`, `affiliate_commissions`, `affiliate_gutschrift_counter` und `affiliate_gutschriften`. (rust/migrations/20260617030000_baseline_missing_tables.sql)
