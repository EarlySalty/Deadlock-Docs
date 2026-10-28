# docs-twitch2: Twitch-bot docs refresh (2026-10-28)

Scope: `public/twitch-bot/` and `internal/deadlock-twitch-bot/` in Deadlock-Docs.
Code reference: `~/repos/Deadlock-Twitch-Bot` origin/main `d1b234cc` (read-only).
Live checks: Caddyfile routes and HTTP status codes, plus the code paths listed per row.

## Audit: page → wrong or missing facts → fix

| Page | Wrong or missing (before) | Fix (this change) |
|---|---|---|
| chat-befehle.html | `!discord` listed as a trigger. The catalog has no `!discord`; the triggers are `!dldc`/`!dlde`/`!invite`. Missing: `!trustpilot`/`!bewerten`, `!clipcontest`, `!vodclip`, `!raid <name>`, custom command names (`command_names.rs`, max 5 extra names). | Removed `!discord`; added the missing commands with their group rules; new section "Eigene Befehlsnamen". |
| faq-community.html | `!discord` as invite trigger. | `!invite` / `!dldc`. |
| faq-support.html | `!discord` as invite trigger. | `!invite` / `!dldc`. |
| auto-raid.html | Raid scope (language, home server) not described. | New section "Welche Kanäle kommen als Ziel infrage?" (rule from `raid_scope_allows`, `partner_roster.rs`). |
| faq-raids.html | "Den Zielkanal wählst du nicht selbst" is wrong for `!raid <name>` (commit 69ebacb23). `!raid_status` wording kept (code has no role gate). | Documents `!raid <name>`; manual vs. automatic target rules separated. |
| faq-stats-overlay.html | Stats require "über den Discord verknüpften Steam-Account"; `!connect` also links Steam without Discord (`player_links.rs`). | Both link paths named. |
| twitchbot-ueberblick.html | Onboarding path `/streamer/onboarding/` (live: 308 to `/twitch/onboarding`). Feature list lacked overlays, social media, VOD, language. | Path → `/twitch/onboarding`; list extended. |
| twitch-streamer-dashboard.html | No dashboard language info; no dono goal, caster overlays, Social Media Manager, VOD range downloads, Uplink language. | New sections: "Sprache des Dashboards", "Spendenziel und Caster-Overlays", "Social Media Manager", "VOD-Ausschnitte herunterladen". |
| uplink-*.html, faq-* (others) | Uplink help language not stated. | Stated in the dashboard language section (Uplink help and VOD links follow dashboard language, commit 5fdafff4d). Uplink pages stay German. |

Checked, no change needed: berechtigungen, discord-golive, faq-einstieg, faq-funktionen, faq-plaene (no `/twitch/abbo` link left), faq-affiliate, faq-analytics, faq-werbung, uplink-stoerungen, vertrauen-seriositaet, einrichtung, ueber-den-bot (auto-raid-off wording still true: no switch exists), analytics-dashboard.

## Facts verified in code

- `!sub erinnerung an|aus|status` matches `sub_reminder.rs`.
- `!vodclip`: Mod group; numbers are minutes; range 1 to 10 minutes; file max 64 MiB; download retention 24 h (`vod_range.rs`, `commands.rs` `cmd_vodclip`).
- `!raid <name>`: target must be live; Deadlock eligibility and global bans still apply; offline target gets a chat reply; scope rule not documented as applying (see open items).
- Raid scope for automatic selection: shared guild OR same language group AND home guild enabled; target needs at least one enabled guild; partner must be active (`guild_membership.rs` `raid_scope_allows`, `partner_roster.rs`).
- Dashboard language: stored choice, else `dead-lock.de` → English, else browser language (any `de*` → German, otherwise English). Switch is under Verwaltung > Konto (commit 04a5d0336).

## Open items (not documented, or documented as limit)

1. Paten program: Discord feature, `public/discord-server/` belongs to another agent. Not touched.
2. Multi-server onboarding and Hub (768d324fb): runtime activation disabled per commit message. Not documented as a live feature.
3. Dashboard language default: commit b69500f14 says "German default", but `dictionary.ts` falls back to English for non-German browsers on first visit. Docs follow the code. Product decision needed if German default was intended.
4. Scope rule for `!raid <name>`: `start_targeted_raid` (`auto_raid.rs`) applies no scope rule; the page says so.
5. TikTok uploads may wait for TikTok approval (`waiting_tiktok_approval`); documented in the Social Media section.
6. `internal/deadlock-twitch-bot/`: not reviewed in this pass; open item.

## Gate round 1 (fa94cce, BLOCK, 11 findings) and fixes

| Finding | Fix |
|---|---|
| `!raid <name>` said the target must pass the Deadlock check | Deadlock check applies to the caller's own stream (`start_manual_raid`, `classify_eligibility`); the target only needs to be live and not the caller (`start_targeted_raid`). Fixed in chat-befehle and faq-raids. |
| auto-raid: "mindestens einen aktiven Server" and "Hauptserver aktiv" as rules | Removed. Shared server needs no switch; same language needs the cross-server release on both sides (`raid_scope_allows`, `partner_roster.rs`). The release is set per server by the community team (`admin_guild_raids.rs`, admin UI), not by streamers. |
| faq-stats-overlay: "beides" works with `!connect` | The overlay resolves the streamer via Discord only (`overlay.rs` `resolve_discord_id`); `!connect` feeds chat stats only. Meta, body, setup and troubleshooting fixed. |
| Overlay meta description contained `<code>` | Plain text now. |
| twitch-streamer-dashboard: 64 MB and "nur für dich" | Limit is 64 MiB, shown as "etwa 67 MB"; the download is for the channel owner, created by owner or mod. |
| auto-raid: "Den Zielkanal wählst du nicht selbst" without scope | Limited to the automatic raid, points to `!raid <name>`. |
| faq-raids: list indentation | Fixed. |
| Review report bound to old content | Hashes refreshed for all changed pages; new entries for chat-moderation, faq-support, faq-stats-overlay, twitch-streamer-dashboard, twitchbot-ueberblick, pause-loop-obs. |

## Public-rule pass (no internals in public/)

Rule: public pages describe what a feature does and how members or streamers use it, never the selection, scoring, weights, thresholds, ordering, cooldowns, tie-breaks or detection logic. Removed from touched pages: partner and server threshold wording in auto-raid; no numbers for the pause-loop pool, clip limits or concurrency (kept in the internal doc only). Scam-guard thresholds and providers are not in public/ (only the three user-chosen actions and the switch).

## Features added for public/ (were only in internal/ or repo docs)

| Feature | Source | Public page |
|---|---|---|
| OBS-Pause-Loop (browser source /twitch/pause-loop) | internal/pause-loop-obs.html, pause_loop.rs | new `public/twitch-bot/pause-loop-obs.html`, linked from twitchbot-ueberblick |
| Scam-Schutz (Auto-Bann, Auto-Timeout, Nur melden, switch, !explain, !unban) | internal/scam-guard.html, ScamGuardSection.tsx | section "Scam-Schutz im Chat" in chat-moderation.html |
| Bot vom Kanal trennen (moderator removal, partner end, auto-raid off, nothing deleted, re-auth restores) | internal/bot-trennen.html, streamers.rs | section "bot-trennen" in twitch-streamer-dashboard.html |

Not made public (internal or staff only): crew-guard-radar (staff alert channel), stream-coaching-audit (internal coaching service for own team), smalltalk-shadow (no sending, internal test mode), knowledge-faq, architektur, betrieb, datenmodell, integrationen, uebersicht, affiliate (public faq-affiliate exists), verwaltung-selbstbedienung (internal toggle API).

## Gate round 2 (BLOCK, 8 findings) and fixes

| Finding | Cause | Fix |
|---|---|---|
| `<code>` left in faq-stats-overlay meta description | instance (round-1 fix recorded but not applied) | Plain `!connect` in the meta description. |
| Audit `code` paths did not cover the page claims (chat-befehle, chat-moderation, auto-raid, faq-raids, faq-community, faq-stats-overlay, twitch-streamer-dashboard, twitchbot-ueberblick) | spec (no rule that every claim needs its code paths) | Paths extended with the code that backs each claim (commands, catalog, player_links, rank_lookup, moderation, channel_policy, eligibility, GuildRaidsSection, DonoGoal, caster overlay, Social Media Manager, disconnect, onboarding route). |
| "Der Befehl funktioniert nur, wenn du selbst gerade Deadlock streamst" | spec (after-stream DB fallback in `auto_raid.rs` manual path not in the page) | Wording now covers the last Deadlock stream and the short window after it, without numbers. |
| "gelten nur der automatischen Auswahl" | instance (German dative) | "gelten nur für die automatische Auswahl". |
| Live release `4bfc09af` does not contain the d1b234cc changes in the listed paths (raid scope `guild_membership.rs`, Scam-Schutz, VOD range, overlay, pause loop, bot-trennen, catalog) and `live_code_note` said "ohne Diff" | spec (importer checks only against origin/main, never against the live release) | Each of the 10 affected audits now carries a gap until the release containing d1b234cc is live; `live_code_note` corrected. These pages are withheld from the Brain until then. |
| Stand dates 2026-09-20 on edited pages | instance | Set to 2026-10-28 on all touched pages. |
| Hashes not recomputed | process | Recomputed for the 10 touched pages. |
| "bis zu fünf weitere Namen je Befehl" disputed | false | Disproved: `MAX_EXTRA_NAMES = 5` in `command_names.rs` at d1b234cc (the reviewer checked another checkout, 730c8e1). Claim kept. |
| README stale (chat-moderation listed as unchanged, open item 4) | instance | Updated. |

Unit tests: 195 run, 1 failure in `test_update_team_doc` (team doc, discord-server). The same test fails on origin/main, so it is pre-existing. `validate_corpus.py` passes.

## Open items after round 2

- Release gap: the twitch bot release `4bfc09af` is behind d1b234cc. Until a release with d1b234cc is live, the 10 twitch-bot audits stay pending and the Brain will not serve their new content. Deploying is not part of this docs change.
- `pause-loop-obs` is only verifiable live once the release contains `pause_loop.rs` changes.
- Paten program (discord-server scope) not touched.
- Hub multi-server not documented as live.
- Dashboard language default conflict: commit b69500f14 says German default, `dictionary.ts` falls back to English for non-German browsers; docs follow code. Product decision.
- Cross-server opt-in is set per server by the community team (`GuildRaidsSection.tsx`), not by streamers.
- `internal/deadlock-twitch-bot/` not reviewed in this pass.
- Brain path for subdirectory pages to confirm after the brain-job run.
- Pre-existing en dashes in untouched public lines (chat-befehle, twitchbot-ueberblick, twitch-streamer-dashboard).
