# FAQ-Entwurf: Spielmechanik und Matchablauf

status: entwurf
stand: 2026-09-19
quelle: `Deadlock-Brain` Commit `15bc1d3ac3158791ab5260aa83d415a38fb7beb1`, Korpuslücke aus `Deadlock-Docs`

Nicht für `public/` freigegeben.

## Was muss eine Grundlagen-FAQ überhaupt abdecken?

Das interne Brain-Modell führt als globale Spielkonzepte Souls, Urn, Troopers, Guardians, Walkers, Patron, Shrines, Rejuvenator, Map/Movement sowie Shop/Economy. Beleg: `Deadlock-Brain/rust/docs/specs/2026-06-25-top-down-wissensmodell.md:135` und `Deadlock-Brain/rust/docs/specs/2026-06-25-top-down-wissensmodell.md:312`.

Der öffentliche Korpus hat genau hier eine strukturelle Lücke. Die Korpusprüfung nennt fehlende eigene Abschnitte für Souls-Ökonomie, Last Hits und Denies, Farmen, Kartenobjekte, Matchphasen, Bewegung, Ausdauer, Nahkampf und Parieren, `Deadlock-Docs/internal/wissensbasis/faq-korpus-abdeckung.md:166-175`.

## Was sind Souls?

Im aktuellen Build-Optimizer werden Souls als Währung und Erfahrung modelliert, `Deadlock-Brain/rust/crates/dbrain-learn/src/build_optimizer.rs:903-942`.

Der Entwurf übernimmt bewusst keine festen Schwellenwerte aus dieser Funktion in eine öffentliche FAQ. Solche Werte sind patchabhängig und müssen vor Veröffentlichung gegen den aktuellen Datenstand geprüft werden.

## Kennt das Brain Last Hits und Denies?

Die Retrieval-Schicht erkennt Spielbegriffe wie `souls`, `guardian`, `walker`, `trooper` und `denying`, `Deadlock-Brain/rust/crates/dbrain-retrieval/src/lib.rs:150-168`.

Für Deny- und Soul-Begriffe existieren zusätzlich normalisierte Synonymgruppen, `Deadlock-Brain/rust/crates/dbrain-retrieval/src/lib.rs:3707-3736`.

Das belegt Suchwissen, aber keine vollständige Spielregel. Ein späterer Public-Text zu Orb-Timing, Deny-Fenstern oder exakten Soul-Werten braucht deshalb einen aktuellen Mechanikbeleg.

## Was kann der Entwurf zu Parry sagen?

Der Reasoner kennt `parry` als aktionsgebundene Bedingung. `condition_factor_for_hero` behandelt diese Bedingung konservativ und setzt sie nicht automatisch als erfüllbar voraus, `Deadlock-Brain/rust/crates/dbrain-reasoner/src/mechanics.rs:74-88`.

Daraus lässt sich kein allgemeines Parade-Timing ableiten. Für eine nutzersichtbare Erklärung des Timings fehlt in diesem Paket ein ausreichend belastbarer Primärbeleg.

## Wie sollte "Farmen oder rotieren?" beantwortet werden?

Der Build-Optimizer klassifiziert Items und Build-Signale unter anderem nach `lane_farm`, `waveclear`, `orb_secure`, `objective_damage` und `splitpush`, `Deadlock-Brain/rust/crates/dbrain-learn/src/build_optimizer.rs:997-1045`.

Damit kann eine spätere Antwort Wirtschaft, Waveclear und Objective-Druck gemeinsam betrachten. Der Code enthält aber keine allgemeine Regel wie "ab Minute X rotieren". Die FAQ sollte deshalb Kriterien erklären und konkrete Timingwerte aus dem jeweils aktuellen Spielstand beziehen.

## Freigabegrenze

Vor einer Übernahme nach `public/` fehlen aktuelle Primärbelege für die Detailregeln, die über das modellierte Brain-Wissen hinausgehen. Bis dahin ist dieser Text ein Redaktionsentwurf und keine Spielerreferenz.
