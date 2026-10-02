# Expliziter Brain-Adapter für öffentliche Dokumentationsfragen

Stand: 2026-10-03. C9 macht den typisierten Adapter zum direkt nutzbaren Query-Pfad dieses Repositories. Das Repository bleibt ein Wissensbestand und startet weiterhin keinen eigenen Antwortdienst.

Der einzige Antworttransport ist `brain-client` aus Deadlock-Brain, gepinnt auf `3b86d3cbe5ea39a67b8b1fbd8a3d48ab935982ef`. Kein direkter Modellaufruf, keine lokale RAG-Suche und kein automatischer Ersatzpfad.

## Vertrag und Schutzgrenzen

Der Adapter erlaubt ausschließlich `docs.public`. Weder Frage noch JSON-Eingabe dürfen Principal oder zusätzliche Scopes erzeugen. Der Server authentifiziert das Bearer-Token und prüft die tatsächliche Dokumentberechtigung. Endpunkte müssen Loopback sein; externe HTTPS-Ziele sind keine implizite Egress-Erlaubnis.

Die Docs-Credential gehört serverseitig zur Identität `docs-client` im Kanal `docs`. Sie muss genau `docs.public` und einen eigenen, dafür veröffentlichten öffentlichen Docs-Release erhalten. Der Client wählt weder Identität noch Release. Der private 2nd-Brain-Operatorweg mit `brain.internal.operator.v1` ist über einen getrennten Unixsocket erreichbar; die Docs-Credential erhält dafür keine Berechtigung. `second_brain.internal` ist im Docs-Adapter als Scope ausgeschlossen.

Timeout, Request-/Response-Limits, Redirect-/Proxy-Schutz und Token-Redaktion kommen aus dem typisierten BrainClient. `unavailable` und `build_rejected` sind Teil des gepinnten Wire-Vertrags und werden als unveränderter `PublicAnswerResponse` ausgegeben.

Die normale Laufzeitkonfiguration liegt unter `/home/nathanael/.config/deadlock-docs/bot.toml`. Der Adapter lädt ausschließlich `[brain.docs]` mit den bisherigen Feldern `endpoint` und `timeout_ms` sowie `[brain.docs.infisical]` mit den bisherigen sicheren Credentialparametern. Fehlende, ungültige oder widersprüchliche Konfiguration bricht den Aufruf ab.

Die nicht geheime [Config-Vorlage](config.example.toml) enthält Loopback-Endpunkt, Frist, Infisical-Projekt, `credential_fd = 5` und den Namen eines für `docs.public` vorgesehenen Tokens. Der vertrauenswürdige Starter öffnet die vorhandene geschützte Runtime-Credential auf FD5. Der Adapter liest positionsunabhängig aus einer eigenen CLOEXEC-Kopie und schützt auch den geerbten Deskriptor gegen Weitergabe an Kindprozesse. Die Quelle muss eine reguläre, nur für ihren Besitzer zugängliche Datei sein. Fehlende, ungültige oder unlesbare Deskriptoren brechen den Lauf ab. Für vorhandene dateibasierte Aufrufer bleibt die ausdrücklich konfigurierte absolute `credential_file` unterstützt; beide Quellen zusammen werden abgewiesen. Es gibt keinen automatischen Wechsel zwischen Quellen. Der Adapter legt keine Credential-Datei an.

Weder Bootstrap- noch Brain-Token erscheinen in Argumenten, Environment-Variablen oder Logs. Der Infisical-Zugriff verwendet ausschließlich den geschützten lokalen Unix-Socket und fragt genau den benannten Secret-Wert ab, ohne Listenabruf oder Import. Fehlende, abweichende oder ungültige Token-Werte brechen den Lauf ab. Vor einer echten Nutzung muss der Betreiber den gewählten Secret-Namen mit der Brain-Serve-Credential-ACL abgleichen und den erlaubten öffentlichen Wissensrelease live prüfen.

## Tatsächlicher Query-Pfad

```sh
# Typisierte Query direkt an eine ausdrücklich freigegebene lokale brain-serve-Instanz.
# CONFIG_TOML bezeichnet die normale bot.toml ohne Secret-Werte.
cargo run --manifest-path tools/brain-adapter/Cargo.toml --locked -- \
  query CONFIG_TOML "Welche öffentliche Dokumentation gibt es dazu?"
```

Der `query`-Befehl erzeugt eindeutige Request-/Conversation-IDs und bindet fest `docs.public`. Für Contract-/Fixture-Arbeit bleiben `prepare` und `answer` erhalten.

## Offline prüfen

```sh
cargo test --manifest-path tools/brain-adapter/Cargo.toml --all-targets --locked --offline
cargo clippy --manifest-path tools/brain-adapter/Cargo.toml --all-targets --locked --offline -- -D warnings
cargo fmt --manifest-path tools/brain-adapter/Cargo.toml -- --check
```

Die gesperrten Abhängigkeiten müssen bereits im lokalen Cargo-Cache liegen. Die Prüfungen laufen lokal; ein GitHub-Actions-Workflow wird dafür nicht angelegt.

Zur Abnahme gehören eine authentifizierte lesende Probe mit echten Docs-Belegen und Negativproben für fremde Scopes, eine eingegebene Identität oder Releasewahl sowie den privaten Operator-Socket. Ein erfolgreicher Offline-Test ersetzt weder die Serverfreigabe noch den Live-Nachweis.
