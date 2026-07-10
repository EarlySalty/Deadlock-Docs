---
title: "Turniere"
tags: [turniere, events, community]
stand: 2026-07-10
quelle: "Deadlock-Turniere/rust (Code-Abgleich) + Deadlock-Bots/docs/turniere.md"
---
# Turniere

## Worum geht es?
Das Turnier-Portal auf der Website deckt den kompletten Spielerweg ab: Profil und Einwilligung hinterlegen, einem Event beitreten, ein Team gründen oder einem Team anschließen, Check-in erledigen und später Bracket, Gruppen und Leaderboard verfolgen. Sichtbar für Spieler sind vor allem die öffentlichen Turnierseiten, der eigene Status im Event, Team-Einladungen und die globale Rangliste.

Wichtig: Turniere laufen komplett über das Web-Portal. Die alten In-Discord-Turnierbefehle (z. B. `/turnier`, `!balance`) gibt es nicht mehr.

## Wie läuft die Anmeldung ab?
Vor der ersten Teilnahme musst du eingeloggt sein und den Consent-Flow abschließen. Ohne aktuelle Einwilligung blockiert das System jede Team- oder Solo-Anmeldung. Im selben Bereich kannst du auch dein Spielerprofil pflegen: Anzeigename, Bio, Avatar und Benachrichtigungsoptionen für Matchstart, Check-in, Team-Einladungen und Turnier-News.

Danach gibt es drei übliche Wege in ein Turnier:

- Du meldest dich solo an. Dann landest du zunächst als freier Spieler im Turnierpool.
- Du gründest ein eigenes Team. Das System setzt dich automatisch als Captain und trägt deine vorhandenen Rank-/Steam-Daten mit ein.
- Du trittst einem bestehenden Team bei oder nimmst eine Einladung an.

Beitritte und Bewerbungen sind offen, solange die Anmeldung läuft (Anmelde- und Check-in-Phase). Einige Aktionen gehen nur in der Anmeldephase: Solo-Abmeldung, Team verlassen, Mitglieder kicken und die direkte Captain-Einladung. Wenn ein Team schon voll ist, blockiert der Join. Wer bereits in einem Team desselben Turniers steckt, kann nicht parallel noch einem zweiten Team beitreten.

## Team- und Recruit-Flow
Captains können Teams auf drei Arten auffüllen:

- Direkte Einladung eines solo angemeldeten Spielers
- Einladung über einen konkreten Signup-Eintrag
- Bewerbungsmodus eines Teams

Teams haben dafür einen sichtbaren Recruiting-Status:

- **Offen**: direkte Beitritte sind möglich
- **Auf Bewerbung**: Interessenten schicken eine Bewerbung, der Captain entscheidet
- **Geschlossen**: kein Recruiting

Wenn du Einladungen lieber automatisch annehmen willst, kann dein Profil das speichern. Dann wird eine passende Team-Einladung sofort angenommen, ohne dass du noch einmal manuell klicken musst. Offene Einladungen kannst du außerdem gesammelt abrufen sowie einzeln annehmen oder ablehnen.

## Check-in und Turnierstatus
Für aktive Events gibt es einen separaten Check-in. Das System speichert, ob du bereits eingecheckt bist, und führt eine öffentliche Statusübersicht mit Anzahl registrierter und eingecheckter Spieler. Ohne gültigen Check-in riskierst du, beim Finalisieren des Teilnehmerfelds nicht berücksichtigt zu werden.

Öffentlich sichtbar sind außerdem:

- Turnierliste
- Turnierdetails
- Teams und Mitglieder
- Gruppenphase
- Bracket
- freie Einzelanmeldungen (Spieler ohne Team)

## Welche Formate gibt es?
Es gibt zwei Turnierformate:

- **K.-o.-Format**: direkt im Bracket, wer verliert ist raus.
- **Gruppenphase + Playoffs**: erst Gruppen, danach der K.-o.-Baum.

Welches Format ein Event nutzt, legt die Turnierleitung fest; größere Turniere laufen in der Regel mit Gruppenphase, kleinere direkt im Bracket. Den K.-o.-Baum gibt es als Single- und Double-Elimination. Für dich als Spieler heißt das vor allem: Je nach Event spielst du entweder sofort im K.-o.-Baum oder zuerst in Gruppen und danach in den Playoffs.

Dazu kommen Spielmodus-Varianten pro Event: Standard, Spiegel-Modus, alle denselben Helden, zufällige Helden und Single-Lane. Welche gilt, legt die Turnierleitung beim Anlegen fest — genauso wie Lobby-Details, Erinnerungen und der Umgang mit No-Shows.

## Leaderboard und Spielerprofil
Das globale Leaderboard ist öffentlich und sortiert nach Turnierpunkten. Angezeigt werden unter anderem:

- Gesamtpunkte
- gespielte Turniere
- gespielte und gewonnene Matches
- beste Platzierung
- aktueller Rank, falls vorhanden

Zusätzlich gibt es öffentliche Spielerprofile. Dort siehst du Anzeigename, Avatar, Bio, Rank, Statistiken und die bisherige Turnierhistorie mit Teamnamen. Das ist besonders nützlich, wenn du Kandidaten für dein Team oder bekannte Gegner einordnen willst.

## Draft-System aus Spielersicht
Ein Draft-System ist technisch vorhanden, aber aktuell kein Self-Service-Feature für normale Spieler. Die Draft-Session wird von Admin-Seite für ein Match gestartet und dort auch bedient. Für dich als Spieler bedeutet das praktisch:

- Es gibt eine definierte Hero-Liste für Drafts.
- Drafts hängen an konkreten Matches.
- Die Bedienung läuft derzeit nicht als Selbstbedienung für Spieler.

Wenn ein Event Draft-Regeln nutzt, bekommst du die Picks/Bans also nicht über ein eigenes Spieler-Dashboard, sondern über die Turnierleitung oder den Match-Flow mitgeteilt.

## Turnier-DMs abbestellen
Turnier-Benachrichtigungen per Discord-DM kannst du im Portal selbst abbestellen — getrennt nach Fun-Turnieren, Competitive oder allem. Der Bot überspringt dich dann bei den entsprechenden Erinnerungen.

## Häufige Grenzen
- Ohne aktuelle Einwilligung ist keine Anmeldung möglich.
- Captain-Wechsel und Team-Auflösung haben Sonderregeln: Ein Captain kann nicht einfach verschwinden, solange noch andere Teammitglieder im Kader sind.
- Ein Widerruf der Einwilligung ist blockiert, solange du in einem aktiven Turnier angemeldet bist.
- Einladungen **annehmen** und Bewerbungen **einreichen** geht nur, solange der Turnierstatus es erlaubt; **ablehnen** geht jederzeit.

Dein Rang und deine Steam-Angaben werden beim Anmelden und bei jedem Teamwechsel frisch nachgeladen, damit Bracket und öffentliches Profil zusammenpassen.

## Wann findet das nächste Turnier statt? Ist ein neues Turnier geplant?
Feste Termine gibt es hier bewusst nicht, die veralten sofort. Aktuelle und kommende Turniere findest du an zwei Stellen: in den Server-Ankündigungen <#1371952264620806214> und auf den öffentlichen Turnierseiten des Web-Portals. Wenn dort nichts angekündigt ist, steht der nächste Termin schlicht noch nicht fest. Das gilt auch für die Frage, ob gerade ein neues Turnier geplant ist: Sobald etwas geplant ist, steht es in den Ankündigungen und im Portal, vorher gibt es nichts Verlässliches.
