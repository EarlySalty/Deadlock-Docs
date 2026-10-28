# Docs refresh: streamer analytics, coaching, assistant (2026-10-28)

Scope: streamer- and viewer-facing numbers and coaching in Deadlock-Twitch-Bot dashboard_v2, chat commands and tb-dashboard-api. Branch docs/twitch-analytics-20261028, base origin/main 2da63d1.

## Inventory

| Feature | Visible where | Documented before | Action |
|---|---|---|---|
| Analytics tabs (Übersicht, Streams, Publikum, Wachstum, Planung, Zusammen spielen, Mein Profil, Was tun?, Monetization) | /twitch/analyse tab bar (TabNavigation.tsx) | wrong list ("Empfehlungen", "Monetarisierung") | fixed in analytics-dashboard, faq-analytics |
| Übersicht KPIs and gauges (Growth, Revenue, Network, Retention) | Übersicht | partial | fixed in analytics-dashboard |
| Viewer segments, Vermisste Chatter, Exklusiv/Shared, Viewer-Verzeichnis | Publikum | missing | documented in analytics-dashboard |
| Stream list and details | Streams | partial | documented in analytics-dashboard |
| Wachstum (followers, raids) | Wachstum | missing | documented in analytics-dashboard |
| Planung | Planung | missing | documented in analytics-dashboard |
| Mein Profil | Mein Profil | missing | described in analytics-dashboard (Bio, Bild, Banner, Streamplan, Entwurf/Veröffentlicht), matches PartnerProfile.tsx |
| Was tun? coaching (Pro Session, Empfehlungen, Format & Auffindbarkeit, Community & Konkurrenz, KI-Analyse) | Was tun? | missing | new page coaching-was-tun |
| Markt-Unterreiter (Wachstum > Markt) | Wachstum | missing | new page kategorie-markt; /twitch/kategorie is a different page (CategoryCollector), not covered |
| Zusammen spielen (partner overlap, voice channels) | Zusammen spielen | missing | new page zusammen-spielen |
| Dashboard assistant "Hilfe bekommen" | Live release 4bfc09af: every dashboard route except preview/demo (App.tsx zeigeAssistent); origin/main d1b234cc restricts it to /twitch/dashboard (PREVIEW_HOME_ROUTE) | missing | page written for live state; update when the restriction ships |
| Lurker-Steuer and reward "Lurker Steuer" | Verwaltung | partial (reminder only) | new page lurker-steuer, streamer-dashboard updated |
| !lurkersteuer_off aliases | Chat, broadcaster only | documented, matches code | kept |
| Go-live Discord ping | Discord | wrong ("bestimmte Rollen-Pings") | fixed in discord-golive (no role ping) |
| Stats overlay | Verwaltung overlay | documented, matches | no change |
| Stream audit (tb-stream-audit) | admin DM only | n/a | not documented: private coaching audit, not streamer-facing |
| Titel-Studio (/twitch/titel) | Dashboard | outside this area | open item for title page owner |
| Partner challenges / ranking | Dashboard | outside this area, overlaps Paten | open item |
| Tagesform plan details | Dashboard | unverified | open item |
| watchtime text in chat-befehle | chat | not deeply verified | open item |
| stt and observability | not streamer-facing | n/a | not documented |

Counts: features found 22 (rows above, excluding the two open-item notes), already correct 3, fixed 3, newly documented 8, out of scope or private 4 (stream audit, stt, observability, Monetization content detail).

## Checks

- Importer format checker run on all 9 touched pages: h1 once, section ids ASCII, h2/h3 direct child of each section, no dashes: all OK.
- Still to do: merge gate, import run, Brain questions.

## Open items

- Mein Profil detail page and Monetization content are only named, not described.
- Titel-Studio, Partner challenges, Tagesform, watchtime wording in chat-befehle: other owners.
