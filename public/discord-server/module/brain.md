---
title: "Wissensabfrage (!brain)"
tags: [discord-server, brain, wissensabfrage]
stand: 2026-07-07
quelle: "Deadlock-Bots/docs/support-kb/modules/brain.html"
---
# Wissensabfrage (!brain)

Mit dem !brain-Befehl stellen Mitglieder eine Deadlock-Frage und bekommen eine KI-gestützte Antwort im Chat. Der Befehl prüft die Frage, bremst Vielfrager kurz aus und teilt lange Antworten Discord-gerecht auf.

## Was Mitglieder merken

Ein Mitglied schreibt !brain mit seiner Frage und bekommt eine Antwort direkt im Chat. Schickt es keine Frage mit, kommt nur ein kurzer Hinweis zur Benutzung. Ist die Frage zu lang, wird sie abgewiesen. Nach einer Frage muss man kurz warten, bevor man erneut fragen kann. Fragen, die nichts mit Deadlock zu tun haben, werden nicht beantwortet. Sehr lange Antworten erscheinen automatisch als mehrere aufeinanderfolgende Nachrichten.

## Mögliche Ausgänge

- Antwort im Chat
- Benutzungshinweis
- Frage-zu-lang-Hinweis
- Wartezeit-Hinweis
- Ausserhalb-des-Themas-Hinweis
- Keine-Antwort-Hinweis
- Technischer-Fehler-Hinweis

## Sichtbare Zustände

| Zustand | Was du siehst | Was es bedeutet | Sicherer nächster Schritt |
| --- | --- | --- | --- |
| Benutzungshinweis | Kurzer Hinweis, wie der Befehl zu benutzen ist | Es wurde keine Frage mitgeschickt | Befehl mit einer konkreten Frage erneut senden |
| Frage zu lang | Meldung, dass die Frage zu lang ist | Die Frage ist länger als erlaubt | Frage kürzer und knapper formulieren |
| Wartezeit | Hinweis, dass man noch kurz warten muss, mit verbleibender Zeit | Kurz zuvor wurde bereits eine Frage gestellt; die Wartezeit läuft noch | Die angezeigte Zeit abwarten und dann erneut fragen |
| Antwort | Die inhaltliche Antwort auf die Frage, bei Bedarf über mehrere Nachrichten verteilt | Kontext gefunden und die KI hat eine Antwort geliefert | Keiner; bei Bedarf nächste Frage nach Ablauf der Wartezeit |
| Ausserhalb des Themas | Hinweis, dass die Frage nicht zum Deadlock-Thema gehört und nicht beantwortet wird | Die Frage wurde als themenfremd eingestuft; die KI wird gar nicht erst befragt | Eine Frage rund um Deadlock stellen |
| Keine Antwort | Hinweis, dass keine Antwort gefunden wurde | Die KI lieferte keine oder eine leere Antwort | Frage anders oder präziser formulieren und erneut versuchen |
| Technischer Fehler | Hinweis auf einen technischen Fehler | Der Kontextabruf oder der KI-Aufruf ist fehlgeschlagen | Später erneut versuchen; bei Dauerproblem das Team informieren |

## So läuft es ab

1. Frage wird bereinigt; ist sie leer, kommt der Benutzungshinweis
2. Zu lange Fragen werden abgewiesen
3. Bei kürzlich gestellter Frage kommt eine Wartezeit-Meldung mit verbleibender Zeit
4. Der Wissenskontext zur Frage wird abgerufen
5. Themenfremde Fragen werden ohne KI-Antwort abgelehnt
6. Andernfalls beantwortet die KI die Frage
7. Eine leere oder fehlende KI-Antwort ergibt einen Keine-Antwort-Hinweis
8. Gültige Antworten werden ausgegeben und bei Überlänge in mehrere Nachrichten aufgeteilt

## Typische Meldungen & Fehler

| Signal | Was es bedeutet | Nächster Schritt |
| --- | --- | --- |
| Wissenskontext nicht erreichbar | Der Dienst, der den Wissenskontext zur Frage liefert, war nicht erreichbar oder fehlerhaft | Später erneut versuchen; bei Dauerproblem das Team informieren |
| Kein verwertbarer Kontext | Der Kontextdienst lieferte nichts Verwertbares zurück | Frage anders formulieren oder später erneut versuchen |
| KI nicht ansprechbar | Die KI-Komponente konnte nicht angesprochen werden | Später erneut versuchen |
| Keine passende Antwort | Die KI hatte keine passende Antwort auf die Frage | Frage präziser oder anders formulieren |

## Befehle

- `!brain`

### Das darf der Support sagen

- Wenn nur ein Benutzungshinweis kommt, wurde keine Frage mitgeschickt; schick !brain mit einer konkreten Frage.
- Nach einer Frage gilt eine kurze Wartezeit; warte die angezeigte Zeit ab und frag dann erneut.
- Fragen ausserhalb des Deadlock-Themas werden bewusst nicht beantwortet; bleib beim Deadlock-Thema.
- Sehr lange Antworten werden automatisch auf mehrere Nachrichten aufgeteilt, das ist normal.

### Nie an Mitglieder weitergeben

- Interne Zahlen jeder Art: Schwellen, Sicherheitswerte, Gewichte, Zeitgrenzen, Limits.
- Die interne Entscheidungs- oder Durchsetzungslogik — welche Signale zu welcher Wirkung führen und in welcher Reihenfolge.
- Interne Technik: IDs, Pfade, Endpunkte, Namespaces, KI-Anbieter oder -Modelle, Zugangsdaten.
- Verdeckte Mechaniken oder Betriebsarten — auch nicht andeutungsweise, welche es geben könnte.
- Im Zweifel abstrahieren und an einen Menschen eskalieren (Details im Agenten-Leitfaden).

**Bewusst nicht dokumentiert:** Schwellenwerte und Zeitgrenzen, verdeckte Mechaniken. Diese internen Details bleiben aus Sicherheitsgründen außerhalb dieser Wissensbasis.
