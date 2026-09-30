# FAQ-Entwurf: Item-Referenz

status: entwurf

Nicht für `public/` freigegeben.

Quellstand: `Deadlock-Brain` Commit `458d56d0845f83bb50fdb635e78c0367f3cff8a1`.

## Welche Daten kann die Item-Referenz liefern?

`item_summary` im Build-Optimizer verdichtet die aktuellen Item-Payloads zu einer stabilen Antwortstruktur. Erfasst werden:

* Name und technische Klassenkennung
* Shop-Slot und Tier
* Kosten
* Active- oder Passive-Eigenschaft
* Aktivierungsdaten
* bereinigte Beschreibung
* Komponenten
* relevante Properties
* Upgrades
* abgeleitete Archetypen

Quelle: `Deadlock-Brain/rust/crates/dbrain-learn/src/build_optimizer.rs`, Funktion `item_summary`.

Die Rohdaten kommen laut Projektübersicht aus der Deadlock Assets API und werden als versionierte Entity-Snapshots im Brain gespeichert.

Quelle: `Deadlock-Brain/README.md`, Abschnitte "Quellen", "Datenablage" und "Timelines, Reviews und Qualitaet".

## Was bedeuten die Item-Archetypen?

`classify_item_archetypes` ordnet Items anhand ihrer strukturierten Daten und Texte in Funktionsgruppen ein. Der aktuelle Code kennt unter anderem:

* `lane_farm`, `waveclear` und `orb_secure`
* `lane_trade`, `duel`, `burst` und `sustained_dps`
* `kill_setup`, `escape`, `teamfight_engage`
* `counter`, `defensive_active`, `defensive_proc`
* `anti_heal`, `anti_carry`, `save`
* `core_scaling`, `support`, `objective_damage`, `splitpush`
* `luxury` und `active_burden`

Quelle: `Deadlock-Brain/rust/crates/dbrain-learn/src/build_optimizer.rs`, Funktion `classify_item_archetypes`.

Diese Tags sind eine interne Klassifikation für Retrieval und Build-Begründung. Sie sind keine offiziellen Shop-Kategorien des Spiels.

## Wie entsteht aus einem Item eine Build-Empfehlung?

Der Build-Optimizer verbindet mehrere Signalarten. Die Projektübersicht nennt Deadlock-API-Itemdaten, Hero-`item_draft_bucketing`, Shop-Bonus-Kurven, Sheet-Hinweise, Patchsignale und optional gecachte Wiki-Zusammenfassungen. Die Ausgabe trennt unter anderem frühen Economy-Aufbau, Core-Impact, situative Counter und Late- beziehungsweise Luxury-Käufe.

Quelle: `Deadlock-Brain/README.md`, Beschreibung des Befehls `build`.

Der daraus entstehende Plan ist laut Projektübersicht ein erklärbarer Kandidatenplan und keine finale Copy-Paste-Buyorder. Für die FAQ bedeutet das: "Core" ist eine begründete Empfehlung im aktuellen Kontext, kein unveränderlicher Status eines Items.

## Warum kann sich eine Item-Empfehlung nach einem Patch ändern?

Das Brain speichert Patchereignisse, normalisiert Entitäten und Aliase und kann historische Änderungen in Timelines zusammenführen. Build-Signale können dadurch mit aktuellen Itemdaten und Patchsignalen kombiniert werden.

Quellen:

* `Deadlock-Brain/README.md`, Abschnitte "Patch-Events", "Enrichment, Sheet-Stats und Kontext" sowie "Timelines, Reviews und Qualitaet"
* `Deadlock-Brain/rust/crates/dbrain-learn/src/build_optimizer.rs`

Eine öffentliche Item-Seite sollte deshalb konkrete Kosten, Werte und Effekte mit einem Datenstand versehen und nach einem relevanten Patch neu geprüft werden.

## Wie sollten aktive Items erklärt werden?

`item_summary` übernimmt `is_active_item` und die Aktivierungsdaten in die interne Referenz. Der Optimizer markiert aktive Items zusätzlich mit dem Archetyp `active_burden`. Die Economy-Zusammenfassung modelliert außerdem eine Begrenzung aktiver Items.

Quelle: `Deadlock-Brain/rust/crates/dbrain-learn/src/build_optimizer.rs`, Funktionen `item_summary`, `classify_item_archetypes` und `economy_summary`.

Patchabhängige Grenzwerte sollten vor einer Veröffentlichung aus dem aktuellen Datenstand bestätigt werden.

## Was fehlt für eine öffentliche Item-Referenz?

Der bestehende öffentliche Korpus enthält Hero-Builds und Community-Funktionen rund um Builds, aber keinen eigenständigen systematischen Item-Katalog. Die Korpusprüfung nennt Kosten, Effekte, Wechselwirkungen, Kaufreihenfolge und situative Alternativen als nicht ausreichend separat belegte Tiefe.

Quelle: `Deadlock-Docs/internal/wissensbasis/faq-korpus-abdeckung.md`, Abschnitt "Lücken für Deadlock-Fragen".

Für die spätere Veröffentlichung sollte deshalb aus dem versionierten Brain-Datenbestand eine reproduzierbare Item-Seite pro Item oder eine strukturierte Referenz generiert werden. Der Entwurf selbst bleibt intern.
