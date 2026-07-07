---
title: "Deadlock Scrims"
tags: [discord-server, scrims, discord]
stand: 2026-07-07
quelle: "Deadlock-Bots/docs/scrims.html"
---
# Deadlock Scrims

Anmeldung, Teams und Matches — automatisch statt per Hand.

## 🎯 Was das Ganze macht

Früher lief bei den Scrims alles manuell: Anmeldung als Freitext, Teams von Hand in einer Excel-Tabelle, Termine per Umfrage auszählen, Lobby- und Match-Codes einzeln tippen. Jetzt übernimmt der Bot die Fließarbeit.

**Anmeldung** → **Team-Bau** → **Match starten** → **Lobby & Join-Code** → **Ergebnis**

Du meldest dich einmal strukturiert an, die Coaches bauen daraus die Teams und starten das Match mit einem Klick — der Bot erstellt die Custom-Lobby, lädt alle ein und trägt hinterher den Sieger ein.

## Wann ist das nächste Scrim?
Feste Scrim-Termine stehen nicht in dieser Doku, die plant das Coaching-Team nach den Verfügbarkeiten aus den Anmeldungen. Konkrete Ansagen kommen in den Scrim-Ankündigungskanal <#1521522998199324853>. Wenn du im Pool bist (einmal `/scrim-signup` ausfüllen), wirst du eingeplant und dein Team-Channel bekommt rechtzeitig den Join-Code.

## 🎮 Für Spieler — so meldest du dich an

1. Tippe `/scrim-signup` in den Chat. Es öffnet sich ein kurzes Formular.
2. Trag ein: **Rang** (leer lassen, wenn dein Steam verifiziert ist — dann übernimmt der Bot ihn automatisch), **bevorzugte Rolle/Lane** und **wann du kannst** (z. B. „Mo-Fr ab 19 Uhr" oder „Wochenende ganzer Tag").
3. Absenden — fertig. Du bist im Pool, die Coaches sehen dich und planen dich ein.
4. Wenn dein Match ansteht, postet der Bot den **Join-Code** in euren Team-Channel. Reinklicken, spielen.

Verknüpf deinen Steam-Account unter **🔗deadlock-rang**. Dann wird dein Rang verifiziert übernommen *und* der Bot kann dich direkt in die Lobby einladen — ohne Steam-Link musst du per Join-Code manuell beitreten.

## 🏆 Für Coaches — Matches ohne Handarbeit

Im **Coaching-Dashboard** gibt es einen neuen **Scrims-Tab**. Alles läuft dort, kein SQL, kein Gefrickel.

### Ein Match durchziehen

1. **Match anlegen**: Team A gegen Team B wählen, optional Termin und dich selbst als Zuschauer (Discord-ID) eintragen.
2. **Start** drücken. Der Bot erstellt die Custom-Lobby, lädt beide Teams ein und postet den Join-Code in die Team-Channels.
3. Nach dem Spiel **Ergebnis holen** drücken — der Bot zieht das Match-Ergebnis von Steam und trägt den Sieger ein.

### Pool & Notizen

Im Teilnehmer-Pool siehst du Rang, Rolle und Verfügbarkeit jedes Spielers und kannst eine private **Coach-Notiz** hinterlegen (nur im Cockpit sichtbar).

Der Bot fasst laufende Matches nicht an: solange ein Match läuft, sind „Start"/„Ergebnis" gesperrt — so kommt nichts durcheinander. Spieler ohne verknüpften Steam-Account kann der Bot nicht automatisch einladen; die kommen über den Join-Code rein.

## ⚙️ Wie es unter der Haube funktioniert

Der Start läuft vollautomatisch: Der Bot erstellt die Lobby, lädt verknüpfte Spieler ein und meldet den Join-Code zurück in den Channel — dieselbe bewährte Technik wie bei den Turnieren.

Deutsche Deadlock Community — Scrim-Automatik. Fragen? Im Coaching-Chat oder beim Team melden.
