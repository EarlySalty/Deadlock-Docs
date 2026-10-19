# Frische der internen Wissensseiten

Erzeugt: 2026-09-30 von `tools/check_freshness.py` aus `quellen.json`.

- ohne Eintrag in `quellen.json`: **0**
- veraltet: **75**, davon 31 mit genauer und 44 mit grober Bindung
- aktuell: 5
- unbekannt: 1
- nicht verfolgt: 2

`veraltet` heisst: seit dem geprueften Commit wurde in den gebundenen
Quellpfaden weitergearbeitet. Es heisst nicht, dass die Seite falsch ist,
sondern dass sie ungeprueft ist.

45 Seiten haben über alle Zustände hinweg grobe Bindungen. Davon sind 44
veraltet und eine unbekannt. Die 31 genau gebundenen veralteten Seiten
gehören deshalb zusammen mit den 44 grob gebundenen zum Gesamtwert 75.
Die bisherige Darstellung mischte diese beiden Zählmengen.

Die Commit-Zahlen grober Bindungen sind Obergrenzen, kein fachlicher Befund.
Wer eine solche Seite überarbeitet, trägt in `quellen.json` die genauen
Pfade nach. Eine Quellenänderung allein belegt keinen falschen Inhalt.

## veraltet (75)

### internal/deadlock-bots/stats-und-privacy-devs.html (genau, 381 Commits seit Pruefung)

Stand der Seite: 2026-07-12
- `Deadlock-Bots` (rust/crates/dl-activity, rust/crates/dl-community, rust/crates/dl-voice, rust/crates/dl-central-db) ab `3bc8ca8a` [explizit, genau]: 232 Commits, 144 Dateien
  - `rust/crates/dl-activity/Cargo.toml`
  - `rust/crates/dl-activity/src/analyzer.rs`
  - `rust/crates/dl-activity/src/db.rs`
  - `rust/crates/dl-activity/src/journey.rs`
  - `rust/crates/dl-activity/src/journey/voice_reconcile.rs`
  - `rust/crates/dl-activity/src/lfg_freetext.rs`
  - `rust/crates/dl-activity/src/lib.rs`
  - `rust/crates/dl-activity/src/outbox.rs`
  - … 136 weitere
- `Deadlock-Steam-Bot` (rust) ab `6fad947c` [explizit, grob]: 149 Commits, 198 Dateien
  - `rust/.sqlx/query-0206b6cdb9ad61c91d680e8938b06fd9f504d740e38fcd6e13c71881616f1d9d.json`
  - `rust/.sqlx/query-1045b3d8cc81ee6518f699e634cd7396ea5b0619312f291bc9a7cc73d70e1a32.json`
  - `rust/.sqlx/query-158079b4bdbfb714a7d4845bbc45bb1690f77595b07d53df9630f3a7e4639e3c.json`
  - `rust/.sqlx/query-2266eaf88d227d9de58ff57fcadca118b8f1e5d711cbea9499ddf1411ac1b449.json`
  - `rust/.sqlx/query-28b7acee3c82a1105ee3bc9df8d29bfb2c6328e95dfc51a1dea980ef68ef9263.json`
  - `rust/.sqlx/query-2be74e269e4364624ed0479bca9e1da5af4ce45bc4de5f0f071b993898b8940d.json`
  - `rust/.sqlx/query-2fb699804b88f1f704057f7becdceaabd31f175b4e52516db53c789dda092789.json`
  - `rust/.sqlx/query-30f98c7f1674cd5b47d4a26d88ec1c16a87d816bd982aaf1430b3fa060605328.json`
  - … 190 weitere
- `Deadlock-Docs` (public/discord-server/stats-und-privacy.html) ab `08c01ff0` [datum-abgeleitet, genau]: 0 Commits, 0 Dateien

### internal/betrieb/datenbank.html (genau, 104 Commits seit Pruefung)

Stand der Seite: 2026-07-07
- `Deadlock-Bots` (rust/crates/dl-central-db, rust/crates/dl-central-etl) ab `9669df25` [datum-abgeleitet, genau]: 104 Commits, 96 Dateien
  - `rust/crates/dl-central-db/Cargo.toml`
  - `rust/crates/dl-central-db/build.rs`
  - `rust/crates/dl-central-db/migrations/2026070913_invite_requests.sql`
  - `rust/crates/dl-central-db/migrations/2026071010_router_intro_dm_marker.sql`
  - `rust/crates/dl-central-db/migrations/2026071110_discord_audit_log.sql`
  - `rust/crates/dl-central-db/migrations/2026071111_steam_bot_event_log.sql`
  - `rust/crates/dl-central-db/migrations/2026071112_pate_journey_metadata_scrub.sql`
  - `rust/crates/dl-central-db/migrations/2026071120_invite_dispatch_claim.sql`
  - … 88 weitere

### internal/deadlock-bots/datenmodell.html (genau, 104 Commits seit Pruefung)

Stand der Seite: 2026-07-07
- `Deadlock-Bots` (rust/crates/dl-central-db) ab `9669df25` [datum-abgeleitet, genau]: 104 Commits, 96 Dateien
  - `rust/crates/dl-central-db/Cargo.toml`
  - `rust/crates/dl-central-db/build.rs`
  - `rust/crates/dl-central-db/migrations/2026070913_invite_requests.sql`
  - `rust/crates/dl-central-db/migrations/2026071010_router_intro_dm_marker.sql`
  - `rust/crates/dl-central-db/migrations/2026071110_discord_audit_log.sql`
  - `rust/crates/dl-central-db/migrations/2026071111_steam_bot_event_log.sql`
  - `rust/crates/dl-central-db/migrations/2026071112_pate_journey_metadata_scrub.sql`
  - `rust/crates/dl-central-db/migrations/2026071120_invite_dispatch_claim.sql`
  - … 88 weitere

### internal/deadlock-bots/voice-features-devs.html (genau, 78 Commits seit Pruefung)

Stand der Seite: 2026-07-11
- `Deadlock-Bots` (rust/crates/dl-voice) ab `7b0f35bb` [datum-abgeleitet, genau]: 76 Commits, 27 Dateien
  - `rust/crates/dl-voice/Cargo.toml`
  - `rust/crates/dl-voice/src/adaptive.rs`
  - `rust/crates/dl-voice/src/feedback.rs`
  - `rust/crates/dl-voice/src/glue.rs`
  - `rust/crates/dl-voice/src/lfg_panel.rs`
  - `rust/crates/dl-voice/src/lfg_watch.rs`
  - `rust/crates/dl-voice/src/lib.rs`
  - `rust/crates/dl-voice/src/mate_survey.rs`
  - … 19 weitere
- `Deadlock-Docs` (public/discord-server/voice-features.html) ab `5dfe43fb` [datum-abgeleitet, genau]: 2 Commits, 1 Dateien
  - `public/discord-server/voice-features.html`

### internal/deadlock-bots/faq-bot-selbst-devs.html (genau, 49 Commits seit Pruefung)

Stand der Seite: 2026-07-12
- `Deadlock-Bots` (rust/bin/dl-knowledge, rust/crates/dl-community/src/faq.rs, rust/crates/dl-community/src/concierge.rs) ab `3bc8ca8a` [explizit, genau]: 49 Commits, 33 Dateien
  - `rust/bin/dl-knowledge/Cargo.toml`
  - `rust/bin/dl-knowledge/README.md`
  - `rust/bin/dl-knowledge/examples/production_preflight.rs`
  - `rust/bin/dl-knowledge/src/dense/bench.rs`
  - `rust/bin/dl-knowledge/src/dense/cli.rs`
  - `rust/bin/dl-knowledge/src/dense/local.rs`
  - `rust/bin/dl-knowledge/src/dense/mod.rs`
  - `rust/bin/dl-knowledge/src/dense/store.rs`
  - … 25 weitere
- `Deadlock-Docs` (public/discord-server/faq-bot-selbst.html) ab `08c01ff0` [datum-abgeleitet, genau]: 0 Commits, 0 Dateien

### internal/deadlock-bots/faq-grounding.html (genau, 49 Commits seit Pruefung)

Stand der Seite: 2026-07-12
- `Deadlock-Bots` (rust/bin/dl-knowledge, rust/crates/dl-community/src/faq.rs, rust/crates/dl-community/src/concierge.rs) ab `3bc8ca8a` [explizit, genau]: 49 Commits, 33 Dateien
  - `rust/bin/dl-knowledge/Cargo.toml`
  - `rust/bin/dl-knowledge/README.md`
  - `rust/bin/dl-knowledge/examples/production_preflight.rs`
  - `rust/bin/dl-knowledge/src/dense/bench.rs`
  - `rust/bin/dl-knowledge/src/dense/cli.rs`
  - `rust/bin/dl-knowledge/src/dense/local.rs`
  - `rust/bin/dl-knowledge/src/dense/mod.rs`
  - `rust/bin/dl-knowledge/src/dense/store.rs`
  - … 25 weitere

### internal/deadlock-bots/support-agent-design.html (genau, 49 Commits seit Pruefung)

Stand der Seite: 2026-07-12
- `Deadlock-Bots` (rust/bin/dl-knowledge, rust/crates/dl-community/src/faq.rs, rust/crates/dl-community/src/concierge.rs) ab `3bc8ca8a` [explizit, genau]: 49 Commits, 33 Dateien
  - `rust/bin/dl-knowledge/Cargo.toml`
  - `rust/bin/dl-knowledge/README.md`
  - `rust/bin/dl-knowledge/examples/production_preflight.rs`
  - `rust/bin/dl-knowledge/src/dense/bench.rs`
  - `rust/bin/dl-knowledge/src/dense/cli.rs`
  - `rust/bin/dl-knowledge/src/dense/local.rs`
  - `rust/bin/dl-knowledge/src/dense/mod.rs`
  - `rust/bin/dl-knowledge/src/dense/store.rs`
  - … 25 weitere

### internal/deadlock-bots/onboarding-concierge-llm-compliance.html (genau, 46 Commits seit Pruefung)

Stand der Seite: 2026-07-07
- `Deadlock-Bots` (rust/crates/dl-community/src/concierge.rs) ab `9669df25` [datum-abgeleitet, genau]: 46 Commits, 1 Dateien
  - `rust/crates/dl-community/src/concierge.rs`

### internal/wissensbasis/dl-ai-provider.md (genau, 34 Commits seit Pruefung)

Stand der Seite: 2026-09-17
- `Deadlock-Bots` (rust/crates/dl-ai/src/lib.rs, rust/crates/dl-ai/src/chat_provider.rs, rust/crates/dl-ai/src/chat_text.rs, rust/bin/dl-knowledge/src/main.rs, rust/bin/dl-bot/src/main.rs, rust/crates/dl-community/src/concierge.rs) ab `bb03deb5` [explizit, genau]: 34 Commits, 6 Dateien
  - `rust/bin/dl-bot/src/main.rs`
  - `rust/bin/dl-knowledge/src/main.rs`
  - `rust/crates/dl-ai/src/chat_provider.rs`
  - `rust/crates/dl-ai/src/chat_text.rs`
  - `rust/crates/dl-ai/src/lib.rs`
  - `rust/crates/dl-community/src/concierge.rs`

### internal/wissensbasis/dl-bot-kern.md (genau, 26 Commits seit Pruefung)

Stand der Seite: 2026-09-19
- `Deadlock-Bots` (rust/bin/dl-bot/src/main.rs, rust/crates/dl-discord/src/interactions.rs, rust/crates/dl-discord/src/gateway.rs, rust/crates/dl-discord/src/dispatch.rs, rust/crates/dl-voice/src/router.rs) ab `bb03deb5` [explizit, genau]: 26 Commits, 4 Dateien
  - `rust/bin/dl-bot/src/main.rs`
  - `rust/crates/dl-discord/src/dispatch.rs`
  - `rust/crates/dl-discord/src/gateway.rs`
  - `rust/crates/dl-voice/src/router.rs`

### internal/deadlock-bots/twitch-clips-und-social.html (genau, 22 Commits seit Pruefung)

Stand der Seite: 2026-07-07
- `Deadlock-Bots` (docs/twitch-clips-und-social.md, rust/crates/dl-bridges) ab `9669df25` [datum-abgeleitet, genau]: 22 Commits, 6 Dateien
  - `rust/crates/dl-bridges/Cargo.toml`
  - `rust/crates/dl-bridges/src/lib.rs`
  - `rust/crates/dl-bridges/src/matcher.rs`
  - `rust/crates/dl-bridges/src/steam.rs`
  - `rust/crates/dl-bridges/src/steam_operating.rs`
  - `rust/crates/dl-bridges/src/twitch.rs`

### internal/deadlock-bots/onboarding-concierge-slice-b-c.html (genau, 21 Commits seit Pruefung)

Stand der Seite: 2026-07-11
- `Deadlock-Bots` (rust/crates/dl-community/src/concierge.rs, rust/crates/dl-voice/src/nudge.rs, rust/crates/dl-voice/src/feedback.rs) ab `7b0f35bb` [datum-abgeleitet, genau]: 21 Commits, 3 Dateien
  - `rust/crates/dl-community/src/concierge.rs`
  - `rust/crates/dl-voice/src/feedback.rs`
  - `rust/crates/dl-voice/src/nudge.rs`

### internal/deadlock-bots/onboarding-concierge-devs.html (genau, 19 Commits seit Pruefung)

Stand der Seite: 2026-07-11
- `Deadlock-Bots` (rust/crates/dl-community/src/concierge.rs) ab `b069b5c8` [explizit, genau]: 19 Commits, 1 Dateien
  - `rust/crates/dl-community/src/concierge.rs`

### internal/deadlock-bots/onboarding-concierge-texte.html (genau, 19 Commits seit Pruefung)

Stand der Seite: 2026-07-11
- `Deadlock-Bots` (rust/crates/dl-community/src/concierge.rs) ab `b069b5c8` [explizit, genau]: 19 Commits, 1 Dateien
  - `rust/crates/dl-community/src/concierge.rs`

### internal/wissensbasis/faq-entwurf/spielmechanik-matchablauf.md (genau, 18 Commits seit Pruefung)

Stand der Seite: 2026-09-19
- `Deadlock-Brain` (rust/docs/specs/2026-06-25-top-down-wissensmodell.md, rust/crates/dbrain-learn/src/build_optimizer.rs, rust/crates/dbrain-retrieval/src/lib.rs, rust/crates/dbrain-reasoner/src/mechanics.rs) ab `15bc1d3a` [explizit, genau]: 18 Commits, 2 Dateien
  - `rust/crates/dbrain-reasoner/src/mechanics.rs`
  - `rust/crates/dbrain-retrieval/src/lib.rs`
- `Deadlock-Docs` (internal/wissensbasis/faq-korpus-abdeckung.md) ab `9674a3cd` [explizit, genau]: 0 Commits, 0 Dateien
  - Hinweis: geprueft liegt nicht auf main; verglichen ab gemeinsamem Vorfahr 2c4b5de5 (meldet eher zu viel als zu wenig)

### internal/deadlock-bots/server-insights.html (genau, 17 Commits seit Pruefung)

Stand der Seite: 2026-07-07
- `Deadlock-Bots` (docs/server_insights.md, rust/crates/dl-stats) ab `9669df25` [datum-abgeleitet, genau]: 17 Commits, 3 Dateien
  - `docs/server_insights.md`
  - `rust/crates/dl-stats/src/me.rs`
  - `rust/crates/dl-stats/src/public.rs`

### internal/deadlock-bots/integrationen.html (genau, 16 Commits seit Pruefung)

Stand der Seite: 2026-07-11
- `Deadlock-Bots` (rust/crates/dl-bridges) ab `7b0f35bb` [datum-abgeleitet, genau]: 16 Commits, 6 Dateien
  - `rust/crates/dl-bridges/Cargo.toml`
  - `rust/crates/dl-bridges/src/lib.rs`
  - `rust/crates/dl-bridges/src/matcher.rs`
  - `rust/crates/dl-bridges/src/steam.rs`
  - `rust/crates/dl-bridges/src/steam_operating.rs`
  - `rust/crates/dl-bridges/src/twitch.rs`

### internal/deadlock-bots/moderation-scam-guard.html (genau, 13 Commits seit Pruefung)

Stand der Seite: 2026-07-07
- `Deadlock-Bots` (rust/crates/dl-moderation) ab `9669df25` [datum-abgeleitet, genau]: 13 Commits, 8 Dateien
  - `rust/crates/dl-moderation/src/action_policy.rs`
  - `rust/crates/dl-moderation/src/behavior_detector.rs`
  - `rust/crates/dl-moderation/src/case_embed.rs`
  - `rust/crates/dl-moderation/src/content_analyzer.rs`
  - `rust/crates/dl-moderation/src/content_verifier.rs`
  - `rust/crates/dl-moderation/src/lib.rs`
  - `rust/crates/dl-moderation/src/moderation_system.rs`
  - `rust/crates/dl-moderation/src/moderation_verdict.rs`

### internal/wissensbasis/dl-central-db.md (genau, 12 Commits seit Pruefung)

Stand der Seite: 2026-09-19
- `Deadlock-Bots` (rust/crates/dl-central-db/src/pool.rs, rust/crates/dl-central-db/src/locks.rs, rust/crates/dl-central-db/migrations, rust/bin/dl-central-migrate/src/main.rs, rust/crates/dl-central-db/tests/fresh_migrations_schema.rs) ab `bb03deb5` [explizit, genau]: 12 Commits, 9 Dateien
  - `rust/bin/dl-central-migrate/src/main.rs`
  - `rust/crates/dl-central-db/migrations/2026091802_knowledge_dense.sql`
  - `rust/crates/dl-central-db/migrations/2026092601_steam_build_publish_requests.sql`
  - `rust/crates/dl-central-db/migrations/2026092701_qualified_twitch_invites.sql`
  - `rust/crates/dl-central-db/migrations/2026093001_twitch_effort_read_access.sql`
  - `rust/crates/dl-central-db/migrations/2026093002_twitch_invite_qualification_readiness.sql`
  - `rust/crates/dl-central-db/migrations/2026093003_twitch_invite_identity.sql`
  - `rust/crates/dl-central-db/migrations/2026093004_twitch_invite_code_history.sql`
  - … 1 weitere

### internal/wissensbasis/dl-knowledge-engine.md (genau, 12 Commits seit Pruefung)

Stand der Seite: 2026-09-17
- `Deadlock-Bots` (rust/bin/dl-knowledge/src/main.rs) ab `bb03deb5` [explizit, genau]: 12 Commits, 1 Dateien
  - `rust/bin/dl-knowledge/src/main.rs`

### internal/wissensbasis/dl-web.md (genau, 8 Commits seit Pruefung)

Stand der Seite: 2026-09-19
- `Deadlock-Bots` (rust/bin/dl-web/src/main.rs, rust/crates/dl-webcore/src/config.rs, rust/crates/dl-dashboard/src/config.rs, rust/crates/dl-dashboard/src/authority.rs, rust/crates/dl-dashboard/src/web.rs) ab `bb03deb5` [explizit, genau]: 8 Commits, 4 Dateien
  - `rust/bin/dl-web/src/main.rs`
  - `rust/crates/dl-dashboard/src/config.rs`
  - `rust/crates/dl-dashboard/src/web.rs`
  - `rust/crates/dl-webcore/src/config.rs`

### internal/deadlock-bots/tierlist-und-builds-devs.html (genau, 6 Commits seit Pruefung)

Stand der Seite: 2026-07-08
- `Deadlock-Docs` (public/discord-server/tierlist-und-builds.html) ab `728368dc` [datum-abgeleitet, genau]: 6 Commits, 1 Dateien
  - `public/discord-server/tierlist-und-builds.html`

### internal/website/website-portale-technik.html (genau, 6 Commits seit Pruefung)

Stand der Seite: 2026-07-07
- `Deadlock-Docs` (public/website/website-portale.html) ab `89390f67` [datum-abgeleitet, genau]: 6 Commits, 1 Dateien
  - `public/website/website-portale.html`

### internal/deadlock-bots/rules-und-channels-devs.html (genau, 5 Commits seit Pruefung)

Stand der Seite: 2026-07-07
- `Deadlock-Docs` (public/discord-server/rules-und-channels.html) ab `89390f67` [datum-abgeleitet, genau]: 5 Commits, 1 Dateien
  - `public/discord-server/rules-und-channels.html`

### internal/wissensbasis/concierge-frontend.md (genau, 4 Commits seit Pruefung)

Stand der Seite: 2026-09-17
- `Deadlock-Bots` (rust/crates/dl-community/src/concierge.rs, rust/crates/dl-community/src/knowledge_client.rs) ab `bb03deb5` [explizit, genau]: 4 Commits, 2 Dateien
  - `rust/crates/dl-community/src/concierge.rs`
  - `rust/crates/dl-community/src/knowledge_client.rs`

### internal/wissensbasis/dl-community.md (genau, 4 Commits seit Pruefung)

Stand der Seite: 2026-09-19
- `Deadlock-Bots` (rust/crates/dl-community/src/onboarding.rs, rust/crates/dl-community/src/concierge.rs, rust/crates/dl-community/src/privacy.rs, rust/crates/dl-community/src/privacy_ui.rs, rust/crates/dl-central-db/src/locks.rs, rust/crates/dl-central-db/migrations/0007_bot.sql, rust/crates/dl-voice/src/router.rs) ab `bb03deb5` [explizit, genau]: 4 Commits, 2 Dateien
  - `rust/crates/dl-community/src/concierge.rs`
  - `rust/crates/dl-voice/src/router.rs`

### internal/deadlock-bots/steam-integration-devs.html (genau, 3 Commits seit Pruefung)

Stand der Seite: 2026-07-07
- `Deadlock-Docs` (public/discord-server/steam-integration.html) ab `89390f67` [datum-abgeleitet, genau]: 3 Commits, 1 Dateien
  - `public/discord-server/steam-integration.html`

### internal/deadlock-bots/coaching-devs.html (genau, 2 Commits seit Pruefung)

Stand der Seite: 2026-07-07
- `Deadlock-Docs` (public/discord-server/coaching.html) ab `89390f67` [datum-abgeleitet, genau]: 2 Commits, 1 Dateien
  - `public/discord-server/coaching.html`

### internal/deadlock-bots/community-tools-devs.html (genau, 2 Commits seit Pruefung)

Stand der Seite: 2026-07-11
- `Deadlock-Docs` (public/discord-server/community-tools.html) ab `5dfe43fb` [datum-abgeleitet, genau]: 2 Commits, 1 Dateien
  - `public/discord-server/community-tools.html`

### internal/deadlock-bots/onboarding-und-invites-devs.html (genau, 2 Commits seit Pruefung)

Stand der Seite: 2026-07-10
- `Deadlock-Docs` (public/discord-server/onboarding-und-invites.html) ab `91f8207a` [datum-abgeleitet, genau]: 2 Commits, 1 Dateien
  - `public/discord-server/onboarding-und-invites.html`

### internal/deadlock-bots/scrim-orga-redaction-notes.html (genau, 2 Commits seit Pruefung)

Stand der Seite: 2026-07-24
- `Deadlock-Docs` (public/dokus/scrims) ab `697f05d0` [datum-abgeleitet, genau]: 2 Commits, 1 Dateien
  - `public/dokus/scrims/scrim-orga.html`

### internal/deadlock-twitch-bot/affiliate.html (grob, 1696 Commits seit Pruefung)

Stand der Seite: 2026-07-07
- `Deadlock-Twitch-Bot` (rust, bot) ab `03822a50` [datum-abgeleitet, grob]: 1696 Commits, 1886 Dateien
  - `bot/__init__.py`
  - `bot/admin_dashboard/eslint.config.js`
  - `bot/admin_dashboard/package-lock.json`
  - `bot/admin_dashboard/package.json`
  - `bot/admin_dashboard/src/App.tsx`
  - `bot/admin_dashboard/src/api/brainLab.ts`
  - `bot/admin_dashboard/src/api/client.ts`
  - `bot/admin_dashboard/src/api/types.ts`
  - … 1878 weitere

### internal/deadlock-twitch-bot/integrationen.html (grob, 1696 Commits seit Pruefung)

Stand der Seite: 2026-07-07
- `Deadlock-Twitch-Bot` (rust, bot) ab `03822a50` [datum-abgeleitet, grob]: 1696 Commits, 1886 Dateien
  - `bot/__init__.py`
  - `bot/admin_dashboard/eslint.config.js`
  - `bot/admin_dashboard/package-lock.json`
  - `bot/admin_dashboard/package.json`
  - `bot/admin_dashboard/src/App.tsx`
  - `bot/admin_dashboard/src/api/brainLab.ts`
  - `bot/admin_dashboard/src/api/client.ts`
  - `bot/admin_dashboard/src/api/types.ts`
  - … 1878 weitere

### internal/deadlock-twitch-bot/uebersicht.html (grob, 1696 Commits seit Pruefung)

Stand der Seite: 2026-07-07
- `Deadlock-Twitch-Bot` (rust, bot) ab `03822a50` [datum-abgeleitet, grob]: 1696 Commits, 1886 Dateien
  - `bot/__init__.py`
  - `bot/admin_dashboard/eslint.config.js`
  - `bot/admin_dashboard/package-lock.json`
  - `bot/admin_dashboard/package.json`
  - `bot/admin_dashboard/src/App.tsx`
  - `bot/admin_dashboard/src/api/brainLab.ts`
  - `bot/admin_dashboard/src/api/client.ts`
  - `bot/admin_dashboard/src/api/types.ts`
  - … 1878 weitere

### internal/deadlock-twitch-bot/architektur.html (grob, 1428 Commits seit Pruefung)

Stand der Seite: 2026-07-18
- `Deadlock-Twitch-Bot` (rust, bot) ab `9e740716` [datum-abgeleitet, grob]: 1428 Commits, 1771 Dateien
  - `bot/__init__.py`
  - `bot/admin_dashboard/eslint.config.js`
  - `bot/admin_dashboard/package-lock.json`
  - `bot/admin_dashboard/package.json`
  - `bot/admin_dashboard/src/App.tsx`
  - `bot/admin_dashboard/src/api/brainLab.ts`
  - `bot/admin_dashboard/src/api/client.ts`
  - `bot/admin_dashboard/src/api/types.ts`
  - … 1763 weitere

### internal/deadlock-twitch-bot/datenmodell.html (grob, 1428 Commits seit Pruefung)

Stand der Seite: 2026-07-18
- `Deadlock-Twitch-Bot` (rust, bot) ab `9e740716` [datum-abgeleitet, grob]: 1428 Commits, 1771 Dateien
  - `bot/__init__.py`
  - `bot/admin_dashboard/eslint.config.js`
  - `bot/admin_dashboard/package-lock.json`
  - `bot/admin_dashboard/package.json`
  - `bot/admin_dashboard/src/App.tsx`
  - `bot/admin_dashboard/src/api/brainLab.ts`
  - `bot/admin_dashboard/src/api/client.ts`
  - `bot/admin_dashboard/src/api/types.ts`
  - … 1763 weitere

### internal/deadlock-twitch-bot/bot-trennen.html (grob, 1297 Commits seit Pruefung)

Stand der Seite: 2026-08-03
- `Deadlock-Twitch-Bot` (rust, bot) ab `22fd298d` [datum-abgeleitet, grob]: 1297 Commits, 1202 Dateien
  - `bot/admin_dashboard/eslint.config.js`
  - `bot/admin_dashboard/package-lock.json`
  - `bot/admin_dashboard/package.json`
  - `bot/admin_dashboard/src/App.tsx`
  - `bot/admin_dashboard/src/api/brainLab.ts`
  - `bot/admin_dashboard/src/api/client.ts`
  - `bot/admin_dashboard/src/api/types.ts`
  - `bot/admin_dashboard/src/components/layout/AdminShell.tsx`
  - … 1194 weitere

### internal/deadlock-twitch-bot/knowledge-faq.html (grob, 1258 Commits seit Pruefung)

Stand der Seite: 2026-07-07
- `Deadlock-Twitch-Bot` (rust, features) ab `03822a50` [datum-abgeleitet, grob]: 1258 Commits, 1058 Dateien
  - `rust/.cargo/audit.toml`
  - `rust/.sqlx/query-004ba92b98bdf1a1aa1755b0eee685c8b9ab83a6c566a3df29f4c8393cfba652.json`
  - `rust/.sqlx/query-00748f8a6734810c5b88b17f3db55311a86abaf4e77a2e2cb672e418c2e4d11c.json`
  - `rust/.sqlx/query-02a5b8176dcc3368deae56d6b19a152732cd2286b9e0e86e8f5a6b548f10514f.json`
  - `rust/.sqlx/query-04b227969422b64c03140040d7bd1b9daafa6afb1a4551652399895c7e9dbdd4.json`
  - `rust/.sqlx/query-04dc5e537dc37e55c45532a66ef09c4a0e4344971de5a6037002ebf556a7df5e.json`
  - `rust/.sqlx/query-059d1a2e654bd6abccfaf72c731ca9d424930efbcb6151b7b5b051d209eda6a7.json`
  - `rust/.sqlx/query-061406bc629371d66a7830dd84ff0960f996fb02d4768b97b29abee449899b19.json`
  - … 1050 weitere

### internal/deadlock-twitch-bot/pause-loop-obs.html (grob, 1060 Commits seit Pruefung)

Stand der Seite: 2026-07-20
- `Deadlock-Twitch-Bot` (rust, features) ab `a0a3f8d7` [datum-abgeleitet, grob]: 1009 Commits, 971 Dateien
  - `rust/.cargo/audit.toml`
  - `rust/.sqlx/query-004ba92b98bdf1a1aa1755b0eee685c8b9ab83a6c566a3df29f4c8393cfba652.json`
  - `rust/.sqlx/query-00748f8a6734810c5b88b17f3db55311a86abaf4e77a2e2cb672e418c2e4d11c.json`
  - `rust/.sqlx/query-02a5b8176dcc3368deae56d6b19a152732cd2286b9e0e86e8f5a6b548f10514f.json`
  - `rust/.sqlx/query-04b227969422b64c03140040d7bd1b9daafa6afb1a4551652399895c7e9dbdd4.json`
  - `rust/.sqlx/query-04dc5e537dc37e55c45532a66ef09c4a0e4344971de5a6037002ebf556a7df5e.json`
  - `rust/.sqlx/query-059d1a2e654bd6abccfaf72c731ca9d424930efbcb6151b7b5b051d209eda6a7.json`
  - `rust/.sqlx/query-061406bc629371d66a7830dd84ff0960f996fb02d4768b97b29abee449899b19.json`
  - … 963 weitere
- `Caddy` (.) ab `ed03744a` [datum-abgeleitet, grob]: 51 Commits, 11 Dateien
  - `.tasks/2026-09-26-devfeed-public/CONTRACT.md`
  - `CLAUDE.md`
  - `README.md`
  - `conf/Caddyfile`
  - `docker-compose.yml`
  - `hosts/v50671/Caddyfile`
  - `hosts/v50671/partner-profile-assets.caddy`
  - `hosts/v50671/partner-profiles.caddy`
  - … 3 weitere

### internal/deadlock-twitch-bot/betrieb.html (grob, 1011 Commits seit Pruefung)

Stand der Seite: 2026-07-27
- `Deadlock-Twitch-Bot` (ops, rust) ab `3b74c611` [datum-abgeleitet, grob]: 1011 Commits, 1020 Dateien
  - `ops/caddy/partner-profile-assets.caddy`
  - `ops/caddy/partner-profiles.caddy`
  - `ops/highlight-detector/.gitignore`
  - `ops/highlight-detector/config/gewichte.toml`
  - `ops/highlight-detector/config/regionen.toml`
  - `ops/highlight-detector/highlight-detector`
  - `ops/highlight-detector/highlight_detector/__init__.py`
  - `ops/highlight-detector/highlight_detector/__main__.py`
  - … 1012 weitere

### internal/deadlock-twitch-bot/scam-guard.html (grob, 962 Commits seit Pruefung)

Stand der Seite: 2026-07-27
- `Deadlock-Twitch-Bot` (rust, features) ab `3b74c611` [datum-abgeleitet, grob]: 962 Commits, 958 Dateien
  - `rust/.cargo/audit.toml`
  - `rust/.sqlx/query-004ba92b98bdf1a1aa1755b0eee685c8b9ab83a6c566a3df29f4c8393cfba652.json`
  - `rust/.sqlx/query-00748f8a6734810c5b88b17f3db55311a86abaf4e77a2e2cb672e418c2e4d11c.json`
  - `rust/.sqlx/query-02a5b8176dcc3368deae56d6b19a152732cd2286b9e0e86e8f5a6b548f10514f.json`
  - `rust/.sqlx/query-04b227969422b64c03140040d7bd1b9daafa6afb1a4551652399895c7e9dbdd4.json`
  - `rust/.sqlx/query-04dc5e537dc37e55c45532a66ef09c4a0e4344971de5a6037002ebf556a7df5e.json`
  - `rust/.sqlx/query-059d1a2e654bd6abccfaf72c731ca9d424930efbcb6151b7b5b051d209eda6a7.json`
  - `rust/.sqlx/query-061406bc629371d66a7830dd84ff0960f996fb02d4768b97b29abee449899b19.json`
  - … 950 weitere

### internal/deadlock-twitch-bot/smalltalk-shadow.html (grob, 962 Commits seit Pruefung)

Stand der Seite: 2026-07-27
- `Deadlock-Twitch-Bot` (rust, features) ab `3b74c611` [datum-abgeleitet, grob]: 962 Commits, 958 Dateien
  - `rust/.cargo/audit.toml`
  - `rust/.sqlx/query-004ba92b98bdf1a1aa1755b0eee685c8b9ab83a6c566a3df29f4c8393cfba652.json`
  - `rust/.sqlx/query-00748f8a6734810c5b88b17f3db55311a86abaf4e77a2e2cb672e418c2e4d11c.json`
  - `rust/.sqlx/query-02a5b8176dcc3368deae56d6b19a152732cd2286b9e0e86e8f5a6b548f10514f.json`
  - `rust/.sqlx/query-04b227969422b64c03140040d7bd1b9daafa6afb1a4551652399895c7e9dbdd4.json`
  - `rust/.sqlx/query-04dc5e537dc37e55c45532a66ef09c4a0e4344971de5a6037002ebf556a7df5e.json`
  - `rust/.sqlx/query-059d1a2e654bd6abccfaf72c731ca9d424930efbcb6151b7b5b051d209eda6a7.json`
  - `rust/.sqlx/query-061406bc629371d66a7830dd84ff0960f996fb02d4768b97b29abee449899b19.json`
  - … 950 weitere

### internal/deadlock-twitch-bot/crew-guard-radar.html (grob, 940 Commits seit Pruefung)

Stand der Seite: 2026-07-28
- `Deadlock-Twitch-Bot` (rust, features) ab `1283d481` [datum-abgeleitet, grob]: 940 Commits, 944 Dateien
  - `rust/.cargo/audit.toml`
  - `rust/.sqlx/query-004ba92b98bdf1a1aa1755b0eee685c8b9ab83a6c566a3df29f4c8393cfba652.json`
  - `rust/.sqlx/query-00748f8a6734810c5b88b17f3db55311a86abaf4e77a2e2cb672e418c2e4d11c.json`
  - `rust/.sqlx/query-02a5b8176dcc3368deae56d6b19a152732cd2286b9e0e86e8f5a6b548f10514f.json`
  - `rust/.sqlx/query-04b227969422b64c03140040d7bd1b9daafa6afb1a4551652399895c7e9dbdd4.json`
  - `rust/.sqlx/query-04dc5e537dc37e55c45532a66ef09c4a0e4344971de5a6037002ebf556a7df5e.json`
  - `rust/.sqlx/query-059d1a2e654bd6abccfaf72c731ca9d424930efbcb6151b7b5b051d209eda6a7.json`
  - `rust/.sqlx/query-061406bc629371d66a7830dd84ff0960f996fb02d4768b97b29abee449899b19.json`
  - … 936 weitere

### internal/deadlock-twitch-bot/verwaltung-selbstbedienung.html (grob, 901 Commits seit Pruefung)

Stand der Seite: 2026-08-03
- `Deadlock-Twitch-Bot` (rust, features) ab `22fd298d` [datum-abgeleitet, grob]: 901 Commits, 896 Dateien
  - `rust/.cargo/audit.toml`
  - `rust/.sqlx/query-004ba92b98bdf1a1aa1755b0eee685c8b9ab83a6c566a3df29f4c8393cfba652.json`
  - `rust/.sqlx/query-00748f8a6734810c5b88b17f3db55311a86abaf4e77a2e2cb672e418c2e4d11c.json`
  - `rust/.sqlx/query-02a5b8176dcc3368deae56d6b19a152732cd2286b9e0e86e8f5a6b548f10514f.json`
  - `rust/.sqlx/query-04b227969422b64c03140040d7bd1b9daafa6afb1a4551652399895c7e9dbdd4.json`
  - `rust/.sqlx/query-04dc5e537dc37e55c45532a66ef09c4a0e4344971de5a6037002ebf556a7df5e.json`
  - `rust/.sqlx/query-059d1a2e654bd6abccfaf72c731ca9d424930efbcb6151b7b5b051d209eda6a7.json`
  - `rust/.sqlx/query-061406bc629371d66a7830dd84ff0960f996fb02d4768b97b29abee449899b19.json`
  - … 888 weitere

### internal/deadlock-bots/architektur.html (grob, 611 Commits seit Pruefung)

Stand der Seite: 2026-07-07
- `Deadlock-Bots` (rust) ab `9669df25` [datum-abgeleitet, grob]: 611 Commits, 391 Dateien
  - `rust/.sqlx/query-00cbd620a306b6128f21c744d815c1f46d6698fe84aae23739772996b49402fc.json`
  - `rust/.sqlx/query-0328bf9078f50021b72b40dda4b6e3b755ad0045461bdeb2519ebdecde3f3f44.json`
  - `rust/.sqlx/query-115f831897ce9f7ec2e81cc7ac7e28021cdcab6aac51fda1e94d733304c8e43e.json`
  - `rust/.sqlx/query-14fdb6d7fa6d976e5890147a53bd1d7b31168661e01dcf2bb79aa6b0b8a4d61e.json`
  - `rust/.sqlx/query-1d13bd25d56c4bed501e77fafb48a37f383b758e6d8fda6d37eb086c026cdef6.json`
  - `rust/.sqlx/query-24dfe426673fcb6c5e23b9c7009cc42241b0627e2afd5ae99362b3fc9fd69c6b.json`
  - `rust/.sqlx/query-2dcc3b77350e59caef3af267e1ea961d664f450b424be977e7b2cbdd6c6027aa.json`
  - `rust/.sqlx/query-2e9682b2bb3267e7980b3b1bfab7697df0dabf5b7510ee803963dcc1344ec22d.json`
  - … 383 weitere

### internal/deadlock-bots/uebersicht.html (grob, 611 Commits seit Pruefung)

Stand der Seite: 2026-07-07
- `Deadlock-Bots` (rust) ab `9669df25` [datum-abgeleitet, grob]: 611 Commits, 391 Dateien
  - `rust/.sqlx/query-00cbd620a306b6128f21c744d815c1f46d6698fe84aae23739772996b49402fc.json`
  - `rust/.sqlx/query-0328bf9078f50021b72b40dda4b6e3b755ad0045461bdeb2519ebdecde3f3f44.json`
  - `rust/.sqlx/query-115f831897ce9f7ec2e81cc7ac7e28021cdcab6aac51fda1e94d733304c8e43e.json`
  - `rust/.sqlx/query-14fdb6d7fa6d976e5890147a53bd1d7b31168661e01dcf2bb79aa6b0b8a4d61e.json`
  - `rust/.sqlx/query-1d13bd25d56c4bed501e77fafb48a37f383b758e6d8fda6d37eb086c026cdef6.json`
  - `rust/.sqlx/query-24dfe426673fcb6c5e23b9c7009cc42241b0627e2afd5ae99362b3fc9fd69c6b.json`
  - `rust/.sqlx/query-2dcc3b77350e59caef3af267e1ea961d664f450b424be977e7b2cbdd6c6027aa.json`
  - `rust/.sqlx/query-2e9682b2bb3267e7980b3b1bfab7697df0dabf5b7510ee803963dcc1344ec22d.json`
  - … 383 weitere

### internal/website/uebersicht.html (grob, 196 Commits seit Pruefung)

Stand der Seite: 2026-07-07
- `Website` (builds, dl-coaching, dl-landing) ab `66a9c32b` [datum-abgeleitet, grob]: 196 Commits, 135 Dateien
  - `builds/backend-rust/Cargo.lock`
  - `builds/backend-rust/Cargo.toml`
  - `builds/backend-rust/DEPLOY-NOTES-video-bibliothek.md`
  - `builds/backend-rust/README.md`
  - `builds/backend-rust/migrations/2026071999_video_library.sql`
  - `builds/backend-rust/migrations/2026072000_video_action_audit.sql`
  - `builds/backend-rust/src/app.rs`
  - `builds/backend-rust/src/auth.rs`
  - … 127 weitere

### internal/deadlock-steam-bot/betrieb.html (grob, 192 Commits seit Pruefung)

Stand der Seite: 2026-07-08
- `Deadlock-Steam-Bot` (rust, scripts) ab `d8025714` [datum-abgeleitet, grob]: 192 Commits, 276 Dateien
  - `rust/.sqlx/query-016202238c2fe79d321d1f8c873d75585a5f0a35be607126b724b298e205fa8d.json`
  - `rust/.sqlx/query-0206b6cdb9ad61c91d680e8938b06fd9f504d740e38fcd6e13c71881616f1d9d.json`
  - `rust/.sqlx/query-04fcd77056839e21ca8270bca1c2c29328533082baf6dab083f0aa721df1d381.json`
  - `rust/.sqlx/query-0863636aa6ac78389deb8751d87fd069a1a7d27cd1f250423e735e082bbc2077.json`
  - `rust/.sqlx/query-0a32af394f4f16de182fbb55cd68e99fe6a1a9f44d17f32dc780b91ae37ba78d.json`
  - `rust/.sqlx/query-0d49b183c1421760ae41af8f85fb92e00118fa937162197241bfff1875ed0712.json`
  - `rust/.sqlx/query-1045b3d8cc81ee6518f699e634cd7396ea5b0619312f291bc9a7cc73d70e1a32.json`
  - `rust/.sqlx/query-123972121ed49650b28f6eddc1fe2b09b41e08158ff8dc2e889924b416426667.json`
  - … 268 weitere

### internal/deadlock-steam-bot/architektur.html (grob, 191 Commits seit Pruefung)

Stand der Seite: 2026-07-08
- `Deadlock-Steam-Bot` (rust) ab `d8025714` [datum-abgeleitet, grob]: 191 Commits, 274 Dateien
  - `rust/.sqlx/query-016202238c2fe79d321d1f8c873d75585a5f0a35be607126b724b298e205fa8d.json`
  - `rust/.sqlx/query-0206b6cdb9ad61c91d680e8938b06fd9f504d740e38fcd6e13c71881616f1d9d.json`
  - `rust/.sqlx/query-04fcd77056839e21ca8270bca1c2c29328533082baf6dab083f0aa721df1d381.json`
  - `rust/.sqlx/query-0863636aa6ac78389deb8751d87fd069a1a7d27cd1f250423e735e082bbc2077.json`
  - `rust/.sqlx/query-0a32af394f4f16de182fbb55cd68e99fe6a1a9f44d17f32dc780b91ae37ba78d.json`
  - `rust/.sqlx/query-0d49b183c1421760ae41af8f85fb92e00118fa937162197241bfff1875ed0712.json`
  - `rust/.sqlx/query-1045b3d8cc81ee6518f699e634cd7396ea5b0619312f291bc9a7cc73d70e1a32.json`
  - `rust/.sqlx/query-123972121ed49650b28f6eddc1fe2b09b41e08158ff8dc2e889924b416426667.json`
  - … 266 weitere

### internal/deadlock-steam-bot/datenmodell.html (grob, 191 Commits seit Pruefung)

Stand der Seite: 2026-07-08
- `Deadlock-Steam-Bot` (rust) ab `d8025714` [datum-abgeleitet, grob]: 191 Commits, 274 Dateien
  - `rust/.sqlx/query-016202238c2fe79d321d1f8c873d75585a5f0a35be607126b724b298e205fa8d.json`
  - `rust/.sqlx/query-0206b6cdb9ad61c91d680e8938b06fd9f504d740e38fcd6e13c71881616f1d9d.json`
  - `rust/.sqlx/query-04fcd77056839e21ca8270bca1c2c29328533082baf6dab083f0aa721df1d381.json`
  - `rust/.sqlx/query-0863636aa6ac78389deb8751d87fd069a1a7d27cd1f250423e735e082bbc2077.json`
  - `rust/.sqlx/query-0a32af394f4f16de182fbb55cd68e99fe6a1a9f44d17f32dc780b91ae37ba78d.json`
  - `rust/.sqlx/query-0d49b183c1421760ae41af8f85fb92e00118fa937162197241bfff1875ed0712.json`
  - `rust/.sqlx/query-1045b3d8cc81ee6518f699e634cd7396ea5b0619312f291bc9a7cc73d70e1a32.json`
  - `rust/.sqlx/query-123972121ed49650b28f6eddc1fe2b09b41e08158ff8dc2e889924b416426667.json`
  - … 266 weitere

### internal/deadlock-steam-bot/integrationen.html (grob, 191 Commits seit Pruefung)

Stand der Seite: 2026-07-08
- `Deadlock-Steam-Bot` (rust) ab `d8025714` [datum-abgeleitet, grob]: 191 Commits, 274 Dateien
  - `rust/.sqlx/query-016202238c2fe79d321d1f8c873d75585a5f0a35be607126b724b298e205fa8d.json`
  - `rust/.sqlx/query-0206b6cdb9ad61c91d680e8938b06fd9f504d740e38fcd6e13c71881616f1d9d.json`
  - `rust/.sqlx/query-04fcd77056839e21ca8270bca1c2c29328533082baf6dab083f0aa721df1d381.json`
  - `rust/.sqlx/query-0863636aa6ac78389deb8751d87fd069a1a7d27cd1f250423e735e082bbc2077.json`
  - `rust/.sqlx/query-0a32af394f4f16de182fbb55cd68e99fe6a1a9f44d17f32dc780b91ae37ba78d.json`
  - `rust/.sqlx/query-0d49b183c1421760ae41af8f85fb92e00118fa937162197241bfff1875ed0712.json`
  - `rust/.sqlx/query-1045b3d8cc81ee6518f699e634cd7396ea5b0619312f291bc9a7cc73d70e1a32.json`
  - `rust/.sqlx/query-123972121ed49650b28f6eddc1fe2b09b41e08158ff8dc2e889924b416426667.json`
  - … 266 weitere

### internal/deadlock-steam-bot/task-queue.html (grob, 191 Commits seit Pruefung)

Stand der Seite: 2026-07-08
- `Deadlock-Steam-Bot` (rust) ab `d8025714` [datum-abgeleitet, grob]: 191 Commits, 274 Dateien
  - `rust/.sqlx/query-016202238c2fe79d321d1f8c873d75585a5f0a35be607126b724b298e205fa8d.json`
  - `rust/.sqlx/query-0206b6cdb9ad61c91d680e8938b06fd9f504d740e38fcd6e13c71881616f1d9d.json`
  - `rust/.sqlx/query-04fcd77056839e21ca8270bca1c2c29328533082baf6dab083f0aa721df1d381.json`
  - `rust/.sqlx/query-0863636aa6ac78389deb8751d87fd069a1a7d27cd1f250423e735e082bbc2077.json`
  - `rust/.sqlx/query-0a32af394f4f16de182fbb55cd68e99fe6a1a9f44d17f32dc780b91ae37ba78d.json`
  - `rust/.sqlx/query-0d49b183c1421760ae41af8f85fb92e00118fa937162197241bfff1875ed0712.json`
  - `rust/.sqlx/query-1045b3d8cc81ee6518f699e634cd7396ea5b0619312f291bc9a7cc73d70e1a32.json`
  - `rust/.sqlx/query-123972121ed49650b28f6eddc1fe2b09b41e08158ff8dc2e889924b416426667.json`
  - … 266 weitere

### internal/deadlock-steam-bot/uebersicht.html (grob, 191 Commits seit Pruefung)

Stand der Seite: 2026-07-08
- `Deadlock-Steam-Bot` (rust) ab `d8025714` [datum-abgeleitet, grob]: 191 Commits, 274 Dateien
  - `rust/.sqlx/query-016202238c2fe79d321d1f8c873d75585a5f0a35be607126b724b298e205fa8d.json`
  - `rust/.sqlx/query-0206b6cdb9ad61c91d680e8938b06fd9f504d740e38fcd6e13c71881616f1d9d.json`
  - `rust/.sqlx/query-04fcd77056839e21ca8270bca1c2c29328533082baf6dab083f0aa721df1d381.json`
  - `rust/.sqlx/query-0863636aa6ac78389deb8751d87fd069a1a7d27cd1f250423e735e082bbc2077.json`
  - `rust/.sqlx/query-0a32af394f4f16de182fbb55cd68e99fe6a1a9f44d17f32dc780b91ae37ba78d.json`
  - `rust/.sqlx/query-0d49b183c1421760ae41af8f85fb92e00118fa937162197241bfff1875ed0712.json`
  - `rust/.sqlx/query-1045b3d8cc81ee6518f699e634cd7396ea5b0619312f291bc9a7cc73d70e1a32.json`
  - `rust/.sqlx/query-123972121ed49650b28f6eddc1fe2b09b41e08158ff8dc2e889924b416426667.json`
  - … 266 weitere

### internal/website/architektur.html (grob, 189 Commits seit Pruefung)

Stand der Seite: 2026-07-10
- `Website` (builds, dl-coaching, dl-landing) ab `f305c821` [datum-abgeleitet, grob]: 189 Commits, 132 Dateien
  - `builds/backend-rust/Cargo.lock`
  - `builds/backend-rust/Cargo.toml`
  - `builds/backend-rust/DEPLOY-NOTES-video-bibliothek.md`
  - `builds/backend-rust/README.md`
  - `builds/backend-rust/migrations/2026071999_video_library.sql`
  - `builds/backend-rust/migrations/2026072000_video_action_audit.sql`
  - `builds/backend-rust/src/app.rs`
  - `builds/backend-rust/src/auth.rs`
  - … 124 weitere

### internal/deadlock-turniere/uebersicht.html (grob, 157 Commits seit Pruefung)

Stand der Seite: 2026-07-07
- `Deadlock-Turniere` (rust, backend, frontend) ab `c6a5d2c9` [datum-abgeleitet, grob]: 157 Commits, 229 Dateien
  - `backend/__init__.py`
  - `backend/admin/__init__.py`
  - `backend/admin/test_mode.py`
  - `backend/auth/__init__.py`
  - `backend/auth/discord_oauth.py`
  - `backend/auth/middleware.py`
  - `backend/auth/permissions.py`
  - `backend/config.py`
  - … 221 weitere

### internal/patchnotes-bot/architektur.html (grob, 157 Commits seit Pruefung)

Stand der Seite: 2026-07-07
- `Deadlock--Patchnotes-Bot` (.) ab `e1c71cba` [datum-abgeleitet, grob]: 157 Commits, 388 Dateien
  - `.github/workflows/codeql.yml`
  - `.github/workflows/dev-tracker-rust.yml`
  - `.github/workflows/secret-scanning.yml`
  - `.github/workflows/security.yml`
  - `.tasks/2026-09-20-global-toml/AUFTRAG.md`
  - `.tasks/2026-09-20-global-toml/INVENTAR.md`
  - `.tasks/2026-09-20-global-toml/audit_legacy.py`
  - `.tasks/2026-09-20-global-toml/candidate-comparison.json`
  - … 380 weitere

### internal/patchnotes-bot/betrieb.html (grob, 157 Commits seit Pruefung)

Stand der Seite: 2026-07-07
- `Deadlock--Patchnotes-Bot` (.) ab `e1c71cba` [datum-abgeleitet, grob]: 157 Commits, 388 Dateien
  - `.github/workflows/codeql.yml`
  - `.github/workflows/dev-tracker-rust.yml`
  - `.github/workflows/secret-scanning.yml`
  - `.github/workflows/security.yml`
  - `.tasks/2026-09-20-global-toml/AUFTRAG.md`
  - `.tasks/2026-09-20-global-toml/INVENTAR.md`
  - `.tasks/2026-09-20-global-toml/audit_legacy.py`
  - `.tasks/2026-09-20-global-toml/candidate-comparison.json`
  - … 380 weitere

### internal/patchnotes-bot/integrationen.html (grob, 157 Commits seit Pruefung)

Stand der Seite: 2026-07-07
- `Deadlock--Patchnotes-Bot` (.) ab `e1c71cba` [datum-abgeleitet, grob]: 157 Commits, 388 Dateien
  - `.github/workflows/codeql.yml`
  - `.github/workflows/dev-tracker-rust.yml`
  - `.github/workflows/secret-scanning.yml`
  - `.github/workflows/security.yml`
  - `.tasks/2026-09-20-global-toml/AUFTRAG.md`
  - `.tasks/2026-09-20-global-toml/INVENTAR.md`
  - `.tasks/2026-09-20-global-toml/audit_legacy.py`
  - `.tasks/2026-09-20-global-toml/candidate-comparison.json`
  - … 380 weitere

### internal/patchnotes-bot/uebersicht.html (grob, 157 Commits seit Pruefung)

Stand der Seite: 2026-07-07
- `Deadlock--Patchnotes-Bot` (.) ab `e1c71cba` [datum-abgeleitet, grob]: 157 Commits, 388 Dateien
  - `.github/workflows/codeql.yml`
  - `.github/workflows/dev-tracker-rust.yml`
  - `.github/workflows/secret-scanning.yml`
  - `.github/workflows/security.yml`
  - `.tasks/2026-09-20-global-toml/AUFTRAG.md`
  - `.tasks/2026-09-20-global-toml/INVENTAR.md`
  - `.tasks/2026-09-20-global-toml/audit_legacy.py`
  - `.tasks/2026-09-20-global-toml/candidate-comparison.json`
  - … 380 weitere

### internal/website/betrieb.html (grob, 152 Commits seit Pruefung)

Stand der Seite: 2026-07-10
- `Website` (builds, scripts) ab `f305c821` [datum-abgeleitet, grob]: 152 Commits, 72 Dateien
  - `builds/backend-rust/Cargo.lock`
  - `builds/backend-rust/Cargo.toml`
  - `builds/backend-rust/DEPLOY-NOTES-video-bibliothek.md`
  - `builds/backend-rust/README.md`
  - `builds/backend-rust/migrations/2026071999_video_library.sql`
  - `builds/backend-rust/migrations/2026072000_video_action_audit.sql`
  - `builds/backend-rust/src/app.rs`
  - `builds/backend-rust/src/auth.rs`
  - … 64 weitere

### internal/deadlock-brain/match-demo-learning.html (grob, 149 Commits seit Pruefung)

Stand der Seite: 2026-07-10
- `Deadlock-Brain` (rust, src) ab `10edcd42` [datum-abgeleitet, grob]: 149 Commits, 108 Dateien
  - `rust/Cargo.lock`
  - `rust/Cargo.toml`
  - `rust/crates/dbrain-builds/src/api.rs`
  - `rust/crates/dbrain-builds/src/engine.rs`
  - `rust/crates/dbrain-builds/src/lib.rs`
  - `rust/crates/dbrain-builds/src/patch_tag.rs`
  - `rust/crates/dbrain-builds/src/spec.rs`
  - `rust/crates/dbrain-builds/src/sync.rs`
  - … 100 weitere

### internal/deadlock-turniere/betrieb.html (grob, 142 Commits seit Pruefung)

Stand der Seite: 2026-07-12
- `Deadlock-Turniere` (rust, ops, scripts) ab `208c28bf` [datum-abgeleitet, grob]: 142 Commits, 124 Dateien
  - `ops/systemd/60-global-toml.conf`
  - `ops/systemd/deadlock-turniere.service.example`
  - `rust/Cargo.lock`
  - `rust/Cargo.toml`
  - `rust/crates/turnier-api/Cargo.toml`
  - `rust/crates/turnier-api/src/admin/automatik.rs`
  - `rust/crates/turnier-api/src/app.rs`
  - `rust/crates/turnier-api/src/auth.rs`
  - … 116 weitere

### internal/deadlock-turniere/architektur.html (grob, 139 Commits seit Pruefung)

Stand der Seite: 2026-07-07
- `Deadlock-Turniere` (rust, backend) ab `c6a5d2c9` [datum-abgeleitet, grob]: 139 Commits, 176 Dateien
  - `backend/__init__.py`
  - `backend/admin/__init__.py`
  - `backend/admin/test_mode.py`
  - `backend/auth/__init__.py`
  - `backend/auth/discord_oauth.py`
  - `backend/auth/middleware.py`
  - `backend/auth/permissions.py`
  - `backend/config.py`
  - … 168 weitere

### internal/deadlock-turniere/datenmodell.html (grob, 139 Commits seit Pruefung)

Stand der Seite: 2026-07-10
- `Deadlock-Turniere` (rust, backend) ab `c6a5d2c9` [datum-abgeleitet, grob]: 139 Commits, 176 Dateien
  - `backend/__init__.py`
  - `backend/admin/__init__.py`
  - `backend/admin/test_mode.py`
  - `backend/auth/__init__.py`
  - `backend/auth/discord_oauth.py`
  - `backend/auth/middleware.py`
  - `backend/auth/permissions.py`
  - `backend/config.py`
  - … 168 weitere

### internal/deadlock-turniere/integrationen.html (grob, 139 Commits seit Pruefung)

Stand der Seite: 2026-07-07
- `Deadlock-Turniere` (rust, backend) ab `c6a5d2c9` [datum-abgeleitet, grob]: 139 Commits, 176 Dateien
  - `backend/__init__.py`
  - `backend/admin/__init__.py`
  - `backend/admin/test_mode.py`
  - `backend/auth/__init__.py`
  - `backend/auth/discord_oauth.py`
  - `backend/auth/middleware.py`
  - `backend/auth/permissions.py`
  - `backend/config.py`
  - … 168 weitere

### internal/deadlock-turniere/match-automatik.html (grob, 139 Commits seit Pruefung)

Stand der Seite: 2026-07-07
- `Deadlock-Turniere` (rust, backend) ab `c6a5d2c9` [datum-abgeleitet, grob]: 139 Commits, 176 Dateien
  - `backend/__init__.py`
  - `backend/admin/__init__.py`
  - `backend/admin/test_mode.py`
  - `backend/auth/__init__.py`
  - `backend/auth/discord_oauth.py`
  - `backend/auth/middleware.py`
  - `backend/auth/permissions.py`
  - `backend/config.py`
  - … 168 weitere

### internal/deadlock-turniere/draft-lobbys.html (grob, 117 Commits seit Pruefung)

Stand der Seite: 2026-07-16
- `Deadlock-Turniere` (rust, backend, frontend) ab `16490dcf` [datum-abgeleitet, grob]: 117 Commits, 208 Dateien
  - `backend/__init__.py`
  - `backend/admin/__init__.py`
  - `backend/admin/test_mode.py`
  - `backend/auth/__init__.py`
  - `backend/auth/discord_oauth.py`
  - `backend/auth/middleware.py`
  - `backend/auth/permissions.py`
  - `backend/config.py`
  - … 200 weitere

### internal/website/datenmodell.html (grob, 92 Commits seit Pruefung)

Stand der Seite: 2026-07-07
- `Website` (builds) ab `66a9c32b` [datum-abgeleitet, grob]: 92 Commits, 56 Dateien
  - `builds/backend-rust/Cargo.lock`
  - `builds/backend-rust/Cargo.toml`
  - `builds/backend-rust/DEPLOY-NOTES-video-bibliothek.md`
  - `builds/backend-rust/README.md`
  - `builds/backend-rust/migrations/2026071999_video_library.sql`
  - `builds/backend-rust/migrations/2026072000_video_action_audit.sql`
  - `builds/backend-rust/src/app.rs`
  - `builds/backend-rust/src/auth.rs`
  - … 48 weitere

### internal/website/integrationen.html (grob, 92 Commits seit Pruefung)

Stand der Seite: 2026-07-07
- `Website` (builds) ab `66a9c32b` [datum-abgeleitet, grob]: 92 Commits, 56 Dateien
  - `builds/backend-rust/Cargo.lock`
  - `builds/backend-rust/Cargo.toml`
  - `builds/backend-rust/DEPLOY-NOTES-video-bibliothek.md`
  - `builds/backend-rust/README.md`
  - `builds/backend-rust/migrations/2026071999_video_library.sql`
  - `builds/backend-rust/migrations/2026072000_video_action_audit.sql`
  - `builds/backend-rust/src/app.rs`
  - `builds/backend-rust/src/auth.rs`
  - … 48 weitere

### internal/betrieb/uebersicht.html (grob, 82 Commits seit Pruefung)

Stand der Seite: 2026-07-11
- `Deadlock-Bots` (scripts) ab `7b0f35bb` [datum-abgeleitet, grob]: 22 Commits, 13 Dateien
  - `scripts/check-local.sh`
  - `scripts/dl_bot_mcp_stdio_proxy.py`
  - `scripts/export_infisical_env.py`
  - `scripts/kill_stale_bot.sh`
  - `scripts/maintenance/repair_discord_system_messages_20260908.sql`
  - `scripts/run_brain_feeder.sh`
  - `scripts/run_dl_insights_sync.sh`
  - `scripts/run_dl_knowledge_service.sh`
  - … 5 weitere
- `Caddy` (.) ab `9f2bd24b` [datum-abgeleitet, grob]: 60 Commits, 11 Dateien
  - `.tasks/2026-09-26-devfeed-public/CONTRACT.md`
  - `CLAUDE.md`
  - `README.md`
  - `conf/Caddyfile`
  - `docker-compose.yml`
  - `hosts/v50671/Caddyfile`
  - `hosts/v50671/partner-profile-assets.caddy`
  - `hosts/v50671/partner-profiles.caddy`
  - … 3 weitere
- `Deadlock-Twitch-Bot` (ops/systemd, rust/scripts) ab `5082d53f` [explizit, genau]: 0 Commits, 0 Dateien
  - Hinweis: fatal: Needed a single revision

### internal/betrieb/routing-caddy.html (grob, 62 Commits seit Pruefung)

Stand der Seite: 2026-07-07
- `Caddy` (.) ab `89c1f8ab` [datum-abgeleitet, grob]: 62 Commits, 11 Dateien
  - `.tasks/2026-09-26-devfeed-public/CONTRACT.md`
  - `CLAUDE.md`
  - `README.md`
  - `conf/Caddyfile`
  - `docker-compose.yml`
  - `hosts/v50671/Caddyfile`
  - `hosts/v50671/partner-profile-assets.caddy`
  - `hosts/v50671/partner-profiles.caddy`
  - … 3 weitere

### internal/betrieb/deploy.html (grob, 24 Commits seit Pruefung)

Stand der Seite: 2026-07-07
- `Deadlock-Bots` (scripts) ab `9669df25` [datum-abgeleitet, grob]: 24 Commits, 13 Dateien
  - `scripts/check-local.sh`
  - `scripts/dl_bot_mcp_stdio_proxy.py`
  - `scripts/export_infisical_env.py`
  - `scripts/kill_stale_bot.sh`
  - `scripts/maintenance/repair_discord_system_messages_20260908.sql`
  - `scripts/run_brain_feeder.sh`
  - `scripts/run_dl_insights_sync.sh`
  - `scripts/run_dl_knowledge_service.sh`
  - … 5 weitere

### internal/betrieb/secrets-infisical.html (grob, 19 Commits seit Pruefung)

Stand der Seite: 2026-07-12
- `Deadlock-Bots` (scripts) ab `3bc8ca8a` [explizit, grob]: 19 Commits, 13 Dateien
  - `scripts/check-local.sh`
  - `scripts/dl_bot_mcp_stdio_proxy.py`
  - `scripts/export_infisical_env.py`
  - `scripts/kill_stale_bot.sh`
  - `scripts/maintenance/repair_discord_system_messages_20260908.sql`
  - `scripts/run_brain_feeder.sh`
  - `scripts/run_dl_insights_sync.sh`
  - `scripts/run_dl_knowledge_service.sh`
  - … 5 weitere

### internal/deadlock-bots/betrieb.html (grob, 19 Commits seit Pruefung)

Stand der Seite: 2026-07-12
- `Deadlock-Bots` (scripts) ab `3bc8ca8a` [explizit, grob]: 19 Commits, 13 Dateien
  - `scripts/check-local.sh`
  - `scripts/dl_bot_mcp_stdio_proxy.py`
  - `scripts/export_infisical_env.py`
  - `scripts/kill_stale_bot.sh`
  - `scripts/maintenance/repair_discord_system_messages_20260908.sql`
  - `scripts/run_brain_feeder.sh`
  - `scripts/run_dl_insights_sync.sh`
  - `scripts/run_dl_knowledge_service.sh`
  - … 5 weitere
- `Deadlock-Docs` (tools/deploy_corpus.sh) ab `08c01ff0` [datum-abgeleitet, genau]: 0 Commits, 0 Dateien

### internal/website/scrim-cockpit-handbuch.html (grob, 14 Commits seit Pruefung)

Stand der Seite: 2026-07-16
- `Website` (dl-coaching, builds/backend-rust/src/routes/scrim.rs) ab `5b9bfa3b` [datum-abgeleitet, grob]: 14 Commits, 11 Dateien
  - `builds/backend-rust/src/routes/scrim.rs`
  - `dl-coaching/index.html`
  - `dl-coaching/package-lock.json`
  - `dl-coaching/package.json`
  - `dl-coaching/src/App.tsx`
  - `dl-coaching/src/api/client.ts`
  - `dl-coaching/src/components/Layout.tsx`
  - `dl-coaching/src/lib/commandCenter.test.ts`
  - … 3 weitere

## unbekannt (1)

### internal/deadlock-twitch-bot/stream-coaching-audit.html

Stand der Seite: 2026-08-14
- `Deadlock-Twitch-Bot` (rust/crates/tb-stream-audit, rust/bin/tb-stream-audit, rust/crates/tb-engagement/src/audio_capture.rs, rust/crates/tb-engagement/src/transcribe.rs, rust/crates/tb-llm/src/selection.rs, rust/scripts/run_stream_audit_service.sh, ops/systemd/deadlock-twitch-stream-coaching-watch.service) ab `5082d53f` [explizit, genau]: 0 Commits, 0 Dateien
  - Hinweis: fatal: Needed a single revision

## aktuell (5)

### internal/STYLEGUIDE.html

Stand der Seite: 2026-07-11
- `Deadlock-Docs` (tools/validate_corpus.py) ab `5dfe43fb` [datum-abgeleitet, genau]: 0 Commits, 0 Dateien

### internal/wissensbasis/deadlock-brain-retrieval.md

Stand der Seite: 2026-09-17
- `Deadlock-Brain` (src/deadlock_brain/retrieval.py, src/deadlock_brain/brain_pipeline.py, src/deadlock_brain/storage.py) ab `15bc1d3a` [explizit, genau]: 0 Commits, 0 Dateien

### internal/wissensbasis/faq-entwurf/item-referenz.md

Stand der Seite: 2026-09-19
- `Deadlock-Brain` (rust/crates/dbrain-learn/src/build_optimizer.rs, README.md) ab `15bc1d3a` [explizit, grob]: 0 Commits, 0 Dateien
- `Deadlock-Docs` (public/deadlock-helden, internal/wissensbasis/faq-korpus-abdeckung.md) ab `9674a3cd` [explizit, genau]: 0 Commits, 0 Dateien
  - Hinweis: geprueft liegt nicht auf main; verglichen ab gemeinsamem Vorfahr 2c4b5de5 (meldet eher zu viel als zu wenig)

### internal/wissensbasis/faq-entwurf/ranks-matchmaking.md

Stand der Seite: 2026-09-19
- `Deadlock-Bots` (rust/crates/dl-stats/src/ranks.rs) ab `bb03deb5` [explizit, genau]: 0 Commits, 0 Dateien
- `Deadlock-Docs` (internal/wissensbasis/faq-korpus-abdeckung.md) ab `9674a3cd` [explizit, genau]: 0 Commits, 0 Dateien
  - Hinweis: geprueft liegt nicht auf main; verglichen ab gemeinsamem Vorfahr 2c4b5de5 (meldet eher zu viel als zu wenig)

### internal/wissensbasis/faq-korpus-abdeckung.md

Stand der Seite: 2026-09-17
- `Deadlock-Docs` (public) ab `9674a3cd` [explizit, grob]: 0 Commits, 0 Dateien
  - Hinweis: geprueft liegt nicht auf main; verglichen ab gemeinsamem Vorfahr 2c4b5de5 (meldet eher zu viel als zu wenig)

## nicht-verfolgt (2)

### internal/betrieb/zentrale-bot-config.html

Stand der Seite: 2026-07-27
Grund: Quelle sind Host-Dateien (~/.config/deadlock/bots.env, systemd-Drop-ins), kein Repo

### internal/deadlock-turniere/draft-lobbys-redaction-notes.html

Stand der Seite: 2026-07-16
Grund: Redaktionspruefung einer Doku-Seite, kein Code-Bezug
