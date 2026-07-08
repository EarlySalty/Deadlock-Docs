---
title: "Steam verknüpfen & Rang"
tags: [discord-server, steam, verknuepfen, rang]
stand: 2026-07-07
quelle: "Deadlock-Bots/docs/support-kb/workflows/steam-verknuepfen-rang.html"
---
# Steam verknüpfen & Rang

Über den Rang-Kanal verknüpfen Mitglieder ihr Steam-Konto mit dem Bot; danach erkennt der Bot den Deadlock-Rang und setzt automatisch die passende Rang-Rolle. Der Rang bleibt aktuell, solange die Steam-Freundschaft mit dem Bot besteht.

## Was Mitglieder merken

Im Rang-Kanal gibt es ein Panel mit den Buttons "Steam verknüpfen", "Freundescode eingeben" und "Rang prüfen". Über "Steam verknüpfen" startet die Anmeldung per Steam; über "Freundescode eingeben" öffnet sich ein lokales Eingabefeld für den eigenen Code. Damit der Rang gelesen werden kann, muss das Mitglied mit dem Bot auf Steam befreundet sein, also die Freundschaftsanfrage annehmen. Sobald das steht, erkennt der Bot den In-Game-Rang und vergibt die passende Rang-Rolle, wodurch Ranked-Lanes und die Mitspieler-Suche freigeschaltet werden. Der Rang wird danach automatisch aktuell gehalten. Antworten des Bots zu Steam-Aktionen erscheinen meist als private (ephemere) Nachricht. Nach einiger Voice-Zeit kann der Bot per DM an die noch fehlende Steam-Verknüpfung erinnern; das ist optional.

## Ablauf Schritt für Schritt

1. Im Rang-Kanal auf 'Steam verknüpfen' klicken und sich per Steam anmelden.
2. Über 'Freundescode eingeben' den eigenen Freundescode im geöffneten Eingabefeld hinterlegen.
3. Die Freundschaftsanfrage des Bots auf Steam annehmen, damit der Rang gelesen werden kann.
4. Der Bot erkennt den In-Game-Rang und setzt die passende Rang-Rolle.
5. Der Rang wird danach automatisch aktuell gehalten, solange die Steam-Freundschaft besteht.

## Mögliche Ausgänge

- Steam-Konto mit Discord verknüpft
- Rang-Rolle gesetzt und selbstaktualisierend
- Ranked-Lanes und Mitspieler-Suche freigeschaltet
- Angezeigter Deadlock-Rang beim Prüfen
- Hinweis, wenn der Steam-Dienst gerade nicht erreichbar ist

## Sichtbare Zustände

| Zustand | Was du siehst | Was es bedeutet | Sicherer nächster Schritt |
| --- | --- | --- | --- |
| Steam-Panel angezeigt | Panel mit den Buttons 'Steam verknüpfen', 'Freundescode eingeben', 'Rang prüfen'. | Einstiegspunkt für alle Steam-Aktionen. | Gewünschten Button anklicken; für den Freundescode öffnet sich ein Eingabefeld. |
| Steam verknüpft / Rang erkannt | Nach Verknüpfung und bestätigter Freundschaft wird der In-Game-Rang erkannt und als Rang-Rolle gesetzt. | Der Rang wird automatisch gepflegt, solange man mit dem Bot auf Steam befreundet bleibt. | Passiert nichts, auf 'Rang prüfen' klicken oder die Freundschaft mit dem Bot prüfen. |
| Erinnerung zur Steam-Verknüpfung | Nach einiger Zeit in Voice kommt eine private Erinnerung, Steam zu verknüpfen. | Automatischer, optionaler Hinweis, ausgelöst durch Voice-Aktivität. | Verknüpfen oder ignorieren; keine Pflicht. |
| Hinweis nach Onboarding | Nach abgeschlossenem Onboarding schickt der Bot eine private Nachricht mit Verweis auf die Rang-Verknüpfung. | Automatischer Anschluss-Hinweis; man muss nichts tun, wenn man nicht will. | Bei Interesse dem Hinweis folgen und im Rang-Kanal verknüpfen; sonst ignorieren. |
| Steam-Dienst gerade nicht erreichbar | 'Steam-Bot ist gerade nicht erreichbar. Bitte versuche es in wenigen Sekunden erneut.' | Der Steam-Dienst antwortet vorübergehend nicht. | Kurz warten und die Aktion erneut auslösen. |

## Typische Meldungen & Fehler

| Signal | Was es bedeutet | Nächster Schritt |
| --- | --- | --- |
| Meldung, dass der Steam-Bot gerade nicht erreichbar ist | Steam-Funktionen (Verknüpfen, Rang, Freundescode) sind vorübergehend nicht verfügbar. | Ein paar Sekunden warten und erneut versuchen; hält es an, Team informieren. |
| Verknüpfung ließ sich nicht speichern | Die Zuordnung von Steam und Discord wurde nicht gespeichert. | Erneut versuchen; bei Wiederholung Team kontaktieren. |
| Die private Erinnerung kommt nicht an | Der Bot konnte keine DM schicken, weil private Nachrichten für den Server gesperrt sind. | DMs für den Server erlauben, wenn man die Hinweise erhalten möchte. |
| Rang-Rolle wird nicht vergeben, obwohl verknüpft | Die Verknüpfung steht, aber die Rolle konnte gerade nicht gesetzt werden. | Kurz warten und 'Rang prüfen' erneut nutzen; hält es an, Team bitten, die Rolle zu setzen. |

## Für den Support

### Das darf der Support sagen

- Der Rang wird nur gelesen, wenn du mit dem Bot auf Steam befreundet bist - nimm die Freundschaftsanfrage an und klick dann auf 'Rang prüfen'.
- Nach der Verknüpfung setzt der Bot die passende Rang-Rolle automatisch und hält sie aktuell, solange die Steam-Freundschaft besteht.
- Wenn die Meldung kommt, dass der Steam-Bot nicht erreichbar ist, kurz warten und die Aktion erneut auslösen.
- Die Erinnerungs-DM zur Steam-Verknüpfung ist optional; wer sie erhalten will, muss DMs für den Server erlauben.

### Nie an Mitglieder weitergeben

- Interne Zahlen jeder Art: Schwellen, Sicherheitswerte, Gewichte, Zeitgrenzen, Limits.
- Die interne Entscheidungs- oder Durchsetzungslogik — welche Signale zu welcher Wirkung führen und in welcher Reihenfolge.
- Interne Technik: IDs, Pfade, Endpunkte, Namespaces, KI-Anbieter oder -Modelle, Zugangsdaten.
- Verdeckte Mechaniken oder Betriebsarten — auch nicht andeutungsweise, welche es geben könnte.
- Im Zweifel abstrahieren und an einen Menschen eskalieren (Details im Agenten-Leitfaden).

## Verwandte Seiten

- [Steam- & Twitch-Verknüpfung](../module/steam-twitch-verknuepfung.md)

**Bewusst nicht dokumentiert:** Schwellenwerte und Zeitgrenzen, Bewertungslogik, Durchsetzungsbedingungen, verdeckte Mechaniken, interne Endpunkte, Zugangsdaten, sonstige interne Details. Diese internen Details bleiben aus Sicherheitsgründen außerhalb dieser Wissensbasis.
