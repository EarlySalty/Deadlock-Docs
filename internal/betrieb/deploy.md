---
title: "Cross-System-Betrieb - Deploy"
tags: [internal, betrieb, deploy, systemd]
stand: 2026-07-07
quelle: "Service-Wrapper, Cargo-Workspaces, systemd-User-Units"
---
# Cross-System-Betrieb - Deploy

Rust-Dienste werden als Release-Binary gebaut und per systemd-User-Service neu gestartet.
Der Live-Beweis ist PID-Wechsel plus `/proc/<pid>/exe`.
Git-Schritte gehören nicht in dieses Runbook.

## Build

| Repo | Build-Pfad | Kommando | Beleg |
|---|---|---|---|
| `Deadlock-Bots` | `/home/naniadm/Documents/Deadlock-Bots/rust` | `cargo build --release --workspace` | `Deadlock-Bots/rust/Cargo.toml`; `Deadlock-Bots/scripts/run_dl_bot_service.sh`; `Deadlock-Bots/scripts/run_dl_web_service.sh` |
| `Deadlock-Steam-Bot` | `/home/naniadm/Documents/Deadlock-Steam-Bot/rust` | `cargo build --release --workspace` | `Deadlock-Steam-Bot/rust/Cargo.toml`; `Deadlock-Steam-Bot/rust/deploy/run-steam-core.sh`; `Deadlock-Steam-Bot/rust/deploy/run-steam-bot.sh` |
| `Deadlock-Twitch-Bot` | `/home/naniadm/Documents/Deadlock-Twitch-Bot/rust` | `cargo build --release --workspace` | `Deadlock-Twitch-Bot/rust/Cargo.toml`; `Deadlock-Twitch-Bot/rust/scripts/run_tb_bot_service.sh`; `Deadlock-Twitch-Bot/rust/scripts/run_tb_dashboard_service.sh` |
| `Deadlock-Turniere` | `/home/naniadm/Documents/Deadlock-Turniere/rust` | `cargo build --release --workspace` | `Deadlock-Turniere/rust/Cargo.toml`; `Deadlock-Turniere/scripts/run_turniere_backend_rust.sh` |
| `Website` | `/home/naniadm/Documents/Website/builds/backend-rust` | `cargo build --release` | `Website/builds/backend-rust/Cargo.toml`; `Website/scripts/run_builds_backend.sh` |

Patchnotes ist die Ausnahme: `deadlock-patchnotes.service` startet `main.py` über den Wrapper und hat keinen Rust-Build im Servicepfad. (`systemctl --user cat deadlock-patchnotes.service`; `Deadlock--Patchnotes-Bot/scripts/run_patchnotes_bot.sh`)

## Neustart

Nach einem erfolgreichen Build wird nur der betroffene User-Service neu gestartet:

```bash
systemctl --user restart <service-name>
```

Bei abhängigen Paaren ist die Reihenfolge aus den Units und Wrappern abzuleiten: `steam-bot.service` hängt an `steam-core.service` und wartet zusätzlich auf `http://127.0.0.1:8782/`; Twitch-Dashboard und Twitch-Worker sind getrennte Rust-Services. (`systemctl --user cat steam-bot.service`; `Deadlock-Steam-Bot/rust/deploy/run-steam-bot.sh`; `systemctl --user cat deadlock-twitch-bot-rust.service`; `systemctl --user cat deadlock-twitch-dashboard-rust.service`)

## Live-Beweis

Der minimale Beweis nach einem Neustart:

```bash
svc=<service-name>
before=<pid-vor-restart>
systemctl --user restart "$svc"
after="$(systemctl --user show -p MainPID --value "$svc")"
test "$after" != "$before"
readlink -f "/proc/$after/exe"
journalctl --user -u "$svc" -n 200 --no-pager | rg -i 'panic|error|failed|traceback'
```

`readlink -f /proc/<pid>/exe` muss auf das erwartete `target/release/*`-Binary zeigen, weil die Wrapper am Ende `exec` verwenden. Der Journal-Grep darf bekannte Warnungen zeigen, aber keine neuen Startfehler, Panics oder Tracebacks. (`Deadlock-Bots/scripts/run_dl_bot_service.sh`; `Deadlock-Steam-Bot/rust/deploy/run-steam-core.sh`; `Deadlock-Twitch-Bot/rust/scripts/run_tb_bot_service.sh`; `Deadlock-Turniere/scripts/run_turniere_backend_rust.sh`; `Website/scripts/run_builds_backend.sh`)

## Haupttree belegt

Wenn der Haupttree durch laufende Arbeit belegt ist, im vorhandenen Worktree unter `.claude/worktrees/...` bauen oder den Build dort anstoßen lassen. Die Repos ignorieren diese Worktree-Pfade, also gehören Artefakte nicht in den Haupttree zurück außer dem freigegebenen Release-Binary. (`Deadlock-Bots/.gitignore`; `Deadlock-Twitch-Bot/.gitignore`)

Binary-Swap ist nur der letzte Schritt: aus dem Worktree bauen, Zielservice stoppen oder kontrolliert neu starten, dann das geprüfte Binary in den vom Wrapper erwarteten Pfad unter `target/release/` installieren. Danach gilt wieder der Live-Beweis mit PID-Wechsel, `/proc/<pid>/exe` und Journal-Grep. (`Deadlock-Steam-Bot/rust/deploy/run-steam-bot.sh`; `Deadlock-Turniere/scripts/run_turniere_backend_rust.sh`; `Website/scripts/run_builds_backend.sh`)

