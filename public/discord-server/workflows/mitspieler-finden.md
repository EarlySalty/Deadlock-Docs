---
title: "Mitspieler finden"
tags: [discord-server, mitspieler, finden]
stand: 2026-07-07
quelle: "Deadlock-Bots/docs/support-kb/workflows/mitspieler-finden.html"
---
# Mitspieler finden

Der Bot hilft beim Finden von Mitspielern: Wer im LFG-Kanal eine passende Nachricht schreibt, bekommt Lobby-Vorschläge, und über das LFG-Panel lassen sich eigene Gesuche posten oder Benachrichtigungen aktivieren. Lanes zeigen zusätzlich live den Match-Status an.

## Was Mitglieder merken

Mitglieder merken das vor allem an der Lobby-Suche: Wer im LFG-Kanal eine erkennbare Suchnachricht schreibt (z. B. "wer hat Bock auf ein paar Runden" oder "suche noch Mitspieler"), bekommt vom Bot eine Antwort mit passenden Voice-Lobbys, die passen, plus den Hinweis, notfalls selbst eine Lane aufzumachen. Über ein LFG-Panel können Mitglieder außerdem ein eigenes Gesuch als Forum-Post mit Modus, Rang-Bereich und Beitreten-Button erstellen oder sich einmalig benachrichtigen lassen, wenn ein passendes Gesuch auftaucht. In den Sprachkanälen hängt der Bot live den Match- oder Lobby-Status an den Lane-Namen. Team-Mitglieder können zusätzlich einzelne Leute gezielt in eine Lobby einladen (Smartping), sofern die Zielperson das gerade zulässt.

## Ablauf Schritt für Schritt

1. Im LFG-Kanal eine klare Suchnachricht schreiben (Modus/Bedarf nennen, z. B. "suche noch Mitspieler für Ranked").
2. Der Bot erkennt ein Mitspieler-Gesuch und richtet die Benachrichtigung passend aus.
3. Der Bot postet ein Embed mit den besten Lobby-Vorschlägen plus dem Hinweis, notfalls selbst eine Lane aufzumachen.
4. In eine vorgeschlagene Lobby springen oder selbst eine Lane eröffnen.
5. Alternativ über das LFG-Panel ein eigenes Gesuch (Modus, Rang-Bereich, Plätze) als Forum-Post erstellen oder eine einmalige Benachrichtigung für passende Gesuche aktivieren.
6. Team-Mitglieder können eine bestimmte Person per Smartping gezielt in eine Lobby einladen, sofern die Zielperson das gerade zulässt.

## Mögliche Ausgänge

- Antwort-Embed mit Lobby-Vorschlägen
- Sichtbares LFG-Gesuch als Forum-Post mit Beitreten-Button
- Gematchte Mitspieler über Beitritte oder Benachrichtigungen
- In manchen Fällen antwortet der Bot bewusst nicht
- Smartping-Einladung an das Zielmitglied oder Blockmeldung

## Sichtbare Zustände

| Zustand | Was du siehst | Was es bedeutet | Sicherer nächster Schritt |
| --- | --- | --- | --- |
| LFG-Antwort erhalten | Ein Embed "Lobby-Finder" mit einem oder mehreren Lobby-Vorschlägen und dem Hinweis, selbst eine Lane aufzumachen. | Die Nachricht wurde als Lobby-Suche erkannt und passende Voice-Lanes wurden zugeordnet. | In eine der vorgeschlagenen Lobbys springen oder selbst eine aufmachen. |
| Keine LFG-Antwort | Der Bot antwortet nicht auf die Suchnachricht. | Der Bot hat auf dieses Gesuch bewusst nicht geantwortet. | Kurz warten und es mit einer klaren Suchnachricht erneut versuchen. |
| LFG-Gesuch erstellt | Ein eigener Forum-Post mit Modus, Rang-Bereich und Beitreten-Button; er räumt sich selbst weg, wenn die Lane schließt. | Die Mitspieler-Suche wurde als sichtbares Gesuch veröffentlicht. | Auf Beitritte warten oder selbst per Beitreten in andere Lanes springen. |
| LFG-Benachrichtigung | Eine DM "Passendes Gesuch!" mit Link zum Thread. | Ein neues Gesuch passt zum eigenen Watch-Filter; die Benachrichtigung kommt einmalig. | Thread öffnen; für weitere Treffer den Watch erneut aktivieren. |
| Live-Match-Status im Lane-Namen | Der Lane-Name trägt einen Zusatz wie "im Match" (mit Minuten- und Spielerangabe) oder "in der Lobby". | Die Steam-Präsenz der Mitglieder wird live an den Kanalnamen gehängt. | Nur Anzeige; nichts zu tun. |
| Smartping blockiert | "Diese Person kann gerade nicht gepingt werden – zum Beispiel, weil sie keine Pings möchte." | Die Zielperson erfüllt gerade nicht die Bedingungen, um angepingt zu werden. | Später erneut versuchen; wiederholte Blockierung ist normal und beabsichtigt. |

## Typische Meldungen & Fehler

| Signal | Was es bedeutet | Nächster Schritt |
| --- | --- | --- |
| "Diese Person kann gerade nicht gepingt werden – zum Beispiel, weil sie keine Pings möchte." | Der Smartping wurde nicht zugestellt – zum Beispiel, weil die Zielperson keine Pings möchte. | Später erneut versuchen; wiederholte Blockierung ist gewollter Schutz. |
| Hinweis zur richtigen Nutzung von !smartping | Der Smartping-Befehl wurde ohne Ziel-User aufgerufen. | Befehl mit @Erwähnung des Zielmitglieds wiederholen. |
| "Für Ranked-Lanes brauchst du einen verifizierten Rang." | Ranked-Beitritt oder -Erstellung ohne verifizierte Rang-Rolle. | Steam verknüpfen, um die Rang-Rolle zu erhalten. |
| "Unbekannter Rang" bei einem Gesuch oder Filter | Der eingegebene Rang-Name wird nicht erkannt. | Einen gültigen Rang aus der Auswahl wählen (Haupt- oder Sub-Rang). |

## Befehle

- `!smartping`

### Das darf der Support sagen

- Wenn du im LFG-Kanal klar schreibst, dass du Mitspieler suchst, antwortet der Bot mit passenden Lobby-Vorschlägen, in die du direkt springen kannst.
- Über das LFG-Panel kannst du ein eigenes Gesuch posten oder dich einmalig benachrichtigen lassen, sobald ein passendes Gesuch auftaucht.
- Kommt keine Antwort, kurz warten und mit einer klaren Suchnachricht erneut versuchen.
- Wenn ein Smartping blockiert wird, ist das ein gewollter Schutz der Zielperson; einfach später erneut versuchen.

### Nie an Mitglieder weitergeben

- Interne Zahlen jeder Art: Schwellen, Sicherheitswerte, Gewichte, Zeitgrenzen, Limits.
- Die interne Entscheidungs- oder Durchsetzungslogik — welche Signale zu welcher Wirkung führen und in welcher Reihenfolge.
- Interne Technik: IDs, Pfade, Endpunkte, Namespaces, KI-Anbieter oder -Modelle, Zugangsdaten.
- Verdeckte Mechaniken oder Betriebsarten — auch nicht andeutungsweise, welche es geben könnte.
- Im Zweifel abstrahieren und an einen Menschen eskalieren (Details im Agenten-Leitfaden).

## Verwandte Seiten

- [Mitspielersuche (LFG)](../module/mitspielersuche-lfg.md)
- [Voice-Lanes (TempVoice)](../module/voice-lanes.md)

**Bewusst nicht dokumentiert:** Schwellenwerte und Zeitgrenzen, Bewertungslogik, Ranking- und Sortierlogik, Zuordnungslogik, Durchsetzungsbedingungen, verdeckte Mechaniken, interne Endpunkte. Diese internen Details bleiben aus Sicherheitsgründen außerhalb dieser Wissensbasis.
