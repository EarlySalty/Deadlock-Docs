---
title: "Deadlock Brain Match-Demo-Lernen"
tags: [internal, deadlock-brain, demos, lernen, kalibrierung]
stand: 2026-07-10
quelle: "Deadlock-Brain"
---
# Match-Demo-Lernen

Der erste Tracer lernt Mo & Krill aus echten Match-Demos des Referenzspielers `281768392` (`SteamID64 76561198242034120`). Alle verfuegbaren Mo-Matches bleiben im Katalog; Siege, Niederlagen und historische Patches werden nicht ausgefiltert. Nur Matches mit vollstaendig abrufbarer Demo-Evidenz koennen analysiert werden.

## Ablauf

Vom Root des Deadlock-Brain-Repos:

```bash
./rust/target/release/deadlock-brain player sync-matches 281768392 --hero-id 18 --pretty
./rust/target/release/deadlock-brain player fetch-demo 281768392 <MATCH_ID> --hero-id 18 --steam-id64 76561198242034120 --pretty
./rust/target/release/deadlock-brain player analyze-demo-match 281768392 <MATCH_ID> --pretty
```

Der Dry-Run baut nur den Modellkontext und speichert `context_ready`:

```bash
./rust/target/release/deadlock-brain player analyze-demo-match 281768392 <MATCH_ID> --dry-run --pretty
```

`fetch-demo` zieht zuerst vollstaendige Match-Metadaten. Danach laufen genau drei versionierte Demo-Queries fuer Player-State, zielspielerbezogene Combat-Ereignisse und Economy/Objectives. Erst nach drei erfolgreichen Jobs wird `deadlock_api_demo_evidence` gespeichert. Rohantworten bleiben als Source-Dokumente erhalten. (`rust/crates/dbrain-sources/src/deadlock_api.rs`)

## Evidenz- und Reportvertrag

Jede Rohzeile hat eine stabile Evidenz-ID. Combat-Zeilen werden fuer den Modellkontext in Fight-Fenster verdichtet; jedes Fenster traegt eine eigene `fight_window:*`-ID und alle darunterliegenden Roh-IDs. Player-State sowie Economy-/Objective-Ereignisse bleiben einzeln erhalten. (`rust/crates/dbrain-learn/src/match_demo_learning.rs`)

Der deterministische Matchkopf enthaelt Match, Account, Hero, Ergebnis, Dauer, Lane und Patchprovenienz. Das Modell darf ihn nicht aendern. Entscheidungen trennen Beobachtung, Aktion, Wirkung, Interpretation, Bewertung und Alternative und muessen bekannte Evidenz-IDs nennen.

Prompt `mo_full_report_de_v2` fordert mindestens zwei Economy-, drei Combat-, zwei Macro-Entscheidungen sowie eine starke Entscheidung, einen Fehler und einen Wendepunkt. Insgesamt muessen mindestens sieben unterschiedliche Kernentscheidungen vorliegen. Dieselbe Entscheidung kann in Phase und Fachabschnitt erscheinen, wird aber ueber Tick plus Evidenz kanonisiert, erhaelt dieselbe `D`-ID und wird im Markdown nur einmal voll ausgegeben.

Reports werden erst nach JSON-, Metadaten-, Evidenz- und Abdeckungsvalidierung als `calibration_pending` in `brain.player_match_decision_notes` gespeichert. Ungueltige Antworten erzeugen keinen fertigen Report. Aktive Regeln, Builds oder Coaching-Aussagen werden in diesem Tracer nicht geschrieben.

## Review

Ein Review muss alle kanonischen Entscheidungs-IDs des Reports als geprueft nennen. `corrections` enthaelt nur fehlerhafte Entscheidungen:

```json
{
  "reviewed_decision_ids": ["D1", "D2", "D3", "D4", "D5", "D6", "D7"],
  "corrections": [
    {
      "decision_id": "D3",
      "label": "unbelegt",
      "comment": "Das globale Objective-Ereignis belegt keine Spielerbeteiligung.",
      "replacement": "Nur das globale Ereignis nennen; Beteiligung bleibt unbekannt."
    }
  ]
}
```

Erlaubte Labels sind `falsch`, `unbelegt`, `Kontext fehlt` und `wichtige Entscheidung uebersehen`. Reviews werden versioniert als `source='human_review'`, `entity_type='player_match_report_review'` gespeichert.

```bash
./rust/target/release/deadlock-brain player review-demo-report <NOTE_ID> --file review.json --pretty
./rust/target/release/deadlock-brain player demo-calibration-status 281768392 --pretty
```

## Kalibrierungstor

Das Gate zaehlt nur das jeweils neueste vollstaendige Review pro Report. Es ist bestanden, wenn mindestens fuenf unterschiedliche Reports geprueft wurden und die letzten drei jeweils keinen kritischen Fehler sowie eine Korrekturquote strikt unter `0.10` haben.

`falsch`, `unbelegt` und `wichtige Entscheidung uebersehen` sind kritisch. `Kontext fehlt` ist kritisch, wenn eine nichtleere Ersetzung die Entscheidung aendert. Die Korrekturquote ist Zahl korrigierter IDs geteilt durch alle geprueften kanonischen IDs. Das Gate basiert ausschliesslich auf gespeicherten Reviews, nie auf der Modell-Selbsteinschaetzung.

## API-Limits und Fehler

Die Deadlock API dokumentiert Limits endpointabhaengig und meldet Ueberschreitungen als HTTP 429; fuer Demo-Queries ist keine feste oeffentliche Quote belastbar dokumentiert. Der Pilot sendet Jobs seriell, pollt standardmaessig alle 5 Sekunden und hat 900 Sekunden Gesamt-Timeout. Ein Poll-GET hat genau einen inneren HTTP-Versuch; 429, Server- und Transportfehler werden in der asynchronen Poll-Schleife wiederholt. Anfragezeit, Backoff und Poll-Pause sind jeweils auf die verbleibende Gesamtdauer begrenzt. Andere idempotente GETs nutzen weiterhin den zentralen Retry-/Backoff-Pfad. Demo-POSTs werden nicht blind wiederholt, weil ein Job trotz verlorener Antwort bereits erstellt sein kann. (`rust/crates/deadlock-brain-core/src/http.rs`, `rust/crates/dbrain-sources/src/deadlock_api.rs`)

Bei 404 bleibt das Match offen. Bei fehlgeschlagenem oder unvollstaendigem Query-Buendel entsteht kein fertiger Evidenz-Snapshot. Der Game-/Steam-Demo-Fallback bleibt vertagt, bis mehrere API-Reports den fachlichen Evidenz- und Reviewvertrag bestanden haben.

## Live-Tracer

Match `92685682` lieferte 4.472 Rohbelege und 36 abgeleitete Fight-Fenster. Der erste `v1`-Report war zu duenn und enthielt falsche Itemwirkungen. `v2` loest die beobachteten Items aus der Assets API auf, hat sieben kanonische Entscheidungen und besteht die formalen Gates.

`v2` ist fachlich noch nicht freigegeben: Die erste Vollpruefung fand unter anderem eine unbelegte Zuordnung eines globalen Boss-Ereignisses zum Zielspieler, eine inkonsistente Phasenreihenfolge und eine nur mit dem Nachher-Zustand belegte Rotation. Note `8` bleibt deshalb `calibration_pending`. Der Kalibrierungsstatus des Accounts steht nach dem bereinigten Smoke-Test bei `0/5`, `passed=false`.
