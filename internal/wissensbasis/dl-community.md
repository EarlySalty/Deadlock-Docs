# dl-community: Onboarding, Patenschaften und Datenschutz

Interne Referenz für Support und Entwicklung. Beschrieben ist `Deadlock-Bots` am Commit `bb03deb53b28a7266de83748c3b834bff9c9a205`. Die Seite trennt aktuellen Code von verbliebenem Legacy-Schema.

## 1. Aktueller Onboarding-Stand

Die Datei `Deadlock-Bots/rust/crates/dl-community/src/onboarding.rs` ist heute eine kleine Sammlung gemeinsamer Guild- und Rollen-IDs. Ihr Modulkommentar hält fest, dass der alte Wizard, die AI-Tour und die Welcome-DM-Flows entfernt sind. Der Zugang läuft über Discords natives Onboarding. Der Concierge beantwortet anschließende Fragen.

Wichtige Konstanten sind `MAIN_GUILD_ID`, `RULES_CHANNEL_ID`, `ONBOARD_COMPLETE_ROLE_ID` sowie Rollen-IDs für Streamer, LFG, Custom Games, Patchnotes und Spielstil.

Ein abgeschlossenes natives Onboarding wird im Concierge weiterverarbeitet. Der relevante Einstieg liegt in `Deadlock-Bots/rust/crates/dl-community/src/concierge.rs`, Symbol `handle_native_onboarding_completed`. Der Bot verbindet das Discord-Rollenereignis zusätzlich mit der Journey-Schicht in `Deadlock-Bots/rust/bin/dl-bot/src/journeyglue.rs`.

## 2. Status des alten Verify-Pfads

Im aktuellen `dl-community` existiert kein aktives Verify-Modul neben `onboarding.rs`. Die Tabelle `bot.onboarding_pending_verify` ist weiterhin im Datenbankschema vorhanden und wird im Privacy-Inventar berücksichtigt.

Fundstellen:

* Schema: `Deadlock-Bots/rust/crates/dl-central-db/migrations/0007_bot.sql`
* Löschinventar: `Deadlock-Bots/rust/crates/dl-community/src/privacy.rs`, `TABLE_SPECS`

Damit belegt die vorhandene Tabelle keinen aktuellen Verifikations-Workflow. Für Supportdokumentation ist der native Discord-Onboarding-Pfad maßgeblich.

## 3. Patenschaften

Die Patenschaftslogik liegt im Concierge.

### Anfrage

`request_pate` in `Deadlock-Bots/rust/crates/dl-community/src/concierge.rs` baut die Anfrage für den vorgesehenen Patenkanal. Die Datei definiert dafür unter anderem `PATE_ROLE_ID` und `PATE_REQUEST_CHANNEL_ID`.

### Übernahme

`claim_pate` prüft den Kontext der Übernahme, arbeitet mit dem Privacy-Lock und legt die Patenschaft transaktional an. Die Persistenz liegt in `bot.concierge_patenschaften`. Der Store bietet dafür unter anderem `create_patenschaft` und `active_patenschaft_count`.

### Scheduler

`run_scheduler` verarbeitet zeitabhängige Concierge-Aufgaben. Patenschaftszustände und ihre Sicherheit hängen nicht allein an Discord-Nachrichten, sondern zusätzlich an den persistenten Datensätzen und den Privacy-Sperren im Concierge.

## 4. Privacy und Löschen

Die Datenschutzlogik ist in `Deadlock-Bots/rust/crates/dl-community/src/privacy.rs` gebündelt.

Wichtige Symbole:

| Symbol | Aufgabe |
|---|---|
| `export_user_data` | personenbezogene, dem Nutzer zugeordnete Daten für den Export sammeln |
| `delete_user_data` | Löschpfad über registrierte Tabellen und weitere nutzerbezogene Speicher |
| `lock_user_privacy` | dl-community Wrapper für die zentrale Privacy-Sperre |
| `set_opt_in` | Opt-in beziehungsweise Opt-out Zustand unter Lock aktualisieren |
| `TABLE_SPECS` | Tabelleninventar für Export und Löschung |

Die Datei beschreibt im Kopf den Erasure-Ansatz: nutzerbezogene Zeilen werden aus den erfassten Tabellen entfernt, Steam-bezogene Daten werden über die verknüpfte Steam-ID einbezogen und in `core.user_privacy` bleibt ein Privacy-Tombstone zurück. Die Transaktionssperre kommt aus `Deadlock-Bots/rust/crates/dl-central-db/src/locks.rs`, Symbol `lock_user_privacy`.

Die sichtbaren Discord-Aktionen liegen in `Deadlock-Bots/rust/crates/dl-community/src/privacy_ui.rs`. `register` bindet die Datenschutz-Kommandos und Component-Aktionen an den Interaction-Router. Die Handler rufen `export_user_data`, `delete_user_data` und `set_opt_in` auf.

## 5. Voice-Router gehört zu dl-voice

Der ältere Paketplan ordnete den Voice-Router dem Community-Paket zu. Im aktuellen Quellstand liegt die Implementierung in `Deadlock-Bots/rust/crates/dl-voice/src/router.rs`.

Relevante Symbole sind `LaneRouter`, `decide_auto_move`, `spawn_fallback_lane_and_onboard` und `register`. `dl-bot` bindet dieses Modul in den gemeinsamen Interaction-Router ein.

Für die Wissensbasis gilt:

* `dl-community` dokumentiert Onboarding, Concierge, Patenschaften und Privacy.
* `dl-voice` dokumentiert die Voice-Router-Entscheidung und die Voice-Interaktionen.
* `dl-bot` dokumentiert die Verdrahtung beider Bereiche.

## 6. Quellreferenzen

| Thema | Datei und Symbol |
|---|---|
| Native-Onboarding-Konstanten und Legacy-Hinweis | `Deadlock-Bots/rust/crates/dl-community/src/onboarding.rs` |
| Onboarding-Abschluss, Patenschaften, Scheduler | `Deadlock-Bots/rust/crates/dl-community/src/concierge.rs`, `handle_native_onboarding_completed`, `request_pate`, `claim_pate`, `run_scheduler` |
| Datenschutzkern | `Deadlock-Bots/rust/crates/dl-community/src/privacy.rs`, `export_user_data`, `delete_user_data`, `set_opt_in` |
| Datenschutz-UI | `Deadlock-Bots/rust/crates/dl-community/src/privacy_ui.rs`, `register` |
| Zentrale Privacy-Sperre | `Deadlock-Bots/rust/crates/dl-central-db/src/locks.rs`, `lock_user_privacy` |
| Voice-Router | `Deadlock-Bots/rust/crates/dl-voice/src/router.rs`, `LaneRouter`, `register` |
| Journey-Anbindung | `Deadlock-Bots/rust/bin/dl-bot/src/journeyglue.rs` |

## 7. Grenzen dieser Referenz

Nicht geprüft wurden Live-Rollen in Discord, aktuelle Kanalexistenz, konkrete laufende Scheduler-Zyklen und der Inhalt produktiver Patenschaftstabellen. Die Beschreibung bezieht sich auf den Code am genannten Commit.
