# Expliziter Brain-Adapter für öffentliche Dokumentationsfragen

Stand: 2026-09-25. Vorbereitet, **nicht produktiv verdrahtet**.

Dieses Repository ist laut S01 ein Wissensbestand, kein eigener Antwortdienst. Der neue Rust-Adapter stellt deshalb einen ausdrücklich aufrufbaren Query-Port bereit. Er liest keine Dokumentationsdateien, importiert nichts und startet keinen Dienst. `public/`, `internal/` und bestehende Publikationswerkzeuge bleiben unverändert.

Der einzige Antworttransport ist `brain-client` aus Deadlock-Brain, exakt gepinnt auf `bdcc6dec3424bd313d36e5f545de2a07df564c7f` (PR #39, aufgebaut auf CODEX A/PR #38). Kein direkter Modellaufruf, keine lokale RAG-Suche, keine automatische Ersatzantwort.

## Vertrag und Schutzgrenzen

Eingang ist der kanonische `Query`; Ausgang unverändert `brain.public.v1` mit Status, Text, Release und opaken Quellenlabels. Der Adapter erlaubt ausschließlich die explizite Bereichsmenge `docs.public`, keine leere oder aus dem Fragetext abgeleitete Berechtigung. Der Server muss das Bearer-Token selbst authentifizieren und die tatsächliche Dokumentberechtigung prüfen. Dieses Tool erteilt keine Veröffentlichungserlaubnis für `internal/`.

Nur Loopback-Endpunkte sind zulässig. HTTPS allein erlaubt keinen Export an externe Hosts. Request-Limit 64 KiB, Response-Limit 512 KiB; keine Redirects, Proxy-Vererbung oder Wiederholungen. Frist ausdrücklich 1–60000 Millisekunden. Token über die ausschließlich für diesen manuellen Aufruf gesetzte Variable `BRAIN_ADAPTER_TOKEN`, nie über Kommandozeilenargumente oder `.env`-Autoload. Fehlertexte enthalten keine Anfrage, Zugangsdaten oder upstream Fehlernachrichten.

## Offline prüfen

```sh
cargo fetch --manifest-path tools/brain-adapter/Cargo.toml --locked
bash tools/brain-adapter/check.sh
```

Rust 1.97.1 mit rustfmt/clippy. Das Skript führt Formatprüfung, Tests und Clippy aus, schreibt Exitcodes/Logs nach `.consumer-ci-reports/` und entfernt die geerbte Anwendungsumgebung. Die GitHub-Actions-Prüfung verwendet denselben Einstieg, ausschließlich selbst verfasste Fixtures und keine Produktions-Secrets. Kein Workflow in dieser Änderung deployt oder mergt.

## Manueller Aufruf nach separater Freigabe

```sh
# Nur validieren/normalisieren; benötigt kein Token und kein Netzwerk:
cargo run --manifest-path tools/brain-adapter/Cargo.toml --locked --offline -- prepare < query.json

# Erst nach lokaler Auth-/ACL-/Egress-Prüfung. Das Token separat sicher bereitstellen:
cargo run --manifest-path tools/brain-adapter/Cargo.toml --locked --offline -- answer http://127.0.0.1:PORT 5000 < query.json
```

`PORT` ist bewusst kein Produktionsport. `request_id` muss pro Anfrage eindeutig und `conversation_id` vertrauenswürdig an den tatsächlichen Benutzer gebunden sein. Ausgabe nur an den aufrufenden Operator, keine Nachricht an Discord/Twitch.

## Noch lokal zu prüfen

Claude muss den vorgesehenen Aufrufer verbinden, Credentials/Scope-Bindung und öffentliche Corpus-Freigabe prüfen, die konkrete Wissensrelease zuweisen sowie Autorisierungsfehler, Timeouts und Quellenanzeige gegen eine isolierte echte Brain-Runtime testen. Diese Arbeit hat keine Dokumente veröffentlicht und keinen produktiven Runtime-Test ausgeführt. Historie, persönliche Datenkarten, fachliche Intent-Metadaten und Publishing sind im aktuellen API-Vertrag nicht abgebildet und werden durch dieses Tool nicht erfunden.
