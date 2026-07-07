---
title: "Streamer-Partner werden"
tags: [discord-server, streamer, partner, werden]
stand: 2026-07-07
quelle: "Deadlock-Bots/docs/support-kb/workflows/streamer-partner-werden.html"
---
# Streamer-Partner werden

Mitglieder, die Streamer-Partner werden wollen, starten den Vorgang im Discord und verbinden ihren Twitch-Account auf der Website. Kurz darauf werden Discord- und Twitch-Konto automatisch verknüpft und die Streamer-Rolle vergeben.

## Was Mitglieder merken

Wer Streamer-Partner werden will, löst den Vorgang im Discord aus und bekommt eine nur für sich sichtbare Nachricht mit einem Link zur Streamer-Onboarding-Website plus dem Hinweis, dass die Verknüpfung bald automatisch passiert. Sobald das Mitglied seinen Twitch-Account auf der Website verbunden hat, führt der Bot Discord- und Twitch-Konto von selbst zusammen und vergibt die Streamer-Rolle - ohne dass das Mitglied noch etwas anklicken muss. Die neue Rolle taucht dann im Profil auf. Klickt das Mitglied später auf eine Live-Ankündigung, bekommt es seinen persönlichen Twitch-Link zum Stream.

## Ablauf Schritt für Schritt

1. Mitglied löst den Streamer-Vorgang im Discord aus
2. Bot antwortet nur für das Mitglied sichtbar mit einem Link zur Streamer-Onboarding-Website und dem Hinweis, dass die Verknüpfung bald automatisch passiert
3. Mitglied verbindet seinen Twitch-Account auf der Website
4. Der Bot erkennt den neu verbundenen Streamer und verknüpft Discord- und Twitch-Konto automatisch
5. Die Streamer-Rolle wird vergeben

## Mögliche Ausgänge

- Discord und Twitch automatisch verknüpft, Streamer-Rolle vergeben
- Klappt die Zuordnung nicht sofort, kann sie später nachgezogen werden
- Ohne Twitch-Verbindung verfällt die Absicht ohne Wirkung

## Sichtbare Zustände

| Zustand | Was du siehst | Was es bedeutet | Sicherer nächster Schritt |
| --- | --- | --- | --- |
| Streamer-Absicht erfasst | Nur für dich sichtbare Nachricht 'Streamer-Partner werden' mit Onboarding-Link und dem Hinweis, dass die Verknüpfung bald automatisch passiert | Der Bot hat gemerkt, dass das Mitglied Streamer werden will, und reagiert auf deine Twitch-Verbindung über die Website | Twitch-Account über den genannten Link verbinden; danach passiert die Verknüpfung automatisch |
| Automatisch verknüpft + Streamer-Rolle | Die Streamer-Rolle taucht im Profil auf | Discord- und Twitch-Konto wurden automatisch zusammengeführt und die Rolle vergeben | Bei einer unerwarteten oder falschen Verknüpfung das Team kontaktieren |
| Vorschlag zur Bestätigung offen | Für Mitglieder nicht sichtbar; ein Moderator sieht einen Match-Vorschlag mit Verknüpfen-/Ablehnen-Buttons | In diesem Fall bestätigt das Team die Verknüpfung manuell | Auf die Moderator-Entscheidung warten; bei Verzögerung das Team ansprechen |
| Twitch-Link ausgegeben | Nur für dich sichtbare Nachricht 'Hier ist dein Twitch-Link für..' mit einem Link-Button | Der Klick auf eine Live-Ankündigung wurde erkannt und der persönliche Link bereitgestellt | Auf den Link-Button klicken, um den Stream zu öffnen |

## Typische Meldungen & Fehler

| Signal | Was es bedeutet | Nächster Schritt |
| --- | --- | --- |
| 'Streamer-Rolle nicht gefunden - nur verknüpft.' | Die Konten wurden verknüpft, aber die Streamer-Rolle konnte nicht vergeben werden | Team bitten, die Streamer-Rolle manuell zu vergeben |
| 'Rolle konnte nicht vergeben werden.' | Die Verknüpfung ist erfolgt, aber die Rollenvergabe schlug fehl (z. B. Rechteproblem des Bots) | Team informieren, damit die Rolle manuell gesetzt wird |
| 'Diese Live-Ankündigung ist nicht mehr aktiv.' | Der geklickte Live-Button gehört zu einem veralteten Stream-Post | Eine aktuelle Live-Ankündigung im Server nutzen |
| Verknüpfung ließ sich nicht speichern | Die Verknüpfung konnte nicht in der Datenbank abgelegt werden | Erneut versuchen; bei Wiederholung das Team kontaktieren |

## Befehle

- `/streamer`

### Das darf der Support sagen

- Nach dem Start des Vorgangs musst du deinen Twitch-Account über den Link in der Nachricht verbinden; danach passiert die Verknüpfung von selbst.
- Die Streamer-Rolle wird automatisch vergeben, sobald Discord und Twitch verknüpft sind - du musst dafür nichts weiter anklicken.
- Wenn die Rolle nach der Verknüpfung fehlt, können wir sie manuell für dich vergeben.
- Bei einer unerwarteten oder falschen Verknüpfung melde dich beim Team, dann sehen wir uns das an.

### Nie an Mitglieder weitergeben

- Interne Zahlen jeder Art: Schwellen, Sicherheitswerte, Gewichte, Zeitgrenzen, Limits.
- Die interne Entscheidungs- oder Durchsetzungslogik — welche Signale zu welcher Wirkung führen und in welcher Reihenfolge.
- Interne Technik: IDs, Pfade, Endpunkte, Namespaces, KI-Anbieter oder -Modelle, Zugangsdaten.
- Verdeckte Mechaniken oder Betriebsarten — auch nicht andeutungsweise, welche es geben könnte.
- Im Zweifel abstrahieren und an einen Menschen eskalieren (Details im Agenten-Leitfaden).

## Verwandte Seiten

- [Steam- & Twitch-Verknüpfung](../module/steam-twitch-verknuepfung.md)

**Bewusst nicht dokumentiert:** Durchsetzungsbedingungen, Schwellenwerte und Zeitgrenzen, Bewertungslogik, verdeckte Mechaniken, Gewichtungen, interne Endpunkte, Zugangsdaten, sonstige interne Details. Diese internen Details bleiben aus Sicherheitsgründen außerhalb dieser Wissensbasis.
