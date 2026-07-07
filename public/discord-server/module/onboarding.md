---
title: "Onboarding & Rollen"
tags: [discord-server, onboarding, rollen]
stand: 2026-07-07
quelle: "Deadlock-Bots/docs/support-kb/modules/onboarding.html"
---
# Onboarding & Rollen

Beim Beitritt führt der Bot ein Mitglied durch einen mehrschrittigen Einstieg mit Fragen, vergibt danach automatisch Rollen und schaltet Kanalzugriff frei. Rollen lassen sich zusätzlich über Emoji-Reaktionen an Panel-Nachrichten selbst geben, und eine Rang-Verknüpfung wird angeboten.

## Was Mitglieder merken

Ein neues Mitglied durchläuft nach dem Beitritt einen geführten Ablauf mit Buttons und Fragen zu Interessen, Erwartungen und Spielstil, optional mit Angaben zu Streaming, Ton und Alter. Wer den Regeln-bestätigen-Schritt abschliesst, bekommt automatisch Rollen (z.B. Verifiziert, Ping-Rollen) und damit Zugriff auf weitere Kanäle; passend zu den Angaben können Streamer- oder Ping-Rollen gesetzt werden. Zusätzlich wird eine Steam-/Rang-Verknüpfung angeboten. Ausserhalb des Onboardings kann sich ein Mitglied über Emoji-Reaktionen an Panel-Nachrichten selbst Rollen geben oder wieder entziehen, teils mit einer einmaligen Willkommens-DM. Bei längeren Aktionen zeigt der Bot kurz einen Ladezustand und reicht die Antwort danach nach; viele Bestätigungen sind nur für das auslösende Mitglied selbst sichtbar.

## Mögliche Ausgänge

- Rollen und Kanalzugriff freigeschaltet
- Streamer-/Ping-Rollen gesetzt
- Onboarding abgeschlossen
- Rolle per Reaktion vergeben oder entzogen

## Sichtbare Zustände

| Zustand | Was du siehst | Was es bedeutet | Sicherer nächster Schritt |
| --- | --- | --- | --- |
| Onboarding läuft | Geführte Schritte mit Buttons und Fragen, danach automatisch vergebene Rollen (z.B. Verifiziert, Ping-Rollen) | Der Beitritts-Ablauf ist gestartet; nach Abschluss werden Zugriffe und Rollen freigeschaltet | Den Schritten folgen und den Bestätigungs-Button drücken |
| Reaction-Role vergeben | Rolle erscheint im Profil, optional eine einmalige Willkommens-DM | Die Emoji-Reaktion auf der Panel-Nachricht hat die zugeordnete Rolle vergeben | Reaktion entfernen, wenn die Rolle (sofern so konfiguriert) wieder weg soll |
| Eingabeformular (Modal) | Ein Popup-Formular mit Eingabefeldern (z.B. für Codes/Texte) | Der Bot erwartet eine Eingabe, bevor er fortfährt | Felder ausfüllen und absenden |
| Interaktion wird verarbeitet (Ladezustand) | Nach dem Klick oder Befehl erscheint kurz ein Verarbeitungshinweis, danach die eigentliche Antwort | Die Antwort brauchte etwas länger und wurde nachgereicht statt sofort geschickt | Kurz warten; die Antwort kommt automatisch. Kommt gar nichts, Aktion erneut auslösen |
| Nur für dich sichtbare Antwort | Eine Antwort mit dem Hinweis, dass nur das auslösende Mitglied sie sieht | Bestätigungen und private Rückmeldungen werden absichtlich nur dem Auslöser gezeigt | Kein Handlungsbedarf; das ist gewollt |
| DM nicht zustellbar | Eine erwartete Direktnachricht (z.B. Willkommens-DM) kommt nicht an | Das Mitglied nimmt keine DMs vom Server an oder ist nicht erreichbar; die Rolle ist trotzdem aktiv | Server-DMs in den Privatsphäre-Einstellungen erlauben und die Aktion wiederholen |

## So läuft es ab

1. Nach dem Beitritt bzw. Klick auf den Einstiegs-Button startet ein mehrschrittiger Ablauf mit Fragen zu Interessen, Erwartungen und Spielstil
2. Optional werden Angaben zu Streaming, Ton und Alter abgefragt
3. Der Regeln-bestätigen-Schritt schaltet Zugriff und Rollen frei
4. Passend zu den Angaben können Streamer- oder Ping-Rollen gesetzt werden
5. Eine Steam-/Rang-Verknüpfung wird angeboten
6. Der Rollen-Abschluss wird erkannt und stößt passende Folgeprozesse an (z.B. Verknüpfungs-Abschluss)

## Typische Meldungen & Fehler

| Signal | Was es bedeutet | Nächster Schritt |
| --- | --- | --- |
| Willkommens-DM konnte nicht zugestellt werden | Die Rolle wurde vergeben, aber die Begrüßungs-DM kam nicht an (meist geschlossene DMs) | DMs für Servermitglieder erlauben; die Rolle ist trotzdem aktiv |
| DM dauerhaft nicht zustellbar | Eine DM ist dauerhaft nicht zustellbar; es wird nicht erneut versucht | DM-Einstellungen prüfen, falls Nachrichten erwartet werden |
| Bot konnte das Mitglied nicht anschreiben | Der Bot erreichte das Konto nicht (DMs geschlossen oder Konto nicht erreichbar) | Server-Direktnachrichten erlauben und die Aktion erneut auslösen |
| Mitglied, Server oder Rolle nicht auffindbar | Mitglied, Server oder Rolle war zum Zeitpunkt der Aktion nicht auffindbar | Sicherstellen, dass das Mitglied noch auf dem Server ist, dann erneut versuchen |
| Interaktion fehlgeschlagen | Die Antwort auf einen Klick oder Befehl kam nicht durch; Discord zeigt ggf. "Interaktion fehlgeschlagen" | Aktion erneut auslösen; bei Wiederholung ein Team-Mitglied informieren |
| Eingabeformular liess sich nicht mehr öffnen | Ein Formular konnte nicht mehr geöffnet werden, weil die Aktion zu lange gebraucht hat | Aktion erneut auslösen; das Formular sollte dann sofort erscheinen |

### Das darf der Support sagen

- Der Regeln-bestätigen-Schritt im Onboarding schaltet automatisch Rollen und Kanalzugriff frei; einfach dem geführten Ablauf bis zum Ende folgen.
- Rollen kann man sich auch selbst geben, indem man mit dem passenden Emoji auf die Panel-Nachricht reagiert; die Reaktion wieder zu entfernen kann die Rolle (sofern so eingerichtet) zurücknehmen.
- Wenn die Willkommens-DM nicht ankommt, liegt das meist an geschlossenen DMs - Server-Direktnachrichten erlauben; die Rolle ist trotzdem aktiv.
- Wenn 'Interaktion fehlgeschlagen' erscheint oder ein Formular sich nicht öffnet, die Aktion einfach erneut auslösen; bei Wiederholung ein Team-Mitglied informieren.

### Nie an Mitglieder weitergeben

- Interne Zahlen jeder Art: Schwellen, Sicherheitswerte, Gewichte, Zeitgrenzen, Limits.
- Die interne Entscheidungs- oder Durchsetzungslogik — welche Signale zu welcher Wirkung führen und in welcher Reihenfolge.
- Interne Technik: IDs, Pfade, Endpunkte, Namespaces, KI-Anbieter oder -Modelle, Zugangsdaten.
- Verdeckte Mechaniken oder Betriebsarten — auch nicht andeutungsweise, welche es geben könnte.
- Im Zweifel abstrahieren und an einen Menschen eskalieren (Details im Agenten-Leitfaden).

## Verwandte Seiten

- [Server betreten](../workflows/onboarding-beitritt.md)

**Bewusst nicht dokumentiert:** interne IDs und Namen, Schwellenwerte und Zeitgrenzen, verdeckte Mechaniken, sonstige interne Details. Diese internen Details bleiben aus Sicherheitsgründen außerhalb dieser Wissensbasis.
