---
title: "Styleguide für alle Doku in diesem Repo"
tags: [meta, styleguide]
stand: 2026-07-07
quelle: "Deadlock-Docs"
---
# Styleguide — verbindlich für jede Datei hier

## Sprache & Zeichen

- Deutsch. Echte Umlaute und Eszett als UTF-8: ä ö ü Ä Ö Ü ß. **Niemals** ae/oe/ue-Ersatz, niemals HTML-Entities (`&auml;`), niemals Unicode-Escapes (`ä`).
- Gerade ASCII-Anführungszeichen ("...") statt typografischer („..."). Bindestrich statt Gedankenstrich-Exoten ist okay; kein Zeichensalat.
- Nach dem Schreiben Pflicht-Check: `grep -rn 'Ã\|&auml\|\\u00' <dateien>` muss leer sein.

## Ton — Dev-Doku, nicht AI-Prosa

So schreibt hier ein Entwickler für den nächsten Entwickler:

- Kurze Sätze. Aktiv. Konkret. "Der Bot pollt alle 35 s das Forum" statt "Es findet eine regelmäßige Überprüfung statt".
- **Verboten:** "In diesem Dokument...", "Zusammenfassend lässt sich sagen", "Es ist wichtig zu beachten", "robust", "nahtlos", "leistungsstark", Emojis, Marketing, Füll-Adjektive.
- Keine Bullet-Explosion: Bullets nur für echte Aufzählungen. Zusammenhänge als Fließtext, 2-4 Sätze pro Absatz.
- Mechanismus statt Behauptung: nicht "das System ist sicher", sondern "der Endpoint bindet nur 127.0.0.1".
- Zahlen, Pfade, Namen exakt — oder gar nicht.

## Wahrheit

- Jede Aussage muss aus Code/Config/Schema belegbar sein. Referenz in Klammern dazu: (`rust/bin/dl-bot/src/main.rs`).
- **Rust ist die Wahrheit.** Alle Dienste außer dem Patchnotes-Bot laufen auf Rust; Python ist Legacy in Ablösung. Doku beschreibt den Rust-Pfad als DEN Pfad — nicht "es gibt zwei Backends". Python-Code höchstens ein kurzer Absatz am Ende ("Legacy: der alte Python-Pfad unter `backend/` ist abgelöst"), keine Python-Mechanik-Details, keine Py/Rust-Vergleiche pro Absatz.
- Laufzeit-Wahrheit bei systemd: immer die **komplette** Unit inkl. Overrides lesen (`systemctl --user cat <svc>`), nicht nur die erste `ExecStart`-Zeile — Overrides ersetzen ExecStart weiter unten.
- Bestehende alte Doku ist Verdachtsmaterial, nicht Quelle: gegen den Code prüfen, Veraltetes weglassen und im Bericht melden.
- Unsicher? Weglassen oder Zeile mit `UNSICHER:` prefixen — niemals raten.
- HTTP-Status-Codes: Handler **und** Error-Mapping prüfen (`error.rs`/`IntoResponse`), nie aus Funktionsnamen oder Kommentaren raten.
- "Die DB ist X": vorher alle Pfad-Resolver greppen (`*_DB`, `DB_PATH`, `connect`, DSN-Env) — Rust und Legacy können divergieren.
- Keine Meta-Dateien (`bericht.md`, Dateilisten, Alt-Doku-Funde) im Doku-Baum; Bericht gehört in die Worker-Antwort, nicht ins Repo.
- Secrets: nur Env-Var-/Secret-Namen nennen, niemals Werte. Keine Tokens, keine DSNs mit Credentials.

## Form

- Frontmatter wie überall hier: `title`, `tags`, `stand` (Datum), `quelle` (Repo/Pfad-Bezug).
- `title` immer spezifisch: "Turniere — Betrieb", nie generisch "Betrieb" (landet im Suchindex und in Quellenangaben).
- Nach der H1: 2-3 Zeilen Kurzfassung, was dieses Dokument beantwortet. Dann erst Details.
- Zwischenüberschriften (`##`) alle 3-5 Absätze — keine Prosa-Wand über 15 Absätze.
- Aufzählungen ab ~5 gleichartigen Einträgen (Env-Vars, Tabellen, Endpunkte) als Markdown-Tabelle, nicht als Fließtext-Kette.
- Code-Referenzen: eine Klammer pro Absatz-Ende mit max. 3 Pfaden — nicht nach jedem Satz.
- Dateinamen: kebab-case, deutsch (`datenmodell.md`, `betrieb.md`).
- `internal/` darf Technik enthalten (Ports, Tabellen, Pfade). `public/` niemals — dort gilt zusätzlich: keine internen Zahlen, keine Endpunkte, keine Admin-Wege (siehe README).
