---
title: "Turniere — Datenmodell"
tags: [internal, deadlock-turniere, datenmodell]
stand: 2026-07-10
quelle: Deadlock-Turniere
---
# Turniere — Datenmodell

Rust nutzt die zentrale Postgres-DB aus `DEADLOCK_CENTRAL_DSN`. Die produktiven Tabellen werden im Schema `turnier.*` angesprochen; lokale Dateidatenbanken sind nicht der Fachdatenpfad. Produktive Migrationen laufen außerhalb des Turnier-Dienstes, denn `turnier_db::run_migrations()` ist ein No-op. (`rust/crates/turnier-db/src/pool.rs`, `rust/crates/turnier-config/src/lib.rs`)

## Zugriff

`connect_central()` liest die DSN über `dl_central_db::dsn_from_env()` und baut daraus einen `PgPool`. Der Pool wird in `AppState` gehalten und an API, Scheduler, MatchManager, DiscordNotifier und RankResolver weitergereicht. (`rust/crates/turnier-db/src/pool.rs`, `rust/crates/turnier-api/src/state.rs`)

Rust-Queries sind schemaqualifiziert. Beispiele sind `turnier.tournaments`, `turnier.teams`, `turnier.team_members`, `turnier.bracket_matches`, `turnier.group_matches`, `turnier.sessions`, `turnier.rank_cache` und `turnier.tournament_presets`. (`rust/crates/turnier-api/src/public/teams.rs`, `rust/crates/turnier-match/src/repo.rs`, `rust/crates/turnier-auth/src/session.rs`)

## Turniere und Teams

`turnier.tournaments` trägt den Turnierstatus, Modus, Teamgröße, Zeitfenster, Serienformat, Spielmodus, Auto-Lobby-Flag, Test-Flag, Reminder-Offsets und Lobby-Settings. Status- und Moduswerte sind in `turnier-core` als String-Enums modelliert. (`rust/crates/turnier-core/src/enums.rs`, `rust/crates/turnier-api/src/admin/tournaments.rs`)

Der Modus ist `bracket_only` oder `group_stage`. `determine_tournament_mode` schaltet ab **≥ 16 Teams** automatisch auf `group_stage`, darunter bleibt `bracket_only`; ein Admin-Override erzwingt beides. Diese Schwelle ist in der public-Doku bewusst nur als „größere Turniere → Gruppenphase" umschrieben. (`rust/crates/turnier-engine/src/status.rs`, `rust/crates/turnier-core/src/tournament.rs`)

Teams liegen in `turnier.teams`, Mitglieder in `turnier.team_members`, Solo-Anmeldungen in `turnier.tournament_signups`. Team-Erstellen, Team-Beitritt, 1vs1-Autoteam und Check-in schreiben diese Tabellen in Transaktionen. (`rust/crates/turnier-api/src/public/teams.rs`, `rust/crates/turnier-api/src/public/signups.rs`)

Gruppen bestehen aus `turnier.groups`, `turnier.group_teams` und `turnier.group_matches`. Die Engine erzeugt Gruppen per Snake-Draft, legt `group_teams` mit `wins=0`, `losses=0`, `points=0` an und erzeugt Round-Robin-`group_matches`. (`rust/crates/turnier-engine/src/persist/groups.rs`)

## Matches, Serien und Draft

Bracket-Daten liegen in `turnier.bracket_matches`, `turnier.bracket_mini_groups` und `turnier.bracket_mini_group_teams`. Der Match-Repo-Code liest Bracket- und Group-Matches über zwei feste Query-Zweige und schreibt Lobby-Daten scope-gebunden zurück. (`rust/crates/turnier-match/src/repo.rs`)

Nach Lobby-Erstellung schreibt Rust `steam_party_id`, `party_code`, `status='lobby_created'` und optional `hero_assignments`. Nach Match-Start setzt Rust `status='in_progress'` und übernimmt optional `deadlock_match_id`. (`rust/crates/turnier-match/src/lobby.rs`, `rust/crates/turnier-match/src/repo.rs`)

Serien liegen in `turnier.match_games`. `record_game_result()` erzeugt fehlende Spiele idempotent, schreibt Gewinner, Steam-/Deadlock-IDs, Dauer und Stats und entscheidet die Serie über `wins_needed = series_format / 2 + 1`. (`rust/crates/turnier-match/src/series.rs`)

Drafts liegen in `turnier.draft_sessions` und `turnier.draft_actions`. `start_draft()` legt eine Session und die Standard-Aktionssequenz an; `take_action()` läuft in einer Postgres-Transaktion mit Compare-and-Swap auf `current_action_index`. (`rust/crates/turnier-draft/src/repo.rs`, `rust/crates/turnier-draft/src/state.rs`)

## Ergebnisse und Punkte

Bracket-Ergebnisse setzen `turnier.bracket_matches.status='completed'`, schreiben `turnier.match_results`, propagieren Gewinner in Folge-Matches, schließen Mini-Groups bei Bedarf ab und planen Folge-Lobbys best-effort. (`rust/crates/turnier-match/src/result.rs`)

Group-Ergebnisse setzen `turnier.group_matches.status='completed'`, schreiben Gewinner, Dauer, Stats und `match_results`, erhöhen beim Gewinner `wins` und `points` um 3 und beim Verlierer `losses`. (`rust/crates/turnier-match/src/result.rs`)

Eine bestehende Datenfalle bleibt erhalten: im Bracket-Pfad steht in `match_results.winning_team` die Gewinner-Team-ID, im Group-Pfad der Slot `1` oder `2`. Das ist im Rust-Code ausdrücklich als `needs-decision` markiert und nicht vereinheitlicht. (`rust/crates/turnier-match/src/result.rs`)

## Auth, Profile und Automatik

Sessions liegen in `turnier.sessions` als opake Tokens mit sieben Tagen Laufzeit. Rollen werden als CSV gespeichert, beim Request gelesen und gegen die beim Start materialisierten RoleSets ausgewertet. (`rust/crates/turnier-auth/src/session.rs`, `rust/crates/turnier-auth/src/roles.rs`, `rust/crates/turnier-api/src/extract.rs`)

Profile, Consent, Avatare und Benachrichtigungsschalter liegen in `turnier.user_profiles` und `turnier.user_consents`. Die Consent/Profile-Routen lesen und schreiben diese Tabellen über den gemeinsamen Pool. (`rust/crates/turnier-api/src/consent.rs`)

Rangdaten liegen in `turnier.rank_cache` (L2-Cache, TTL 24 h). Der Resolver liest zuerst L1/L2-Cache, dann die externe Steam-Bridge-SQLite (`steam_links`, bevorzugt der Primary-Account) und danach als REST-Fallback die Discord-Rang-Rollen; Treffer aus Bridge oder Rollen werden wieder in `rank_cache` gespeichert. (`rust/crates/turnier-steam/src/resolver.rs`, `rust/crates/turnier-steam/src/cache.rs`)

Turnier-Automatik nutzt `turnier.tournament_presets`, `turnier.tournament_proposals`, `turnier.tournament_proposal_votes`, `turnier.tournament_proposal_feedback`, `turnier.tournament_dm_optout` und `turnier.tournament_signals`. Presets speichern wiederverwendbare Konfiguration, Proposals speichern Vorschläge und Votes, Opt-out unterdrückt Kategorie-DMs. (`rust/crates/turnier-automatik/src/presets.rs`, `rust/crates/turnier-automatik/src/proposals.rs`, `rust/crates/turnier-automatik/src/optout.rs`)
