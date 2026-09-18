# Frische der internen Wissensseiten

Erzeugt: 2026-09-18 von `tools/check_freshness.py` aus `quellen.json`.

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

### internal/deadlock-bots/stats-und-privacy-devs.html (genau, 305 Commits seit Pruefung)

Stand der Seite: 2026-07-12
- `Deadlock-Bots` (rust/crates/dl-activity, rust/crates/dl-community, rust/crates/dl-voice, rust/crates/dl-central-db) ab `3bc8ca8a` [explizit, genau]: 192 Commits, 117 Dateien
  - `rust/crates/dl-activity/Cargo.toml`
  - `rust/crates/dl-activity/src/analyzer.rs`
  - `rust/crates/dl-activity/src/lfg_freetext.rs`
  - `rust/crates/dl-activity/src/lib.rs`
  - `rust/crates/dl-activity/src/outbox.rs`
  - `rust/crates/dl-activity/src/survey_pulse.rs`
  - `rust/crates/dl-central-db/Cargo.toml`
  - `rust/crates/dl-central-db/build.rs`
  - … 109 weitere
- `Deadlock-Steam-Bot` (rust) ab `6fad947c` [explizit, grob]: 113 Commits, 152 Dateien
  - `rust/.sqlx/query-0206b6cdb9ad61c91d680e8938b06fd9f504d740e38fcd6e13c71881616f1d9d.json`
  - `rust/.sqlx/query-1045b3d8cc81ee6518f699e634cd7396ea5b0619312f291bc9a7cc73d70e1a32.json`
  - `rust/.sqlx/query-158079b4bdbfb714a7d4845bbc45bb1690f77595b07d53df9630f3a7e4639e3c.json`
  - `rust/.sqlx/query-2266eaf88d227d9de58ff57fcadca118b8f1e5d711cbea9499ddf1411ac1b449.json`
  - `rust/.sqlx/query-28b7acee3c82a1105ee3bc9df8d29bfb2c6328e95dfc51a1dea980ef68ef9263.json`
  - `rust/.sqlx/query-2be74e269e4364624ed0479bca9e1da5af4ce45bc4de5f0f071b993898b8940d.json`
  - `rust/.sqlx/query-2fb699804b88f1f704057f7becdceaabd31f175b4e52516db53c789dda092789.json`
  - `rust/.sqlx/query-35e28e42ca581cae21549de2294b018938c9f19801392c1edc23c280547eae62.json`
  - … 144 weitere
- `Deadlock-Docs` (public/discord-server/stats-und-privacy.html) ab `08c01ff0` [datum-abgeleitet, genau]: 0 Commits, 0 Dateien

### internal/betrieb/uebersicht.html (genau, 124 Commits seit Pruefung)

Stand der Seite: 2026-07-11
- `Deadlock-Bots` (scripts) ab `7b0f35bb` [datum-abgeleitet, grob]: 17 Commits, 10 Dateien
  - `scripts/check-local.sh`
  - `scripts/export_infisical_env.py`
  - `scripts/kill_stale_bot.sh`
  - `scripts/maintenance/repair_discord_system_messages_20260908.sql`
  - `scripts/run_brain_feeder.sh`
  - `scripts/run_dl_insights_sync.sh`
  - `scripts/run_dl_knowledge_service.sh`
  - `scripts/run_verbinder.sh`
  - … 2 weitere
- `Caddy` (.) ab `9f2bd24b` [datum-abgeleitet, grob]: 51 Commits, 8 Dateien
  - `CLAUDE.md`
  - `README.md`
  - `conf/Caddyfile`
  - `docker-compose.yml`
  - `hosts/v50671/Caddyfile`
  - `hosts/v50671/systemd/10-logs.conf`
  - `hosts/v50671/systemd/20-tailscale.conf`
  - `hosts/v50671/systemd/99-caddy-nonlocal-bind.sysctl.conf`
- `Deadlock-Twitch-Bot` (ops/systemd, rust/scripts) ab `5082d53f` [explizit, genau]: 56 Commits, 22 Dateien
  - Hinweis: geprueft liegt nicht auf main; verglichen ab gemeinsamem Vorfahr 17017cbc (meldet eher zu viel als zu wenig)
  - `ops/systemd/README-twitch-runtime-security.md`
  - `ops/systemd/audit.conf`
  - `ops/systemd/bot.conf`
  - `ops/systemd/dashboard.conf`
  - `ops/systemd/deadlock-streamlink`
  - `ops/systemd/deadlock-twitch-bot-rust.service`
  - `ops/systemd/deadlock-twitch-bot-watchdog.conf`
  - `ops/systemd/deadlock-twitch-bot-watchdog.service`
  - … 14 weitere

### internal/deadlock-twitch-bot/stream-coaching-audit.html (genau, 108 Commits seit Pruefung)

Stand der Seite: 2026-08-14
- `Deadlock-Twitch-Bot` (rust/crates/tb-stream-audit, rust/bin/tb-stream-audit, rust/crates/tb-engagement/src/audio_capture.rs, rust/crates/tb-engagement/src/transcribe.rs, rust/crates/tb-llm/src/selection.rs, rust/scripts/run_stream_audit_service.sh, ops/systemd/deadlock-twitch-stream-coaching-watch.service) ab `5082d53f` [explizit, genau]: 108 Commits, 17 Dateien
  - Hinweis: geprueft liegt nicht auf main; verglichen ab gemeinsamem Vorfahr 17017cbc (meldet eher zu viel als zu wenig)
  - `ops/systemd/deadlock-twitch-stream-coaching-watch.service`
  - `rust/bin/tb-stream-audit/Cargo.toml`
  - `rust/bin/tb-stream-audit/src/main.rs`
  - `rust/crates/tb-engagement/src/audio_capture.rs`
  - `rust/crates/tb-engagement/src/transcribe.rs`
  - `rust/crates/tb-llm/src/selection.rs`
  - `rust/crates/tb-stream-audit/Cargo.toml`
  - `rust/crates/tb-stream-audit/src/archiv.rs`
  - … 9 weitere

### internal/betrieb/datenbank.html (genau, 93 Commits seit Pruefung)

Stand der Seite: 2026-07-07
- `Deadlock-Bots` (rust/crates/dl-central-db, rust/crates/dl-central-etl) ab `9669df25` [datum-abgeleitet, genau]: 93 Commits, 87 Dateien
  - `rust/crates/dl-central-db/Cargo.toml`
  - `rust/crates/dl-central-db/build.rs`
  - `rust/crates/dl-central-db/migrations/2026070913_invite_requests.sql`
  - `rust/crates/dl-central-db/migrations/2026071010_router_intro_dm_marker.sql`
  - `rust/crates/dl-central-db/migrations/2026071110_discord_audit_log.sql`
  - `rust/crates/dl-central-db/migrations/2026071111_steam_bot_event_log.sql`
  - `rust/crates/dl-central-db/migrations/2026071112_pate_journey_metadata_scrub.sql`
  - `rust/crates/dl-central-db/migrations/2026071120_invite_dispatch_claim.sql`
  - … 79 weitere

### internal/deadlock-bots/datenmodell.html (genau, 93 Commits seit Pruefung)

Stand der Seite: 2026-07-07
- `Deadlock-Bots` (rust/crates/dl-central-db) ab `9669df25` [datum-abgeleitet, genau]: 93 Commits, 87 Dateien
  - `rust/crates/dl-central-db/Cargo.toml`
  - `rust/crates/dl-central-db/build.rs`
  - `rust/crates/dl-central-db/migrations/2026070913_invite_requests.sql`
  - `rust/crates/dl-central-db/migrations/2026071010_router_intro_dm_marker.sql`
  - `rust/crates/dl-central-db/migrations/2026071110_discord_audit_log.sql`
  - `rust/crates/dl-central-db/migrations/2026071111_steam_bot_event_log.sql`
  - `rust/crates/dl-central-db/migrations/2026071112_pate_journey_metadata_scrub.sql`
  - `rust/crates/dl-central-db/migrations/2026071120_invite_dispatch_claim.sql`
  - … 79 weitere

### internal/deadlock-bots/voice-features-devs.html (genau, 63 Commits seit Pruefung)

Stand der Seite: 2026-07-11
- `Deadlock-Bots` (rust/crates/dl-voice) ab `7b0f35bb` [datum-abgeleitet, genau]: 61 Commits, 20 Dateien
  - `rust/crates/dl-voice/Cargo.toml`
  - `rust/crates/dl-voice/src/adaptive.rs`
  - `rust/crates/dl-voice/src/feedback.rs`
  - `rust/crates/dl-voice/src/glue.rs`
  - `rust/crates/dl-voice/src/lfg_panel.rs`
  - `rust/crates/dl-voice/src/lfg_watch.rs`
  - `rust/crates/dl-voice/src/lib.rs`
  - `rust/crates/dl-voice/src/mate_survey.rs`
  - … 12 weitere
- `Deadlock-Docs` (public/discord-server/voice-features.html) ab `5dfe43fb` [datum-abgeleitet, genau]: 2 Commits, 1 Dateien
  - `public/discord-server/voice-features.html`

### internal/deadlock-bots/onboarding-concierge-llm-compliance.html (genau, 43 Commits seit Pruefung)

Stand der Seite: 2026-07-07
- `Deadlock-Bots` (rust/crates/dl-community/src/concierge.rs) ab `9669df25` [datum-abgeleitet, genau]: 43 Commits, 1 Dateien
  - `rust/crates/dl-community/src/concierge.rs`

### internal/deadlock-bots/faq-bot-selbst-devs.html (genau, 20 Commits seit Pruefung)

Stand der Seite: 2026-07-12
- `Deadlock-Bots` (rust/bin/dl-knowledge, rust/crates/dl-community/src/faq.rs, rust/crates/dl-community/src/concierge.rs) ab `3bc8ca8a` [explizit, genau]: 20 Commits, 3 Dateien
  - `rust/bin/dl-knowledge/src/main.rs`
  - `rust/crates/dl-community/src/concierge.rs`
  - `rust/crates/dl-community/src/faq.rs`
- `Deadlock-Docs` (public/discord-server/faq-bot-selbst.html) ab `08c01ff0` [datum-abgeleitet, genau]: 0 Commits, 0 Dateien

### internal/deadlock-bots/faq-grounding.html (genau, 20 Commits seit Pruefung)

Stand der Seite: 2026-07-12
- `Deadlock-Bots` (rust/bin/dl-knowledge, rust/crates/dl-community/src/faq.rs, rust/crates/dl-community/src/concierge.rs) ab `3bc8ca8a` [explizit, genau]: 20 Commits, 3 Dateien
  - `rust/bin/dl-knowledge/src/main.rs`
  - `rust/crates/dl-community/src/concierge.rs`
  - `rust/crates/dl-community/src/faq.rs`

### internal/deadlock-bots/support-agent-design.html (genau, 20 Commits seit Pruefung)

Stand der Seite: 2026-07-12
- `Deadlock-Bots` (rust/bin/dl-knowledge, rust/crates/dl-community/src/faq.rs, rust/crates/dl-community/src/concierge.rs) ab `3bc8ca8a` [explizit, genau]: 20 Commits, 3 Dateien
  - `rust/bin/dl-knowledge/src/main.rs`
  - `rust/crates/dl-community/src/concierge.rs`
  - `rust/crates/dl-community/src/faq.rs`

### internal/deadlock-bots/onboarding-concierge-slice-b-c.html (genau, 18 Commits seit Pruefung)

Stand der Seite: 2026-07-11
- `Deadlock-Bots` (rust/crates/dl-community/src/concierge.rs, rust/crates/dl-voice/src/nudge.rs, rust/crates/dl-voice/src/feedback.rs) ab `7b0f35bb` [datum-abgeleitet, genau]: 18 Commits, 3 Dateien
  - `rust/crates/dl-community/src/concierge.rs`
  - `rust/crates/dl-voice/src/feedback.rs`
  - `rust/crates/dl-voice/src/nudge.rs`

### internal/deadlock-bots/twitch-clips-und-social.html (genau, 18 Commits seit Pruefung)

Stand der Seite: 2026-07-07
- `Deadlock-Bots` (docs/twitch-clips-und-social.md, rust/crates/dl-bridges) ab `9669df25` [datum-abgeleitet, genau]: 18 Commits, 3 Dateien
  - `rust/crates/dl-bridges/src/matcher.rs`
  - `rust/crates/dl-bridges/src/steam.rs`
  - `rust/crates/dl-bridges/src/twitch.rs`

### internal/deadlock-bots/server-insights.html (genau, 17 Commits seit Pruefung)

Stand der Seite: 2026-07-07
- `Deadlock-Bots` (docs/server_insights.md, rust/crates/dl-stats) ab `9669df25` [datum-abgeleitet, genau]: 17 Commits, 3 Dateien
  - `docs/server_insights.md`
  - `rust/crates/dl-stats/src/me.rs`
  - `rust/crates/dl-stats/src/public.rs`

### internal/deadlock-bots/onboarding-concierge-devs.html (genau, 16 Commits seit Pruefung)

Stand der Seite: 2026-07-11
- `Deadlock-Bots` (rust/crates/dl-community/src/concierge.rs) ab `b069b5c8` [explizit, genau]: 16 Commits, 1 Dateien
  - `rust/crates/dl-community/src/concierge.rs`

### internal/deadlock-bots/onboarding-concierge-texte.html (genau, 16 Commits seit Pruefung)

Stand der Seite: 2026-07-11
- `Deadlock-Bots` (rust/crates/dl-community/src/concierge.rs) ab `b069b5c8` [explizit, genau]: 16 Commits, 1 Dateien
  - `rust/crates/dl-community/src/concierge.rs`

### internal/deadlock-bots/integrationen.html (genau, 12 Commits seit Pruefung)

Stand der Seite: 2026-07-11
- `Deadlock-Bots` (rust/crates/dl-bridges) ab `7b0f35bb` [datum-abgeleitet, genau]: 12 Commits, 3 Dateien
  - `rust/crates/dl-bridges/src/matcher.rs`
  - `rust/crates/dl-bridges/src/steam.rs`
  - `rust/crates/dl-bridges/src/twitch.rs`

### internal/deadlock-bots/moderation-scam-guard.html (genau, 7 Commits seit Pruefung)

Stand der Seite: 2026-07-07
- `Deadlock-Bots` (rust/crates/dl-moderation) ab `9669df25` [datum-abgeleitet, genau]: 7 Commits, 7 Dateien
  - `rust/crates/dl-moderation/src/action_policy.rs`
  - `rust/crates/dl-moderation/src/behavior_detector.rs`
  - `rust/crates/dl-moderation/src/case_embed.rs`
  - `rust/crates/dl-moderation/src/content_analyzer.rs`
  - `rust/crates/dl-moderation/src/content_verifier.rs`
  - `rust/crates/dl-moderation/src/lib.rs`
  - `rust/crates/dl-moderation/src/moderation_system.rs`

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

### internal/deadlock-bots/onboarding-und-invites-devs.html (genau, 2 Commits seit Pruefung)

Stand der Seite: 2026-07-10
- `Deadlock-Docs` (public/discord-server/onboarding-und-invites.html) ab `91f8207a` [datum-abgeleitet, genau]: 2 Commits, 1 Dateien
  - `public/discord-server/onboarding-und-invites.html`

### internal/deadlock-bots/scrim-orga-redaction-notes.html (genau, 2 Commits seit Pruefung)

Stand der Seite: 2026-07-24
- `Deadlock-Docs` (public/dokus/scrims) ab `697f05d0` [datum-abgeleitet, genau]: 2 Commits, 1 Dateien
  - `public/dokus/scrims/scrim-orga.html`

### internal/deadlock-twitch-bot/affiliate.html (grob, 1480 Commits seit Pruefung)

Stand der Seite: 2026-07-07
- `Deadlock-Twitch-Bot` (rust, bot) ab `03822a50` [datum-abgeleitet, grob]: 1480 Commits, 1707 Dateien
  - `bot/__init__.py`
  - `bot/admin_dashboard/package-lock.json`
  - `bot/admin_dashboard/package.json`
  - `bot/admin_dashboard/src/App.tsx`
  - `bot/admin_dashboard/src/api/brainLab.ts`
  - `bot/admin_dashboard/src/api/client.ts`
  - `bot/admin_dashboard/src/api/types.ts`
  - `bot/admin_dashboard/src/components/layout/AdminShell.tsx`
  - … 1699 weitere

### internal/deadlock-twitch-bot/integrationen.html (grob, 1480 Commits seit Pruefung)

Stand der Seite: 2026-07-07
- `Deadlock-Twitch-Bot` (rust, bot) ab `03822a50` [datum-abgeleitet, grob]: 1480 Commits, 1707 Dateien
  - `bot/__init__.py`
  - `bot/admin_dashboard/package-lock.json`
  - `bot/admin_dashboard/package.json`
  - `bot/admin_dashboard/src/App.tsx`
  - `bot/admin_dashboard/src/api/brainLab.ts`
  - `bot/admin_dashboard/src/api/client.ts`
  - `bot/admin_dashboard/src/api/types.ts`
  - `bot/admin_dashboard/src/components/layout/AdminShell.tsx`
  - … 1699 weitere

### internal/deadlock-twitch-bot/uebersicht.html (grob, 1480 Commits seit Pruefung)

Stand der Seite: 2026-07-07
- `Deadlock-Twitch-Bot` (rust, bot) ab `03822a50` [datum-abgeleitet, grob]: 1480 Commits, 1707 Dateien
  - `bot/__init__.py`
  - `bot/admin_dashboard/package-lock.json`
  - `bot/admin_dashboard/package.json`
  - `bot/admin_dashboard/src/App.tsx`
  - `bot/admin_dashboard/src/api/brainLab.ts`
  - `bot/admin_dashboard/src/api/client.ts`
  - `bot/admin_dashboard/src/api/types.ts`
  - `bot/admin_dashboard/src/components/layout/AdminShell.tsx`
  - … 1699 weitere

### internal/deadlock-twitch-bot/architektur.html (grob, 1212 Commits seit Pruefung)

Stand der Seite: 2026-07-18
- `Deadlock-Twitch-Bot` (rust, bot) ab `9e740716` [datum-abgeleitet, grob]: 1212 Commits, 1585 Dateien
  - `bot/__init__.py`
  - `bot/admin_dashboard/package-lock.json`
  - `bot/admin_dashboard/package.json`
  - `bot/admin_dashboard/src/App.tsx`
  - `bot/admin_dashboard/src/api/brainLab.ts`
  - `bot/admin_dashboard/src/api/client.ts`
  - `bot/admin_dashboard/src/api/types.ts`
  - `bot/admin_dashboard/src/components/layout/AdminShell.tsx`
  - … 1577 weitere

### internal/deadlock-twitch-bot/datenmodell.html (grob, 1212 Commits seit Pruefung)

Stand der Seite: 2026-07-18
- `Deadlock-Twitch-Bot` (rust, bot) ab `9e740716` [datum-abgeleitet, grob]: 1212 Commits, 1585 Dateien
  - `bot/__init__.py`
  - `bot/admin_dashboard/package-lock.json`
  - `bot/admin_dashboard/package.json`
  - `bot/admin_dashboard/src/App.tsx`
  - `bot/admin_dashboard/src/api/brainLab.ts`
  - `bot/admin_dashboard/src/api/client.ts`
  - `bot/admin_dashboard/src/api/types.ts`
  - `bot/admin_dashboard/src/components/layout/AdminShell.tsx`
  - … 1577 weitere

### internal/deadlock-twitch-bot/knowledge-faq.html (grob, 1119 Commits seit Pruefung)

Stand der Seite: 2026-07-07
- `Deadlock-Twitch-Bot` (rust, features) ab `03822a50` [datum-abgeleitet, grob]: 1119 Commits, 913 Dateien
  - `rust/.cargo/audit.toml`
  - `rust/.sqlx/query-00748f8a6734810c5b88b17f3db55311a86abaf4e77a2e2cb672e418c2e4d11c.json`
  - `rust/.sqlx/query-04b227969422b64c03140040d7bd1b9daafa6afb1a4551652399895c7e9dbdd4.json`
  - `rust/.sqlx/query-061406bc629371d66a7830dd84ff0960f996fb02d4768b97b29abee449899b19.json`
  - `rust/.sqlx/query-06df9f1066fbe003f82f4eb567df77e08edcf9ae7f31f8db0796613e96d214c4.json`
  - `rust/.sqlx/query-071f5f74ff245c6d767eb4edbfb7b83f07d7c31093e4551dcbaa0234fdddcf29.json`
  - `rust/.sqlx/query-07e85552c7c34d4721a4d35d01091001db448f6cf395c35f64943f75d7a010c8.json`
  - `rust/.sqlx/query-08262ee6cf43e404aad8038fa616d91b8d1fe587cb3d93513037f926689bfb65.json`
  - … 905 weitere

### internal/deadlock-twitch-bot/bot-trennen.html (grob, 1081 Commits seit Pruefung)

Stand der Seite: 2026-08-03
- `Deadlock-Twitch-Bot` (rust, bot) ab `22fd298d` [datum-abgeleitet, grob]: 1081 Commits, 1009 Dateien
  - `bot/admin_dashboard/package-lock.json`
  - `bot/admin_dashboard/package.json`
  - `bot/admin_dashboard/src/App.tsx`
  - `bot/admin_dashboard/src/api/brainLab.ts`
  - `bot/admin_dashboard/src/api/client.ts`
  - `bot/admin_dashboard/src/api/types.ts`
  - `bot/admin_dashboard/src/components/layout/AdminShell.tsx`
  - `bot/admin_dashboard/src/components/layout/Sidebar.tsx`
  - … 1001 weitere

### internal/deadlock-twitch-bot/pause-loop-obs.html (grob, 912 Commits seit Pruefung)

Stand der Seite: 2026-07-20
- `Deadlock-Twitch-Bot` (rust, features) ab `a0a3f8d7` [datum-abgeleitet, grob]: 870 Commits, 820 Dateien
  - `rust/.cargo/audit.toml`
  - `rust/.sqlx/query-00748f8a6734810c5b88b17f3db55311a86abaf4e77a2e2cb672e418c2e4d11c.json`
  - `rust/.sqlx/query-04b227969422b64c03140040d7bd1b9daafa6afb1a4551652399895c7e9dbdd4.json`
  - `rust/.sqlx/query-061406bc629371d66a7830dd84ff0960f996fb02d4768b97b29abee449899b19.json`
  - `rust/.sqlx/query-06df9f1066fbe003f82f4eb567df77e08edcf9ae7f31f8db0796613e96d214c4.json`
  - `rust/.sqlx/query-071f5f74ff245c6d767eb4edbfb7b83f07d7c31093e4551dcbaa0234fdddcf29.json`
  - `rust/.sqlx/query-07e85552c7c34d4721a4d35d01091001db448f6cf395c35f64943f75d7a010c8.json`
  - `rust/.sqlx/query-08262ee6cf43e404aad8038fa616d91b8d1fe587cb3d93513037f926689bfb65.json`
  - … 812 weitere
- `Caddy` (.) ab `ed03744a` [datum-abgeleitet, grob]: 42 Commits, 8 Dateien
  - `CLAUDE.md`
  - `README.md`
  - `conf/Caddyfile`
  - `docker-compose.yml`
  - `hosts/v50671/Caddyfile`
  - `hosts/v50671/systemd/10-logs.conf`
  - `hosts/v50671/systemd/20-tailscale.conf`
  - `hosts/v50671/systemd/99-caddy-nonlocal-bind.sysctl.conf`

### internal/deadlock-twitch-bot/betrieb.html (grob, 851 Commits seit Pruefung)

Stand der Seite: 2026-07-27
- `Deadlock-Twitch-Bot` (ops, rust) ab `3b74c611` [datum-abgeleitet, grob]: 851 Commits, 851 Dateien
  - `ops/highlight-detector/.gitignore`
  - `ops/highlight-detector/config/gewichte.toml`
  - `ops/highlight-detector/config/regionen.toml`
  - `ops/highlight-detector/highlight-detector`
  - `ops/highlight-detector/highlight_detector/__init__.py`
  - `ops/highlight-detector/highlight_detector/__main__.py`
  - `ops/highlight-detector/highlight_detector/audio.py`
  - `ops/highlight-detector/highlight_detector/cache.py`
  - … 843 weitere

### internal/deadlock-twitch-bot/scam-guard.html (grob, 823 Commits seit Pruefung)

Stand der Seite: 2026-07-27
- `Deadlock-Twitch-Bot` (rust, features) ab `3b74c611` [datum-abgeleitet, grob]: 823 Commits, 805 Dateien
  - `rust/.cargo/audit.toml`
  - `rust/.sqlx/query-00748f8a6734810c5b88b17f3db55311a86abaf4e77a2e2cb672e418c2e4d11c.json`
  - `rust/.sqlx/query-04b227969422b64c03140040d7bd1b9daafa6afb1a4551652399895c7e9dbdd4.json`
  - `rust/.sqlx/query-061406bc629371d66a7830dd84ff0960f996fb02d4768b97b29abee449899b19.json`
  - `rust/.sqlx/query-06df9f1066fbe003f82f4eb567df77e08edcf9ae7f31f8db0796613e96d214c4.json`
  - `rust/.sqlx/query-071f5f74ff245c6d767eb4edbfb7b83f07d7c31093e4551dcbaa0234fdddcf29.json`
  - `rust/.sqlx/query-07e85552c7c34d4721a4d35d01091001db448f6cf395c35f64943f75d7a010c8.json`
  - `rust/.sqlx/query-08262ee6cf43e404aad8038fa616d91b8d1fe587cb3d93513037f926689bfb65.json`
  - … 797 weitere

### internal/deadlock-twitch-bot/smalltalk-shadow.html (grob, 823 Commits seit Pruefung)

Stand der Seite: 2026-07-27
- `Deadlock-Twitch-Bot` (rust, features) ab `3b74c611` [datum-abgeleitet, grob]: 823 Commits, 805 Dateien
  - `rust/.cargo/audit.toml`
  - `rust/.sqlx/query-00748f8a6734810c5b88b17f3db55311a86abaf4e77a2e2cb672e418c2e4d11c.json`
  - `rust/.sqlx/query-04b227969422b64c03140040d7bd1b9daafa6afb1a4551652399895c7e9dbdd4.json`
  - `rust/.sqlx/query-061406bc629371d66a7830dd84ff0960f996fb02d4768b97b29abee449899b19.json`
  - `rust/.sqlx/query-06df9f1066fbe003f82f4eb567df77e08edcf9ae7f31f8db0796613e96d214c4.json`
  - `rust/.sqlx/query-071f5f74ff245c6d767eb4edbfb7b83f07d7c31093e4551dcbaa0234fdddcf29.json`
  - `rust/.sqlx/query-07e85552c7c34d4721a4d35d01091001db448f6cf395c35f64943f75d7a010c8.json`
  - `rust/.sqlx/query-08262ee6cf43e404aad8038fa616d91b8d1fe587cb3d93513037f926689bfb65.json`
  - … 797 weitere

### internal/deadlock-twitch-bot/crew-guard-radar.html (grob, 801 Commits seit Pruefung)

Stand der Seite: 2026-07-28
- `Deadlock-Twitch-Bot` (rust, features) ab `1283d481` [datum-abgeleitet, grob]: 801 Commits, 790 Dateien
  - `rust/.cargo/audit.toml`
  - `rust/.sqlx/query-00748f8a6734810c5b88b17f3db55311a86abaf4e77a2e2cb672e418c2e4d11c.json`
  - `rust/.sqlx/query-04b227969422b64c03140040d7bd1b9daafa6afb1a4551652399895c7e9dbdd4.json`
  - `rust/.sqlx/query-061406bc629371d66a7830dd84ff0960f996fb02d4768b97b29abee449899b19.json`
  - `rust/.sqlx/query-06df9f1066fbe003f82f4eb567df77e08edcf9ae7f31f8db0796613e96d214c4.json`
  - `rust/.sqlx/query-071f5f74ff245c6d767eb4edbfb7b83f07d7c31093e4551dcbaa0234fdddcf29.json`
  - `rust/.sqlx/query-07e85552c7c34d4721a4d35d01091001db448f6cf395c35f64943f75d7a010c8.json`
  - `rust/.sqlx/query-08262ee6cf43e404aad8038fa616d91b8d1fe587cb3d93513037f926689bfb65.json`
  - … 782 weitere

### internal/deadlock-twitch-bot/verwaltung-selbstbedienung.html (grob, 762 Commits seit Pruefung)

Stand der Seite: 2026-08-03
- `Deadlock-Twitch-Bot` (rust, features) ab `22fd298d` [datum-abgeleitet, grob]: 762 Commits, 740 Dateien
  - `rust/.cargo/audit.toml`
  - `rust/.sqlx/query-00748f8a6734810c5b88b17f3db55311a86abaf4e77a2e2cb672e418c2e4d11c.json`
  - `rust/.sqlx/query-04b227969422b64c03140040d7bd1b9daafa6afb1a4551652399895c7e9dbdd4.json`
  - `rust/.sqlx/query-061406bc629371d66a7830dd84ff0960f996fb02d4768b97b29abee449899b19.json`
  - `rust/.sqlx/query-071f5f74ff245c6d767eb4edbfb7b83f07d7c31093e4551dcbaa0234fdddcf29.json`
  - `rust/.sqlx/query-07e85552c7c34d4721a4d35d01091001db448f6cf395c35f64943f75d7a010c8.json`
  - `rust/.sqlx/query-08262ee6cf43e404aad8038fa616d91b8d1fe587cb3d93513037f926689bfb65.json`
  - `rust/.sqlx/query-088424abdc92ba8c210b4d20627b639a872f6f1b85a165867890c05face7f40d.json`
  - … 732 weitere

### internal/deadlock-bots/architektur.html (grob, 481 Commits seit Pruefung)

Stand der Seite: 2026-07-07
- `Deadlock-Bots` (rust) ab `9669df25` [datum-abgeleitet, grob]: 481 Commits, 274 Dateien
  - `rust/.sqlx/query-00cbd620a306b6128f21c744d815c1f46d6698fe84aae23739772996b49402fc.json`
  - `rust/.sqlx/query-115f831897ce9f7ec2e81cc7ac7e28021cdcab6aac51fda1e94d733304c8e43e.json`
  - `rust/.sqlx/query-14fdb6d7fa6d976e5890147a53bd1d7b31168661e01dcf2bb79aa6b0b8a4d61e.json`
  - `rust/.sqlx/query-1d13bd25d56c4bed501e77fafb48a37f383b758e6d8fda6d37eb086c026cdef6.json`
  - `rust/.sqlx/query-24dfe426673fcb6c5e23b9c7009cc42241b0627e2afd5ae99362b3fc9fd69c6b.json`
  - `rust/.sqlx/query-2dcc3b77350e59caef3af267e1ea961d664f450b424be977e7b2cbdd6c6027aa.json`
  - `rust/.sqlx/query-2e9682b2bb3267e7980b3b1bfab7697df0dabf5b7510ee803963dcc1344ec22d.json`
  - `rust/.sqlx/query-45623204c0ce3c836ca17e31d5eab228607cd49337cf79700fcae82fec6bab77.json`
  - … 266 weitere

### internal/deadlock-bots/uebersicht.html (grob, 481 Commits seit Pruefung)

Stand der Seite: 2026-07-07
- `Deadlock-Bots` (rust) ab `9669df25` [datum-abgeleitet, grob]: 481 Commits, 274 Dateien
  - `rust/.sqlx/query-00cbd620a306b6128f21c744d815c1f46d6698fe84aae23739772996b49402fc.json`
  - `rust/.sqlx/query-115f831897ce9f7ec2e81cc7ac7e28021cdcab6aac51fda1e94d733304c8e43e.json`
  - `rust/.sqlx/query-14fdb6d7fa6d976e5890147a53bd1d7b31168661e01dcf2bb79aa6b0b8a4d61e.json`
  - `rust/.sqlx/query-1d13bd25d56c4bed501e77fafb48a37f383b758e6d8fda6d37eb086c026cdef6.json`
  - `rust/.sqlx/query-24dfe426673fcb6c5e23b9c7009cc42241b0627e2afd5ae99362b3fc9fd69c6b.json`
  - `rust/.sqlx/query-2dcc3b77350e59caef3af267e1ea961d664f450b424be977e7b2cbdd6c6027aa.json`
  - `rust/.sqlx/query-2e9682b2bb3267e7980b3b1bfab7697df0dabf5b7510ee803963dcc1344ec22d.json`
  - `rust/.sqlx/query-45623204c0ce3c836ca17e31d5eab228607cd49337cf79700fcae82fec6bab77.json`
  - … 266 weitere

### internal/website/uebersicht.html (grob, 176 Commits seit Pruefung)

Stand der Seite: 2026-07-07
- `Website` (builds, dl-coaching, dl-landing) ab `66a9c32b` [datum-abgeleitet, grob]: 176 Commits, 163 Dateien
  - `builds/backend-rust/Cargo.lock`
  - `builds/backend-rust/Cargo.toml`
  - `builds/backend-rust/DEPLOY-NOTES-video-bibliothek.md`
  - `builds/backend-rust/README.md`
  - `builds/backend-rust/migrations/2026071999_video_library.sql`
  - `builds/backend-rust/migrations/2026072000_video_action_audit.sql`
  - `builds/backend-rust/src/app.rs`
  - `builds/backend-rust/src/auth.rs`
  - … 155 weitere

### internal/website/architektur.html (grob, 169 Commits seit Pruefung)

Stand der Seite: 2026-07-10
- `Website` (builds, dl-coaching, dl-landing) ab `f305c821` [datum-abgeleitet, grob]: 169 Commits, 161 Dateien
  - `builds/backend-rust/Cargo.lock`
  - `builds/backend-rust/Cargo.toml`
  - `builds/backend-rust/DEPLOY-NOTES-video-bibliothek.md`
  - `builds/backend-rust/README.md`
  - `builds/backend-rust/migrations/2026071999_video_library.sql`
  - `builds/backend-rust/migrations/2026072000_video_action_audit.sql`
  - `builds/backend-rust/src/app.rs`
  - `builds/backend-rust/src/auth.rs`
  - … 153 weitere

### internal/deadlock-steam-bot/betrieb.html (grob, 156 Commits seit Pruefung)

Stand der Seite: 2026-07-08
- `Deadlock-Steam-Bot` (rust, scripts) ab `d8025714` [datum-abgeleitet, grob]: 156 Commits, 234 Dateien
  - `rust/.sqlx/query-016202238c2fe79d321d1f8c873d75585a5f0a35be607126b724b298e205fa8d.json`
  - `rust/.sqlx/query-0206b6cdb9ad61c91d680e8938b06fd9f504d740e38fcd6e13c71881616f1d9d.json`
  - `rust/.sqlx/query-04fcd77056839e21ca8270bca1c2c29328533082baf6dab083f0aa721df1d381.json`
  - `rust/.sqlx/query-0863636aa6ac78389deb8751d87fd069a1a7d27cd1f250423e735e082bbc2077.json`
  - `rust/.sqlx/query-0a32af394f4f16de182fbb55cd68e99fe6a1a9f44d17f32dc780b91ae37ba78d.json`
  - `rust/.sqlx/query-0d49b183c1421760ae41af8f85fb92e00118fa937162197241bfff1875ed0712.json`
  - `rust/.sqlx/query-1045b3d8cc81ee6518f699e634cd7396ea5b0619312f291bc9a7cc73d70e1a32.json`
  - `rust/.sqlx/query-123972121ed49650b28f6eddc1fe2b09b41e08158ff8dc2e889924b416426667.json`
  - … 226 weitere

### internal/deadlock-steam-bot/architektur.html (grob, 155 Commits seit Pruefung)

Stand der Seite: 2026-07-08
- `Deadlock-Steam-Bot` (rust) ab `d8025714` [datum-abgeleitet, grob]: 155 Commits, 232 Dateien
  - `rust/.sqlx/query-016202238c2fe79d321d1f8c873d75585a5f0a35be607126b724b298e205fa8d.json`
  - `rust/.sqlx/query-0206b6cdb9ad61c91d680e8938b06fd9f504d740e38fcd6e13c71881616f1d9d.json`
  - `rust/.sqlx/query-04fcd77056839e21ca8270bca1c2c29328533082baf6dab083f0aa721df1d381.json`
  - `rust/.sqlx/query-0863636aa6ac78389deb8751d87fd069a1a7d27cd1f250423e735e082bbc2077.json`
  - `rust/.sqlx/query-0a32af394f4f16de182fbb55cd68e99fe6a1a9f44d17f32dc780b91ae37ba78d.json`
  - `rust/.sqlx/query-0d49b183c1421760ae41af8f85fb92e00118fa937162197241bfff1875ed0712.json`
  - `rust/.sqlx/query-1045b3d8cc81ee6518f699e634cd7396ea5b0619312f291bc9a7cc73d70e1a32.json`
  - `rust/.sqlx/query-123972121ed49650b28f6eddc1fe2b09b41e08158ff8dc2e889924b416426667.json`
  - … 224 weitere

### internal/deadlock-steam-bot/datenmodell.html (grob, 155 Commits seit Pruefung)

Stand der Seite: 2026-07-08
- `Deadlock-Steam-Bot` (rust) ab `d8025714` [datum-abgeleitet, grob]: 155 Commits, 232 Dateien
  - `rust/.sqlx/query-016202238c2fe79d321d1f8c873d75585a5f0a35be607126b724b298e205fa8d.json`
  - `rust/.sqlx/query-0206b6cdb9ad61c91d680e8938b06fd9f504d740e38fcd6e13c71881616f1d9d.json`
  - `rust/.sqlx/query-04fcd77056839e21ca8270bca1c2c29328533082baf6dab083f0aa721df1d381.json`
  - `rust/.sqlx/query-0863636aa6ac78389deb8751d87fd069a1a7d27cd1f250423e735e082bbc2077.json`
  - `rust/.sqlx/query-0a32af394f4f16de182fbb55cd68e99fe6a1a9f44d17f32dc780b91ae37ba78d.json`
  - `rust/.sqlx/query-0d49b183c1421760ae41af8f85fb92e00118fa937162197241bfff1875ed0712.json`
  - `rust/.sqlx/query-1045b3d8cc81ee6518f699e634cd7396ea5b0619312f291bc9a7cc73d70e1a32.json`
  - `rust/.sqlx/query-123972121ed49650b28f6eddc1fe2b09b41e08158ff8dc2e889924b416426667.json`
  - … 224 weitere

### internal/deadlock-steam-bot/integrationen.html (grob, 155 Commits seit Pruefung)

Stand der Seite: 2026-07-08
- `Deadlock-Steam-Bot` (rust) ab `d8025714` [datum-abgeleitet, grob]: 155 Commits, 232 Dateien
  - `rust/.sqlx/query-016202238c2fe79d321d1f8c873d75585a5f0a35be607126b724b298e205fa8d.json`
  - `rust/.sqlx/query-0206b6cdb9ad61c91d680e8938b06fd9f504d740e38fcd6e13c71881616f1d9d.json`
  - `rust/.sqlx/query-04fcd77056839e21ca8270bca1c2c29328533082baf6dab083f0aa721df1d381.json`
  - `rust/.sqlx/query-0863636aa6ac78389deb8751d87fd069a1a7d27cd1f250423e735e082bbc2077.json`
  - `rust/.sqlx/query-0a32af394f4f16de182fbb55cd68e99fe6a1a9f44d17f32dc780b91ae37ba78d.json`
  - `rust/.sqlx/query-0d49b183c1421760ae41af8f85fb92e00118fa937162197241bfff1875ed0712.json`
  - `rust/.sqlx/query-1045b3d8cc81ee6518f699e634cd7396ea5b0619312f291bc9a7cc73d70e1a32.json`
  - `rust/.sqlx/query-123972121ed49650b28f6eddc1fe2b09b41e08158ff8dc2e889924b416426667.json`
  - … 224 weitere

### internal/deadlock-steam-bot/task-queue.html (grob, 155 Commits seit Pruefung)

Stand der Seite: 2026-07-08
- `Deadlock-Steam-Bot` (rust) ab `d8025714` [datum-abgeleitet, grob]: 155 Commits, 232 Dateien
  - `rust/.sqlx/query-016202238c2fe79d321d1f8c873d75585a5f0a35be607126b724b298e205fa8d.json`
  - `rust/.sqlx/query-0206b6cdb9ad61c91d680e8938b06fd9f504d740e38fcd6e13c71881616f1d9d.json`
  - `rust/.sqlx/query-04fcd77056839e21ca8270bca1c2c29328533082baf6dab083f0aa721df1d381.json`
  - `rust/.sqlx/query-0863636aa6ac78389deb8751d87fd069a1a7d27cd1f250423e735e082bbc2077.json`
  - `rust/.sqlx/query-0a32af394f4f16de182fbb55cd68e99fe6a1a9f44d17f32dc780b91ae37ba78d.json`
  - `rust/.sqlx/query-0d49b183c1421760ae41af8f85fb92e00118fa937162197241bfff1875ed0712.json`
  - `rust/.sqlx/query-1045b3d8cc81ee6518f699e634cd7396ea5b0619312f291bc9a7cc73d70e1a32.json`
  - `rust/.sqlx/query-123972121ed49650b28f6eddc1fe2b09b41e08158ff8dc2e889924b416426667.json`
  - … 224 weitere

### internal/deadlock-steam-bot/uebersicht.html (grob, 155 Commits seit Pruefung)

Stand der Seite: 2026-07-08
- `Deadlock-Steam-Bot` (rust) ab `d8025714` [datum-abgeleitet, grob]: 155 Commits, 232 Dateien
  - `rust/.sqlx/query-016202238c2fe79d321d1f8c873d75585a5f0a35be607126b724b298e205fa8d.json`
  - `rust/.sqlx/query-0206b6cdb9ad61c91d680e8938b06fd9f504d740e38fcd6e13c71881616f1d9d.json`
  - `rust/.sqlx/query-04fcd77056839e21ca8270bca1c2c29328533082baf6dab083f0aa721df1d381.json`
  - `rust/.sqlx/query-0863636aa6ac78389deb8751d87fd069a1a7d27cd1f250423e735e082bbc2077.json`
  - `rust/.sqlx/query-0a32af394f4f16de182fbb55cd68e99fe6a1a9f44d17f32dc780b91ae37ba78d.json`
  - `rust/.sqlx/query-0d49b183c1421760ae41af8f85fb92e00118fa937162197241bfff1875ed0712.json`
  - `rust/.sqlx/query-1045b3d8cc81ee6518f699e634cd7396ea5b0619312f291bc9a7cc73d70e1a32.json`
  - `rust/.sqlx/query-123972121ed49650b28f6eddc1fe2b09b41e08158ff8dc2e889924b416426667.json`
  - … 224 weitere

### internal/deadlock-turniere/uebersicht.html (grob, 132 Commits seit Pruefung)

Stand der Seite: 2026-07-07
- `Deadlock-Turniere` (rust, backend, frontend) ab `c6a5d2c9` [datum-abgeleitet, grob]: 132 Commits, 189 Dateien
  - `backend/__init__.py`
  - `backend/admin/__init__.py`
  - `backend/admin/test_mode.py`
  - `backend/auth/__init__.py`
  - `backend/auth/discord_oauth.py`
  - `backend/auth/middleware.py`
  - `backend/auth/permissions.py`
  - `backend/config.py`
  - … 181 weitere

### internal/website/betrieb.html (grob, 125 Commits seit Pruefung)

Stand der Seite: 2026-07-10
- `Website` (builds, scripts) ab `f305c821` [datum-abgeleitet, grob]: 125 Commits, 109 Dateien
  - `builds/backend-rust/Cargo.lock`
  - `builds/backend-rust/Cargo.toml`
  - `builds/backend-rust/DEPLOY-NOTES-video-bibliothek.md`
  - `builds/backend-rust/README.md`
  - `builds/backend-rust/migrations/2026071999_video_library.sql`
  - `builds/backend-rust/migrations/2026072000_video_action_audit.sql`
  - `builds/backend-rust/src/app.rs`
  - `builds/backend-rust/src/auth.rs`
  - … 101 weitere

### internal/deadlock-turniere/betrieb.html (grob, 123 Commits seit Pruefung)

Stand der Seite: 2026-07-12
- `Deadlock-Turniere` (rust, ops, scripts) ab `208c28bf` [datum-abgeleitet, grob]: 123 Commits, 88 Dateien
  - `ops/systemd/deadlock-turniere.service.example`
  - `rust/Cargo.lock`
  - `rust/Cargo.toml`
  - `rust/crates/turnier-api/Cargo.toml`
  - `rust/crates/turnier-api/src/admin/automatik.rs`
  - `rust/crates/turnier-api/src/app.rs`
  - `rust/crates/turnier-api/src/comp.rs`
  - `rust/crates/turnier-api/src/consent.rs`
  - … 80 weitere

### internal/deadlock-turniere/architektur.html (grob, 120 Commits seit Pruefung)

Stand der Seite: 2026-07-07
- `Deadlock-Turniere` (rust, backend) ab `c6a5d2c9` [datum-abgeleitet, grob]: 120 Commits, 142 Dateien
  - `backend/__init__.py`
  - `backend/admin/__init__.py`
  - `backend/admin/test_mode.py`
  - `backend/auth/__init__.py`
  - `backend/auth/discord_oauth.py`
  - `backend/auth/middleware.py`
  - `backend/auth/permissions.py`
  - `backend/config.py`
  - … 134 weitere

### internal/deadlock-turniere/datenmodell.html (grob, 120 Commits seit Pruefung)

Stand der Seite: 2026-07-10
- `Deadlock-Turniere` (rust, backend) ab `c6a5d2c9` [datum-abgeleitet, grob]: 120 Commits, 142 Dateien
  - `backend/__init__.py`
  - `backend/admin/__init__.py`
  - `backend/admin/test_mode.py`
  - `backend/auth/__init__.py`
  - `backend/auth/discord_oauth.py`
  - `backend/auth/middleware.py`
  - `backend/auth/permissions.py`
  - `backend/config.py`
  - … 134 weitere

### internal/deadlock-turniere/integrationen.html (grob, 120 Commits seit Pruefung)

Stand der Seite: 2026-07-07
- `Deadlock-Turniere` (rust, backend) ab `c6a5d2c9` [datum-abgeleitet, grob]: 120 Commits, 142 Dateien
  - `backend/__init__.py`
  - `backend/admin/__init__.py`
  - `backend/admin/test_mode.py`
  - `backend/auth/__init__.py`
  - `backend/auth/discord_oauth.py`
  - `backend/auth/middleware.py`
  - `backend/auth/permissions.py`
  - `backend/config.py`
  - … 134 weitere

### internal/deadlock-turniere/match-automatik.html (grob, 120 Commits seit Pruefung)

Stand der Seite: 2026-07-07
- `Deadlock-Turniere` (rust, backend) ab `c6a5d2c9` [datum-abgeleitet, grob]: 120 Commits, 142 Dateien
  - `backend/__init__.py`
  - `backend/admin/__init__.py`
  - `backend/admin/test_mode.py`
  - `backend/auth/__init__.py`
  - `backend/auth/discord_oauth.py`
  - `backend/auth/middleware.py`
  - `backend/auth/permissions.py`
  - `backend/config.py`
  - … 134 weitere

### internal/deadlock-brain/match-demo-learning.html (grob, 110 Commits seit Pruefung)

Stand der Seite: 2026-07-10
- `Deadlock-Brain` (rust, src) ab `10edcd42` [datum-abgeleitet, grob]: 110 Commits, 76 Dateien
  - `rust/Cargo.lock`
  - `rust/Cargo.toml`
  - `rust/crates/dbrain-builds/src/lib.rs`
  - `rust/crates/dbrain-builds/src/patch_tag.rs`
  - `rust/crates/dbrain-builds/src/spec.rs`
  - `rust/crates/dbrain-builds/src/sync.rs`
  - `rust/crates/dbrain-enrich/src/lib.rs`
  - `rust/crates/dbrain-learn/src/build_learning.rs`
  - … 68 weitere

### internal/deadlock-turniere/draft-lobbys.html (grob, 92 Commits seit Pruefung)

Stand der Seite: 2026-07-16
- `Deadlock-Turniere` (rust, backend, frontend) ab `16490dcf` [datum-abgeleitet, grob]: 92 Commits, 161 Dateien
  - `backend/__init__.py`
  - `backend/admin/__init__.py`
  - `backend/admin/test_mode.py`
  - `backend/auth/__init__.py`
  - `backend/auth/discord_oauth.py`
  - `backend/auth/middleware.py`
  - `backend/auth/permissions.py`
  - `backend/config.py`
  - … 153 weitere

### internal/website/datenmodell.html (grob, 82 Commits seit Pruefung)

Stand der Seite: 2026-07-07
- `Website` (builds) ab `66a9c32b` [datum-abgeleitet, grob]: 82 Commits, 96 Dateien
  - `builds/backend-rust/Cargo.lock`
  - `builds/backend-rust/Cargo.toml`
  - `builds/backend-rust/DEPLOY-NOTES-video-bibliothek.md`
  - `builds/backend-rust/README.md`
  - `builds/backend-rust/migrations/2026071999_video_library.sql`
  - `builds/backend-rust/migrations/2026072000_video_action_audit.sql`
  - `builds/backend-rust/src/app.rs`
  - `builds/backend-rust/src/auth.rs`
  - … 88 weitere

### internal/website/integrationen.html (grob, 82 Commits seit Pruefung)

Stand der Seite: 2026-07-07
- `Website` (builds) ab `66a9c32b` [datum-abgeleitet, grob]: 82 Commits, 96 Dateien
  - `builds/backend-rust/Cargo.lock`
  - `builds/backend-rust/Cargo.toml`
  - `builds/backend-rust/DEPLOY-NOTES-video-bibliothek.md`
  - `builds/backend-rust/README.md`
  - `builds/backend-rust/migrations/2026071999_video_library.sql`
  - `builds/backend-rust/migrations/2026072000_video_action_audit.sql`
  - `builds/backend-rust/src/app.rs`
  - `builds/backend-rust/src/auth.rs`
  - … 88 weitere

### internal/betrieb/routing-caddy.html (grob, 53 Commits seit Pruefung)

Stand der Seite: 2026-07-07
- `Caddy` (.) ab `89c1f8ab` [datum-abgeleitet, grob]: 53 Commits, 8 Dateien
  - `CLAUDE.md`
  - `README.md`
  - `conf/Caddyfile`
  - `docker-compose.yml`
  - `hosts/v50671/Caddyfile`
  - `hosts/v50671/systemd/10-logs.conf`
  - `hosts/v50671/systemd/20-tailscale.conf`
  - `hosts/v50671/systemd/99-caddy-nonlocal-bind.sysctl.conf`

### internal/patchnotes-bot/architektur.html (grob, 39 Commits seit Pruefung)

Stand der Seite: 2026-07-07
- `Deadlock--Patchnotes-Bot` (.) ab `e1c71cba` [datum-abgeleitet, grob]: 39 Commits, 16 Dateien
  - `.github/workflows/codeql.yml`
  - `.github/workflows/secret-scanning.yml`
  - `.github/workflows/security.yml`
  - `changelog_latest_fetcher.py`
  - `entity_emojis.py`
  - `main.py`
  - `patch_view.py`
  - `requirements.txt`
  - … 8 weitere

### internal/patchnotes-bot/betrieb.html (grob, 39 Commits seit Pruefung)

Stand der Seite: 2026-07-07
- `Deadlock--Patchnotes-Bot` (.) ab `e1c71cba` [datum-abgeleitet, grob]: 39 Commits, 16 Dateien
  - `.github/workflows/codeql.yml`
  - `.github/workflows/secret-scanning.yml`
  - `.github/workflows/security.yml`
  - `changelog_latest_fetcher.py`
  - `entity_emojis.py`
  - `main.py`
  - `patch_view.py`
  - `requirements.txt`
  - … 8 weitere

### internal/patchnotes-bot/integrationen.html (grob, 39 Commits seit Pruefung)

Stand der Seite: 2026-07-07
- `Deadlock--Patchnotes-Bot` (.) ab `e1c71cba` [datum-abgeleitet, grob]: 39 Commits, 16 Dateien
  - `.github/workflows/codeql.yml`
  - `.github/workflows/secret-scanning.yml`
  - `.github/workflows/security.yml`
  - `changelog_latest_fetcher.py`
  - `entity_emojis.py`
  - `main.py`
  - `patch_view.py`
  - `requirements.txt`
  - … 8 weitere

### internal/patchnotes-bot/uebersicht.html (grob, 39 Commits seit Pruefung)

Stand der Seite: 2026-07-07
- `Deadlock--Patchnotes-Bot` (.) ab `e1c71cba` [datum-abgeleitet, grob]: 39 Commits, 16 Dateien
  - `.github/workflows/codeql.yml`
  - `.github/workflows/secret-scanning.yml`
  - `.github/workflows/security.yml`
  - `changelog_latest_fetcher.py`
  - `entity_emojis.py`
  - `main.py`
  - `patch_view.py`
  - `requirements.txt`
  - … 8 weitere

### internal/betrieb/deploy.html (grob, 19 Commits seit Pruefung)

Stand der Seite: 2026-07-07
- `Deadlock-Bots` (scripts) ab `9669df25` [datum-abgeleitet, grob]: 19 Commits, 10 Dateien
  - `scripts/check-local.sh`
  - `scripts/export_infisical_env.py`
  - `scripts/kill_stale_bot.sh`
  - `scripts/maintenance/repair_discord_system_messages_20260908.sql`
  - `scripts/run_brain_feeder.sh`
  - `scripts/run_dl_insights_sync.sh`
  - `scripts/run_dl_knowledge_service.sh`
  - `scripts/run_verbinder.sh`
  - … 2 weitere

### internal/betrieb/secrets-infisical.html (grob, 14 Commits seit Pruefung)

Stand der Seite: 2026-07-12
- `Deadlock-Bots` (scripts) ab `3bc8ca8a` [explizit, grob]: 14 Commits, 10 Dateien
  - `scripts/check-local.sh`
  - `scripts/export_infisical_env.py`
  - `scripts/kill_stale_bot.sh`
  - `scripts/maintenance/repair_discord_system_messages_20260908.sql`
  - `scripts/run_brain_feeder.sh`
  - `scripts/run_dl_insights_sync.sh`
  - `scripts/run_dl_knowledge_service.sh`
  - `scripts/run_verbinder.sh`
  - … 2 weitere

### internal/deadlock-bots/betrieb.html (grob, 14 Commits seit Pruefung)

Stand der Seite: 2026-07-12
- `Deadlock-Bots` (scripts) ab `3bc8ca8a` [explizit, grob]: 14 Commits, 10 Dateien
  - `scripts/check-local.sh`
  - `scripts/export_infisical_env.py`
  - `scripts/kill_stale_bot.sh`
  - `scripts/maintenance/repair_discord_system_messages_20260908.sql`
  - `scripts/run_brain_feeder.sh`
  - `scripts/run_dl_insights_sync.sh`
  - `scripts/run_dl_knowledge_service.sh`
  - `scripts/run_verbinder.sh`
  - … 2 weitere
- `Deadlock-Docs` (tools/deploy_corpus.sh) ab `08c01ff0` [datum-abgeleitet, genau]: 0 Commits, 0 Dateien

### internal/website/scrim-cockpit-handbuch.html (grob, 13 Commits seit Pruefung)

Stand der Seite: 2026-07-16
- `Website` (dl-coaching, builds/backend-rust/src/routes/scrim.rs) ab `5b9bfa3b` [datum-abgeleitet, grob]: 13 Commits, 11 Dateien
  - `builds/backend-rust/src/routes/scrim.rs`
  - `dl-coaching/index.html`
  - `dl-coaching/package-lock.json`
  - `dl-coaching/package.json`
  - `dl-coaching/src/App.tsx`
  - `dl-coaching/src/api/client.ts`
  - `dl-coaching/src/components/Layout.tsx`
  - `dl-coaching/src/lib/commandCenter.test.ts`
  - … 3 weitere

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
