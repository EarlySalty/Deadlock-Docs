# Docs refresh: Twitch-Bot raids, go-live, streamer role, ads, monitoring (2026-10-28)

Scope: public/twitch-bot/ pages for auto-raid, raid network, Discord go-live, streamer role, Werbemanager and ads, stream monitoring visible to streamers. Outreach checked.

## Feature inventory

| Feature | Visible where | Documented before | Action |
|---|---|---|---|
| Auto-Raid at stream end | Chat hint, Dashboard Startseite (`Auto-Raid: Aktiv`), `!raid_status`, `!raid_history` | yes, but target rules spelled out (wrong depth) | fixed: rewritten in auto-raid.html |
| Target selection rules (same server, same language, Community-Freigabe) | not user-facing as a rule set | wrong depth (public explained selection) | removed from auto-raid.html and faq-raids.html |
| Auto-Raid separate off switch | no toggle found in dashboard_v2 (only status text) | wrong ("vorgesehen, noch nicht verfügbar") | fixed: states no separate switch, disconnect as the only way |
| Manual `!raid <name>` (mod/broadcaster, live target) | Chat command | yes, but claimed selection-based | fixed in faq-raids.html and auto-raid.html |
| `!raid` / `!traid` bot-chosen target | Chat command | yes | kept, selection rule removed |
| `!raid` availability rule (Deadlock or just switched from Deadlock) | Chat reply text | not documented | removed again: unverified wording dropped from faq-raids.html |
| `!raid_status` / `!raid_history` open to all | Chat commands | yes | kept, verified in tb-chat commands.rs |
| Flip protection (short flip holds raid, repeated flips pause auto-raids for hours) | Chat hint from tb-bot flip_unraid.rs | not documented | added to auto-raid.html, behaviour only, no constants |
| Raid pre-lead ad protection (target channel spared own ads right before a raid) | Effect in Werbemanager | not documented | not documented on the page (only commit and module doc, not verified live) |
| Discord go-live post while live in Deadlock category | Community-Discord | yes, but no runtime, no flap guard | updated discord-golive.html |
| Offline embed with stream duration (omitted when unknown) | Community-Discord | not documented | added to discord-golive.html |
| Reannounce guard after offline (no double post on brief drop) | Community-Discord | not documented | added to discord-golive.html |
| Separate live role while Deadlock live | Discord role | not documented | added briefly to discord-golive.html |
| Streamer role on Discord (valid auth, not banned, not paused) | Discord role | not documented | new page aktivitaet-und-pausen.html, no thresholds |
| Deadlock-Pause (mod rights dropped after long Deadlock absence, partnership stays, auto return) | Chat/DM text, Dashboard | not documented | new page aktivitaet-und-pausen.html |
| Silent raid notes (`Raid-Hinweise stummschalten`) | Dashboard Verwaltung, Bot & Schutz | not documented | left to auto-raid settings; not added (cross-area chat notes page) |
| Werbemanager (Twitch ad planning, tab `Werbung (Experimentell)`) | Dashboard Verwaltung | not documented (faq-werbung covered bot promo only) | new page werbemanager.html |
| Werbemanager strategies, Matchschutz, Steam status requirement, Chat-Hinweis, history, snooze 5 min | Dashboard tab | not documented | werbemanager.html (snooze and ad-protection detail removed, not verified live) |
| Bot promo Werbefrei (Bot-Werbung) | Plan page | yes | kept, linked to werbemanager.html |
| Stream monitoring (go-live, offline, EventSub) | Discord posts | partly | covered via discord-golive.html |
| Courtesy / raid etiquette reminders | Not visible to streamers in a documented UI | not documented | not documented, open item (visibility unverified) |
| Outreach shadow agent (tb-engagement) | Not streamer-visible (shadow review) | not documented | not documented, correct by omission |

Counts: 22 rows. Already correct: 2 (`!raid_status`/`!raid_history`, bot promo Werbefrei). Corrected: 6 (auto-raid, selection rule, off switch, `!raid <name>`, `!raid` target wording, go-live base). Newly documented: 9. Not documented on purpose: 4 (silent raid notes, courtesy reminders, outreach, stream monitoring beyond go-live).

## Cross-area pages (not edited, report to orchestrator)

- chat-befehle.html: repeats the target selection rule for `!raid`.
- twitchbot-ueberblick.html: auto-raid summary is fine, no change needed.
- faq-einstieg.html, faq-funktionen.html, faq-community.html, faq-plaene.html: check for auto-raid and go-live claims.
- twitch-streamer-dashboard.html: claims "Bot vom Kanal trennen" removes streamer role and partnership; consistent with aktivitaet-und-pausen.html. Go-live section fine.
- discord-server/twitch-chat-hilfe.html and discord-server/kanaele-und-rollen-karte.html: may describe the Streamer role and go-live channel differently.

## Open items

- Werbemanager live state: repo doc docs/streamer/WERBEMANAGER.md (2026-09-24) says not yet productive, while main shows the tab as experimental. The page says experimental and does not claim productive delivery.
- Raid pre-lead protection: described from commit 0861dc9fc and module doc of raid_vorlauf.rs; not verified live.
- Courtesy reminders: not checked for streamer-visible UI; left out.
- Live curl of public pages not run (no change to behaviour claims).
