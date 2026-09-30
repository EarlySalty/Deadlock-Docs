# FAQ-Entwurf: Spielmechanik und Matchablauf

status: entwurf

Nicht für `public/` freigegeben.

Quellstand: `Deadlock-Brain` Commit `458d56d0845f83bb50fdb635e78c0367f3cff8a1`, ergänzend die bestehende Korpusprüfung in `Deadlock-Docs`.

## Welche Grundsysteme muss eine Match-Erklärung abdecken?

Das aktuelle Wissensmodell des Deadlock-Brain führt als globale Spielkonzepte unter anderem Souls, Soul Urn, Troopers, Guardians, Walkers, Patron, Shrines, Rejuvenator, Jungle Camps, Zipline, Jump Pad sowie Shop und Economy. Diese Liste stammt aus der modellierten Themenstruktur und den eingelesenen Patchereignissen. Sie ist eine Abdeckungsliste, keine vollständige Regelerklärung.

Quelle: `Deadlock-Brain/rust/docs/specs/2026-06-25-top-down-wissensmodell.md`, Abschnitte zu `global_objective_economy` und den Global Concepts.

## Was sind Souls im aktuellen Brain-Modell?

`dbrain-learn` behandelt Souls gleichzeitig als Währung und Erfahrung. Der Build-Optimizer verbindet die Soul-Ökonomie mit Itemkosten, Shop-Kategorieboni, Komponenten und Ability-Fortschritt.

Quelle: `Deadlock-Brain/rust/crates/dbrain-learn/src/build_optimizer.rs`, Funktion `economy_summary`.

Für eine öffentliche FAQ sollten konkrete Schwellenwerte erst nach einem aktuellen Datenabgleich übernommen werden. Der Code enthält Zahlen für Item-Tiers, Ability-Unlocks und Shop-Spikes, die sich durch Balance-Änderungen verändern können.

## Wie sollen Fragen zu Last Hits, Soul Orbs und Denies beantwortet werden?

Die aktuelle Retrieval-Schicht erkennt Begriffe rund um Souls und Denying und besitzt ein Item-Archetyp `orb_secure`. Das belegt Such- und Klassifikationswissen, aber noch keine kanonische, ausreichend vollständige Regelbeschreibung für eine öffentliche FAQ.

Quellen:

* `Deadlock-Brain/rust/crates/dbrain-retrieval/src/lib.rs`, Query-Begriffe für `deny`, `denying`, `soul` und `souls`
* `Deadlock-Brain/rust/crates/dbrain-learn/src/build_optimizer.rs`, `classify_item_archetypes`

Entwurfsregel: Bei einer Detailfrage zu Orb-Timing, Deny-Fenster oder exakten Soul-Werten soll die spätere öffentliche Fassung einen aktuellen Mechanikbeleg aus dem Brain oder einer freigegebenen Primärquelle verlangen, statt aus Retrieval-Schlüsselwörtern eine Spielregel abzuleiten.

## Wie werden Silence, Stun und Immobilize unterschieden?

Der Build-Optimizer hält in seiner Economy- und Mechanikzusammenfassung folgende Unterscheidung fest:

* Silence verhindert Abilities und Active Items.
* Stun verhindert Bewegung, Schießen und Aktionen.
* Immobilize bindet die Bewegung, verhindert aber nicht automatisch Abilities oder Waffen.

Quelle: `Deadlock-Brain/rust/crates/dbrain-learn/src/build_optimizer.rs`, Funktion `economy_summary`, Feld `mechanic_notes`.

Diese Aussagen sind im aktuellen Code explizit modelliert. Vor einer Veröffentlichung sollten sie dennoch gegen den dann aktuellen Spielstand geprüft werden.

## Was kann der Entwurf zu Parry sagen?

Der Reasoner kennt `parry` als aktionsgebundene Bedingung. `condition_factor_for_hero` bewertet diese Bedingung bewusst nicht automatisch als verlässlich erfüllbar, sondern setzt den Faktor für `parry` auf null. Das ist eine wichtige Grenze: Aus dem Reasoner lässt sich keine allgemeine Erfolgsregel oder ein Timingfenster für Paraden ableiten.

Quelle: `Deadlock-Brain/rust/crates/dbrain-reasoner/src/mechanics.rs`, Funktion `condition_factor_for_hero`.

## Wie sollte "Farmen oder rotieren?" beantwortet werden?

Der aktuelle Brain-Code klassifiziert Items und Build-Signale unter anderem nach `lane_farm`, `waveclear`, `orb_secure`, `objective_damage` und `splitpush`. Damit kann ein späterer Antwortpfad Wirtschaft, Waveclear und Objective-Druck gemeinsam betrachten.

Quelle: `Deadlock-Brain/rust/crates/dbrain-learn/src/build_optimizer.rs`, Funktion `classify_item_archetypes`.

Der Code enthält jedoch keine universelle Regel "ab Minute X rotieren". Die FAQ sollte deshalb situationsabhängige Entscheidungskriterien erklären und patchabhängige Zeit- oder Soulwerte aus aktuellen Daten beziehen.

## Welche echte Lücke bleibt?

Die bestehende öffentliche Dokumentation erklärt den Einstieg und viele Hero-spezifische Builds, hat aber keine eigenständige, systematische Mechanikreferenz. Die Metadatenprüfung nennt genau diese Lücke für Souls-Ökonomie, Last Hits und Denies, Farmen und Rotationen, Kartenobjekte, Matchphasen, Bewegung, Ausdauer, Nahkampf und Parieren.

Quelle: `Deadlock-Docs/internal/wissensbasis/faq-korpus-abdeckung.md`, Abschnitt "Lücken für Deadlock-Fragen".

Vor einer Verschiebung nach `public/` fehlen deshalb noch aktuelle Primärbelege für die Regeln, die über das heute modellierte Brain-Wissen hinausgehen.
