# dl-central-db: zentrale PostgreSQL-Schicht und Migrationen

Interne Referenz für Support und Entwicklung. Beschrieben ist `Deadlock-Bots` am Commit `bb03deb53b28a7266de83748c3b834bff9c9a205`. Datenbestände einer laufenden Produktionsdatenbank wurden für diese Seite nicht gelesen.

## 1. Rolle der Crate

`Deadlock-Bots/rust/crates/dl-central-db` enthält die gemeinsame PostgreSQL-Basis für die Rust-Dienste. Die öffentliche Oberfläche in `src/lib.rs` exportiert unter anderem:

* `connect_pool` und `dsn_from_env` aus `pool.rs`
* Core-User-Funktionen aus `core_users.rs`
* KV-Zugriffe aus `kv.rs`
* Privacy- und Retention-Locks aus `locks.rs`
* Proactive-DM-Prüfungen und Scrim-Runtime-Helfer

Die Crate führt beim normalen Verbindungsaufbau keine Migration aus. Migrationen besitzen ein separates Binärprogramm.

## 2. Verbindung und Pool

`Deadlock-Bots/rust/crates/dl-central-db/src/pool.rs` liest den DSN über `DEADLOCK_CENTRAL_DSN`. `connect_pool` baut einen `sqlx::PgPool` mit maximal acht Verbindungen und einem Acquire-Timeout von zehn Sekunden.

Diese Werte sind Quellcode-Defaults der zentralen Crate. Ein Konsument kann zusätzliche Zeitlimits oder eigene Transaktionen darüber legen.

## 3. Schemas

Die erste Migration `Deadlock-Bots/rust/crates/dl-central-db/migrations/0001_core_and_schemas.sql` legt die Ausgangsschemas `core`, `coaching`, `scrim`, `steam`, `turnier`, `patchnotes` und `activity` an.

`0002_sp1_schemas_and_core.sql` ergänzt `voice`, `tierlist`, `moderation`, `bot`, `clips` und `content`.

Spätere Migrationen ergänzen weitere fachliche Schemas. Beispiele im aktuellen Migrationsbestand sind `brain`, `community` und `server_config`. Deshalb ist die Schema-Liste keine unveränderliche Enum. Maßgeblich ist das Verzeichnis `rust/crates/dl-central-db/migrations`.

## 4. Core-Identität und Rollenfelder

`core.users` ist in `0001_core_and_schemas.sql` der zentrale Discord-User-Stamm. `core.steam_links` verbindet Discord- und Steam-Identität und wird in späteren Migrationen erweitert.

`0002_sp1_schemas_and_core.sql` enthält außerdem `core.meta_users` mit einem Textfeld `role` und `core.user_privacy`.

Wichtig für die Formulierung "Rollen": Die Migrationsdateien modellieren mehrere fachliche Discord- beziehungsweise Anwendungsrollen, etwa in Voice-, Turnier- oder Konfigurationstabellen. Im untersuchten Migrationsbestand ist die Datenbank-Zugriffsverwaltung nicht als `CREATE ROLE`-Konzept dieser Crate dokumentiert. Diese Seite bezeichnet mit Rollen deshalb Datenmodell-Felder und Discord-Rollenbezüge, nicht PostgreSQL-Loginrollen.

## 5. Migrationsweg

Das ausführbare Migrationsprogramm liegt in `Deadlock-Bots/rust/bin/dl-central-migrate/src/main.rs`, Symbol `main`.

Ablauf:

1. DSN über `dl_central_db::dsn_from_env` lesen.
2. Pool über `connect_pool` verbinden.
3. Einen historisch bekannten, kurz veröffentlichten Prüfsummenfall für Migration `2026071602` gezielt abgleichen.
4. `sqlx::migrate!("../../crates/dl-central-db/migrations")` ausführen.
5. Mit Erfolg oder Fehlercode beenden.

Die Migrationen sind durch `sqlx::migrate!` zur Build-Zeit im Migrator eingebettet. Für eine neue SQL-Datei muss deshalb ein neu gebauter `dl-central-migrate` verwendet werden, bevor neuer Anwendungscode auf das Schema angewiesen ist.

## 6. Migrationen sind fortlaufende Historie

Frühe Dateien tragen kurze Sequenznummern wie `0001` bis `0012`. Spätere Dateien verwenden zeitstempelartige Versionsnummern wie `2026070210` oder `2026083101`.

Die operative Referenz ist die gesamte sortierte Migrationshistorie, nicht die Zahl der Dateien mit einem bestimmten Präfix. Bereits angewandte Migrationen werden von SQLx über `_sqlx_migrations` verfolgt.

Rollback-Dateien unter `Deadlock-Bots/rust/crates/dl-central-db/rollbacks` sind separate Betriebswerkzeuge. Sie sind nicht Teil des normalen `sqlx::migrate!`-Laufs.

## 7. Privacy-Locks

`Deadlock-Bots/rust/crates/dl-central-db/src/locks.rs` stellt transaktionsgebundene Advisory Locks bereit.

* `lock_user_privacy` sperrt den nutzerbezogenen Schreibpfad bis zum Transaktionsende.
* `lock_user_privacy_and_is_opted_out` hält denselben Lock und prüft danach den Tombstone in `core.user_privacy`.
* `lock_raw_event_retention_erasure` serialisiert Retention und Löschpfade, die dieselben Rohereignisse verändern.

Diese Sperren sind Infrastruktur für Crates wie `dl-community`. Sie ersetzen keine fachliche Löschlogik.

## 8. Tests und Schema-Harness

Unter `Deadlock-Bots/rust/crates/dl-central-db/tests` liegen Integrationstests für frische Migrationen und fachliche Invarianten. `fresh_migrations_schema.rs` startet den Migrator gegen eine Wegwerf-Datenbank. Weitere Tests prüfen unter anderem Steam-Link-Invarianten und Scrim-Grundlagen.

Für eine Änderung an Migrationen sind diese Tests aussagekräftiger als eine reine SQL-Syntaxprüfung, weil sie die vollständige Historie gegen ein frisches Schema ausführen.

## 9. Quellreferenzen

| Thema | Datei und Symbol |
|---|---|
| öffentliche API | `Deadlock-Bots/rust/crates/dl-central-db/src/lib.rs` |
| DSN und Pool | `Deadlock-Bots/rust/crates/dl-central-db/src/pool.rs`, `dsn_from_env`, `connect_pool` |
| Advisory Locks | `Deadlock-Bots/rust/crates/dl-central-db/src/locks.rs` |
| Ausgangsschemas und Core | `Deadlock-Bots/rust/crates/dl-central-db/migrations/0001_core_and_schemas.sql`, `0002_sp1_schemas_and_core.sql` |
| Migrator | `Deadlock-Bots/rust/bin/dl-central-migrate/src/main.rs`, `main` |
| Fresh-Schema-Test | `Deadlock-Bots/rust/crates/dl-central-db/tests/fresh_migrations_schema.rs` |

## 10. Grenzen dieser Referenz

Nicht geprüft wurden Datenbankgröße, Tabellenzeilenzahlen, aktuell angewandte Migrationen, Replikation, Backups und Produktionsrollen des PostgreSQL-Servers. Dafür sind Live- und Betriebsquellen erforderlich.
