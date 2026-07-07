---
title: "Deadlock-Bots Datenmodell"
tags: [deadlock-bots, intern, postgres, datenmodell]
stand: 2026-07-07
quelle: Deadlock-Bots
---
# Datenmodell

Die zentrale Datenbank ist Postgres. Alle Rust-Binaries, die zentrale Daten brauchen, lesen genau `DEADLOCK_CENTRAL_DSN` über `dl_central_db::dsn_from_env`; es gibt keinen Fallback auf `DATABASE_URL` (`rust/crates/dl-central-db/src/pool.rs`, `rust/bin/dl-central-migrate/src/main.rs`, `rust/bin/dl-web/src/main.rs`).

## Schemata

| Schema | Inhalt | Beleg |
|---|---|---|
| `core` | Nutzer, Steam-Links, Privacy, Tags und Discord-Role-Connection-Tokens. | `rust/crates/dl-central-db/migrations/0001_core_and_schemas.sql`, `rust/crates/dl-central-db/migrations/0002_sp1_schemas_and_core.sql`, `rust/crates/dl-central-db/migrations/2026070330_discord_role_connections.sql` |
| `steam` | Beta-Invite-Flows, Friend-Requests, Steam-Links, Rank-History, Rich-Presence und Steam-Tasks. | `rust/crates/dl-central-db/migrations/0003_steam.sql`, `rust/crates/dl-central-db/migrations/2026070311_steam_rank_history_account_scope.sql` |
| `coaching` | Coaching-Anfragen, Coaches, Sessions, Surveys, Reviews, Termine und Ziele. | `rust/crates/dl-central-db/migrations/0004_coaching_scrim.sql` |
| `scrim` | Scrim-Teilnehmer, Teams, Team-Members und Matches. | `rust/crates/dl-central-db/migrations/0004_coaching_scrim.sql`, `rust/crates/dl-central-db/migrations/2026070230_scrim_management.sql`, `rust/crates/dl-central-db/migrations/2026070620_scrim_match_orchestrator.sql` |
| `voice` | Voice-Stats, TempVoice, Router-Prefs, Rank-Anker, Rename-Queue und LFG-Posts. | `rust/crates/dl-central-db/migrations/0005_voice.sql`, `rust/crates/dl-central-db/migrations/2026070320_lfg_posts.sql`, `rust/crates/dl-central-db/migrations/2026070335_lfg_post_ids.sql` |
| `tierlist` | Heroes, Builds, Snapshots, Votes, Streamer und Meta-Importe. | `rust/crates/dl-central-db/migrations/0006_tierlist.sql` |
| `bot` | FAQ-Sessions, KV-Store, Reaction-Roles, OAuth-States, Notifications, Invite-Caches und Twitch-Streamer-Invites. | `rust/crates/dl-central-db/migrations/0007_bot.sql` |
| `clips` | Clip-Einsendungen, Fenster, Contests, Fetch-Historie und Templates. | `rust/crates/dl-central-db/migrations/0008_clips.sql` |
| `turnier` | Turnierdaten, Teams, Matches, Sessions, Reminders, Profile und Audit-Log. | `rust/crates/dl-central-db/migrations/0009_turnier.sql` |
| `activity` | Member-Events, Message-/Voice-Aktivität, Journey, Presence, Interactions, Insights und Directory. | `rust/crates/dl-central-db/migrations/0010_activity_moderation_content_patchnotes.sql`, `rust/crates/dl-central-db/migrations/2026070220_journey_ingestion_analytics.sql`, `rust/crates/dl-central-db/migrations/2026070610_server_insights_backend.sql` |
| `moderation` | AI-Moderation-Cases, Ragebait-Hits und Security-Guard-Incidents. | `rust/crates/dl-central-db/migrations/0010_activity_moderation_content_patchnotes.sql`, `rust/crates/dl-central-db/migrations/2026070250_moderation_unified_behavior_cases.sql` |
| `content` | Meta-Announcements und Meta-Reports. | `rust/crates/dl-central-db/migrations/0010_activity_moderation_content_patchnotes.sql` |
| `patchnotes` | Changelog-Posts, Deadlock-Changelogs und Meta-Patchnotes. | `rust/crates/dl-central-db/migrations/0010_activity_moderation_content_patchnotes.sql`, `rust/crates/dl-central-db/migrations/0014_patchnotes_identity_sequences.sql` |
| `brain` | Source-Runs, Dokumente, Entities, Patch-Events, Forum-Claims, Knowledge-Events und Insights. | `rust/crates/dl-central-db/migrations/0012_brain_knowledge_timeline.sql`, `rust/crates/dl-central-db/migrations/0013_brain_insight_records.sql` |
| `server_config` | Server-as-Code-Sollzustand, Live-Snapshots, Diffs, Apply-Runs, Drift, Adoption und Rollback-Exports. | `rust/crates/dl-central-db/migrations/2026070210_server_config_schema.sql`, `rust/crates/dl-central-db/migrations/2026070240_server_sync_rollback_exports.sql` |

## Invarianten

`core.steam_links` hat den Primärschlüssel `(discord_id, steam_id)`, einen eindeutigen Owner pro `steam_id64` und seit Migration `0015` höchstens einen primären Steam-Link pro Discord-User. Privacy-Deletes greifen zusätzlich Steam-Seitentabellen ab (`rust/crates/dl-central-db/migrations/0002_sp1_schemas_and_core.sql`, `rust/crates/dl-central-db/migrations/0015_steam_links_one_primary.sql`, `rust/crates/dl-community/src/privacy.rs`).

`core.user_privacy.user_id` ist Primärschlüssel. Journey-Metadaten prüfen vor Inserts auf `opted_out`, und der Privacy-Erasure-Pfad löscht oder anonymisiert Aktivitäts-, Voice-, Coaching-, KV- und Steam-Daten (`rust/crates/dl-central-db/migrations/0002_sp1_schemas_and_core.sql`, `rust/crates/dl-activity/src/journey.rs`, `rust/crates/dl-community/src/privacy.rs`).

FAQ-Daten hängen an `bot.faq_chat_sessions.session_id`. `bot.faq_chat_messages.session_id` referenziert die Session mit `ON DELETE CASCADE`; der Code liest nur die letzten 10 Nachrichten als Gesprächskontext (`rust/crates/dl-central-db/migrations/0007_bot.sql`, `rust/crates/dl-community/src/faq.rs`).

Voice-State nutzt zusammengesetzte Schlüssel für konfliktarme Zustände: `voice.deadlock_party_members` nutzt `(party_id, steam_id)`, `voice.deadlock_subrank_roles` nutzt `(guild_id, rank_value, subrank)`, und `voice.tempvoice_interface` schützt `(guild_id, message_id)` plus eindeutige `lane_id` (`rust/crates/dl-central-db/migrations/0005_voice.sql`, `rust/crates/dl-voice/src/lib.rs`).

`tierlist.deadlock_heroes` ist eindeutig nach `hero_id` und `name`, `tierlist.deadlock_hero_builds` nach `(hero_id, build_id)`, und `tierlist.tierlist_snapshots` nach `(bucket, fetched_at)`. Votes hängen am `build_id` als Primärschlüssel (`rust/crates/dl-central-db/migrations/0006_tierlist.sql`, `rust/crates/dl-tierlist/src/lib.rs`).

Moderations-Cases werden nur weiterverarbeitet, wenn der Insert in `moderation.ai_moderation_cases` gelingt. Auto-Aktionen aktualisieren danach `action`; Review-Buttons schreiben Moderator, Zeitpunkt und Ergebnis zurück (`rust/crates/dl-moderation/src/store.rs`, `rust/crates/dl-moderation/src/moderation_system.rs`).

Journey-Rohdaten halten Nutzerbezug maximal 180 Tage und werden danach in Tagesaggregate verdichtet. Message-Inhalte werden im Journey-Pfad nicht persistiert; gespeichert werden Metadaten wie wer, wo, wann, Länge, Anhang und Reply (`rust/crates/dl-activity/src/journey.rs`).

Server-Insights trennen Live-Daten und Importdaten. `activity.insights_imports` ist eindeutig nach `(guild_id, import_kind, period_start, dimension)`, während `activity.presence_daily_seen` nach `(guild_id, user_id, day)` dedupliziert (`rust/crates/dl-central-db/migrations/2026070610_server_insights_backend.sql`, `rust/crates/dl-dashboard/src/insights.rs`).

Server-as-Code trennt gewünschte Objekte und Live-Snapshots. Snapshot-Kindtabellen referenzieren `server_config.live_snapshots` mit `ON DELETE CASCADE`, und `apply_runs.status` ist auf `planned`, `running`, `applied`, `dry_run`, `failed` oder `hash_mismatch` begrenzt (`rust/crates/dl-central-db/migrations/2026070210_server_config_schema.sql`, `rust/crates/dl-server-as-code/src/lib.rs`).
