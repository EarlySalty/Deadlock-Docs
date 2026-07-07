---
title: "Statistiken & Privatsphäre"
tags: [discord-server, statistiken, privatsphaere]
stand: 2026-07-07
quelle: "Deadlock-Bots/docs/support-kb/modules/statistiken-privatsphaere.html"
---
# Statistiken & Privatsphäre

Die Aktivitäts-Statistik-Website zeigt öffentliche Auswertungen (Aktivität nach Uhrzeit/Wochentag, Rangverteilung, Lane-Vorlieben, Voice- und Text-Leaderboards) und nach Discord-Login die eigenen Werte. Den eigenen Rang-Verlauf gibt jedes Mitglied selbst frei; zusätzlich lässt sich per Datenschutz-Opt-out die gesamte Erfassung abschalten.

## Was Mitglieder merken

Auf der Statistik-Seite sieht jedes Mitglied auch ohne Login öffentliche Auswertungen: Aktivität pro Uhrzeit und Wochentag, Rangverteilung, Lane-Vorlieben sowie Voice- und Text-Leaderboards. Nach Login über Discord kommen die eigenen Werte dazu (Voice-Zeit, Nachrichten, Punkte, Platzierung, Verlauf, Heatmap, Mitspieler). Der eigene Rang-Verlauf ist standardmäßig für andere nicht sichtbar; wer im Rang-Leaderboard und in der öffentlichen Rang-Historie auftauchen möchte, gibt ihn im Dashboard selbst frei – wahlweise für niemanden, nur für Server-Mitglieder oder für alle. Über die Statistik-Befehle im Discord lassen sich eigene Aktivität, Nachrichten und Mitspieler abfragen. Wer gar nicht erfasst werden will, nutzt den Datenschutz-Opt-out; danach sammelt und zeigt der Bot keine Aktivitätsdaten mehr.

## Mögliche Ausgänge

- Angemeldet: persönliche Stats, Verlauf, Heatmap und Mitspieler sichtbar.
- Abgebrochen oder nicht angemeldet: Anmelde-Aufforderung bleibt, öffentliche Zahlen bleiben sichtbar.
- Rang-Historie privat: für niemanden sichtbar, kein Eintrag im Rang-Leaderboard.
- Rang-Historie nur Mitglieder: nur für aktuelle Server-Mitglieder sichtbar.
- Rang-Historie öffentlich: für alle sichtbar und im Rang-Leaderboard.
- Opt-out aktiv: keine Erfassung, Statistik-Befehle liefern keine Daten.

## Sichtbare Zustände

| Zustand | Was du siehst | Was es bedeutet | Sicherer nächster Schritt |
| --- | --- | --- | --- |
| Nicht eingeloggt (persönlicher Bereich) | Persönliche Ansichten (eigene Stats, Verlauf, Heatmap, Mitspieler) antworten mit einer Anmelde-Aufforderung statt mit Daten. | Es besteht keine gültige Discord-Sitzung; öffentliche Auswertungen bleiben trotzdem sichtbar. | Über Discord anmelden und die persönliche Ansicht erneut öffnen. |
| Rang-Historie: privat | Der eigene Rang-Verlauf erscheint für andere nicht und man taucht nicht im Rang-Leaderboard auf. | Dieser Zustand gilt, solange man die Sichtbarkeit nicht selbst freigegeben hat. | Im Dashboard die Sichtbarkeit auf 'nur Mitglieder' oder 'öffentlich' stellen. |
| Rang-Historie: nur Mitglieder | Der Rang-Verlauf ist nur für aktuelle Server-Mitglieder sichtbar; Außenstehende sehen ihn nicht. | Für andere ist nur freigegebene Rang-Historie sichtbar. | Für volle Öffentlichkeit auf 'öffentlich' umstellen. |
| Rang-Historie: öffentlich | Der Rang-Verlauf ist für alle sichtbar und erscheint im Rang-Leaderboard. | Die Sichtbarkeit wurde vollständig freigegeben. | Zum Zurückziehen die Sichtbarkeit wieder auf 'privat' setzen. |
| Eigene Stats vorhanden / leer | Bei fehlenden Aktivitätsdaten werden Nullwerte und keine Platzierung angezeigt. | Für das Konto liegen noch keine Voice-/Text-Sitzungen vor. | Aktiv werden (Voice/Text) und später erneut prüfen; Daten aktualisieren sich verzögert. |
| Datenschutz-Opt-out aktiv | Statistik-Befehle liefern 'keine Daten'; die eigene Aktivität taucht nirgends auf. | Für dieses Mitglied werden keine Aktivitätsdaten mehr geschrieben oder ausgewertet. | Opt-out zurücknehmen, wenn man wieder erfasst werden möchte. |

## So läuft es ab

1. Statistik-Seite aufrufen; öffentliche Auswertungen sind auch ohne Login sichtbar.
2. Für die eigenen Werte über Discord anmelden; danach werden die persönlichen Ansichten freigeschaltet.
3. Im Dashboard die Rang-Sichtbarkeit wählen: privat, nur Mitglieder oder öffentlich.
4. Einstellung speichern; Rang-Leaderboard und öffentliche Historie richten sich danach.
5. Wer gar nicht erfasst werden möchte, aktiviert den Datenschutz-Opt-out; danach werden keine Aktivitätsdaten mehr geschrieben oder gezeigt.
6. Opt-out zurücknehmen, wenn man wieder erfasst werden will.

## Typische Meldungen & Fehler

| Signal | Was es bedeutet | Nächster Schritt |
| --- | --- | --- |
| Persönliche Ansicht verlangt Anmeldung | Für einen persönlichen Bereich besteht keine gültige Sitzung. | Neu über Discord anmelden und erneut versuchen. |
| Ungültige Sichtbarkeitsstufe gewählt | Beim Setzen der Rang-Sichtbarkeit wurde ein unzulässiger Wert übergeben; erlaubt sind nur privat, nur Mitglieder oder öffentlich. | Eine der angebotenen Sichtbarkeitsstufen wählen. |
| Ungültiger Filter- oder Ansichtsparameter | Ein Wert für Sortierung, Zeitraum, Modus oder Anzahl war unzulässig. | Seite neu laden und Filter über die Oberfläche statt manuell setzen. |
| Rang-Historie nicht auffindbar | Nicht freigegebene Rang-Historie ist für andere nicht einsehbar. | Prüfen, ob die Person ihre Historie freigegeben hat und ob man selbst berechtigt (Mitglied) ist. |
| Unbekannter Rangname | Es wurde ein Rang angefragt, den es nicht gibt. | Einen der gültigen Ränge auswählen. |
| Login-Dienst antwortet nicht | Der Anmeldedienst ist gerade nicht erreichbar oder liefert eine ungültige Antwort. | Später erneut anmelden; bei Dauerproblem den Betreiber informieren. |
| Interner Fehler beim Laden der Statistik | Beim Laden der Auswertung ist serverseitig etwas schiefgelaufen. | Später erneut versuchen; bei Wiederholung den Betreiber informieren. |
| Statistik-Seite nicht verfügbar | Die Seite selbst konnte gerade nicht ausgeliefert werden. | Später erneut aufrufen. |
| Keine Aktivitäts-/Nachrichtendaten vorhanden | Für die abgefragte Person liegen keine passenden Daten vor, oder sie hat Datenschutz-Opt-out aktiviert. | Hinweisen, dass Daten erst nach etwas Aktivität entstehen; bei dauerhaftem Fehlen Opt-out als Ursache prüfen. |

## Befehle

- `!myactivity`
- `!useranalysis`
- `!ua`
- `!analyze`
- `!messagestats`
- `!memberevents`
- `!tleaderboard`
- `!serverstats`

### Das darf der Support sagen

- Der eigene Rang-Verlauf ist standardmäßig für andere nicht sichtbar; du musst ihn im Dashboard selbst freigeben, um im Rang-Leaderboard aufzutauchen.
- Die Stufe 'nur Mitglieder' zeigt deinen Rang-Verlauf ausschließlich aktuellen Server-Mitgliedern; wer den Server verlassen hat, sieht ihn nicht mehr.
- Wenn dich jemand nicht in der Rang-Historie findet, prüfe die gewählte Sichtbarkeitsstufe und ob die Person noch Mitglied ist – eine nicht freigegebene Historie sieht aus wie eine nicht vorhandene.
- Mit dem Datenschutz-Opt-out kannst du die gesamte Aktivitätserfassung abschalten; danach zeigen die Statistik-Befehle keine Daten mehr, bis du es zurücknimmst.

### Nie an Mitglieder weitergeben

- Interne Zahlen jeder Art: Schwellen, Sicherheitswerte, Gewichte, Zeitgrenzen, Limits.
- Die interne Entscheidungs- oder Durchsetzungslogik — welche Signale zu welcher Wirkung führen und in welcher Reihenfolge.
- Interne Technik: IDs, Pfade, Endpunkte, Namespaces, KI-Anbieter oder -Modelle, Zugangsdaten.
- Verdeckte Mechaniken oder Betriebsarten — auch nicht andeutungsweise, welche es geben könnte.
- Im Zweifel abstrahieren und an einen Menschen eskalieren (Details im Agenten-Leitfaden).

## Verwandte Seiten

- [Rang-Sichtbarkeit einstellen](../workflows/rang-sichtbarkeit.md)

**Bewusst nicht dokumentiert:** verdeckte Mechaniken, Durchsetzungsbedingungen, sonstige interne Details, Bewertungslogik, Ranking- und Sortierlogik, Schwellenwerte und Zeitgrenzen, interne Endpunkte. Diese internen Details bleiben aus Sicherheitsgründen außerhalb dieser Wissensbasis.
