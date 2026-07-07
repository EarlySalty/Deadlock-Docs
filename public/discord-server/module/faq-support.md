---
title: "FAQ & Support-Chat"
tags: [discord-server, faq, chat]
stand: 2026-07-07
quelle: "Deadlock-Bots/docs/support-kb/modules/faq-support.html"
---
# FAQ & Support-Chat

Der FAQ-/Support-Chat gibt Mitgliedern einen privaten Kanal, in dem der Bot Fragen anhand der Server-Doku beantwortet. Antworten werden vor der Ausgabe geprüft, und wenn nichts Passendes gefunden wird, schweigt der Bot bewusst.

## Was Mitglieder merken

Ein Mitglied startet über das FAQ-/Support-Panel eine Session und bekommt dafür einen eigenen, privaten Textkanal. Dort kann es Fragen stellen und erhält Antworten, die aus der Doku stammen und von einem Sprachmodell formuliert werden. Die Session lässt sich per Schliessen-Button beenden und schliesst sonst nach längerer Inaktivität automatisch. Manche Antworten kommen kurz, manche werden zurückgehalten, und wenn es keine klare Antwort gibt, meldet sich stattdessen menschlicher Support.

## Mögliche Ausgänge

- hilfreiche Antwort aus der Doku
- bewusstes Schweigen, wenn es keine klare Antwort gibt
- Antwort blockiert bei Sicherheitsverdacht

## Sichtbare Zustände

| Zustand | Was du siehst | Was es bedeutet | Sicherer nächster Schritt |
| --- | --- | --- | --- |
| FAQ-Chat offen | Privater Textkanal in der FAQ-Kategorie mit Bot-Antworten und einem Schliessen-Button | Eine FAQ-Session läuft; Antworten stammen aus der Doku und einem Sprachmodell | Frage stellen oder mit dem Schliessen-Button beenden |
| FAQ-Session abgelaufen | Der Kanal wird nach längerer Inaktivität automatisch geschlossen | Die Session wurde wegen längerer Inaktivität beendet | Über das Panel eine neue Session starten |

## So läuft es ab

1. Mitglied klickt den FAQ-Panel-Button oder schreibt die erste Nachricht in einem neuen Ticket-Kanal
2. Ein privater Kanal wird eröffnet
3. Fragen werden gegen die Doku geprüft und per Sprachmodell beantwortet
4. Antworten durchlaufen eine Redigier-/Sicherheitsprüfung, bevor sie erscheinen
5. Die Session schliesst per Button oder automatisch nach längerer Inaktivität

## Typische Meldungen & Fehler

| Signal | Was es bedeutet | Nächster Schritt |
| --- | --- | --- |
| Antwort wurde zurückgehalten | Eine erzeugte Antwort wurde nicht ausgegeben, weil sie möglicherweise interne oder fremde Daten enthalten hätte | Frage anders formulieren oder über ein Ticket den Support nutzen |
| Bot antwortet nicht auf die Frage | Der Bot hat in der Doku keine klare Antwort gefunden und schweigt bewusst, statt zu raten | Im Ticket auf menschlichen Support warten |

### Das darf der Support sagen

- Der Bot beantwortet im FAQ-Chat nur Fragen anhand der Server-Doku; findet er nichts Passendes, schweigt er bewusst und ein Mensch übernimmt.
- Antworten werden vor der Ausgabe auf sensible Inhalte geprüft und können zurückgehalten werden - formulier die Frage dann anders oder öffne ein Ticket.
- Wenn dein FAQ-Kanal automatisch geschlossen wurde, lag längere Inaktivität vor; starte einfach über das Panel eine neue Session.
- Der Support-Helfer kann für deine eigene Anfrage begrenzte, geschwärzte Infos heranziehen, aber niemals Daten fremder Accounts.

### Nie an Mitglieder weitergeben

- Interne Zahlen jeder Art: Schwellen, Sicherheitswerte, Gewichte, Zeitgrenzen, Limits.
- Die interne Entscheidungs- oder Durchsetzungslogik — welche Signale zu welcher Wirkung führen und in welcher Reihenfolge.
- Interne Technik: IDs, Pfade, Endpunkte, Namespaces, KI-Anbieter oder -Modelle, Zugangsdaten.
- Verdeckte Mechaniken oder Betriebsarten — auch nicht andeutungsweise, welche es geben könnte.
- Im Zweifel abstrahieren und an einen Menschen eskalieren (Details im Agenten-Leitfaden).

**Bewusst nicht dokumentiert:** verdeckte Mechaniken, interne Endpunkte, Durchsetzungsbedingungen, Schwellenwerte und Zeitgrenzen. Diese internen Details bleiben aus Sicherheitsgründen außerhalb dieser Wissensbasis.
