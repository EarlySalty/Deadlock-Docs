# Deadlock-Docs

Zentrales Wissens-Repo (SSOT) für alle Deadlock-DACH-Projekte. Hier — und nur hier — wird Wissen gepflegt; die Code-Repos verweisen hierher.

## Struktur

```
public/     User-gerichtetes, redigiertes Wissen — Quelle für den FAQ-Bot (öffentlich!)
  <produkt>/  z.B. discord-server/, twitch-bot/, website/, turniere/
internal/   Dev-/Admin-Wissen — Architektur, Runbooks, Cross-System (NIE öffentlich)
  <repo>/     spiegelt die Code-Repos
  betrieb/    Ports, Routing, Deploy-Runbooks, Dienst-Übersicht
```

Wissensseiten sind **kanonisches, semantisches HTML5** (`.html`). Root-Dateien wie
README/PLAN/CHANGELOG bleiben Markdown und werden nie indexiert.

## Regeln

- **public/ ist öffentlich erreichbar** (FAQ-Bot liefert daraus wörtlich): keine Admin-Pfade, keine Schwellwerte, keine internen URLs/Ports, keine Secrets. Vor jedem Merge nach `public/`: Redaction-Audit.
- **internal/ und public/ mischen nie.** Ein Dokument gehört genau in eine Welt; der Wissens-Dienst baut zwei getrennte Indizes. internal/ wird committet, aber vom öffentlichen Prozess **nie** geladen.
- Format: semantisches HTML5. Pflicht-Metadaten pro Seite: `title` (`<title>`), `tags`, `stand`, `quelle` (als `<meta name="…">`); Pflicht-Rumpf: genau ein `<main>` und ein `<h1>`. Keine Skripte, externen Assets, Fonts, CDNs oder JavaScript. Deutsch, locker-nüchtern, konkret.
- Metadaten sind für den Dienst und werden **nie** in Antworten ausgeliefert (`quelle` nennt die Herkunft).
- `tools/validate_corpus.py <root>` erzwingt den Vertrag: Metadaten, genau ein `main`/`h1`, eindeutige IDs, keine Skripte/externen Assets, keine toten relativen Links, keine Markdown-Wissensseiten und keine öffentlichen Referenzen auf `internal/`.
- Doku-Änderung gehört zu jeder Code-Änderung dazu (Anti-Drift-Schritt im Standardablauf).

## Deployment (committed Artefakt)

- `tools/deploy_corpus.sh <git-ref>` exportiert **nur** den committeten `public/`-Baum (`git archive`, nie die Arbeitskopie), legt ihn als SHA-benannten Snapshot unter `$HOME/.local/share/dl-knowledge/` ab, validiert ihn und schaltet danach den `current`-Symlink atomar um. `internal/` landet nie im Laufzeit-Artefakt; ältere Snapshots bleiben erhalten.
- Der Team-Updater (`tools/update_team_doc.py`) schreibt `public/discord-server/team-und-ansprechpartner.html`, committet/pusht, ruft dann `deploy_corpus.sh HEAD` und zuletzt den Reload-Endpoint.

## Konsumenten

- `dl-knowledge`-Dienst (Binary im Deadlock-Bots-Workspace): Index über das deployte `public/`-Artefakt (internal/ nur loopback+Token) → FAQ-Antworten in Discord-Support-Threads (Confidence-Gate: lieber schweigen als raten).
- Website-FAQ und Twitch In-App bleiben künftige Konsumenten (future work).
