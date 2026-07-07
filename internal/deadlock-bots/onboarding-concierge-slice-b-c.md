---
title: "Onboarding-Concierge — Spec Slice B (Paten-Matching) + Slice C (eine DM-Stimme)"
tags: [deadlock-bots, onboarding, concierge, paten]
stand: 2026-07-07
quelle: "Deadlock-Bots rust/crates/dl-community/src/concierge.rs, rust/crates/dl-voice/src/nudge.rs, rust/crates/dl-voice/src/feedback.rs"
---

# Slice B — Paten-Matching, Slice C — eine DM-Stimme

Verbindliche Umsetzungs-Spec. Alle user-sichtbaren Texte stehen in §T und
werden EXAKT übernommen (keine Umformulierung). Basis-Design aus dem
grillme vom 07.07.: Pate ist immer ein Mensch aus der Rolle
1524047896297738311, der Concierge vermittelt und zieht sich zurück.

## Slice B — Flow

Heutiger Stand (Slice A): Klick auf „Ja, gern" (`concierge:pate:yes`) →
`request_pate` postet einen Rollen-Ping als Text in `pater_channel_id`.
Kein Claim, kein Kanal, kein Match.

Neu:

1. **Claim-Post statt Roh-Ping.** `request_pate` postet in
   `DL_CONCIERGE_PATE_CHANNEL_ID` (Kanal existiert: 1524083665838276860,
   #paten-zentrale) eine V2-Nachricht (Gold-Container wie alle
   Concierge-Posts): Rollen-Ping `<@&1524047896297738311>` +
   Kurz-Digest des Neulings (`short_digest`, existiert) +
   Rang-Empfehlung + Button „Ich übernehme"
   (`custom_id: concierge:pate:claim:<user_id>`). Texte §T1.
2. **Rang-Empfehlung.** Kandidaten = Member der Paten-Rolle. Dafür
   bekommt der `ConciergePort` eine neue Methode
   `role_member_ids(guild_id, role_id) -> Result<Vec<u64>, String>`;
   Implementierung im dl-bot-Glue über den bestehenden Adapter/REST
   (Member-Liste holen, nach Rolle filtern; es gibt bereits
   `role_members` im dl-broker-Port als Vorbild). Score = Abstand der
   Rang-Indizes: Rang je User aus `core.steam_links.deadlock_rank_name`
   (Query wie `has_linked_rank`, `ORDER BY primary_account DESC,
   deadlock_rank_updated_at DESC LIMIT 1`), Index über `RANK_ORDER` aus
   `dl-stats` (Crate-Dependency nur, wenn kein Zyklus entsteht; sonst
   SQL + lokale Konstante mit Kommentar auf die Quelle). Paten mit ≥3
   aktiven Patenschaften fliegen aus der Empfehlung. Ohne Rang-Daten
   oder ohne Kandidaten: Fallback-Zeile §T1b, kein Fehler.
3. **Claim.** Handler prüft in dieser Reihenfolge: Klicker hat die
   Paten-Rolle (Member-Roles aus der Interaction) → sonst §T2a
   ephemeral. KV-Claim `claim_once("concierge:pate_claim", user_id)`
   gegen Doppelvergabe → verloren heißt §T2b ephemeral. Load-Limit:
   Klicker hat <3 aktive Patenschaften → sonst §T2c ephemeral (und der
   KV-Claim wird NICHT verbraucht bzw. wieder freigegeben, damit ein
   anderer Pate noch übernehmen kann; wenn claim_once das nicht kann,
   Reihenfolge tauschen: Limit vor Claim prüfen).
4. **Match.** Bei Erfolg: Zeile in `bot.concierge_patenschaften`;
   privaten Textkanal erstellen (bestehender Port
   `create_private_channel`, Kategorie `DL_CONCIERGE_PATE_CATEGORY_ID`,
   Default 1465839366634209361, Fallback `fallback_category_id`), Name
   `pate-<username-slug>`; der Kanal braucht zusätzlich ein Overwrite
   für den Paten (View/Send/History) — wenn `create_private_channel`
   nur einen User kann, Port-Methode um `extra_user_id: Option<u64>`
   erweitern. Dann: Intro-Post §T3 im neuen Kanal (V2), DM §T4 an den
   Neuling, Bestätigung als Reply auf den Claim-Post §T5, Journey-Event
   `pate_matched`.
5. **„Auf Wunsch".** LLM-Antwortvertrag (JSON in `llm_answer`) um Feld
   `"pate_request": bool` erweitern; System-Prompt-Ergänzung §T6. Wenn
   true: an die normale Antwort die bestehenden Ja/Nein-Buttons
   (`concierge:pate:yes/no`) hängen; ist die Antwort leer, stattdessen
   Text §T6b mit denselben Buttons.
6. **DB-Migration** `2026070712_concierge_patenschaften.sql`:
   - `bot.concierge_patenschaften` (`id BIGSERIAL PK`, `user_id BIGINT
     NOT NULL`, `pate_id BIGINT NOT NULL`, `guild_id BIGINT NOT NULL`,
     `channel_id BIGINT`, `created_at TIMESTAMPTZ NOT NULL`,
     `released_at TIMESTAMPTZ`); Unique-Partial-Index ein aktives Match
     pro User (`WHERE released_at IS NULL`), Index auf `pate_id` mit
     demselben Filter (Load-Query).
   - `journey_events`-CHECK-Constraint um `'pate_matched'` erweitern
     (Constraint droppen und mit vollständiger Liste neu anlegen, wie in
     Migration 2026070710).
   - Neue Journey-Variante `PateMatched` in
     `dl-activity/src/journey.rs`.
   - `bot.concierge_patenschaften` in `privacy.rs` `USER_TABLES`
     aufnehmen (Erasure) und in `forget_user` mitlöschen.
7. **Kein Auto-Release in v1.** Patenschaften enden nur manuell (SQL);
   Load zählt `released_at IS NULL`. Bewusste Lücke, steht hier.

## Slice C — Flow

Stufe 1 (Ton) + Gedächtnis-Light. Nur diese zwei Streams, Leave-Survey
und Coaching-DMs bleiben unangetastet:

1. **Steam-Nudge** (`rust/crates/dl-voice/src/nudge.rs`): Embed-Titel
   und `DM_DESCRIPTION` durch §T7 ersetzen. Button-Label und Mechanik
   unverändert.
2. **Voice-Feedback** (`rust/crates/dl-voice/src/feedback.rs`): Texte in
   `build_message` (first/second), `ACK_TEXT`,
   `FEEDBACK_ALREADY_RESPONDED_TEXT`, `FEEDBACK_WINDOW_EXPIRED_TEXT`
   durch §T8 ersetzen. Button-Label bleibt.
3. **Gedächtnis-Light:** Neue pub-Methode
   `ConciergeStore::record_system_dm(user_id, guild_id, marker: &str)`
   (kapselt `ensure_profile` + `record_conversation` mit Rolle
   `assistant`). Im dl-bot-Glue nach ERFOLGREICHEM Versand der
   Steam-Nudge-DM bzw. Feedback-DM aufrufen, Marker §T9, nur wenn
   `concierge_config.enabled`. dl-voice bleibt frei von
   Concierge-Wissen, die Verknüpfung lebt ausschließlich im Glue.

## §T — Finale Texte (exakt übernehmen)

T1 Claim-Post (Content über dem Button; `{user_mention}`, `{digest}`,
`{candidate_mention}` ersetzen):

> <@&1524047896297738311> Ein Neuling hätte gern einen Paten an seiner Seite: {user_mention}
> {digest}
> Vom Rang her würde {candidate_mention} am besten passen. Übernehmen darf, wer zuerst drückt.

T1b Fallback-Schlusszeile (statt der Rang-Zeile, wenn keine Empfehlung
möglich): `Wer Zeit und Lust hat, drückt auf Übernehmen.`

T1-Button-Label: `Ich übernehme`

T2a (ephemeral, Klicker ohne Paten-Rolle): `Der Knopf ist für unsere
Paten reserviert. Wenn du selbst Pate werden willst, meld dich bei den
Mods, wir freuen uns über jeden.`

T2b (ephemeral, schon vergeben): `Da war jemand schneller, die
Patenschaft ist schon vergeben. Danke dir fürs Draufdrücken.`

T2c (ephemeral, Load-Limit): `Du begleitest gerade schon drei Neulinge,
das reicht erstmal. Lass diesmal jemand anderem den Vortritt und danke,
dass du so aktiv bist.`

T3 Kanal-Intro (V2 im neuen privaten Kanal; `{user_mention}`,
`{pate_mention}`, `{digest}`):

> Willkommen ihr beiden. {user_mention}, darf ich vorstellen: {pate_mention} kennt unseren Server und das Spiel und ist ab jetzt dein direkter Draht.
>
> Kurz zu {user_mention}:
> {digest}
>
> Der Kanal hier gehört euch. Macht doch direkt mal eine Runde zusammen aus. Ich zieh mich zurück, wenn ihr mich braucht, bin ich per DM da.

T4 Match-DM an den Neuling (`{pate_name}`, `{channel_mention}`):
`Gute Nachrichten: {pate_name} übernimmt deine Patenschaft. Ich hab euch
einen eigenen Kanal eingerichtet: {channel_mention}. Schau rein, ihr
könnt direkt loslegen.`

T5 Reply auf den Claim-Post (`{pate_mention}`): `Erledigt, {pate_mention}
übernimmt. Danke dir!`

T6 System-Prompt-Ergänzung (als zusätzliche Regel-Zeile an den
bestehenden SYSTEM_PROMPT anhängen, JSON-Vertrag entsprechend um das
Feld ergänzen): `Wenn der User sich einen Paten, Mentor oder eine feste
Bezugsperson wünscht, setze "pate_request": true. Setze es nicht, wenn
er nur wissen will, was ein Pate ist.`

T6b (Antwort, wenn pate_request true und reply leer):
`Klingt, als würde dir ein fester Ansprechpartner guttun. Soll ich einen
unserer Paten für dich suchen?`

T7 Steam-Nudge:
- Titel: `Dein Rang gehört auf den Server`
- Beschreibung: `Schön, dass du so oft in unseren Voice-Lanes bist. Ein
  Tipp von mir: Verknüpf einmal kurz deinen Steam-Account, dann bekommst
  du deinen Deadlock-Rang als Rolle, wirst in der Spielersuche richtig
  einsortiert und dein Live-Status in den Lanes stimmt. Dauert keine
  Minute, der Knopf unten bringt dich direkt hin. Und wenn du dabei
  Fragen hast, schreib mir einfach, ich bin per DM da.`

T8 Voice-Feedback (`{name}` ersetzen):
- first: `Hey {name}, schön, dass du bei uns in den Voice-Lanes warst.
  Wie waren deine ersten Runden? Wenn du zwei Minuten hast, erzähl mir
  kurz, was gut lief und wo es gehakt hat. Das landet direkt bei den
  Leuten, die den Server bauen.`
- second: `Hey {name}, danke, dass du wieder in den Lanes warst. Magst
  du mir kurz erzählen, wie es diesmal war? Dein Eindruck hilft uns mehr
  als jede Statistik.`
- ACK: `Danke dir, ist angekommen und wird weitergegeben. Wenn dir sonst
  noch was auffällt, schreib mir jederzeit.`
- ALREADY: `Du hast mir dazu schon geantwortet, alles gut. Danke dir!`
- EXPIRED: `Das Fenster für dieses Feedback ist leider schon zu. Wenn du
  mir trotzdem was mitgeben willst, schreib einfach los, ich lese alles.`

T9 Gedächtnis-Marker:
- Steam-Nudge: `[Ich habe dir eine DM mit dem Tipp zur
  Steam-Verknüpfung geschickt.]`
- Feedback: `[Ich habe dich per DM nach Feedback zu deinen Voice-Runden
  gefragt.]`

Formregel wie im Textpaket: Doku-Zeilenumbrüche mitten im Satz werden im
Code zu Leerzeichen, nur bewusste Absätze bleiben `\n\n`.

## Env / Betrieb

- `DL_CONCIERGE_PATE_CHANNEL_ID=1524083665838276860` (Kanal
  #paten-zentrale, nur Paten-Rolle sieht ihn)
- `DL_CONCIERGE_PATE_CATEGORY_ID=1465839366634209361` (Kategorie „Neue
  Spieler" für die privaten Paten-Kanäle), Fallback bleibt
  `fallback_category_id`.
- Beide werden beim Deploy ins (gitignorte) Startskript eingetragen.

## Tests (Vertrag zuerst)

- Claim-Reihenfolge: ohne Rolle T2a; zweiter Klick T2b; Pate mit 3
  aktiven Patenschaften T2c und die Patenschaft bleibt vergebbar.
- Match legt genau eine aktive Patenschaft pro User an (Unique-Index),
  Journey `pate_matched` wird emittiert.
- Rang-Empfehlung: nächster Rang-Index gewinnt; Pate am Limit wird
  übersprungen; ohne Daten T1b.
- pate_request=true hängt Buttons an; false nicht.
- record_system_dm legt Profil an und schreibt assistant-Turn.
- Bestehende 88 dl-community-Tests bleiben grün.
