---
title: Deadlock Twitch Bot Architektur
tags: [internal, deadlock-twitch-bot, architektur]
stand: 2026-07-07
quelle: Deadlock-Twitch-Bot
---

## Crates

- Der Rust-Workspace enthält Domänen-, Config-, DB-, Transport-, Monitoring-, Raid-, Chat-, Dashboard-, Internal-API-, Social-, Highlight-, Engagement-, Knowledge-, Tips- und LLM-Crates. (rust/Cargo.toml)
- `bin/tb-bot` hängt an `tb-config`, `tb-db`, `tb-internal-api`, `tb-chat`, `tb-knowledge`, `tb-tips`, `tb-monitoring`, `tb-raid`, `tb-transport-twitch`, `tb-transport-discord`, `tb-social-media`, `tb-analytics`, `tb-highlight` und `tb-engagement`. (rust/bin/tb-bot/Cargo.toml)
- `bin/tb-dashboard` hängt an `tb-config`, `tb-db` und `tb-dashboard-api`. (rust/bin/tb-dashboard/Cargo.toml)

## Prozessgrenzen

- `tb-bot` erstellt die interne API und injiziert Helix, EventSub-Dispatcher, Raid-Ports, Chat-Ports, Scam-Guard-Ports, Analytics-Ports und Discord-Relay in den Router. (rust/bin/tb-bot/src/main.rs; rust/crates/tb-internal-api/src/lib.rs)
- `tb-dashboard` erstellt den Dashboard-Router und mischt öffentliche Routen, Auth-Routen, Affiliate-Routen, Admin-Routen, Billing-Routen, Website-Routen und SPA-Routen. (rust/bin/tb-dashboard/src/main.rs; rust/crates/tb-dashboard-api/src/lib.rs)
- `tb-dashboard` spricht für Scam-Guard-Aktionen, Chat-Aktionen, Raid-Seiten und Self-Explainer-Logs gegen die interne API des Bots. (rust/crates/tb-dashboard-api/src/handlers/scam_guard_enforce.rs; rust/crates/tb-dashboard-api/src/handlers/admin_chat_action.rs; rust/crates/tb-dashboard-api/src/handlers/raid_pages.rs; rust/crates/tb-dashboard-api/src/handlers/self_explainer.rs)

## EventSub-Fluss

- Twitch ruft `/twitch/eventsub/callback` auf, der Receiver prüft Message-ID, Timestamp, HMAC und ein Zeitfenster von 600 Sekunden. (rust/crates/tb-monitoring/src/webhook_receiver.rs)
- Verification-Events geben die Challenge zurück, Revocation-Events markieren Subscriptions als untrackbar, Notification-Events gehen an den Dispatcher. (rust/crates/tb-monitoring/src/webhook_receiver.rs)
- Der Dispatcher dedupliziert EventSub-Messages über `eventsub_guard_state` und leitet Core-Events wie `stream.online`, `stream.offline`, `channel.update` und `channel.raid` in `twitch_eventsub_processing_inbox`. (rust/crates/tb-monitoring/src/dispatch.rs; rust/migrations/20260601000000_baseline_schema.sql)
- Chat- und Telemetrie-Events laufen über EventSub-Hooks oder direkte Telemetrie-Stores, statt über die Core-Inbox. (rust/crates/tb-monitoring/src/dispatch.rs)

## Chat- und IRC-Fluss

- Native Chat ist nur aktiv, wenn `TB_CHAT_ENABLED=1` gesetzt ist. (rust/bin/tb-bot/src/chat_wiring.rs)
- Der Chat-Stack nutzt EventSub Webhooks für `channel.chat.message` und `channel.chat.notification`; ein Join ist eine Webhook-Subscription und kein WebSocket-Join. (rust/crates/tb-chat/src/lib.rs; rust/bin/tb-bot/src/chat_wiring.rs)
- `ChatHooks` nimmt Chat-Events aus EventSub an und reicht Message-Events an die Pipeline weiter. (rust/bin/tb-bot/src/chat_wiring.rs)
- Die Pipeline filtert eigene Nachrichten, bekannte Bots, Channel-Typen, globale Bans, Scam-Pitches, Spam, Invite-Verdacht, Fun-Antworten, Tracking, Engagement, Promo und Commands in fester Reihenfolge. (rust/crates/tb-chat/src/pipeline.rs)
- Ausgehende Chat-Aktionen laufen über `ChatApi` und den Helix-Chat-Client mit Bot-Token-Refresh. (rust/crates/tb-chat/src/api.rs; rust/crates/tb-chat/src/moderation.rs; rust/bin/tb-bot/src/chat_wiring.rs)
- Der IRC-Lurker ist ein anonymer Präsenzsammler, wenn `TB_IRC_LURKER_ENABLED=1` gesetzt ist; er synchronisiert Live-Kanäle aus `twitch_live_state` und schreibt Chatter-Präsenz. (rust/bin/tb-bot/src/irc_lurker_wiring.rs)

## Datenfluss

- Beide Binaries lesen `TWITCH_ANALYTICS_DSN` und bauen daraus einen PostgreSQL-Pool. (rust/crates/tb-config/src/lib.rs; rust/crates/tb-db/src/pool.rs)
- Rust-Migrationen liegen unter `rust/migrations` und werden über `sqlx::migrate!` eingebettet. (rust/crates/tb-db/src/migrate.rs)
- Der Schema-Owner-Marker `tb_schema_ownership` kennzeichnet `analytics_schema` als Rust-owned. (rust/crates/tb-db/src/migrate.rs; rust/migrations/20260702090000_schema_ownership.sql)

## Legacy

Legacy: Die alten Python-Units `deadlock-twitch-bot.service` und `deadlock-twitch-dashboard.service` existieren noch, waren beim Abgleich aber inaktiv. Die aktiven Live-Units starten `rust/target/release/tb-bot` und `rust/target/release/tb-dashboard` (`/home/naniadm/.config/systemd/user/deadlock-twitch-bot.service`, `/home/naniadm/.config/systemd/user/deadlock-twitch-dashboard.service`, `/home/naniadm/.config/systemd/user/deadlock-twitch-bot-rust.service`, `/home/naniadm/.config/systemd/user/deadlock-twitch-dashboard-rust.service`).
