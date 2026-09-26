# Expliziter Brain-Adapter für öffentliche Dokumentationsfragen

Stand: 2026-09-26. C9 macht den typisierten Adapter zum direkt nutzbaren Query-Pfad dieses Repositories. Das Repository bleibt ein Wissensbestand und startet weiterhin keinen eigenen Antwortdienst.

Der einzige Antworttransport ist `brain-client` aus Deadlock-Brain, gepinnt auf `54dcae30a172f5cccdb9f53b6bd6ed746f9315ec`. Kein direkter Modellaufruf, keine lokale RAG-Suche und kein automatischer Ersatzpfad.

## Vertrag und Schutzgrenzen

Der Adapter erlaubt ausschließlich `docs.public`. Weder Frage noch JSON-Eingabe dürfen Principal oder zusätzliche Scopes erzeugen. Der Server authentifiziert das Bearer-Token und prüft die tatsächliche Dokumentberechtigung. Endpunkte müssen Loopback sein; externe HTTPS-Ziele sind keine implizite Egress-Erlaubnis.

Timeout, Request-/Response-Limits, Redirect-/Proxy-Schutz und Token-Redaktion kommen aus dem typisierten BrainClient. `unavailable` und `build_rejected` sind Teil des gepinnten Wire-Vertrags und werden als unveränderter `PublicAnswerResponse` ausgegeben.

## Tatsächlicher Query-Pfad

```sh
# Typisierte Query direkt an eine ausdrücklich freigegebene lokale brain-serve-Instanz.
# BRAIN_ADAPTER_TOKEN separat sicher setzen.
cargo run --manifest-path tools/brain-adapter/Cargo.toml --locked -- \
  query http://127.0.0.1:PORT 5000 "Welche öffentliche Dokumentation gibt es dazu?"
```

Der `query`-Befehl erzeugt eindeutige Request-/Conversation-IDs und bindet fest `docs.public`. Für Contract-/Fixture-Arbeit bleiben `prepare` und `answer` erhalten.

## Offline prüfen

```sh
cargo test --manifest-path tools/brain-adapter/Cargo.toml --all-targets --locked
cargo clippy --manifest-path tools/brain-adapter/Cargo.toml --all-targets --locked -- -D warnings
cargo fmt --manifest-path tools/brain-adapter/Cargo.toml -- --check
```

Vor einer späteren realen Nutzung bleibt ein isolierter Test gegen brain-serve mit einem nichtproduktiven Public-Token nötig. Keine Dokumente wurden veröffentlicht, keine Produktionskonfiguration geändert und kein Deployment ausgeführt.
