---
title: "Concierge & Support-Hilfe"
tags: [discord-server, faq, chat]
stand: 2026-07-08
quelle: "Deadlock-Bots/docs/support-kb/modules/faq-support.html"
---
# Concierge & Support-Hilfe

Der Concierge beantwortet Server-, Bot- und Concierge-Fragen anhand der Server-Doku. In Support-Tickets hilft er nur automatisch, wenn die Doku eine sichere Antwort hergibt.

## Was Mitglieder merken

Ein Mitglied stellt allgemeine Fragen in <#1491953161747955853> oder direkt per DM an den Bot. Bei Support- oder Moderationsfällen öffnet es ein Ticket in <#1459628609705738539>. Dort kann der Concierge auf die erste Nachricht antworten, aber nur wenn er sicher helfen kann; sonst übernimmt menschlicher Support.

## Mögliche Ausgänge

- hilfreiche Antwort aus der Doku
- bewusstes Schweigen, wenn es keine klare Antwort gibt
- Antwort blockiert bei Sicherheitsverdacht

## Sichtbare Zustände

| Zustand | Was du siehst | Was es bedeutet | Sicherer nächster Schritt |
| --- | --- | --- | --- |
| Concierge-Antwort | Antwort vom Bot in DM, Fragekanal oder Ticket | Die Frage war aus der Server-Doku beantwortbar | Bei Bedarf nachfragen |
| Keine Bot-Antwort im Ticket | Der Concierge bleibt still | Es gab keine sichere Antwort aus der Doku oder das Anliegen braucht Menschen | Auf das Team warten |

## So läuft es ab

1. Mitglied stellt eine Frage in <#1491953161747955853>, per DM oder als erste Nachricht im Ticket
2. Die Frage wird gegen die Server-Doku geprüft
3. Nur sichere Antworten erscheinen
4. Bei Unsicherheit bleibt der Bot still oder verweist auf Menschen

## Typische Meldungen & Fehler

| Signal | Was es bedeutet | Nächster Schritt |
| --- | --- | --- |
| Antwort wurde zurückgehalten | Eine erzeugte Antwort wurde nicht ausgegeben, weil sie möglicherweise interne oder fremde Daten enthalten hätte | Frage anders formulieren oder bei Supportbedarf ein Ticket öffnen |
| Bot antwortet nicht auf die Frage | Der Bot hat in der Doku keine klare Antwort gefunden und schweigt bewusst, statt zu raten | Im Ticket auf menschlichen Support warten |

### Das darf der Support sagen

- Der Bot beantwortet nur Fragen anhand der Server-Doku; findet er nichts Passendes, schweigt er bewusst und ein Mensch übernimmt.
- Antworten werden vor der Ausgabe auf sensible Inhalte geprüft und können zurückgehalten werden - formulier die Frage dann anders oder öffne bei Supportbedarf ein Ticket.
- Der Support-Helfer kann für deine eigene Anfrage begrenzte, geschwärzte Infos heranziehen, aber niemals Daten fremder Accounts.

### Nie an Mitglieder weitergeben

- Interne Zahlen jeder Art: Schwellen, Sicherheitswerte, Gewichte, Zeitgrenzen, Limits.
- Die interne Entscheidungs- oder Durchsetzungslogik — welche Signale zu welcher Wirkung führen und in welcher Reihenfolge.
- Interne Technik: IDs, Pfade, Endpunkte, Namespaces, KI-Anbieter oder -Modelle, Zugangsdaten.
- Verdeckte Mechaniken oder Betriebsarten — auch nicht andeutungsweise, welche es geben könnte.
- Im Zweifel abstrahieren und an einen Menschen eskalieren (Details im Agenten-Leitfaden).

**Bewusst nicht dokumentiert:** verdeckte Mechaniken, interne Endpunkte, Durchsetzungsbedingungen, Schwellenwerte und Zeitgrenzen. Diese internen Details bleiben aus Sicherheitsgründen außerhalb dieser Wissensbasis.
