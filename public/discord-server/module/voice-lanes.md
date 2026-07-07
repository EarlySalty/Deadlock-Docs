---
title: "Voice-Lanes (TempVoice)"
tags: [discord-server, voice, lanes, tempvoice]
stand: 2026-07-07
quelle: "Deadlock-Bots/docs/support-kb/modules/voice-lanes.html"
---
# Voice-Lanes (TempVoice)

Die Voice-Lanes (TempVoice) geben jedem Mitglied beim Beitritt eines Erstell-Kanals automatisch eine eigene, selbstverwaltete Sprach-Lane. Dazu kommen Rang-sortierte Ranked-Lanes, eine Mitspielersuche, ein Live-Match-Zusatz im Kanalnamen und gelegentliche Hinweis-DMs.

## Was Mitglieder merken

Wer einem der Erstell-/Router-Sprachkanäle beitritt, wird automatisch in eine frisch erzeugte eigene Lane gezogen und ist deren Owner. Über ein Verwaltungs-Panel kann der Owner die Lane umbenennen, ein Teilnehmerlimit setzen, Leute kicken, bannen und entbannen, die Sprache (Deutsch/Offen) wählen, einen Mindest-Rang festlegen, Presets speichern und die Lane als leiser Zuhörer betreten. In den Ranked-Kanälen werden Lanes nach Rang gruppiert und tragen den Rang im Namen; zusätzlich hängt live der Deadlock-Match-Status am Kanalnamen. Über ein LFG-Panel lassen sich Mitspieler-Gesuche als eigene Posts erstellen, und man kann sich bei passenden Gesuchen benachrichtigen lassen. Gelegentlich bekommst du eine automatische DM – einen Steam-Hinweis oder eine kurze Feedback-Frage.

## Mögliche Ausgänge

- Eigene, selbstverwaltete Lane
- Angepasste Lane mit gespeicherten Presets
- Entfernte oder gebannte Mitglieder
- Mitglied in passender Lane (Router/Anfänger-Umleitung)
- Rang-homogene Ranked-Lane
- Sichtbares LFG-Gesuch und gematchte Mitspieler
- Lane-Name mit Live-Status
- Optionale Steam-Verknüpfung und eingesammeltes Feedback

## Sichtbare Zustände

| Zustand | Was du siehst | Was es bedeutet | Sicherer nächster Schritt |
| --- | --- | --- | --- |
| Lane erstellt | Ein neuer Sprachkanal (z. B. mit Namen wie 'Lane', 'Chill' oder einem Rang-Label), in den man automatisch verschoben wird. | Der Beitritt zu einem Erstell-/Router-Kanal hat eine persönliche Lane erzeugt; man ist deren Owner. | Lane über das Verwaltungs-Panel anpassen oder einfach mit anderen spielen. |
| Lane-Verwaltungs-Panel | Ein TempVoice-Embed mit Buttons: Owner übernehmen, Limit, Kick, Ban, Unban, Duo/Trio/Reset, Umbenennen, Presets, Region, Lurker. | Steuerzentrale für die eigene Lane; Buttons wirken sofort, sofern man Owner ist. | Gewünschte Aktion anklicken; bei 'Nur der Lane-Owner kann das.' zuerst Owner werden. |
| Owner übernommen | Meldung 'Du bist jetzt Owner dieser Lane.' | Der vorherige Owner hat die Lane verlassen und man erfüllt die Übernahme-Bedingungen. | Lane jetzt selbst verwalten. |
| Gebannt aus einer Lane | Man kann der Lane nicht mehr beitreten; der Owner sieht einen Hinweis, dass der Bann für alle seine Lanes gilt. | Der Lane-Owner hat einen persönlichen Bann gesetzt, der für alle seine Lanes gilt. | Anderen Kanal nutzen oder den Owner um Entbannung bitten. |
| Ranked-Lane rang-gesperrt | Beitritt zu einer Ranked-Lane ist nicht möglich, obwohl Plätze frei wären; die Lane trägt einen Rang im Namen. | Die Lane ist an einen Rang-Bereich gebunden bzw. hat einen Mindest-Rang; die eigene Rang-Rolle liegt außerhalb. | Eine Lane im passenden Rang-Bereich wählen oder eine eigene erstellen. |
| Ranked ohne verifizierten Rang | DM-Hinweis, dass man für Ranked-Lanes einen verifizierten Rang braucht. | Ranked-Zugang erfordert eine verifizierte Rang-Rolle über die Steam-Verknüpfung. | Steam verknüpfen, um die Rang-Rolle zu erhalten. |
| Anfänger-Umleitung | Statt in die normale Lane landet man in einer Neue-Spieler-Lane. | Neu oder niedrig eingestufte Mitglieder werden in eine Einsteiger-Kategorie gelenkt. | Dort spielen; höher eingestufte Mitglieder spielen im normalen Bereich. |
| Live-Match-Status im Lane-Namen | Der Lane-Name bekommt einen Zusatz, der Match- oder Lobby-Status samt Spieleranzahl zeigt. | Die Steam-Presence der Mitglieder wird live an den Kanalnamen gehängt. | Nur Anzeige; nichts zu tun. |
| LFG-Gesuch erstellt | Ein eigener Forum-Post mit Modus, Rang-Bereich und Beitreten-Button; er räumt sich selbst weg, wenn die Lane schließt. | Die Mitspieler-Suche wurde als sichtbares Gesuch veröffentlicht. | Auf Beitritte warten oder selbst per Beitreten in andere Lanes springen. |
| LFG-Benachrichtigung | DM mit dem Hinweis auf ein passendes Gesuch und Link zum Thread. | Ein neues Gesuch passt zum eigenen Watch-Filter (einmalige Benachrichtigung). | Thread öffnen; für weitere Benachrichtigungen erneut Watch aktivieren. |
| Steam-Nudge-DM | DM mit der Aufforderung, Steam zu verknüpfen, plus Steam-Login-Button. | Man war länger in Voice ohne Steam-Verknüpfung. | Optional dem Login folgen oder die DM ignorieren/schließen. |
| Voice-Feedback-DM | DM mit einem Button zum Ausfüllen von Feedback. | Nach einer Voice-Session wird kurzes Feedback erbeten. | Ausfüllen oder ignorieren; das Fenster läuft nach einiger Zeit ab. |

## So läuft es ab

1. Mitglied betritt einen Erstell-/Router-Sprachkanal; der Bot legt eine neue Lane in der passenden Kategorie an und verschiebt das Mitglied hinein, das damit Owner wird.
2. Der Name wird je nach Modus vergeben (Casual/Chill/Street-Brawl bzw. ein Rang-Label bei Ranked).
3. Über das TempVoice-Panel verwaltet der Owner die Lane: Limit, Kick, Ban/Unban, Umbenennen, Region, Presets, Mindest-Rang, Lurker.
4. In Ranked-Lanes wird die Lane an einen Rang gebunden und danach benannt; nur passende Ränge können verbinden.
5. Live-Match-Status aus der Steam-Presence wird in Abständen an den Kanalnamen gehängt.
6. Verlässt der Owner die Lane, kann ein berechtigtes Mitglied sie übernehmen; leert sich die Lane, wird sie automatisch entfernt.

## Typische Meldungen & Fehler

| Signal | Was es bedeutet | Nächster Schritt |
| --- | --- | --- |
| Nur der Lane-Owner kann das. | Man versucht eine Owner-Aktion (Kick/Ban/Limit/Rename), ist aber nicht Owner der Lane. | Zuerst 'Owner übernehmen' nutzen (nur möglich, wenn der Owner die Lane verlassen hat und man die Bedingungen erfüllt). |
| Mindest-Rang ist hier deaktiviert. | In dieser Lane ist die Mindest-Rang-Funktion abgeschaltet (z. B. Street-Brawl-Modus). | Für eine Rang-Beschränkung eine Comp/Ranked-Lane verwenden. |
| Min-Rang gilt nur für Comp/Ranked-Lanes. | Ein Mindest-Rang wurde in einer Casual-/Chill-Lane versucht. | In eine Ranked-Lane wechseln, wenn ein Mindest-Rang gewünscht ist. |
| Unbekannter Rang bei der Eingabe | Der eingegebene Rang-Name wird nicht erkannt. | Einen gültigen Rang aus der Auswahl wählen (Haupt- oder Sub-Rang). |
| Du hast niemanden gebannt. | Unban wurde gedrückt, aber es existiert kein eigener Bann. | Keine Aktion nötig. |
| Kick/Limit/Ban fehlgeschlagen | Discord hat die Aktion abgelehnt (z. B. Person schon weg oder Rechteproblem). | Erneut versuchen; bei Dauerproblem an einen Moderator wenden. |
| Für Ranked-Lanes brauchst du einen verifizierten Rang. | Ranked-Beitritt/-Erstellung ohne verifizierte Rang-Rolle. | Steam verknüpfen, um die Rang-Rolle zu erhalten. |
| Dieses Feedback-Fenster ist abgelaufen. | Auf eine Feedback-DM wurde zu spät reagiert. | Anliegen direkt an das Team schreiben. |
| Danke, dein Voice-Feedback ist schon angekommen. | Feedback wurde bereits abgegeben. | Keine Aktion nötig. |

### Das darf der Support sagen

- Beim Beitritt eines Erstell-/Router-Kanals bekommst du automatisch eine eigene Lane und bist deren Owner; anpassen kannst du sie über das TempVoice-Panel.
- Wenn du eine Ranked-Lane nicht betreten kannst, obwohl Plätze frei sind, liegt dein Rang außerhalb des Lane-Rangs — wähle eine Lane im passenden Bereich oder erstelle eine eigene.
- Für Ranked-Lanes brauchst du eine verifizierte Rang-Rolle; die bekommst du, indem du Steam verknüpfst.
- Owner-Aktionen wie Kick, Ban oder Limit gehen nur, wenn du Owner der Lane bist — sonst zuerst 'Owner übernehmen', was erst nach dem Verlassen des bisherigen Owners möglich ist.

### Nie an Mitglieder weitergeben

- Interne Zahlen jeder Art: Schwellen, Sicherheitswerte, Gewichte, Zeitgrenzen, Limits.
- Die interne Entscheidungs- oder Durchsetzungslogik — welche Signale zu welcher Wirkung führen und in welcher Reihenfolge.
- Interne Technik: IDs, Pfade, Endpunkte, Namespaces, KI-Anbieter oder -Modelle, Zugangsdaten.
- Verdeckte Mechaniken oder Betriebsarten — auch nicht andeutungsweise, welche es geben könnte.
- Im Zweifel abstrahieren und an einen Menschen eskalieren (Details im Agenten-Leitfaden).

## Verwandte Seiten

- [Voice-Lane erstellen & verwalten](../workflows/voice-lane-erstellen-verwalten.md)
- [Mitspieler finden](../workflows/mitspieler-finden.md)

**Bewusst nicht dokumentiert:** verdeckte Mechaniken, Schwellenwerte und Zeitgrenzen, Zuordnungslogik, Durchsetzungsbedingungen, interne Endpunkte, Bewertungslogik. Diese internen Details bleiben aus Sicherheitsgründen außerhalb dieser Wissensbasis.
