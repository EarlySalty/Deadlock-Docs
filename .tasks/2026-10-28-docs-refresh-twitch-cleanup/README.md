# Twitch and Discord docs cleanup, 2026-10-28

Scope: follow-up to audit merges c7ec169, ac9297c, ae15a37, f68b1cf.

Done in this change:
- streamer-partner-werden.html: bot pause line now states the 60-day rule (mod rights removed, DM, automatic return on Deadlock stream with valid Twitch connection). Source: rust/crates/tb-raid/src/deadlock_pause.rs at twitch 8e00a346.
- clip-befehle.html: vodclip section states one active job per channel and at most three per hour. Source: rust/crates/tb-vod-archive/src/private_range.rs at 8e00a346.
- twitch audit: 11 entries with a false "Codeänderungen aus d1b234cc" gap cleared; 4 same-code entries moved to live revision 8e00a346; clip-befehle rehashed with new claim. d1b234cc only changes docs, so the checked code paths equal the live release. Claim text of the 11 cleared entries was carried from the earlier verification on identical code, not re-read line by line in this pass.

Not done, left for a follow-up (the refresh tool withdraws these to archive/ until re-verified):
- Pages with real code drift since their audited revision: kategorie-markt, dashboard-hilfe, lurker-steuer, zusammen-spielen, coaching-was-tun, analytics-dashboard, faq-analytics.
- Stale page hashes: einrichtung, faq-einstieg, uplink-obs, uplink-was-ist, uplink-stoerungen, quellen/twitch/features, berechtigungen, quellen/twitch/chat_network_disabled, quellen/twitch/werbemanager, quellen/website/{anfaenger,beitreten,coaching,mitspieler,transparenz,wohin}, quellen/turniere/{help_tournament_modes,comp-finder}, faq-stats-overlay.
- discord-brain entry for streamer-partner-werden.html: stale hash, and its Streamer-Rolle claims (lines 36-37, 4 weeks / 4 days in 30) are not re-verified.

Werbemanager: the "Werbung (Experimentell)" tab is in the live bundle and not gated, so the page stays with its experimental label.
Duplicate audit entries: none found in either berichte file; prepare-only exits 0.
