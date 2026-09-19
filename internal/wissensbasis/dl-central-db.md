# dl-central-db: PostgreSQL-Schicht und Migrationen

stand: 2026-09-19  
quelle: `Deadlock-Bots` Commit `bb03deb53b28a7266de83748c3b834bff9c9a205`

Interne Referenz für Support und Entwicklung. Produktionsdaten wurden für diese Seite nicht gelesen.

## Verbindung und Pool

Die zentrale Crate liest den DSN aus `DEADLOCK_CENTRAL_DSN`, `Deadlock-Bots/rust/crates/dl-central-db/src/pool.rs:7-9`. `connect_pool` baut den SQLx-Pool in `Deadlock-Bots/rust/crates/dl-central-db/src/pool.rs:11-18`. Der Quellstand setzt maximal acht Verbindungen und zehn Sekunden Acquire-Timeout, ebenfalls `pool.rs:8-9`.

`dsn_from_env` liegt in `Deadlock-Bots/rust/crates/dl-central-db/src/pool.rs:21-26`.

## Schemas

Die Ausgangsmigration legt `core`, `coaching`, `scrim`, `steam`, `turnier`, `patchnotes` und `activity` an, `Deadlock-Bots/rust/crates/dl-central-db/migrations/0001_core_and_schemas.sql:3-9`.

Die nächste Grundmigration ergänzt `voice`, `tierlist`, `moderation`, `bot`, `clips` und `content`, `Deadlock-Bots/rust/crates/dl-central-db/migrations/0002_sp1_schemas_and_core.sql:1-6`.

Spätere Migrationen erweitern die Schema-Landschaft weiter. Die operative Quelle ist deshalb das gesamte Verzeichnis `Deadlock-Bots/rust/crates/dl-central-db/migrations`, nicht eine feste Liste aus dieser Seite.

## User- und Rollenbezüge

`core.users` und `core.steam_links` werden in `Deadlock-Bots/rust/crates/dl-central-db/migrations/0001_core_and_schemas.sql:11-30` angelegt.

`core.meta_users` und `core.user_privacy` folgen in `Deadlock-Bots/rust/crates/dl-central-db/migrations/0002_sp1_schemas_and_core.sql:163-188`. Das Feld `role` in `core.meta_users` ist ein Anwendungsfeld. Discord-Rollenbezüge tauchen zusätzlich in Fachschemas auf. Diese Doku macht keine Aussage über PostgreSQL-Loginrollen des Hosts.

## Migrationsweg

Der separate Migrator startet in `Deadlock-Bots/rust/bin/dl-central-migrate/src/main.rs:49-65`.

Vor dem normalen SQLx-Lauf kann er einen historisch bekannten Prüfsummenfall gezielt abgleichen. Die Hilfsfunktion beginnt in `Deadlock-Bots/rust/bin/dl-central-migrate/src/main.rs:14-45`.

Der eigentliche Lauf verwendet `sqlx::migrate!("../../crates/dl-central-db/migrations")`, `Deadlock-Bots/rust/bin/dl-central-migrate/src/main.rs:60-62`. Die Migrationen werden dadurch beim Build des Migrators eingebettet. Eine neue Migrationsdatei erfordert daher einen neu gebauten Migrator, bevor Anwendungscode auf das neue Schema angewiesen wird.

## Privacy-Locks

Die Crate stellt transaktionsgebundene Advisory Locks bereit:

- Retention gegen Löschpfade: `Deadlock-Bots/rust/crates/dl-central-db/src/locks.rs:7-16`
- User-Privacy-Lock: `Deadlock-Bots/rust/crates/dl-central-db/src/locks.rs:19-28`
- Lock plus Opt-out/Tombstone-Prüfung: `Deadlock-Bots/rust/crates/dl-central-db/src/locks.rs:31-45`

Diese Sperren koordinieren konkurrierende Schreib- und Löschpfade. Die fachliche Löschung selbst liegt in den konsumierenden Crates.

## Testweg

Der Fresh-Schema-Harness liegt in `Deadlock-Bots/rust/crates/dl-central-db/tests/fresh_migrations_schema.rs`. Er führt den Migrator gegen eine Wegwerf-Datenbank aus und prüft die vollständige Migrationshistorie.

Nicht geprüft wurden Produktionsgröße, Backups, Replikation, aktuell angewandte Migrationen und Host-Rollen.
