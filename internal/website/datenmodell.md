---
title: "Website Datenmodell"
tags: [website, intern, datenmodell]
stand: 2026-07-07
quelle: "Website"
---
# Datenmodell

Das Rust-Backend liest die Datenbank-URL über `dl_central_db::dsn_from_env()` und verlangt `DEADLOCK_CENTRAL_DSN`; `db::init` führt im Website-Repo nur `SELECT 1` aus und legt keine Tabellen an (`/home/naniadm/Documents/Website/builds/backend-rust/src/db.rs`).

Die Tabellenquelle liegt im per Cargo eingebundenen lokalen Crate `../../../Deadlock-Bots/rust/crates/dl-central-db`; die Website-Cargo-Datei referenziert diesen Pfad direkt (`/home/naniadm/Documents/Website/builds/backend-rust/Cargo.toml`, `/home/naniadm/Documents/Deadlock-Bots/rust/crates/dl-central-db/migrations`).

## Core und Auth

| Tabelle | Nutzung im Website-Code | Beleg |
|---|---|---|
| `core.meta_users` | Auth legt Nutzer nach Discord-Login an oder aktualisiert sie; Admin-Routen lesen Nutzer und ändern Rollen. | `/home/naniadm/Documents/Website/builds/backend-rust/src/auth.rs`, `/home/naniadm/Documents/Website/builds/backend-rust/src/routes/meta.rs`, `/home/naniadm/Documents/Deadlock-Bots/rust/crates/dl-central-db/migrations/0002_sp1_schemas_and_core.sql` |
| `core.discord_role_connection_tokens` | Linked-Role-OAuth speichert verschlüsselte Discord-Tokens pro Discord-ID. | `/home/naniadm/Documents/Website/builds/backend-rust/src/routes/linked_role.rs`, `/home/naniadm/Documents/Deadlock-Bots/rust/crates/dl-central-db/migrations/2026070330_discord_role_connections.sql` |
| `core.discord_role_connection_sync_state` | Der interne Sync-Endpunkt und der Worker arbeiten mit Pending-State für Role-Connection-Sync. | `/home/naniadm/Documents/Website/builds/backend-rust/src/routes/linked_role.rs`, `/home/naniadm/Documents/Deadlock-Bots/rust/crates/dl-central-db/migrations/2026070330_discord_role_connections.sql` |

## Coaching

| Tabelle | Nutzung im Website-Code | Beleg |
|---|---|---|
| `coaching.requests` | Öffentliche Anfragen, Bot-Spiegelung, Queue und Discord-Benachrichtigung nutzen dieselbe Request-Tabelle. | `/home/naniadm/Documents/Website/builds/backend-rust/src/routes/coaching.rs`, `/home/naniadm/Documents/Website/builds/backend-rust/src/routes/platform.rs`, `/home/naniadm/Documents/Deadlock-Bots/rust/crates/dl-central-db/migrations/0004_coaching_scrim.sql` |
| `coaching.coaches` | Coach-Liste, Profile, Dashboard, Coach-Sync und Berechtigungsprüfung lesen oder schreiben Coaches. | `/home/naniadm/Documents/Website/builds/backend-rust/src/routes/coaching.rs`, `/home/naniadm/Documents/Website/builds/backend-rust/src/routes/platform.rs`, `/home/naniadm/Documents/Website/builds/backend-rust/src/routes/scrim.rs` |
| `coaching.coach_applications` | Bewerbungen werden erstellt und per Admin-Review auf Status gesetzt. | `/home/naniadm/Documents/Website/builds/backend-rust/src/routes/coaching.rs`, `/home/naniadm/Documents/Deadlock-Bots/rust/crates/dl-central-db/migrations/0004_coaching_scrim.sql` |
| `coaching.sessions` | Matching, Session-Ende, Bot-Sync, Dashboard und Spieleransicht lesen oder schreiben Sessions. | `/home/naniadm/Documents/Website/builds/backend-rust/src/routes/coaching.rs`, `/home/naniadm/Documents/Website/builds/backend-rust/src/routes/platform.rs` |
| `coaching.surveys` und `coaching.coach_reviews` | Survey-Abschluss schreibt Feedback, aktualisiert Coach-Rating und erzeugt Reviews. | `/home/naniadm/Documents/Website/builds/backend-rust/src/routes/coaching.rs`, `/home/naniadm/Documents/Deadlock-Bots/rust/crates/dl-central-db/migrations/0004_coaching_scrim.sql` |
| `coaching.coachees` | Plattform-Views, Bot-Sync, Termine, Ziele und Spieleransicht hängen am Coachee-Datensatz. | `/home/naniadm/Documents/Website/builds/backend-rust/src/routes/platform.rs`, `/home/naniadm/Documents/Deadlock-Bots/rust/crates/dl-central-db/migrations/0004_coaching_scrim.sql` |
| `coaching.appointments` | Terminliste, Terminänderung, Reminder und Ack schreiben Status- und Notify-Spalten. | `/home/naniadm/Documents/Website/builds/backend-rust/src/routes/platform.rs`, `/home/naniadm/Documents/Deadlock-Bots/rust/crates/dl-central-db/migrations/0004_coaching_scrim.sql` |
| `coaching.goals`, `coaching.milestones`, `coaching.session_notes` | Coach- und Spieleransicht speichern Ziele, Meilensteine und Notizen pro Coachee. | `/home/naniadm/Documents/Website/builds/backend-rust/src/routes/platform.rs`, `/home/naniadm/Documents/Website/dl-coaching/src/api/client.ts` |

## Scrims

| Tabelle | Nutzung im Website-Code | Beleg |
|---|---|---|
| `scrim.participants` | Signup, eigene Verfügbarkeit, Pool, Statuswechsel, Coach-Notizen und Discord-Rollensync hängen am Participant. | `/home/naniadm/Documents/Website/builds/backend-rust/src/routes/scrim.rs`, `/home/naniadm/Documents/Deadlock-Bots/rust/crates/dl-central-db/migrations/0004_coaching_scrim.sql`, `/home/naniadm/Documents/Deadlock-Bots/rust/crates/dl-central-db/migrations/2026070230_scrim_management.sql` |
| `scrim.teams` | Coach-Teams werden gelistet, erstellt und im Board gelesen. | `/home/naniadm/Documents/Website/builds/backend-rust/src/routes/scrim.rs`, `/home/naniadm/Documents/Deadlock-Bots/rust/crates/dl-central-db/migrations/0004_coaching_scrim.sql` |
| `scrim.team_members` | Teamzuweisung, Captain-/Bench-Status und Board-Mitglieder laufen über diese Join-Tabelle. | `/home/naniadm/Documents/Website/builds/backend-rust/src/routes/scrim.rs`, `/home/naniadm/Documents/Deadlock-Bots/rust/crates/dl-central-db/migrations/0004_coaching_scrim.sql` |
| `scrim.matches` | Spieleransicht liest das nächste Match; spätere Orchestrator-Felder liegen als additive Spalten auf derselben Tabelle. | `/home/naniadm/Documents/Website/builds/backend-rust/src/routes/scrim.rs`, `/home/naniadm/Documents/Deadlock-Bots/rust/crates/dl-central-db/migrations/2026070620_scrim_match_orchestrator.sql` |

## Meta, Builds und Patchnotes

| Tabelle | Nutzung im Website-Code | Beleg |
|---|---|---|
| `tierlist.meta_heroes` | Hero-Liste und Hero-Admin schreiben Name, Tier, Rolle, Bild, Abilities und Stats. | `/home/naniadm/Documents/Website/builds/backend-rust/src/routes/meta.rs`, `/home/naniadm/Documents/Deadlock-Bots/rust/crates/dl-central-db/migrations/0006_tierlist.sql` |
| `tierlist.meta_builds` | Builds werden gelistet, erstellt, geändert, gelöscht, bewertet und gemeldet. | `/home/naniadm/Documents/Website/builds/backend-rust/src/routes/meta.rs`, `/home/naniadm/Documents/Deadlock-Bots/rust/crates/dl-central-db/migrations/0006_tierlist.sql` |
| `tierlist.meta_items` | Item-Routen lesen Items nach Name oder ID. | `/home/naniadm/Documents/Website/builds/backend-rust/src/routes/meta.rs`, `/home/naniadm/Documents/Deadlock-Bots/rust/crates/dl-central-db/migrations/0006_tierlist.sql` |
| `tierlist.meta_tier_lists`, `tierlist.meta_votes`, `tierlist.meta_tier_history` | Tierlisten, Forks, Votes und History hängen an diesen Tabellen. | `/home/naniadm/Documents/Website/builds/backend-rust/src/routes/meta.rs`, `/home/naniadm/Documents/Deadlock-Bots/rust/crates/dl-central-db/migrations/0006_tierlist.sql` |
| `content.meta_reports`, `content.meta_announcements` | Admin-Reports und Ankündigungen nutzen das `content`-Schema. | `/home/naniadm/Documents/Website/builds/backend-rust/src/routes/meta.rs`, `/home/naniadm/Documents/Deadlock-Bots/rust/crates/dl-central-db/migrations/0010_activity_moderation_content_patchnotes.sql` |
| `patchnotes.changelog_posts`, `patchnotes.meta_patch_notes` | Patch-Public-Endpunkte und Patchnotes-Meta lesen Changelog- und Meta-Patchdaten. | `/home/naniadm/Documents/Website/builds/backend-rust/src/routes/public.rs`, `/home/naniadm/Documents/Website/builds/backend-rust/src/routes/meta.rs`, `/home/naniadm/Documents/Deadlock-Bots/rust/crates/dl-central-db/migrations/0010_activity_moderation_content_patchnotes.sql` |

## Nicht im Website-Datenmodell

`/aktivitaet` nutzt das Website-Frontend `dl-activity`, aber die produktive API liegt laut Caddy hinter `127.0.0.1:8768` und laut systemd-Beschreibung im separaten `deadlock-web-rust.service`; das zugehörige API-Schema liegt nicht im Website-Repo (`/home/naniadm/Documents/Caddy/conf/Caddyfile`, `/home/naniadm/.config/systemd/user/deadlock-web-rust.service`, `/home/naniadm/Documents/Website/dl-activity/src/activity.js`).
