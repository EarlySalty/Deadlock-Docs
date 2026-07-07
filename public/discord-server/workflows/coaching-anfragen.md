---
title: "Coaching anfragen"
tags: [discord-server, coaching, anfragen]
stand: 2026-07-07
quelle: "Deadlock-Bots/docs/support-kb/workflows/coaching-anfragen.html"
---
# Coaching anfragen

Coaching läuft über die Coaching-Website: Termine werden dort angefragt und danach mit dem Discord abgeglichen, sodass das Mitglied Erinnerungen und im Anschluss einen Feedback-Zugang bekommt.

## Was Mitglieder merken

Ein Mitglied fragt sein Coaching auf der Coaching-Website an. Steht ein Termin an, wird er mit dem Discord synchronisiert und das Mitglied bekommt eine persönliche DM mit Terminhinweis und Link zur Website. Details zum Coaching sieht man jeweils auf der Website. Nach einem Coaching ist für eine begrenzte Zeit ein Feedback-Kanal zugänglich, in dem Rückmeldung gegeben werden kann. Bleibt eine erwartete Erinnerung aus, hilft der Support weiter.

## Ablauf Schritt für Schritt

1. Coaching auf der Coaching-Website anfragen bzw. Termin festlegen
2. Der Termin wird mit dem Discord abgeglichen
3. Vor dem Termin kommt eine persönliche DM mit Hinweis und Website-Link
4. Details jeweils auf der Coaching-Website ansehen
5. Nach dem Coaching für begrenzte Zeit im Feedback-Kanal Rückmeldung geben

## Mögliche Ausgänge

- Coaching-Erinnerung als DM zugestellt
- Feedback-Kanal nach dem Coaching für begrenzte Zeit zugänglich

## Sichtbare Zustände

| Zustand | Was du siehst | Was es bedeutet | Sicherer nächster Schritt |
| --- | --- | --- | --- |
| Coaching-Erinnerung | Persönliche DM mit Termin-/Coaching-Hinweis und Link zur Coaching-Website | Ein anstehendes Coaching wurde mit dem Discord abgeglichen | Details auf der Coaching-Website ansehen |
| Feedback-Zugang nach Coaching | Zugriff auf den Feedback-Kanal für begrenzte Zeit nach dem Termin | Das Coaching ist gelaufen und Rückmeldung ist vorgesehen | Feedback im dafür geöffneten Kanal hinterlassen |

## Typische Meldungen & Fehler

| Signal | Was es bedeutet | Nächster Schritt |
| --- | --- | --- |
| Keine Coaching-Erinnerung erhalten | Ein erwarteter Termin-Hinweis kam nicht an, obwohl ein Coaching ansteht | Beim Support melden, damit der Abgleich geprüft wird |
| Begrüßungs-/Hinweis-DM kam nicht an | DMs sind vermutlich geschlossen, deshalb konnte die Nachricht nicht zugestellt werden | DMs für Servermitglieder erlauben; erwartete Hinweise kommen dann wieder an |
| Community-Funktionen sind gesperrt | Es ist ein Datenschutz-Opt-out gesetzt, das Funktionen blockiert | Aktives Opt-in nötig, um die Funktionen wieder zu nutzen |

### Das darf der Support sagen

- Coaching-Termine läufst du über die Coaching-Website; der Termin wird danach mit dem Discord abgeglichen.
- Vor dem Coaching bekommst du eine persönliche DM mit Erinnerung und einem Link zur Website.
- Nach dem Coaching ist für eine begrenzte Zeit ein Feedback-Kanal offen, in dem du Rückmeldung geben kannst.
- Kommt keine erwartete Erinnerung an, meld dich beim Support, dann prüfen wir den Abgleich.

### Nie an Mitglieder weitergeben

- Interne Zahlen jeder Art: Schwellen, Sicherheitswerte, Gewichte, Zeitgrenzen, Limits.
- Die interne Entscheidungs- oder Durchsetzungslogik — welche Signale zu welcher Wirkung führen und in welcher Reihenfolge.
- Interne Technik: IDs, Pfade, Endpunkte, Namespaces, KI-Anbieter oder -Modelle, Zugangsdaten.
- Verdeckte Mechaniken oder Betriebsarten — auch nicht andeutungsweise, welche es geben könnte.
- Im Zweifel abstrahieren und an einen Menschen eskalieren (Details im Agenten-Leitfaden).

## Verwandte Seiten

- [Coaching](../module/coaching.md)

**Bewusst nicht dokumentiert:** Bewertungslogik, Zugangsdaten, Schwellenwerte und Zeitgrenzen. Diese internen Details bleiben aus Sicherheitsgründen außerhalb dieser Wissensbasis.
