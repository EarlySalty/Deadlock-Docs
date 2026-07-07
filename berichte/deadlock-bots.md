---
title: "Deadlock-Bots Bericht"
tags: [deadlock-bots, intern, bericht]
stand: 2026-07-07
quelle: Deadlock-Bots
---
# Bericht

## Dateiliste

- `uebersicht.md`: Systemzweck, Binaries, Ports und Service-Namen aus Skripten.
- `architektur.md`: Crates, Zuständigkeiten und Datenflüsse.
- `datenmodell.md`: Postgres-Schemata und Invarianten aus Migrationen.
- `betrieb.md`: Build, Start, Restart, Env-Variablen und Fallen.
- `integrationen.md`: MCP, Broker, Website-APIs, Twitch-Bridge, Steam und Discord-REST.
- `faq-grounding.md`: FAQ-Doku-Loader, Sessions, Ticket-Tools und Guard.
- `moderation-scam-guard.md`: Moderationspipeline, Scam-Heuristiken, Policy und Retention.
- `bericht.md`: Arbeitsbericht, veraltete Funde und offene Unsicherheiten.

## Veraltete oder widersprüchliche Funde

`rust/Cargo.toml` kommentiert noch "2 Binaries (dl-bot, dl-web)", aber `members` enthält sechs `rust/bin/*`-Pakete; zusätzlich liegt `rust/bin/dl-mcp` im Baum, aber nicht in `members` (`rust/Cargo.toml`, `rust/bin/dl-mcp/Cargo.toml`).

`scripts/run_dl_web_service.sh` kommentiert `Turnier :8767`; `rust/bin/dl-web/src/main.rs` bindet nur Dashboard `:8766`, Public-Stats `:8768` und Tierlist `:8771` (`scripts/run_dl_web_service.sh`, `rust/bin/dl-web/src/main.rs`).

`scripts/run_twitch_invite_sync.sh` kommentiert "Deadlock-sqlite" und setzt `DEADLOCK_DB_PATH`; `dl-twitch-invite-sync` ruft `dl_central_db::dsn_from_env()` auf und schreibt Postgres-Tabellen (`scripts/run_twitch_invite_sync.sh`, `rust/bin/dl-twitch-invite-sync/src/main.rs`, `rust/crates/dl-central-db/src/pool.rs`).

`old/docs/deadlock-steam-watchdog.service` bindet an `deadlock-bot.service` und startet einen Python-Watchdog aus `old/standalone`. Die aktive Rust-Steam-Bridge im Code ist HTTP-forwarding zum Steam-Bot und kein Watchdog-Service (`old/docs/deadlock-steam-watchdog.service`, `rust/crates/dl-bridges/src/steam.rs`).

`twitch-clips-und-social.md` beschreibt eine Social-Upload-Pipeline. In die neue Doku wurde nur der belegte Clip-Einsende- und Fensterpfad übernommen; Social-Uploads, Approval-Queue und Plattform-Analytics wurden nicht als aktiver Rust-Pfad dokumentiert (`rust/crates/dl-community/src/clips.rs`, `rust/crates/dl-central-db/migrations/0008_clips.sql`).

## UNSICHER

UNSICHER: Die Unit-Dateien für `deadlock-bot-rust`, `deadlock-web-rust` und `deadlock-twitch-invite-sync` liegen nicht im Repo. Belegt sind nur Service-Namen in Skripten und die Ziel-Binaries (`scripts/set_infisical_token.sh`, `scripts/run_dl_bot_service.sh`, `scripts/run_dl_web_service.sh`, `scripts/run_twitch_invite_sync.sh`).

UNSICHER: `dl-mcp` liegt unter `rust/bin/`, fehlt aber im Workspace. Ob es absichtlich separat gebaut wird, ist aus Code und Skripten nicht belegt (`rust/Cargo.toml`, `rust/bin/dl-mcp/Cargo.toml`).

UNSICHER: FAQ-Patchnote-Anreicherung ist im Rust-Kommentar als Lücke markiert. Ein aktiver Codepfad dafür ist in `dl-community/src/faq.rs` nicht belegt (`rust/crates/dl-community/src/faq.rs`).
