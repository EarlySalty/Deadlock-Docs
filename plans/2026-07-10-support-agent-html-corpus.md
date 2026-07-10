# Support-Agent HTML Corpus Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development. Public copy is authored by Claude Opus 4.8; every Claude commit requires a fresh Codex factual/redaction review.

**Goal:** Convert every knowledge page in `public/` and `internal/` to canonical semantic HTML, correct confirmed feature drift, remove customer-reachable internals, and publish a committed corpus plus complete evaluation set.

**Architecture:** Migrate disjoint file sets in isolated branches/worktrees, then merge into `feature/support-agent-html`. Public and internal remain physically separated. Public work is split into Discord-Kern, Discord-Tools, Twitch, Steam+Website, Patchnotes+Turniere and a final Cross-Product-Integration; no Content-Agent owns more than two closely related themes/products. README/PLAN/CHANGELOG and implementation plans stay Markdown and are never indexed.

**Tech Stack:** Semantic HTML5, existing Python team-doc updater, Git, `html5lib` validation during migration, Rust `dl-knowledge` parser as the canonical release validator.

## Global Constraints

- Base all child branches on the reviewed Task-1 commit at the then-current `feature/support-agent-html` head.
- Worktrees live only under `/home/naniadm/.worktrees/Deadlock-Docs-<task>`.
- Public text contains observable behavior and safe next steps only; no internal thresholds, intervals, weights, admin paths, private tools, model/provider details, or covert mechanics.
- `plans/2026-07-10-support-agent-coverage-matrix.md` is the mandatory 84-row coverage and answerability contract. Every row is checked against HTML plus exactly one owning evaluation package.
- Internal pages are committed but never loaded by the public process.
- Required HTML metadata: `title`, `tags`, `stand`, `quelle`; required body: exactly one `main` and one `h1`.
- No external scripts, fonts, CDNs, analytics, or JavaScript.
- No public Content-Agent starts before Task 1A is green and reviewed. Its raw-file gate scans complete `public/**/*.html`, including `head`, metadata, links, comments and attributes, in raw form plus `html.unescape` + NFKC normalization; a clean `<main>` alone is insufficient.
- The machine gate blocks only high-signal categories: Discord snowflakes, internal/host/code paths, private or loopback URLs, secret material and secret environment names, and concrete provider/prompt/retrieval/Shadow control terms. Findings expose only file, line and category, never the matched value. `meta[name="quelle"]` contains safe product/live text, never a file path or host.
- Internal thresholds, intervals, formulas and private Admin-/Coach mechanics remain forbidden but are not broad regex blockers because visible member limits, dates, Owner/Mod/Coach contact and appeals may be legitimate. Every package and final gate therefore requires a human semantic redaction review; any reconstructable internal fact blocks merge.
- Binary evidence assets may remain binary and are linked from HTML; they are not indexed.
- Delete an internal Markdown page only after normalized visible-text parity. Delete a public Markdown page only after code-backed factual coverage and redaction review; public corrections intentionally need not preserve stale or unsafe text.
- Treat the three pre-existing user edits in `/home/naniadm/Documents/Deadlock-Docs` (`coaching.md`, `twitchbot-ueberblick.md`, and untracked `chat-befehle.md`) as source material: verify and incorporate their intended facts, but never modify, stage, reset, or delete that dirty checkout.
- Do not mechanically convert public control material: `public/discord-server/support/agent-guide.md` and `public/discord-server/sicherheit/redaktions-hinweise.md` are removed from the public corpus after any still-valid internal guidance is moved to `internal/`; `public/discord-server/referenz/status-und-fehler.md` is fully re-authored as curated member-visible symptoms and safe next steps. None of their raw text may enter a public `<main>`.
- Public aggregate activity and a member's own logged-in activity/statistics/privacy controls are positive support knowledge. Other people's private details plus private/moderative data remain negative.
- Dynamic questions about service status, prices, dates, the newest patch, the currently best hero/build, tickets and legitimate support questions containing injection are answerable routing/boundary cases. They name a visible current-information or human-support path without inventing live data. Pure injection, requests for private internals/data and requested actions may be non-answerable.
- LFG pages describe only currently visible options. They never expose internal time windows, cooldowns or matching intervals.
- DM-Concierge, structured LFG, automatic moderation and Go-Live are documented conditionally when visible/active, always with a stable alternative member path.
- No live-status feature, auto-debug, command execution or ticket live reply is added by this plan.
- Each agent receives at most two tasks and only its directory context.
- Every verified commit is pushed immediately.

---

## Execution DAG and release definition

```text
Task 1 (tooling baseline) -> Task 1A (raw-HTML redaction gate)
Task 1 -------------------> Task 2 (internal migration; separate)
Task 1A ------------------> Tasks 3A,3B,4-6 (five isolated public packages, parallel)
Tasks 3A,3B,4-6 ----------> Task 7 (cross-product integration and broad routing)
Tasks 1A,2,3A,3B,4-7 + Runtime Task 4 -> Task 8 (corpus-wide gates)
Task 8 -------------------> Task 9 (merge/deploy/reload, coordinated with Runtime Task 5)
```

Every content package is done only when its matrix rows are checked, its own six-field Eval JSON is schema-valid, HTML/link validation and the normalized full-file raw gate pass, code/live-dependent claims have evidence, the semantic reviewer has ruled out reconstructable thresholds/intervals/formulas/private Admin-/Coach mechanics, and a fresh Codex factual/redaction critic has no Critical or Important finding. Task 8 is done only when all 84 rows and at least 168 cases are present, all six Eval files pass the Rust harness, and both independent final critics approve.

---

### Task 1: Repository contract, committed corpus deployment, and updater

**Agent:** GPT-5.5 xhigh in the isolated support-agent worktree. A fresh Claude Opus 4.8 reviewer performs a code-correctness and security review of the Python/Bash tooling before integration; a self-review or factual copy review is not sufficient.

**Files:**
- Modify: `README.md`
- Modify: `PLAN.md`
- Modify: `tools/update_team_doc.py`
- Modify: `tools/test_update_team_doc.py`
- Create: `tools/deploy_corpus.sh`
- Create: `tools/test_deploy_corpus.py`
- Create: `tools/validate_corpus.py`
- Create: `tools/test_validate_corpus.py`

**Interfaces:**
- `tools/deploy_corpus.sh <git-ref>` exports only the committed `public/` tree into a versioned directory below `$HOME/.local/share/dl-knowledge/` and atomically updates `current`; `internal/` is never copied into the runtime artifact.
- Team updater writes `public/discord-server/team-und-ansprechpartner.html`, commits/pushes it, deploys the committed corpus, then calls the existing reload endpoint.
- `tools/validate_corpus.py <root>` rejects missing metadata/main/h1, duplicate IDs, scripts or external assets, broken relative links, Markdown knowledge pages, and public references to `internal/`.

- [ ] **Step 1: Change updater tests to expect semantic HTML**

Assert required meta fields, one `main`, one `h1`, escaped Discord display names, and unchanged detection that ignores only the `stand` value.

- [ ] **Step 2: Add failing deployment and validator contract tests**

Use temporary Git repositories. Prove that deployment reads the requested commit rather than a dirty worktree, never exports `internal/`, retains an older snapshot, updates `current` to the requested SHA, and refuses a commit without public HTML. Prove that the validator accepts one minimal canonical page and rejects each contract violation listed above.

- [ ] **Step 3: Run red**

Run:

```bash
python3 -m unittest tools/test_update_team_doc.py
python3 -m unittest tools/test_deploy_corpus.py tools/test_validate_corpus.py
```

Expected: the existing Markdown renderer fails HTML assertions and both new test modules fail because their implementations do not exist.

- [ ] **Step 4: Render the canonical HTML shape**

The updater output must follow:

```html
<!doctype html>
<html lang="de"><head>
  <meta charset="utf-8">
  <title>Team und Ansprechpartner</title>
  <meta name="tags" content="discord-server, team, support">
  <meta name="stand" content="YYYY-MM-DD">
  <meta name="quelle" content="Discord-Rollenabfrage">
</head><body><main>
  <h1>Team und Ansprechpartner</h1>
  <section id="ansprechpartner"><h2>Ansprechpartner</h2>...</section>
</main></body></html>
```

Use `html.escape` for all Discord-derived text. Do not add a new Python dependency.

- [ ] **Step 5: Add committed-artifact deployment and corpus validation**

`deploy_corpus.sh` must use `git archive <ref> public`, extract into a new SHA-named directory, run the corpus validator, then atomically replace only the `current` symlink. It must never copy the working tree, copy `internal/`, or delete older snapshots. The validator uses only Python's standard library.

- [ ] **Step 6: Wire updater and update README/PLAN**

After its commit and push succeed, the updater must invoke the deploy script with `HEAD`, then call the existing reload endpoint; tests mock those boundaries and assert this order. Document HTML as canonical, public-only indexing, committed-artifact deployment, current phases, and that Twitch/Website consumers remain future work. Remove obsolete Markdown-mirror instructions after cutover.

- [ ] **Step 7: Test, commit, push, and request fresh Opus correctness/security review**

Run all three unittest modules. The full repository cannot satisfy the HTML-only validator before Tasks 2–4; run `tools/validate_corpus.py .` against the real repository from Task 5 onward.

Commit: `feat(docs): HTML-Korpusvertrag und committed Deploy einführen`.

### Task 1A: Blockierendes Roh-HTML-Redaction-Gate

**Dependency:** Start after Task 1. Merge and review this task before Tasks 3A, 3B and 4–6 begin. Task 2 may proceed separately because `internal/` is never public-indexed.

**Files:**
- Modify: `tools/validate_corpus.py`
- Modify: `tools/test_validate_corpus.py`

**Interfaces:**
- `tools/validate_corpus.py <root>` reads every complete raw file below `public/`, not only parsed visible text, and checks both original UTF-8 text and `unicodedata.normalize("NFKC", html.unescape(source))`.
- The gate checks `head`, metadata values, URLs, comments and every attribute as well as `main`, and reports only relative file, line and stable finding class without echoing sensitive source text.

- [ ] **Step 1: Add failing safe-`<main>` fixtures with high-signal values in `head`, meta, comments, `href` and `data-*`: Snowflake (plain and entity-encoded), internal/repository/absolute path, loopback/private/einteiliger Service-Host, synthetic secret/token/credential Env name, concrete provider, system-prompt/injection, retrieval term and Ticket-Shadow**
- [ ] **Step 2: Add passing fixtures for `quelle="Produktdokumentation und geprüftes Live-Verhalten"`, public FQDN/Invite/mail/relative links, safe OAuth/password help, provider-free „KI-gestützte Antwort“, visible `6 gegen 6`, public duration and Owner/Moderation/Coach appeal/contact**
- [ ] **Step 3: Run `python3 -m unittest tools/test_validate_corpus.py` and observe the new cases fail**
- [ ] **Step 4: Implement only the high-signal patterns and normalized view in the existing standard-library validator; do not add broad number/Admin/Coach regexes, a second validator or dependency**
- [ ] **Step 5: Run all three tooling test modules and `git diff --check`**
- [ ] **Step 6: Commit, push and obtain a fresh Opus correctness/security review covering false positives, normalization bypasses and non-disclosing findings; fix every Critical/Important finding before public branches are cut**

Commit: `fix(docs): öffentliche HTML-Rohdaten vor Interna schützen`.

### Task 2: Convert internal knowledge pages mechanically and preserve evidence

**Files:**
- Replace every tracked `internal/**/*.md` knowledge page with the same relative `.html` path.
- Preserve: `internal/deadlock-bots/fireworks-dpa-v3.2.pdf`.
- Read as migration input only: `public/discord-server/support/agent-guide.md`, `public/discord-server/sicherheit/redaktions-hinweise.md`; write any still-current internal-only guidance into the appropriate `internal/deadlock-bots/*.html` page, never back into `public/`.
- Do not convert root plans, README, PLAN, or CHANGELOG.

**Agent:** Claude Opus 4.8, isolated worktree `Deadlock-Docs-internal-html`.

- [ ] **Step 1: Produce a manifest with `rg --files internal -g '*.md' | sort`**
- [ ] **Step 2: Convert each page to required semantic HTML without changing technical meaning; verify and absorb only still-current internal guidance from the two named public control files**
- [ ] **Step 3: Rewrite relative `.md` links to `.html`; retain code blocks as escaped `<pre><code>`**
- [ ] **Step 4: Validate every file with strict HTML5 parsing and required metadata checks**
- [ ] **Step 5: Compare old/new normalized visible text and resolve omissions**
- [ ] **Step 6: Delete replaced Markdown pages, commit, push**
- [ ] **Step 7: Fresh Codex reviewer checks content parity, links, and accidental public mixing**

Commit: `docs(internal): Wissensseiten vollständig nach HTML migrieren`.

## Shared public evaluation interface

Each Task 3A–7 Eval file is one JSON array. The exact package names are `public-discord-core.json`, `public-discord-tools.json`, `public-twitch.json`, `public-steam-website.json`, `public-patchnotes-turniere.json` and `public-integration.json`. Every object has exactly `question` (string), `answerable` (boolean), `expected_sources` (array of relative `.html` paths), `context_terms` (case-insensitive substrings checked against combined top-six context), `answer_terms` (case-insensitive substrings checked only against the live generated answer), and `forbidden_terms` (checked against context and answer). Answerable cases require nonempty sources, context terms and answer terms. Non-answerable cases use empty arrays for all three positive fields. The answerability assignments in the coverage matrix are binding.

### Task 3A: Discord server core, accounts and support

**Dependency:** Task 1A is merged and reviewed.

**Files (exclusive ownership):**
- Convert exactly these Markdown sources to same-path `.html`:

```text
public/discord-server/deadlock-grundlagen.md
public/discord-server/dm-concierge.md
public/discord-server/faq-bot-selbst.md
public/discord-server/haeufige-probleme.md
public/discord-server/module/changelog-ankuendigungen.md
public/discord-server/module/dashboard-login.md
public/discord-server/module/faq-support.md
public/discord-server/module/moderation.md
public/discord-server/module/onboarding.md
public/discord-server/module/serverstruktur.md
public/discord-server/module/statistiken-privatsphaere.md
public/discord-server/module/steam-twitch-verknuepfung.md
public/discord-server/negativ-wissen.md
public/discord-server/onboarding-und-invites.md
public/discord-server/referenz/glossar.md
public/discord-server/regeln.md
public/discord-server/rules-und-channels.md
public/discord-server/stats-und-privacy.md
public/discord-server/steam-integration.md
public/discord-server/support/troubleshooting.md
public/discord-server/team-und-ansprechpartner.md
public/discord-server/ueber-bot-und-server.md
public/discord-server/workflows/austritt-datenloeschung.md
public/discord-server/workflows/moderationsfall-einspruch.md
public/discord-server/workflows/onboarding-beitritt.md
public/discord-server/workflows/rang-sichtbarkeit.md
public/discord-server/workflows/steam-verknuepfen-rang.md
public/discord-server/workflows/streamer-partner-werden.md
```

- Completely rewrite `public/discord-server/referenz/status-und-fehler.md` to same-path `.html` as curated member help.
- Delete without HTML mirror: `public/discord-server/support/agent-guide.md`, `public/discord-server/sicherheit/redaktions-hinweise.md`.
- Create: `evals/public-discord-core.json`.
- Never edit Task 3B files or `public/discord-server/bots-und-dienste.html`.

**Agent:** Claude Opus 4.8, isolated worktree `Deadlock-Docs-public-discord-core`; exactly two themes: server core/support and member account/privacy/integrations.

**Coverage:** C02–C08, C18–C20 and C22–C25.

- [ ] **Step 1: Verify the exclusive file manifest; classify the two control pages for deletion and the status dump for complete member rewrite, with no raw control/status text entering public HTML**
- [ ] **Step 2: Author current server/rules/team, Concierge/FAQ/onboarding/Invite, Steam/Twitch linkage, aggregate-versus-own activity/privacy and safe support flows from code/live evidence**
- [ ] **Step 3: Keep aggregate and own logged-in routes positive; make DM, moderation and other configured surfaces conditional with stable alternatives**
- [ ] **Step 4: Add a natural question and paraphrase for every owned matrix row to `evals/public-discord-core.json`; ticket C25 is answerable member-routing knowledge**
- [ ] **Step 5: Run schema/HTML/link validation, normalized raw gate and semantic redaction review, then commit and push**
- [ ] **Step 6: Obtain a fresh Codex factual/redaction review with zero Critical/Important findings**

Commit: `docs(public): Discord-Kernwissen migrieren`.

### Task 3B: Discord group tools and gameplay help

**Dependency:** Task 1A is merged and reviewed. Runs in parallel with Task 3A and owns no common file.

**Files (exclusive ownership):**
- Convert exactly these Markdown sources to same-path `.html`:

```text
public/discord-server/coaching.md
public/discord-server/community-tools.md
public/discord-server/module/brain.md
public/discord-server/module/coaching.md
public/discord-server/module/mitspielersuche-lfg.md
public/discord-server/module/tierlist-builds.md
public/discord-server/module/voice-lanes.md
public/discord-server/scrims.md
public/discord-server/tempvoice-guide.md
public/discord-server/tierlist-und-builds.md
public/discord-server/voice-features.md
public/discord-server/workflows/builds-abstimmen.md
public/discord-server/workflows/coaching-anfragen.md
public/discord-server/workflows/mitspieler-finden.md
public/discord-server/workflows/voice-lane-erstellen-verwalten.md
```

- Create: `public/discord-server/custom-games.html`.
- Create: `evals/public-discord-tools.json`.
- Never edit Task 3A files or `public/discord-server/bots-und-dienste.html`.

**Agent:** Claude Opus 4.8, isolated worktree `Deadlock-Docs-public-discord-tools`; exactly two themes: group/match organization and gameplay/build help.

**Coverage:** C09–C17 and C21.

- [ ] **Step 1: Verify the exclusive file manifest and current Voice/Ranked, LFG, Brain, Coaching, Scrim, Custom Games and Tierlist/Build behavior against code/live evidence**
- [ ] **Step 2: Author visible Owner/Lane and group flows without live lane-status claims or internal selection/matching mechanics**
- [ ] **Step 3: Describe only visible LFG options, never internal time windows/cooldowns; structured LFG remains conditional with the classic member fallback**
- [ ] **Step 4: Add a natural question and paraphrase for every owned matrix row to `evals/public-discord-tools.json`**
- [ ] **Step 5: Run schema/HTML/link validation, normalized raw gate and semantic redaction review, then commit and push**
- [ ] **Step 6: Obtain a fresh Codex factual/redaction review with zero Critical/Important findings**

Commit: `docs(public): Discord-Gruppenwerkzeuge migrieren`.

### Task 4: Convert and correct Twitch knowledge

**Dependency:** Task 1A is merged and reviewed.

**Files:**
- Replace all knowledge pages under `public/twitch-bot/` with canonical `.html` counterparts.
- Create: `evals/public-twitch.json`

**Agent:** Claude Opus 4.8, isolated worktree `Deadlock-Docs-public-twitch`; one product only.

**Coverage:** T02–T15. T01 broad routing belongs to Task 7.

- [ ] **Step 1: Verify each existing page against current Twitch-Bot code and the visible product; remove an unsupported page instead of preserving stale claims**
- [ ] **Step 2: Author current OAuth/revocation, complete viewer and role-gated command catalog, category/Steam prerequisites, dashboard/analytics/overlay, raids, moderation/appeal, engagement controls, plans, affiliate and support/legal boundaries**
- [ ] **Step 3: Treat Go-Live, moderation and other configured surfaces conditionally and name a stable visible fallback; publish no fixed price, quota, retention, frequency or reach**
- [ ] **Step 4: Add a natural question and paraphrase for T02–T15 to `evals/public-twitch.json`; dynamic current-price questions route to the visible billing surface and remain answerable**
- [ ] **Step 5: Run schema/HTML/link validation plus the full raw-file gate, commit and push**
- [ ] **Step 6: Obtain a fresh Codex factual/redaction review against current code with zero Critical/Important findings**

Commit: `docs(public): Twitch-Supportwissen verifizieren und migrieren`.

### Task 5: Convert Steam and Website knowledge

**Dependency:** Task 1A is merged and reviewed.

**Files:**
- Create: `public/steam-bot/steam-bot.html`
- Replace all knowledge pages under `public/website/` with canonical `.html` counterparts.
- Create: `evals/public-steam-website.json`
- Do not create or edit: `public/index.html` (owned by Task 7).

**Agent:** Claude Opus 4.8, isolated worktree `Deadlock-Docs-public-steam-website`; two tightly related product surfaces.

**Coverage:** S02–S07 and W02–W07. S01/W01 broad routing belongs to Task 7.

- [ ] **Step 1: Verify Steam account/panel, primary/unlink/whoami, rank, Invite, build-catalog and privacy boundaries against current code**
- [ ] **Step 2: Verify Website coaching, Scrim member path, builds/catalog boundary, patch archive, aggregate-versus-own activity/privacy and tournament-portal paths**
- [ ] **Step 3: Author only observable member behavior; do not expose private Coach/Admin areas, fixed marketing counts or non-visible sort effects**
- [ ] **Step 4: Add natural questions and paraphrases for S02–S07 and W02–W07 to `evals/public-steam-website.json`**
- [ ] **Step 5: Run schema/HTML/link validation plus the full raw-file gate, commit and push**
- [ ] **Step 6: Obtain a fresh Codex factual/redaction review against both current products with zero Critical/Important findings**

Commit: `docs(public): Steam- und Website-Supportwissen migrieren`.

### Task 6: Convert Patchnotes and tournament knowledge

**Dependency:** Task 1A is merged and reviewed.

**Files:**
- Replace all knowledge pages under `public/patchnotes-bot/` and `public/turniere/` with canonical `.html` counterparts.
- Create: `evals/public-patchnotes-turniere.json`

**Agent:** Claude Opus 4.8, isolated worktree `Deadlock-Docs-public-patchnotes-turniere`; two related announcement/event products.

**Coverage:** P02–P06 and R02–R10. P01/R01 broad routing belongs to Task 7.

- [ ] **Step 1: Verify Patchnotes sources/output/archive/delay behavior and remove public retranslation/operator commands**
- [ ] **Step 2: Verify tournament consent, team/recruitment, check-in, format/bracket/draft, own result, no-show human confirmation, profile visibility and DM/privacy paths before authoring them**
- [ ] **Step 3: Keep current patch and next tournament answerable by routing to the visible current portal/announcement source; never freeze a date or patch as current**
- [ ] **Step 4: Add natural questions and paraphrases for P02–P06 and R02–R10 to `evals/public-patchnotes-turniere.json`**
- [ ] **Step 5: Run schema/HTML/link validation plus the full raw-file gate, commit and push**
- [ ] **Step 6: Obtain a fresh Codex factual/redaction review against both current products with zero Critical/Important findings**

Commit: `docs(public): Patchnotes- und Turnierwissen migrieren`.

### Task 7: Cross-product integration, indexes and broad routing

**Dependencies:** Start only after reviewed Tasks 3A, 3B and 4–6 are merged into `feature/support-agent-html`. This task does not repair Fachseiten opportunistically; a missing fact goes back to its owning package.

**Files:**
- Create: `public/index.html`
- Create: `public/discord-server/bots-und-dienste.html`
- Create: `evals/public-integration.json`

**Agent:** Fresh Claude Opus 4.8, isolated worktree `Deadlock-Docs-public-integration`; only aggregation/routing, no product deep-dive.

**Coverage:** C01, S01, T01, P01, R01, W01 and B01–B14.

- [ ] **Step 1: Build the two concise indexes from reviewed Fachseiten so broad Server/Bot questions route to all six product groups without copying product internals**
- [ ] **Step 2: Add natural questions and paraphrases for all six broad routing rows and all B rows to `evals/public-integration.json`**
- [ ] **Step 3: Serialize B01/B02/B03/B05/B06/B14 as non-answerable; serialize current status, price, date, patch, best hero/build, ticket, changing names and legitimate question+injection as answerable source-backed boundaries**
- [ ] **Step 4: Ensure ticket text promises only visible human support and never names Shadow/Log processing; injection cannot alter source choice or trigger an action**
- [ ] **Step 5: Run all six Eval schema checks, cross-file duplicate-question check, HTML/link validation and the normalized full-file raw gate, then commit and push**
- [ ] **Step 6: Obtain a fresh Codex cross-product coverage/redaction review with zero Critical/Important findings**

Commit: `docs(public): Supportwissen produktübergreifend routen`.

### Task 8: Merge partitions and run corpus-wide gates

**Dependencies:** Tasks 1A, 2, 3A, 3B and 4–7 are reviewed; Runtime Task 4 can now consume all six Eval files.

**Worktree:** `/home/naniadm/.worktrees/Deadlock-Docs-support-agent`.

- [ ] **Step 1: Merge every reviewed child branch with `--no-ff`; verify ancestry before any branch/worktree cleanup**
- [ ] **Step 2: Assert no `.md` remains below `public/` or `internal/`; confirm the prohibited public control pages have no HTML mirror and the status dump was curated rather than copied**
- [ ] **Step 3: Run all tooling unittests and validate structure, links, unique IDs, public/internal separation and the complete raw bytes of every public HTML file**
- [ ] **Step 4: Check all 84 matrix rows and at least 168 unique questions across the six exact six-field Eval files**
- [ ] **Step 5: Run Runtime Task 4's real-corpus retrieval Golden test; fix source content in the owning package, never by weakening assertions**
- [ ] **Step 6: Have a fresh Codex adversarial reviewer read only raw `public/` and attempt to recover IDs, hosts/paths, prompts/models, operator mechanics, thresholds/intervals/formulas or private data; any recovery blocks release**
- [ ] **Step 7: Have a different fresh Codex reviewer audit matrix-to-HTML-to-Eval coverage, dynamic/ticket/injection answerability and all six broad product routes**
- [ ] **Step 8: Add one user-facing CHANGELOG entry, run `git diff --check`, commit and push the integrated feature branch**

### Task 9: Merge, deploy committed corpus, reload, and prove live behavior

**Dependency:** Task 8 and Runtime Task 4 are green and reviewed. Coordinate with Runtime Task 5; this task adds no live-status or auto-debug feature.

- [ ] **Step 1: Merge `feature/support-agent-html` into Deadlock-Docs `main`, push**
- [ ] **Step 2: Run `tools/deploy_corpus.sh origin/main`; record deployed commit SHA and artifact path without printing secrets**
- [ ] **Step 3: Complete Runtime Task 5 and restart affected services**
- [ ] **Step 4: Verify `/healthz` reports nonzero chunks and HTML sources plus exactly zero non-HTML and internal-path sources**
- [ ] **Step 5: Run every live Golden API case from all six files; no incorrect answer or safety leak is permitted**
- [ ] **Step 6: Run real Discord smokes on DM, private FAQ chat and server questions; verify ticket output remains Shadow-only without exposing that mechanism to members**
- [ ] **Step 7: Publish the verified user-facing changelog and clean merged branches/worktrees**
