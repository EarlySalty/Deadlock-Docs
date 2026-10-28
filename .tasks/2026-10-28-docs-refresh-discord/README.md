# Docs-Refresh Discord (2026-10-28)

Ziel: Der Deadlock Brain soll Fragen zum Discord-Server der Deutschen Deadlock Community (Guild 1289721245281292288) aus den öffentlichen Docs beantworten können.

Geltungsbereich: `public/discord-server/` und Discord-bezogene Seiten im `public/`-Stamm.

Abnahme: Jedes Thema der Tabelle hat eine Quelle und eine Seite mit Status. Neue Seiten sind validiert. Die Brain-Abdeckung ist separat gemessen (siehe offene Punkte).

## Coverage-Tabelle

| Thema | Quelle | Docs-Seite | Status |
|---|---|---|---|
| Turnierformate (Gruppenphase, Bracket, Single/Double Elimination) | Deadlock-Turniere `docs/HELP_TOURNAMENT_MODES.md` | `public/discord-server/turniere.html` | neu, gegen Quelle geprüft |
| Anmeldung und Check-in für Turniere | Deadlock-Turniere `docs/HELP_TOURNAMENT_MODES.md` | `public/discord-server/turniere.html` | neu, gegen Quelle geprüft |
| Comp-Finder (Lobby, 6 Plätze, Code, 24 h, Prioritäten, keine Discord-Nachrichten) | Deadlock-Turniere `docs/comp-finder.md` | `public/discord-server/turniere.html` | neu, gegen Quelle geprüft |
| Kanäle nach Zweck (Information, Neue Spieler, Community, Support, Voice, Custom Games, Rang-Rollen) | Live-Kanalliste über dl-bot `api_call` GET `/guilds/1289721245281292288/channels`, Overwrites für @everyone | `public/discord-server/kanaele-und-rollen-karte.html` | neu, Stand 2026-10-28. Nur Kanäle ohne @everyone-Sichtverbot. Coaching-, Scrim- und Streamer-Bereiche sind bewusst nicht enthalten, weil sie für Mitglieder ohne Rolle nicht sichtbar sind. Offen: Sichtbarkeit von dev-updates und mitspieler-suche für Mitglieder mit Rolle klären. |
| Rang-Rollen (Initiate bis Eternus, 11 Haupt-Ränge) | Bots `dl-voice/src/rank.rs` (`major_rank_roles`), `dl-stats/src/ranks.rs` (`RANK_ORDER`) | `kanaele-und-rollen-karte.html`, `workflows/steam-verknuepfen-rang.html` | Live-Abgleich 2026-10-28 (dl-bot `api_call` GET `/guilds/1289721245281292288/roles`, 212 Rollen): Live-Ränge sind Initiate, Seeker, Acolyte, Sentinel, Mystic, Ritualist, Emissary, Oracle, Phantom, Ascendant, Eternus (je 6 Stufen, plus „(unverifiziert)"-Varianten). Alchemist, Arcanist und Archon existieren nicht mehr. Die fünf Rollen-IDs in `dl-voice/src/rank.rs:58-68` (1331457571118387210, 1331457699992436829, 1331457724848017539, 1331457949654319114, 1331458087349129296) sind in der Guild nicht vorhanden. Die Code-Tabelle ist veraltet; die Docs folgen der Live-Guild. |
| Ping-Rollen und Benachrichtigungen | Live-Rollenliste | `kanaele-und-rollen-karte.html` | neu, allgemein formuliert, keine Einzelrollen aufgelistet |
| Weitere Rollen (Steam Verifiziert, Booster, Unterstützer, Lurker) | Live-Rollenliste | `kanaele-und-rollen-karte.html` | neu, Lurker und Verknüpfte Rollen nicht live bestätigt |
| Begrüßung und Einstieg | Bots `assets/welcome_texts.toml` | `rules-und-channels.html`, `onboarding-und-invites.html` | bestehend, unverändert, keine Abweichung zu den Begrüßungstexten festgestellt |
| FAQ-Menü des Bots (15 Optionen) | Bots `assets/faq_texts.toml` | `faq-bot-selbst.html`, `haeufige-probleme.html` | offen: nicht Option für Option abgeglichen |
| Regelwerk | Bots `assets/regelwerk_texts.toml` | `regeln.html` | offen: nicht abgeglichen |
| Paten-Programm | Bots `assets/paten_leitfaden` | `paten.html` | offen: nicht abgeglichen |
| Rang-Guide | Bots `assets/rang_guide_texts.toml` | `workflows/steam-verknuepfen-rang.html` | offen: nicht abgeglichen |
| Steam-Verknüpfung | Steam-Bot README (steam-core, steam-bot) | `steam-integration.html` | bestehend, unverändert |
| Reaction Roles | Bots `dl-community/src/reaction_roles.rs` (generisch) | keine | bewusst nicht dokumentiert: kein Live-Nachweis der Panels |
| LFG-Rang-Tags | keine geprüfte Quelle | keine | offen |
| Team-Bewerbung | Bots `assets/team_application_texts.toml` | `team-und-ansprechpartner.html` | offen: nicht abgeglichen |

## Änderungen

- Neu: `public/discord-server/turniere.html`.
- Neu: `public/discord-server/kanaele-und-rollen-karte.html`.
- Drei Fehler im Entwurf der Karte korrigiert: NSFW-Beschreibung, Coaching-Lane-Bezeichnung und Satz zur Team-Rollenvergabe. Die beiden letzten Punkte beziehen sich auf Abschnitte, die später entfernt wurden.
- Sichtbarkeitsregel (Nutzervorgabe 2026-10-28): Docs nur mit Inhalten, die jedes Mitglied ohne Rolle sehen kann. Karte darauf gekürzt: Coaching-, Scrim-, Streamer-Abschnitte und Einträge für @everyone-verborgene Kanäle entfernt. Vier Kanalnamen waren aus dem Entwurf gestrichen, weil sie @everyone verborgen sind (dev-updates, mitspieler-suche, server-faq, lobby-suche); ihre Sichtbarkeit für Mitglieder mit Rolle ist offen.
- Gate-Runde 1: Satz zu Ranked-Lanes entfernt.
- Gate-Runde 2: Rangliste auf die Live-Guild umgestellt (siehe Tabelle, Zeile „Rang-Rollen"). Alchemist, Arcanist, Archon sind in der Guild nicht vorhanden. Der Bot-Code (`dl-voice/src/rank.rs`, `dl-stats/src/ranks.rs`) ist als Fehlerquelle zu melden, nicht als Maßstab für die Docs. Turnier-Zählung auf das einfache K.-o.-Turnier begrenzt.
- Keine bestehende Seite geändert.

## Prüfungen

- Alle internen Links der beiden neuen Seiten lösen auf.
- `tools/validate_corpus.py`: „Korpus gültig“.
- Keine Mitgliedernamen, Nachrichten oder IDs in den Seiten.
- Keine Admin-Host-Links.

## Offene Punkte

1. Brain-Abdeckung: `community-docs` hat im Status-Summary 0 öffentliche Dokumente und 134 ausgeschlossene. `public-sources.json` hat für `community-docs` keine Prüfnachweise (`reviews {}`). Ohne Prüfnachweise nimmt der Korpus die neuen Seiten nicht auf.
2. Frozen Baseline: `ops/brain-hilfefragen-release.json` friert `community-docs` auf 89c57910. Ein Deploy allein ändert den Brain-Stand nicht, solange die Baseline gilt.
3. Veralteter Live-Link: `/opt/deadlock-docs/current` zeigt auf `releases/brain-hilfefragen-20261002`.
4. Offen wie oben in der Tabelle markiert: FAQ, Regelwerk, Paten, Rang-Guide, Team-Bewerbung, LFG-Rang-Tags.
5. Ranked-Lanes: `module/voice-lanes.html` sagt „grundsätzlich offen“, `dl-voice/src/rank.rs` setzt Rang-Fenster mit `@everyone deny`. Erst ein Live-Check der Kanalrechte entscheidet; bis dahin steht dazu nichts in der Karte.
