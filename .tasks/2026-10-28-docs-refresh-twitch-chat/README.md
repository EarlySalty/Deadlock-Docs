# Docs refresh: Twitch chat (2026-10-28)

Source: Deadlock-Twitch-Bot origin/main d1b234cc3 (local ref, read from the ~/repos checkout; tb-chat command dispatch, sub_reminder.rs, follow_hint.rs, command catalog).

## Inventory (chat-befehle scope)
| Feature | Where visible | Before | Action |
|---|---|---|---|
| !raid/!traid, !silentban, !silentraid, !engagement_on/off: super-mods allowed | chat | wrong (only broadcaster/mods) | fixed |
| !uban/!unban, !explain: broadcaster and mods only | chat | correct | kept |
| !title/!titel: needs dashboard switch | chat | missing switch | added |
| !raid failure replies (Neu-Autorisierung, partner, raids switch) | chat | missing | added |
| !clip: 5-60 s setting in dashboard, pause, offline refusal | chat | partial | added |
| !clipcontest: max 3 per channel per day, community votes in Discord | chat | missing limit | added |
| !invite via @mention, default self | chat | partial | added |
| !dldc/!dlde: streamer vs viewer link | chat | missing | added |
| !sub erinnerung an/aus/status, public reminder after end | chat | partial | added as own subsection |
| Follow-Hinweis (opt-in, non-followers, mods/commands excluded) | chat | undocumented | added |
| Begrüßung: only replies to a bare greeting, once per person and stream, default off | chat | undocumented | added |
| Eigene Befehlsnamen: letters/digits, max 32 chars | dashboard | partial | added rule |
| Eight per-channel stat command switches | dashboard | missing | added sentence |
| Em/en dashes in existing text | page | rule violation | removed |

## Not verified or not documented yet (open)
- Release-question reply in standard_replies.rs: exact trigger unclear, omitted.
- Follow hint: verified. Pipeline calls it only for a first chat message (tracked_was_first_message), sends only to non-followers, skips mods, commands and foreign shared chat, 90 s channel cooldown. Page states this.
- Smalltalk/AI chat replies, promos, promo pitch, LFG pitch, invite question, streamer voice: not read in this pass.
- Title studio /twitch/titel details, crew_guard action state, token-health notifications, bot language in chat: not covered.
- chat-moderation, faq-funktionen, faq-community: not edited in this pass.
