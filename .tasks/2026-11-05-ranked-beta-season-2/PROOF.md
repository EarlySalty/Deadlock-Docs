# Live proof: Brain answers on Ranked Beta Season 2

Path: POST 127.0.0.1:8788/v1/answer, requested_scopes `bot.public`, profile `fact`, Discord reads disabled. Token via Infisical eval, unset after each run.

Import: `sudo -n systemctl start brain-job@deadlock-docs.service`.

- Round 1 after d84ec0a (run 11886, accepted=1): only the Soft Reset question was right. Hero unlock was answered from the Halloween page, "Wann endet die Season?" returned insufficient_evidence, "Wie viele Schilde habe ich?" was read as items, "Wie funktioniert Ranked?" hit a one-off tool failure (correct on retry).
- Fix 8762d1d: season heading now says "aktuelle Season", unlock text names the Freischalt-Voraussetzungen, the Halloween page links to the new unlock rule.
- Round 2 after 8762d1d (run 11891, accepted=2): all five questions correct, answered from the new page.

## Round 2, 2026-11-05 (final)

### Wie funktioniert Ranked?
HTTP 200, status `answered`, 5 citations, release `maintenance-bf5a6d0dc2a9e82797518135d9d2a77550ce47dd9c38295b19d671538b0d4b8f`

Ranked läuft in Beta Season 2 vom 5. November 2026 bis zum 11. März 2027, und die Regeln aus Beta Season 1 gelten nicht mehr. Zum Start gibt es einen kleinen Soft Reset von im Schnitt etwa 1 Badge. Die höchste Startplatzierung ist Ascendant I, je nach Leistung in Beta Season 1 bis zu Ascendant III.

Pro Match gibt es 350 Rangpunkte. Vom letzten Unterrang zum nächsten Badge brauchst du 1500 Punkte, zwischen Unterrängen 1000. Phantom, Ascendant und Eternus haben keine Schilde mehr. Alle anderen haben 3 Schilde an der Grenze eines ganzen Rangs und 1 Schild zwischen Unterrängen.

Pro Ranked-Match gibt es 4 Helden-Bans, in Beta Season 1 waren es 3. Um einen Helden fürs Ranked freizuschalten, brauchst du 35 Punkte mit dem Helden: 2 pro Sieg und 1 pro Niederlage.

Jede Season hat eine eigene Bestenliste. Dafür brauchst du mindestens 50 Ranked-Matches in der Season innerhalb der letzten 30 Tage. Für eine Helden-Bestenliste sind mindestens 15 Ranked-Matches mit dem Helden in den letzten 30 Tagen nötig.

### Wie viele Schilde habe ich?
HTTP 200, status `answered`, 2 citations, release `maintenance-bf5a6d0dc2a9e82797518135d9d2a77550ce47dd9c38295b19d671538b0d4b8f`

Das hängt von deinem Rang ab, und ich sehe deinen Rang nicht. Ich gehe von den Rang-Schilden für Ranked aus, die bei Rangverlust schützen. In Beta Season 2 haben Phantom, Ascendant und Eternus keine Schilde mehr. Alle anderen Ränge haben 3 Schilde an der Grenze eines ganzen Rangs und 1 Schild zwischen Unterrängen.

Meinst du etwas anderes, etwa ein Item wie Ancient Shield, Spirit Shielding, Weapon Shielding oder Enchanter's Emblem? Sag kurz Bescheid, dann schaue ich nach den Werten.

### Wie schalte ich Helden fürs Ranked frei?
HTTP 200, status `answered`, 2 citations, release `maintenance-bf5a6d0dc2a9e82797518135d9d2a77550ce47dd9c38295b19d671538b0d4b8f`

Für Ranked schaltest du einen Helden mit 35 Punkten frei. Jeder Sieg mit dem Helden bringt 2 Punkte, jede Niederlage 1 Punkt. Seit Beta Season 2 zählen Punkte statt nur Siegen, die 15 Siege aus Beta Season 1 gelten nicht mehr.

Seit dem Update vom 30. Oktober 2026 gelten die neuesten 6 Helden nicht mehr als neu. Für sie gelten die normalen Freischalt-Voraussetzungen, und sie können ab sofort gebannt werden.

### Wann endet die Season?
HTTP 200, status `answered`, 1 citations, release `maintenance-bf5a6d0dc2a9e82797518135d9d2a77550ce47dd9c38295b19d671538b0d4b8f`

Die aktuelle Season ist Ranked Beta Season 2. Sie hat am 5. November 2026 begonnen und endet am Donnerstag, 11. März 2027.

### Wie funktioniert der Soft Reset?
HTTP 200, status `answered`, 2 citations, release `maintenance-bf5a6d0dc2a9e82797518135d9d2a77550ce47dd9c38295b19d671538b0d4b8f`

Zum Start von Beta Season 2 werden die Ränge leicht zurückgesetzt. Im Schnitt verlierst du etwa 1 Badge. Davor werden alle Ränge global neu verteilt, also zuerst die Kurve aller bestehenden Ränge, danach greift der Soft Reset. Zusätzlich nutzt Valve die Winrate aus Beta Season 1, um Spieler um 1 bis 2 Unterränge feiner einzuordnen. Das Ergebnis ist für jeden anders: Manche steigen trotz Reset sogar auf, andere rutschen etwas weiter ab als 1 Badge.

## Round 1, 2026-11-05 (before fix)

### Wie funktioniert Ranked?
HTTP 200, status `unavailable`, 0 citations, release `maintenance-bf5a6d0dc2a9e82797518135d9d2a77550ce47dd9c38295b19d671538b0d4b8f`

Werkzeugantwort konnte nicht sicher abgeschlossen werden.

### Wie viele Schilde habe ich?
HTTP 200, status `answered`, 4 citations, release `maintenance-bf5a6d0dc2a9e82797518135d9d2a77550ce47dd9c38295b19d671538b0d4b8f`

Ich sehe dein Inventar nicht, deshalb kann ich dir nicht sagen, wie viele Schilde du hast. Ich kann dir aber Werte und Wirkung einzelner Items nachschlagen. Welchen meinst du? Zur Auswahl stehen Ancient Shield (Antiker Schild), Spirit Shielding (Magieschild), Weapon Shielding (Waffenschild) und Enchanter's Emblem (Wappen des Zauberers).

### Wie schalte ich Helden fürs Ranked frei?
HTTP 200, status `answered`, 1 citations, release `maintenance-bf5a6d0dc2a9e82797518135d9d2a77550ce47dd9c38295b19d671538b0d4b8f`

Die genauen Voraussetzungen zum Freischalten für Ranked kann ich dir leider nicht sicher nennen. Sicher weiß ich nur: Seit dem Halloween 2026 + Gameplay Update vom 30. Oktober 2026 gelten die neuesten 6 Helden nicht mehr als neu. Für sie gelten für Ranked jetzt die normalen Freischalt-Voraussetzungen, und sie können ab sofort gebannt werden. Welche 6 Helden gemeint sind, steht im Update nicht.

### Wann endet die Season?
HTTP 200, status `insufficient_evidence`, 0 citations, release `maintenance-bf5a6d0dc2a9e82797518135d9d2a77550ce47dd9c38295b19d671538b0d4b8f`

Dazu habe ich gerade keine gesicherten Infos. Frag mich was zum Spiel: Held, Item, Build oder Mechanik.

### Wie funktioniert der Soft Reset?
HTTP 200, status `answered`, 2 citations, release `maintenance-bf5a6d0dc2a9e82797518135d9d2a77550ce47dd9c38295b19d671538b0d4b8f`

Zum Start von Beta Season 2 werden die Ränge leicht zurückgesetzt, im Schnitt verliert man etwa 1 Badge. Vorher wird die Rangverteilung global neu ausgerichtet: Zuerst wird die Kurve aller bestehenden Ränge neu verteilt, danach greift der Soft Reset von im Schnitt etwa 1 Badge. Zusätzlich nutzt Valve die Winrate aus Beta Season 1, um Spieler um 1 bis 2 Unterränge feiner einzuordnen.

Das Ergebnis ist für jeden anders: Manche steigen trotz Soft Reset auf, andere rutschen etwas weiter ab als 1 Badge.
