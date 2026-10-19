# dl-bot: Prozesskern, Discord-Ereignisse und Interaktionen

stand: 2026-09-19
quelle: `Deadlock-Bots` Commit `bb03deb53b28a7266de83748c3b834bff9c9a205`

Interne Referenz für Support und Entwicklung. Sie beschreibt den gelesenen Quellstand, nicht den Live-Zustand eines Dienstes.

## Rolle des Prozesses

`dl-bot` ist der Integrationsprozess des Community-Bots. Der Einstieg liegt in `Deadlock-Bots/rust/bin/dl-bot/src/main.rs:469-474`. Dort beginnt der Aufbau von Konfiguration und Runtime.

Der gemeinsame Interaction-Router wird in `Deadlock-Bots/rust/bin/dl-bot/src/main.rs:535` angelegt. Fachmodule registrieren ihre Handler anschließend an diesem Router. Beispiele sind der Voice-Router in `Deadlock-Bots/rust/bin/dl-bot/src/main.rs:803`, FAQ in `Deadlock-Bots/rust/bin/dl-bot/src/main.rs:1068`, Concierge in `Deadlock-Bots/rust/bin/dl-bot/src/main.rs:1095` und Privacy in `Deadlock-Bots/rust/bin/dl-bot/src/main.rs:1098`.

## Interaction-Router

Der Router-Typ liegt in `Deadlock-Bots/rust/crates/dl-discord/src/interactions.rs:233-237`. Er hält getrennte Routen für Components und Commands.

Die drei zentralen Registrierungsarten sind:

| Symbol | Beleg | Zweck |
|---|---|---|
| `on_custom_id` | `Deadlock-Bots/rust/crates/dl-discord/src/interactions.rs:245-247` | exakte Component-ID |
| `on_prefix` | `Deadlock-Bots/rust/crates/dl-discord/src/interactions.rs:251-253` | Component-ID-Präfix |
| `on_command` | `Deadlock-Bots/rust/crates/dl-discord/src/interactions.rs:257-262` | Slash-Command |

## Weg einer Discord-Interaktion

Serenity ruft `Handler::interaction_create` auf. Der Handler publiziert zuerst das normalisierte Interaction-Ereignis und ruft danach den zentralen Dispatcher auf. Das ist in `Deadlock-Bots/rust/crates/dl-discord/src/gateway.rs:315-323` belegt.

`dispatch` unterscheidet Command, Component und Modal in `Deadlock-Bots/rust/crates/dl-discord/src/dispatch.rs:47-56`. Damit müssen Fachmodule den Discord-Transport nicht jeweils selbst implementieren.

## Gateway und Prozesslebensdauer

Der Gateway-Pfad wird in `Deadlock-Bots/rust/bin/dl-bot/src/main.rs:1361-1363` über `DL_BOT_GATEWAY` entschieden. Im untersuchten Stand aktiviert der exakte Wert `1` diesen Pfad.

Der Serenity-Client wird über `dl_discord::gateway::build_client` gebaut, Aufruf in `Deadlock-Bots/rust/bin/dl-bot/src/main.rs:1752-1757`. Die Client-Fabrik selbst beginnt in `Deadlock-Bots/rust/crates/dl-discord/src/gateway.rs:680-685`.

Die laufenden Server, der Gateway-Task und Shutdown-Signale werden in einem gemeinsamen `tokio::select!` koordiniert, `Deadlock-Bots/rust/bin/dl-bot/src/main.rs:1852-1896`.

## Panels gehören den Fachmodulen

Ein Panel ist im aktuellen Aufbau kein eigener zentraler Dienst. `dl-bot` registriert die Fachmodule, die eigentliche Logik lebt in der jeweiligen Crate.

Beispiele:

- Voice-Router: `Deadlock-Bots/rust/crates/dl-voice/src/router.rs:889-896`, Registrierung in `Deadlock-Bots/rust/crates/dl-voice/src/router.rs:1905-1908`.
- FAQ und Concierge werden aus `dl-community` in `main.rs` registriert, Belege oben.
- LFG-Panel und weitere Voice-Oberflächen liegen in `dl-voice`, nicht im Prozesskern.

## Support-Grenze

Ein erreichbarer interner HTTP-Endpunkt beweist nicht, dass der Discord-Gateway-Pfad aktiv ist. Gateway-Aktivierung und erfolgreicher Client-Start sind davon getrennt, siehe `Deadlock-Bots/rust/bin/dl-bot/src/main.rs:1361-1363` und `Deadlock-Bots/rust/bin/dl-bot/src/main.rs:1752-1757`.

Nicht geprüft wurden systemd-Konfiguration, Live-PID, Discord-Berechtigungen und externe Reverse-Proxy-Routen.
