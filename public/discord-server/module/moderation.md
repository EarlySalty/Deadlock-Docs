---
title: "Moderation & Scam-Schutz"
tags: [discord-server, moderation, scam, schutz]
stand: 2026-07-07
quelle: "Deadlock-Bots/docs/support-kb/modules/moderation.html"
---
# Moderation & Scam-Schutz

Der Bot prüft in einem überwachten Kanal Nachrichten und Bilder per KI, ahndet klare schwere Verstöße selbst (Löschen plus Timeout oder Bann) und legt Grenzfälle dem Mod-Team als Vorschlag vor. Jede Aktion kann das Team wieder zurücknehmen.

## Was Mitglieder merken

Wer im überwachten Kanal schreibt oder ein Bild postet, dessen Beitrag wird automatisch auf verbotene Inhalte und verdächtiges Verhalten geprüft. Bei einem klaren schweren Verstoß verschwindet die Nachricht sofort und der Account bekommt einen Timeout oder Bann. Weniger eindeutige Fälle bleiben zunächst stehen und werden dem Moderationsteam mit Prüf-Buttons vorgelegt, das dann entscheidet. In Voice-Bereichen, die als „Ragebaiter-Free“ markiert sind, gibt es bei Provokationen zuerst eine freundliche private Hinweis-Nachricht statt einer Strafe. Timeouts und Banns kann das Team jederzeit wieder aufheben.

## Mögliche Ausgänge

- Nachricht gelöscht + Timeout
- Nachricht gelöscht + Bann
- Fall als Vorschlag im Mod-Kanal
- Keine sichtbare Aktion
- Hinweis-DM im Ragebaiter-Free-Bereich
- Timeout aufgehoben / Account entbannt

## Sichtbare Zustände

| Zustand | Was du siehst | Was es bedeutet | Sicherer nächster Schritt |
| --- | --- | --- | --- |
| Auto-Löschung + Timeout | Die eigene Nachricht verschwindet und man ist für eine feste Zeit stummgeschaltet (kann nicht mehr schreiben/sprechen) | Ein klarer schwerer Verstoß wurde mit hoher Sicherheit erkannt und sofort geahndet. | Bei vermutetem Fehler an das Mod-Team wenden; das Team kann den Timeout mit einem Klick aufheben. |
| Auto-Löschung + Bann | Die Nachricht ist weg und der Account ist vom Server gebannt. | Ein sehr schwerer Fall wurde erkannt und sofort mit Bann geahndet. | Über einen zweiten Kontakt Einspruch beim Team einlegen; das Team kann entbannen. |
| Zur Prüfung vorgelegt (Vorschlag) | Zunächst nichts - die eigene Nachricht bleibt sichtbar. Ein Moderator entscheidet später. | Der Fall war nicht eindeutig genug für automatische Ahndung und wartet auf eine Team-Entscheidung. | Nichts nötig; das Team übernimmt, bannt oder verwirft den Fall. |
| Hinweis-DM im Ragebaiter-Free-Bereich | Eine private Nachricht mit der Bitte, Provokationen zu reduzieren. | In einem als besonders ruhig markierten Voice-Bereich wurde grenzwertiges Verhalten erkannt; noch keine Strafe. | Tonfall im markierten Bereich anpassen; wiederholtes Verhalten kann das Team prüfen. |
| Aktion zurückgenommen | Ein zuvor gesetzter Timeout/Bann ist wieder aufgehoben. | Das Mod-Team hat den Fall verworfen oder die Strafe manuell zurückgenommen. | Keiner; normal weiter teilnehmen. |

## So läuft es ab

1. Ein Mitglied schreibt eine Nachricht oder postet ein Bild im überwachten Kanal.
2. Der Beitrag wird automatisch auf verbotene Inhalte und verdächtiges Verhalten geprüft.
3. Je nach Ergebnis folgt: automatische Ahndung, Vorlage als Vorschlag an das Team oder keine Aktion.
4. Bei automatischer Ahndung wird die Nachricht gelöscht und ein Timeout oder Bann gesetzt; im Mod-Kanal erscheint ein Fall-Eintrag.
5. Bei einem Vorschlag entscheidet ein Moderator per Buttons: übernehmen, bannen oder verwerfen.
6. Gesetzte Timeouts und Banns kann das Team später wieder aufheben.

## Typische Meldungen & Fehler

| Signal | Was es bedeutet | Nächster Schritt |
| --- | --- | --- |
| Automatische Ahndung schlug technisch fehl | Der Bot wollte automatisch ahnden, konnte den Timeout oder Bann aber nicht durchsetzen (z. B. fehlende Bot-Rechte oder der Nutzer war schon weg); die Nachricht kann trotzdem gelöscht worden sein. | Team informieren, dass die Aktion technisch fehlschlug; ein Moderator führt sie manuell aus oder verwirft den Fall. |

### Das darf der Support sagen

- Der überwachte Kanal wird automatisch geprüft; klare schwere Verstöße werden sofort gelöscht und mit Timeout oder Bann geahndet.
- Weniger eindeutige Fälle werden nicht automatisch bestraft, sondern dem Mod-Team als Vorschlag vorgelegt - die Nachricht bleibt bis zur Entscheidung stehen.
- Jeder automatische Timeout oder Bann kann vom Team wieder aufgehoben werden; bei einem vermuteten Fehler soll sich das Mitglied ans Mod-Team wenden.
- In Ragebaiter-Free-Voice-Bereichen kommt bei Provokationen zuerst eine freundliche Hinweis-DM, noch keine Strafe.

### Nie an Mitglieder weitergeben

- Interne Zahlen jeder Art: Schwellen, Sicherheitswerte, Gewichte, Zeitgrenzen, Limits.
- Die interne Entscheidungs- oder Durchsetzungslogik — welche Signale zu welcher Wirkung führen und in welcher Reihenfolge.
- Interne Technik: IDs, Pfade, Endpunkte, Namespaces, KI-Anbieter oder -Modelle, Zugangsdaten.
- Verdeckte Mechaniken oder Betriebsarten — auch nicht andeutungsweise, welche es geben könnte.
- Im Zweifel abstrahieren und an einen Menschen eskalieren (Details im Agenten-Leitfaden).

## Verwandte Seiten

- [Moderationsfall & Einspruch](../workflows/moderationsfall-einspruch.md)

**Bewusst nicht dokumentiert:** Schwellenwerte und Zeitgrenzen, Durchsetzungsbedingungen, verdeckte Mechaniken, interne Endpunkte. Diese internen Details bleiben aus Sicherheitsgründen außerhalb dieser Wissensbasis.
