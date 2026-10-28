# Docs refresh Twitch a-k (live 8e00a346)

Re-verified at 8e00a346 with audit entries (content_sha256, verified_at, claims, evidence), verified with knowledge_metadata.verified_audit:
- dashboard-hilfe.html
- coaching-was-tun.html
- analytics-dashboard.html
- aktivitaet-und-pausen.html (60-day pause sentence, evidence rust/crates/tb-raid/src/deadlock_pause.rs)
- faq-stats-overlay.html
- berechtigungen.html
- faq-analytics.html (unverified privacy, retention and deletion claims removed)
- quellen/twitch/features.html (editor removal via 410 routes; unverified auto-announcement conditions removed)
- quellen/twitch/chat_network_disabled.html (switch fixed to off in CHAT_SOCIAL_GRAPH_ENABLED)

Not attested (listed, audit entries left as they were):
- twitch-bot/einrichtung.html: "Jetzt Partner werden" button wording and onboarding flow not found at 8e00 or in Website HEAD db8647d.
- twitch-bot/faq-einstieg.html: same reason as einrichtung.
- quellen/website/anfaenger.html: game-mechanic tips (Souls, lanes, parry, items) not checked against the pinned game-brain revision b306fa90 (Deadlock-Brain repo), claim by claim. Not attested.
- quellen/website/beitreten.html and coaching.html: Website ff6ebffd and discord 371a90e8 pins exist; the Discord onboarding and coaching-request flow claims were not checked in this pass.
- quellen/turniere/comp-finder.html and help_tournament_modes.html: Deadlock-Turniere c9fad434 pin not checked in this pass.

Left to the l-z agent: kategorie-markt.html and zusammen-spielen.html (origin/main 31c9cdf is the current version).

History note: the branch history was rebased onto origin/main during the run. One intermediate commit carried conflict markers in the audit JSON; the branch was squashed into one commit before the merge gate.

Remaining steps: gate-review until ALLOW; push origin HEAD:main; sudo -n systemctl start brain-job@deadlock-docs.service; confirm 0 ops.ingest_rejection rows for the new run; ask.sh (analytics, coaching, and the pause question twice; both must say 60 days); delete worktree, local branch docs/twitch-reverify-a-20261028 and remote branch.
