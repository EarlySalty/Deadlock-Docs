---
title: "Über Builds abstimmen"
tags: [discord-server, builds, abstimmen, ueber]
stand: 2026-07-07
quelle: "Deadlock-Bots/docs/support-kb/workflows/builds-abstimmen.html"
---
# Über Builds abstimmen

Mitglieder können zu jedem Build in der Helden-Tierlist mit Daumen hoch oder runter abstimmen. Beliebtere Builds rücken in der Anzeige nach oben.

## Was Mitglieder merken

Unter den empfohlenen Builds eines Helden gibt es Daumen-hoch- und Daumen-runter-Buttons. Nach einer Stimme aktualisieren sich die Up-/Downvote-Zahlen des Builds. Wer zu schnell hintereinander abstimmt, wird kurz geblockt und sieht einen Hinweis, kurz zu warten. Über die Zeit verändert das gemeinsame Abstimmen die Reihenfolge: Builds mit mehr Zustimmung erscheinen weiter oben. Die Abstimmung ist anonym, deshalb sind die Zahlen ein grober Community-Trend und keine exakte Zählung.

## Ablauf Schritt für Schritt

1. An einem Build den Daumen hoch oder runter anklicken
2. Die Stimme wird gezählt, sofern nicht zu schnell hintereinander abgestimmt wurde
3. Die aktualisierten Up-/Downvote-Zahlen erscheinen am Build
4. Beliebtere Builds rücken in der Anzeige nach oben

## Mögliche Ausgänge

- Stimme gezählt
- Kurzzeitig geblockt bei zu schnellem erneuten Abstimmen
- Fehler, wenn der Build nicht mehr existiert

## Sichtbare Zustände

| Zustand | Was du siehst | Was es bedeutet | Sicherer nächster Schritt |
| --- | --- | --- | --- |
| Abstimmung erfolgreich | Aktualisierte Up-/Downvote-Zahlen für den Build | Die Stimme wurde gezählt | Vor der nächsten Stimme kurz warten |
| Abstimmung geblockt | Hinweis, kurz zu warten | Abstimmung aktuell nicht möglich – bitte später erneut versuchen | Kurz warten und erneut abstimmen |
| Build weiter oben in der Liste | Ein beliebterer Build erscheint höher unter den Empfehlungen | Builds werden unter anderem nach Zustimmung/Ablehnung sortiert | Mit Daumen hoch/runter mitgestalten |

## Typische Meldungen & Fehler

| Signal | Was es bedeutet | Nächster Schritt |
| --- | --- | --- |
| Meldung, dass zu schnell erneut abgestimmt wurde | Es wurde zu schnell hintereinander abgestimmt | Kurz warten und erneut abstimmen |
| Der Build zur Stimme existiert nicht mehr | Der Build wurde vermutlich entfernt | Seite neu laden und erneut versuchen |
| Die Stimme wird nicht angenommen (ungültige Auswahl) | Es wurde weder klar 'hoch' noch 'runter' übermittelt | Über die regulären Daumen-Buttons abstimmen |
| Die Abstimmung schlägt fehl, Seite reagiert fehlerhaft | Die Anfrage war fehlerhaft aufgebaut oder ein interner Fehler trat auf | Seite neu laden und erneut versuchen; bei Dauerproblem ans Team |

### Das darf der Support sagen

- Du kannst zu jedem Build mit Daumen hoch oder runter abstimmen; Builds mit mehr Zustimmung erscheinen weiter oben.
- Wenn du zu schnell hintereinander abstimmst, wird die Stimme kurz geblockt: einfach kurz warten und erneut abstimmen.
- Wird ein Build nicht mehr gefunden, lade die Seite neu; er wurde vermutlich entfernt.
- Die Abstimmung ist anonym, die Zahlen zeigen einen groben Community-Trend und keine exakte Zählung.

### Nie an Mitglieder weitergeben

- Interne Zahlen jeder Art: Schwellen, Sicherheitswerte, Gewichte, Zeitgrenzen, Limits.
- Die interne Entscheidungs- oder Durchsetzungslogik — welche Signale zu welcher Wirkung führen und in welcher Reihenfolge.
- Interne Technik: IDs, Pfade, Endpunkte, Namespaces, KI-Anbieter oder -Modelle, Zugangsdaten.
- Verdeckte Mechaniken oder Betriebsarten — auch nicht andeutungsweise, welche es geben könnte.
- Im Zweifel abstrahieren und an einen Menschen eskalieren (Details im Agenten-Leitfaden).

## Verwandte Seiten

- [Tierlist & Builds](../module/tierlist-builds.md)

**Bewusst nicht dokumentiert:** Schwellenwerte und Zeitgrenzen, Ranking- und Sortierlogik, Missbrauchsabwehr, interne Endpunkte, verdeckte Mechaniken, sonstige interne Details. Diese internen Details bleiben aus Sicherheitsgründen außerhalb dieser Wissensbasis.
