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

## Regeln

- **public/ ist öffentlich erreichbar** (FAQ-Bot liefert daraus wörtlich): keine Admin-Pfade, keine Schwellwerte, keine internen URLs/Ports, keine Secrets. Vor jedem Merge nach `public/`: Redaction-Audit.
- **internal/ und public/ mischen nie.** Ein Dokument gehört genau in eine Welt; der Wissens-Dienst baut zwei getrennte Indizes.
- Format: Markdown mit Frontmatter (`title`, `tags`, `stand`, `quelle`). Deutsch, locker-nüchtern, konkret.
- Doku-Änderung gehört zu jeder Code-Änderung dazu (Anti-Drift-Schritt im Standardablauf).

## Konsumenten

- `dl-knowledge`-Dienst (Binary im Deadlock-Bots-Workspace): BM25-Index über public/ (und internal/ nur loopback+Token) → FAQ-Antworten in Discord-Support-Threads (Confidence-Gate: lieber schweigen als raten).
- Später: Website-FAQ, Twitch In-App (P4).
