# Docs refresh: verify discord public pages (mitspieler, transparenz, wohin)

Sources at origin/main: Deadlock-Bots c68f89a8, Deadlock-Brain 2bb225de, Deadlock-Twitch-Bot d1b234cc3. Live channel and voice facts via dl-bot read-only (public_server_facts, list_channels).

## mitspieler.html
- Replaced the non-existent "player-finder" claim. Now describes the LFG panel in 📖sprachkanal-verwalten, Gesuch posts in 🎯mitspieler-suche, Join-to-create in ➕Sprachkanal erstellen, Owner übernehmen, the Ranked rank gate, the 🔎mitspieler-suche text channel, and the Brain (Concierge/!brain) linking open lanes.
- Open: purpose of 🔎mitspieler-suche is inferred from name and activity. A second channel 🔎mitspieler-suche (1563950781441384458, Neue Spieler) is not described.

## transparenz.html
- Dashboard disclaimer aligned to public/twitch-bot/analytics-dashboard.html wording. Attendance-specific claim removed (no code basis).
- Open: gaps and delays in the Twitch-Bot collection logic not checked.

## wohin.html
- Scrim and Turnier links point to existing pages. Uplink OBS link added. Support channel named.
- Open: "freiwilliges Coaching" only checked by channel existence.

## Brain check
- Brain answers teammate questions with open lanes and placeholder join links (provider_input.rs, discord_live.rs).
