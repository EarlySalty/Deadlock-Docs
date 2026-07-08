---
title: "User-Doku-Coverage-Audit fuer Concierge/RAG"
tags: [audit, public-docs, concierge, rag, user-doku]
stand: 2026-07-08
quelle: "Agenten-Audit ueber Deadlock-Bots, Steam-Bot, Twitch-Bot, Turniere, Patchnotes-Bot und Website"
---
# User-Doku-Coverage-Audit fuer Concierge/RAG

## Ziel

Der Concierge soll Nutzerfragen aus `public/` beantworten koennen, ohne interne Architektur, Prompts, Modelle, Secrets, Schwellenwerte oder Admin-Ablaeufe preiszugeben. Dieser Audit sammelt, wo der Code user-sichtbare Funktionen hat, die in `public/` fehlen, veraltet oder zu technisch sind.

Ausgeschlossen: Deadlock-Brain, AI-Coach, TradingBot.

## Harte Leitplanken fuer Public-Doku

- Public-Doku beschreibt nur sichtbares Nutzerverhalten: was ein Mitglied sieht, was es tun kann, was eine Meldung bedeutet.
- Keine internen Implementierungsdetails: keine DB-Tabellen, API-Routen, Ports, Service-Namen, Systemd, Infisical, Prompts, Modelle, Provider, Tokens.
- Keine Moderations-/Anti-Abuse-Mechanik: keine Schwellen, Scoring, Heuristiken, Retry-Caps, Erkennungslogik.
- Keine Admin-Workflows als Self-Service darstellen.
- Bei nicht oeffentlichen Daten immer fail-closed: Online-Zahlen, letzte Moderator-Nachrichten, private Viewer-/Member-Daten und aehnliches gehoeren nicht in Public-Doku.
- Alte Code-Funde sind nicht automatisch Zielzustand. Owner-Korrektur vom 2026-07-08: `/ticket` und `/betainvite` nicht mehr bewerben; Nutzer sollen im Fragekanal `https://discord.com/channels/1289721245281292288/1426220702054355077` fragen.

## Prioritaet P0: Falsche oder gefaehrlich veraltete Public-Antworten

### Fragekanal statt alter Ticket-/Invite-Flows

Status: Public-Doku und Code enthalten gemischte Altstaende. Einzelne Dateien sagen noch Ticket-Button, alte Code-/Servertexte nennen `/betainvite`, andere Dateien sagen bereits, dass Befehle nicht mehr gelten.

Zielzustand fuer Public-Doku:
- Kein `/ticket` als Nutzerweg.
- Kein `/betainvite` als Nutzerweg.
- Bei Support-, Invite- und allgemeinen Fragen auf den Fragekanal verweisen: `https://discord.com/channels/1289721245281292288/1426220702054355077`.
- Ticket-Auto-Hilfe nur dokumentieren, wenn es noch live und user-sichtbar ist; sonst aus Public-Doku entfernen.

Betroffene Public-Dateien:
- `public/discord-server/community-tools.md`
- `public/discord-server/negativ-wissen.md`
- `public/discord-server/team-und-ansprechpartner.md`
- `public/discord-server/regeln.md`
- `public/discord-server/haeufige-probleme.md`
- `public/discord-server/support/troubleshooting.md`
- `public/discord-server/module/faq-support.md`
- `public/discord-server/faq-bot-selbst.md`
- `public/discord-server/onboarding-und-invites.md`
- `public/discord-server/steam-integration.md`
- `public/discord-server/deadlock-grundlagen.md`

Beispielfragen, die danach eindeutig beantwortbar sein sollen:
- "Wo frage ich, wenn ich Hilfe brauche?"
- "Gibt es noch Tickets?"
- "Wie bekomme ich einen Deadlock Invite?"
- "Gibt es `/betainvite` noch?"

### Helden-Coverage und Aliase

Status: Website-Daten listen 38 Helden; `public/deadlock-helden/` hat 37 Dateien. `Seven` fehlt. Mehrere Namen weichen ab:
- Website: `Grey Talon`, Public: `talon.md`
- Website: `Lady Geist`, Public: `geist.md`
- Website: `Vyper`, Public: `viper.md`
- Website: `Holliday`, Public: `holyday.md`
- Website: `Graves`, Public: `fgraves.md`
- Website: `The Doorman`, Public: `doorman.md`
- Website: `Mo & Krill`, Public: `mo_krill.md`

Vorschlaege:
- `public/deadlock-helden/seven.md` ergaenzen.
- `public/deadlock-helden/aliases.md` ergaenzen oder Alias-Frontmatter in bestehende Heldenseiten aufnehmen.
- RAG-Frage "wie viele Charaktere gibt es?" erst nach Doc-Sync wieder gegen Public-Zaehler pruefen.

Beispielfragen:
- "Wie spielt man Seven?"
- "Ist Grey Talon dasselbe wie Talon?"
- "Wo finde ich Lady Geist?"
- "Heisst der Held Viper oder Vyper?"

### Urne / Spielbegriffe

Status: Reale Concierge-Fragen zu "Urne abgeben" fallen korrekt auf Gap, weil Public-Doku fehlt.

Vorschlag:
- `public/deadlock-guides/spielobjekte-und-belohnungen.md` oder bestehende `public/discord-server/deadlock-grundlagen.md` erweitern.
- Nur gesichertes, user-sichtbares Spielwissen dokumentieren. Keine Spekulation.

Beispielfragen:
- "Was bringt die Urne?"
- "Welche Vorteile bekomme ich, wenn ich die Urne abgebe?"
- "Was soll ich mit der Urne machen?"

## Prioritaet P1: Concierge-Antwortqualitaet deutlich verbessern

### Deadlock-Anfaenger-Guide

Status: Website hat einen kompletten Anfaenger-Guide; Public-Doku hat nur kurze Grundlagen.

Vorschlag:
- `public/deadlock-guides/anfaenger-guide.md`

Beispielfragen:
- "Wie fange ich mit Deadlock an?"
- "Was sind Souls?"
- "Welche Items soll ich zuerst kaufen?"
- "Welche Helden sind anfaengerfreundlich?"

### Items und Item-Anzahl

Status: Fragen nach Item-Anzahl fallen auf Gap. Es gibt keine vollstaendige, public-faehige Item-Liste.

Vorschlag:
- `public/deadlock-guides/items.md`
- Mindestens: erklaeren, wo Builds/Kernitems sichtbar sind, und dass keine vollstaendige statische Item-Zaehlliste garantiert wird, wenn sie nicht gepflegt ist.

Beispielfragen:
- "Wie viele Items gibt es?"
- "Welche Item-Arten gibt es?"
- "Wo sehe ich gute Items fuer meinen Helden?"

### Tierlist-/Meta-Fragen robust machen

Status: Direkte Fragen zu Tierlist/Winrate funktionieren oft, weiche Formulierungen wie "deine Meinung zum besten Champ" koennen auf Gap fallen.

Vorschlaege:
- `public/discord-server/tierlist-und-builds.md` um "beste Helden / Meinung / Meta" erweitern.
- Klarstellen: keine persoenliche Meinung, datenbasierte Tierlist unter `/builds/`.

Beispielfragen:
- "Wer ist gerade der beste Champ?"
- "Was ist deine Meinung zum besten Helden?"
- "Welche Heroes haben gerade die hoechste Winrate?"

### Concierge, Pate und Steckbrief

Status: `dm-concierge.md` erklaert den Bot grob; Pate/Steckbrief verdienen einen eigenen Nutzer-Workflow.

Vorschlag:
- `public/discord-server/workflows/concierge-pate-steckbrief.md`

Beispielfragen:
- "Wie lasse ich mich vorstellen?"
- "Postet der Bot meinen Steckbrief automatisch?"
- "Wie bekomme ich einen Paten?"
- "Was macht 'vergiss mich'?"

### Router / Auto-Join / Voice-Panel

Status: Voice-Doku ist breit, aber Router/Auto-Join ist fuer Nutzer verstreut.

Vorschlag:
- `public/discord-server/workflows/router-autojoin-nutzen.md`

Beispielfragen:
- "Was macht Auto-Join?"
- "Warum bleibe ich im Deadlock Router?"
- "Wie wechsle ich Casual, Ranked oder Street Brawl?"

### Clip-Einsendung

Status: Code hat Clip-Submission-Flows, Public-Doku ist grob.

Vorschlag:
- `public/discord-server/workflows/clip-einsenden.md`

Beispielfragen:
- "Wie reiche ich einen Clip ein?"
- "Warum wird mein Clip nicht sofort gepostet?"
- "Welche Angaben braucht das Formular?"

### Austritts-Feedback

Status: Website hat persoenliche Feedback-Links; Public-Erklaerung fehlt.

Vorschlag:
- `public/discord-server/workflows/austritts-feedback.md`

Beispielfragen:
- "Warum habe ich einen Feedback-Link bekommen?"
- "Kann ich Bilder anhaengen?"
- "Warum ist mein Link ungueltig?"

## Prioritaet P1: Steam-Bot und Rang

### Steam-Account verwalten

Status: Verknuepfen ist gut dokumentiert, Account-Verwaltung nur knapp.

Vorschlag:
- `public/discord-server/workflows/steam-account-verwalten.md`

Beispielfragen:
- "Wie aendere ich meinen Hauptaccount?"
- "Wie entferne ich einen falschen Steam-Link?"
- "Was bedeutet primary?"
- "Welche Eingaben akzeptiert `/steam whoami`?"

### Rang pruefen vs. Rollen synchronisieren

Status: Unterschied zwischen `/steam_rank` und `/checkrank` ist nicht klar genug.

Vorschlag:
- `public/discord-server/workflows/rang-pruefen-rollensync.md` oder `steam-verknuepfen-rang.md` erweitern.

Beispielfragen:
- "Warum stimmt meine Rolle nach `/steam_rank` nicht?"
- "Welcher Steam-Account zaehlt bei mehreren Accounts?"
- "Wann brauche ich `/checkrank`?"

### Steam-Bot-Meldungen

Status: Viele sichtbare Meldungen werden nicht gebuendelt erklaert.

Vorschlag:
- `public/discord-server/support/steam-bot-meldungen.md`

Beispielfragen:
- "Steam-Account ist schon verknuepft, was jetzt?"
- "Freundescode schon eingereicht?"
- "Freundschaft noch nicht bestaetigt?"
- "Deadlock schon im Account?"

### Verified oder Rang verloren

Status: Nutzerwirkung dokumentieren, aber keine Cleanup-/Retry-Interna.

Vorschlag:
- `public/discord-server/support/steam-freundschaft-und-verified-verloren.md`

Beispielfragen:
- "Warum ist meine Verified-Rolle weg?"
- "Warum muss ich den Bot wieder auf Steam adden?"
- "Was mache ich nach Server-Wiedereintritt?"

## Prioritaet P1: Twitch-Bot

### Raid-Doku korrigieren

Status: `public/twitch-bot/faq-raids.md` klingt zu sehr nach "immer aktiv / nichts tun"; reale Nutzerflaechen enthalten Auth/Re-Auth, Aktivierung, manuellen Raid, Status und History.

Vorschlag:
- `public/twitch-bot/faq-raids.md` aktualisieren.

Beispielfragen:
- "Warum hat der Bot nicht geraidet?"
- "Wie aktiviere ich Auto-Raid?"
- "Wie starte ich einen manuellen Raid?"

### Twitch-Community-FAQ korrigieren

Status: `!twl` und Affiliate/Leaderboard sind in Public-Doku teils fachlich schief.

Vorschlag:
- `public/twitch-bot/faq-community.md` korrigieren.

Beispielfragen:
- "Wo nutze ich `!twl`?"
- "Was zeigt das Leaderboard wirklich?"
- "Wie funktioniert das Affiliate-Portal?"

### Go-Live-Builder

Status: Public-Doku ist nur ein kurzer Einzeiler, real gibt es Builder, Preview, Testsendung und Platzhalter.

Vorschlag:
- `public/twitch-bot/go-live-builder.md` neu oder `public/twitch-bot/discord-golive.md` stark ausbauen.

Beispielfragen:
- "Kann ich den Discord-Go-Live-Post anpassen?"
- "Welche Platzhalter gehen?"
- "Warum wurde kein Post gesendet?"

### Verwaltung und Re-Auth

Status: Einstieg klingt zu glatt; Nutzer brauchen Hilfe bei fehlenden Rechten, Reconnects, Discord-/Steam-Linking.

Vorschlag:
- `public/twitch-bot/verwaltung-und-reauth.md`

Beispielfragen:
- "Wo sehe ich fehlende Rechte?"
- "Wie verbinde ich Discord oder Steam neu?"
- "Warum gehen Clips oder Raids gerade nicht?"

### Streamer-Dashboard und Social Media

Status: `twitch-streamer-dashboard.md` ist teils veraltet; `/social-media` ist streamer-relevant, nicht nur Admin-Kontext.

Vorschlaege:
- `public/twitch-bot/twitch-streamer-dashboard.md` aktualisieren.
- `public/twitch-bot/social-media-clips.md`
- `public/twitch-bot/highlight-clips.md`
- `public/twitch-bot/titel-generator.md`

Beispielfragen:
- "Welche Tabs habe ich im Free/Basic/Erweitert?"
- "Was ist auf `/social-media`?"
- "Wie bekomme ich Titelvorschlaege?"
- "Werden Shorts automatisch gepostet oder muss ich freigeben?"

### Preise und Analytics vereinheitlichen

Status: Preis-/Plan-Aussagen sind ueber mehrere Twitch-Dateien verteilt und koennen auseinanderlaufen.

Vorschlag:
- `public/twitch-bot/faq-plaene.md` als kanonische Preisquelle.
- Andere Twitch-Dateien auf Plan-Namen und grobe Feature-Gruppen beschraenken.

Beispielfragen:
- "Ist Analytics kostenlos?"
- "Was kostet werbefrei?"
- "Welche Features sind Free?"

## Prioritaet P1: Turniere und Scrims

### Team-Recruiting

Vorschlag:
- `public/turniere/team-recruiting.md`

Beispielfragen:
- "Warum kann ich mein Team nicht verlassen?"
- "Was heisst Bewerbung bei einem Team?"
- "Warum wurde eine Einladung automatisch angenommen?"

### Check-in und No-Show

Vorschlag:
- `public/turniere/checkin-und-no-show.md`

Beispielfragen:
- "Wo checke ich ein?"
- "Was passiert, wenn mein Gegner nicht kommt?"
- "Wie lange wartet ihr?"

### Lobby und Ergebnisse

Vorschlag:
- `public/turniere/lobby-und-ergebnisse.md`

Beispielfragen:
- "Wo finde ich den Join-Code?"
- "Wer darf ein Ergebnis melden?"
- "Warum steht mein Ergebnis noch nicht im Bracket?"

### Modi und Wertung

Vorschlag:
- `public/turniere/modi-und-wertung.md`

Beispielfragen:
- "Was ist ein Bracket Reset?"
- "Wer kommt aus Gruppen weiter?"
- "Was bedeutet Random Heroes?"

### Leaderboard, Profile und DMs

Vorschlaege:
- `public/turniere/leaderboard-und-profile.md`
- `public/turniere/dms-und-benachrichtigungen.md`
- `public/discord-server/referenz/status-und-fehler.md` um Turniermeldungen ergaenzen.

Beispielfragen:
- "Wie bekomme ich Punkte?"
- "Kann ich Avatar oder Bio aendern?"
- "Wie stelle ich Turnier-DMs aus?"
- "Warum kann ich nicht beitreten?"

### Scrim-Website-Flow

Status: Public-Doku nennt teils Chat-Command; Website hat Login, Webformular und "Mein Team".

Vorschlag:
- `public/discord-server/workflows/scrim-anmeldung-website.md` oder `public/discord-server/scrims.md` aktualisieren.

Beispielfragen:
- "Wo melde ich mich fuer Scrims an?"
- "Wie aendere ich meine Verfuegbarkeit?"
- "Warum sehe ich kein Team?"

## Prioritaet P1: Website-Portale

### Coaching-Website

Status: Grunddoku existiert, aber Coach-Auswahl, Profile, Bewertungen, Termine, Ziele und Meilensteine fehlen.

Vorschlag:
- `public/discord-server/workflows/coaching-website.md`

Beispielfragen:
- "Kann ich mir einen Coach aussuchen?"
- "Wo sehe ich Termine?"
- "Was sind Coaching-Ziele?"

### Patch-Timeline-Portal

Status: Patch-Bot ist dokumentiert, Website-Timeline nur grob.

Vorschlag:
- `public/patchnotes-bot/patch-timeline-portal.md`

Beispielfragen:
- "Wie finde ich alle Nerfs fuer Haze?"
- "Was bedeutet Hotspot?"
- "Warum sehe ich Fallback-Daten?"

### Portal-/URL-Karte

Status: `website-portale.md` ist gut, sollte aber Sitemap/Navigation nachziehen.

Vorschlag:
- `public/website/website-portale.md` aktualisieren.

Beispielfragen:
- "Welche Portale gibt es?"
- "Wo ist die Streamer-FAQ?"
- "Wo finde ich Turniere?"

## Prioritaet P2: Patchnotes-Bot

### Anzeige, Fortsetzungen und Emojis

Vorschlag:
- `public/patchnotes-bot/discord-anzeige.md`

Beispielfragen:
- "Warum haben Patchnotes Helden-Icons?"
- "Warum kommt ein Patch in mehreren Nachrichten?"
- "Was bedeutet Fortsetzung?"
- "Warum ist der Rollen-Ping eine eigene Nachricht?"

### Werte und Prozentangaben

Vorschlag:
- `public/patchnotes-bot/werte-und-prozentangaben.md`

Beispielfragen:
- "Warum steht da +17.6%?"
- "Berechnet der Bot Buff-/Nerf-Prozente?"
- "Sind Sekunden oder Meter auch abgedeckt?"

### Uebersetzung und Begriffe

Vorschlag:
- `public/patchnotes-bot/uebersetzung-und-begriffe.md`

Beispielfragen:
- "Warum bleibt Silenced englisch?"
- "Warum bleiben Itemnamen englisch?"
- "Fasst der Bot Patches zusammen oder uebersetzt er nur?"

### Concierge und neue Patches

Vorschlag:
- `public/patchnotes-bot/patchnotes-und-concierge.md`

Beispielfragen:
- "Kann der Concierge den neuesten Patch erklaeren?"
- "Warum kennt er einen gerade geposteten Patch noch nicht?"
- "Kann er mir den naechsten Patchtermin sagen?"

### Redaction in bestehender Patchnotes-Doku

Status: `public/patchnotes-bot/patchnotes-bot.md` nennt im technischen Abschnitt DB, Inhalts-Signatur, URL- und Patch-ID-Abgleich. Das ist fuer Public zu intern.

Vorschlag:
- Entschaerfen zu: "Der Bot merkt sich bereits veroeffentlichte Inhalte und aktualisiert danach die Wissensbasis."

## Dinge, die bewusst nicht public werden sollen

- Interne Architektur, Service-Aufteilung, Rust/Python-Cutover, Migrationsplaene.
- DB-Schemas, Tabellen, API-Routen, interne Ports, lokale Binary-Pfade.
- Secrets, Tokens, Infisical, systemd, Deployment-Runbooks.
- Prompts, Modellnamen, Provider, Tokenlimits, JSON-Schemas.
- Moderations-, Spam-, Scam-, Raid-, Matching- und Recruiter-Heuristiken.
- Exakte Schwellen, Scoring, Cooldowns, Retry-Caps, Cleanup-Intervalle.
- Private User-/Memberdaten: Online-Zahlen, weibliche User online, letzte Moderator-Nachricht, private Stream-Viewer-Daten.
- Admin-Only-Features als Nutzer-Self-Service.
- Deaktivierte oder experimentelle Features als live verfuegbar.

## Empfohlene Umsetzung in kleinen Batches

1. P0-Korrektur: Fragekanal als Support-/Invite-Ziel, keine `/ticket`-/`/betainvite`-Wege; Helden `Seven` und Aliase; Urne/Items falls gesicherte Daten vorhanden.
2. Concierge-Qualitaet: Anfaenger-Guide, Tierlist/Meta-Formulierungen, Concierge-Pate/Steckbrief, Router/Auto-Join.
3. Steam/Twitch: Steam-Account-Verwaltung, Rang-Sync, Twitch-Raids, Go-Live, Verwaltung/Re-Auth, Plan-Konsistenz.
4. Turniere/Scrims/Website: Team-Recruiting, Check-in, Lobby/Ergebnisse, Scrim-Webflow, Coaching-Website.
5. Patchnotes: Anzeige, Prozentwerte, Begriffe, Concierge-Sync, Redaction.

Nach jedem Public-Doku-Batch:
- `dl-knowledge` reload/restart oder `/internal/reload`, je nachdem was im Betrieb vorgesehen ist.
- Eine kleine Frage-Matrix gegen `/public/v1/ask` laufen lassen.
- Antworten auf interne Leaks pruefen.
