---
title: "Rang-Sichtbarkeit einstellen"
tags: [discord-server, rang, sichtbarkeit, einstellen]
stand: 2026-07-07
quelle: "Deadlock-Bots/docs/support-kb/workflows/rang-sichtbarkeit.html"
---
# Rang-Sichtbarkeit einstellen

Auf der Aktivitäts-Statistik-Seite kann jedes Mitglied selbst entscheiden, wer seinen Rang-Verlauf sehen darf: niemand, nur Server-Mitglieder oder alle. Persönliche Ansichten und das Umstellen der Sichtbarkeit setzen einen Login über Discord voraus.

## Was Mitglieder merken

Öffentliche Auswertungen (Aktivität nach Uhrzeit/Wochentag, Rangverteilung, Lane-Vorlieben, Voice- und Text-Leaderboards) sind auch ohne Login sichtbar. Nach Anmeldung über Discord kommen die eigenen Werte dazu: Voice-Zeit, Nachrichten, Punkte, Platzierung, Verlauf, Heatmap und Mitspieler. Der eigene Rang-Verlauf bleibt für andere unsichtbar, bis man ihn selbst freigibt. Im Dashboard lässt sich die Stufe wählen: privat, nur Mitglieder oder öffentlich. Erst mit "öffentlich" taucht man im Rang-Leaderboard und in der öffentlichen Rang-Historie auf; mit "nur Mitglieder" sehen den Verlauf ausschließlich Personen, die aktuell auf dem Server sind.

## Ablauf Schritt für Schritt

1. Über Discord anmelden, um den persönlichen Bereich freizuschalten.
2. Im Dashboard die Einstellung für die Rang-Verlauf-Sichtbarkeit öffnen.
3. Eine Stufe wählen: privat, nur Mitglieder oder öffentlich.
4. Die Einstellung wird gespeichert.
5. Sichtbarkeit im Rang-Leaderboard und in der öffentlichen Historie richtet sich danach.
6. Zum Zurückziehen die Sichtbarkeit wieder auf privat setzen.

## Mögliche Ausgänge

- privat: der Rang-Verlauf ist für niemanden sichtbar und man erscheint nicht im Rang-Leaderboard.
- nur Mitglieder: der Rang-Verlauf ist nur für aktuelle Server-Mitglieder sichtbar.
- öffentlich: der Rang-Verlauf ist für alle sichtbar und erscheint im Rang-Leaderboard.
- Angemeldet: persönliche Stats und die Sichtbarkeits-Einstellung sind verfügbar.
- Login abgebrochen/fehlgeschlagen: die Anmelde-Aufforderung bleibt bestehen.

## Sichtbare Zustände

| Zustand | Was du siehst | Was es bedeutet | Sicherer nächster Schritt |
| --- | --- | --- | --- |
| Nicht eingeloggt (persönlicher Bereich) | Persönliche Ansichten (eigene Stats, Verlauf, Heatmap, Mitspieler) zeigen eine Anmelde-Aufforderung statt Daten. | Es besteht keine gültige Discord-Sitzung; öffentliche Auswertungen bleiben trotzdem sichtbar. | Über Discord anmelden, danach die persönliche Ansicht erneut öffnen. |
| Rang-Historie: privat | Der eigene Rang-Verlauf erscheint für andere nicht und man taucht nicht im Rang-Leaderboard auf. | Dieser Zustand gilt, solange man die Sichtbarkeit nicht selbst freigegeben hat. | Im Dashboard die Sichtbarkeit auf 'nur Mitglieder' oder 'öffentlich' stellen. |
| Rang-Historie: nur Mitglieder | Der Rang-Verlauf ist nur für aktuelle Server-Mitglieder sichtbar; Außenstehende sehen ihn nicht. | Für andere ist nur freigegebene Rang-Historie sichtbar. | Für volle Öffentlichkeit auf 'öffentlich' umstellen. |
| Rang-Historie: öffentlich | Der Rang-Verlauf ist für alle sichtbar und erscheint im Rang-Leaderboard. | Die Sichtbarkeit wurde vollständig freigegeben. | Zum Zurückziehen die Sichtbarkeit wieder auf 'privat' setzen. |
| Eigene Stats vorhanden / leer | Bei fehlenden Aktivitätsdaten werden Nullwerte und keine Platzierung angezeigt. | Für das Konto liegen noch keine Voice-/Text-Sitzungen vor. | Aktiv werden (Voice/Text) und später erneut prüfen; Daten aktualisieren sich verzögert. |

## Typische Meldungen & Fehler

| Signal | Was es bedeutet | Nächster Schritt |
| --- | --- | --- |
| Eine persönliche Ansicht verlangt eine Anmeldung statt Daten anzuzeigen. | Es gibt keine gültige Sitzung für einen persönlichen Bereich. | Neu über Discord anmelden und erneut versuchen. |
| Die Rang-Sichtbarkeit lässt sich nicht speichern, weil ein unzulässiger Wert gewählt wurde. | Zulässig sind nur die Stufen privat, nur Mitglieder oder öffentlich. | Eine der angebotenen Sichtbarkeitsstufen wählen. |
| Die Rang-Historie einer Person ist nicht auffindbar. | Nicht freigegebene Historie ist für andere nicht einsehbar - sie ist dann für andere nicht einsehbar. | Prüfen, ob die Person ihre Historie freigegeben hat und ob man selbst berechtigt (Mitglied) ist. |
| Der Login-Dienst antwortet nicht oder liefert eine ungültige Antwort. | Die Anmeldung über Discord ist gerade nicht möglich. | Später erneut anmelden; bei Dauerproblem den Betreiber informieren. |
| Die Statistik lädt wegen eines internen Fehlers nicht. | Interner Server-/Datenbankfehler beim Laden der Statistik. | Später erneut versuchen; bei Wiederholung den Betreiber informieren. |
| Die Statistik-Seite lässt sich gerade nicht aufrufen. | Die Seite selbst konnte nicht ausgeliefert werden. | Später erneut aufrufen. |

### Das darf der Support sagen

- Der Rang-Verlauf ist für andere zunächst nicht sichtbar; du gibst ihn selbst im Dashboard frei.
- Mit 'nur Mitglieder' sehen ihn nur aktuelle Server-Mitglieder, mit 'öffentlich' alle - und dann erscheinst du im Rang-Leaderboard.
- Wenn dich jemand nicht sehen kann, prüfe deine gewählte Stufe und ob die Person noch auf dem Server ist.
- Für persönliche Ansichten musst du dich über Discord anmelden; ohne Login kommt eine Anmelde-Aufforderung.

### Nie an Mitglieder weitergeben

- Interne Zahlen jeder Art: Schwellen, Sicherheitswerte, Gewichte, Zeitgrenzen, Limits.
- Die interne Entscheidungs- oder Durchsetzungslogik — welche Signale zu welcher Wirkung führen und in welcher Reihenfolge.
- Interne Technik: IDs, Pfade, Endpunkte, Namespaces, KI-Anbieter oder -Modelle, Zugangsdaten.
- Verdeckte Mechaniken oder Betriebsarten — auch nicht andeutungsweise, welche es geben könnte.
- Im Zweifel abstrahieren und an einen Menschen eskalieren (Details im Agenten-Leitfaden).

## Verwandte Seiten

- [Statistiken & Privatsphäre](../module/statistiken-privatsphaere.md)

**Bewusst nicht dokumentiert:** verdeckte Mechaniken, Durchsetzungsbedingungen, Zugangsdaten, Schwellenwerte und Zeitgrenzen, interne Endpunkte. Diese internen Details bleiben aus Sicherheitsgründen außerhalb dieser Wissensbasis.
