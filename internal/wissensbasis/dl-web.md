# dl-web: Web-Prozess, OAuth und Broker-Anbindung

stand: 2026-09-19  
quelle: `Deadlock-Bots` Commit `bb03deb53b28a7266de83748c3b834bff9c9a205`

Interne Referenz für Support und Entwicklung. Sie beschreibt den Rust-Code, nicht die öffentliche Erreichbarkeit.

## Drei Server im Prozess

Der aktuelle `main` startet Tierlist, Public Stats und Master Dashboard.

- Tierlist wird ab `Deadlock-Bots/rust/bin/dl-web/src/main.rs:28-50` aufgebaut. Der Kommentar nennt `:8771`.
- Public Stats wird in `Deadlock-Bots/rust/bin/dl-web/src/main.rs:53-60` aufgebaut. Der Kommentar nennt `:8768`.
- Master Dashboard wird in `Deadlock-Bots/rust/bin/dl-web/src/main.rs:62-80` aufgebaut. Der Kommentar nennt `:8766`.

Die tatsächlichen Ports kommen aus `dl_core::Config`. Die Kommentare sind deshalb keine Live-Portprüfung.

Die drei Server laufen im gemeinsamen `tokio::select!`, `Deadlock-Bots/rust/bin/dl-web/src/main.rs:82-88`.

Der Dateikopf bezeichnet Public Stats und Dashboard noch als folgende Arbeit, `Deadlock-Bots/rust/bin/dl-web/src/main.rs:1-6`. Das ausführbare `main` darunter startet beide bereits. Für den aktuellen Ist-Stand ist der ausgeführte Code maßgeblich.

## Gemeinsame Web-Konfiguration

`WebConfig` beginnt in `Deadlock-Bots/rust/crates/dl-webcore/src/config.rs:6-30`.

Die interne Dashboard-Basis fällt auf `http://127.0.0.1:8766` zurück, `Deadlock-Bots/rust/crates/dl-webcore/src/config.rs:76-77`. Public Stats bindet standardmäßig an Loopback, `Deadlock-Bots/rust/crates/dl-webcore/src/config.rs:86`.

`DL_TIERLIST_REFRESH` wird mit Default `true` ausgewertet, `Deadlock-Bots/rust/crates/dl-webcore/src/config.rs:89`. Der Prozess startet den Refresh-Loop nur bei aktivem Wert, `Deadlock-Bots/rust/bin/dl-web/src/main.rs:40-45`.

## Dashboard und OAuth

`DashboardConfig` beginnt in `Deadlock-Bots/rust/crates/dl-dashboard/src/config.rs:51-82`. Die Broker-Basis fällt auf `http://127.0.0.1:8770` zurück, Konstante in `Deadlock-Bots/rust/crates/dl-dashboard/src/config.rs:30` und Zuweisung in `Deadlock-Bots/rust/crates/dl-dashboard/src/config.rs:152-153`.

Der Dashboard-Router beginnt in `Deadlock-Bots/rust/crates/dl-dashboard/src/web.rs:316-324`. Dort liegen unter anderem `/auth/discord/login`, `/auth/discord/callback` und `/callback/discord`. Weitere interne OAuth- und Session-Routen folgen direkt danach.

Der Session-Cookie heißt `master_dash_session`, `Deadlock-Bots/rust/crates/dl-dashboard/src/web.rs:37-40`.

## Login-Broker

`dl-web` besitzt in dieser Schicht keinen eigenen Discord-Gateway-Cache. Die Zugriffsprüfung wird über `BrokerMemberLookup` gelöst, Typ in `Deadlock-Bots/rust/crates/dl-dashboard/src/authority.rs:88-105`.

Der Lookup ruft den Broker-Endpunkt `/internal/master/v1/discord/member-access` auf, `Deadlock-Bots/rust/crates/dl-dashboard/src/authority.rs:109-126`.

Die lokale Zugriffsentscheidung liegt in `decide_access`, `Deadlock-Bots/rust/crates/dl-dashboard/src/authority.rs:58-83`. Sie unterscheidet Owner, Admin-Berechtigung, Moderator-Rolle und zusätzliche Dashboard-Zugriffsrollen.

## Auth bleibt geschlossen

`DashboardConfig::auth_enforced` liefert im untersuchten Code `true`, `Deadlock-Bots/rust/crates/dl-dashboard/src/config.rs:171-175`. Eine unvollständige OAuth-Konfiguration wird damit nicht zu einem offenen Dashboard.

Nicht geprüft wurden Caddy, DNS, TLS, Live-Listener, OAuth-Secrets und aktive Sessions.
