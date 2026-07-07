---
title: Deadlock Twitch Bot Affiliate
tags: [internal, deadlock-twitch-bot, affiliate]
stand: 2026-07-07
quelle: Deadlock-Twitch-Bot
---

## Flow

- Affiliate-Onboarding startet über `/twitch/auth/affiliate/login` und endet über `/twitch/auth/affiliate/callback` in einer Affiliate-Session. (rust/crates/tb-dashboard-api/src/handlers/affiliate.rs)
- Stripe-Connect läuft über `/twitch/affiliate/connect/stripe` und `/twitch/affiliate/connect/stripe/callback`. (rust/crates/tb-dashboard-api/src/handlers/affiliate.rs)
- Streamer-Claims laufen über `/twitch/affiliate/claim` und API-Routen unter `/twitch/api/affiliate/*`. (rust/crates/tb-dashboard-api/src/handlers/affiliate.rs; rust/crates/tb-dashboard-api/src/lib.rs)
- Das Affiliate-Cookie heißt `twitch_affiliate_session`. (rust/crates/tb-dashboard-api/src/session.rs)

## Daten

- `affiliate_accounts` hält Affiliate-Account-Status, Twitch-ID, Twitch-Login, Stripe-Account und Payout-Status. (rust/migrations/20260617030000_baseline_missing_tables.sql)
- `affiliate_pii` hält personenbezogene Auszahlungsdaten getrennt vom Account. (rust/migrations/20260617030000_baseline_missing_tables.sql)
- `affiliate_streamer_claims` hält beanspruchte Streamer-Beziehungen. (rust/migrations/20260617030000_baseline_missing_tables.sql)
- `affiliate_commissions`, `affiliate_gutschrift_counter` und `affiliate_gutschriften` halten Provisionen und Gutschriften. (rust/migrations/20260617030000_baseline_missing_tables.sql)

## Admin und Job

- Admin-Routen liefern Affiliate-Stats, Listen, Detaildaten, Status-Toggle, Gutschriften und Gutschrift-Generierung. (rust/crates/tb-dashboard-api/src/handlers/admin_affiliate.rs)
- `tb-dashboard` startet einen Affiliate-Gutschrift-Loop, der nach 20 Sekunden beginnt und danach alle 6 Stunden läuft. (rust/bin/tb-dashboard/src/main.rs; rust/crates/tb-dashboard-api/src/handlers/admin_affiliate.rs)
- Der Gutschrift-Job nutzt Feldverschlüsselung und einen SMTP-Sender. (rust/crates/tb-dashboard-api/src/handlers/admin_affiliate.rs)

## Env-Namen

- Twitch-OAuth nutzt `TWITCH_CLIENT_ID` und `TWITCH_CLIENT_SECRET`. (rust/crates/tb-dashboard-api/src/handlers/affiliate.rs)
- Stripe-Connect nutzt `STRIPE_CONNECT_CLIENT_ID` und den Stripe-Secret-Key aus `STRIPE_SECRET_KEY` oder `TWITCH_BILLING_STRIPE_SECRET_KEY`. (rust/crates/tb-dashboard-api/src/handlers/affiliate.rs)
- Öffentliche URLs für Gutschriften kommen aus `TWITCH_PUBLIC_DASHBOARD_BASE_URL`, `TWITCH_PUBLIC_URL`, `PUBLIC_URL`, `TWITCH_ADMIN_PUBLIC_URL` oder `MASTER_DASHBOARD_PUBLIC_URL`. (rust/crates/tb-dashboard-api/src/handlers/admin_affiliate.rs)
