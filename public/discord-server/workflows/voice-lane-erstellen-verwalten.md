---
title: "Voice-Lane erstellen & verwalten"
tags: [discord-server, voice, lane, erstellen, verwalten]
stand: 2026-07-07
quelle: "Deadlock-Bots/docs/support-kb/workflows/voice-lane-erstellen-verwalten.html"
---
# Voice-Lane erstellen & verwalten

Wer einem Erstell-/Router-Sprachkanal beitritt, bekommt automatisch eine eigene, selbstverwaltete Voice-Lane und wird als Owner hineingezogen. Über ein Verwaltungs-Panel steuert der Owner Namen, Limit, Rausschmiss/Bann, Region und Mindest-Rang; in den Ranked-Kanälen werden Lanes nach Rang gruppiert.

## Was Mitglieder merken

Sobald du einem der Erstell-/Router-Sprachkanäle beitrittst, legt der Bot eine neue Lane an und verschiebt dich automatisch hinein — du bist deren Owner. Der Name richtet sich nach dem Modus (z. B. eine normale Lane, eine Chill-Lane oder eine Rang-benannte Ranked-Lane). Über das Panel "TempVoice" kannst du deine Lane umbenennen, das Teilnehmerlimit setzen, andere kicken oder bannen/entbannen, die Region (Deutsch/Offen) wählen, einen Mindest-Rang festlegen, Presets speichern und die Lane als stiller Zuhörer betreten. In den Ranked-Kanälen sortiert der Bot Lanes automatisch nach Rang und hängt den Rang an den Namen; zusätzlich kann der Lane-Name live den Deadlock-Match-Status zeigen. Bist du nicht Owner, kommt bei Owner-Aktionen eine Ablehnung, und du kannst die Lane erst übernehmen, wenn der bisherige Owner sie verlassen hat.

## Ablauf Schritt für Schritt

1. Betritt einen Erstell-/Staging-Sprachkanal; der Bot legt eine neue Lane in der passenden Kategorie an.
2. Du wirst automatisch in die Lane verschoben und wirst deren Owner.
3. Der Name wird je nach Modus vergeben (normale Lane / Chill / Street Brawl bzw. Rang-Label in Ranked).
4. Öffne das 'TempVoice'-Panel und nutze die Buttons: Owner übernehmen, Limit, Kick, Ban, Unban, Duo/Trio/Reset, Umbenennen, Presets, Region (DE/Offen), Lurker.
5. Deine Aktionen wirken sofort, solange du Owner bist; ein Ban gilt für alle deine Lanes bis zum Unban.
6. In Comp/Ranked-Lanes bindet der Bot die Lane an einen Rang-Anker, benennt den Kanal nach dem Rang und lässt nur Mitglieder im passenden Rang-Bereich beitreten (es wird nie gekickt, nur die Beitritts-Rechte gesetzt).

## Mögliche Ausgänge

- Eigene, selbstverwaltete Lane
- Angepasste Lane (Name, Limit, Region, Presets)
- Entfernte oder gebannte Mitglieder
- Rang-homogene Ranked-Lane

## Sichtbare Zustände

| Zustand | Was du siehst | Was es bedeutet | Sicherer nächster Schritt |
| --- | --- | --- | --- |
| Lane erstellt | Ein neuer Sprachkanal (z. B. 'Lane 2', 'Chill 3' oder 'Phantom 1'), in den du automatisch verschoben wirst. | Dein Beitritt zu einem Erstell-/Router-Kanal hat eine persönliche Lane erzeugt; du bist deren Owner. | Lane über das Verwaltungs-Panel anpassen oder einfach mit anderen spielen. |
| Lane-Verwaltungs-Panel | Embed 'TempVoice – <Lane>' mit Buttons: Owner übernehmen, Limit, Kick, Ban, Unban, Duo/Trio/Reset, Umbenennen, Presets, Region, Lurker. | Steuerzentrale für deine Lane; Buttons wirken sofort, sofern du Owner bist. | Gewünschte Aktion anklicken; bei 'Nur der Lane-Owner kann das.' zuerst Owner werden. |
| Owner übernommen | 'Du bist jetzt Owner dieser Lane.' | Der vorherige Owner hat die Lane verlassen und du erfüllst die Übernahme-Bedingungen. | Lane jetzt selbst verwalten. |
| Gebannt aus einer Lane | Du kannst der Lane nicht mehr beitreten; der Owner sieht einen Hinweis, dass der Bann für alle seine Lanes gilt. | Der Lane-Owner hat einen persönlichen Bann gesetzt, der für alle seine Lanes gilt. | Anderen Kanal nutzen oder den Owner um Entbannung bitten. |
| Ranked-Lane rang-gesperrt | Beitritt zu einer Ranked-Lane ist nicht möglich, obwohl Plätze frei wären; die Lane heißt nach einem Rang (z. B. 'Phantom 3'). | Die Lane ist an einen Rang-Bereich gebunden bzw. hat einen Mindest-Rang; deine Rang-Rolle liegt außerhalb. | Eine Lane im passenden Rang-Bereich wählen oder eine eigene erstellen. |
| Ranked ohne verifizierten Rang | DM-Hinweis, dass du für Ranked-Lanes einen verifizierten Rang brauchst. | Ranked-Zugang erfordert eine verifizierte Rang-Rolle über die Steam-Verknüpfung. | Steam verknüpfen, um die Rang-Rolle zu erhalten. |
| Anfänger-Umleitung | Statt in die normale Lane landest du in einer Neue-Spieler-Lane. | Neu oder niedrig eingestufte Mitglieder werden in eine Einsteiger-Kategorie gelenkt. | Dort spielen; höher eingestufte Mitglieder spielen im normalen Bereich. |
| Live-Match-Status im Lane-Namen | Lane-Name mit Zusatz wie 'im Match' plus Minuten/Slots oder 'in der Lobby'. | Die Steam-Presence der Mitglieder wird live an den Kanalnamen gehängt. | Nur Anzeige; nichts zu tun. |

## Typische Meldungen & Fehler

| Signal | Was es bedeutet | Nächster Schritt |
| --- | --- | --- |
| Nur der Lane-Owner kann das. | Du versuchst eine Owner-Aktion (Kick/Ban/Limit/Umbenennen), bist aber nicht Owner der Lane. | Zuerst 'Owner übernehmen' nutzen (nur möglich, wenn der Owner die Lane verlassen hat und du die Bedingungen erfüllst). |
| Mindest-Rang ist hier deaktiviert. | In dieser Lane ist die Mindest-Rang-Funktion abgeschaltet (z. B. Street-Brawl-Modus). | Für eine Rang-Beschränkung eine Comp/Ranked-Lane verwenden. |
| Min-Rang gilt nur für Comp/Ranked-Lanes. | Ein Mindest-Rang wurde in einer Casual-/Chill-Lane versucht. | In eine Ranked-Lane wechseln, wenn ein Mindest-Rang gewünscht ist. |
| Unbekannter Rang: <Eingabe> | Der eingegebene Rang-Name wird nicht erkannt. | Einen gültigen Rang aus der Auswahl wählen (Haupt- oder Sub-Rang). |
| Du hast niemanden gebannt. | Unban wurde gedrückt, aber es existiert kein eigener Bann. | Keine Aktion nötig. |
| Kick / Limit / Ban fehlgeschlagen | Discord hat die Aktion abgelehnt (z. B. Person schon weg oder Rechteproblem). | Erneut versuchen; bei Dauerproblem an einen Moderator wenden. |
| Für Ranked-Lanes brauchst du einen verifizierten Rang. | Ranked-Beitritt/-Erstellung ohne verifizierte Rang-Rolle. | Steam verknüpfen, um die Rang-Rolle zu erhalten. |

### Das darf der Support sagen

- Wenn du einem Erstell-/Router-Kanal beitrittst, bekommst du automatisch eine eigene Lane und wirst als Owner hineingezogen — verwalten kannst du sie über das TempVoice-Panel.
- Owner-Aktionen wie Kick, Ban oder Umbenennen gehen nur, wenn du Owner bist; übernehmen kannst du eine Lane erst, wenn der bisherige Owner sie verlassen hat.
- Ranked-Lanes lassen nur Mitglieder im passenden Rang-Bereich beitreten; ohne verifizierten Rang bekommst du einen DM-Hinweis — verknüpf dafür Steam, um die Rang-Rolle zu erhalten.
- Ein Bann des Lane-Owners gilt für alle seine Lanes, bis er ihn selbst wieder aufhebt; nutz solange einen anderen Kanal oder bitte um Entbannung.

### Nie an Mitglieder weitergeben

- Interne Zahlen jeder Art: Schwellen, Sicherheitswerte, Gewichte, Zeitgrenzen, Limits.
- Die interne Entscheidungs- oder Durchsetzungslogik — welche Signale zu welcher Wirkung führen und in welcher Reihenfolge.
- Interne Technik: IDs, Pfade, Endpunkte, Namespaces, KI-Anbieter oder -Modelle, Zugangsdaten.
- Verdeckte Mechaniken oder Betriebsarten — auch nicht andeutungsweise, welche es geben könnte.
- Im Zweifel abstrahieren und an einen Menschen eskalieren (Details im Agenten-Leitfaden).

## Verwandte Seiten

- [Voice-Lanes (TempVoice)](../module/voice-lanes.md)

**Bewusst nicht dokumentiert:** verdeckte Mechaniken, Schwellenwerte und Zeitgrenzen, Zuordnungslogik, Durchsetzungsbedingungen, interne Endpunkte. Diese internen Details bleiben aus Sicherheitsgründen außerhalb dieser Wissensbasis.
