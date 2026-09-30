# dl-web: Web-Prozess, OAuth und Broker-Anbindung

Interne Referenz für Support und Entwicklung. Beschrieben ist `Deadlock-Bots` am Commit `bb03deb53b28a7266de83748c3b834bff9c9a205`. Die Seite beschreibt den aktuellen Rust-Code, nicht die Erreichbarkeit der öffentlichen Domains.

## 1. Prozessaufbau

Der Einstieg liegt in `Deadlock-Bots/rust/bin/dl-web/src/main.rs`, Symbol `main`.

Der Prozess baut am untersuchten Stand drei Axum-Server:

| Bereich | Port aus `dl_core::Config` | Bind-Host |
|---|---|---|
| Tierlist | `cfg.ports.tierlist_public` | `WebConfig::tierlist_host` |
| Public Stats | `cfg.ports.public_stats` | `WebConfig::stats_host` |
| Master Dashboard | `cfg.ports.dashboard` | `DASHBOARD_HOST`, Fallback `127.0.0.1` |

Die Kommentare im Einstieg nennen für die etablierte Portbelegung Tierlist `:8771`, Public Stats `:8768` und Master Dashboard `:8766`. Die numerischen Werte stammen letztlich aus `dl_core::Config` und sind deshalb kein eigenständiger Laufzeitbeweis.

Alle drei Server teilen denselben zentralen PostgreSQL-Pool. `tokio::select!` hält den Prozess aktiv und beendet ihn, wenn ein Serverpfad endet oder `Ctrl+C` eintrifft.

## 2. Gemeinsame Web-Konfiguration

`Deadlock-Bots/rust/crates/dl-webcore/src/config.rs`, Typ `WebConfig`, bündelt die Kompatibilitätskonfiguration für Stats und Tierlist.

Wichtige Felder:

* Session-Secret und Cookie-Sicherheitsflag
* CORS-Allowlist
* interne Dashboard-Basis-URL
* interne Relay-Token-Konfiguration
* Stats-Callback-URL
* Stats- und Tierlist-Bind-Hosts
* statisches Datenverzeichnis
* Schalter `DL_TIERLIST_REFRESH`

Der Standard für `dashboard_base` ist im Code `http://127.0.0.1:8766`. Der Standard für Stats- und Tierlist-Host ist `127.0.0.1`.

## 3. Master Dashboard ist OAuth-Besitzer

Die Dashboard-Schicht liegt in `Deadlock-Bots/rust/crates/dl-dashboard`.

`DashboardConfig` in `src/config.rs` enthält Discord-OAuth-Konfiguration, Session-TTL, erlaubte Origins, Zugriffsrollen, Broker-Basis und interne Tokenlisten. Der Standard für `broker_base` ist `http://127.0.0.1:8770`.

Der Router in `Deadlock-Bots/rust/crates/dl-dashboard/src/web.rs`, Symbol `router`, bindet unter anderem:

* `/auth/discord/login`
* `/auth/discord/callback`
* `/callback/discord`
* `/auth/logout`
* interne Initiate- und Consume-Routen für delegierte OAuth-Flows
* interne Discord-Session-Routen für Turnier-, Twitch- und Steam-Link-Pfade
* session-geschützte Analytics-Routen

Der eigene Session-Cookie heißt im Code `master_dash_session`.

## 4. Login-Broker

`dl-web` besitzt keine Discord-Gateway-Verbindung. Die Mitgliedsprüfung für den Dashboard-Login läuft deshalb über den Master-Broker.

Die zentrale Implementierung liegt in `Deadlock-Bots/rust/crates/dl-dashboard/src/authority.rs`.

* `BrokerMemberLookup` ruft `/internal/master/v1/discord/member-access` am konfigurierten Broker auf.
* `decide_access` entscheidet danach lokal über Owner, Discord-Admin-Berechtigung, Moderator-Rolle und zusätzliche Dashboard-Zugriffsrollen.
* Ein nicht erreichbarer Broker wird als fehlgeschlagener Lookup behandelt und nicht mit "Mitglied ohne Rechte" verwechselt.

Zusätzlich verwendet `BrokerNameResolver` in `dl-dashboard/src/names.rs` den Broker für aktuelle Discord-Anzeigenamen. Weitere Dashboard-Funktionen holen Guild-Statistiken und öffentliche Linkdaten über Broker-Endpunkte.

## 5. Fail-Closed bei Auth-Konfiguration

`DashboardConfig::auth_enforced` liefert im untersuchten Code `true`. Die Kommentare und Tests in `config.rs` halten fest, dass eine unvollständige Discord-OAuth-Konfiguration das Dashboard nicht offen schaltet. Die Handler antworten in diesem Fall mit einem Fehlerzustand.

Damit ist "OAuth nicht konfiguriert" vom Zustand "ohne Anmeldung zugänglich" zu unterscheiden.

## 6. Delegation von Stats und Tierlist

`dl-webcore::DashboardClient` wird in `dl-web/main.rs` einmal gebaut und an Tierlist und Stats weitergegeben. Diese Dienste können Session- beziehungsweise OAuth-Funktionen an das Master Dashboard delegieren.

Die Public-Stats-Auth-Schicht liegt in `Deadlock-Bots/rust/crates/dl-stats/src/auth.rs`. Sie fordert für den Activity-Flow eine delegierte Discord-Anmeldung beim Dashboard an. Die konkrete Browser-Weiterleitung und Cookie-Verarbeitung gehört zur Stats- beziehungsweise Dashboard-Schicht, nicht zum Broker selbst.

## 7. Tierlist Refresh

`DL_TIERLIST_REFRESH` wird in `WebConfig` ausgewertet. Der Default ist aktiv. Bei deaktiviertem Schalter startet `dl-web/main.rs` den Refresh-Loop nicht und protokolliert, dass Lesen und Votes weiterlaufen.

Der Schalter ist für Paralleltests gegen dieselbe Produktionsdatenbank relevant, weil zwei Refresh-Prozesse sonst dieselben Snapshot-Daten schreiben könnten.

## 8. Quellreferenzen

| Thema | Datei und Symbol |
|---|---|
| drei Server, Bindings, Prozess-Select | `Deadlock-Bots/rust/bin/dl-web/src/main.rs`, `main` |
| gemeinsame Web-Konfiguration | `Deadlock-Bots/rust/crates/dl-webcore/src/config.rs`, `WebConfig` |
| Dashboard-Konfiguration | `Deadlock-Bots/rust/crates/dl-dashboard/src/config.rs`, `DashboardConfig` |
| Dashboard-Router und Login | `Deadlock-Bots/rust/crates/dl-dashboard/src/web.rs`, `router` |
| Broker-gestützte Zugriffsprüfung | `Deadlock-Bots/rust/crates/dl-dashboard/src/authority.rs`, `BrokerMemberLookup`, `decide_access` |
| Broker-Namensauflösung | `Deadlock-Bots/rust/crates/dl-dashboard/src/names.rs`, `BrokerNameResolver` |
| Stats-OAuth-Delegation | `Deadlock-Bots/rust/crates/dl-stats/src/auth.rs` |

## 9. Grenzen dieser Referenz

Nicht geprüft wurden Caddy-Routen, DNS, TLS, aktuelle Listener, OAuth-Secrets, aktive Session-Datensätze und Live-Erreichbarkeit. Diese Punkte benötigen Betriebsdaten außerhalb des statischen Codes.
