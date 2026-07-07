---
title: "Tierlist & Builds"
tags: [discord-server, tierlist, builds]
stand: 2026-07-07
quelle: "Deadlock-Bots/docs/support-kb/modules/tierlist-builds.html"
---
# Tierlist & Builds

Zeigt die öffentliche Helden-Tierlist mit Builds, Streamer-Empfehlungen und Community-Abstimmung über Builds. Die Daten werden regelmäßig automatisch aus einer externen Statistik-Quelle aktualisiert.

## Was Mitglieder merken

Mitglieder sehen eine nach Stufen (S+ bis C) sortierte Helden-Tierlist mit Winrate, einem Trendpfeil zur letzten Auswertung, der Matchzahl, einer Kurzbeschreibung sowie empfohlenen Builds und Streamern. Es gibt mehrere Rang-Ansichten derselben Liste, zwischen denen man wechseln kann. Zu jedem Build können Mitglieder mit Daumen hoch oder runter abstimmen; beliebtere Builds rücken in der Anzeige nach oben. Nur Ansehen und Bewerten ist für reguläre Mitglieder möglich; Inhalte pflegen kann nur das Team.

## Mögliche Ausgänge

- Gefüllte Tierlist für die gewählte Ansicht
- Leere Tierlist, falls noch kein Snapshot vorliegt
- Build-Stimme gezählt
- Abstimmung kurzzeitig geblockt bei zu schnellem erneuten Voten
- Fehler, wenn der Build nicht mehr existiert

## Sichtbare Zustände

| Zustand | Was du siehst | Was es bedeutet | Sicherer nächster Schritt |
| --- | --- | --- | --- |
| Tierlist angezeigt | Helden in Stufen S+/S/A/B/C mit Winrate, Trendpfeil, Matchzahl, Beschreibung, Builds und Streamern | Für die gewählte Rang-Ansicht liegt ein aktueller Auswertungs-Snapshot vor | Ansicht wechseln, um andere Rangbereiche zu sehen |
| Held fehlt in der Liste | Ein erwarteter Held taucht nicht auf | Der Held hat in dieser Auswertung zu wenige gewertete Matches oder ist nicht aktiv | Später erneut schauen; wenig gespielte Helden erscheinen zeitweise nicht |
| Leere Tierlist | Stufen ohne Helden, keine Patch-/Aktualisierungsangabe | Für diese Ansicht liegt noch kein Auswertungs-Snapshot vor | Warten, bis die nächste automatische Aktualisierung gelaufen ist |
| Trendpfeil an einem Helden | Positive oder negative Winrate-Änderung | Vergleich zur vorherigen Auswertung derselben Ansicht | Kein Handlungsbedarf; rein informativ |
| Abstimmung erfolgreich | Aktualisierte Daumen-hoch/runter-Zahlen für den Build | Die Stimme wurde gezählt | Vor der nächsten Stimme kurz warten |
| Abstimmung geblockt | Hinweis, kurz zu warten | Es wurde zu schnell hintereinander abgestimmt | Kurz warten und erneut abstimmen |

## So läuft es ab

1. Rang-Ansicht der Tierlist wählen
2. Helden erscheinen in Stufen S+ bis C, nach Winrate sortiert
3. Pro Held zeigen sich Winrate, Trend zur letzten Auswertung, Matchzahl, Beschreibung, Builds und Streamer
4. An einem Build mit Daumen hoch oder runter abstimmen
5. Die Stimme wird gezählt, sofern nicht zu schnell hintereinander abgestimmt wurde
6. Aktualisierte Stimmzahlen erscheinen; beliebtere Builds rücken nach oben

## Typische Meldungen & Fehler

| Signal | Was es bedeutet | Nächster Schritt |
| --- | --- | --- |
| Gewählte Rang-Ansicht existiert nicht | Die aufgerufene Rang-Ansicht der Tierlist gibt es nicht | Eine der angebotenen Ansichten wählen |
| Build zur Abstimmung nicht erkannt | Die Zuordnung des Builds bei der Abstimmung ist ungültig | Seite neu laden und erneut abstimmen |
| Stimme war weder hoch noch runter | Die abgegebene Stimme war keine gültige Daumen-hoch/runter-Wertung | Über die regulären Buttons abstimmen |
| Anfrage fehlerhaft aufgebaut | Die Abstimmungs-Anfrage kam beschädigt an | Seite neu laden und erneut versuchen |
| Build existiert nicht mehr | Der Build zu dieser Stimme wurde vermutlich entfernt | Seite neu laden |
| Zu schnell erneut abgestimmt | Es wurde in zu kurzem Abstand erneut abgestimmt und die Stimme wurde vorerst geblockt | Kurz warten und erneut abstimmen |
| Externe Statistik-Quelle war nicht erreichbar | Bei einer Aktualisierung war die externe Statistik-Quelle nicht erreichbar | Kein Handlungsbedarf; die nächste automatische Aktualisierung versucht es erneut |
| Interner Serverfehler | Auf Serverseite ist etwas schiefgelaufen | Später erneut versuchen; bei Dauerproblem ans Team |
| Zugriff auf Verwaltung ohne Team-Anmeldung | Verwaltungsfunktionen wurden ohne gültige Team-Anmeldung aufgerufen | Nur für Team-Admins; reguläre Mitglieder brauchen das nicht |

### Das darf der Support sagen

- Die Tierlist gibt es in mehreren Rang-Ansichten; dieselbe Held-Winrate kann je Ansicht abweichen. Wechsel die Ansicht, um andere Rangbereiche zu sehen.
- Wenn ein Held fehlt, hat er in dieser Auswertung meist zu wenige gewertete Matches. Schau später noch einmal.
- Die Zahlen kommen aus einer externen Statistik-Quelle und werden in festen Abständen automatisch aktualisiert, hinken dem Live-Spiel also etwas hinterher.
- Wenn die Abstimmung geblockt wird, wurde zu schnell hintereinander gevotet - kurz warten und erneut abstimmen.

### Nie an Mitglieder weitergeben

- Interne Zahlen jeder Art: Schwellen, Sicherheitswerte, Gewichte, Zeitgrenzen, Limits.
- Die interne Entscheidungs- oder Durchsetzungslogik — welche Signale zu welcher Wirkung führen und in welcher Reihenfolge.
- Interne Technik: IDs, Pfade, Endpunkte, Namespaces, KI-Anbieter oder -Modelle, Zugangsdaten.
- Verdeckte Mechaniken oder Betriebsarten — auch nicht andeutungsweise, welche es geben könnte.
- Im Zweifel abstrahieren und an einen Menschen eskalieren (Details im Agenten-Leitfaden).

## Verwandte Seiten

- [Über Builds abstimmen](../workflows/builds-abstimmen.md)

**Bewusst nicht dokumentiert:** Schwellenwerte und Zeitgrenzen, Ranking- und Sortierlogik, Missbrauchsabwehr, interne Endpunkte, sonstige interne Details, verdeckte Mechaniken. Diese internen Details bleiben aus Sicherheitsgründen außerhalb dieser Wissensbasis.
