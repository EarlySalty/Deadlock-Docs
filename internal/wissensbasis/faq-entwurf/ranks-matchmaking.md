# FAQ-Entwurf: Ranks und Matchmaking

status: entwurf  
stand: 2026-09-19  
quelle: `Deadlock-Bots` Commit `bb03deb53b28a7266de83748c3b834bff9c9a205`, Korpuslücke aus `Deadlock-Docs`

Nicht für `public/` freigegeben.

## Welche Rangnamen erkennt die Community-Statistik?

`RANK_ORDER` führt elf Rangfamilien, von Initiate bis Eternus, `Deadlock-Bots/rust/crates/dl-stats/src/ranks.rs:13-25`.

Das ist die vom Community-Code akzeptierte Rangnamensliste am geprüften Commit. Sie ist kein Beleg für die interne Matchmaking-Formel des Spiels.

## Woher kommt der angezeigte Rang?

`RankResolver::rank_of` beginnt in `Deadlock-Bots/rust/crates/dl-stats/src/ranks.rs:59`. Die Abfrage liest `deadlock_rank_name` aus `core.steam_links` für die Discord-ID, verlangt eine verifizierte Verknüpfung und bevorzugt den primären Account sowie den jüngeren Rangstand, `Deadlock-Bots/rust/crates/dl-stats/src/ranks.rs:63-72`.

Anschließend wird der Name normalisiert und gegen `RANK_ORDER` geprüft, `Deadlock-Bots/rust/crates/dl-stats/src/ranks.rs:74-79`.

## Ist der sichtbare Rang dasselbe wie MMR?

Aus diesem Code lässt sich das nicht ableiten. Das Modul liest einen gespeicherten Rangnamen. Es berechnet keine Matchmaking-Wertung und bildet keine spielinterne Matchmaking-Entscheidung nach, siehe den vollständigen Rangpfad in `Deadlock-Bots/rust/crates/dl-stats/src/ranks.rs:53-82`.

## Warum kann ein Rang fehlen?

Auf Codeebene braucht die Anzeige eine passende Discord-ID, eine verifizierte Steam-Verknüpfung, einen gesetzten Rangnamen und einen Namen aus `RANK_ORDER`, `Deadlock-Bots/rust/crates/dl-stats/src/ranks.rs:59-79`.

Ob ein fehlender oder alter Wert durch externe Daten, Refresh-Verzögerung oder eine Änderung im Spiel entsteht, entscheidet diese Methode nicht.

## Was fehlt für eine echte Matchmaking-FAQ?

Die Korpusprüfung trennt vorhandene Ranganzeige und Community-Rollen ausdrücklich von Rangberechnung, MMR und Matchmaking-Regeln, `Deadlock-Docs/internal/wissensbasis/faq-korpus-abdeckung.md:166-175`.

Vor einer Übernahme nach `public/` braucht dieser Entwurf deshalb aktuelle Primärbelege für Platzierung, Auf- und Abstieg, sichtbare oder verborgene Wertung sowie Gruppen-Matchmaking. Der Community-Code kann zuverlässig erklären, was er speichert und anzeigt, nicht die interne Matchmaking-Entscheidung des Spiels.
