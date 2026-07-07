---
title: "Deadlock Steam-Bot Datenmodell"
tags: [internal, steam, datenmodell]
stand: 2026-07-07
quelle: "Deadlock-Steam-Bot"
---
# Datenmodell

Die produktive Persistenz läuft über Postgres und `sqlx::PgPool`. `steam-persistence` sagt ausdrücklich, dass es keine produktiven Migrationen ausführt und dass das Schema in `dl-central-db` liegt. (`rust/crates/steam-persistence/src/lib.rs`)

Die DSN kommt aus `DEADLOCK_CENTRAL_DSN`. `dl-central-db::dsn_from_env()` liest genau diesen Namen. (`/home/naniadm/Documents/Deadlock-Bots/rust/crates/dl-central-db/src/pool.rs`)

## Schema `steam`

`dl-central-db` legt `CREATE SCHEMA IF NOT EXISTS steam` an. Die Steam-spezifischen Tabellen entstehen in `0003_steam.sql`; spätere Migrationen ergänzen Rank-History, Friend-Request-Task-Link und Rank-History-Visibility. (`/home/naniadm/Documents/Deadlock-Bots/rust/crates/dl-central-db/migrations/0003_steam.sql`, `/home/naniadm/Documents/Deadlock-Bots/rust/crates/dl-central-db/migrations/2026070311_steam_rank_history_account_scope.sql`, `/home/naniadm/Documents/Deadlock-Bots/rust/crates/dl-central-db/migrations/2026070312_steam_friend_requests_task_link.sql`, `/home/naniadm/Documents/Deadlock-Bots/rust/crates/dl-central-db/migrations/2026070260_rank_history_visibility.sql`)

`steam.steam_tasks` enthält `id`, `type`, `payload`, `status`, `result`, `error`, `created_at`, `updated_at`, `started_at`, `finished_at` und `attempts`. Die Migration setzt Indizes auf `attempts`, `created_at`, `(status, id)` und `updated_at`. (`/home/naniadm/Documents/Deadlock-Bots/rust/crates/dl-central-db/migrations/0003_steam.sql`)

`steam.steam_tasks` ist die GC-/Steam-Task-Queue. `insert()` schreibt `PENDING`, `next_pending()` claimt per `UPDATE ... FOR UPDATE SKIP LOCKED ... RETURNING`, `finalize()` setzt `DONE` oder `FAILED` und löscht den Payload. (`rust/crates/steam-persistence/src/tasks.rs`)

Sensitive Task-Typen sind `AUTH_LOGIN` und `AUTH_GUARD_CODE`. Der Claim setzt deren `payload` in der Tabelle auf `NULL`, liefert dem Handler aber den vor dem Löschen gelesenen Payload zurück. (`rust/crates/steam-core/src/task/lanes.rs`, `rust/crates/steam-persistence/src/tasks.rs`)

`steam.steam_friend_requests` speichert ausgehende Steam-Friend-Requests. `2026070312_steam_friend_requests_task_link.sql` ergänzt `task_id`, damit Reconcile nach Neustarts Task-Ergebnisse wiederfindet. (`/home/naniadm/Documents/Deadlock-Bots/rust/crates/dl-central-db/migrations/0003_steam.sql`, `/home/naniadm/Documents/Deadlock-Bots/rust/crates/dl-central-db/migrations/2026070312_steam_friend_requests_task_link.sql`, `rust/crates/steam-persistence/src/friends.rs`)

`steam.steam_friend_check_cache`, `steam.steam_friendship_miss_tracker` und `steam.steam_cleanup_poll_state` tragen Friend-Status, Miss-Zähler und Cleanup-Poll-Zustand. (`/home/naniadm/Documents/Deadlock-Bots/rust/crates/dl-central-db/migrations/0003_steam.sql`, `rust/crates/steam-persistence/src/friend_cache.rs`, `rust/crates/steam-persistence/src/miss_tracker.rs`)

`steam.steam_launch_tokens` speichert kurzlebige One-Time-Launch-Tokens für den Link-Flow. `consume_launch_token()` setzt `consumed_at`, wenn das Token noch gültig und unbenutzt ist. (`/home/naniadm/Documents/Deadlock-Bots/rust/crates/dl-central-db/migrations/0003_steam.sql`, `rust/crates/steam-persistence/src/oauth_state.rs`)

`steam.steam_beta_invites`, `steam.beta_invite_*` und `steam.steam_quick_invites` tragen Playtest-Invite, Ticket, Payment, Auto-Poll und Supporter-Zustand. (`/home/naniadm/Documents/Deadlock-Bots/rust/crates/dl-central-db/migrations/0003_steam.sql`, `rust/crates/steam-persistence/src/betainvite.rs`, `rust/crates/steam-persistence/src/supporter.rs`)

`steam.steam_rank_history` speichert Rang-Snapshots. `2026070311_steam_rank_history_account_scope.sql` ergänzt `steam_id`, und `2026070260_rank_history_visibility.sql` ergänzt Sichtbarkeitsdaten. (`/home/naniadm/Documents/Deadlock-Bots/rust/crates/dl-central-db/migrations/0003_steam.sql`, `/home/naniadm/Documents/Deadlock-Bots/rust/crates/dl-central-db/migrations/2026070311_steam_rank_history_account_scope.sql`, `/home/naniadm/Documents/Deadlock-Bots/rust/crates/dl-central-db/migrations/2026070260_rank_history_visibility.sql`, `rust/crates/steam-persistence/src/rank.rs`)

`steam.steam_links_archive`, `steam.steam_links_leave_archive` und `steam.steam_role_cleanup_pending` speichern entfernte Links und ausstehende Rollenbereinigung. (`/home/naniadm/Documents/Deadlock-Bots/rust/crates/dl-central-db/migrations/0003_steam.sql`, `rust/crates/steam-persistence/src/role_cleanup.rs`)

## Link-Daten außerhalb `steam`

Aktive Steam-Verknüpfungen liegen in `core.steam_links`, nicht in `steam.*`. Der Code liest und schreibt `discord_id`, `steam_id`, `steam_id64`, `steam_display_name`, `verified`, `is_steam_friend`, `primary_account` und Rangfelder dort. (`rust/crates/steam-persistence/src/links.rs`, `/home/naniadm/Documents/Deadlock-Bots/rust/crates/dl-central-db/migrations/0002_sp1_schemas_and_core.sql`)

Die Migration `0015_steam_links_one_primary.sql` erzwingt höchstens einen `primary_account` pro Discord-User über `uq_steam_links_one_primary`. (`/home/naniadm/Documents/Deadlock-Bots/rust/crates/dl-central-db/migrations/0015_steam_links_one_primary.sql`)

`upsert_link()` nimmt zusätzlich einen Postgres-Advisory-Lock auf `steam_links.primary:{user_id}` und ignoriert nur die spezifische Unique-Verletzung `uq_steam_links_one_primary` als benign. (`rust/crates/steam-persistence/src/links.rs`)

OAuth-States des Link-Flows liegen in `bot.oauth_states`. `create_state()`, `peek_state()` und `consume_state()` lesen und schreiben diese Tabelle. (`/home/naniadm/Documents/Deadlock-Bots/rust/crates/dl-central-db/migrations/0007_bot.sql`, `rust/crates/steam-persistence/src/oauth_state.rs`)

## Presence und Party

`activity.live_player_state` kommt aus der zentralen Activity-Migration und wird vom Steam-Presence-Logger mit Deadlock-Status, Hero, Stage und Zeitdaten gefüllt. (`/home/naniadm/Documents/Deadlock-Bots/rust/crates/dl-central-db/migrations/0011_barrier_orphans_and_cross_fks.sql`, `rust/crates/steam-persistence/src/presence.rs`, `rust/crates/steam-core/src/steam/presence.rs`)

`voice.deadlock_party_members` kommt aus der Voice-Migration und wird über Rich-Presence oder CSO-Party-Pushes aktualisiert. (`/home/naniadm/Documents/Deadlock-Bots/rust/crates/dl-central-db/migrations/0005_voice.sql`, `rust/crates/steam-persistence/src/presence.rs`, `rust/crates/steam-persistence/src/party_members.rs`, `rust/crates/steam-core/src/steam/cso.rs`)

Die gelesenen Live-Units setzen keinen `DEADLOCK_DB_PATH`. `steam-core.service` und `steam-bot.service` laden Secrets über Wrapper und systemd-Credentials; der Rust-Code öffnet die zentrale Postgres-DB über `DEADLOCK_CENTRAL_DSN` (`/home/naniadm/.config/systemd/user/steam-core.service`, `/home/naniadm/.config/systemd/user/steam-bot.service`, `rust/deploy/run-steam-core.sh`, `rust/deploy/run-steam-bot.sh`, `/home/naniadm/Documents/Deadlock-Bots/rust/crates/dl-central-db/src/pool.rs`).
