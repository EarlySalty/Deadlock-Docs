# FAQ-Entwurf: Item-Referenz

status: entwurf
stand: 2026-09-19
quelle: `Deadlock-Brain` Commit `15bc1d3ac3158791ab5260aa83d415a38fb7beb1`, ergänzend bestehende Heldenguides

Nicht für `public/` freigegeben.

## Welche Item-Daten kann die Referenz liefern?

`item_summary` verdichtet Item-Payloads zu Name, Klassenkennung, Shop-Slot, Tier, Kosten, Active-Status, Aktivierung, Beschreibung, Komponenten, Properties und Upgrades, `Deadlock-Brain/rust/crates/dbrain-learn/src/build_optimizer.rs:970-995`.

Die Projektübersicht nennt die Deadlock Assets API als Quelle für Heroes, Items und Rohdaten, `Deadlock-Brain/README.md:9-14`.

## Wie werden Items für Build-Fragen eingeordnet?

`classify_item_archetypes` beginnt in `Deadlock-Brain/rust/crates/dbrain-learn/src/build_optimizer.rs:997`. Der Code leitet daraus Funktionsgruppen wie Farm, Waveclear, Orb-Sicherung, Burst, Escape, Counter, Support, Objective-Damage und Splitpush ab, `Deadlock-Brain/rust/crates/dbrain-learn/src/build_optimizer.rs:1020-1045`.

Diese Archetypen sind interne Klassifikationen für Retrieval und Build-Begründung. Sie sind keine offiziellen Shop-Kategorien.

## Wie entsteht eine Build-Empfehlung?

Die Projektübersicht beschreibt `build` als deterministischen Kandidatenplan, der Itemdaten, Hero-Signale, Shop-Boni, Patchsignale und weitere Kontexte kombiniert. Beleg: `Deadlock-Brain/README.md:275-285`.

Die Ausgabe ist laut derselben Beschreibung kein unveränderlicher Copy-Paste-Build. Für eine FAQ bedeutet das: "Core" oder "situativ" ist eine begründete Empfehlung im aktuellen Kontext, kein fester Status eines Items.

## Warum braucht die Referenz Patchbezug?

Das Brain speichert und verarbeitet Patch-Events als eigene Wissensschicht, `Deadlock-Brain/README.md:198-216`. Itemkosten, Effekte und Build-Prioritäten können sich damit über Zeit verändern.

Konkrete Zahlen in einer späteren Public-Seite brauchen deshalb einen Stand und eine erneute Prüfung nach relevanten Patches.

## Was sagen die vorhandenen Heldenguides?

Der öffentliche Abrams-Guide hat einen eigenen Build-Abschnitt, `Deadlock-Docs/public/deadlock-helden/abrams.html:39-47`. Seine Metadaten tragen einen eigenen Stand und eine Quellenangabe, `Deadlock-Docs/public/deadlock-helden/abrams.html:7-8`.

Die Korpusprüfung zeigt zugleich, dass alle 36 Heldenseiten Build-Abschnitte haben, aber kein eigenständiger Item-Katalog vorhanden ist, `Deadlock-Docs/internal/wissensbasis/faq-korpus-abdeckung.md:166-175`.

## Freigabegrenze

Vor einer Übernahme nach `public/` sollte die Item-Referenz reproduzierbar aus dem versionierten Brain-Datenbestand erzeugt oder gegen ihn geprüft werden. Kosten, Effekte und situative Empfehlungen dürfen nicht aus einem alten Entwurf übernommen werden.
