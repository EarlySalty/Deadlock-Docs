# Expliziter Brain-Adapter für öffentliche Dokumentationsfragen

Stand: 2026-09-26. C9 macht den typisierten Adapter zum direkt nutzbaren Query-Pfad dieses Repositories. Das Repository bleibt ein Wissensbestand und startet weiterhin keinen eigenen Antwortdienst.

Der einzige Antworttransport ist `brain-client` aus Deadlock-Brain, gepinnt auf `3b86d3cbe5ea39a67b8b1fbd8a3d48ab935982ef`. Kein direkter Modellaufruf, keine lokale RAG-Suche und kein automatischer Ersatzpfad.

## Vertrag und Schutzgrenzen

Der Adapter erlaubt ausschließlich `docs.public`. Weder Frage noch JSON-Eingabe dürfen Principal oder zusätzliche Scopes erzeugen. Der Server authentifiziert das Bearer-Token und prüft die tatsächliche Dokumentberechtigung. Endpunkte müssen Loopback sein; externe HTTPS-Ziele sind keine implizite Egress-Erlaubnis.

Timeout, Request-/Response-Limits, Redirect-/Proxy-Schutz und Token-Redaktion kommen aus dem typisierten BrainClient. `unavailable` und `build_rejected` sind Teil des gepinnten Wire-Vertrags und werden als unveränderter `PublicAnswerResponse` ausgegeben.

Die nicht geheime [Config-Vorlage](config.example.json) enthält Loopback-Endpunkt, Frist, Infisical-Projekt und den **Namen** eines für `docs.public` vorgesehenen Tokens. Der vorhandene Infisical-Bootstrap-Token wird ausschließlich aus seiner geschützten Runtime-Credential-Datei gelesen; der Adapter legt keine Credential-Datei an. Weder Bootstrap- noch Brain-Token erscheinen in Argumenten, Environment-Variablen oder Logs. Der Infisical-Zugriff verwendet ausschließlich den geschützten lokalen Unix-Socket. Fehlende, doppelte oder ungültige Token-Werte brechen den Lauf ab. Vor einer echten Nutzung muss der Betreiber den gewählten Secret-Namen mit der Brain-Serve-Credential-ACL abgleichen und den erlaubten öffentlichen Wissensrelease live prüfen.

## Tatsächlicher Query-Pfad

```sh
# Typisierte Query direkt an eine ausdrücklich freigegebene lokale brain-serve-Instanz.
# CONFIG_JSON ist eine bearbeitete Kopie der Vorlage ohne Secret-Werte.
cargo run --manifest-path tools/brain-adapter/Cargo.toml --locked -- \
  query CONFIG_JSON "Welche öffentliche Dokumentation gibt es dazu?"
```

Der `query`-Befehl erzeugt eindeutige Request-/Conversation-IDs und bindet fest `docs.public`. Für Contract-/Fixture-Arbeit bleiben `prepare` und `answer` erhalten.

## Offline prüfen

```sh
cargo test --manifest-path tools/brain-adapter/Cargo.toml --all-targets --locked
cargo clippy --manifest-path tools/brain-adapter/Cargo.toml --all-targets --locked -- -D warnings
cargo fmt --manifest-path tools/brain-adapter/Cargo.toml -- --check
```

Vor einer späteren realen Nutzung bleibt ein isolierter Test gegen brain-serve mit einem nichtproduktiven Public-Token nötig. Keine Dokumente wurden veröffentlicht, keine Produktionskonfiguration geändert und kein Deployment ausgeführt.
