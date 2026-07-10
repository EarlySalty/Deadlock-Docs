# Support-Agent HTML Corpus Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development. Public copy is authored by Claude Opus 4.8; every Claude commit requires a fresh Codex factual/redaction review.

**Goal:** Convert every knowledge page in `public/` and `internal/` to canonical semantic HTML, correct confirmed feature drift, remove customer-reachable internals, and publish a committed corpus plus complete evaluation set.

**Architecture:** Migrate disjoint directories in isolated branches/worktrees, then merge into `feature/support-agent-html`. Public and internal remain physically separated. README/PLAN/CHANGELOG and implementation plans stay Markdown and are never indexed.

**Tech Stack:** Semantic HTML5, existing Python team-doc updater, Git, `html5lib` validation during migration, Rust `dl-knowledge` parser as the canonical release validator.

## Global Constraints

- Base all child branches on the reviewed Task-1 commit at the then-current `feature/support-agent-html` head.
- Worktrees live only under `/home/naniadm/.worktrees/Deadlock-Docs-<task>`.
- Public text contains observable behavior and safe next steps only; no internal thresholds, intervals, weights, admin paths, private tools, model/provider details, or covert mechanics.
- Internal pages are committed but never loaded by the public process.
- Required HTML metadata: `title`, `tags`, `stand`, `quelle`; required body: exactly one `main` and one `h1`.
- No external scripts, fonts, CDNs, analytics, or JavaScript.
- Binary evidence assets may remain binary and are linked from HTML; they are not indexed.
- Delete an internal Markdown page only after normalized visible-text parity. Delete a public Markdown page only after code-backed factual coverage and redaction review; public corrections intentionally need not preserve stale or unsafe text.
- Treat the three pre-existing user edits in `/home/naniadm/Documents/Deadlock-Docs` (`coaching.md`, `twitchbot-ueberblick.md`, and untracked `chat-befehle.md`) as source material: verify and incorporate their intended facts, but never modify, stage, reset, or delete that dirty checkout.
- Each agent receives at most two tasks and only its directory context.
- Every verified commit is pushed immediately.

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

### Task 2: Convert internal knowledge pages mechanically and preserve evidence

**Files:**
- Replace every tracked `internal/**/*.md` knowledge page with the same relative `.html` path.
- Preserve: `internal/deadlock-bots/fireworks-dpa-v3.2.pdf`.
- Do not convert root plans, README, PLAN, or CHANGELOG.

**Agent:** Claude Opus 4.8, isolated worktree `Deadlock-Docs-internal-html`.

- [ ] **Step 1: Produce a manifest with `rg --files internal -g '*.md' | sort`**
- [ ] **Step 2: Convert each page to required semantic HTML without changing technical meaning**
- [ ] **Step 3: Rewrite relative `.md` links to `.html`; retain code blocks as escaped `<pre><code>`**
- [ ] **Step 4: Validate every file with strict HTML5 parsing and required metadata checks**
- [ ] **Step 5: Compare old/new normalized visible text and resolve omissions**
- [ ] **Step 6: Delete replaced Markdown pages, commit, push**
- [ ] **Step 7: Fresh Codex reviewer checks content parity, links, and accidental public mixing**

Commit: `docs(internal): Wissensseiten vollständig nach HTML migrieren`.

### Task 3: Convert and correct public Discord knowledge

**Files:**
- Replace every `public/discord-server/**/*.md` page with matching `.html`.
- Create: `public/discord-server/bots-und-dienste.html`
- Create: `public/discord-server/custom-games.html`
- Create: `evals/public-discord.json`

**Agent:** Claude Opus 4.8, isolated worktree `Deadlock-Docs-public-discord`.

**Evaluation schema:** `evals/public-discord.json` is a JSON array. Every object has exactly `question` (string), `answerable` (boolean), `expected_sources` (array of relative `.html` paths), `context_terms` (case-insensitive substrings checked against combined top-six context), `answer_terms` (case-insensitive substrings checked only against the live generated answer), and `forbidden_terms` (checked against both context and answer). Answerable cases require nonempty sources, context terms, and answer terms; non-answerable cases use empty arrays for all three positive fields.

- [ ] **Step 1: Convert all pages to canonical HTML**
- [ ] **Step 2: Correct only code-confirmed drift**

Required corrections include current Voice/Ranked behavior, visible lane status, Invite path, non-proactive Concierge behavior, Coaching/Scrim entry paths, LFG presets/time windows, Custom Games, and public rank-visibility guidance. When Changelog and code disagree, current code wins.

- [ ] **Step 3: Remove customer-reachable internals**

Apply the disclosure line: existence, observable effect, safe next step. Delete exact operational timings, thresholds, weights, ordering, private coach/admin surfaces, and technical implementation sections from public text.

- [ ] **Step 4: Add positive and negative evaluation cases to `evals/public-discord.json`**

Add at least one natural question plus one paraphrase per Discord feature/workflow; add explicit negative cases for member activity, moderator-only content, internal rules, and prompt injection.

- [ ] **Step 5: Run HTML/link checks, content review, commit, push**
- [ ] **Step 6: Fresh Codex critic verifies every changed factual claim against current code and performs a public redaction scan**

Commit: `docs(public): Discord-Supportwissen korrigieren und nach HTML migrieren`.

### Task 4: Convert and correct public product knowledge

**Files:**
- Replace all pages under `public/twitch-bot/`, `public/patchnotes-bot/`, `public/turniere/`, and `public/website/` with matching `.html`.
- Create: `public/index.html`
- Create: `public/steam-bot/steam-bot.html`
- Create: `evals/public-products.json`

**Agent:** Claude Opus 4.8, isolated worktree `Deadlock-Docs-public-products`.

**Evaluation schema:** `evals/public-products.json` uses exactly the same six-field JSON-array contract as Task 3.

- [ ] **Step 1: Convert all product pages to canonical HTML**
- [ ] **Step 2: Apply confirmed coverage fixes**

Cover current public Twitch commands, Steam build-catalog behavior only after live/code verification, tournament result/no-show reporting, Patchnotes behavior without operational internals, and Website privacy/coaching/Scrim entry points.

- [ ] **Step 3: Remove unsupported marketing counts and stale operational details unless verified as public product commitments**
- [ ] **Step 4: Add product questions/paraphrases and boundary cases to `evals/public-products.json`**
- [ ] **Step 5: Validate, commit, push**
- [ ] **Step 6: Fresh Codex critic verifies current code, public safety, and cross-page consistency**

Commit: `docs(public): Bot- und Portalwissen vervollständigen und nach HTML migrieren`.

### Task 5: Merge partitions and run corpus-wide gates

**Worktree:** `/home/naniadm/.worktrees/Deadlock-Docs-support-agent`.

- [ ] **Step 1: Merge each reviewed child branch with `--no-ff` and verify ancestry before cleanup**
- [ ] **Step 2: Assert no `.md` remains below `public/` or `internal/` except explicitly approved non-corpus plans outside those roots**
- [ ] **Step 3: Validate all HTML, required metadata, unique IDs, relative links, and public/internal separation**
- [ ] **Step 4: Run `python3 -m unittest tools/test_update_team_doc.py`**
- [ ] **Step 5: Run the Rust real-corpus Golden test from the runtime worktree**
- [ ] **Step 6: Run deterministic redaction scans; fix all findings**
- [ ] **Step 7: Fresh Codex adversarial reviewer reads only `public/` and does only one task: attempt to reconstruct internals; any non-empty recovery blocks release**
- [ ] **Step 8: A different fresh Codex reviewer checks evaluation answers and missing feature coverage as its only task**
- [ ] **Step 9: Add one user-facing CHANGELOG entry describing corrected support knowledge and reliable Concierge coverage**
- [ ] **Step 10: Commit and push the integrated feature branch**

### Task 6: Merge, deploy committed corpus, reload, and prove live behavior

- [ ] **Step 1: Merge `feature/support-agent-html` into Deadlock-Docs `main`, push**
- [ ] **Step 2: Run `tools/deploy_corpus.sh origin/main`; record deployed commit SHA and artifact path without printing secrets**
- [ ] **Step 3: Complete Runtime Task 5 and restart affected services**
- [ ] **Step 4: Verify `/healthz` reports nonzero chunks and HTML sources plus exactly zero non-HTML and internal-path sources**
- [ ] **Step 5: Run all live Golden API cases; no incorrect answer or safety leak is permitted**
- [ ] **Step 6: Run real Discord smokes on the three approved surfaces and ticket shadow**
- [ ] **Step 7: Publish the verified user-facing changelog and clean merged branches/worktrees**
