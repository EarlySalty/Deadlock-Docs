---
title: "Fehlerbehebung"
tags: [discord-server, troubleshooting, fehlerbehebung]
stand: 2026-07-07
quelle: "Deadlock-Bots/docs/support-kb/support/troubleshooting.html"
---
# Fehlerbehebung

Die Anliegen, die im Support am häufigsten auftauchen — mit konkreten Selbsthilfe-Schritten. Löst ein Punkt das Problem nicht, gehört es ins Ticket, dann schaut das Team drauf.

## Steam lässt sich nicht verbinden / Rang wird nicht erkannt

Die Steam-Verknüpfung hat **drei** Schritte — ein reiner Login reicht nicht:

1. Steam über das Steam-Panel oder `/account_verknüpfen` verknüpfen. Der Login läuft über Steam selbst, ohne Passwort-Eingabe beim Bot.
2. Den **Steam-Freundescode** eingeben, damit der Bot die Freundschaftsanfrage schicken kann.
3. Die **Freundschaftsanfrage des Bots annehmen.** Erst dann gilt der Link als verifiziert — und erst dann funktionieren Verified-Rolle, Rang-Erkennung und Invite sauber.

Mehrere Konten? `/steam links` zeigt das Hinterlegte. Rang anzeigen: `/steam_rank`. Stimmen die **Rang-Rollen** nicht, hilft `/checkrank` — das gleicht die Rollen tatsächlich ab, statt sie nur anzuzeigen.

## Kein Beta-Invite / Invite kommt nicht an

1. **Im richtigen Kanal gefragt?** Eine nette Frage plus dein Steam-Freundescode. Ohne Code kann dich niemand einladen.
2. **Freundschaftsanfrage angenommen?** Wer einlädt, muss zuerst mit dir auf Steam befreundet sein.
3. **„Limited User"?** Steam blockiert Playtest-Invites, solange auf dem Account noch kein Mindestumsatz erreicht ist. Das ist eine Valve-Regel, die niemand umgehen kann — sobald der Account die Voraussetzung erfüllt, klappt es.
4. Ein Invite taucht nicht immer sofort auf; das kann etwas dauern. Später noch einmal in den Steam-Playtest-Einladungen nachsehen.

## Rang erscheint nicht an den Voice-Lanes

- Der Server-Rang wird automatisch vergeben, sobald der Steam-Account **verifiziert** verknüpft ist (siehe oben).
- Bei Ranked-Lanes erscheint der Rang automatisch im Kanalnamen; Basis ist der Rang-Anker der Lane.
- Ist der Rang gesetzt, aber die Lane bleibt gesperrt, kann eine Rang-Voraussetzung der Lane dahinterstecken — welche genau, ist nicht öffentlich. Dann eine passende Lane wählen oder im Ticket nachfragen.

## Nachricht wurde entfernt / Timeout oder Bann kassiert

- Im überwachten Kanal prüft der Bot Beiträge automatisch. Klare schwere Verstöße werden sofort entfernt und mit Timeout oder Bann geahndet; weniger eindeutige Fälle gehen als Vorschlag ans Team.
- Jede automatische Aktion kann das **Team wieder aufheben.** Bei vermutetem Fehler: kurz im Ticket schildern — ein Mensch prüft es. Warum genau geahndet wurde, ist nicht im Detail einsehbar.
- In „Ragebaiter-Free"-Voice-Bereichen kommt bei Provokationen zuerst eine freundliche Hinweis-DM, noch keine Strafe.

## Coaching: Zugang, Ablauf, Status

1. Coaching läuft über die **Website** (Login mit Discord, dann Formular mit Rang, Zielen und Verfügbarkeit). Der Coaching-Kanal führt dich hin.
2. Coaching ist **kostenlos**, und du darfst **mehrfach** anfragen. Deine Anfrage landet automatisch beim Coach-Team.
3. Den Stand deiner Anfrage siehst du über den dokumentierten Status-Weg.
4. Kommunikation läuft **nur im Coaching-Bereich auf dem Server** — keine DMs oder Freundschaftsanfragen an Coaches.
5. Nach der Session kommt eine Feedback-Anfrage — bitte ehrlich ausfüllen.

## Rang-Verlauf: wer sieht meine Historie?

- Die Sichtbarkeit deiner Rang-Historie stellst du selbst: **privat**, **nur für Mitglieder** oder **öffentlich**. Die Voreinstellung beschreiben wir bewusst nicht — maßgeblich ist, was du einstellst.
- Für den persönlichen Statistik-Bereich musst du eingeloggt sein.

## Was dieser Bereich nicht klärt

- Zwischenmenschliche Konflikte und Moderationsfälle — die übernimmt das Team direkt.
- Reine Gameplay-Fragen zu Deadlock (Builds, Timings, Map-Wissen).
- Interne Werte und Regeln des Bots — die sind bewusst nicht dokumentiert.
