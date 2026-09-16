# Concierge: DM-Frontend vor dl-knowledge

Interne Referenz zum Frage-Antwort-Pfad des Concierge. Quelle: `/home/nathanael/repos/Deadlock-Bots/rust/crates/dl-community/src/concierge.rs` (untersuchte Datei: 14255 Zeilen) und `/home/nathanael/repos/Deadlock-Bots/rust/crates/dl-community/src/knowledge_client.rs` (595 Zeilen). Zeilenangaben beziehen sich auf den Stand dieser Prüfung und können sich verschieben. Die Doku beschreibt den Code, nicht einen geprüften Live-Betrieb.

## 1. Rolle des Concierge

Der Concierge ist die erste Anlaufstelle für neue Mitglieder im deutschen Deadlock-Discord-Server (System-Prompt, Zeilen 235 bis 253). Er nimmt direkte Nachrichten und öffentliche Serverfragen entgegen, entscheidet über die Antwortroute und benutzt die Wissensbasis dl-knowledge als einzigen Faktenpfad. Der Code nennt das explizit: „Der Wissensdienst ist der EINZIGE Faktenpfad des Concierge" (Kommentar vor `answer_decision`, Zeilen um 4385 bis 4392). Reine Wissenslücken dürfen nicht mehr generisch in ein anderes Brain fallen, sondern landen in der sicheren Wissenslücke (Kommentar bei Tests zu `!brain`, Zeilen um 560 bis 580 der Testmodule, siehe auch `KNOWLEDGE_GAP_TEXT`, Zeile 137).

Rollenverteilung:

- **Concierge (dl-community)**: DM-Frontend. Gesprächsverlauf, Datenschutz-Opt-out, Vergessen, Cooldowns, Persona-LLM, Unsicherheitskommunikation und Persistenz liegen hier.
- **dl-knowledge** (Port 8896, `/public/v1/ask`): belegt-geprüfte Faktenantworten. Der Server liefert `answerable`, `answer` und `sources` oder stur Abstain. Details in `dl-knowledge-engine.md`.
- **LLM (dl_ai)**: formuliert die Persona-Antwort im Free-Voice-Modus auf Basis des Wissenskontexts, darf aber nichts erfinden (`ANTI_INVENT_RULE`, Zeile 143).

Neben dem Wissenspfad gibt es lokale Kurzantworten ohne Wissensabruf: Bot-Identität, Link-only, Smalltalk, Favoriten, Offtopic und expliziter Patenwunsch (`local_conversational_answer`, Zeilen um 5470 bis 5510). Sie greifen vor dem Wissensdienst.

## 2. Wie eine Nutzerfrage entgegengenommen und beantwortet wird

### 2.1 Eingang: `handle_user_message`

- `handle_user_message` (Zeilen 3606 bis 3616) nimmt pro User einen `tokio::sync::Mutex`-Lock (`user_action_lock`) und ruft `handle_user_message_inner` (Zeilen 3834 bis 3899).
- Zugangsfilter: `config.user_allowed(user_id)` (Zeile 3837). Ohne Berechtigung passiert nichts.
- Kanalklassen (Zeilen 3838 bis 3846): direkte DM (`guild_id.is_none()`) oder öffentlicher Support im Hauptserver nur im Kanal `SERVER_BOT_FRAGEN_CHANNEL_ID` (Konstante Zeile 74). Andere Guild-Kanäle werden über `effective_guild_id` (Zeilen um 3910) abgelehnt, außer es ist ein verifizierter privater Fallback-Kanal des Nutzers.
- DM-Kontrollbefehle: In DMs prüft `handle_dm_control` (Zeilen 3679 bis 3730) zuerst `forget_intent` und `optout_intent`. „vergiss mich" löscht den Zustand, „stopp" setzt den globalen Opt-out. Beide enden vor dem Wissenspfad.
- `!brain`-Präfix: `parse_brain_command` (Zeilen um 5960) entfernt ein exakt vorangestelltes `!brain` nur bei Wissensfragen. Damit kann der Präfix nie eine Kontroll-direktive wie „stopp" auslösen (Kommentar Zeilen 3850 bis 3852).
- Öffentliche Support-Fragen: flüchtiger Cooldown im Prozess (maximal 3 Aufrufe pro 60-Sekunden-Fenster, mindestens 10 Sekunden Abstand, `check_cooldown` Zeilen 34 bis 55), dann `acquire_stateful_support_turn` (Semaphore mit vier Plätzen, `knowledge_client.rs` Zeilen 20 bis 45) und zustandslose Antwort `send_stateless_reply` (Zeilen 3892 bis 3898).
- DMs laufen in `answer_dm_question_inner` (Zeilen 3893 bis 3899) mit `allow_personal_actions: is_direct_dm` und Route `Concierge`.

### 2.2 Stateful DM-Zug: `answer_dm_question_inner`

`answer_dm_question_inner` (Zeilen 3909 bis 4210) ist der zentrale Pfad für DM-Antworten:

1. Datenschutz prüfen: `begin_privacy_action` hält ein Lock auf `user_privacy`. Mit aktivem Opt-out wird der Zug zustandslos (`PrivacyStateless`) und ohne Speichern beantwortet.
2. Frage speichern: `record_conversation_tx` legt die User-Nachricht in `bot.concierge_conversations` ab; Intent wird per Stichwort gesetzt (`classify_intent`).
3. Cooldown prüfen: bei Treffer kommt `COOLDOWN_TEXT` (Zeile 144).
4. Verlauf laden: die letzten fünf User-Fragen (`recent_user_questions_tx`) und die letzten zwölf Gesprächsnachrichten mit Rollen (`recent_conversation_messages_tx`).
5. Entscheidung: `answer_decision` (Zeilen um 4380 bis 4545).
6. Antwort speichern und senden: die Assistant-Antwort wird in denselben Transaktionskontext geschrieben, danach per `port.send_channel_v2` an Discord gesendet und die Transaktion committet. Der Zustellaufruf hat ein Zeitlimit von `CONCIERGE_DISCORD_IO_TIMEOUT` (3 Sekunden, Zeile 66).

### 2.3 Entscheidung: `answer_decision`

`answer_decision` (Zeilen um 4380 bis 4545) arbeitet in Stufen:

1. **Lokale Kurzantworten**: `local_conversational_answer` trifft bei Identität, Link-only, Smalltalk, Favoriten, Offtopic oder Patenwunsch ohne Wissensabruf.
2. **Retrievalfrage bauen**: Für zuständige Züge kombiniert `knowledge_question_from_user_history` (Zeilen 1175 bis 1190) die letzten vier früheren User-Fragen mit der aktuellen Frage, getrennt durch Zeilenumbrüche. Nur User-Nachrichten kommen hinein, keine Assistant-Antworten (Test ab Zeile 7950).
3. **Wissensabruf**: `knowledge_client::ask(&self.config.knowledge_url, &retrieval_question, KNOWLEDGE_TIMEOUT)` (Zeilen 4415 bis 4428). `KNOWLEDGE_TIMEOUT` ist 8 Sekunden (Zeile 65, Test Zeile 7197).
4. **Auswertung** (Zeilen 4428 bis 4440):
   - `KnowledgeLookup::Answer` → bereinigter Antworttext, Ergebnis `Answered`.
   - `Unanswerable` → kein Text, Ergebnis `NoAnswer`.
   - `Timeout` → Ergebnis `Timeout`.
   - `Transport` oder `InvalidResponse` → Ergebnis `Error`.
5. **Free-Voice-Modus** (Standard, `free_voice: true`):
   - Mit Wissenstext wird `Wissenskontext aus dl-knowledge:\n{answer}` als zusätzliches Systemnachrichtenfeld an das LLM gegeben (Zeilen 4457 bis 4461). Das LLM formuliert die Antwort in der Concierge-Persona als JSON (`parse_llm_answer`, Zeilen um 6000 bis 6040).
   - Ohne Wissenstext bekommt das LLM `GAP_GUIDANCE` (Zeile 138): keine Serverfakten erfinden, Gesprächs- und Geschmacksfragen normal beantworten, Faktenfragen mit dem Verweis-Satz `KNOWLEDGE_GAP_TEXT` beantworten.
   - LLM-Fehler oder -Timeout mit vorhandenem Wissenstext liefern den Wissensfakt wortgetreu (`llm_error_verbatim`); ohne Wissenstext die `KNOWLEDGE_GAP_TEXT`-Lücke (`llm_error_gap`, Zeilen 4475 bis 4535).
6. **Free Voice aus**: Die Wissensantwort geht wortgetreu raus (`knowledge_llm`), sonst `KNOWLEDGE_GAP_TEXT` (`gap_llm`, Zeilen 4443 bis 4460). In diesem Modus ruft der Concierge kein LLM.
7. **Geduldshinweis**: `llm_answer_with_patience` (Zeilen 4550 bis 4580) schickt nach `AI_GEDULD_HINWEIS_NACH` (15 Sekunden, Zeile 92) einmal `AI_GEDULD_TEXT` (Zeile 142) in denselben Kanal, ohne den Zug zu beenden. Zustellfehler beim Hinweis bleiben folgenlos.

Das LLM-Antwortschema verlangt `{"reply": "...", "intent": "...", "pate_request": false}` (Zeilen um 5915 bis 5925). Ein Kaputt-JSON wird nie roh ausgeliefert: Parse-Fehlschlag führt zu `KNOWLEDGE_GAP_TEXT` (Test `kaputtes_llm_json_wird_nie_roh_ausgeliefert`, Zeilen um 10360).

## 3. Berührung mit dl-knowledge: HTTP-Client

Der Concierge spricht dl-knowledge ausschließlich über `knowledge_client.rs` an:

- **Endpunkt**: `POST {knowledge_url}/public/v1/ask` mit JSON-Body `{"question": "..."}`. Base-URL ist `DEFAULT_KNOWLEDGE_URL` = `http://127.0.0.1:8896` (concierge.rs Zeile 60, `knowledge_url` in `ConciergeConfig` Zeile 265). Ein Env-Override `DL_KNOWLEDGE_URL` wird in der Produktionskonfiguration bewusst ignoriert, `from_env` setzt immer den Default (Zeilen 296 bis 300, Test Zeilen 7417 bis 7423).
- **Härtung des Clients** (knowledge_client.rs, `ask`, Zeilen 176 bis 315):
  - Nur Loopback-Ziele erlaubt (localhost oder Loopback-IP), sonst `InvalidResponse` mit Grund `invalid_target`, ohne Request.
  - `no_proxy()`: Loopback-Anfragen umgehen Systemproxies (Test `loopback_anfrage_ignoriert_systemproxy`).
  - Keine Redirect-Folge (`Policy::none`), Query und Fragment werden entfernt.
  - Zeitlimit 8 Sekunden, vom Aufrufer als `KNOWLEDGE_TIMEOUT` übergeben.
  - Timeout → `Timeout`, sonstiger Transportfehler → `Transport`, HTTP-Status ungleich 2xx → `Transport`.
- **Antwortobjekt**: `KnowledgeAnswer { answerable, answer: Option<String>, sources: Vec<KnowledgeSource> }` mit `KnowledgeSource { title, path }` (Zeilen 60 bis 72).
- **Validierung** (Zeilen 280 bis 315): `answerable: true` zählt nur mit nichtleerem Antworttext, mindestens einer Quelle und ausschließlich sicheren Quellenpfaden (`safe_source_path`, Zeilen 84 bis 105): relativer Pfad, Endung `.html`, keine Steuerzeichen, keine `..`- oder `internal`-Segmente. Verletzt → `InvalidResponse`. `answerable: false` → `Unanswerable`.
- **Decision-Log**: Jeder Ausgang schreibt eine strukturierte Zeile `dl-community knowledge-client decision` mit `verdict`, `confidence`, `reason`, `sources`, `error_class` und nur der Fragenlänge, nie dem Frageninhalt (`logged_lookup`, Zeilen 107 bis 140).
- **Zugangs-Semaphore**: `acquire_stateful_support_turn` begrenzt alle DB-stateful Support-Züge (Concierge-DM, öffentlicher Support, Steckbrief) auf vier gleichzeitige Plätze (Zeilen 20 bis 45).

## 4. Unsicherheit und Abstain gegenüber dem Nutzer

### 4.1 Unsicherheits-Hinweistext

`send_answer_uncertain_notice_inner` (Zeilen 4770 bis 4795) sendet `ANSWER_UNCERTAIN_TEXT` (Zeile 140): „Die Antwort von eben steht vielleicht noch oben im Verlauf, verlass dich aber nicht drauf. ..." Es wird gesendet, wenn:

- die Antwortzustellung fehlschlägt oder das 3-Sekunden-Zeitlimit überschreitet (stateful und stateless Pfade, Zeilen 4199 bis 4210, 4651 bis 4675),
- der Commit der Antwort-Transaktion unsicher bleibt, ohne die sichtbare Antwort destruktiv zu entfernen (Zeilen 4212 bis 4225, Test `zentrale_antwort_bleibt_bei_commit_unsicherheit_sichtbar_und_warnt`, Zeilen um 10880),
- Kontroll- oder interne Fehlerzüge scheitern (`send_control_reply_inner`, `send_internal_error_reply_inner`).

Im Onboarding-Tour-Pfad (Route `OnboardingTour`, `answer_tour_dm_question_inner`, Zeilen 3630 bis 3677) ersetzt der Unsicherheitshinweis die Antwort und behält die Tour-Buttons.

### 4.2 Abstain aus der Wissensbasis

Ein Wissens-Abstain (`answerable: false`) ist kein technischer Fehler, sondern ein normales Ergebnis: Ergebnis `NoAnswer`, Quelle `gap_llm`, dem Nutzer geht `KNOWLEDGE_GAP_TEXT` („Da will ich dir nichts Falsches erzählen. Stell die Frage am besten in <#1491953161747955853> ...") oder im Free-Voice-Modus eine gemäß GAP_GUIDANCE formulierte Antwort raus. Der Abstain wird nicht als Unsicherheitshinweis dargestellt und nicht persistiert.

### 4.3 Ergebnis-Klassen

`ConciergeAnswerOutcome` (Zeilen um 3140 bis 3160) unterscheidet `Answered`, `NoAnswer`, `PrivacyStateless`, `Uncertain`, `Timeout`, `Error`. Jeder Zug wird strukturiert geloggt (`log_answer_decision`, Zeilen um 5985 bis 6000).

### 4.4 Fail-closed-Persistenz

Neben der Antwortkommunikation persistiert der Concierge Unklarheiten zustandstreu und ehrlich:

- **Kontrollbefehle**: Opt-out und Vergessen bestätigen nur den Erfolg (`OPTOUT_TEXT`/`FORGET_TEXT`). Bei Persistenzfehler kommt `OPTOUT_PERSIST_ERROR_TEXT` beziehungsweise `FORGET_PERSIST_ERROR_TEXT`, keine falsche Zusage (`optout_reply_text` und `forget_reply_text`, Zeilen um 1830 bis 1845).
- **Unsicher-Marker mit Readback**: `persist_t0_uncertain` (Zeilen 2989), `persist_pate_request_uncertain` (Zeilen 3071), `persist_pate_claim_uncertain` (Zeilen 3167) und `persist_cadence_uncertain` (Zeilen 3277) schreiben nach fehlgeschlagenem Commit (bis zu zwei Versuche) einen KV-Claim oder Profilmarker und verifizieren den Zustand per Readback-Query. Gelingt auch das nicht, wird der Fehler geloggt und es erfolgt keine Zustellwiederholung.
- **Steckbrief-Widerruf**: `persist_steckbrief_revocation` sperrt nach unsicherer Zustellung jeden Neustart-Retry.

Diese Marker betreffen die Onboarding- und Patenpfade; der reine Q&A-Pfad persistiert Unsicherheit nur über den sichtbaren Hinweis und den Journey-/Log-Eintrag.

## 5. Relevante Konfiguration (`ConciergeConfig`, Zeilen 255 bis 340)

| Feld | Bedeutung | Quelle |
|---|---|---|
| `knowledge_url` | Base-URL des Wissensdienstes, fest auf `http://127.0.0.1:8896` | Zeilen 265, 296 bis 300 |
| `model` | Optionales LLM-Modell via `DL_CONCIERGE_MODEL` | Zeilen 301 bis 304 |
| `ai_timeout` | Notbremse für den LLM-Aufruf, Default 100 s, Deckel 110 s, via `DL_CONCIERGE_AI_TIMEOUT_SECS` | Zeilen 79 bis 100, 306 bis 311 |
| `free_voice` | Persona-LLM an (Default) oder Fixtexte, via `CONCIERGE_FREE_VOICE` | Zeilen 312 bis 313 |
| `proactive` | Proaktive DMs, Default aus (siehe unten) | Zeilen 314 bis 320 |
| `test_user_allowlist` | Leere Liste = offener Modus | Zeilen 277, 327 bis 329 |
| `fallback_category_id` | Kategorie für private Fallback-Kanäle | Zeilen 276, 325 bis 326 |

Hinweis: `from_env` setzt `knowledge_url` bewusst ohne Env-Override, damit ein Test- oder Env-Wert die Produktions-Loopback-URL nicht ersetzt (Test Zeilen 7417 bis 7423). Zeitlimits: `KNOWLEDGE_TIMEOUT` 8 s (Zeile 65), Discord-I/O 3 s (Zeilen 66 bis 69), LLM 100 s (Zeile 86), Geduldshinweis nach 15 s (Zeile 92).

## 6. Quellreferenzen

Alle Angaben: `concierge.rs` (C) beziehungsweise `knowledge_client.rs` (K) im Crate `dl-community/src`.

| Thema | Referenz |
|---|---|
| Rate-Limit/Cooldown | C Zeilen 34 bis 55, 140 bis 144 |
| `DEFAULT_KNOWLEDGE_URL` | C Zeile 60 |
| Zeitlimits (Knowledge 8 s, Discord 3 s, LLM 100 s, Geduld 15 s) | C Zeilen 65 bis 100 |
| `ANSWER_UNCERTAIN_TEXT`, `KNOWLEDGE_GAP_TEXT`, `GAP_GUIDANCE`, `AI_GEDULD_TEXT` | C Zeilen 140, 137, 138, 142 |
| `ANTI_INVENT_RULE`, `PATE_REQUEST_RULE` | C Zeilen 143 bis 144 |
| System-Prompt der Persona | C Zeilen 235 bis 253 |
| `ConciergeConfig`, `from_env` | C Zeilen 255 bis 340 |
| `ConciergeAnswerOutcome` | C Zeilen 3140 bis 3160 |
| `persist_t0_uncertain` | C Zeilen 2989 ff. |
| `persist_pate_request_uncertain` | C Zeilen 3071 ff. |
| `persist_pate_claim_uncertain` | C Zeilen 3167 ff. |
| `persist_cadence_uncertain` | C Zeilen 3277 ff. |
| `handle_user_message` / `_inner` | C Zeilen 3606 bis 3616, 3834 bis 3899 |
| `answer_tour_dm_question_inner` | C Zeilen 3630 bis 3677 |
| `handle_dm_control` | C Zeilen 3679 bis 3730 |
| `answer_dm_question_inner` | C Zeilen 3909 bis 4210 |
| `answer_decision` (Wissensabruf, LLM-Pfade) | C Zeilen 4380 bis 4545 |
| `llm_answer_with_patience`, `send_patience_notice` | C Zeilen 4550 bis 4620 |
| `send_answer_uncertain_notice_inner` | C Zeilen 4770 bis 4795 |
| `knowledge_question_from_user_history` | C Zeilen 1175 bis 1190 |
| `local_conversational_answer`, Identitätserkennung | C Zeilen 5470 ff., 5590 ff. |
| `parse_llm_answer`, `llm_system` | C Zeilen 5915 ff., 6000 ff. |
| 4-Slot-Semaphore | K Zeilen 20 bis 45 |
| `KnowledgeAnswer`/`KnowledgeSource` | K Zeilen 60 bis 72 |
| `safe_source_path`, Quellenvalidierung | K Zeilen 84 bis 105, 280 bis 315 |
| `logged_lookup` (Decision-Log ohne Frageinhalt) | K Zeilen 107 bis 140 |
| `ask` (POST `/public/v1/ask`, Loopback-only, no_proxy, kein Redirect) | K Zeilen 176 bis 315 |

## 7. Offene Punkte

- Die konkrete Bereitstellung des dl-knowledge-Dienstes (Startart, Überwachung, Portkonflikt-Verhalten) ist in diesen beiden Dateien nicht belegt; siehe `dl-knowledge-engine.md` Abschnitt 5.
- `acquire_stateful_support_turn` begrenzt die vier DB-stateful Pfade (Concierge-DM, öffentlicher Support, Steckbrief-Post, Steckbrief-Entwurf). Ob das weitere stateful-Zugriffe in anderen Crates umfasst, wurde hier nicht geprüft.
- Der Concierge kennt keine Quellenanzeige an den Nutzer: `KnowledgeSource` wird nur für das Decision-Log genutzt, nicht in der Discord-Antwort ausgegeben. Eine Nutzeranzeige von Quellen ist im Code nicht vorhanden.
