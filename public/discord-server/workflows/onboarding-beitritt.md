---
title: "Server betreten"
tags: [discord-server, onboarding, beitritt, betreten]
stand: 2026-07-07
quelle: "Deadlock-Bots/docs/support-kb/workflows/onboarding-beitritt.html"
---
# Server betreten

Wenn jemand dem Server beitritt, führt der Bot durch einen kurzen Einstiegs-Ablauf: Begrüßung mit ein paar Fragen, Regeln bestätigen, Zugangs- und Interessen-Rollen bekommen, danach ein Hinweis auf die optionale Steam-Verknüpfung.

## Was Mitglieder merken

Nach dem Beitritt startet ein mehrschrittiger Einstieg mit Buttons und Fragen zu Interessen, Erwartungen und Spielstil. Wer die Regeln bestätigt, bekommt die Zugangsrolle und wird freigeschaltet; passende Rollen (z. B. Ping- oder Streamer-Rollen) werden dabei vergeben. Zum Abschluss weist der Bot auf die Steam-Verknüpfung hin, mit der später automatisch die Rang-Rolle gesetzt wird. Diese Verknüpfung ist freiwillig. Manche Rückmeldungen sieht nur das Mitglied selbst, und bei längeren Aktionen zeigt der Bot kurz einen Ladehinweis, bevor die Antwort nachkommt.

## Ablauf Schritt für Schritt

1. Mitglied tritt dem Server bei und der Einstiegs-/Tour-Ablauf startet.
2. Der Bot stellt mehrschrittig Fragen zu Interessen, Erwartungen und Spielstil (optional auch Streamer-, Ton- und Alters-Angaben).
3. Im Regeln-bestätigen-Schritt klickt das Mitglied auf die Bestätigung.
4. Der Bot vergibt die Zugangsrolle sowie passende Rollen (z. B. Ping-/Streamer-/Ranked-Rollen) und meldet die Freischaltung.
5. Zum Abschluss bietet der Bot die Steam-Verknüpfung an und schickt dazu einen Folge-Hinweis per DM.
6. Über die Buttons im Rang-Kanal kann das Mitglied Steam optional verknüpfen, damit die Rang-Rolle automatisch gesetzt und aktuell gehalten wird.

## Mögliche Ausgänge

- Zugang zum Server freigeschaltet
- Rollen und Kanalzugriff gesetzt (u. a. Ping-/Streamer-/Ranked-Rollen)
- Onboarding abgeschlossen
- Optionaler Folge-Hinweis zur Steam-/Rang-Verknüpfung erhalten

## Sichtbare Zustände

| Zustand | Was du siehst | Was es bedeutet | Sicherer nächster Schritt |
| --- | --- | --- | --- |
| Onboarding läuft | Einstiegs-/Tour-Schritte mit Buttons und Fragen zu Interessen, Erwartungen und Stil; danach werden Rollen vergeben. | Der Beitritts-Ablauf ist gestartet; nach Abschluss werden Zugriffe und Rollen freigeschaltet. | Den Schritten folgen und den Bestätigungs-Button drücken. |
| Interaktion wird verarbeitet (Ladezustand) | Nach einem Klick erscheint kurz ein Verarbeitungs-/Ladehinweis, danach die eigentliche Antwort. | Die Antwort brauchte etwas länger und wird nachgereicht statt sofort geschickt. | Kurz warten; die Antwort kommt automatisch. Kommt gar nichts, die Aktion erneut auslösen. |
| Nur für dich sichtbare Antwort | Eine Antwort mit dem Hinweis, dass nur das Mitglied selbst sie sieht. | Bestätigungen und private Rückmeldungen werden absichtlich nur dem Auslöser gezeigt. | Kein Handlungsbedarf; das ist gewollt. |
| Onboarding abgeschlossen | Nach der Regelbestätigung erscheint eine Willkommens-Meldung und man erhält die Zugangsrolle. | Die Bestätigung der Regeln schaltet den Server frei (Zugangs-Gate). | Fehlt die Rolle, im angegebenen Kanal erneut bestätigen oder das Team ansprechen. |
| Rolle konnte nicht vergeben werden | Meldung, dass die Regeln bestätigt sind, die Rolle aber gerade nicht vergeben werden konnte und das Team draufschaut. | Die Bestätigung ist angekommen, die Rollenvergabe scheiterte technisch. | Kurz warten und erneut versuchen; hält es an, das Team informieren. |
| Folge-DM nach Onboarding | Nach Abschluss des Einstiegs kommt eine private Nachricht mit Verweis auf die Rang-/Steam-Verknüpfung. | Ein automatischer Anschluss-Hinweis; man muss nichts tun, wenn man nicht will. | Bei Interesse dem Link folgen; sonst ignorieren. |
| DM nicht zustellbar | Eine erwartete Direktnachricht kommt nicht an. | Das Mitglied nimmt keine DMs vom Server an oder ist nicht erreichbar. | Server-DMs in den Privatsphäre-Einstellungen erlauben und die Aktion wiederholen. |

## Typische Meldungen & Fehler

| Signal | Was es bedeutet | Nächster Schritt |
| --- | --- | --- |
| Regeln bestätigt, aber keine Zugangsrolle | Die Bestätigung ist registriert, die Zugangsrolle wurde jedoch nicht gesetzt. | Erneut bestätigen; hält es an, das Team informieren — die Bestätigung selbst bleibt erhalten. |
| Willkommens- oder Folge-DM kommt nicht an | Die Rolle wurde vergeben, aber die private Nachricht ließ sich nicht zustellen (meist geschlossene DMs). | Server-Direktnachrichten erlauben; die Rolle ist trotzdem aktiv. |
| Interaktion fehlgeschlagen oder nichts passiert | Die Antwort auf einen Klick kam nicht durch oder eine Ziel-Ressource war kurz nicht auffindbar. | Die Aktion erneut auslösen; bei Wiederholung ein Team-Mitglied informieren. |
| Einstieg reagiert direkt nach einem Neustart nicht | Kurz nach einem Neustart sind manche Funktionen noch nicht vollständig verfügbar. | Kurz warten, bis der Bot vollständig verbunden ist, dann erneut versuchen. |

### Das darf der Support sagen

- Die Regelbestätigung schaltet den Zugang frei; wenn die Rolle fehlt, im genannten Kanal noch einmal bestätigen oder das Team ansprechen.
- Wenn Willkommens- oder Folge-DMs nicht ankommen, liegt es meist an geschlossenen Server-DMs — die vergebene Rolle bleibt davon unberührt.
- Die Steam-Verknüpfung am Ende des Einstiegs ist freiwillig; sie sorgt dafür, dass die Rang-Rolle automatisch gesetzt und aktuell gehalten wird.
- Bei einem kurzen Ladehinweis reicht Warten; die Antwort wird automatisch nachgereicht.

### Nie an Mitglieder weitergeben

- Interne Zahlen jeder Art: Schwellen, Sicherheitswerte, Gewichte, Zeitgrenzen, Limits.
- Die interne Entscheidungs- oder Durchsetzungslogik — welche Signale zu welcher Wirkung führen und in welcher Reihenfolge.
- Interne Technik: IDs, Pfade, Endpunkte, Namespaces, KI-Anbieter oder -Modelle, Zugangsdaten.
- Verdeckte Mechaniken oder Betriebsarten — auch nicht andeutungsweise, welche es geben könnte.
- Im Zweifel abstrahieren und an einen Menschen eskalieren (Details im Agenten-Leitfaden).

## Verwandte Seiten

- [Onboarding & Rollen](../module/onboarding.md)

**Bewusst nicht dokumentiert:** Durchsetzungsbedingungen, verdeckte Mechaniken, Schwellenwerte und Zeitgrenzen, Bewertungslogik, Zugangsdaten, Missbrauchsabwehr, interne Endpunkte. Diese internen Details bleiben aus Sicherheitsgründen außerhalb dieser Wissensbasis.
