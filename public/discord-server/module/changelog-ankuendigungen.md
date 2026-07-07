---
title: "Changelog & Ankündigungen"
tags: [discord-server, changelog, ankuendigungen]
stand: 2026-07-07
quelle: "Deadlock-Bots/docs/support-kb/modules/changelog-ankuendigungen.html"
---
# Changelog & Ankündigungen

Über diesen Dienst erscheinen Changelog-/Update-Beiträge, Highlight-Clips und Betriebs-Warnungen als Discord-Nachrichten in festen Kanälen. Mitglieder lösen hier nichts aus; die Beiträge kommen automatisch oder von der Redaktion.

## Was Mitglieder merken

Mitglieder sehen formatierte Beitragskarten mit Titel und Text in bestimmten Kanälen, teils mit mehreren Abschnitten in einer Nachricht, sowie hochgeladene Highlight-Clips zu Matches. Manche Beiträge lösen zusätzlich eine Rollen-Benachrichtigung aus, sodass die angesprochene Rolle angepingt wird. Ein Mitglied selbst startet nichts davon; die Inhalte werden automatisch bzw. von der Redaktion veröffentlicht.

## Mögliche Ausgänge

- Beitrag erscheint für Mitglieder im gewählten Kanal.
- Ein mehrteiliger Beitrag erscheint, ggf. mit @Rolle-Ping; eine frühere Fassung wird ersetzt.
- Übersicht plus einzelne Highlight-Clips erscheinen im Kanal; manche Clips werden nicht übernommen.
- Der Betriebs-/Monitor-Kanal zeigt eine Warnung; bei ernsteren Stufen wird der Betrieb benachrichtigt.
- Bei Fehler erscheint nichts.

## Sichtbare Zustände

| Zustand | Was du siehst | Was es bedeutet | Sicherer nächster Schritt |
| --- | --- | --- | --- |
| Changelog-Beitrag sichtbar | Eine Beitragskarte mit Titel (mit Klemmbrett-Symbol) und Text im Update-Kanal, mit Zeitstempel und Fußzeile. | Ein neuer Changelog-/Update-Eintrag wurde veröffentlicht. | Einfach lesen; keine Aktion nötig. |
| Twitch-Changelog sichtbar | Dieselbe Art Beitragskarte, jedoch im Twitch-bezogenen Kanal mit passender Fußzeile. | Der Beitrag betrifft den Twitch-Teil und wurde im zugehörigen Kanal gepostet. | Einfach lesen; keine Aktion nötig. |
| Mehrteiliger Beitrag mit Rollen-Ping | Eine Nachricht mit mehreren Abschnitten und ggf. einer Benachrichtigung (@Rolle) an eine bestimmte Rolle. | Ein umfangreicherer Beitrag; wer die angesprochene Rolle hat, wird benachrichtigt. | Beitrag lesen; die Benachrichtigung ist beabsichtigt. |
| Highlight-Clips gepostet | Eine Übersichtskarte 'Highlights — <Streamer> (Match #…)' gefolgt von einzelnen Video-Clips als Datei-Anhänge. | Zu einem Match wurden Highlight-Clips hochgeladen. | Clips anschauen; keine Aktion nötig. |
| Aktualisierter Beitrag | Ein früherer Beitrag ist verschwunden und durch eine neue Version ersetzt. | Der Beitrag wurde neu veröffentlicht und die alte Fassung entfernt. | Die aktuelle Fassung lesen. |

## So läuft es ab

1. Ein interner Aufruf mit Titel, Inhalt und Ziel geht ein (Standard: allgemeiner Update-Kanal; alternativ Twitch-Kanal oder direkter Kanal).
2. Die Berechtigung des Aufrufs wird geprüft.
3. Titel und Inhalt werden validiert.
4. Der Zielkanal wird anhand des Ziels bestimmt.
5. Eine Beitragskarte wird in den Kanal gepostet; bei mehrteiligen Beiträgen erscheinen mehrere Abschnitte als eine Nachricht, ggf. mit Rollen-Ping, und eine frühere Fassung kann ersetzt werden.
6. Bei Highlight-Clips wird eine Übersichtskarte gepostet und jeder Clip als Datei angehängt.
7. Bei Betriebs-Warnungen wird eine farbcodierte Warnkarte im Monitor-Kanal gepostet, bei ernsteren Stufen zusätzlich mit Ping an den Betrieb.

## Typische Meldungen & Fehler

| Signal | Was es bedeutet | Nächster Schritt |
| --- | --- | --- |
| Beitrag erscheint gar nicht, obwohl er angekündigt war | Der interne Aufruf hatte keine gültige Berechtigung; der Beitrag wurde nicht gepostet und ist für Mitglieder nicht sichtbar. | Kein Mitglieder-Handeln; Redaktion/Betrieb prüft die Zugangsdaten des aufrufenden Dienstes. |
| Beitrag wurde abgewiesen, weil er unvollständig oder falsch adressiert war | Dem Beitrag fehlten Pflichtangaben oder das Ziel war ungültig, deshalb wurde nichts veröffentlicht. | Kein Mitglieder-Handeln; die Redaktion korrigiert den Beitrag und sendet erneut. |
| Zielkanal nicht erreichbar, nichts erscheint | Der Zielkanal existiert nicht (mehr) oder ist nicht erreichbar. | Kein Mitglieder-Handeln; Betrieb prüft die Kanal-Konfiguration. |
| Beitrag oder Clip kam gar nicht oder nur teilweise an | Beim Senden an Discord ging etwas schief. | Kein Mitglieder-Handeln; erneuter Versuch durch den Absender. |

### Das darf der Support sagen

- Changelog- und Update-Beiträge in diesen Kanälen werden zentral eingespeist und automatisch bzw. von der Redaktion gepostet; du musst dafür nichts tun.
- Wenn ein Beitrag eine @Rolle anpingt, ist das beabsichtigt und richtet sich an alle mit dieser Rolle.
- Wenn ein früherer Beitrag verschwunden und durch eine neue Version ersetzt ist, gilt die aktuelle Fassung.
- Erscheint ein angekündigter Beitrag gar nicht, liegt das an der Veröffentlichung selbst; die Redaktion/der Betrieb schaut das an, ein Mitglied kann nichts nachjustieren.

### Nie an Mitglieder weitergeben

- Interne Zahlen jeder Art: Schwellen, Sicherheitswerte, Gewichte, Zeitgrenzen, Limits.
- Die interne Entscheidungs- oder Durchsetzungslogik — welche Signale zu welcher Wirkung führen und in welcher Reihenfolge.
- Interne Technik: IDs, Pfade, Endpunkte, Namespaces, KI-Anbieter oder -Modelle, Zugangsdaten.
- Verdeckte Mechaniken oder Betriebsarten — auch nicht andeutungsweise, welche es geben könnte.
- Im Zweifel abstrahieren und an einen Menschen eskalieren (Details im Agenten-Leitfaden).

**Bewusst nicht dokumentiert:** Zugangsdaten, Bewertungslogik, interne Endpunkte, Schwellenwerte und Zeitgrenzen, verdeckte Mechaniken. Diese internen Details bleiben aus Sicherheitsgründen außerhalb dieser Wissensbasis.
