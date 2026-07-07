---
title: "Mitspielersuche (LFG)"
tags: [discord-server, mitspielersuche, lfg]
stand: 2026-07-07
quelle: "Deadlock-Bots/docs/support-kb/modules/mitspielersuche-lfg.html"
---
# Mitspielersuche (LFG)

Die Mitspielersuche (LFG) hilft Mitgliedern, für Deadlock-Runden zusammenzufinden: Der Bot schlägt passende Voice-Lobbys vor, man kann eigene Gesuche veröffentlichen und sich bei passenden Gesuchen benachrichtigen lassen. Dazu gehören der Smartping als Staff-Anstoß und das Scrim-/Squad-Programm als organisierte Team-Ebene.

## Was Mitglieder merken

Wer im LFG-Kanal eine erkennbare Suchnachricht schreibt (z. B. "suche Mitspieler" oder einen Ranked-Hinweis), bekommt vom Bot ein "Lobby-Finder"-Embed mit vorgeschlagenen Voice-Lobbys, die zu Rang und Umfeld passen, plus dem Hinweis, notfalls selbst eine Lane aufzumachen. Über ein LFG-Panel lässt sich außerdem ein eigenes Mitspieler-Gesuch als sichtbarer Forum-Post mit Beitreten-Button erstellen; wer einen passenden Watch-Filter gesetzt hat, erhält dazu einmalig eine DM. Manchmal antwortet der Bot bewusst nicht. Über das Scrim-/Squad-Programm kann man sich per Discord-Reaktion oder Webanmeldung als Interessent eintragen und wird später von der Orga einem Team zugeteilt; den eigenen Status (neu, im Team, Bank, Warteliste) verwaltet die Scrim-Organisation.

## Mögliche Ausgänge

- Antwort-Embed mit passenden Lobby-Vorschlägen
- Sichtbares LFG-Gesuch als Forum-Post mit Beitreten-Button
- Gematchte Mitspieler bzw. einmalige Benachrichtigung an Watcher
- Keine Antwort bei kurzer Pause, oder nicht erkannter Absicht
- Scrim-Teilnehmer im Pool erfasst und bereit für eine Team-Zuteilung

## Sichtbare Zustände

| Zustand | Was du siehst | Was es bedeutet | Sicherer nächster Schritt |
| --- | --- | --- | --- |
| LFG-Antwort erhalten | Ein Embed "Lobby-Finder" mit einer oder mehreren vorgeschlagenen Lobbys und dem Hinweis, selbst eine Lane aufzumachen. | Die Nachricht wurde als Lobby-Suche erkannt und passende Voice-Lanes wurden zugeordnet. | In eine der vorgeschlagenen Lobbys springen oder selbst eine aufmachen. |
| Keine LFG-Antwort | Der Bot antwortet nicht auf die Suchnachricht. | Der Bot hat auf dieses Gesuch bewusst nicht geantwortet. | Kurz warten und es mit einer klaren Suchnachricht erneut versuchen. |
| LFG-Gesuch erstellt | Ein eigener Forum-Post mit Modus, Rang-Bereich und Beitreten-Button; er räumt sich selbst weg, wenn die Lane schließt. | Die Mitspieler-Suche wurde als sichtbares Gesuch veröffentlicht. | Auf Beitritte warten oder selbst per Beitreten in andere Lanes springen. |
| LFG-Benachrichtigung | Eine DM mit Hinweis auf ein passendes Gesuch und einem Link zum Thread. | Ein neues Gesuch passt zum gesetzten Watch-Filter (einmalige Benachrichtigung). | Thread öffnen; für weitere Treffer den Watch erneut aktivieren. |
| Smartping blockiert | Hinweis, dass dieses Mitglied gerade nicht gepingt werden kann. | Die Zielperson erfüllt gerade nicht die Bedingungen, um angepingt zu werden, oder hat Opt-out. | Später erneut versuchen; wiederholte Blockierung ist normal und beabsichtigt. |
| Scrim: neu im Pool | Man ist als Scrim-Interessent erfasst, aber noch keinem Team zugeteilt. | Anfangszustand nach Anmeldung per Discord-Reaktion oder Webanmeldung. | Abwarten, bis die Scrim-Organisation eine Team-Zuteilung vornimmt. |
| Scrim: einem Team zugeteilt | Man ist festes Mitglied eines Scrim-Teams. | Man wurde einem Team als spielendes Mitglied hinzugefügt. | Keine Aktion nötig; über das zugeordnete Team spielen. |
| Scrim: Ersatzbank | Man gehört zu einem Team, ist aber als Ersatz/Bank markiert. | Team-Mitgliedschaft mit Bank-Kennzeichen. | Bei Bedarf mit der Scrim-Organisation klären, ob ein Aufrücken möglich ist. |
| Scrim: Warteliste | Man ist angemeldet, steht aber im nicht zugeteilten Pool auf der Warteliste. | Es ist noch kein Team-Platz zugeteilt. | Warten, bis ein Platz frei wird oder die Organisation zuteilt. |

## So läuft es ab

1. Ein Mitglied schreibt im LFG-Kanal eine erkennbare Suchnachricht.
2. Der Bot erkennt Mitspieler-Gesuche und richtet die Benachrichtigung passend aus.
3. Der Rang wird automatisch bestimmt.
4. Aktuelle Voice-Lanes werden nach Passung einsortiert.
5. Der Bot postet ein Embed mit den besten Lobby-Vorschlägen und dem Hinweis, selbst eine Lane aufzumachen.
6. Alternativ erstellt das Mitglied über das LFG-Panel ein eigenes Gesuch als Forum-Post; Watcher erhalten einmalig eine DM.

## Typische Meldungen & Fehler

| Signal | Was es bedeutet | Nächster Schritt |
| --- | --- | --- |
| Mitglied kann gerade nicht angepingt werden | Der Smartping wurde bewusst geblockt (z. B. zu häufig genutzt oder die Zielperson möchte keine Pings). | Später erneut versuchen; wiederholte Blockierung ist gewollter Schutz. |
| Smartping ohne genanntes Mitglied | Der Smartping-Befehl wurde ohne Ziel-User aufgerufen. | Befehl mit @Erwähnung des Zielmitglieds wiederholen. |
| Anzeigename bei Scrim-Anmeldung schon vergeben | Der Anzeigename ist bereits von einem anderen Teilnehmer belegt, daher wurde die Anmeldung nicht gespeichert. | Eindeutigen Anzeigenamen verwenden oder die Doppelung an die Scrim-Organisation melden. |
| Kein gültiger Name bei Scrim-Anmeldung | Es wurde kein sichtbarer, nicht-leerer Name übergeben. | Mit einem sichtbaren Namen erneut anmelden. |
| Match-Termin im falschen Datumsformat | Ein geplanter Scrim-Termin wurde nicht im geforderten Datumsformat angegeben. | Termin im korrekten Format angeben (Aufgabe der Scrim-Organisation). |

## Befehle

- `!smartping`

### Das darf der Support sagen

- Wer im LFG-Kanal eine klare Suchnachricht schreibt, bekommt vom Bot passende Lobby-Vorschläge; wenn nichts kommt, kurz warten und erneut versuchen.
- Nach einer LFG-Antwort gibt es eine kurze Pause, und wer schon im Voice sitzt, wird nicht erneut geroutet - beides ist normal.
- Ein blockierter Smartping ist gewollter Schutz; wiederholte Blockierung ist beabsichtigt, später erneut versuchen hilft.
- Für Scrims meldet man sich per Discord-Reaktion oder Webanmeldung an; die Team-Zuteilung (neu/zugeteilt/Bank/Warteliste) übernimmt die Scrim-Organisation.

### Nie an Mitglieder weitergeben

- Interne Zahlen jeder Art: Schwellen, Sicherheitswerte, Gewichte, Zeitgrenzen, Limits.
- Die interne Entscheidungs- oder Durchsetzungslogik — welche Signale zu welcher Wirkung führen und in welcher Reihenfolge.
- Interne Technik: IDs, Pfade, Endpunkte, Namespaces, KI-Anbieter oder -Modelle, Zugangsdaten.
- Verdeckte Mechaniken oder Betriebsarten — auch nicht andeutungsweise, welche es geben könnte.
- Im Zweifel abstrahieren und an einen Menschen eskalieren (Details im Agenten-Leitfaden).

## Verwandte Seiten

- [Mitspieler finden](../workflows/mitspieler-finden.md)

**Bewusst nicht dokumentiert:** Schwellenwerte und Zeitgrenzen, Ranking- und Sortierlogik, Bewertungslogik, Zuordnungslogik, interne Endpunkte, verdeckte Mechaniken. Diese internen Details bleiben aus Sicherheitsgründen außerhalb dieser Wissensbasis.
