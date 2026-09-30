# FAQ-Entwurf: Ranks und Matchmaking

status: entwurf

Nicht für `public/` freigegeben.

Quellstand: `Deadlock-Bots` Commit `bb03deb53b28a7266de83748c3b834bff9c9a205`.

## Welche Rangnamen erkennt die Community-Statistik?

Die Rust-Statistikschicht führt in `RANK_ORDER` diese elf Rangfamilien:

1. Initiate
2. Seeker
3. Alchemist
4. Arcanist
5. Ritualist
6. Emissary
7. Archon
8. Oracle
9. Phantom
10. Ascendant
11. Eternus

Quelle: `Deadlock-Bots/rust/crates/dl-stats/src/ranks.rs`, Konstante `RANK_ORDER`.

Diese Liste beschreibt die vom Community-Code akzeptierten Rangnamen am genannten Commit. Sie ist kein eigenständiger Nachweis für zusätzliche Unterstufen oder für die aktuelle Matchmaking-Logik des Spiels.

## Woher nimmt die Website den Rang eines Discord-Nutzers?

`RankResolver::rank_of` liest `deadlock_rank_name` aus `core.steam_links`. Berücksichtigt werden verifizierte Steam-Verknüpfungen mit vorhandenem Rangnamen. Bei mehreren Verknüpfungen wird der primäre Account bevorzugt und danach der jüngere Rangstand.

Quelle: `Deadlock-Bots/rust/crates/dl-stats/src/ranks.rs`, Typ `RankResolver`, Methode `rank_of`.

Der gelesene Name wird kleingeschrieben und gegen `RANK_ORDER` geprüft. Ein anderer Wert wird von dieser Statistikschicht nicht als bekannter Rang zurückgegeben.

## Ist der angezeigte Rang dasselbe wie das Matchmaking Rating?

Aus dem untersuchten Community-Code lässt sich das nicht ableiten. `RankResolver` liest einen gespeicherten Rangnamen. Er berechnet weder ein verstecktes Rating noch bildet er die Matchmaking-Entscheidung des Spiels nach.

Quelle: `Deadlock-Bots/rust/crates/dl-stats/src/ranks.rs`, Methode `rank_of`.

Für eine öffentliche Erklärung von verborgenem Rating, Kalibrierung oder Matchmaking-Formeln wird deshalb eine aktuelle, dafür geeignete Primärquelle benötigt.

## Kennt der Bot den Matchmaking-Algorithmus?

Im untersuchten Rangmodul existiert keine Matchmaking-Implementierung. Es gibt dort Rangreihenfolge, Rangfarben, Rangauflösung aus der verifizierten Steam-Verknüpfung und eine separate Erkennung von Voice-Lane-Namen.

Quelle: `Deadlock-Bots/rust/crates/dl-stats/src/ranks.rs`.

Die Lane-Erkennung in derselben Datei wertet Namen wie `mid`, `off`, `safe`, `carry` oder `jungle` aus. Sie gehört zur Community-Darstellung und darf nicht als Beleg für das Matchmaking des Spiels verwendet werden.

## Warum kann ein Rang in der Community fehlen?

Auf Codeebene gibt es mehrere klare Voraussetzungen:

* Es muss eine Steam-Verknüpfung für die Discord-ID vorhanden sein.
* Die Verknüpfung muss als verifiziert markiert sein.
* `deadlock_rank_name` muss gesetzt sein.
* Der normalisierte Rangname muss in `RANK_ORDER` vorkommen.

Quelle: `Deadlock-Bots/rust/crates/dl-stats/src/ranks.rs`, Methode `rank_of`.

Ob ein fehlender oder alter Wert durch eine verzögerte externe Datenquelle, einen noch nicht gelaufenen Refresh oder eine Spieländerung verursacht wurde, lässt sich aus dieser Methode allein nicht entscheiden.

## Welche echte Lücke bleibt?

Die bestehende Korpusprüfung unterscheidet ausdrücklich zwischen vorhandener Steam- und Rangintegration und einer eigenständigen Erklärung des Rangsystems im Spiel. Matchmaking, Kalibrierung, sichtbare und verborgene Wertung sowie mögliche Unterstufen sind in der bisherigen öffentlichen Themenstruktur nicht ausreichend als eigene Referenz belegt.

Quelle: `Deadlock-Docs/internal/wissensbasis/faq-korpus-abdeckung.md`, Abschnitt "Lücken für Deadlock-Fragen".

Vor einer Verschiebung nach `public/` braucht dieser Entwurf deshalb aktuelle Primärbelege für das spielseitige Rang- und Matchmaking-System. Die Community-Implementierung kann zuverlässig erklären, welche Rangnamen sie speichert und anzeigt, aber nicht die interne Matchmaking-Entscheidung des Spiels.
