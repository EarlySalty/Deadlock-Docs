---
title: "Deadlock Steam-Bot Task-Queue"
tags: [internal, steam, queue]
stand: 2026-07-08
quelle: "Deadlock-Steam-Bot"
---
# Task-Queue

`steam-core` bedient `steam.steam_tasks` alle 500 ms. Der Runner bereinigt stale `RUNNING`-Tasks, verwirft stale sensitive oder unbekannte `PENDING`-Tasks und claimt danach neue Tasks pro Lane. (`rust/crates/steam-core/src/task/runner.rs`, `rust/crates/steam-persistence/src/tasks.rs`)

Ein Task-Erfolg wird als `status='DONE'` mit `result={"ok":true,"data":...}` gespeichert. Ein Fehler wird als `status='FAILED'` mit `result={"ok":false,"error":...}` gespeichert. (`rust/crates/steam-core/src/task/runner.rs`)

Der Runner claimt atomar per `FOR UPDATE SKIP LOCKED`. Dadurch können mehrere Worker dieselbe Zeile nicht gleichzeitig übernehmen. (`rust/crates/steam-persistence/src/tasks.rs`)

## Lanes

| Lane | Parallelität | Task-Typen | Beleg |
|---|---:|---|---|
| `interactive_reads` | 2 | `AUTH_STATUS`, `AUTH_GET_FRIENDS_LIST`, `AUTH_CHECK_FRIENDSHIP` | `rust/crates/steam-core/src/task/lanes.rs` |
| `profile_card` | 1 | `GC_GET_PROFILE_CARD`, `GC_GET_ACCOUNT_STATS`, `GC_GET_MATCH_HISTORY` | `rust/crates/steam-core/src/task/lanes.rs` |
| `control` | 1 | `AUTH_LOGIN`, `AUTH_GUARD_CODE`, `AUTH_LOGOUT`, `AUTH_REFRESH_GAME_VERSION`, `AUTH_SEND_FRIEND_REQUEST`, `AUTH_REMOVE_FRIEND`, `AUTH_SEND_PLAYTEST_INVITE` | `rust/crates/steam-core/src/task/lanes.rs` |
| `lobby` | 1 | `GC_CREATE_CUSTOM_LOBBY`, `GC_LOBBY_SET_CONVAR`, `GC_LOBBY_APPLY_CONVARS`, `GC_LOBBY_INVITE_PLAYER`, `GC_LOBBY_SET_SPECTATOR`, `GC_LOBBY_READY`, `GC_LOBBY_START_MATCH`, `GC_LOBBY_LEAVE`, `GC_GET_MATCH_RESULT` | `rust/crates/steam-core/src/task/lanes.rs` |
| `background` | 1 | `BUILD_PUBLISH`, `BUILD_DELETE`, `DISCOVER_WATCHED_BUILDS`, `DISCOVER_BUILDS_VIA_HEROES`, `MAINTAIN_BUILD_CATALOG`, `BUILD_CATALOG_CYCLE`, `GC_SEARCH_BUILDS` | `rust/crates/steam-core/src/task/lanes.rs` |

`profile_card` bleibt bewusst auf Parallelität 1, weil Profilkarten-, Account-Stats- und Match-History-Antworten aus dem GC nicht sauber genug mit parallelen Requests korrelierbar sind. (`rust/crates/steam-core/src/task/lanes.rs`, `rust/crates/steam-core/src/task/runner.rs`)

## Registry

`default_registry()` registriert Handler für Status, Auth, Friends, GC-Reads, Lobby, Playtest-Invite und Build-Katalog. Aktive Build-Handler sind `BUILD_PUBLISH`, `BUILD_DELETE`, `MAINTAIN_BUILD_CATALOG` und `BUILD_CATALOG_CYCLE`; `DISCOVER_WATCHED_BUILDS` und `DISCOVER_BUILDS_VIA_HEROES` sind registrierte Legacy-Stubs und schließen mit `legacy=true`, `skipped=true` ab. Wenn ein Task-Typ keine Registrierung hat, finalisiert der Runner ihn als `unsupported_task_type`. (`rust/crates/steam-core/src/task/mod.rs`, `rust/crates/steam-core/src/task/handlers/builds/discovery.rs`, `rust/crates/steam-core/src/task/runner.rs`)

`TaskContext` trägt GC-Verbindung, Steam-Verbindung, Friends-State, Party-Cache und optional DB-Handle zu jedem Handler. (`rust/crates/steam-core/src/task/handler.rs`)

## HTTP-IPC

`POST /tasks` schreibt neue Tasks in `steam.steam_tasks`. Der Request nutzt `type` und optional `payload`; der Handler gibt nur die neue ID zurück. (`rust/crates/steam-core/src/api/mod.rs`)

`GET /tasks/{id}` liest `status`, `result` und `error`. Das Ergebnis wird von Flow-Code gepollt, bis `DONE`, `FAILED` oder Timeout erreicht ist. (`rust/crates/steam-core/src/api/mod.rs`, `rust/crates/steam-flows/src/shared.rs`)

`/health` ist immer offen. `POST /tasks`, `GET /tasks/{id}`, `/status` und `/friends` sind nur geschützt, wenn `STEAM_CORE_API_TOKEN` gesetzt ist; sonst bleiben sie im Loopback-/Dev-Modus offen. Bei falschem oder fehlendem Header antwortet die API mit `ungültiges oder fehlendes X-Internal-Token`. (`rust/crates/steam-core/src/api/mod.rs`)

`steam-flows` pollt Task-Status alle 500 ms und unterscheidet `Settled` von `Timeout`; ein Timeout lässt den Task in der Queue weiterlaufen. (`rust/crates/steam-flows/src/shared.rs`)

## Wartung

Stale `RUNNING`-Tasks werden nach 600 Sekunden auf `FAILED` gesetzt. (`rust/crates/steam-core/src/task/runner.rs`)

Sensitive `PENDING`-Tasks mit Payload werden nach 120 Sekunden auf `FAILED` gesetzt und verlieren den Payload. Der Fehlertext lautet `Task stale: sensitiver Payload ohne Abholung verworfen`. Unbekannte `PENDING`-Task-Typen werden ebenfalls `FAILED` mit `Task stale: unbekannter Task-Typ wurde nicht verarbeitet`. (`rust/crates/steam-core/src/task/runner.rs`, `rust/crates/steam-persistence/src/tasks.rs`)

`STEAM_TASKS_MAX_ROWS` steuert die Prune-Obergrenze; ohne Variable behält `prune()` höchstens 1000 Zeilen und löscht nur terminale Tasks. (`rust/crates/steam-persistence/src/tasks.rs`)

Der Catalog-Maintenance-Scheduler plant `MAINTAIN_BUILD_CATALOG` erstmals nach 30 Sekunden und danach alle `CATALOG_MAINTENANCE_INTERVAL_MS` ein, wenn kein offener Catalog-Task existiert. (`rust/crates/steam-core/src/main.rs`, `rust/crates/steam-persistence/src/builds.rs`)
