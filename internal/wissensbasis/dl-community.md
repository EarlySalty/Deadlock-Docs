# dl-community: Onboarding, Patenschaften und Datenschutz

stand: 2026-09-19
quelle: `Deadlock-Bots` Commit `bb03deb53b28a7266de83748c3b834bff9c9a205`

Interne Referenz für Support und Entwicklung. Sie trennt aktuellen Code von verbliebenem Legacy-Schema.

## Onboarding

`Deadlock-Bots/rust/crates/dl-community/src/onboarding.rs:1-5` hält fest, dass der alte Wizard, die AI-Tour und die Welcome-DM-Flows entfernt sind. Der Einstieg läuft über Discords natives Onboarding. Gemeinsame Guild- und Rollen-IDs beginnen in `Deadlock-Bots/rust/crates/dl-community/src/onboarding.rs:8-18`.

Der Concierge verarbeitet ein abgeschlossenes natives Onboarding über `handle_native_onboarding_completed`, `Deadlock-Bots/rust/crates/dl-community/src/concierge.rs:3359-3367`.

## Alter Verify-Bestand

Die Tabelle `bot.onboarding_pending_verify` existiert weiterhin im DB-Schema, `Deadlock-Bots/rust/crates/dl-central-db/migrations/0007_bot.sql:176-181`. Das Privacy-Inventar führt sie weiterhin als löschbaren Altbestand, `Deadlock-Bots/rust/crates/dl-community/src/privacy.rs:625-630`.

Im aktuellen `onboarding.rs` ist kein aktiver Verify-Workflow implementiert. Die vorhandene Tabelle ist deshalb kein Beleg für einen heute aktiven Verify-Ablauf.

## Patenschaften

Die Patenschaftslogik liegt im Concierge.

- Patenrolle und Anfragekanal sind als Konstanten in `Deadlock-Bots/rust/crates/dl-community/src/concierge.rs:66-67` definiert.
- `request_pate` beginnt in `Deadlock-Bots/rust/crates/dl-community/src/concierge.rs:5450-5457`.
- `claim_pate` prüft unter anderem Guild und Anfragekanal, `Deadlock-Bots/rust/crates/dl-community/src/concierge.rs:5707-5713`.
- Der Store zählt aktive Patenschaften über `active_patenschaft_count`, `Deadlock-Bots/rust/crates/dl-community/src/concierge.rs:2589-2597`.
- Neue Patenschaften werden über `create_patenschaft` transaktional vorbereitet, `Deadlock-Bots/rust/crates/dl-community/src/concierge.rs:2600-2616`.

Zeitabhängige Concierge-Arbeit wird über `run_scheduler` angestoßen, `Deadlock-Bots/rust/crates/dl-community/src/concierge.rs:4849-4860`. Diese Fundstelle belegt den Scheduler, nicht eine bestimmte Live-Taktung.

## Privacy, Export und Löschen

Die sichtbare Privacy-Oberfläche registriert ihre Commands und Components in `Deadlock-Bots/rust/crates/dl-community/src/privacy_ui.rs:151-194`.

Die drei Kernaktionen sind:

| Aktion | Beleg |
|---|---|
| Opt-in | `Deadlock-Bots/rust/crates/dl-community/src/privacy.rs:3700-3720` |
| Löschen | `Deadlock-Bots/rust/crates/dl-community/src/privacy.rs:3723-3745` |
| Export | `Deadlock-Bots/rust/crates/dl-community/src/privacy.rs:3994-4005` |

Die UI ruft diese Funktionen direkt auf: Opt-in in `Deadlock-Bots/rust/crates/dl-community/src/privacy_ui.rs:78-83`, Löschung in `Deadlock-Bots/rust/crates/dl-community/src/privacy_ui.rs:85-90` und Export in `Deadlock-Bots/rust/crates/dl-community/src/privacy_ui.rs:114-120`.

Der zentrale transaktionsgebundene Privacy-Lock liegt in `Deadlock-Bots/rust/crates/dl-central-db/src/locks.rs:19-28`. Die kombinierte Sperre plus Tombstone-Prüfung liegt in `Deadlock-Bots/rust/crates/dl-central-db/src/locks.rs:31-45`.

## Voice-Router gehört zu dl-voice

Der ältere Paketplan nennt den Voice-Router im Community-Baustein. Im aktuellen Quellstand liegt die Implementierung in `dl-voice`.

- Auto-Move-Entscheidung: `Deadlock-Bots/rust/crates/dl-voice/src/router.rs:338-356`
- `LaneRouter`: `Deadlock-Bots/rust/crates/dl-voice/src/router.rs:889-897`
- Fallback-Lane plus Onboarding-Hinweis: `Deadlock-Bots/rust/crates/dl-voice/src/router.rs:1040-1051`
- Interaction-Registrierung: `Deadlock-Bots/rust/crates/dl-voice/src/router.rs:1905-1909`

Für Support und Doku ist die Trennung daher: Onboarding, Concierge, Patenschaften und Privacy in `dl-community`; Voice-Routing in `dl-voice`; Verdrahtung in `dl-bot`.

Nicht geprüft wurden Live-Rollen, Kanalexistenz, produktive Tabelleninhalte und laufende Scheduler-Zyklen.
