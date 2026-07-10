# Plan: Deadlock-Docs + FAQ-Bot (Stand 2026-07-07)

Ziel: Ein Wissens-SSOT für alles + FAQ-Bot, der Community-Fragen automatisch beantwortet.

## Entscheidungen

- Zielgruppen: öffentlicher Community-FAQ-Bot **und** interner Admin-Wissensmodus, strikt getrennt.
- SSOT per Migration: Wissen zieht hierher um, alte Orte werden Verweise. Auch Dev-Doku (P3).
- Dienst `dl-knowledge`: eigener Prozess, Binary im Deadlock-Bots-Workspace (nutzt `dl-ai`/FireworksClient, DeepSeek v4 Flash).
- Retrieval: BM25/Volltext in-memory, Chunks nach Überschriften. Keine Embeddings in V1.
- Format: kanonisches, semantisches HTML5 (Pflicht-Metadaten `title`/`tags`/`stand`/`quelle`, genau ein `main`/`h1`, keine Skripte/externen Assets). Root-Docs (README/PLAN/CHANGELOG) bleiben Markdown und werden nie indexiert.
- Deployment: committed public-only Artefakt. `tools/deploy_corpus.sh <ref>` exportiert nur den committeten `public/`-Baum (`git archive`), validiert ihn mit `tools/validate_corpus.py` und schaltet `current` atomar um; internal/ landet nie im Laufzeit-Artefakt.
- Zwei physisch getrennte Indizes (public/internal); Public-Endpoint kennt internal nicht. Internal nur loopback + X-Internal-Token.
- Discord: Auto-Antwort in Support-Foren-Threads **nur** bei Confidence (answerable=true), sonst Schweigen. Shadow-Mode (Log-Kanal-Review) vor Live.
- Anti-Drift: Pflichtschritt im Standardablauf + Hook-Erinnerung + Doku-Pfad in Worker-Aufträgen (P3).

## Ausgeschlossene Repos

TradingBot, Deadlock-Brain und AI-Assistant/AI-Coach sind rein interne Projekte: **keine Doku in diesem Repo, weder public noch internal.** Erwähnungen sichtbarer Discord-Features (z. B. `!brain`-Befehl in der Server-Doku) sind davon unberührt.

## Phasen

- **P1 (läuft):** Repo + User-Wissen migrieren. Quellen: Deadlock-Bots/docs (User-Dateien), docs/support-kb (30 HTML → Markdown, Original gelöscht — kein Konsument), Deadlock-Twitch-Bot/rust/knowledge/bot (kopiert). Redaction-Audit über public/ (LEAK-Funde → „Für Devs"-Sektionen nach internal/ abgespalten).
  **Wichtig:** dl-bot lädt `Deadlock-Bots/docs/*.md` zur Laufzeit als FAQ-Grounding (`load_docs`), tb-knowledge lädt `rust/knowledge/`. Beide Originale bleiben bis zur Umstellung; bis dahin Änderungen zuerst hier, dann spiegeln.
- **P2:** dl-knowledge-Dienst + Public-API (`POST /ask` → `{answerable, answer, sources}`) + Discord-Shadow-Mode → Live. Grounding auf das deployte public-Artefakt (`dl-knowledge/current`) umstellen und die gespiegelten Markdown-Originale in Deadlock-Bots/docs löschen.
- **P3:** Dev-Doku aller Repos → internal/, Internal-Index + Admin-Endpoint, Anti-Drift-Hook + CLAUDE.md-Regel.
- **P4 (future work):** Website-FAQ + Twitch In-App vom selben Endpoint; tb-knowledge auf das deployte Artefakt umstellen; Originale löschen.
