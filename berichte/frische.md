# Frische der internen Wissensseiten

Erzeugt: 2026-08-21 von `tools/check_freshness.py` aus `quellen.json`.

- ohne Eintrag in `quellen.json`: **0**
- veraltet: **68**, davon 25 mit genauer Bindung
- aktuell: 1
- unbekannt: 0
- nicht verfolgt: 2

`veraltet` heisst: seit dem geprueften Commit wurde in den gebundenen
Quellpfaden weitergearbeitet. Es heisst nicht, dass die Seite falsch ist,
sondern dass sie ungeprueft ist.

43 Seiten haengen noch an groben Pfaden (ganze Repo-Verzeichnisse).
Ihre Commit-Zahlen sind Obergrenzen, kein Befund. Wer eine solche Seite
ueberarbeitet, traegt in `quellen.json` gleich die genauen Pfade nach;
danach meldet der Bericht fuer sie nur noch echte Treffer.

## veraltet (68)

### internal/deadlock-bots/stats-und-privacy-devs.html (genau, 206 Commits seit Pruefung)

Stand der Seite: 2026-07-12
- `Deadlock-Bots` (rust/crates/dl-activity, rust/crates/dl-community, rust/crates/dl-voice, rust/crates/dl-central-db) ab `3bc8ca8a` [explizit, genau]: 148 Commits, 107 Dateien
  - `rust/crates/dl-activity/Cargo.toml`
  - `rust/crates/dl-activity/src/analyzer.rs`
  - `rust/crates/dl-activity/src/lfg_freetext.rs`
  - `rust/crates/dl-activity/src/lib.rs`
  - `rust/crates/dl-activity/src/outbox.rs`
  - `rust/crates/dl-activity/src/survey_pulse.rs`
  - `rust/crates/dl-central-db/Cargo.toml`
  - `rust/crates/dl-central-db/build.rs`
  - … 99 weitere
- `Deadlock-Steam-Bot` (rust) ab `6fad947c` [explizit, grob]: 58 Commits, 106 Dateien
  - `rust/.sqlx/query-1045b3d8cc81ee6518f699e634cd7396ea5b0619312f291bc9a7cc73d70e1a32.json`
  - `rust/.sqlx/query-158079b4bdbfb714a7d4845bbc45bb1690f77595b07d53df9630f3a7e4639e3c.json`
  - `rust/.sqlx/query-2266eaf88d227d9de58ff57fcadca118b8f1e5d711cbea9499ddf1411ac1b449.json`
  - `rust/.sqlx/query-28b7acee3c82a1105ee3bc9df8d29bfb2c6328e95dfc51a1dea980ef68ef9263.json`
  - `rust/.sqlx/query-2fb699804b88f1f704057f7becdceaabd31f175b4e52516db53c789dda092789.json`
  - `rust/.sqlx/query-35e28e42ca581cae21549de2294b018938c9f19801392c1edc23c280547eae62.json`
  - `rust/.sqlx/query-3c6da0afe42464f2db195115b100a04ca7b9d8207dc6b1efd30619353293bea6.json`
  - `rust/.sqlx/query-48d77e96128a0c95d10ca981e8f6c71bef767e47cab146f6526ca47de5fe67ce.json`
  - … 98 weitere
- `Deadlock-Docs` (public/discord-server/stats-und-privacy.html) ab `08c01ff0` [datum-abgeleitet, genau]: 0 Commits, 0 Dateien

### internal/betrieb/datenbank.html (genau, 80 Commits seit Pruefung)

Stand der Seite: 2026-07-07
- `Deadlock-Bots` (rust/crates/dl-central-db, rust/crates/dl-central-etl) ab `9669df25` [datum-abgeleitet, genau]: 80 Commits, 82 Dateien
  - `rust/crates/dl-central-db/Cargo.toml`
  - `rust/crates/dl-central-db/build.rs`
  - `rust/crates/dl-central-db/migrations/2026070913_invite_requests.sql`
  - `rust/crates/dl-central-db/migrations/2026071010_router_intro_dm_marker.sql`
  - `rust/crates/dl-central-db/migrations/2026071110_discord_audit_log.sql`
  - `rust/crates/dl-central-db/migrations/2026071111_steam_bot_event_log.sql`
  - `rust/crates/dl-central-db/migrations/2026071112_pate_journey_metadata_scrub.sql`
  - `rust/crates/dl-central-db/migrations/2026071120_invite_dispatch_claim.sql`
  - … 74 weitere

### internal/deadlock-bots/datenmodell.html (genau, 80 Commits seit Pruefung)

Stand der Seite: 2026-07-07
- `Deadlock-Bots` (rust/crates/dl-central-db) ab `9669df25` [datum-abgeleitet, genau]: 80 Commits, 82 Dateien
  - `rust/crates/dl-central-db/Cargo.toml`
  - `rust/crates/dl-central-db/build.rs`
  - `rust/crates/dl-central-db/migrations/2026070913_invite_requests.sql`
  - `rust/crates/dl-central-db/migrations/2026071010_router_intro_dm_marker.sql`
  - `rust/crates/dl-central-db/migrations/2026071110_discord_audit_log.sql`
  - `rust/crates/dl-central-db/migrations/2026071111_steam_bot_event_log.sql`
  - `rust/crates/dl-central-db/migrations/2026071112_pate_journey_metadata_scrub.sql`
  - `rust/crates/dl-central-db/migrations/2026071120_invite_dispatch_claim.sql`
  - … 74 weitere

### internal/betrieb/uebersicht.html (genau, 60 Commits seit Pruefung)

Stand der Seite: 2026-07-11
- `Deadlock-Bots` (scripts) ab `7b0f35bb` [datum-abgeleitet, grob]: 10 Commits, 7 Dateien
  - `scripts/check-local.sh`
  - `scripts/export_infisical_env.py`
  - `scripts/kill_stale_bot.sh`
  - `scripts/run_brain_feeder.sh`
  - `scripts/run_dl_knowledge_service.sh`
  - `scripts/run_verbinder.sh`
  - `scripts/test_dl_knowledge_launcher.py`
- `Caddy` (.) ab `9f2bd24b` [datum-abgeleitet, grob]: 34 Commits, 8 Dateien
  - `CLAUDE.md`
  - `README.md`
  - `conf/Caddyfile`
  - `docker-compose.yml`
  - `hosts/v50671/Caddyfile`
  - `hosts/v50671/systemd/10-logs.conf`
  - `hosts/v50671/systemd/20-tailscale.conf`
  - `hosts/v50671/systemd/99-caddy-nonlocal-bind.sysctl.conf`
- `Deadlock-Twitch-Bot` (ops/systemd, rust/scripts) ab `5082d53f` [explizit, genau]: 16 Commits, 2 Dateien
  - Hinweis: geprueft liegt nicht auf main; verglichen ab gemeinsamem Vorfahr 8b450be1 (meldet eher zu viel als zu wenig)
  - `ops/systemd/deadlock-twitch-stream-coaching-watch.service`
  - `rust/scripts/run_stream_audit_service.sh`

### internal/deadlock-twitch-bot/stream-coaching-audit.html (genau, 52 Commits seit Pruefung)

Stand der Seite: 2026-08-14
- `Deadlock-Twitch-Bot` (rust/crates/tb-stream-audit, rust/bin/tb-stream-audit, rust/crates/tb-engagement/src/audio_capture.rs, rust/crates/tb-engagement/src/transcribe.rs, rust/crates/tb-llm/src/selection.rs, rust/scripts/run_stream_audit_service.sh, ops/systemd/deadlock-twitch-stream-coaching-watch.service) ab `5082d53f` [explizit, genau]: 52 Commits, 14 Dateien
  - Hinweis: geprueft liegt nicht auf main; verglichen ab gemeinsamem Vorfahr 8b450be1 (meldet eher zu viel als zu wenig)
  - `ops/systemd/deadlock-twitch-stream-coaching-watch.service`
  - `rust/bin/tb-stream-audit/Cargo.toml`
  - `rust/bin/tb-stream-audit/src/main.rs`
  - `rust/crates/tb-engagement/src/transcribe.rs`
  - `rust/crates/tb-stream-audit/Cargo.toml`
  - `rust/crates/tb-stream-audit/src/config.rs`
  - `rust/crates/tb-stream-audit/src/last.rs`
  - `rust/crates/tb-stream-audit/src/lib.rs`
  - … 6 weitere

### internal/deadlock-bots/voice-features-devs.html (genau, 47 Commits seit Pruefung)

Stand der Seite: 2026-07-11
- `Deadlock-Bots` (rust/crates/dl-voice) ab `7b0f35bb` [datum-abgeleitet, genau]: 45 Commits, 19 Dateien
  - `rust/crates/dl-voice/Cargo.toml`
  - `rust/crates/dl-voice/src/feedback.rs`
  - `rust/crates/dl-voice/src/glue.rs`
  - `rust/crates/dl-voice/src/lfg_panel.rs`
  - `rust/crates/dl-voice/src/lfg_watch.rs`
  - `rust/crates/dl-voice/src/lib.rs`
  - `rust/crates/dl-voice/src/mate_survey.rs`
  - `rust/crates/dl-voice/src/nudge.rs`
  - … 11 weitere
- `Deadlock-Docs` (public/discord-server/voice-features.html) ab `5dfe43fb` [datum-abgeleitet, genau]: 2 Commits, 1 Dateien
  - `public/discord-server/voice-features.html`

### internal/deadlock-bots/onboarding-concierge-llm-compliance.html (genau, 35 Commits seit Pruefung)

Stand der Seite: 2026-07-07
- `Deadlock-Bots` (rust/crates/dl-community/src/concierge.rs) ab `9669df25` [datum-abgeleitet, genau]: 35 Commits, 1 Dateien
  - `rust/crates/dl-community/src/concierge.rs`

### internal/deadlock-bots/twitch-clips-und-social.html (genau, 14 Commits seit Pruefung)

Stand der Seite: 2026-07-07
- `Deadlock-Bots` (docs/twitch-clips-und-social.md, rust/crates/dl-bridges) ab `9669df25` [datum-abgeleitet, genau]: 14 Commits, 3 Dateien
  - `rust/crates/dl-bridges/src/matcher.rs`
  - `rust/crates/dl-bridges/src/steam.rs`
  - `rust/crates/dl-bridges/src/twitch.rs`

### internal/deadlock-bots/faq-bot-selbst-devs.html (genau, 10 Commits seit Pruefung)

Stand der Seite: 2026-07-12
- `Deadlock-Bots` (rust/bin/dl-knowledge, rust/crates/dl-community/src/faq.rs, rust/crates/dl-community/src/concierge.rs) ab `3bc8ca8a` [explizit, genau]: 10 Commits, 3 Dateien
  - `rust/bin/dl-knowledge/src/main.rs`
  - `rust/crates/dl-community/src/concierge.rs`
  - `rust/crates/dl-community/src/faq.rs`
- `Deadlock-Docs` (public/discord-server/faq-bot-selbst.html) ab `08c01ff0` [datum-abgeleitet, genau]: 0 Commits, 0 Dateien

### internal/deadlock-bots/faq-grounding.html (genau, 10 Commits seit Pruefung)

Stand der Seite: 2026-07-12
- `Deadlock-Bots` (rust/bin/dl-knowledge, rust/crates/dl-community/src/faq.rs, rust/crates/dl-community/src/concierge.rs) ab `3bc8ca8a` [explizit, genau]: 10 Commits, 3 Dateien
  - `rust/bin/dl-knowledge/src/main.rs`
  - `rust/crates/dl-community/src/concierge.rs`
  - `rust/crates/dl-community/src/faq.rs`

### internal/deadlock-bots/onboarding-concierge-slice-b-c.html (genau, 10 Commits seit Pruefung)

Stand der Seite: 2026-07-11
- `Deadlock-Bots` (rust/crates/dl-community/src/concierge.rs, rust/crates/dl-voice/src/nudge.rs, rust/crates/dl-voice/src/feedback.rs) ab `7b0f35bb` [datum-abgeleitet, genau]: 10 Commits, 3 Dateien
  - `rust/crates/dl-community/src/concierge.rs`
  - `rust/crates/dl-voice/src/feedback.rs`
  - `rust/crates/dl-voice/src/nudge.rs`

### internal/deadlock-bots/support-agent-design.html (genau, 10 Commits seit Pruefung)

Stand der Seite: 2026-07-12
- `Deadlock-Bots` (rust/bin/dl-knowledge, rust/crates/dl-community/src/faq.rs, rust/crates/dl-community/src/concierge.rs) ab `3bc8ca8a` [explizit, genau]: 10 Commits, 3 Dateien
  - `rust/bin/dl-knowledge/src/main.rs`
  - `rust/crates/dl-community/src/concierge.rs`
  - `rust/crates/dl-community/src/faq.rs`

### internal/deadlock-bots/integrationen.html (genau, 8 Commits seit Pruefung)

Stand der Seite: 2026-07-11
- `Deadlock-Bots` (rust/crates/dl-bridges) ab `7b0f35bb` [datum-abgeleitet, genau]: 8 Commits, 3 Dateien
  - `rust/crates/dl-bridges/src/matcher.rs`
  - `rust/crates/dl-bridges/src/steam.rs`
  - `rust/crates/dl-bridges/src/twitch.rs`

### internal/deadlock-bots/onboarding-concierge-devs.html (genau, 8 Commits seit Pruefung)

Stand der Seite: 2026-07-11
- `Deadlock-Bots` (rust/crates/dl-community/src/concierge.rs) ab `b069b5c8` [explizit, genau]: 8 Commits, 1 Dateien
  - `rust/crates/dl-community/src/concierge.rs`

### internal/deadlock-bots/onboarding-concierge-texte.html (genau, 8 Commits seit Pruefung)

Stand der Seite: 2026-07-11
- `Deadlock-Bots` (rust/crates/dl-community/src/concierge.rs) ab `b069b5c8` [explizit, genau]: 8 Commits, 1 Dateien
  - `rust/crates/dl-community/src/concierge.rs`

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

### internal/deadlock-bots/moderation-scam-guard.html (genau, 2 Commits seit Pruefung)

Stand der Seite: 2026-07-07
- `Deadlock-Bots` (rust/crates/dl-moderation) ab `9669df25` [datum-abgeleitet, genau]: 2 Commits, 4 Dateien
  - `rust/crates/dl-moderation/src/content_analyzer.rs`
  - `rust/crates/dl-moderation/src/content_verifier.rs`
  - `rust/crates/dl-moderation/src/lib.rs`
  - `rust/crates/dl-moderation/src/moderation_system.rs`

### internal/deadlock-bots/onboarding-und-invites-devs.html (genau, 2 Commits seit Pruefung)

Stand der Seite: 2026-07-10
- `Deadlock-Docs` (public/discord-server/onboarding-und-invites.html) ab `91f8207a` [datum-abgeleitet, genau]: 2 Commits, 1 Dateien
  - `public/discord-server/onboarding-und-invites.html`

### internal/deadlock-bots/scrim-orga-redaction-notes.html (genau, 2 Commits seit Pruefung)

Stand der Seite: 2026-07-24
- `Deadlock-Docs` (public/dokus/scrims) ab `697f05d0` [datum-abgeleitet, genau]: 2 Commits, 1 Dateien
  - `public/dokus/scrims/scrim-orga.html`

### internal/deadlock-bots/server-insights.html (genau, 1 Commits seit Pruefung)

Stand der Seite: 2026-07-07
- `Deadlock-Bots` (docs/server_insights.md, rust/crates/dl-stats) ab `9669df25` [datum-abgeleitet, genau]: 1 Commits, 2 Dateien
  - `rust/crates/dl-stats/src/me.rs`
  - `rust/crates/dl-stats/src/public.rs`

### internal/deadlock-twitch-bot/affiliate.html (grob, 576 Commits seit Pruefung)

Stand der Seite: 2026-07-07
- `Deadlock-Twitch-Bot` (rust, bot) ab `03822a50` [datum-abgeleitet, grob]: 576 Commits, 1096 Dateien
  - `bot/__init__.py`
  - `bot/admin_dashboard/package-lock.json`
  - `bot/admin_dashboard/package.json`
  - `bot/admin_dashboard/src/App.tsx`
  - `bot/admin_dashboard/src/api/client.ts`
  - `bot/admin_dashboard/src/api/types.ts`
  - `bot/admin_dashboard/src/components/layout/AdminShell.tsx`
  - `bot/admin_dashboard/src/components/layout/Sidebar.tsx`
  - … 1088 weitere

### internal/deadlock-twitch-bot/integrationen.html (grob, 576 Commits seit Pruefung)

Stand der Seite: 2026-07-07
- `Deadlock-Twitch-Bot` (rust, bot) ab `03822a50` [datum-abgeleitet, grob]: 576 Commits, 1096 Dateien
  - `bot/__init__.py`
  - `bot/admin_dashboard/package-lock.json`
  - `bot/admin_dashboard/package.json`
  - `bot/admin_dashboard/src/App.tsx`
  - `bot/admin_dashboard/src/api/client.ts`
  - `bot/admin_dashboard/src/api/types.ts`
  - `bot/admin_dashboard/src/components/layout/AdminShell.tsx`
  - `bot/admin_dashboard/src/components/layout/Sidebar.tsx`
  - … 1088 weitere

### internal/deadlock-twitch-bot/uebersicht.html (grob, 576 Commits seit Pruefung)

Stand der Seite: 2026-07-07
- `Deadlock-Twitch-Bot` (rust, bot) ab `03822a50` [datum-abgeleitet, grob]: 576 Commits, 1096 Dateien
  - `bot/__init__.py`
  - `bot/admin_dashboard/package-lock.json`
  - `bot/admin_dashboard/package.json`
  - `bot/admin_dashboard/src/App.tsx`
  - `bot/admin_dashboard/src/api/client.ts`
  - `bot/admin_dashboard/src/api/types.ts`
  - `bot/admin_dashboard/src/components/layout/AdminShell.tsx`
  - `bot/admin_dashboard/src/components/layout/Sidebar.tsx`
  - … 1088 weitere

### internal/deadlock-twitch-bot/knowledge-faq.html (grob, 472 Commits seit Pruefung)

Stand der Seite: 2026-07-07
- `Deadlock-Twitch-Bot` (rust, features) ab `03822a50` [datum-abgeleitet, grob]: 472 Commits, 455 Dateien
  - `rust/.cargo/audit.toml`
  - `rust/.sqlx/query-00748f8a6734810c5b88b17f3db55311a86abaf4e77a2e2cb672e418c2e4d11c.json`
  - `rust/.sqlx/query-06df9f1066fbe003f82f4eb567df77e08edcf9ae7f31f8db0796613e96d214c4.json`
  - `rust/.sqlx/query-09308917b86027e8e264cb9d3671ff6bf08cb5a69e384e84c633a3a0423337b1.json`
  - `rust/.sqlx/query-0ad212233983ef7c10dc16d202d35251e321f3083c2e8aa28a98444ebc8430f3.json`
  - `rust/.sqlx/query-0d388e1f3845ab67a1621c4ec94b366279585b5fe36258ded71409e34be1d547.json`
  - `rust/.sqlx/query-0dfad953279837024b145902ee231bac620126b9f1f5b1b9d411fe356f24e009.json`
  - `rust/.sqlx/query-111087e8833cf76f4b938091a726389ef07551ce208b440ed120f0b47b0cd34d.json`
  - … 447 weitere

### internal/deadlock-bots/architektur.html (grob, 378 Commits seit Pruefung)

Stand der Seite: 2026-07-07
- `Deadlock-Bots` (rust) ab `9669df25` [datum-abgeleitet, grob]: 378 Commits, 249 Dateien
  - `rust/.sqlx/query-00cbd620a306b6128f21c744d815c1f46d6698fe84aae23739772996b49402fc.json`
  - `rust/.sqlx/query-115f831897ce9f7ec2e81cc7ac7e28021cdcab6aac51fda1e94d733304c8e43e.json`
  - `rust/.sqlx/query-14fdb6d7fa6d976e5890147a53bd1d7b31168661e01dcf2bb79aa6b0b8a4d61e.json`
  - `rust/.sqlx/query-1d13bd25d56c4bed501e77fafb48a37f383b758e6d8fda6d37eb086c026cdef6.json`
  - `rust/.sqlx/query-24dfe426673fcb6c5e23b9c7009cc42241b0627e2afd5ae99362b3fc9fd69c6b.json`
  - `rust/.sqlx/query-2dcc3b77350e59caef3af267e1ea961d664f450b424be977e7b2cbdd6c6027aa.json`
  - `rust/.sqlx/query-2e9682b2bb3267e7980b3b1bfab7697df0dabf5b7510ee803963dcc1344ec22d.json`
  - `rust/.sqlx/query-45623204c0ce3c836ca17e31d5eab228607cd49337cf79700fcae82fec6bab77.json`
  - … 241 weitere

### internal/deadlock-bots/uebersicht.html (grob, 378 Commits seit Pruefung)

Stand der Seite: 2026-07-07
- `Deadlock-Bots` (rust) ab `9669df25` [datum-abgeleitet, grob]: 378 Commits, 249 Dateien
  - `rust/.sqlx/query-00cbd620a306b6128f21c744d815c1f46d6698fe84aae23739772996b49402fc.json`
  - `rust/.sqlx/query-115f831897ce9f7ec2e81cc7ac7e28021cdcab6aac51fda1e94d733304c8e43e.json`
  - `rust/.sqlx/query-14fdb6d7fa6d976e5890147a53bd1d7b31168661e01dcf2bb79aa6b0b8a4d61e.json`
  - `rust/.sqlx/query-1d13bd25d56c4bed501e77fafb48a37f383b758e6d8fda6d37eb086c026cdef6.json`
  - `rust/.sqlx/query-24dfe426673fcb6c5e23b9c7009cc42241b0627e2afd5ae99362b3fc9fd69c6b.json`
  - `rust/.sqlx/query-2dcc3b77350e59caef3af267e1ea961d664f450b424be977e7b2cbdd6c6027aa.json`
  - `rust/.sqlx/query-2e9682b2bb3267e7980b3b1bfab7697df0dabf5b7510ee803963dcc1344ec22d.json`
  - `rust/.sqlx/query-45623204c0ce3c836ca17e31d5eab228607cd49337cf79700fcae82fec6bab77.json`
  - … 241 weitere

### internal/deadlock-twitch-bot/architektur.html (grob, 308 Commits seit Pruefung)

Stand der Seite: 2026-07-18
- `Deadlock-Twitch-Bot` (rust, bot) ab `9e740716` [datum-abgeleitet, grob]: 308 Commits, 890 Dateien
  - `bot/__init__.py`
  - `bot/admin_dashboard/package-lock.json`
  - `bot/admin_dashboard/package.json`
  - `bot/admin_dashboard/src/App.tsx`
  - `bot/admin_dashboard/src/api/client.ts`
  - `bot/admin_dashboard/src/api/types.ts`
  - `bot/admin_dashboard/src/components/layout/AdminShell.tsx`
  - `bot/admin_dashboard/src/components/layout/Sidebar.tsx`
  - … 882 weitere

### internal/deadlock-twitch-bot/datenmodell.html (grob, 308 Commits seit Pruefung)

Stand der Seite: 2026-07-18
- `Deadlock-Twitch-Bot` (rust, bot) ab `9e740716` [datum-abgeleitet, grob]: 308 Commits, 890 Dateien
  - `bot/__init__.py`
  - `bot/admin_dashboard/package-lock.json`
  - `bot/admin_dashboard/package.json`
  - `bot/admin_dashboard/src/App.tsx`
  - `bot/admin_dashboard/src/api/client.ts`
  - `bot/admin_dashboard/src/api/types.ts`
  - `bot/admin_dashboard/src/components/layout/AdminShell.tsx`
  - `bot/admin_dashboard/src/components/layout/Sidebar.tsx`
  - … 882 weitere

### internal/deadlock-twitch-bot/pause-loop-obs.html (grob, 248 Commits seit Pruefung)

Stand der Seite: 2026-07-20
- `Deadlock-Twitch-Bot` (rust, features) ab `a0a3f8d7` [datum-abgeleitet, grob]: 223 Commits, 296 Dateien
  - `rust/.cargo/audit.toml`
  - `rust/.sqlx/query-00748f8a6734810c5b88b17f3db55311a86abaf4e77a2e2cb672e418c2e4d11c.json`
  - `rust/.sqlx/query-06df9f1066fbe003f82f4eb567df77e08edcf9ae7f31f8db0796613e96d214c4.json`
  - `rust/.sqlx/query-09308917b86027e8e264cb9d3671ff6bf08cb5a69e384e84c633a3a0423337b1.json`
  - `rust/.sqlx/query-0ad212233983ef7c10dc16d202d35251e321f3083c2e8aa28a98444ebc8430f3.json`
  - `rust/.sqlx/query-0dfad953279837024b145902ee231bac620126b9f1f5b1b9d411fe356f24e009.json`
  - `rust/.sqlx/query-111087e8833cf76f4b938091a726389ef07551ce208b440ed120f0b47b0cd34d.json`
  - `rust/.sqlx/query-16ff8a93cd6ef1d08bd3e80320a06e2cd3b0ec81223d72abd5717a405a5bb3b8.json`
  - … 288 weitere
- `Caddy` (.) ab `ed03744a` [datum-abgeleitet, grob]: 25 Commits, 8 Dateien
  - `CLAUDE.md`
  - `README.md`
  - `conf/Caddyfile`
  - `docker-compose.yml`
  - `hosts/v50671/Caddyfile`
  - `hosts/v50671/systemd/10-logs.conf`
  - `hosts/v50671/systemd/20-tailscale.conf`
  - `hosts/v50671/systemd/99-caddy-nonlocal-bind.sysctl.conf`

### internal/deadlock-twitch-bot/betrieb.html (grob, 177 Commits seit Pruefung)

Stand der Seite: 2026-07-27
- `Deadlock-Twitch-Bot` (ops, rust) ab `3b74c611` [datum-abgeleitet, grob]: 177 Commits, 272 Dateien
  - `ops/learn-samples.sh`
  - `ops/stt-server/README.md`
  - `ops/stt-server/stt_server.py`
  - `ops/systemd/deadlock-twitch-stream-coaching-watch.service`
  - `rust/.cargo/audit.toml`
  - `rust/.sqlx/query-00748f8a6734810c5b88b17f3db55311a86abaf4e77a2e2cb672e418c2e4d11c.json`
  - `rust/.sqlx/query-06df9f1066fbe003f82f4eb567df77e08edcf9ae7f31f8db0796613e96d214c4.json`
  - `rust/.sqlx/query-09308917b86027e8e264cb9d3671ff6bf08cb5a69e384e84c633a3a0423337b1.json`
  - … 264 weitere

### internal/deadlock-twitch-bot/bot-trennen.html (grob, 177 Commits seit Pruefung)

Stand der Seite: 2026-08-03
- `Deadlock-Twitch-Bot` (rust, bot) ab `22fd298d` [datum-abgeleitet, grob]: 177 Commits, 270 Dateien
  - `bot/admin_dashboard/package-lock.json`
  - `bot/admin_dashboard/package.json`
  - `bot/admin_dashboard/src/App.tsx`
  - `bot/admin_dashboard/src/api/client.ts`
  - `bot/admin_dashboard/src/api/types.ts`
  - `bot/admin_dashboard/src/components/layout/AdminShell.tsx`
  - `bot/admin_dashboard/src/components/layout/Sidebar.tsx`
  - `bot/admin_dashboard/src/components/layout/TopBar.tsx`
  - … 262 weitere

### internal/deadlock-twitch-bot/scam-guard.html (grob, 176 Commits seit Pruefung)

Stand der Seite: 2026-07-27
- `Deadlock-Twitch-Bot` (rust, features) ab `3b74c611` [datum-abgeleitet, grob]: 176 Commits, 268 Dateien
  - `rust/.cargo/audit.toml`
  - `rust/.sqlx/query-00748f8a6734810c5b88b17f3db55311a86abaf4e77a2e2cb672e418c2e4d11c.json`
  - `rust/.sqlx/query-06df9f1066fbe003f82f4eb567df77e08edcf9ae7f31f8db0796613e96d214c4.json`
  - `rust/.sqlx/query-09308917b86027e8e264cb9d3671ff6bf08cb5a69e384e84c633a3a0423337b1.json`
  - `rust/.sqlx/query-0ad212233983ef7c10dc16d202d35251e321f3083c2e8aa28a98444ebc8430f3.json`
  - `rust/.sqlx/query-0dfad953279837024b145902ee231bac620126b9f1f5b1b9d411fe356f24e009.json`
  - `rust/.sqlx/query-111087e8833cf76f4b938091a726389ef07551ce208b440ed120f0b47b0cd34d.json`
  - `rust/.sqlx/query-16ff8a93cd6ef1d08bd3e80320a06e2cd3b0ec81223d72abd5717a405a5bb3b8.json`
  - … 260 weitere

### internal/deadlock-twitch-bot/smalltalk-shadow.html (grob, 176 Commits seit Pruefung)

Stand der Seite: 2026-07-27
- `Deadlock-Twitch-Bot` (rust, features) ab `3b74c611` [datum-abgeleitet, grob]: 176 Commits, 268 Dateien
  - `rust/.cargo/audit.toml`
  - `rust/.sqlx/query-00748f8a6734810c5b88b17f3db55311a86abaf4e77a2e2cb672e418c2e4d11c.json`
  - `rust/.sqlx/query-06df9f1066fbe003f82f4eb567df77e08edcf9ae7f31f8db0796613e96d214c4.json`
  - `rust/.sqlx/query-09308917b86027e8e264cb9d3671ff6bf08cb5a69e384e84c633a3a0423337b1.json`
  - `rust/.sqlx/query-0ad212233983ef7c10dc16d202d35251e321f3083c2e8aa28a98444ebc8430f3.json`
  - `rust/.sqlx/query-0dfad953279837024b145902ee231bac620126b9f1f5b1b9d411fe356f24e009.json`
  - `rust/.sqlx/query-111087e8833cf76f4b938091a726389ef07551ce208b440ed120f0b47b0cd34d.json`
  - `rust/.sqlx/query-16ff8a93cd6ef1d08bd3e80320a06e2cd3b0ec81223d72abd5717a405a5bb3b8.json`
  - … 260 weitere

### internal/deadlock-twitch-bot/crew-guard-radar.html (grob, 154 Commits seit Pruefung)

Stand der Seite: 2026-07-28
- `Deadlock-Twitch-Bot` (rust, features) ab `1283d481` [datum-abgeleitet, grob]: 154 Commits, 248 Dateien
  - `rust/.cargo/audit.toml`
  - `rust/.sqlx/query-00748f8a6734810c5b88b17f3db55311a86abaf4e77a2e2cb672e418c2e4d11c.json`
  - `rust/.sqlx/query-06df9f1066fbe003f82f4eb567df77e08edcf9ae7f31f8db0796613e96d214c4.json`
  - `rust/.sqlx/query-09308917b86027e8e264cb9d3671ff6bf08cb5a69e384e84c633a3a0423337b1.json`
  - `rust/.sqlx/query-0ad212233983ef7c10dc16d202d35251e321f3083c2e8aa28a98444ebc8430f3.json`
  - `rust/.sqlx/query-0dfad953279837024b145902ee231bac620126b9f1f5b1b9d411fe356f24e009.json`
  - `rust/.sqlx/query-111087e8833cf76f4b938091a726389ef07551ce208b440ed120f0b47b0cd34d.json`
  - `rust/.sqlx/query-16ff8a93cd6ef1d08bd3e80320a06e2cd3b0ec81223d72abd5717a405a5bb3b8.json`
  - … 240 weitere

### internal/website/uebersicht.html (grob, 117 Commits seit Pruefung)

Stand der Seite: 2026-07-07
- `Website` (builds, dl-coaching, dl-landing) ab `66a9c32b` [datum-abgeleitet, grob]: 117 Commits, 130 Dateien
  - `builds/backend-rust/Cargo.lock`
  - `builds/backend-rust/Cargo.toml`
  - `builds/backend-rust/DEPLOY-NOTES-video-bibliothek.md`
  - `builds/backend-rust/README.md`
  - `builds/backend-rust/migrations/2026071999_video_library.sql`
  - `builds/backend-rust/migrations/2026072000_video_action_audit.sql`
  - `builds/backend-rust/src/app.rs`
  - `builds/backend-rust/src/auth.rs`
  - … 122 weitere

### internal/deadlock-twitch-bot/verwaltung-selbstbedienung.html (grob, 115 Commits seit Pruefung)

Stand der Seite: 2026-08-03
- `Deadlock-Twitch-Bot` (rust, features) ab `22fd298d` [datum-abgeleitet, grob]: 115 Commits, 177 Dateien
  - `rust/.cargo/audit.toml`
  - `rust/.sqlx/query-00748f8a6734810c5b88b17f3db55311a86abaf4e77a2e2cb672e418c2e4d11c.json`
  - `rust/.sqlx/query-09308917b86027e8e264cb9d3671ff6bf08cb5a69e384e84c633a3a0423337b1.json`
  - `rust/.sqlx/query-0a07d8bfba936f213c2b433571721f61470e6f7799639987620e812b3ccd55f0.json`
  - `rust/.sqlx/query-0ad212233983ef7c10dc16d202d35251e321f3083c2e8aa28a98444ebc8430f3.json`
  - `rust/.sqlx/query-16ff8a93cd6ef1d08bd3e80320a06e2cd3b0ec81223d72abd5717a405a5bb3b8.json`
  - `rust/.sqlx/query-1723ed266dbe2b05dadf505c550993a75eb0b5a18d3e711214ac9c29f2562f8b.json`
  - `rust/.sqlx/query-1832423ba17b4527ad44cbb14f7480f348fdd574eabeed4db326ef51c2a4139f.json`
  - … 169 weitere

### internal/website/architektur.html (grob, 110 Commits seit Pruefung)

Stand der Seite: 2026-07-10
- `Website` (builds, dl-coaching, dl-landing) ab `f305c821` [datum-abgeleitet, grob]: 110 Commits, 128 Dateien
  - `builds/backend-rust/Cargo.lock`
  - `builds/backend-rust/Cargo.toml`
  - `builds/backend-rust/DEPLOY-NOTES-video-bibliothek.md`
  - `builds/backend-rust/README.md`
  - `builds/backend-rust/migrations/2026071999_video_library.sql`
  - `builds/backend-rust/migrations/2026072000_video_action_audit.sql`
  - `builds/backend-rust/src/app.rs`
  - `builds/backend-rust/src/auth.rs`
  - … 120 weitere

### internal/deadlock-turniere/uebersicht.html (grob, 107 Commits seit Pruefung)

Stand der Seite: 2026-07-07
- `Deadlock-Turniere` (rust, backend, frontend) ab `c6a5d2c9` [datum-abgeleitet, grob]: 107 Commits, 139 Dateien
  - `backend/__init__.py`
  - `backend/admin/__init__.py`
  - `backend/admin/test_mode.py`
  - `backend/auth/__init__.py`
  - `backend/auth/discord_oauth.py`
  - `backend/auth/middleware.py`
  - `backend/auth/permissions.py`
  - `backend/config.py`
  - … 131 weitere

### internal/website/betrieb.html (grob, 106 Commits seit Pruefung)

Stand der Seite: 2026-07-10
- `Website` (builds, scripts) ab `f305c821` [datum-abgeleitet, grob]: 106 Commits, 104 Dateien
  - `builds/backend-rust/Cargo.lock`
  - `builds/backend-rust/Cargo.toml`
  - `builds/backend-rust/DEPLOY-NOTES-video-bibliothek.md`
  - `builds/backend-rust/README.md`
  - `builds/backend-rust/migrations/2026071999_video_library.sql`
  - `builds/backend-rust/migrations/2026072000_video_action_audit.sql`
  - `builds/backend-rust/src/app.rs`
  - `builds/backend-rust/src/auth.rs`
  - … 96 weitere

### internal/deadlock-turniere/betrieb.html (grob, 102 Commits seit Pruefung)

Stand der Seite: 2026-07-12
- `Deadlock-Turniere` (rust, ops, scripts) ab `208c28bf` [datum-abgeleitet, grob]: 102 Commits, 68 Dateien
  - `ops/systemd/deadlock-turniere.service.example`
  - `rust/Cargo.lock`
  - `rust/crates/turnier-api/Cargo.toml`
  - `rust/crates/turnier-api/src/admin/automatik.rs`
  - `rust/crates/turnier-api/src/app.rs`
  - `rust/crates/turnier-api/src/draft.rs`
  - `rust/crates/turnier-api/src/error.rs`
  - `rust/crates/turnier-api/src/internal_automatik.rs`
  - … 60 weitere

### internal/deadlock-steam-bot/betrieb.html (grob, 101 Commits seit Pruefung)

Stand der Seite: 2026-07-08
- `Deadlock-Steam-Bot` (rust, scripts) ab `d8025714` [datum-abgeleitet, grob]: 101 Commits, 199 Dateien
  - `rust/.sqlx/query-016202238c2fe79d321d1f8c873d75585a5f0a35be607126b724b298e205fa8d.json`
  - `rust/.sqlx/query-04fcd77056839e21ca8270bca1c2c29328533082baf6dab083f0aa721df1d381.json`
  - `rust/.sqlx/query-0863636aa6ac78389deb8751d87fd069a1a7d27cd1f250423e735e082bbc2077.json`
  - `rust/.sqlx/query-0a32af394f4f16de182fbb55cd68e99fe6a1a9f44d17f32dc780b91ae37ba78d.json`
  - `rust/.sqlx/query-0d49b183c1421760ae41af8f85fb92e00118fa937162197241bfff1875ed0712.json`
  - `rust/.sqlx/query-1045b3d8cc81ee6518f699e634cd7396ea5b0619312f291bc9a7cc73d70e1a32.json`
  - `rust/.sqlx/query-123972121ed49650b28f6eddc1fe2b09b41e08158ff8dc2e889924b416426667.json`
  - `rust/.sqlx/query-13285ae2c88d2dd08155b19d411ce5095bd5a21405a357ebd0dd153748c65b03.json`
  - … 191 weitere

### internal/deadlock-turniere/architektur.html (grob, 101 Commits seit Pruefung)

Stand der Seite: 2026-07-07
- `Deadlock-Turniere` (rust, backend) ab `c6a5d2c9` [datum-abgeleitet, grob]: 101 Commits, 123 Dateien
  - `backend/__init__.py`
  - `backend/admin/__init__.py`
  - `backend/admin/test_mode.py`
  - `backend/auth/__init__.py`
  - `backend/auth/discord_oauth.py`
  - `backend/auth/middleware.py`
  - `backend/auth/permissions.py`
  - `backend/config.py`
  - … 115 weitere

### internal/deadlock-turniere/datenmodell.html (grob, 101 Commits seit Pruefung)

Stand der Seite: 2026-07-10
- `Deadlock-Turniere` (rust, backend) ab `c6a5d2c9` [datum-abgeleitet, grob]: 101 Commits, 123 Dateien
  - `backend/__init__.py`
  - `backend/admin/__init__.py`
  - `backend/admin/test_mode.py`
  - `backend/auth/__init__.py`
  - `backend/auth/discord_oauth.py`
  - `backend/auth/middleware.py`
  - `backend/auth/permissions.py`
  - `backend/config.py`
  - … 115 weitere

### internal/deadlock-turniere/integrationen.html (grob, 101 Commits seit Pruefung)

Stand der Seite: 2026-07-07
- `Deadlock-Turniere` (rust, backend) ab `c6a5d2c9` [datum-abgeleitet, grob]: 101 Commits, 123 Dateien
  - `backend/__init__.py`
  - `backend/admin/__init__.py`
  - `backend/admin/test_mode.py`
  - `backend/auth/__init__.py`
  - `backend/auth/discord_oauth.py`
  - `backend/auth/middleware.py`
  - `backend/auth/permissions.py`
  - `backend/config.py`
  - … 115 weitere

### internal/deadlock-turniere/match-automatik.html (grob, 101 Commits seit Pruefung)

Stand der Seite: 2026-07-07
- `Deadlock-Turniere` (rust, backend) ab `c6a5d2c9` [datum-abgeleitet, grob]: 101 Commits, 123 Dateien
  - `backend/__init__.py`
  - `backend/admin/__init__.py`
  - `backend/admin/test_mode.py`
  - `backend/auth/__init__.py`
  - `backend/auth/discord_oauth.py`
  - `backend/auth/middleware.py`
  - `backend/auth/permissions.py`
  - `backend/config.py`
  - … 115 weitere

### internal/deadlock-steam-bot/architektur.html (grob, 100 Commits seit Pruefung)

Stand der Seite: 2026-07-08
- `Deadlock-Steam-Bot` (rust) ab `d8025714` [datum-abgeleitet, grob]: 100 Commits, 197 Dateien
  - `rust/.sqlx/query-016202238c2fe79d321d1f8c873d75585a5f0a35be607126b724b298e205fa8d.json`
  - `rust/.sqlx/query-04fcd77056839e21ca8270bca1c2c29328533082baf6dab083f0aa721df1d381.json`
  - `rust/.sqlx/query-0863636aa6ac78389deb8751d87fd069a1a7d27cd1f250423e735e082bbc2077.json`
  - `rust/.sqlx/query-0a32af394f4f16de182fbb55cd68e99fe6a1a9f44d17f32dc780b91ae37ba78d.json`
  - `rust/.sqlx/query-0d49b183c1421760ae41af8f85fb92e00118fa937162197241bfff1875ed0712.json`
  - `rust/.sqlx/query-1045b3d8cc81ee6518f699e634cd7396ea5b0619312f291bc9a7cc73d70e1a32.json`
  - `rust/.sqlx/query-123972121ed49650b28f6eddc1fe2b09b41e08158ff8dc2e889924b416426667.json`
  - `rust/.sqlx/query-13285ae2c88d2dd08155b19d411ce5095bd5a21405a357ebd0dd153748c65b03.json`
  - … 189 weitere

### internal/deadlock-steam-bot/datenmodell.html (grob, 100 Commits seit Pruefung)

Stand der Seite: 2026-07-08
- `Deadlock-Steam-Bot` (rust) ab `d8025714` [datum-abgeleitet, grob]: 100 Commits, 197 Dateien
  - `rust/.sqlx/query-016202238c2fe79d321d1f8c873d75585a5f0a35be607126b724b298e205fa8d.json`
  - `rust/.sqlx/query-04fcd77056839e21ca8270bca1c2c29328533082baf6dab083f0aa721df1d381.json`
  - `rust/.sqlx/query-0863636aa6ac78389deb8751d87fd069a1a7d27cd1f250423e735e082bbc2077.json`
  - `rust/.sqlx/query-0a32af394f4f16de182fbb55cd68e99fe6a1a9f44d17f32dc780b91ae37ba78d.json`
  - `rust/.sqlx/query-0d49b183c1421760ae41af8f85fb92e00118fa937162197241bfff1875ed0712.json`
  - `rust/.sqlx/query-1045b3d8cc81ee6518f699e634cd7396ea5b0619312f291bc9a7cc73d70e1a32.json`
  - `rust/.sqlx/query-123972121ed49650b28f6eddc1fe2b09b41e08158ff8dc2e889924b416426667.json`
  - `rust/.sqlx/query-13285ae2c88d2dd08155b19d411ce5095bd5a21405a357ebd0dd153748c65b03.json`
  - … 189 weitere

### internal/deadlock-steam-bot/integrationen.html (grob, 100 Commits seit Pruefung)

Stand der Seite: 2026-07-08
- `Deadlock-Steam-Bot` (rust) ab `d8025714` [datum-abgeleitet, grob]: 100 Commits, 197 Dateien
  - `rust/.sqlx/query-016202238c2fe79d321d1f8c873d75585a5f0a35be607126b724b298e205fa8d.json`
  - `rust/.sqlx/query-04fcd77056839e21ca8270bca1c2c29328533082baf6dab083f0aa721df1d381.json`
  - `rust/.sqlx/query-0863636aa6ac78389deb8751d87fd069a1a7d27cd1f250423e735e082bbc2077.json`
  - `rust/.sqlx/query-0a32af394f4f16de182fbb55cd68e99fe6a1a9f44d17f32dc780b91ae37ba78d.json`
  - `rust/.sqlx/query-0d49b183c1421760ae41af8f85fb92e00118fa937162197241bfff1875ed0712.json`
  - `rust/.sqlx/query-1045b3d8cc81ee6518f699e634cd7396ea5b0619312f291bc9a7cc73d70e1a32.json`
  - `rust/.sqlx/query-123972121ed49650b28f6eddc1fe2b09b41e08158ff8dc2e889924b416426667.json`
  - `rust/.sqlx/query-13285ae2c88d2dd08155b19d411ce5095bd5a21405a357ebd0dd153748c65b03.json`
  - … 189 weitere

### internal/deadlock-steam-bot/task-queue.html (grob, 100 Commits seit Pruefung)

Stand der Seite: 2026-07-08
- `Deadlock-Steam-Bot` (rust) ab `d8025714` [datum-abgeleitet, grob]: 100 Commits, 197 Dateien
  - `rust/.sqlx/query-016202238c2fe79d321d1f8c873d75585a5f0a35be607126b724b298e205fa8d.json`
  - `rust/.sqlx/query-04fcd77056839e21ca8270bca1c2c29328533082baf6dab083f0aa721df1d381.json`
  - `rust/.sqlx/query-0863636aa6ac78389deb8751d87fd069a1a7d27cd1f250423e735e082bbc2077.json`
  - `rust/.sqlx/query-0a32af394f4f16de182fbb55cd68e99fe6a1a9f44d17f32dc780b91ae37ba78d.json`
  - `rust/.sqlx/query-0d49b183c1421760ae41af8f85fb92e00118fa937162197241bfff1875ed0712.json`
  - `rust/.sqlx/query-1045b3d8cc81ee6518f699e634cd7396ea5b0619312f291bc9a7cc73d70e1a32.json`
  - `rust/.sqlx/query-123972121ed49650b28f6eddc1fe2b09b41e08158ff8dc2e889924b416426667.json`
  - `rust/.sqlx/query-13285ae2c88d2dd08155b19d411ce5095bd5a21405a357ebd0dd153748c65b03.json`
  - … 189 weitere

### internal/deadlock-steam-bot/uebersicht.html (grob, 100 Commits seit Pruefung)

Stand der Seite: 2026-07-08
- `Deadlock-Steam-Bot` (rust) ab `d8025714` [datum-abgeleitet, grob]: 100 Commits, 197 Dateien
  - `rust/.sqlx/query-016202238c2fe79d321d1f8c873d75585a5f0a35be607126b724b298e205fa8d.json`
  - `rust/.sqlx/query-04fcd77056839e21ca8270bca1c2c29328533082baf6dab083f0aa721df1d381.json`
  - `rust/.sqlx/query-0863636aa6ac78389deb8751d87fd069a1a7d27cd1f250423e735e082bbc2077.json`
  - `rust/.sqlx/query-0a32af394f4f16de182fbb55cd68e99fe6a1a9f44d17f32dc780b91ae37ba78d.json`
  - `rust/.sqlx/query-0d49b183c1421760ae41af8f85fb92e00118fa937162197241bfff1875ed0712.json`
  - `rust/.sqlx/query-1045b3d8cc81ee6518f699e634cd7396ea5b0619312f291bc9a7cc73d70e1a32.json`
  - `rust/.sqlx/query-123972121ed49650b28f6eddc1fe2b09b41e08158ff8dc2e889924b416426667.json`
  - `rust/.sqlx/query-13285ae2c88d2dd08155b19d411ce5095bd5a21405a357ebd0dd153748c65b03.json`
  - … 189 weitere

### internal/website/datenmodell.html (grob, 69 Commits seit Pruefung)

Stand der Seite: 2026-07-07
- `Website` (builds) ab `66a9c32b` [datum-abgeleitet, grob]: 69 Commits, 96 Dateien
  - `builds/backend-rust/Cargo.lock`
  - `builds/backend-rust/Cargo.toml`
  - `builds/backend-rust/DEPLOY-NOTES-video-bibliothek.md`
  - `builds/backend-rust/README.md`
  - `builds/backend-rust/migrations/2026071999_video_library.sql`
  - `builds/backend-rust/migrations/2026072000_video_action_audit.sql`
  - `builds/backend-rust/src/app.rs`
  - `builds/backend-rust/src/auth.rs`
  - … 88 weitere

### internal/website/integrationen.html (grob, 69 Commits seit Pruefung)

Stand der Seite: 2026-07-07
- `Website` (builds) ab `66a9c32b` [datum-abgeleitet, grob]: 69 Commits, 96 Dateien
  - `builds/backend-rust/Cargo.lock`
  - `builds/backend-rust/Cargo.toml`
  - `builds/backend-rust/DEPLOY-NOTES-video-bibliothek.md`
  - `builds/backend-rust/README.md`
  - `builds/backend-rust/migrations/2026071999_video_library.sql`
  - `builds/backend-rust/migrations/2026072000_video_action_audit.sql`
  - `builds/backend-rust/src/app.rs`
  - `builds/backend-rust/src/auth.rs`
  - … 88 weitere

### internal/deadlock-turniere/draft-lobbys.html (grob, 67 Commits seit Pruefung)

Stand der Seite: 2026-07-16
- `Deadlock-Turniere` (rust, backend, frontend) ab `16490dcf` [datum-abgeleitet, grob]: 67 Commits, 89 Dateien
  - `backend/__init__.py`
  - `backend/admin/__init__.py`
  - `backend/admin/test_mode.py`
  - `backend/auth/__init__.py`
  - `backend/auth/discord_oauth.py`
  - `backend/auth/middleware.py`
  - `backend/auth/permissions.py`
  - `backend/config.py`
  - … 81 weitere

### internal/betrieb/routing-caddy.html (grob, 36 Commits seit Pruefung)

Stand der Seite: 2026-07-07
- `Caddy` (.) ab `89c1f8ab` [datum-abgeleitet, grob]: 36 Commits, 8 Dateien
  - `CLAUDE.md`
  - `README.md`
  - `conf/Caddyfile`
  - `docker-compose.yml`
  - `hosts/v50671/Caddyfile`
  - `hosts/v50671/systemd/10-logs.conf`
  - `hosts/v50671/systemd/20-tailscale.conf`
  - `hosts/v50671/systemd/99-caddy-nonlocal-bind.sysctl.conf`

### internal/patchnotes-bot/architektur.html (grob, 26 Commits seit Pruefung)

Stand der Seite: 2026-07-07
- `Deadlock--Patchnotes-Bot` (.) ab `e1c71cba` [datum-abgeleitet, grob]: 26 Commits, 13 Dateien
  - `.github/workflows/security.yml`
  - `changelog_latest_fetcher.py`
  - `entity_emojis.py`
  - `main.py`
  - `patch_view.py`
  - `scripts/recolor_patch_containers.py`
  - `scripts/run_patchnotes_bot.sh`
  - `scripts/run_prepared_patch_once.sh`
  - … 5 weitere

### internal/patchnotes-bot/betrieb.html (grob, 26 Commits seit Pruefung)

Stand der Seite: 2026-07-07
- `Deadlock--Patchnotes-Bot` (.) ab `e1c71cba` [datum-abgeleitet, grob]: 26 Commits, 13 Dateien
  - `.github/workflows/security.yml`
  - `changelog_latest_fetcher.py`
  - `entity_emojis.py`
  - `main.py`
  - `patch_view.py`
  - `scripts/recolor_patch_containers.py`
  - `scripts/run_patchnotes_bot.sh`
  - `scripts/run_prepared_patch_once.sh`
  - … 5 weitere

### internal/patchnotes-bot/integrationen.html (grob, 26 Commits seit Pruefung)

Stand der Seite: 2026-07-07
- `Deadlock--Patchnotes-Bot` (.) ab `e1c71cba` [datum-abgeleitet, grob]: 26 Commits, 13 Dateien
  - `.github/workflows/security.yml`
  - `changelog_latest_fetcher.py`
  - `entity_emojis.py`
  - `main.py`
  - `patch_view.py`
  - `scripts/recolor_patch_containers.py`
  - `scripts/run_patchnotes_bot.sh`
  - `scripts/run_prepared_patch_once.sh`
  - … 5 weitere

### internal/patchnotes-bot/uebersicht.html (grob, 26 Commits seit Pruefung)

Stand der Seite: 2026-07-07
- `Deadlock--Patchnotes-Bot` (.) ab `e1c71cba` [datum-abgeleitet, grob]: 26 Commits, 13 Dateien
  - `.github/workflows/security.yml`
  - `changelog_latest_fetcher.py`
  - `entity_emojis.py`
  - `main.py`
  - `patch_view.py`
  - `scripts/recolor_patch_containers.py`
  - `scripts/run_patchnotes_bot.sh`
  - `scripts/run_prepared_patch_once.sh`
  - … 5 weitere

### internal/betrieb/deploy.html (grob, 12 Commits seit Pruefung)

Stand der Seite: 2026-07-07
- `Deadlock-Bots` (scripts) ab `9669df25` [datum-abgeleitet, grob]: 12 Commits, 7 Dateien
  - `scripts/check-local.sh`
  - `scripts/export_infisical_env.py`
  - `scripts/kill_stale_bot.sh`
  - `scripts/run_brain_feeder.sh`
  - `scripts/run_dl_knowledge_service.sh`
  - `scripts/run_verbinder.sh`
  - `scripts/wait_for_infisical.sh`

### internal/deadlock-brain/match-demo-learning.html (grob, 10 Commits seit Pruefung)

Stand der Seite: 2026-07-10
- `Deadlock-Brain` (rust, src) ab `10edcd42` [datum-abgeleitet, grob]: 10 Commits, 5 Dateien
  - `rust/Cargo.lock`
  - `rust/crates/dbrain-retrieval/Cargo.toml`
  - `rust/crates/dbrain-retrieval/src/game_wiki.rs`
  - `rust/crates/dbrain-retrieval/src/lib.rs`
  - `rust/crates/deadlock-brain/src/main.rs`

### internal/website/scrim-cockpit-handbuch.html (grob, 9 Commits seit Pruefung)

Stand der Seite: 2026-07-16
- `Website` (dl-coaching, builds/backend-rust/src/routes/scrim.rs) ab `5b9bfa3b` [datum-abgeleitet, grob]: 9 Commits, 9 Dateien
  - `builds/backend-rust/src/routes/scrim.rs`
  - `dl-coaching/index.html`
  - `dl-coaching/src/App.tsx`
  - `dl-coaching/src/api/client.ts`
  - `dl-coaching/src/components/Layout.tsx`
  - `dl-coaching/src/lib/commandCenter.test.ts`
  - `dl-coaching/src/lib/commandCenter.ts`
  - `dl-coaching/src/pages/ScrimCommandCenterPage.tsx`
  - … 1 weitere

### internal/betrieb/secrets-infisical.html (grob, 7 Commits seit Pruefung)

Stand der Seite: 2026-07-12
- `Deadlock-Bots` (scripts) ab `3bc8ca8a` [explizit, grob]: 7 Commits, 7 Dateien
  - `scripts/check-local.sh`
  - `scripts/export_infisical_env.py`
  - `scripts/kill_stale_bot.sh`
  - `scripts/run_brain_feeder.sh`
  - `scripts/run_dl_knowledge_service.sh`
  - `scripts/run_verbinder.sh`
  - `scripts/test_dl_knowledge_launcher.py`

### internal/deadlock-bots/betrieb.html (grob, 7 Commits seit Pruefung)

Stand der Seite: 2026-07-12
- `Deadlock-Bots` (scripts) ab `3bc8ca8a` [explizit, grob]: 7 Commits, 7 Dateien
  - `scripts/check-local.sh`
  - `scripts/export_infisical_env.py`
  - `scripts/kill_stale_bot.sh`
  - `scripts/run_brain_feeder.sh`
  - `scripts/run_dl_knowledge_service.sh`
  - `scripts/run_verbinder.sh`
  - `scripts/test_dl_knowledge_launcher.py`
- `Deadlock-Docs` (tools/deploy_corpus.sh) ab `08c01ff0` [datum-abgeleitet, genau]: 0 Commits, 0 Dateien

## aktuell (1)

### internal/STYLEGUIDE.html

Stand der Seite: 2026-07-11
- `Deadlock-Docs` (tools/validate_corpus.py) ab `5dfe43fb` [datum-abgeleitet, genau]: 0 Commits, 0 Dateien

## nicht-verfolgt (2)

### internal/betrieb/zentrale-bot-config.html

Stand der Seite: 2026-07-27
Grund: Quelle sind Host-Dateien (~/.config/deadlock/bots.env, systemd-Drop-ins), kein Repo

### internal/deadlock-turniere/draft-lobbys-redaction-notes.html

Stand der Seite: 2026-07-16
Grund: Redaktionspruefung einer Doku-Seite, kein Code-Bezug
