---
title: "Patchnotes-Bot Architektur"
tags: [internal, patchnotes-bot, architektur]
stand: 2026-07-07
quelle: "Deadlock--Patchnotes-Bot"
---
# Patchnotes-Bot Architektur

`main.py` ist der Prozesskern: Discord-Client, Ready-Handler, Scan-Loop, Retranslation-Befehle, Dispatch-State, Brain-Sync-Start und Discord-Versand liegen dort. (`main.py`)

`changelog_latest_fetcher.py` bestimmt den neuesten Kandidaten aus Steam-News-API und Forum-Thread. Das Modul bewertet Steam-Einträge über Titel-, Bullet- und Abschnittshinweise und liefert nur den neuesten Steam-Kandidaten an die Posting-Pipeline. (`changelog_latest_fetcher.py`)

`changelog_content_fetcher.py` extrahiert den Inhalt. Steam wird aus `data-partnereventstore` und BBCode gelesen, Forum aus `article.message` und `div.bbWrapper`; Steam-Spiegel aus Forumsposts werden nur aus dem ausgewählten Post verfolgt. (`changelog_content_fetcher.py`)

`patchnotes_db.py` ist der Laufzeit-DB-Layer. Er nutzt `asyncpg.create_pool()`, liest `DEADLOCK_CENTRAL_DSN`, schreibt `patchnotes.changelog_posts`, spiegelt Rohtext nach `patchnotes.deadlock_changelogs` und nutzt `bot.kv_store` für Bot-State. (`patchnotes_db.py`)

`perplexity_requests.py` baut System- und User-Prompt, ruft `https://api.perplexity.ai/chat/completions` mit `disable_search=True` auf und liest `PERPLEXITY_API_KEY`, `PERPLEXITY_MODEL` und `PERPLEXITY_MAX_TOKENS`. (`perplexity_requests.py`)

`patch_view.py` und `entity_emojis.py` gehören zum optionalen Components-V2-Pfad. `main.py` nutzt ihn nur, wenn `PATCH_EMBED_V2` gesetzt ist; Renderfehler fallen auf Textversand zurück. (`main.py`, `patch_view.py`, `entity_emojis.py`)

`reconcile_patchnotes.py` ist kein Runtime-Pfad. Das Tool vergleicht alte SQLite-Daten mit zentralem Postgres und schreibt nur mit `--apply --confirm-apply`. (`reconcile_patchnotes.py`)

## Dedup

Die Inhalts-Signatur kommt aus `_content_signature()`: Der Bot trimmt den Rohtext, ersetzt jede Whitespace-Gruppe durch einen Zeilenumbruch und hasht das Ergebnis mit SHA-256. (`main.py`)

Der Dispatch-State liegt in `bot.kv_store` unter Namespace `patchnotes_bot` und Key `dispatch_content_sha256:<signatur>`. `pending` und `sent` blockieren einen erneuten Versand. (`main.py`, `patchnotes_db.py`)

`_patch_data_already_processed()` blockiert Kandidaten über drei Wege: gespeicherter Dispatch-State, gespeicherte kanonische URL oder identischer `raw_content` in `patchnotes.changelog_posts`. (`main.py`, `patchnotes_db.py`)

`_select_candidate_urls()` vergleicht Steam- und Forum-IDs nicht direkt. Bei Steam wird nur der neueste Steam-Link geprüft; bei Forum nutzt der Bot die Post-Reihenfolge und begrenzt Catch-up über `PATCH_MAX_CATCHUP_POSTS`. (`main.py`)

## KI-Aufbereitung

`_translate_patch_content()` versucht große Patches zuerst als einen Request, solange der Text unter `PATCH_TRANSLATE_SPLIT_THRESHOLD` liegt. Bei abgeschnittener Antwort oder überschrittenem Schwellenwert teilt `_translate_patch_content_in_parts()` den Text entlang erkannter Abschnitte. (`main.py`)

`_request_patch_translation()` ruft Perplexity erst normal und dann im Strict-Modus auf. Leere, unbrauchbare oder abgeschnittene Antworten werden verworfen; bei nicht rettbarem Fehler fällt der Bot auf Rohtext zurück oder splittert den Text. (`main.py`)

Nach der KI-Antwort entfernt der Bot Code-Fences, Zitate, Links und Rollen-Pings, repariert bekannte Begriffe, gruppiert Hero- und Item-Blöcke und teilt den Text unter das Discord-Limit. (`main.py`)

Perplexity bekommt keinen Websuchlauf. `fetch_answer()` sendet `disable_search=True`, `temperature=0.0` im Strict-Modus und `temperature=0.2` sonst. (`perplexity_requests.py`)
