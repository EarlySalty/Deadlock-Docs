# Docs refresh: Twitch bot, area Uplink (2026-10-28)

## Inventory (feature, where visible, documented, action)

| Feature | Where visible | Before | Action |
|---|---|---|---|
| Platforms Twitch, YouTube, Kick, TikTok | Uplink destination cards | Missing | Added to uplink-was-ist |
| TikTok only with RTMP access, chat not confirmed | TikTok card | Missing | Added to uplink-was-ist |
| Add-on and waitlist access | Uplink access state, admin waitlist | Missing | Added to uplink-was-ist |
| Desired vs running output, live confirmation | Destination status | Present | Kept |
| Twitch VOD audio automatic (Spur 1 live, Spur 2 VOD) | Twitch card audio hint | Present in uplink-obs step 4 | Kept, note in was-ist |
| Missing VOD track: only Twitch output holds | Twitch card | Present (uplink-obs step 4) | Repeated in stoerungen |
| Encoder analysis: local log only, not uploaded | OBS encoder analysis | Missing | Added to uplink-obs step 2 |
| Four OBS dock windows (chat, activity, stream info, channel points) | Dock section | Missing (step 6 generic) | Added to uplink-docks (new), linked from uplink-obs step 6 |
| Dock address privacy, hidden while live, regeneration | Dock section | Missing | uplink-docks |
| Presets 1080p60 .. 480p30 with bitrates | Quality card | Missing | uplink-ziele-qualitaet (new) |
| Manual output (width, height, fps, bitrate, even numbers) | Quality card | Missing | uplink-ziele-qualitaet |
| Saved vs running profile | Quality card | Partly (was-ist) | uplink-ziele-qualitaet |
| Live change result: applied, applied_restart, too_busy, next_stream | Quality card message | Missing | uplink-ziele-qualitaet |
| Twitch operating modes: Einzelstream, Enhanced, native 2K HEVC, AV1 test | Twitch operating mode | Missing | uplink-ziele-qualitaet |
| Reconnect wait 0..300 s, default 90 s, next session | Disturbance card | Missing | uplink-stoerungen |
| Status texts: Rechte ergänzen, Neu verbinden, Stream-Schlüssel holen | Destination card | Missing | uplink-stoerungen |
| Reconnect wait not yet applied | Reconnect card | Missing | uplink-stoerungen |
| No own waiting image | n/a | Not stated | uplink-stoerungen |
| Hochkant output | Dead component UplinkHochkantEditor.tsx, not mounted | Not stated | Stated as not offered (was-ist) |
| Automatic YouTube live start | Dead component UplinkYouTubeLive.tsx, not mounted | Not stated | Stated as not offered (was-ist) |
| Standard connect wording (Stream-Key, chat, activity, stream info, channel points) | Connect rights list | Missing | Partly, in stoerungen and docks |
| Old "Eingeschaltet" and disturbance texts | Multiple | Garbled German in stoerungen | Rewritten |

Counts: 22 rows. Already correct: 2 (desired vs running output, VOD audio). Garbled text fixed: 1 (stoerungen). Newly documented: 17. Stated as not offered: 2.

## Changed files

- public/twitch-bot/uplink-was-ist.html (rewritten, meta stand 2026-10-28)
- public/twitch-bot/uplink-stoerungen.html (rewritten)
- public/twitch-bot/uplink-obs.html (step 2 encoder note, step 6 dock link)
- public/twitch-bot/uplink-ziele-qualitaet.html (new)
- public/twitch-bot/uplink-docks.html (new)
- public-sources.json (managed_targets: two new pages)

## Checks

- Importer format check (main children h1/p/section, section ids ASCII): all five uplink pages pass.
- No em dashes.

## Open items

- berichte/twitch-website-pruefung.json has audit records for the three edited pages (content hash). The website refresh path (tools/refresh_public_corpus.py, withdraw_invalid_audits) moves pages with a changed hash to archive/ until re-audited. The new pages have no audit record. Brain import (brain-job, origin/main) is not affected by this gate per RULES.md. The website export is, and needs a fachprüfung run.
- obs_docks.enabled defaults to off in rust/bin/tb-bot/src/obs_dock.rs; production switch and config location not verified. The docks page describes what the dashboard shows.
- YouTube live auto-start card and Hochkant editor are unmounted; if they get mounted, update uplink-was-ist.
- rust/knowledge/bot/uplink-obs.md may still say SRT address (bot knowledge, outside this docs area).
- Kick/YouTube server-side availability flag per user not verified.
