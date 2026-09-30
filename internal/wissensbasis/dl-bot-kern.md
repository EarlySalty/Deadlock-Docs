# dl-bot: Prozesskern, Discord-Ereignisse und Interaktionen

Interne Referenz für Support und Entwicklung. Beschrieben ist der Quellstand von `Deadlock-Bots` am Commit `bb03deb53b28a7266de83748c3b834bff9c9a205`. Die Seite dokumentiert den Code. Sie ist kein Nachweis für den aktuellen Laufzeitstatus eines Dienstes.

## 1. Aufgabe des Binärprogramms

`dl-bot` ist der Integrationsprozess, der die Community-Crates verdrahtet. Der Einstieg liegt in `Deadlock-Bots/rust/bin/dl-bot/src/main.rs`, Symbol `main`. Dort werden zentrale Datenbank, Community-Komponenten, Discord-Adapter, Interaction-Router, interne HTTP-Dienste und Hintergrundaufgaben aufgebaut.

Der Prozess besitzt zwei unterschiedliche Ebenen:

1. `dl-bot` entscheidet, welche Komponenten instanziiert und registriert werden.
2. `dl-discord` übernimmt die generische Discord-Anbindung und die Verteilung eingehender Interaktionen.

Damit gehört ein Panel fachlich meist zur jeweiligen Feature-Crate. Der Prozesskern registriert dessen Routen, ist aber nicht automatisch Eigentümer der Fachlogik.

## 2. Interaction-Router

In `Deadlock-Bots/rust/bin/dl-bot/src/main.rs` wird ein `dl_discord::InteractionRouter` aufgebaut. Die Router-Implementierung liegt in `Deadlock-Bots/rust/crates/dl-discord/src/interactions.rs`, Typ `InteractionRouter`.

Relevante Registrierungsfunktionen:

| Symbol | Zweck |
|---|---|
| `InteractionRouter::on_custom_id` | exakte Component-ID registrieren |
| `InteractionRouter::on_prefix` | Component-ID-Präfix registrieren |
| `InteractionRouter::on_command` | Slash-Command registrieren |

`main` ruft die `register`-Funktionen der Features auf. Am untersuchten Stand gehören dazu unter anderem Steam, Scrim-Anmeldung, Matcher, Streamer-Intent, Voice-Nudges, Solo-Watch, Voice-Router, Pairing, LFG, Voice-Feedback, Survey, Tags, Coaching, Team-Bewerbungen, FAQ, Concierge, Privacy, Feedback-Hub, Clips, Austrittsumfrage und Retention. Die maßgebliche Fundstelle ist die Router-Aufbauphase in `Deadlock-Bots/rust/bin/dl-bot/src/main.rs`.

## 3. Weg eines Discord-Ereignisses

Der Gateway-Adapter liegt in `Deadlock-Bots/rust/crates/dl-discord/src/gateway.rs`.

Bei einer Interaktion läuft der relevante Pfad so:

1. Serenity ruft `Handler::interaction_create` auf.
2. Der Handler normalisiert beziehungsweise veröffentlicht das Interaction-Ereignis für die gemeinsame Event-Schicht.
3. Danach ruft er `dl_discord::dispatch::dispatch` auf.
4. `dispatch` in `Deadlock-Bots/rust/crates/dl-discord/src/dispatch.rs` unterscheidet Command, Component und Modal.
5. Der Interaction-Router liefert den registrierten Feature-Handler.

Die Discord-Callback-Typen für normale Antwort, Deferred-Antwort, Component-Update und Modal sind in `dispatch.rs` zentral definiert. Feature-Code muss diese Transportdetails dadurch nicht separat nachbauen.

## 4. Gateway-Schalter und Prozesslebensdauer

Der Gateway-Start ist in `Deadlock-Bots/rust/bin/dl-bot/src/main.rs` an `DL_BOT_GATEWAY` gebunden. Im untersuchten Code aktiviert der exakte Wert `1` den Gateway-Pfad. Ohne diesen Wert wird kein Gateway-Task angelegt.

Bei aktivem Gateway baut `dl_discord::gateway::build_client` den Hauptclient. Zusätzlich wird ein Voice-Worker-Client gestartet. Beide laufen innerhalb des Gateway-Tasks. Die eigentliche Dienstlebensdauer wird in `main` über `tokio::select!` koordiniert. Dort konkurrieren unter anderem interne Server, Gateway, Kontrollpfad, `Ctrl+C` und `SIGTERM`.

Beim Verlassen des Select-Pfads fährt `main` registrierte Hintergrundarbeit herunter und bricht den Gateway-Task ab. Die Details des Systemdienstes oder eines externen Supervisors liegen außerhalb dieser Datei.

## 5. Panels sind verteilte Fachmodule

Ein sichtbares Panel ist im heutigen Aufbau kein eigener zentraler Panel-Dienst. Die Registrierungen liegen in den jeweiligen Crates und werden im Prozesskern zusammengeführt.

Beispiele:

| Bereich | Eigentümer im Code | Registrierung |
|---|---|---|
| Voice-Router | `Deadlock-Bots/rust/crates/dl-voice/src/router.rs` | `dl_voice::router::register` in `dl-bot/main.rs` |
| FAQ | `Deadlock-Bots/rust/crates/dl-community/src/faq.rs` | Registrierung in `dl-bot/main.rs` |
| Privacy | `Deadlock-Bots/rust/crates/dl-community/src/privacy_ui.rs` | `privacy_ui::register` |
| LFG | `Deadlock-Bots/rust/crates/dl-community/src/lfg_panel.rs` | Registrierung in `dl-bot/main.rs` |
| Coaching | `Deadlock-Bots/rust/crates/dl-community/src/coaching_requests.rs` | Registrierung in `dl-bot/main.rs` |

Für Änderungen an einem Panel ist deshalb zuerst der registrierte Feature-Handler zu bestimmen. `main.rs` beantwortet die Verdrahtungsfrage, die Feature-Datei die Fachfrage.

## 6. Interne Dienste im selben Prozess

`main` startet neben Discord mehrere lokale Server und Worker. Dazu gehört unter anderem der interne Broker-Pfad. Die konkrete Zusammensetzung kann sich ändern und wird deshalb über die Symbole in `main.rs` verfolgt, nicht als feste Dienstliste behandelt.

Wichtig für Supportfragen: Ein gesunder HTTP-Endpunkt beweist nicht, dass der Discord-Gateway-Pfad aktiv ist. Der Gateway hängt zusätzlich am Schalter `DL_BOT_GATEWAY` und am erfolgreichen Client-Start.

## 7. Quellreferenzen

| Thema | Datei und Symbol |
|---|---|
| Prozessaufbau, Router-Registrierung, Gateway-Schalter, Haupt-Select | `Deadlock-Bots/rust/bin/dl-bot/src/main.rs`, `main` |
| Router-Datentyp und Registrierungsarten | `Deadlock-Bots/rust/crates/dl-discord/src/interactions.rs`, `InteractionRouter` |
| Discord EventHandler und Clientbau | `Deadlock-Bots/rust/crates/dl-discord/src/gateway.rs`, `Handler::interaction_create`, `build_client` |
| Command-, Component- und Modal-Verteilung | `Deadlock-Bots/rust/crates/dl-discord/src/dispatch.rs`, `dispatch` |
| Voice-Router als Fachmodul | `Deadlock-Bots/rust/crates/dl-voice/src/router.rs`, `LaneRouter`, `register` |

## 8. Grenzen dieser Referenz

Nicht geprüft wurden systemd-Konfiguration, aktuelle Prozess-ID, Live-Gateway-Verbindung, Discord-Berechtigungen und externe Reverse-Proxy-Routen. Diese Seite beschreibt die statische Verdrahtung am genannten Commit.
