---
title: Deadlock Twitch Bot Integrationen
tags: [internal, deadlock-twitch-bot, integrationen]
stand: 2026-07-07
quelle: Deadlock-Twitch-Bot
---

## Twitch Helix

- `HelixClient` kapselt `reqwest`, App-Token-Refresh, User-Token-Anfragen, Timeouts, Retry für 500/502/503/504 und Cooldown bei `invalid_client`. (rust/crates/tb-transport-twitch/src/client.rs)
- Der Bot baut Helix aus `TWITCH_CLIENT_ID` und `TWITCH_CLIENT_SECRET` und nutzt den Client für Monitoring, Raid, Chat und OAuth-Folgeaktionen. (rust/bin/tb-bot/src/main.rs; rust/bin/tb-bot/src/oauth_followups.rs; rust/bin/tb-bot/src/chat_wiring.rs)
- Chat-Nachrichten gehen über Helix `/helix/chat/messages`; der Client erzwingt bei einer ersten 401 einen Token-Refresh und wiederholt einmal. (rust/crates/tb-chat/src/moderation.rs)

## Twitch EventSub

- Der EventSub-Receiver nimmt nur signierte Webhook-Requests an und prüft `sha256=`-Signaturen über Message-ID, Timestamp und Body. (rust/crates/tb-monitoring/src/webhook_receiver.rs)
- Die Subscription-Verwaltung erstellt Core-Subscriptions für `stream.online`, `stream.offline` und `channel.update`; Chat- und Telemetrie-Subscriptions kommen ergänzend dazu. (rust/crates/tb-monitoring/src/subscriptions.rs; rust/bin/tb-bot/src/chat_wiring.rs)
- Der Dispatcher kennt Core-, Chat- und Telemetrie-Events und leitet sie in Inbox, Hooks oder Telemetrie-Stores. (rust/crates/tb-monitoring/src/dispatch.rs)

## Discord

- Der Bot nutzt `BrokerRelay` gegen den Master-Broker und ruft interne Discord-Pfade für Rich-Messages, Rollen, Invites, DMs, Member und Role-Lookups auf. (rust/crates/tb-transport-discord/src/relay.rs)
- `BrokerRelay` setzt `X-Internal-Token`, eine deterministische Idempotency-Key-Header und einen 10-Sekunden-Timeout. (rust/crates/tb-transport-discord/src/relay.rs)
- Twitch-OAuth-Folgeaktionen lösen Discord-User auf und vergeben Streamer-Rollen über den Broker. (rust/bin/tb-bot/src/oauth_followups.rs)
- Der Dashboard-Admin-Login nutzt einen lokalen Discord-OAuth-Broker auf `127.0.0.1:8766`. (rust/crates/tb-dashboard-api/src/auth/discord_admin_login.rs)

## Interne API 8776

- Die interne API liegt unter `/internal/twitch/v1`, läuft im Rust-Bot und bindet im Live-Setup auf Port `8776`. (rust/crates/tb-internal-api/src/lib.rs; rust/bin/tb-bot/src/main.rs; rust/scripts/run_tb_bot_service.sh)
- Die API verlangt Loopback und `X-Internal-Token`. (rust/crates/tb-internal-api/src/lib.rs)
- Die API bietet Health, EventSub-Dispatch, Raid, Streamer-Invites, Chat-Commands, Globalban, Diagnose, Raid-Blacklist, Monitoring, Market-Share, Self-Explainer, Scam-Guard, Spam-Learning, Raid-OAuth, Link-Klicks, Stats, Analytics und Debug-Routen. (rust/crates/tb-internal-api/src/lib.rs)
- Dashboard-Handler bilden interne Aktionen auf diese API ab und verwenden `TWITCH_INTERNAL_API_TOKEN` plus `TWITCH_INTERNAL_API_BASE_URL` oder Host/Port-Fallbacks. (rust/crates/tb-dashboard-api/src/handlers/scam_guard_enforce.rs; rust/crates/tb-dashboard-api/src/handlers/admin_chat_action.rs; rust/crates/tb-dashboard-api/src/handlers/raid_pages.rs; rust/crates/tb-dashboard-api/src/handlers/self_explainer.rs)

## Website

- Die Streamer-Website wird aus `website/dist` ausgeliefert, wenn `WEBSITE_DIST_PATH` nicht gesetzt ist. (rust/crates/tb-dashboard-api/src/handlers/website.rs)
- Die Website nutzt `/streamer/` als Vite-Base und darf beim Build die Knowledge-Dateien unter `rust/knowledge/bot/*.md` lesen. (website/vite.config.ts)
- Öffentliche Links zeigen auf `/twitch/onboarding`, `/twitch/faq`, `/twitch/auth/login`, `/twitch/dashboard`, `/twitch/dashboard-v2`, `/twitch/affiliate`, `/social-media` und `/twitch/raid/auth`. (website/src/data/externalLinks.ts)
