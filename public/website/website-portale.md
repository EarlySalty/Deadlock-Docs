---
title: "Website-Portale"
tags: [website, portale, community]
stand: 2026-07-10
quelle: "Website/dl-* (Code-Abgleich) + Deadlock-Bots/docs/website-portale.md"
---
# Website-Portale

## Worum geht es?
Die Website ist kein einzelner Monolith, sondern besteht aus mehreren klar getrennten Portalen. Für Nutzer sind vor allem diese Einstiege relevant: die Landing-Website, das Aktivitäts-Portal, das Patch-Notes-Portal, das Tierlist-/Builds-Portal und der Coaching-Bereich (inklusive Scrim-Anmeldung). Jedes Subportal löst einen anderen Teil der Community-Erfahrung ab, vom Einstieg über Statistiken bis zu Meta- und Patch-Inhalten.

## Landing
Die Startseite unter `/` ist die zentrale Einstiegsoberfläche der Community, aufgebaut als „Aufzug" mit Navigation und klaren Discord-CTAs. Von dort geht es auf mehrere Unterseiten: Mitspieler, Helden-Übersicht, Guides, Beitreten und die Austritts-Umfrage. Der Streamer-Bereich, das Turnier-Portal und der Brain-Bereich sind ebenfalls von der Startseite verlinkt, laufen aber als eigene Portale (Details in den jeweiligen Bereichen).

Aus Nutzersicht bietet die Landing vor allem:

- einen klaren Community-Einstieg mit Discord-CTA
- eine Navigation auf die anderen Portale
- redaktionelle Seiten wie Guide- und Hero-Übersicht
- Live-Community-Signale auf der Mitspieler-Seite

Die Mitspieler-Seite zieht ihre Zahlen live aus Discord: die aktuelle Mitglieder- und Online-Zahl sowie ein „Server-Hochhaus", das zeigt, welche Voice-Bereiche gerade besetzt sind. Das aktualisiert sich von selbst, ohne dass jemand die Seite pflegen muss. Ist Discord kurz nicht erreichbar, zeigt die Seite einen Hinweis statt leerer Felder.

## Activity
Das Aktivitäts-Portal ist der Statistikbereich. Dort gibt es mehrere Tabs für Voice, Text, Peaks und einen persönlichen Bereich. Ein Teil ist öffentlich sichtbar, der persönliche Bereich hängt am Discord-Login.

Öffentlich zugänglich sind unter anderem:

- Voice-Leaderboards
- Text-Leaderboards
- Rank-Distribution
- Aktivitäts-Timelines über mehrere Tage oder Wochen

Nach Login kommen persönliche Ansichten dazu: eigene Stats, Voice- und Text-Historie, Heatmap und Co-Player-Ansicht.

Die Oberfläche arbeitet stark mit Diagrammen und aufbereiteten Übersichten. Für Nutzer heißt das: keine Rohdaten, sondern fertige Auswertungen zu Vergleich, Verlauf und Aktivitätsmustern. Die Zahlen stammen aus dem Aktivitäts-Tracking des Bots.

## Patch Notes
Das Patch-Portal ist ein lesbarer Patch-Archiv-Bereich. Die Seite lädt Patch-Daten aus einer öffentlichen API und zeigt sie als interaktive Ansicht: Zeitleiste mit Patch-Balken, Übersicht der betroffenen Helden/Items und ein Event-Feed mit Detailansicht.

Wichtige Funktionen:

- Volltextsuche über Patch-Inhalte
- Kategorien-Filter
- Zeitleisten-Ansicht über alle erfassten Patches
- Detailansicht pro Änderung
- Link zurück zur Originalquelle

Der Nutzer bekommt damit keine rohe Forenansicht, sondern eine aufbereitete, deutsch lesbare Archiv-Seite. Bei Ladeproblemen zeigt das Portal explizit eine Fehlermeldung bzw. einen Fallback statt still leer zu bleiben.

## Tierlist / Builds
Das Tierlist-Portal (unter `/builds/`) ist der Meta-Bereich für Hero-Rankings und Build-Empfehlungen. Im ausgelieferten Public-Frontend sind vor allem drei Dinge sichtbar:

- aktuelle Tierliste
- Build-Voting
- Tierlist-Historie

Die Tierliste lässt sich nach Skill-Bereich filtern (All Skill, Phantom+ oder Eternus). Nutzer können zwischen Grid- und Listenansicht wechseln, nach Helden suchen und einzelne Helden aufklappen. Im Detailpanel sieht man Build-Beschreibungen, Kernitems, Ability-Reihenfolge und kann positiv oder negativ voten.

Zusätzlich gibt es eine History-Seite, auf der Snapshots verschiedener Patches oder Abrufe gegeneinander gestellt werden. Falls das Live-Backend ausfällt, besitzt das Portal einen Static-Fallback mit zuletzt gespeicherten JSON-Daten — die Seite fällt dann nicht komplett aus, sondern zeigt weiterhin einen brauchbaren Stand.

## Coaching & Scrims
Der Coaching-Bereich ist ein eigenes Portal unter `/coaching` mit Discord-Login: Anfrage-Formular für kostenloses Coaching (`/coaching/anfrage`), Scrim-Anmeldung und für Coaches eine eigene Plattform mit Warteschlange, Coachee-Details, Zielen/Notizen und Terminen. Details stehen in der Coaching-Doku.

