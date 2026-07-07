---
title: "Deadlock Steam-Bot Architektur"
tags: [internal, steam, architektur]
stand: 2026-07-07
quelle: "Deadlock-Steam-Bot"
---
# Architektur

## Prozessgrenzen

`steam-core` ist der einzige Prozess mit Steam-Session und Deadlock-GC-Verbindung. Er baut die Steam-Verbindung, startet Friends-/Presence-/CSO-Listener, öffnet die Task-Queue und bietet die interne HTTP-API an. (`rust/crates/steam-core/src/main.rs`)

`steam-bot` spricht nicht direkt mit Steam. Er nutzt `FlowContext`, ruft `steam-core` per HTTP `POST /tasks` und `GET /tasks/{id}` auf und schickt Discord-Seiteneffekte an den Master-Broker. (`rust/crates/steam-flows/src/shared.rs`, `rust/crates/steam-discord/src/broker.rs`)

Beide Prozesse öffnen die zentrale Postgres-DB über `dl_central_db::dsn_from_env()` und `dl_central_db::connect_pool()`. Die DSN heißt `DEADLOCK_CENTRAL_DSN` und wird nicht in `Config` gehalten. (`rust/crates/steam-core/src/main.rs`, `rust/crates/steam-bot/src/main.rs`, `/home/naniadm/Documents/Deadlock-Bots/rust/crates/dl-central-db/src/pool.rs`)

## Crate-Schnitt

`steam-persistence` kapselt alle DB-Zugriffe über einen clonebaren `PgPool`. Die Crate führt keine Produktionsmigrationen aus; das Schema liegt laut Crate-Kommentar in `dl-central-db`. (`rust/crates/steam-persistence/src/lib.rs`)

`steam-gc` kapselt GC-IDs, Framing und Codec; `deadlock-proto` baut die Deadlock-Protobuf-Typen aus den Proto-Dateien. (`rust/crates/steam-gc/src/lib.rs`, `rust/crates/deadlock-proto/build.rs`)

`steam-web` baut den Axum-Router für `steam-bot`. Der Router merged Link-, Rank-, Event- und Ko-fi-Routen. (`rust/crates/steam-web/src/lib.rs`, `rust/crates/steam-web/src/routes/mod.rs`)

`steam-flows` enthält Business-Flows ohne HTTP-Server. Es bekommt DB, Discord-Port, HTTP-Client und FlowConfig im `FlowContext`. (`rust/crates/steam-flows/src/shared.rs`)

## Datenfluss

Ein Flow reiht Arbeit über `enqueue_steam_task()` bei `steam-core` ein. Die Funktion sendet JSON an `POST {STEAM_CORE_URL}/tasks` und hängt `x-internal-token` an, wenn `STEAM_CORE_API_TOKEN` gesetzt ist. (`rust/crates/steam-flows/src/shared.rs`)

`steam-core` schreibt den HTTP-Task in `steam.steam_tasks`. Der TaskRunner claimt pro Lane offene Tasks, startet Handler in Tokio-Tasks und finalisiert sie mit `DONE` oder `FAILED`. (`rust/crates/steam-core/src/api/mod.rs`, `rust/crates/steam-core/src/task/runner.rs`)

Der HTTP-Status eines Tasks kommt aus `GET /tasks/{id}`. Der Web-Handler liest `status`, `result` und `error` direkt aus `steam.steam_tasks`. (`rust/crates/steam-core/src/api/mod.rs`, `rust/crates/steam-persistence/src/tasks.rs`)

## Scheduler

`steam-bot` startet `friend_sync`, `rank`, `purge`, `leave_cleanup`, `supporter`, `betainvite_dispatcher`, `friendship_poller` und `ticket_cleanup`. Jeder Scheduler läuft unter `spawn_supervised`; ein Ende oder Panic beendet den Prozess mit Exit 1. (`rust/crates/steam-bot/src/main.rs`)

Der Link-Flow hat keinen Scheduler. Er läuft über HTTP-Routen und Discord-Events. (`rust/crates/steam-bot/src/main.rs`, `rust/crates/steam-flows/src/link.rs`)

`steam-core` startet den TaskRunner, den standalone Command-Consumer, den Catalog-Maintenance-Scheduler und die GC-/Steam-Supervisoren. (`rust/crates/steam-core/src/main.rs`, `rust/crates/steam-core/src/command_loop.rs`)

## Fehlergrenzen

Wenn der Steam-Login mit konfigurierten Zugangsdaten fehlschlägt, gibt `steam-core` einen Fehler zurück und die Unit kann per `Restart=on-failure` neu starten. (`rust/crates/steam-core/src/main.rs`, `rust/deploy/steam-core.service`)

Wenn `steam-core` die Steam-Session verliert, setzt der Disconnect-Supervisor die Shutdown-Ursache auf `Disconnect`; danach beendet der Prozess mit Exit 1. (`rust/crates/steam-core/src/main.rs`, `rust/crates/steam-core/src/steam/supervisor.rs`)

Wenn ein `steam-bot`-Scheduler endet oder panict, ruft der Watcher `std::process::exit(1)`. (`rust/crates/steam-bot/src/main.rs`)

Wenn die `steam-core`-HTTP-API nicht binden kann, loggt sie den Fehler und der Prozess läuft ohne diese API weiter. (`rust/crates/steam-core/src/api/mod.rs`)

