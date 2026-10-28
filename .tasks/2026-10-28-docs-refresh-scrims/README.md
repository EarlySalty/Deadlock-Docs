# docs-refresh: scrims

Scope: public/discord-server/scrims.html (only scrim content).

Rule: the public page holds only the general process. No team names, rosters, team channel contents, team match times, staff, mod or ticket content. Team-specific answers come from the role-filtered live Discord access of the Brain.

Checked (Deadlock-Bots origin/main): reaction_roles.rs SCRIM_SIGNUP_ROLE_ID grant via reaction-role mapping and scrim.participants upsert; scrim_signup.rs (/scrim-signup modal, rank/roles/availability, rank source steam/discord_role/self); dm_gate.rs opt-out button text; commits 58830717, 92b44509, e5ded020, c90cced5. Turniere turnier-scrim: team role sync, substitute expiry (migration 2026071601).

Live (dl-bot list_channels, read-only): Scrims category channel names only. No team content read.

Not verified in code: a Brain or DM path that grants Scrim-Teilnehmer (owner statement only; the reaction path is the code-backed one); the "Scrim-Manager" role name and ID; the lobby code delivery channel; whether /scrim-signup is open in the live scrim runtime (code refuses saves outside legacy mode, scrim_signup.rs:40-41).
