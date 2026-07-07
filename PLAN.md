# Plan: Deadlock-Docs + FAQ-Bot (Stand 2026-07-07)

Ziel: Ein Wissens-SSOT für alles + FAQ-Bot, der Community-Fragen automatisch beantwortet.

## Entscheidungen

- Zielgruppen: öffentlicher Community-FAQ-Bot **und** interner Admin-Wissensmodus, strikt getrennt.
- SSOT per Migration: Wissen zieht hierher um, alte Orte werden Verweise. Auch Dev-Doku (P3).
- Dienst `dl-knowledge`: eigener Prozess, Binary im Deadlock-Bots-Workspace (nutzt `dl-ai`/FireworksClient, DeepSeek v4 Flash).
- Retrieval: BM25/Volltext in-memory, Chunks nach Überschriften. Keine Embeddings in V1.
- Zwei physisch getrennte Indizes (public/internal); Public-Endpoint kennt internal nicht. Internal nur loopback + X-Internal-Token.
- Discord: Auto-Antwort in Support-Foren-Threads **nur** bei Confidence (answerable=true), sonst Schweigen. Shadow-Mode (Log-Kanal-Review) vor Live.
- Anti-Drift: Pflichtschritt im Standardablauf + Hook-Erinnerung + Doku-Pfad in Worker-Aufträgen (P3).

## Phasen

- **P1 (läuft):** Repo + User-Wissen migrieren. Quellen: Deadlock-Bots/docs (User-Dateien, werden verschoben), docs/support-kb (30 HTML → Markdown, verschoben), Deadlock-Twitch-Bot/rust/knowledge/bot (kopiert — tb-knowledge konsumiert die Originale live, Umschalten P4). Redaction-Audit über public/.
- **P2:** dl-knowledge-Dienst + Public-API (`POST /ask` → `{answerable, answer, sources}`) + Discord-Shadow-Mode → Live.
- **P3:** Dev-Doku aller Repos → internal/, Internal-Index + Admin-Endpoint, Anti-Drift-Hook + CLAUDE.md-Regel.
- **P4:** Website-FAQ + Twitch In-App vom selben Endpoint; tb-knowledge auf Deadlock-Docs umstellen; Originale löschen.
