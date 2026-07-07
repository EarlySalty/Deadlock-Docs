---
title: "Turniere — Match-Automatik"
tags: [internal, deadlock-turniere, match-automatik]
stand: 2026-07-07
quelle: Deadlock-Turniere
---
# Turniere — Match-Automatik

Die Automatik läuft im Rust-Prozess. `turnier-bot` startet den Scheduler als Hintergrund-Task; der Scheduler prüft Phasen, Reminder und offene Matches. Match-Lobbys werden vom `MatchManager` erstellt und über Steam-Bridge plus Discord-Broker begleitet. (`rust/crates/turnier-bot/src/main.rs`, `rust/crates/turnier-scheduler/src/loop_runner.rs`, `rust/crates/turnier-match/src/lib.rs`)

## Scheduler

Der Scheduler läuft einmal sofort und danach alle 60 Sekunden. Pro Tick ruft er vier Checks auf: Phasen-Kaskade, Registrierungs-Reminder, Start-Reminder und Match-Reminder; Fehler in einem Check beenden weder die anderen Checks noch den Loop. (`rust/crates/turnier-scheduler/src/loop_runner.rs`)

Die Statuskette ist `draft -> registration -> checkin -> group_phase -> bracket -> completed -> archived`. `valid_next_statuses()` und `is_valid_transition()` definieren die erlaubten Übergänge. (`rust/crates/turnier-engine/src/status.rs`, `rust/crates/turnier-core/src/enums.rs`)

Fällige Wechsel hängen an `registration_start`, `registration_end` oder `checkin_start`, `group_phase_start` und `bracket_start`. Bei `tournament_mode == "bracket_only"` überspringt Rust `group_phase`, wechselt aber erst nach `bracket`, wenn auch `bracket_start` fällig ist. (`rust/crates/turnier-scheduler/src/transition.rs`)

`advance_tournament_status()` ist die gemeinsame Mutation für Scheduler und Admin-Routen. Sie validiert den Übergang, schreibt den Status per Optimistic Lock, generiert bei `group_phase` Gruppen und Gruppenmatches, generiert bei `bracket` das Bracket, schreibt Audit-Log und plant Auto-Lobbys best-effort. (`rust/crates/turnier-scheduler/src/transition.rs`)

## Auto-Lobby

Auto-Lobby ist pro Turnier über `auto_lobby_enabled` und `is_test` gegated. Der Code wählt Bracket- und Group-Matches mit beiden Teams, Status `pending` oder `checkin` und ohne `steam_party_id`. (`rust/crates/turnier-match/src/auto_lobby.rs`)

Für Bracket-Matches ruft Auto-Lobby `create_lobby()`, für Group-Matches `create_group_lobby()`. Fehler pro Match werden geloggt und brechen die restliche Planung nicht ab. (`rust/crates/turnier-match/src/auto_lobby.rs`, `rust/crates/turnier-match/src/lobby.rs`)

Lobby-Erstellung prüft den Match-Status, verhindert doppelte Lobby-Anfragen, lädt Lobby-Settings, Teilnehmer und Spielmodus-Payload und sendet `GC_CREATE_CUSTOM_LOBBY` an die Steam-Bridge. Nach Erfolg schreibt Rust `steam_party_id`, `party_code`, `status='lobby_created'` und optional `hero_assignments`. (`rust/crates/turnier-match/src/lobby.rs`, `rust/crates/turnier-match/src/repo.rs`)

Nach Lobby-Erstellung lädt Rust Teilnehmer per `GC_LOBBY_INVITE_PLAYER` ein. Für Nicht-Test-Turniere erstellt der Notifier einen Match-Channel, sendet Lobby-Info, benachrichtigt Caster und postet das Lobby-Announcement. (`rust/crates/turnier-match/src/lobby.rs`, `rust/crates/turnier-discord/src/notifier.rs`)

## Ergebnisse

Ein Bracket-Ergebnis setzt das Match auf `completed`, löscht alte Result-Zeilen, schreibt `match_results`, propagiert den Gewinner, schließt Mini-Groups bei Bedarf ab und plant Folge-Lobbys. Discord-Stats und Channel-Cleanup laufen best-effort. (`rust/crates/turnier-match/src/result.rs`)

Ein Group-Ergebnis setzt `group_matches.status='completed'`, schreibt Gewinner, Dauer, Stats und `match_results`, erhöht beim Gewinner `wins` und `points` um 3 und erhöht beim Verlierer `losses`. (`rust/crates/turnier-match/src/result.rs`)

Serien für Bracket-Matches liegen in `match_games`. `record_game_result()` stellt das Spiel sicher, schreibt das Ergebnis und entscheidet die Serie über `series_format` oder `final_series_format`. (`rust/crates/turnier-match/src/series.rs`)

## Reminder und Automatik

Registrierungs-Reminder gehen an Profile mit passendem Benachrichtigungsschalter, Start-Reminder an Turnierteilnehmer, Match-Reminder an Teammitglieder offener Bracket-Matches. Dedupe läuft über `sent_tournament_reminders`, `sent_start_reminders` und `sent_match_reminders`. (`rust/crates/turnier-scheduler/src/reminders.rs`)

Turnier-Presets speichern Kategorie `fun` oder `comp`, Teamgröße, Bracket-Format, Serienformat, Turniermodus, Spielmodus, Objective, Invite-Modus, Reminder-Offsets, Regeln und Beschreibungstemplate. Die Admin-API hängt sie unter `/api/admin/presets` ein. (`rust/crates/turnier-automatik/src/presets.rs`, `rust/crates/turnier-api/src/admin/automatik.rs`)

Proposals haben die Zustände `draft`, `pending_approval`, `approved`, `rejected` und `expired`. Die State-Machine erlaubt Submit, Approve, Reject, Expire und Feedback; Approve verlangt mindestens einen Approve-Vote. (`rust/crates/turnier-automatik/src/proposals.rs`)

Votes und Approve-Events verlangen die Caster-Rolle aus `DISCORD_CASTER_ROLE_ID`. Beim Vote speichert Rust die eingeloggte Actor-ID und auditiert zusätzlich die angefragte `caster_id`. (`rust/crates/turnier-api/src/admin/automatik.rs`)

DM-Opt-out speichert Scope `fun`, `comp` oder `all`. `all` unterdrückt beide Kategorien, und die Empfängerberechnung nimmt Rollenmitglieder minus passende Opt-outs bei erhaltener Reihenfolge. (`rust/crates/turnier-automatik/src/optout.rs`)
