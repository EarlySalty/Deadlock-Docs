---
title: "Moderationsfall & Einspruch"
tags: [discord-server, moderationsfall, einspruch]
stand: 2026-07-07
quelle: "Deadlock-Bots/docs/support-kb/workflows/moderationsfall-einspruch.html"
---
# Moderationsfall & Einspruch

Der Bot prüft Nachrichten und Bilder im überwachten Kanal in einem überwachten Kanal. Klare schwere Verstöße ahndet er automatisch (Nachricht löschen plus Timeout oder Bann), unklare Fälle legt er dem Mod-Team als Vorschlag vor. Jede Aktion kann das Team wieder zurücknehmen.

## Was Mitglieder merken

Wenn du im überwachten Kanal schreibst und der Bot einen klaren schweren Verstoß erkennt, verschwindet deine Nachricht und du bekommst einen Timeout (du kannst vorübergehend nicht mehr schreiben/sprechen) oder wirst gebannt. In als besonders ruhig markierten Voice-Bereichen bekommst du bei Provokationen zuerst eine freundliche private Hinweis-DM statt einer Strafe. Ist ein Fall nicht eindeutig, bleibt deine Nachricht zunächst stehen und ein Moderator entscheidet später. Hältst du eine Ahndung für falsch, kannst du dich beim Mod-Team melden; das Team kann einen Timeout oder Bann mit einem Klick wieder aufheben.

## Ablauf Schritt für Schritt

1. Der Inhalt wird automatisch auf verbotene Inhalte und verdächtiges Verhalten geprüft.
2. Klare schwere Verstöße werden sofort geahndet: Nachricht gelöscht plus Timeout oder Bann; im Mod-Kanal erscheint ein Fall-Eintrag.
3. Weniger eindeutige Fälle bleiben stehen und werden dem Team als Vorschlag mit Prüf-Buttons vorgelegt.
4. Ein Moderator kann den Vorschlag übernehmen (löschen + Timeout), bannen oder verwerfen (Nachricht bleibt stehen, keine Aktion).
5. Ein Mitglied kann beim Mod-Team Einspruch einlegen; bei Bann über einen zweiten Kontaktweg.
6. Das Team kann eine automatische oder manuelle Strafe wieder aufheben (Timeout aufheben bzw. entbannen); der Fall wird als zurückgenommen markiert.

## Mögliche Ausgänge

- Nachricht gelöscht + Timeout
- Nachricht gelöscht + Bann
- Fall als Vorschlag im Mod-Kanal
- Keine sichtbare Aktion
- Hinweis-DM im ruhig markierten Voice-Bereich
- Timeout aufgehoben
- Account entbannt

## Sichtbare Zustände

| Zustand | Was du siehst | Was es bedeutet | Sicherer nächster Schritt |
| --- | --- | --- | --- |
| Auto-Löschung + Timeout | Die eigene Nachricht verschwindet und man ist für eine feste Zeit stummgeschaltet | Ein klarer schwerer Verstoß wurde mit hoher Sicherheit erkannt und sofort geahndet. | Bei vermutetem Fehler an das Mod-Team wenden; das Team kann den Timeout mit einem Klick aufheben. |
| Auto-Löschung + Bann | Die Nachricht ist weg und der Account ist vom Server gebannt. | Ein sehr schwerer Fall wurde erkannt und sofort mit Bann geahndet. | Über einen zweiten Kontaktweg Einspruch beim Team einlegen; das Team kann entbannen. |
| Zur Prüfung vorgelegt (Vorschlag) | Zunächst nichts, die eigene Nachricht bleibt sichtbar. Ein Moderator entscheidet später. | Der Fall war nicht eindeutig genug für automatische Ahndung und wartet auf eine Team-Entscheidung. | Nichts nötig; das Team übernimmt, bannt oder verwirft den Fall. |
| Hinweis-DM im Ragebaiter-Free-Bereich | Eine private Nachricht mit der Bitte, Provokationen zu reduzieren. | In einem als besonders ruhig markierten Voice-Bereich wurde grenzwertiges Verhalten erkannt; noch keine Strafe. | Tonfall im markierten Bereich anpassen; wiederholtes Verhalten kann das Team prüfen. |
| Aktion zurückgenommen | Ein zuvor gesetzter Timeout/Bann ist wieder aufgehoben. | Das Mod-Team hat den Fall verworfen oder die Strafe manuell zurückgenommen. | Keiner; normal weiter teilnehmen. |

## Typische Meldungen & Fehler

| Signal | Was es bedeutet | Nächster Schritt |
| --- | --- | --- |
| Automatische Ahndung technisch fehlgeschlagen | Der Bot wollte automatisch ahnden, konnte den Timeout/Bann aber nicht durchsetzen (z. B. fehlende Bot-Rechte oder Nutzer schon weg); die Nachricht kann trotzdem gelöscht worden sein. | Team informieren, dass die Aktion technisch fehlschlug; ein Moderator führt sie manuell aus oder verwirft den Fall. |

### Das darf der Support sagen

- Deine Nachricht wurde automatisch entfernt und dein Account bekam einen Timeout oder Bann, weil ein klarer schwerer Verstoß erkannt wurde; wenn du das für falsch hältst, kann das Team es prüfen.
- Das Mod-Team kann einen Timeout oder Bann mit einem Klick wieder aufheben, wenn der Fall verworfen wird.
- Bei einem Bann legst du am besten über einen zweiten Kontaktweg Einspruch beim Team ein.
- In als ruhig markierten Voice-Bereichen kommt bei Provokationen zuerst eine private Hinweis-DM, noch keine Strafe.

### Nie an Mitglieder weitergeben

- Interne Zahlen jeder Art: Schwellen, Sicherheitswerte, Gewichte, Zeitgrenzen, Limits.
- Die interne Entscheidungs- oder Durchsetzungslogik — welche Signale zu welcher Wirkung führen und in welcher Reihenfolge.
- Interne Technik: IDs, Pfade, Endpunkte, Namespaces, KI-Anbieter oder -Modelle, Zugangsdaten.
- Verdeckte Mechaniken oder Betriebsarten — auch nicht andeutungsweise, welche es geben könnte.
- Im Zweifel abstrahieren und an einen Menschen eskalieren (Details im Agenten-Leitfaden).

## Verwandte Seiten

- [Moderation & Scam-Schutz](../module/moderation.md)

**Bewusst nicht dokumentiert:** Schwellenwerte und Zeitgrenzen, Durchsetzungsbedingungen, verdeckte Mechaniken, Bewertungslogik, interne Endpunkte. Diese internen Details bleiben aus Sicherheitsgründen außerhalb dieser Wissensbasis.
