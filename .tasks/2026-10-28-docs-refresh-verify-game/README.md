# Docs-Refresh: Verifikation dreier Seiten gegen Quellen

Ziel: die Seiten `anfaenger`, `comp-finder` und `help_tournament_modes` gegen den
Quellcode bzw. die gepinnten Spieldaten prüfen, Text korrigieren, Audit-Eintrag
je Seite mit Hash, Pins und Belegen aktualisieren.

## Ergebnis je Seite

- `public/quellen/website/anfaenger.html`: Text geändert. Nicht belegbare
  Aussagen entfernt: Support-Kontakt, Übungsbereich, feste Minutenphasen,
  "Lanes öffnen", Ausweichen. Belegte Aussagen (Souls, Items, Nahkampf Q und F,
  Coaching) mit Spielwiki- bzw. Seitenbelegen bestätigt. Gaps leer.
- `public/quellen/turniere/comp-finder.html`: Text unverändert, alle Aussagen
  gegen Turniere `feb7a2a` bestätigt. Gaps leer.
- `public/quellen/turniere/help_tournament_modes.html`: Text unverändert, alle
  Aussagen gegen Turniere `feb7a2a` bestätigt. Gaps leer.

## Pins

- Spieldaten: Deadlock-Brain `origin/main` 2bb225de. Die Wiki-Seite
  `game-wiki/pages/deadlock-wiki/wiki-page.md` ist dort identisch zum früheren
  Pin b306fa90 (dort war nur `game-wiki/AGENTS.md` geändert).
- Turniere: `origin/main` feb7a2a49c50418b527918e93a8c36671d14c889.

## Manifest

- `public-sources.json` (Reviews der drei Seiten) auf den neuen Audit-Stand gezogen:
  Hash, Zeitstempel und Code-Pins. Die Repo-ID `docs` im Audit ist `community-docs`.
- Route `/turnier/comp`: Caddy-Site `deutsche-deadlock-community.de` leitet
  `/turnier*` an Port 8900 weiter (Caddyfile, Block ab Zeile 203).
