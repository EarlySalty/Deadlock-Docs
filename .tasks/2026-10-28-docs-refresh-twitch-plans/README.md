# Docs refresh: Twitch account lifecycle (2026-10-28)

Branch: docs/twitch-plans-20261028, base origin/main 5ef05ff.

## Inventory (feature, where visible, documented, action)

| Feature | Where visible | Documented before | Action |
|---|---|---|---|
| Plans Free / Plus / Studio (three versions), Plus monthly and yearly | /twitch/pricing | no tiers | fixed: faq-plaene |
| Yearly = 10 months price | /twitch/pricing | no | fixed: faq-plaene |
| Trial 30 days, Plus monthly only | /twitch/pricing FAQ | no | fixed: faq-plaene (card wording left out, see open items) |
| Cancellation at period end, Kundenportal | Kundenportal | yes | kept |
| Analytics data 30 days after cancellation | /twitch/pricing FAQ | no | added: faq-plaene |
| Functions switched off under "Bot & Schutz" on Plus | Verwaltung | no | added: faq-plaene |
| Affiliate portal /twitch/affiliate/portal, active account only | portal | wrong path only | fixed: faq-affiliate |
| Claims (only for active affiliate accounts) | portal | vague | fixed: faq-affiliate |
| Gutschrift status, Stripe payout account | portal | vague | fixed: faq-affiliate |
| Affiliate 30 percent figure | public program page | not stated | left out, open item |
| Verwaltung (/twitch/verwaltung) | dashboard | not listed | added: twitchbot-ueberblick |
| Challenges (/twitch/challenges): achievements, weekly quests, two rankings, monthly rewards | dashboard | no | new page challenges.html |
| Partner profiles and stream calendar (/twitch/partners) | public | no | new page partnerprofil.html |
| Feedback (/twitch/feedback) | dashboard | no | new page feedback.html, linked from faq-support |
| Roadmap (/twitch/roadmap) | public | no | not documented: route returns 404 live (see open items) |
| Onboarding, OAuth connect, revoke, help wording | /twitch/onboarding, twitch.tv settings | yes | checked, unchanged |
| Berechtigungen (scope names) | OAuth consent | general only | not changed, scope names not verified |
| faq-einstieg, vertrauen-seriositaet | docs | yes | checked, unchanged |
| Account deletion | support | described as request via contact | unchanged, no self-service deletion verified |

Counts: 19 items. Fixed or added in existing pages: 9. Newly documented (new pages): 3 (challenges, partnerprofil, feedback). Already correct or unchanged: 5 (cancellation, onboarding/OAuth, berechtigungen, faq-einstieg/vertrauen, deletion). Not documented, see open items: 2 (affiliate 30 percent, roadmap).

## Open items

- Trial card wording conflicts: /twitch/pricing FAQ says the card is charged after the trial, TrialCallout says "Keine Kreditkarte erforderlich". Needs a product decision.
- Affiliate 30 percent: stated in the public website bundle (/streamer/vertriebler/), not on a verified live text. Left out until decided.
- Roadmap: route /twitch/roadmap is merged in origin/main (handlers/roadmap_page.rs) but returns 404 live. Not documented until deployed.
- Scope labels on the OAuth consent screen and account deletion: not verified.
- Partner profile opt-in location in the dashboard: not verified.
- Challenges monthly reward details: page text not verified.
- Tabs of Verwaltung: German labels not verified; only the ids are documented.
- Other agents' pages not touched: titel-studio, auto-raid, faq-raids, werbemanager, chat-befehle, sprache-und-domains, social/VOD/caster/uplink/analytics.
