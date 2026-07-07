---
title: "Steam- & Twitch-Verknüpfung"
tags: [discord-server, steam, twitch, verknuepfung]
stand: 2026-07-07
quelle: "Deadlock-Bots/docs/support-kb/modules/steam-twitch-verknuepfung.html"
---
# Steam- & Twitch-Verknüpfung

Diese Seite deckt die Brücken vom Discord-Bot zum Steam- und Twitch-Bot ab: Steam-Konto verknüpfen, Deadlock-Rang prüfen, persönliche Twitch-Live-Links und die automatische Erkennung von Streamer-Partnern.

## Was Mitglieder merken

Mitglieder können über ein Panel mit Buttons oder über Slash-Befehle ihren Steam-Account verknüpfen, einen Freundescode hinterlegen und ihren Deadlock-Rang prüfen. Wer Streamer-Partner werden will, startet über /streamer und verbindet seinen Twitch-Account auf der verlinkten Website; kurz danach werden Discord- und Twitch-Konto automatisch verknüpft und die Streamer-Rolle vergeben. Ein Klick auf eine Live-Ankündigung liefert dem Mitglied seinen persönlichen Twitch-Link. Nach dem Verbinden deines Twitch-Accounts wird die Streamer-Rolle automatisch vergeben.

## Mögliche Ausgänge

- Discord und Twitch automatisch verknüpft, Streamer-Rolle vergeben
- Login-Link zur Steam-Verknüpfung, angezeigter Deadlock-Rang oder gespeicherter Freundescode
- Persönlicher Twitch-Link zum Stream aus einer aktiven Live-Ankündigung
- Moderator-Vorschläge mit Verknüpfen/Ablehnen bei uneindeutigen Zuordnungen
- Hinweis, wenn der Steam-Bot nicht erreichbar oder die Live-Ankündigung veraltet ist

## Sichtbare Zustände

| Zustand | Was du siehst | Was es bedeutet | Sicherer nächster Schritt |
| --- | --- | --- | --- |
| Streamer-Absicht erfasst | Private Nachricht 'Streamer-Partner werden' mit Onboarding-Link und dem Hinweis, dass die Verknüpfung bald automatisch passiert | Der Bot hat gemerkt, dass das Mitglied Streamer werden will, und reagiert auf deine Twitch-Verbindung über die Website | Twitch-Account über den genannten Link verbinden; danach passiert die Verknüpfung automatisch |
| Automatisch verknüpft + Streamer-Rolle | Die Streamer-Rolle taucht auf | Discord- und Twitch-/Steam-Konto wurden automatisch zusammengeführt und die Rolle vergeben | Bei einer unerwarteten oder falschen Verknüpfung das Team kontaktieren |
| Vorschlag zur Bestätigung offen | Für Mitglieder nicht sichtbar; das Team bestätigt die Verknüpfung | In diesem Fall bestätigt das Team die Verknüpfung manuell | Auf die Moderator-Entscheidung warten; bei Verzögerung das Team ansprechen |
| Steam-Panel angezeigt | Panel mit Buttons 'Steam verknüpfen', 'Freundescode eingeben', 'Rang prüfen' | Einstiegspunkt für alle Steam-Aktionen | Gewünschten Button anklicken; für den Freundescode öffnet sich ein Eingabefeld |
| Twitch-Link ausgegeben | Private Nachricht 'Hier ist dein Twitch-Link für..' mit einem Link-Button | Der Klick auf eine Live-Ankündigung wurde erkannt und der persönliche Link bereitgestellt | Auf den Link-Button klicken, um den Stream zu öffnen |
| Live-Ankündigung nicht mehr aktiv | 'Diese Live-Ankündigung ist nicht mehr aktiv.' | Der zugehörige Stream/Post ist veraltet und nicht mehr verlinkbar | Eine aktuelle Live-Ankündigung nutzen |
| Steam-Bot nicht erreichbar | 'Steam-Bot ist gerade nicht erreichbar. Bitte versuche es in wenigen Sekunden erneut.' | Der Steam-Dienst antwortet vorübergehend nicht | Kurz warten und die Aktion erneut auslösen |

## So läuft es ab

1. Streamer werden: Mitglied nutzt /streamer und erhält eine private Nachricht mit Link zur Onboarding-Website plus Hinweis auf die automatische Verknüpfung.
2. Mitglied verbindet seinen Twitch-Account auf der Website; danach verknüpft ein Hintergrund-Prozess Discord- und Twitch-Konto automatisch und vergibt die Streamer-Rolle.
3. Steam verknüpfen / Rang prüfen: Mitglied klickt einen Steam-Panel-Button oder nutzt einen Steam-Slash-Befehl; die Anfrage geht an den Steam-Bot, dessen Antwort (Login-Link, Rang, Bestätigung) meist privat angezeigt wird.
4. Freundescode: über den entsprechenden Button öffnet sich ein Eingabefeld zum Hinterlegen des Codes.
5. Twitch-Live-Link: Klick auf den Button unter einer Live-Ankündigung liefert dem Mitglied privat seinen persönlichen Twitch-Link als Button.
6. Nicht verknüpfte Streamer können später automatisch erkannt werden; in Zweifelsfällen entscheidet das Team.

## Typische Meldungen & Fehler

| Signal | Was es bedeutet | Nächster Schritt |
| --- | --- | --- |
| Meldung, dass der Steam-Bot gerade nicht erreichbar ist | Steam-Funktionen (Verknüpfen, Rang, Freundescode) sind vorübergehend nicht verfügbar | Ein paar Sekunden warten und erneut versuchen; hält es an, Team informieren |
| Hinweis, dass die Live-Ankündigung nicht mehr aktiv ist | Der geklickte Live-Button gehört zu einem veralteten Stream-Post | Eine aktuelle Live-Ankündigung im Server nutzen |
| Hinweis, dass die Streamer-Rolle nicht gefunden wurde und nur verknüpft wurde | Die Konten wurden verknüpft, aber die Streamer-Rolle konnte nicht vergeben werden | Team bitten, die Streamer-Rolle manuell zu vergeben |
| Hinweis, dass die Rolle nicht vergeben werden konnte | Verknüpfung erfolgt, aber die Rollenvergabe schlug fehl (z. B. Rechteproblem des Bots) | Team informieren, damit die Rolle manuell gesetzt wird |
| Hinweis, dass die Aktion nur Moderatoren mit Rollen-Rechten vorbehalten ist | Es wurde eine Aktion versucht, die nur Moderatoren nutzen dürfen | Kein Handlungsbedarf für Mitglieder; bei Bedarf einen Moderator bitten |
| Hinweis, dass zur Eingabe kein Mitglied gefunden wurde | Bei einer manuellen Verknüpfung (Moderator) wurde kein passendes Mitglied gefunden | Exakten Namen oder die numerische Discord-ID verwenden |
| Hinweis, dass das Speichern der Verknüpfung fehlgeschlagen ist | Die Verknüpfung konnte nicht gespeichert werden | Erneut versuchen; bei Wiederholung Team kontaktieren |
| Hinweis, dass der automatische Streamer-Abgleich inaktiv ist | Die automatische Streamer-Erkennung ist gerade nicht aktiv | Nur für Admins relevant; die Verknüpfung kann später manuell erfolgen |

## Befehle

- `/streamer`
- `/account_verknüpfen`
- `/steam links`
- `/steam_rank`
- `/checkrank`

### Das darf der Support sagen

- Über /streamer bekommst du einen Link zur Onboarding-Website; sobald du deinen Twitch-Account dort verbindest, werden Discord und Twitch automatisch verknüpft und du bekommst die Streamer-Rolle.
- Deinen Deadlock-Rang und die Steam-Verknüpfung erreichst du über das Steam-Panel oder die Steam-Slash-Befehle wie /checkrank.
- Wenn 'Steam-Bot nicht erreichbar' erscheint, ist das nur vorübergehend; kurz warten und die Aktion erneut auslösen.
- Wurde deine Rolle nach der Verknüpfung nicht vergeben oder wurdest du unerwartet verknüpft, melde dich beim Team, damit wir es manuell korrigieren.

### Nie an Mitglieder weitergeben

- Interne Zahlen jeder Art: Schwellen, Sicherheitswerte, Gewichte, Zeitgrenzen, Limits.
- Die interne Entscheidungs- oder Durchsetzungslogik — welche Signale zu welcher Wirkung führen und in welcher Reihenfolge.
- Interne Technik: IDs, Pfade, Endpunkte, Namespaces, KI-Anbieter oder -Modelle, Zugangsdaten.
- Verdeckte Mechaniken oder Betriebsarten — auch nicht andeutungsweise, welche es geben könnte.
- Im Zweifel abstrahieren und an einen Menschen eskalieren (Details im Agenten-Leitfaden).

## Verwandte Seiten

- [Steam verknüpfen & Rang](../workflows/steam-verknuepfen-rang.md)
- [Streamer-Partner werden](../workflows/streamer-partner-werden.md)

**Bewusst nicht dokumentiert:** Durchsetzungsbedingungen, Schwellenwerte und Zeitgrenzen, Bewertungslogik, verdeckte Mechaniken, interne Endpunkte, Zugangsdaten, interne IDs und Namen. Diese internen Details bleiben aus Sicherheitsgründen außerhalb dieser Wissensbasis.
