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

Checked, no change needed: chat-moderation, berechtigungen, discord-golive, faq-einstieg, faq-funktionen, faq-plaene (no `/twitch/abbo` link left), faq-affiliate, faq-analytics, faq-werbung, uplink-stoerungen, vertrauen-seriositaet, einrichtung, ueber-den-bot (auto-raid-off wording still true: no switch exists), analytics-dashboard.

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
4. Scope rule for `!raid <name>`: not verified whether it applies to manual named raids. Page says it does not.
5. TikTok uploads may wait for TikTok approval (`waiting_tiktok_approval`); documented in the Social Media section.
6. `internal/deadlock-twitch-bot/`: not reviewed in this pass; open item.
