# TODO: Twitch-Seiten-Re-Verifikation (Teil b), Stand 2026-10-28

Ziel: jede Seite der Liste gegen Twitch 8e00a346 prüfen und den Audit-Eintrag in berichte/twitch-website-pruefung.json aktualisieren.
Code-Basis: ~/repos/Deadlock-Twitch-Bot bei 8e00a346 (origin/main d1b234cc, 14 Dateien nur Docs abweichend).

## Erledigt (committed, Branch docs/twitch-reverify-b-20261028)

- Branch-Commits: kategorie-markt, zusammen-spielen, lurker-steuer (31c9cdf, Rebase auf origin/main)
- social-media-manager (Instagram-Limit-Satz entfernt, nicht im Code belegt), social-ai-videos (Zitat "Im Claude-Abo enthalten"), vod-archiv (!vodclip für Kanalinhaber und Mods), ueber-den-bot, vertrauen-seriositaet
- tools-Unit-Tests grün. validate_corpus.py meldet 12 Funde, alle in internal/wissensbasis/*.md (nicht durch diesen Branch verändert), keine in public/twitch-bot/.

## Offen

Gelesen, aber noch nicht gegen Code geprüft:
- sprache-und-domains: "Become a partner" als Button-Text im Code nicht gefunden (nur "Wie werde ich Partner?"). Satz ändern oder Button-Text belegen. Begrüßung "höchstens alle zehn Minuten" prüfen (standard_replies.rs, Cooldown-Konstante).
- titel-studio: Stil, "Das will ich nie im Titel" (40 Einträge, Test bestätigt), Experimentell-Schalter, !title/!titel (catalog.rs bestätigt) grob belegt. Restliche Sätze prüfen.
- uplink-docks: Fensternamen und Knopf "Zeigen" grob belegt. "Neu-Erzeugen" im Code nicht gefunden, nur "Neu erzeugen". Sichtbarkeitsregel prüfen.
- uplink-obs: EnableCustomServerVodTrack und Twitch-VOD-Spur im Code belegt. Schritte, Tonmodi und Encoder-Aussagen einzeln prüfen.
- uplink-stoerungen, uplink-was-ist, uplink-ziele-qualitaet: noch nicht gelesen.
- quellen: werbemanager, mitspieler, transparenz, wohin: noch nicht bearbeitet.
- titel-studio und sprache-und-domains brauchen je einen Audit-Eintrag.

## Nächste Schritte

1. Pro offener Seite Behauptungen einzeln prüfen; nur "verified" oder "removed" (Textänderung) setzen.
2. Einträge in /tmp/docs-refresh/reverify-b/entries/ schreiben, mit apply.py anwenden, Unit-Tests laufen lassen.
3. gate-review --repo <worktree> --base origin/main bis ALLOW (rolle-merge-schleuse).
4. Rebase auf origin/main, Push nach main nur nach ALLOW.
5. Brain-Job-Import mit Ablehnungszählung, zwei Brain-Fragen über /tmp/docs-refresh/ask.sh.
6. Worktree und Branch aufräumen.

## Hinweise

- kategorie-markt liegt außerhalb des Buchstabenbereichs l-z, wurde auf ausdrücklichen Wunsch aufgenommen.
- Der Weg Twitch-Einstellungen > Verbindungen (vertrauen-seriositaet) liegt außerhalb des Repos und ist nicht im Code belegt.
