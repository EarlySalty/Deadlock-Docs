# dl-knowledge: Wissensdienst für KI-Support und FAQ (Pilot)

Interne Referenz zum Rust-Dienst `dl-knowledge`. Quelle: `/home/nathanael/repos/Deadlock-Bots/rust/bin/dl-knowledge/src/main.rs` (untersuchte Datei: 4383 Zeilen). Alle Zeilenangaben beziehen sich auf diese Datei und können sich bei Codeänderungen verschieben. Die Beschreibung dokumentiert den Code, nicht einen geprüften Live-Betrieb.

## 1. Architektur-Überblick

`dl-knowledge` ist ein axum-HTTP-Dienst für Supportfragen der deutschen Deadlock-Community. Korpusladen, Chunking, BM25-Retrieval, Prompt-Aufbau und Belegprüfung sind in `main.rs` implementiert. Wichtig: Der Generator formuliert keine freie Antwort. Er wählt ausschließlich IDs vorhandener Passagen; der Server setzt daraus den Antworttext und die Quellen zusammen (Zeilen 22 bis 34, 892 bis 949).

Bestandteile:

- **Loopback-Server**, gebunden an `127.0.0.1:8896` (`BIND_ADDR`, Zeile 20, `main()` ab Zeile 675). Der Listener ist an die lokale IPv4-Loopback-Adresse gebunden. Ein möglicher Proxy oder externer Zugangsweg ist durch diese Datei nicht belegt.
- **Statische Routen** (`router()`, Zeile 723):
  - `GET /healthz`: Chunk- und Quellenzahlen (`health`, Zeile 731).
  - `POST /internal/reload`: lädt den Korpus neu, behält bei Fehlern den letzten gültigen Index (`reload`, Zeile 742).
  - `POST /public/v1/ask`: die eigentliche Frage-Antwort-Logik (`ask`, Zeile 760).
- **Korpus im Speicher**: `AppState` hält den Docs-Pfad, eine `RwLock<KnowledgeBase>` und einen optionalen Generator (Zeilen 50 bis 54).
- **Generator**: `FireworksClient` aus der Crate `dl_ai`, trait-gebunden als `Arc<dyn TextGenerator>`, Initialisierung über Umgebungsvariablen (Zeilen 689 bis 696). Ohne initialisierten Client endet auch eine Anfrage mit relevanten Kandidaten ohne Antwort (Zeilen 800 bis 810). Der Handler ruft den Generator höchstens einmal auf; ein Wiederholungsversuch ist dort nicht implementiert.
- **Retrieval**: reiner BM25-Index über alle Chunks, ohne Dense-Vektoranteil (`Bm25Index`, ab Zeile 609).

Parameter (Zeilen 36 bis 38): Modell-Timeout 7 Sekunden, maximal 4 ausgewählte Kandidaten, maximale Antwortlänge 1800 UTF-16-Einheiten.

## 2. Datenfluss einer Frage

Ablauf im `ask`-Handler (Zeilen 760 bis 890):

1. **Frage annehmen**: JSON-Body `{"question": "..."}` (`AskRequest`, Zeile 622).
2. **Retrieval**: `knowledge.search(question, 6)` sucht im bereits beim Start oder Reload aufgebauten Korpus. `expand_query` ergänzt fest hinterlegte Teilstring-Aliase (Roh-Teilstring per `contains`, nicht über Tokens), beispielsweise für kompakte Bot-Namen, sowie eine Sonderregel für Fragen zum Deadlock-Rang. Diese Rang-Sonderregel greift nicht, wenn die Frage `twitch` enthält oder ein isoliertes `!rank` vorkommt. Ergänzte Begriffe werden dedupliziert; explizite Wiederholungen der Rohfrage bleiben erhalten. Danach folgt BM25 (`KnowledgeBase::search` und `expand_query`, Zeilen 1759 bis 1847).
3. **Erste Abstain-Prüfung**: Ein leeres Retrieval-Ergebnis beendet den Handler sofort mit `answerable: false`, Grund `no_retrieval` im Decision-Log (Zeilen 765 bis 768). Der Generator wird in diesem Fall nicht gerufen.
4. **Kandidaten bauen**: Aus höchstens sechs gefundenen Chunks werden Passagen-Kandidaten mit IDs `P1`, `P2`, ... gebildet. Die Reihenfolge folgt dem Chunk-Rang und innerhalb eines Chunks der Passagenreihenfolge. Sechs Chunks sind nicht gleich sechs Passagen (`candidates_for`, Zeilen 1070 bis 1086).
5. **Grounding-Filter**: `candidate_is_relevant` prüft die ursprüngliche Frage, nicht die alias-erweiterte, rein lexikalische Suchanfrage. Die nichtleere Schnittmenge aus Fragebegriffen und übergeordnetem Chunk-Text muss vollständig in der gerenderten Passage vorkommen. Bei Absätzen müssen alle diese Begriffe im eigentlichen Text stehen; bei Listen und Tabellen darf Überschrift oder Tabellenkopf Kontext liefern, mindestens ein Fragebegriff muss aber im eigentlichen Text vorkommen. Nur bestimmte orthografische Kompaktformen werden zusätzlich zerlegt (`candidate_is_relevant`, `grounding_terms`, Zeilen 951 bis 1001).
6. **Weitere Abstain-Prüfungen**: Fehlen Passagen ganz (`no_candidates`) oder nach der Relevanzprüfung (`no_relevant_candidates`), endet die Anfrage ebenfalls ohne Generatoraufruf (Zeilen 773 bis 799).
7. **Generator-Aufruf**: Frage und Kandidaten werden als JSON-Daten serialisiert (`build_prompt`, Zeilen 1088 bis 1102). Der System-Prompt verlangt ausschließlich Kandidaten-IDs; das Antwortschema erlaubt keine zusätzlichen Felder (Zeilen 22 bis 34, 654 bis 658). Die JSON-Verpackung ist keine Garantie gegen Prompt-Injektion. Der Generator-Request setzt Zeitlimit sieben Sekunden, `max_output_tokens` 2000, `temperature` 0 und `reasoning_effort` none (`model` bleibt None). Das JSON der Antwort wird fail-closed nur getrimmt und geparst, ohne Markdown-Zäune zu entfernen; umgebender Text landet in `model_invalid_json`.
8. **Nachgelagerte Fail-Closed-Schritte**: leere Antwort, ungültiges JSON, leere ID-Liste (`model_rejected`) oder eine ungültige ID-Auswahl führen jeweils zu `answerable: false` (Zeilen 825 bis 878). `grounded_response` (Zeile 892) validiert die Auswahl vollständig (keine unbekannten, doppelten oder zu vielen IDs), rendert die gewählten Passagen serverseitig und lehnt Antworten über 1800 UTF-16-Einheiten ab.
9. **Antwort**: `AskResponse` mit `answerable`, `answer` und `sources` (Titel plus relativer Pfad, Zeilen 627 bis 637).
10. **Decision-Log**: Jeder Ausgang schreibt einen strukturierten Log-Eintrag ohne Fragen- oder Korpusinhalte (`log_decision`, Zeile 1003).

Der Abstain-Test „ohne BM25-Treffer ruft der Handler den Generator nicht“ liegt in der Testsuite unter `ask_handler_ohne_bm25_treffer_ruft_generator_nicht` (Zeile 4102) und prüft, dass die Generator-Aufrufzähler bei Null bleiben.

## 3. Korpus: Herkunft, Format, Chunking

- **Pfad**: `/home/naniadm/.local/share/dl-knowledge/current/public/` (`DEFAULT_DOCS_PATH`, Zeile 19). Produktiv sind CLI-Argument und `DL_DOCS_PATH`-Override verboten (`resolve_production_docs_path`, Zeile 711).
- **Laden und Format**: `load_corpus` sucht rekursiv Dateien mit der Endung `.html`, sortiert die Pfade und liest deren Inhalt. Nur wenn keine HTML-Dateien vorhanden sind, verwendet der allgemeine Lader `.md`. Der Produktionspfad kanonisiert zunächst den Root und lehnt anschließend leere Korpora sowie Nicht-HTML-Quellen ab. Der kanonische Root muss als letztes Segment `public` haben und darf kein Segment `internal` enthalten. Der Collector überspringt Unterverzeichnisse namens `internal` unabhängig von Groß- und Kleinschreibung und sammelt nur echte Dateien und Verzeichnisse (`is_file`/`is_dir`), wodurch Symlinks faktisch ausgelassen werden, ohne dass es dafür einen eigenen Symlink-Test gibt (Zeilen 1108 bis 1211).
- **Aktualisierung**: Beim Start und bei `POST /internal/reload` wird der Index vollständig neu aufgebaut. Erst ein erfolgreich geladener und validierter Korpus ersetzt den bisherigen Speicherbestand. Ein Reload-Fehler liefert HTTP 500 mit `reload_failed` und lässt den bisherigen Bestand erhalten (Zeilen 675 bis 709, 742 bis 758).
- **Pflicht-Metadaten** pro HTML-Datei (`parse_html_file`, ab Zeile 1213): genau ein `title`, genau ein `main` mit genau einem `h1` als direktes Kind, keine `script`-Tags in `main`, sowie die drei Meta-Felder `tags`, `stand` und `quelle`. Verstöße lassen den kompletten Ladevorgang fehlschlagen, nicht nur die Datei.
- **Chunking-Ebene**: Es entsteht ein Intro-Chunk aus den direkten `h1`- und `p`-Elementen von `main`, anschließend je ein Chunk für jedes direkte `section`-Kind. Der Abschnittsname kommt aus einem direkten, nichtleeren `h2`, ersatzweise aus der Abschnitts-ID. `Chunk` enthält `title`, `section`, den relativen `path`, `tags`, `text` und `passages` (Zeilen 553 bis 561, 1269 bis 1366). Es gibt keine gleitenden Textfenster oder überlappenden Chunks.
- **Passagen**: Direkte Absätze ergeben jeweils eine Passage; innerhalb eines Abschnitts ergeben direkte Listen jeweils eine Listenpassage und direkte Tabellen je Datenzeile eine Passage mit Tabellenkopf als Kontext. Intro-Passagen tragen das `h1`, Abschnittspassagen optional das `h2`. Nicht unterstützte direkte Elemente werden nicht als Antwortpassagen übernommen, ihr Text kann aber im vollständigen Abschnittstext für BM25 vorkommen. Ein Chunk kann auch keine Passagen enthalten. Jede gerenderte Passage einschließlich Überschrift und Kontext darf höchstens 1800 UTF-16-Einheiten umfassen; längere Passagen werden abgelehnt, nicht automatisch geteilt (Zeilen 1269 bis 1386).
- **Tabellen** sind strikt reguliert (`table_rows`, Zeile 1406): keine Verschachtelung, kein `rowspan`/`colspan`, Header nur aus nichtleeren `th`, Datenzeilen mit exakt passender `td`-Zahl.
- **Indizierung und Ranking**: `Bm25Index::new` verbindet Titel, Abschnittsname, Tags und Chunk-Text zu einem Suchtext. Pro Chunk speichert der Index Begriffshäufigkeiten und Länge, global Dokumenthäufigkeiten und Durchschnittslänge. Die Tokenisierung normalisiert Groß- und Kleinschreibung sowie Umlaute und ß für den Vergleich und entfernt Stopwörter und zu kurze Begriffe. BM25 bewertet alle Chunks mit `k1 = 1.5` und `b = 0.75`, summiert die Beiträge der Suchbegriffe und behält nur Scores über null. Sortiert wird absteigend nach Score, bei Gleichstand nach ursprünglichem Chunk-Index; anschließend wird auf das angeforderte Limit gekürzt (Zeilen 609 bis 620, 1849 bis 1968).

## 4. Abstain-Verhalten im Detail

Abstain bedeutet hier: keine Antwort ausgeben. Alle Ablehnungen im Handler verwenden `unanswerable()` und liefern denselben JSON-Inhalt: `{"answerable":false,"answer":null,"sources":[]}` (Zeilen 1028 bis 1034). Der konkrete Grund steht im Decision-Log, nicht im Antwortobjekt.

1. **Kein Retrieval-Treffer** (`no_retrieval`): Kein positiver BM25-Treffer, eine nach Verarbeitung leere Anfrage oder ein leerer Index liefern keine Ergebnisse. Der Generator wird nicht aufgerufen (Zeilen 765 bis 768, 1889 bis 1928).
2. **Keine verwendbaren Passagen** (`no_candidates`, `no_relevant_candidates`): Die gefundenen Chunks enthalten keine Passagen oder keine besteht die lexikalische Belegprüfung. Auch hier wird kein Generator aufgerufen (Zeilen 773 bis 799).
3. **Modell lehnt ab** (`model_rejected`): Eine leere ID-Liste führt zur Ablehnung (Zeilen 857 bis 868).
4. **Ungültige Auswahl** (`model_invalid_selection`): Unbekannte oder doppelte IDs, mehr als vier IDs, fehlende Relevanz oder eine zusammengesetzte Antwort über 1800 UTF-16-Einheiten verwerfen die gesamte Auswahl (Zeilen 869 bis 879, 892 bis 949).
5. **Technische Fehler** (`generator_missing`, `model_timeout`, `model_empty`, `model_invalid_json`): Ebenfalls keine Antwort. Fehlende Belege und technische Probleme sind deshalb allein anhand des Antwortobjekts nicht unterscheidbar (Zeilen 800 bis 856).

BM25 verwendet keine zusätzliche Mindestkonfidenz oberhalb von `score > 0`. Ein positiver Treffer garantiert weder eine verwendbare Passage noch eine Antwort. Der beste Retrieval-Score wird protokolliert, aber nicht als weitere Ablehnungsschwelle verwendet (Zeilen 770 bis 771, 1889 bis 1928).

Zusätzlich hält der System-Prompt (Zeilen 22 bis 34) das Modell an, bei fehlender Passage, reinen Injektionsversuchen, Aktionsaufforderungen und Fragen nach privaten oder internen Daten leer zu antworten.

## 5. Grenzen und Ziele des geplanten Hybrid-Ausbaus

Die folgenden Ausbauziele sind Empfehlungen, keine bereits implementierten Eigenschaften.

- **Kein Dense-Retrieval / Embedding**: Die Suche ist lexikalisch. Dense-Retrieval sollte passende Inhalte auch bei abweichenden Formulierungen und Synonymen finden, die die statische Query-Erweiterung nicht abdeckt (Zeilen 1759 bis 1968).
- **Keine Hybrid-Fusion**: Es gibt nur einen Retrieval-Kanal. Ein Ausbau müsste BM25- und Dense-Ergebnisse zusammenführen, damit exakte Begriffe und semantische Ähnlichkeit gemeinsam berücksichtigt werden.
- **Kein separater Reranker**: Aus höchstens sechs BM25-Chunks entstehen Passagen, die vor dem Prompt lexikalisch gefiltert werden. Ein Cross-Encoder oder anderer eigenständiger Reranker fehlt. Die vorhandene Modellwahl ist eine ID-Auswahl, keine neue Rangliste. Ein Reranker sollte passende Belege gegenüber bloß ähnlichen Treffern bevorzugen (Zeilen 760 bis 823, 892 bis 949).
- **Kein Version-Filter**: `stand` und `quelle` sind Pflicht-Metadaten, werden aber nicht im Chunk gespeichert oder für Versionsauswahl beziehungsweise Quellenantworten ausgewertet. Die Quellenantwort stammt aus Titel und relativem Dateipfad. Datumsgültigkeit und Aktualität werden nicht geprüft. Versionsfilter brauchen daher zusätzliche Metadatenverarbeitung; Dense und Reranker allein lösen diese Lücke nicht (Zeilen 553 bis 561, 1055 bis 1068, 1228 bis 1237, 1473 bis 1489).
- **Lexikalische Belegprüfung bleibt eine Grenze**: Rein semantisch gefundene Passagen können weiterhin an `candidate_is_relevant` scheitern. Für Hybrid muss das Zusammenspiel mit dieser Prüfung evaluiert werden, ohne die Quellenbindung oder das sichere Abstain-Verhalten aufzugeben (Zeilen 951 bis 1001).
- **Unterschiedliche Granularität**: BM25 bewertet Abschnitte, das Modell wählt Passagen. Relevante Passagen außerhalb der sechs besten Chunks werden nicht betrachtet. Auch die Grenzen von vier ausgewählten Passagen und 1800 UTF-16-Einheiten bleiben unabhängig vom Retrieval bestehen.

Offen außerhalb dieser Quellprüfung: Bereitstellung und tatsächlicher Inhalt des Produktionskorpus, externer Zugangsweg, konkret verwendetes Generatormodell und gemessene Antwortqualität. Der Handler setzt `model: None`; die konkrete Modellwahl ist hier nicht festgelegt (Zeile 817).

## 6. Test- und Evaluierungsinfrastruktur (Kurzüberblick)

- Die Datei enthält Tests für Parser, Chunking, BM25-Ranking, Grounding und Ablehnungspfade. Der Test ab Zeile 4102 prüft ausdrücklich, dass ohne BM25-Treffer kein Generatoraufruf erfolgt.
- Die Golden-Suite erwartet 224 Fälle in sechs JSON-Dateien (Zeilen 2006 bis 2014). `golden_retrieval_corpus` prüft den Korpus lokal; `golden_live_api` prüft einen laufenden Dienst. Beide sind standardmäßig ignoriert und benötigen externe Testdaten, der Live-Test zusätzlich eine API-Adresse (Zeilen 2289 bis 2291, 2376 bis 2378).
- Für diese Dokumentationsaufgabe wurden keine Rust-Tests oder Live-Anfragen ausgeführt. Ein erfolgreicher Testlauf oder messbarer Qualitätsgewinn des geplanten Hybrid-Ausbaus wird nicht behauptet.

## 7. Quellreferenzen

| Thema | Datei, Zeilen |
|---|---|
| Bind-Adresse 127.0.0.1:8896, Korpuspfad | `main.rs`, Zeilen 19 bis 20 |
| System-Prompt (ID-Auswahl-Vertrag) | Zeilen 22 bis 34 |
| Zeit-/Längen-Limits, Stopwörter | Zeilen 36 bis 47 |
| AppState, Routen, health, reload | Zeilen 50 bis 54, 723 bis 758 |
| Chunk/Passage/Candidate-Struktur | Zeilen 553 bis 601 |
| Bm25Index/IndexedDoc | Zeilen 609 bis 620 |
| Request/Response- und Prompt-Strukturen | Zeilen 622 bis 673 |
| main, Generator-Init | Zeilen 675 bis 709 |
| ask-Handler, Abstain-Logik | Zeilen 760 bis 890 |
| grounded_response, Grounding-Filter | Zeilen 892 bis 1001 |
| Decision-Log, unanswerable, Kandidaten-/Prompt-Bau | Zeilen 1003 bis 1104 |
| load_corpus, Produktionsvalidierung, Collector | Zeilen 1108 bis 1207 |
| parse_html_file (Chunking), Passage-Regeln | Zeilen 1213 bis 1404 |
| KnowledgeBase::search, Query-Expansion | Zeilen 1759 bis 1846 |
| Bm25Index::new und Ranking | Zeilen 1849 bis 1953 |
| Tokenizer, Umlaut-Normalisierung | Zeilen 1931 bis 1965 |
| Golden-Test-Infrastruktur | Zeilen 1976 bis 2430 |
| Abstain-Test ohne Generatoraufruf | Zeile 4102 |
