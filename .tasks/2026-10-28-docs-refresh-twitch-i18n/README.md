# Docs refresh: Twitch language and domains (2026-10-28)

Scope: dashboard and website language, English host, domains, `/twitch/` website pages, public tour, chat behaviour for English channels.

## Sources checked
- origin/main Twitch-Bot: `bot/dashboard_v2/src/i18n/dictionary.ts` (`readInitialLanguage`, `browserLanguage`, `isEnglishDashboardHost`), `context/LanguageContext.tsx`, `components/layout/Header.tsx` and `LanguageSwitch.tsx`, `pages/Verwaltung.tsx` (tab "Konto & Verbindungen", section "Sprache"), `i18n/en/*.ts`, `publicTour.ts`, `preview/routes.ts`, `website/src/lib/landingLocale.ts`, `rust/crates/tb-chat/src/standard_replies.rs`, `rust/crates/tb-raid/src/partner_roster.rs`.
- `docs/architecture/LANGUAGES-AND-DOMAINS.md` (commit d1b234cc3) used as a lead, every claim re-checked against code.
- Caddyfile `~/repos/Caddy/hosts/v50671/Caddyfile` (read only): blocks for `deutsche-deadlock-community.de`, `dead-lock.de`, `twitch.earlysalty.com`, the `dead_lock_english_dashboard` and `dead_lock_oauth_redirects` snippets.
- Live curl (no login): `dead-lock.de/` 302 to `/streamer/`; `dead-lock.de/twitch/dashboard`, `/twitch/rundgang`, `/twitch/faq`, `/twitch/onboarding` 200; `deutsche-deadlock-community.de/twitch/rundgang` 200; `/demo/twitch/rundgang` 404 (not public). Served `landing-metadata.js` sets `lang="en"` on dead-lock.de and English strings ("Become a partner") exist in the served bundle.
- Git log since 2026-06-01 filtered for i18n, English, language, locale, domain (about 60 relevant commits, all in the dashboard, website and Caddy English work from 2026-10-14 to 2026-10-27).

## Inventory

| Feature | User-visible where | Documented before | Action |
| --- | --- | --- | --- |
| DE/EN switch in dashboard header | Dashboard header | wrong (only "Verwaltung, Konto" mentioned) | fixed in twitch-streamer-dashboard, new page |
| Language section in Verwaltung | Verwaltung, tab "Konto & Verbindungen" | partly (called "Konto") | corrected to exact tab name |
| Start language order (URL, stored, dead-lock.de, browser) | Dashboard first visit | correct in dashboard page, incomplete (no `?lang=` rule) | completed in new page |
| `?lang=de` / `?lang=en` URL parameter | any dashboard or partner page | undocumented | new page |
| dead-lock.de English host (dashboard and partner page) | dead-lock.de | undocumented | new page, overview |
| Partner page English on main host with `?lang=en` | /streamer/ on main host | undocumented | new page |
| English partner subpages (FAQ, onboarding, comparison, clips, affiliate portal, Vertriebler) | /streamer/..., /twitch/faq, /twitch/onboarding | undocumented | new page |
| OAuth from English host goes to main domain | Partner page button "Become a partner" | undocumented | new page |
| Social Media Manager English | /twitch/social-media | correct | kept |
| Uplink help, OBS guide, VOD notes follow language | Uplink area | correct | kept |
| Legal pages German only (Impressum, Datenschutz, AGB) | /twitch/impressum etc. | undocumented | new page |
| Chat replies German (greeting, release question) | Twitch chat | undocumented | new page, overview |
| Chat command names identical in all channels | Twitch chat | undocumented | new page |
| Auto-raid same language rule and cross-server release | Auto-raid | correct (auto-raid.html) | linked from new page |
| Invite link depends on guild | `!invite` | undocumented in detail | stated in general terms |
| Public tour `/twitch/rundgang` | Dashboard, no login | undocumented | new page |
| Domain list: main, dead-lock.de, legacy twitch.earlysalty.com | - | undocumented | new page |
| Admin host | - | - | not mentioned, not linked (rule) |
| Preview routes (`PREVIEW_MODE`) | localhost build only | not public | not documented (internal) |

Counts: 17 features in inventory (admin host and preview routes excluded). Already correct: 3 (Social Media Manager English, Uplink language, auto-raid language rule). Wrong or incomplete and fixed: 3 (dashboard switch location, Verwaltung tab name, start-language order). Newly documented: 11.

## Changes
- `public/twitch-bot/sprache-und-domains.html` (new): addresses, language switch, start order, English coverage, English setup path, bot chat behaviour, public tour.
- `public/twitch-bot/twitchbot-ueberblick.html`: section "Sprache und Adressen" with link, nav link.
- `public/twitch-bot/twitch-streamer-dashboard.html`: language paragraph names header switch and exact Verwaltung tab, links to the new page.

## Open items
- Public docs keep no internal rules: no raid target selection, no invite routing logic, no Caddy snippets, no admin host.
- The Deadlock Brain question path is verified after import (see report).
- The "Rundgang" description says only "ohne Anmeldung ansehen"; whether its data is demo data was not verified.
- Legacy `twitch.earlysalty.com` is mentioned generically; no change requested for it.
- `docs/architecture/LANGUAGES-AND-DOMAINS.md` in the bot repo is internal and was not touched (outside this scope).
