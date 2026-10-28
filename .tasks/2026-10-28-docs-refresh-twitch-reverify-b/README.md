# Twitch public pages re-verification, share l-z (agent b)

Goal: every listed public page is checked against the live Twitch release 8e00a346b58a3dbb108f1b4a23ab89d67a51bdcb and its audit entry is updated, so no page is archived or withdrawn from the Brain on a stale entry.

Selection (tools/knowledge_metadata.py verified_audit logic and sha256 of the file bytes; criteria: hash differs, live_release_revision != 8e00a346, or gap/pending note; file name l-z; plus kategorie-markt which the task names explicitly):

- public/quellen/twitch/werbemanager.html (hash differs, live 4bfc09af)
- public/quellen/website/mitspieler.html (hash differs, no live revision)
- public/quellen/website/transparenz.html (hash differs, no live revision)
- public/quellen/website/wohin.html (hash differs, no live revision)
- public/twitch-bot/kategorie-markt.html (named by task; WIP text from 6143a2a; file name starts with k, see note)
- public/twitch-bot/lurker-steuer.html (live 4bfc09af)
- public/twitch-bot/social-ai-videos.html (no audit entry)
- public/twitch-bot/social-media-manager.html (no audit entry)
- public/twitch-bot/sprache-und-domains.html (no audit entry)
- public/twitch-bot/titel-studio.html (no audit entry)
- public/twitch-bot/ueber-den-bot.html (no audit entry)
- public/twitch-bot/uplink-docks.html (no audit entry)
- public/twitch-bot/uplink-obs.html (hash differs, live e4118d3e, operational gap note)
- public/twitch-bot/uplink-stoerungen.html (hash differs, live e4118d3e, operational gap note)
- public/twitch-bot/uplink-was-ist.html (hash differs, live e4118d3e, operational gap note)
- public/twitch-bot/uplink-ziele-qualitaet.html (no audit entry)
- public/twitch-bot/vertrauen-seriositaet.html (no audit entry)
- public/twitch-bot/vod-archiv.html (no audit entry)
- public/twitch-bot/zusammen-spielen.html (hash differs, live 4bfc09af; WIP text from 6143a2a)

Note: kategorie-markt starts with k, outside l-z. Included because the task names it explicitly.

Code basis: ~/repos/Deadlock-Twitch-Bot at 8e00a346. origin/main is d1b234cc; the 14 files that differ are docs only, so code paths are identical.
