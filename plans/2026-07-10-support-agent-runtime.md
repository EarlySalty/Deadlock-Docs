# Support-Agent Runtime Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development to implement this plan task-by-task. Every task is TDD-first and requires a fresh Claude-Opus-4.8 cross-review before integration.

**Goal:** Make `dl-knowledge` consume the canonical HTML corpus safely, route every supported Discord surface through one grounded answer path, log every decision, and prove behavior with real-question evaluations.

**Architecture:** Keep the existing BM25 + LLM design. Add a strict semantic-HTML parser, a shared `dl-community` knowledge client with typed outcomes, and a deterministic evaluation contract. During migration the loader accepts Markdown only when no public HTML exists; after the corpus cutover it becomes HTML-only.

**Tech Stack:** Rust 1.85, Axum, Tokio, `scraper` 0.27.0, existing `dl-ai`, `dl-community`, tracing, serde JSON.

## Global Constraints

- Work only in `/home/naniadm/.worktrees/Deadlock-Bots-support-agent` on `feature/support-agent-runtime`, based on current `origin/main`.
- Preserve foreign changes in `/home/naniadm/Documents/Deadlock-Bots`.
- TDD: failing test, observed red, minimal implementation, green, refactor.
- The production process receives exactly `$HOME/.local/share/dl-knowledge/current/public`; the deployed snapshot contains no `internal/` tree and no prompt-based filtering substitutes for that boundary.
- No embeddings, vector DB, live-status tooling, auto-debug, ticket live replies, or new user actions.
- `plans/2026-07-10-support-agent-coverage-matrix.md` is the mandatory 84-row content/evaluation contract; Runtime Golden tests consume its six package Eval files without changing the six-field schema.
- Public Content Tasks do not start until the Docs raw-HTML gate scans complete files, including `head`, metadata, links, comments and attributes, in raw form plus `html.unescape` + NFKC normalization. Runtime retrieval checks do not replace this gate.
- The machine gate blocks high-signal Snowflakes, internal/host/code paths, private/loopback URLs, secret material/Env names and concrete LLM-/infrastructure-provider, prompt, retrieval and Shadow terms; visible product names such as Discord, Steam, Twitch and Valve remain allowed. Findings never echo matched values. Semantic thresholds/intervals/formulas and private Admin-/Coach mechanics are separate human merge blockers, not broad regex blockers.
- Public aggregate activity and the member's own authenticated activity/statistics/privacy routes are answerable; another person's private details and private/moderative data are not.
- Dynamic status, price, date, newest-patch and best-hero/build questions, ticket questions and legitimate support questions containing injection remain answerable routing/boundary cases. They use public sources and never claim live knowledge. Pure injection, requests for private data/internals and requested actions may be non-answerable.
- Config-dependent DM-Concierge, structured LFG, moderation and Go-Live guidance is conditional and retains a stable public fallback. No LFG internal time windows are exposed.
- Every decision logs truncated input, verdict, confidence label, retrieval score, reason, sources, and error class.
- No plaintext secrets, internal endpoints, or model prompts in public responses.
- Each verified commit is pushed immediately and reviewed by a fresh Opus 4.8 critic.
- Commit trailer: `Co-authored-by: GPT-5.5 <gpt-5.5@local>` for GPT workers, or the actual model identity used.

---

## Execution DAG and definition of done

```text
Runtime Task 1 -> Runtime Task 2 -> Runtime Task 3
Docs Task 1A -> Docs Tasks 3A,3B,4-6 -> Docs Task 7
Runtime Tasks 1-3 + Docs Tasks 3A,3B,4-7 -> Runtime Task 4
Docs Task 8 + Runtime Task 4 -> Docs Task 9 / Runtime Task 5 coordinated cutover
```

Task 4 is done only when it discovers and validates every `*.json` directly below `DL_GOLDEN_DIR`, all 84 matrix rows produce at least 168 unique questions across the six package files, and the retrieval gate passes without weakening source/content assertions. Task 5 is done only after the committed corpus, all Golden cases and all approved Discord surfaces pass live while ticket delivery remains Shadow-only.

---

### Task 1: Semantic HTML corpus parser with migration compatibility

**Files:**
- Modify: `rust/Cargo.toml`
- Modify: `rust/bin/dl-knowledge/Cargo.toml`
- Modify: `rust/bin/dl-knowledge/src/main.rs`
- Test: `rust/bin/dl-knowledge/src/main.rs` (`#[cfg(test)]` module)

**Interfaces:**
- Consumes: `DL_DOCS_PATH` pointing at one public corpus root.
- Produces: `fn load_corpus(root: &Path) -> Result<KnowledgeBase>` that prefers `.html`; Markdown is used only when the root contains no HTML during migration.
- Produces: `fn parse_html_file(root: &Path, path: &Path, raw: &str) -> Result<Vec<Chunk>>`.
- Produces health counters for distinct HTML sources, non-HTML sources, and internal-path sources so the live boundary is provable without exposing source names.

- [ ] **Step 1: Add failing HTML contract tests**

Add tests that use this exact fixture shape:

```rust
const HTML_FIXTURE: &str = r#"<!doctype html>
<html lang="de"><head>
<meta charset="utf-8"><title>Steam-Bot</title>
<meta name="tags" content="steam, rang">
<meta name="stand" content="2026-07-10">
<meta name="quelle" content="Steam-Bot-Code">
</head><body><main>
<h1>Steam-Bot</h1><p>Öffentliche Zusammenfassung.</p>
<section id="verknuepfen"><h2>Steam verknüpfen</h2><p>Nutze das öffentliche Panel.</p></section>
</main></body></html>"#;
```

Assert: title/tags/path are parsed; only `<main>` text appears; `quelle` never appears in chunk text; section IDs/headings create stable chunks; missing `main`, `title`, `tags`, `stand`, or `quelle` returns `Err`; `<script>` inside `main` returns `Err`; a nested `internal/` directory is ignored. Add a reload regression test proving a malformed replacement corpus returns an error while the previously loaded index and health counters remain unchanged.

- [ ] **Step 2: Run the focused test and observe red**

Run: `cargo test -p dl-knowledge parse_html -- --nocapture`

Expected: compile failure because `parse_html_file` does not exist.

- [ ] **Step 3: Add the parser dependency**

Add once in workspace dependencies:

```toml
scraper = { version = "0.27.0", default-features = false }
```

Add `scraper.workspace = true` to `bin/dl-knowledge`.

- [ ] **Step 4: Implement the minimum HTML parser**

Use `scraper::Html` and `scraper::Selector`. Require exactly one `main`, one document title, and all three metadata fields. Create one intro chunk from direct `main > h1` / `main > p` content and one chunk per direct `main > section`; use the first `h2` or section `id` as section name. Normalize whitespace but preserve Discord mentions and link text.

- [ ] **Step 5: Prefer HTML atomically during migration**

Replace `collect_markdown_files` with a format-neutral collector. If any `.html` exists below the passed public root, collect only `.html`; otherwise collect only `.md`. Never index both formats in one process.

- [ ] **Step 6: Verify focused and package tests**

Run:

```bash
cargo fmt --all -- --check
cargo test -p dl-knowledge
cargo clippy -p dl-knowledge --all-targets -- -D warnings
```

Expected: all green.

- [ ] **Step 7: Commit, push, and request Opus cross-review**

Commit: `feat(knowledge): semantischen HTML-Korpus laden`

Reviewer input: base SHA, head SHA, Task 1 contract, focused test output. Fix Critical/Important findings and re-run the commands before proceeding.

### Task 2: Typed knowledge-client outcomes and complete decision logging

**Files:**
- Create: `rust/crates/dl-community/src/knowledge_client.rs`
- Modify: `rust/crates/dl-community/src/lib.rs`
- Modify: `rust/crates/dl-community/src/faq.rs`
- Modify: `rust/crates/dl-community/src/concierge.rs`
- Modify: `rust/bin/dl-knowledge/src/main.rs`
- Test: the same Rust modules

**Interfaces:**
- Produces: `pub(crate) enum KnowledgeLookup { Answer(KnowledgeAnswer), Unanswerable, Timeout, Transport, InvalidResponse }`.
- Produces: `pub(crate) async fn ask(base_url: &str, question: &str, timeout: Duration) -> KnowledgeLookup`.
- Consumers: FAQ and Concierge; both stop owning duplicate HTTP clients/types.

- [ ] **Step 1: Write failing client-classification tests**

Cover HTTP success/answerable, HTTP success/unanswerable, delayed response, non-success status, and invalid JSON. Assert the exact `KnowledgeLookup` variant.

- [ ] **Step 2: Run red**

Run: `cargo test -p dl-community knowledge_client -- --nocapture`

Expected: module/type missing.

- [ ] **Step 3: Implement the shared client and replace both duplicates**

Keep the existing request/response JSON contract. Do not retry a user question inside this client. Return typed outcomes instead of `Option`.

- [ ] **Step 4: Add one decision logger in `dl-knowledge`**

Every return path from `/public/v1/ask` must call one helper with these fields:

```text
question=<max 240 chars> verdict=yes|no|uncertain|timeout|error
confidence=source_grounded|none retrieval_score=<top BM25 score or absent>
reason=character_count|no_retrieval|generator_missing|model_empty|model_invalid_json|model_rejected|answered
sources=<deduplicated relative paths> error_class=<optional stable class>
```

Do not log raw prompts or full model output.

- [ ] **Step 5: Add tests for every decision reason**

Use the existing mock generator and tracing test capture. At minimum assert one `yes`, one `no`, one `uncertain`, and one `error` record with truncated input.

- [ ] **Step 6: Verify and commit**

Run:

```bash
cargo fmt --all -- --check
cargo test -p dl-knowledge
cargo test -p dl-community faq
cargo test -p dl-community concierge
cargo clippy -p dl-knowledge -p dl-community --all-targets -- -D warnings
```

Commit: `fix(support): Wissensentscheidungen vollständig sichtbar machen`

Push and request fresh Opus review.

### Task 3: Route all approved Discord surfaces through the same grounded path

**Files:**
- Modify: `rust/crates/dl-community/src/concierge.rs`
- Modify: `rust/crates/dl-community/src/faq.rs`
- Test: both modules

**Interfaces:**
- Consumes: `knowledge_client::ask` from Task 2.
- Produces: direct grounded responses in DM, active private FAQ session, and `SERVER_BOT_FRAGEN_CHANNEL_ID` in the main guild.
- Preserves: ticket responses target only configured shadow channel.

- [ ] **Step 1: Write the failing public-channel routing test**

Construct `ConciergeConfig` with the main guild. Call `handle_user_message(SERVER_BOT_FRAGEN_CHANNEL_ID, Some(main_guild_id), user_id, question)`. Assert it reaches the knowledge mock and sends exactly one reply. Assert another ordinary guild channel remains unhandled.

- [ ] **Step 2: Write the failing ticket-shadow invariant test**

For both answerable and unanswerable outcomes, assert no message is posted into the ticket channel or directly to its user while shadow mode is configured. An answerable result goes only to the shadow target. An unanswerable result logs `no` or `uncertain` and posts its safe human-escalation text only to the shadow target.

- [ ] **Step 3: Run red**

Run:

```bash
cargo test -p dl-community faq -- --nocapture
cargo test -p dl-community concierge -- --nocapture
```

Expected: the public-channel test fails under the current fallback-owner gate.

- [ ] **Step 4: Implement the single routing guard**

Allow the designated questions channel only when `guild_id == main_guild_id`; keep the existing owner check for private fallback channels. Do not open Concierge handling globally across guild channels.

- [ ] **Step 5: Verify and commit**

Run focused tests, then `cargo test -p dl-community` and clippy. Commit: `fix(concierge): Serverfragen über denselben Wissenspfad beantworten`. Push and request Opus review.

### Task 4: Real-question Golden evaluation contract

**Files:**
- Modify: `rust/bin/dl-knowledge/src/main.rs`
- Consume at test time: every `*.json` directly below the directory passed through `DL_GOLDEN_DIR`

**Interfaces:**
- Produces test-only `#[serde(deny_unknown_fields)] GoldenCase { question: String, answerable: bool, expected_sources: Vec<String>, context_terms: Vec<String>, answer_terms: Vec<String>, forbidden_terms: Vec<String> }`.
- Reads paths from `DL_DOCS_PATH` and `DL_GOLDEN_DIR`; never hardcodes a developer checkout.
- Produces ignored `golden_live_api`, enabled with `DL_GOLDEN_API_URL`, which sends the same cases to the running `/public/v1/ask` endpoint and validates answerability, returned sources, every case-insensitive `answer_terms` substring, and forbidden answer terms.

**Dependency:** Start this task only after Corpus Tasks 3A, 3B and 4–7 are reviewed and progressively merged into `feature/support-agent-html`, so all six evaluation files and their HTML sources exist. `/home/naniadm/.worktrees/Deadlock-Docs-support-agent` is the already-existing checkout of exactly that integrated branch and is updated through Task 7 before this test starts. It must not assume old monolithic `public-products.json` or `public-discord.json` input.

- [ ] **Step 1: Add a failing ignored real-corpus test for every package file**

Each evaluation file is a JSON array of objects with exactly the six fields above. Discover every `*.json` directly below `DL_GOLDEN_DIR`; require `public-discord-core.json`, `public-discord-tools.json`, `public-twitch.json`, `public-steam-website.json`, `public-patchnotes-turniere.json` and `public-integration.json`, and reject duplicate question text across files. `expected_sources` contains relative `.html` paths. The retrieval test loads the HTML corpus and every JSON case, runs BM25, and asserts that every positive case retrieves at least one expected source within the top six. The combined top-six context contains every case-insensitive `context_terms` substring and no `forbidden_terms` entry. The live test checks `answer_terms` only against the generated answer. Negative cases never expose an internal path or forbidden term. Reject unknown or missing fields, missing/empty package files, answerable cases without expected sources/context terms/answer terms, and non-answerable cases with any positive field.

Add explicit contract fixtures: B01/B02/B03/B05/B06/B14-shaped pure private/internals/action/injection cases are allowed to be non-answerable; service status, current price/date/patch/best hero, ticket and legitimate question+injection cases must be answerable with a public routing source. This validates routing behavior only and must not add a live-status lookup, debug action or ticket reply.

- [ ] **Step 2: Run red against the migrated corpus path**

Before running, verify that `/home/naniadm/.worktrees/Deadlock-Docs-support-agent` is on `feature/support-agent-html`, contains the reviewed Task-7 commit and has all six required Eval files. The environment variables below select this prepared checkout; the runtime task does not create or populate it.

Run:

```bash
DL_DOCS_PATH=/home/naniadm/.worktrees/Deadlock-Docs-support-agent/public \
DL_GOLDEN_DIR=/home/naniadm/.worktrees/Deadlock-Docs-support-agent/evals \
cargo test -p dl-knowledge golden_public_corpus -- --ignored --nocapture
```

Expected: FAIL until the corpus and cases are present/correct.

- [ ] **Step 3: Implement only the retrieval and live-API test harnesses**

Do not add retrieval heuristics merely to satisfy one phrase. First fix source titles/tags/content in the corpus. Add query expansion only when at least two natural paraphrases share the same confirmed gap.

- [ ] **Step 4: Verify and commit**

The retrieval Golden test must pass against the feature corpus before this commit. The live-API test must compile here and pass in Task 5 after the feature service is running; both are release gates. Commit: `test(knowledge): reale Supportfragen als Release-Gate`. Push and request Opus review.

### Task 5: HTML-only cutover, build, deploy, and live proof

**Files:**
- Modify: `rust/bin/dl-knowledge/src/main.rs` (remove Markdown parser and fallback after corpus merge)
- Modify: `scripts/run_dl_knowledge_service.sh` (point default exactly to `$HOME/.local/share/dl-knowledge/current/public`)
- Modify: `CHANGELOG.md`

**Dependencies:** Corpus Tasks 1A–8 and Runtime Task 4 are green/reviewed, the Corpus plan is merged to Deadlock-Docs `main`, and committed artifact deployment succeeded.

- [ ] **Step 1: Change the parser test to reject `.md` corpus files**
- [ ] **Step 2: Remove Markdown collection/frontmatter code and make `.html` mandatory**
- [ ] **Step 3: Run fmt, all workspace tests, workspace clippy, and release build**
- [ ] **Step 4: Cross-review final Rust diff with a fresh Opus critic**
- [ ] **Step 5: Merge to `main`, push, build `cargo build --release --workspace`, restart `dl-knowledge.service` and `deadlock-bot-rust.service`**
- [ ] **Step 6: Prove both services with PID change, `/proc/<pid>/exe`, and empty recent `error|panic|fatal` journal scan; `/healthz` must report positive HTML-source count and zero non-HTML/internal-path sources**
- [ ] **Step 7: Run live API Golden smoke and Discord smokes in DM, private FAQ chat, and server questions channel; verify ticket answer appears only in shadow**
- [ ] **Step 8: Post the user-facing changelog only after all live checks pass**
