---
title: "Deadlock-Bots Architektur"
tags: [deadlock-bots, intern, architektur]
stand: 2026-07-07
quelle: Deadlock-Bots
---
# Architektur

Der Rust-Code trennt Laufzeitprozesse und Fachlogik. `rust/bin/*` enthält Prozesse, `rust/crates/*` enthält wiederverwendbare Crates, und `rust/crates/dl-central-db/migrations` enthält das zentrale Postgres-Schema (`rust/Cargo.toml`, `rust/bin/dl-bot/src/main.rs`, `rust/bin/dl-web/src/main.rs`, `rust/crates/dl-central-db/migrations/0001_core_and_schemas.sql`).

## Crates

| Crate | Zuständigkeit | Beleg |
|---|---|---|
| `dl-core` | Start-Konfiguration, SQLite-Pfad und Default-Ports. | `rust/crates/dl-core/src/config.rs` |
| `dl-webcore` | Web-Konfiguration, Session-Cookies und Dashboard-Relay-Client. | `rust/crates/dl-webcore/src/config.rs`, `rust/crates/dl-webcore/src/dashboard.rs` |
| `dl-central-db` | Postgres-Pool, `DEADLOCK_CENTRAL_DSN` und Migrationen. | `rust/crates/dl-central-db/src/pool.rs`, `rust/bin/dl-central-migrate/src/main.rs` |
| `dl-central-etl` | SQLite-Snapshots, ETL-Ledger, Zielschreiber und Reconciliation. | `rust/crates/dl-central-etl/src/lib.rs`, `rust/bin/dl-central-sync/src/main.rs` |
| `dl-discord` | Gateway-Events, Interaction-Router und Discord-Adapter für die anderen Crates. | `rust/crates/dl-discord/src/gateway.rs`, `rust/bin/dl-bot/src/main.rs` |
| `dl-broker` | Interne `/internal/master/v1/*`-API für Discord-Aktionen mit Token und Idempotenz. | `rust/crates/dl-broker/src/lib.rs` |
| `dl-changelog` | Lokale Changelog- und Alert-Routen im Bot-Prozess. | `rust/crates/dl-changelog/src/lib.rs`, `rust/bin/dl-bot/src/main.rs` |
| `dl-bridges` | Twitch- und Steam-Brücken zu Schwester-Bots. | `rust/crates/dl-bridges/src/lib.rs`, `rust/crates/dl-bridges/src/twitch.rs`, `rust/crates/dl-bridges/src/steam.rs` |
| `dl-voice` | Voice-Tracker, TempVoice, Rank-Lanes, Router, Feedback und Nudge. | `rust/crates/dl-voice/src/lib.rs`, `rust/bin/dl-bot/src/main.rs` |
| `dl-activity` | Journey, Text-Stats, LFG, Player-Finder und Aktivitäts-Analysen. | `rust/crates/dl-activity/src/lib.rs`, `rust/crates/dl-activity/src/journey.rs` |
| `dl-community` | FAQ, Tags, Onboarding, Coaching, Privacy, Retention, Clips und Feedback. | `rust/crates/dl-community/src/lib.rs`, `rust/bin/dl-bot/src/main.rs` |
| `dl-moderation` | Content-Analyse, Verifikation, Verhaltensdetektor, Policy und Case-Store. | `rust/crates/dl-moderation/src/lib.rs`, `rust/crates/dl-moderation/src/moderation_system.rs` |
| `dl-dashboard` | Master-Dashboard, OAuth, Sessions, Analytics, Insights, Scrims und Repo-Aktivität. | `rust/crates/dl-dashboard/src/lib.rs`, `rust/crates/dl-dashboard/src/web.rs` |
| `dl-stats` | Öffentliche Aktivitäts- und persönliche Stats-APIs. | `rust/crates/dl-stats/src/lib.rs` |
| `dl-tierlist` | Öffentliche Tierlist-API, Votes, Admin-Routen und Refresh-Loop. | `rust/crates/dl-tierlist/src/lib.rs` |
| `dl-server-as-code` | Soll/Ist-Modell der Discord-Guild, Diffs, Apply-Runs und Drift. | `rust/crates/dl-server-as-code/src/lib.rs` |
| `dl-ai` | MiniMax-, Fireworks-, OpenAI- und Gemini-Clients hinter Text- und Vision-Traits. | `rust/crates/dl-ai/src/lib.rs` |
| `dl-brain` | Frage-Retrieval, Cooldowns und Antwortpfad für Brain-Fragen. | `rust/crates/dl-brain/src/lib.rs`, `rust/bin/dl-bot/src/main.rs` |
| `dl-squads` | Scrim- und Squad-Domäne, unter anderem Seed-Import. | `rust/bin/dl-bot/src/bin/seed_scrim.rs`, `rust/bin/dl-bot/src/scrimglue.rs` |

## Datenflüsse

Discord-Gateway-Events gehen im aktiven Gateway-Modus in `dl-discord`, von dort in Subscriber der Fach-Crates. Voice schreibt Sessions und Stats, Activity schreibt Journey- und Text-Metadaten, Community verarbeitet FAQ/Tags/Privacy, Moderation schreibt Cases und Review-Status (`rust/bin/dl-bot/src/main.rs`, `rust/crates/dl-voice/src/lib.rs`, `rust/crates/dl-activity/src/journey.rs`, `rust/crates/dl-moderation/src/store.rs`).

`dl-bot` stellt interne HTTP-Grenzen bereit. Der Master-Broker nimmt `/internal/master/v1/*` an, prüft `X-Internal-Token`, nutzt Idempotency-Keys und ruft Discord über Ports auf; Changelog, Server-Sync und MCP laufen im selben `tokio::select!` (`rust/crates/dl-broker/src/lib.rs`, `rust/bin/dl-bot/src/main.rs`, `rust/bin/dl-bot/src/mcp.rs`, `rust/bin/dl-bot/src/serversync.rs`).

`dl-web` teilt einen Postgres-Pool zwischen Dashboard, Public-Stats und Tierlist. Public-Stats und Tierlist delegieren Auth- und Session-Prüfungen über `DashboardClient` an das Dashboard (`rust/bin/dl-web/src/main.rs`, `rust/crates/dl-webcore/src/dashboard.rs`, `rust/crates/dl-dashboard/src/web.rs`, `rust/crates/dl-stats/src/lib.rs`, `rust/crates/dl-tierlist/src/lib.rs`).

`dl-central-sync` liest Ledger und SQLite-Snapshots, schreibt Zieltabellen in Postgres und kann Reconciliation gegen Quellsummen ausführen. Der Prozess bricht ab, wenn `snapshot-dir` und `ledger-dir` identisch sind (`rust/bin/dl-central-sync/src/main.rs`, `rust/crates/dl-central-etl/src/lib.rs`).

`dl-twitch-invite-sync` ruft `/internal/twitch/v1/streamer-invites` am Twitch-Bot ab, befüllt `bot.twitch_streamer_invites` und aktualisiert nur Join-Events, deren Klassifikation auf `twitch` zeigt. Website-Invite-Codes aus `bot.kv_store` schützen dabei gegen falsche Twitch-Reklassifikation (`rust/bin/dl-twitch-invite-sync/src/main.rs`, `rust/crates/dl-activity/src/join_source.rs`).

Server-Insights lesen Live-Daten aus Journey-, Presence-, Vanity- und Member-Directory-Tabellen. Alte Discord-Portal-Zahlen kommen per CSV-Import in `activity.insights_imports`; `/api/voice-history` und `/api/server-stats` bleiben eigene Pfade für historische Summen (`rust/crates/dl-dashboard/src/insights.rs`, `rust/crates/dl-dashboard/src/web.rs`, `rust/bin/dl-bot/src/vanity.rs`).

## Legacy

Legacy: Die alten Python-Teile unter `bot_core/`, `cogs/`, `service/` und `tests/` sind abgelöst. Die aktiven Live-Units für Bot und Web starten `rust/target/release/dl-bot` und `rust/target/release/dl-web`; der alte `deadlock-bot.service` war beim Abgleich inaktiv (`/home/naniadm/.config/systemd/user/deadlock-bot-rust.service`, `/home/naniadm/.config/systemd/user/deadlock-web-rust.service`, `scripts/run_dl_bot_service.sh`, `scripts/run_dl_web_service.sh`).
