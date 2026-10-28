# Docs refresh: Twitch bot chat area (2026-10-28)

Scope: public/twitch-bot chat pages (moderation, chat commands, clip commands, automatic chat notices, FAQ funktionen and community). Source of truth: origin/main of Deadlock-Twitch-Bot (d1b234cc3 at start).

## Inventory

| Feature | Visible where | Documented before | Action |
|---|---|---|---|
| Four moderation toggles (Bekannte Betrüger, Abzock-Warnung, Werbe-Spam, Discord-Einladungen bremsen) | Verwaltung > Was der Bot übernimmt | no | added to chat-moderation, faq-funktionen |
| Scam-Schutz for first-time writers, modes Auto-Bann / Auto-Timeout / Nur melden | Verwaltung > Scam-Schutz | wrong ("prüft Chat-Verläufe") | corrected |
| Crew and impersonation alerts (notify only) | Discord mod channel | no | added to chat-moderation |
| !uban / !unban, !explain, !silentban | chat | yes | kept |
| !clip / !createclip, 10 s channel cooldown, offline reply, duration 5-60 s | chat, Verwaltung | yes | kept |
| !vodclip permissions, 1-10 min range, 64 MiB file, 24 h download | chat, Verwaltung | partly wrong ("drei pro Stunde", "15 Minuten", live/offline source unverified) | corrected in clip-befehle, unverified claims removed |
| !clipcontest (partner, own clip, 3 per Berlin day) | chat, Dashboard | no | added to clip-befehle; chat-befehle already correct |
| Community-Hinweise im Chat, default on, off from Netzwerk Plus | Verwaltung > Community-Hinweise im Chat | no | new chat-hinweise page, faq-community question |
| Twitch re-authorization reminder once per go-live | chat | no | new chat-hinweise page, faq-funktionen question |
| KI-Engagement on/off, auto-off at stream end, ignore_me | chat | yes | linked from chat-hinweise |
| Follow hint, greeting, sub reminder | Verwaltung, chat | yes (chat-befehle) | linked |
| Stat command switches (8) | Verwaltung | yes (chat-befehle, first agent) | confirmed, no change |
| LFG pitch, invite access question, streamer voice | chat | no | NOT documented, open item (behaviour and trigger wording not verified) |
| Smalltalk (non-partner outreach experiment) | chat, non-partner channels | no | NOT documented, open item for user decision |

Counts: 16 features in scope (LFG, invite question and streamer voice counted separately). Already correct: 5 (!uban/!explain/!silentban, !clip, stat switches, KI-engagement, follow hint/greeting/sub reminder). Corrected: 2 (Scam-Schutz wording, !vodclip claims). Newly documented: 5 (moderation toggles, crew alerts, !clipcontest, community hints, re-auth reminder; new page chat-hinweise.html). Not documented yet: 4 (LFG, invite question, streamer voice, smalltalk).

## Open items

- LFG pitch, invite access question and streamer voice: need code-level verification of trigger wording and public behaviour before documenting.
- Smalltalk: user decides whether non-partner outreach may be documented publicly.
- Chat reply language German: reply constants checked for clip, vodclip and clipcontest; not checked for every reply path.

## Gate status (not merged)

- Nothing merged to main. No brain-job run, no Brain test questions asked.
- gate-review: round 1 BLOCK (missing publication audits, hash mismatches, crew text); crew text fixed; round 2 BLOCK, only publication audit remains.
- Blocker: audits must verify claims against live behaviour. Live Twitch release 4bfc09af lacks d1b234cc (Scam-Schutz, VOD range, clip contest). Audits not self-attested.
- Affected pages without audit or with changed hash: chat-hinweise.html, clip-befehle.html, chat-moderation.html, chat-befehle.html, faq-community.html, faq-funktionen.html.
- Next steps: user decides on releasing d1b234cc; then audit the six pages against live behaviour; rebase on origin/main; gate-review ALLOW; push HEAD:main; sudo -n systemctl start brain-job@deadlock-docs.service; verify 0 rejections; ask 3 Brain questions (moderation, AI chat reply, promo/invite); remove worktree and branch.
- Decision needed: whether smalltalk (non-partner outreach experiment, .tasks/2026-09-18-smalltalk-live-resume/REPORT.md) may be documented publicly.
