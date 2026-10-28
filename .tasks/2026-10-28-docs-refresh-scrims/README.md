# docs-refresh: scrims

Scope: public/discord-server/scrims.html (only scrim content).

Checked (origin/main, Deadlock-Bots): reaction_roles.rs SCRIM_SIGNUP_ROLE_ID and scrim.participants upsert on reaction-role grant; scrim_signup.rs (/scrim-signup modal, rank/roles/availability); main.rs registration; dm_gate.rs opt-out button text; commits 58830717, 92b44509, e5ded020, c90cced5 (Brain replies, DM error paths). Turniere turnier-scrim: scrim.teams.discord_role_id sync, substitute role expiry (migration 2026071601).
Live (dl-bot list_channels, read-only): Scrims category channels.

Not found in code: any path where a Brain answer grants Scrim-Teilnehmer or a team role; no string "Scrim-Manager" or "Scrim-Teilnehmer". Documented per owner statement, listed as open item.

Open: lobby code delivery to team channel (kept from earlier page, not re-verified); Scrim-Manager role ID not in code.
