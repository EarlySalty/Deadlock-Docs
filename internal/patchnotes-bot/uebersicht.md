---
title: "Patchnotes-Bot Übersicht"
tags: [internal, patchnotes-bot, übersicht]
stand: 2026-07-07
quelle: "Deadlock--Patchnotes-Bot"
---
# Patchnotes-Bot Übersicht

Der Patchnotes-Bot ist ein Python-Discord-Client. `requirements.txt` pinnt `discord.py==2.7.1`, `main.py` baut `PatchnotesClient`, lädt `BOT_TOKEN` und startet `client.run(token)` am Prozessende. (`requirements.txt`, `main.py`)

Der User-Service heißt `deadlock-patchnotes.service`. Die Unit nutzt `/home/naniadm/Documents/Deadlock--Patchnotes-Bot` als `WorkingDirectory`, startet `scripts/run_patchnotes_bot.sh` und hat `Restart=always`. (`/home/naniadm/.config/systemd/user/deadlock-patchnotes.service`)

Der Wrapper lädt Infisical, übernimmt ein systemd-Credential namens `infisical-token`, fordert `DEADLOCK_CENTRAL_DSN` und setzt `BOT_TOKEN` aus `DISCORD_TOKEN_PATCHNOTES` oder `PATCHNOTES_BOT_TOKEN`. (`scripts/run_patchnotes_bot.sh`, `/home/naniadm/.config/systemd/user/deadlock-patchnotes.service.d/20-creds.conf`)

Der Bot scannt Forum und Steam. Das Forum ist `https://forums.playdeadlock.com/forums/changelog.10/`, Steam ist `https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/` für App `1422450` und Feed `steam_community_announcements`. (`changelog_latest_fetcher.py`)

`check_latest()` holt Steam und Forum, verwirft Steam-Einträge ohne Patch-Score, sortiert nach Zeitstempel und bevorzugt bei gleicher Zeit das Forum. (`changelog_latest_fetcher.py`)

`changelog_content_fetcher.process()` lädt die Zielseite, versucht zuerst einen Steam-Event-Store zu parsen und fällt danach auf Forum-HTML zurück. Ein Forumspost mit kurzem Steam-Link-Preview oder Text `steam news` wird als Steam-Announcement nachgeladen. (`changelog_content_fetcher.py`)

Der normale Scan läuft beim Ready-Event sofort an und danach im internen Loop. Das Standardintervall ist `35` Sekunden; Steam-News-Signal und Steam-Version-Burst können den nächsten Scan per Wakeup vorziehen. (`main.py`)

Bei einem neuen Patch lädt `update_patch()` den Rohtext, prüft Dedup-Status, lässt den Text übersetzen, speichert in Postgres, startet den Brain-Sync und sendet danach Discord-Nachrichten. (`main.py`, `patchnotes_db.py`, `perplexity_requests.py`)
