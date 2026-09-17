# deadlock-brain: Retrieval und lokale Embeddings

Interne Referenz für KI-Support-Agenten und FAQ-Redaktion. Sie beschreibt den untersuchten Quellcode, keinen nachgewiesenen Live-Betrieb. Die Python-Quellen liegen unter `/home/nathanael/repos/Deadlock-Brain/src/deadlock_brain/`. Zeilennummern beziehen sich auf den untersuchten Stand und können sich bei Änderungen verschieben.

## 1. Kernantwort: Das Embedding wird lokal berechnet

**`get_embedding()` verwendet keine externe Embedding-API. Die Berechnung erfolgt lokal im Python-Prozess mit `sentence_transformers.SentenceTransformer` und dem Modell `all-MiniLM-L6-v2`.**

Fundstellen in `retrieval.py`:

- Zeile 17: globaler Modellcache `_embedding_model`, zunächst `None`.
- Zeilen 19 bis 24: `_get_embedding_model()` importiert `SentenceTransformer` erst bei Bedarf und initialisiert einmal `SentenceTransformer('all-MiniLM-L6-v2')`.
- Zeilen 26 bis 28: `get_embedding(text)` ruft `model.encode(text).tolist()` auf und liefert eine Liste von Fließkommazahlen.
- Zeile 34: `search_mechanic_notes()` erzeugt damit das Query-Embedding.

Der Code legt weder Gerät noch Modellrevision, Cachepfad oder einen ausschließlich lokalen Ladebetrieb fest. **Lokale Inferenz bedeutet deshalb nicht garantiert netzfreier Erststart:** Sind Modellartefakte nicht vorhanden, kann die Bibliothek sie beim Laden herunterladen. Der konkrete Download- und Cachezustand wurde nicht geprüft. Das ist von einem externen Dienst zur Berechnung der Query-Embeddings zu unterscheiden.

Die Antwortgenerierung ist ein separater Pfad: `brain_pipeline.py` baut eine Chat-Anfrage und ruft `call_minimax_chat()` auf (Zeilen 176 bis 196). Aus lokalen Embeddings darf daher nicht abgeleitet werden, dass die gesamte Fragebeantwortung lokal bleibt. Die Implementierung und Netzwerkkonfiguration des MiniMax-Clients waren nicht Gegenstand dieser Prüfung.

## 2. Rolle bei Deadlock-Spielfragen

`deadlock-brain` verbindet strukturierte Spieldaten, Patch-Ereignisse und Mechaniknotizen mit einer nachgelagerten Antwortgenerierung. Der Einstieg `ask()` lässt eine Frage durch `analyze_query()` planen, baut Kontext und erzeugt daraus eine Antwort. Zurückgegeben werden unter anderem Plan, Kontextübersicht, Antwort und Modellkennung (`brain_pipeline.py`, Zeilen 22 bis 46).

Der Kontextaufbau unterscheidet unter anderem Heldenübersicht, Build-Empfehlung, Itemfrage, Mechanikfrage, Patch-Änderungen und Heldenvergleich. Helden und Patches verwenden `build_review_context()`, Builds und Items zunächst spezialisierte Kontextfunktionen. Optional werden vorhandene Offline-Analysen ergänzt (`brain_pipeline.py`, Zeilen 49 bis 150).

Für Support und FAQ sind zwei verschiedene Suchwege wichtig:

1. **Entitätskontext:** deterministische Namens- und Aliasauflösung mit strukturierten Patch- und Statistikdaten, ohne Embeddings.
2. **Mechaniknotizen:** semantische Suche mit lokalem Query-Embedding und SQLite-Vektordistanzen, mit eingeschränktem Text-Fallback.

Es handelt sich in `retrieval.py` nicht um eine gemeinsame Hybrid-Rangliste aller Helden, Items, Patches und Mechaniken.

## 3. Retrieval-Pfad von der Frage zum Kontext

### 3.1 Planung und Auswahl in der Pipeline

`ask()` übergibt die Frage an `analyze_query(query, conn, config)`. `_build_context()` verwendet danach `plan.intent`, `plan.entities` und `plan.raw_query` zur Auswahl des Kontextpfads (`brain_pipeline.py`, Zeilen 22 bis 25, 49 bis 107).

Die interne Erkennung von Intent und Entitäten in `query_planner.py` wurde nicht untersucht. Ebenso wurde die interne Weiterleitung innerhalb von `build_review_context()` nicht geprüft. Belegt sind dessen Aufrufstellen in der Pipeline und die nachfolgend separat beschriebene Schnittstelle `build_entity_context()` in `retrieval.py`, nicht eine hier vollständig verifizierte Aufrufkette zwischen beiden.

**Wichtige Grenze:** Wenn `plan.entities` leer ist, setzt die Pipeline lediglich den Hinweis „Keine spezifischen Entitäten erkannt.“. Wegen des vorgeschalteten `if not entities` wird dann auch bei einer Mechanikfrage der spätere Mechanikzweig nicht ausgeführt (`brain_pipeline.py`, Zeilen 55 bis 57, 73 bis 81).

### 3.2 Entitäten, Aliase, Patch-Ereignisse und Statistiken

`build_entity_context(conn, query, limit_events=30)` arbeitet entitätsorientiert, nicht als belegte Extraktion beliebiger Entitäten aus einer vollständigen Frage (`retrieval.py`, Zeilen 67 bis 103):

1. Eingabe trimmen und mit `normalize_alias()` normalisieren. Das Ereignislimit wird auf 1 bis 500 begrenzt.
2. `_find_best_entity_match()` durchsucht `entities` und `entity_aliases`. Es bewertet den gesamten übergebenen Suchtext, nicht einzelne aus einer Frage extrahierte Wörter.
3. Bei einem Treffer bis zu 80 Aliase laden. Zusätzlich werden verwandte und historische Namen über die importierten Lineage- und Legacy-Funktionen abgefragt. Deren interne Regeln wurden nicht untersucht.
4. Passende `patch_events` laden, optional Anreicherungen und Statistikdaten ergänzen.
5. Ein Wörterbuch mit `query`, `query_norm`, `best_match`, `aliases`, `lineage`, `patch_events`, `enrichments`, `sheet_stats` und `fallback` zurückgeben.

**Entitätsbewertung:** Ein exakter kanonischer Name ohne Beachtung der Großschreibung erhält 120 Punkte, ein exakter normalisierter kanonischer Alias 115, ein anderer exakter normalisierter Alias 110. Teiltreffer erhalten 80 beziehungsweise 70 Punkte. Die Mindestpunktzahl ist 100, daher reichen reine Teiltreffer nicht für `best_match`. Es wird höchstens eine Entität gewählt (`retrieval.py`, Zeile 15, Zeilen 106 bis 165).

**Patch-Auswahl:** Mit einem Entitätstreffer werden kanonischer Name, geeignete Aliase und historische Namen für einen Namensvergleich verwendet. Ohne Treffer werden historische Namen, soweit vorhanden, mit `entity_name LIKE` kombiniert; sonst bleibt nur `entity_name LIKE`. Zunächst werden höchstens 500 Zeilen nach Snapshot und Zeilenposition geladen. Danach sortiert Python diese Kandidaten absteigend nach Datum, Snapshot und Zeilenposition und kürzt auf das angeforderte Limit (`retrieval.py`, Zeilen 193 bis 269, 451 bis 478).

**Zusatzdaten:** `patch_event_enrichments` wird, falls vorhanden, über Ereignis-ID oder Hash abgefragt. Statistikdaten stammen aus passenden `entity_snapshots` und zusätzlich aus dynamisch erkannten Tabellen mit „sheet“ oder „stat“ im Namen. Pro Statistikquelle werden höchstens fünf Zeilen geladen (`retrieval.py`, Zeile 14, Zeilen 272 bis 403).

### 3.3 Semantische Suche nach Mechaniknotizen

`search_mechanic_notes(conn, query, limit=5)` verwendet diesen Ablauf (`retrieval.py`, Zeilen 30 bis 65):

1. Existenz von **beiden** Tabellen `mechanic_notes` und `vector_embeddings` prüfen. Fehlt eine, sofort `[]` zurückgeben.
2. Query lokal mit `get_embedding()` einbetten.
3. Den Vektor als JSON-Liste an SQLite übergeben.
4. `vector_embeddings` mit `mechanic_notes` über `mn.rowid = ve.rowid` verbinden.
5. `vec_distance_L2(ve.embedding, ?)` berechnen, aufsteigend nach Distanz sortieren und auf das Limit kürzen.
6. `id`, `title`, `content`, `source`, `category` und `distance` zurückgeben.

Es gibt hier keine zusätzliche Relevanzschwelle, keinen BM25-Anteil und keine Rangfusion. Ein Treffer mit kleiner Distanz ist nicht automatisch ein ausreichender Beleg für eine fachliche Aussage.

**Fallback-Grenzen:** Nur Fehler innerhalb des Vektor-SQL- und Ergebnisblocks lösen die Suche mit `title LIKE ? OR content LIKE ?` aus. Dabei wird der gesamte Querytext als Teilzeichenfolge gesucht, ohne eigenes Ranking; die Rückgabedistanz ist pauschal `0.0` und kein semantischer Messwert. Fehlende Tabellen, leere Vektorergebnisse oder Fehler beim Modellladen und Einbetten lösen diesen Fallback nicht aus. Das Embedding wird vor dem `try` berechnet. Die Pipeline fängt Fehler des Mechanikzweigs anschließend ohne Fehlermeldung ab (`retrieval.py`, Zeilen 31 bis 65; `brain_pipeline.py`, Zeilen 73 bis 81).

## 4. Speicherung und Voraussetzungen

`BrainStore` öffnet eine lokale SQLite-Datei am übergebenen `db_path`, verwendet `sqlite3.Row` und aktiviert WAL sowie Fremdschlüssel. Rohdaten erhalten ein separates `raw_dir`. Ein konkreter produktiver Datenbankpfad ist in diesem Konstruktor nicht festgelegt (`storage.py`, Zeilen 21 bis 32).

| Tabelle oder Store | Funktion und Fundstelle |
|---|---|
| `entities`, `entity_aliases` | Kanonische Entitäten und normalisierte Aliase. Schema: `storage.py`, Zeilen 118 bis 151. |
| `patch_events` | Einzelne Patch-Änderungen mit Namen, Werten, Datum, Quellenangaben und Ereignishash. Schema: `storage.py`, Zeilen 83 bis 116. |
| `entity_snapshots` | Versionierte Datenstände mit JSON-Nutzdaten und Verweis auf ein Quelldokument. Schema: `storage.py`, Zeilen 57 bis 72. Statistikabruf: `retrieval.py`, Zeilen 319 bis 342. |
| `source_documents`, `source_runs` | Herkunft, Rohdatenpfade und Importläufe. Schema: `storage.py`, Zeilen 40 bis 55, 74 bis 81. Kein direkter Abruf durch `build_entity_context()`. |
| `mechanic_notes` | Titel, Inhalt, Quelle, Kategorie, explizite `rowid`-Spalte und Erstellungszeit. Titel ist eindeutig. Schema: `storage.py`, Zeilen 167 bis 176. |
| `vector_embeddings` | Virtuelle SQLite-Tabelle mit `vec0`, Spalte `embedding float[384]`. Schema: `storage.py`, Zeilen 163 bis 165. Kein externer Vektorstore in diesem Pfad. |
| Optionale Kontexttabellen | `patch_event_enrichments` sowie erkannte Statistiktabellen. Abruf: `retrieval.py`, Zeilen 272 bis 403. |

`BrainStore.migrate()` lädt die Erweiterung über `import sqlite_vec` und `sqlite_vec.load(self.conn)`. Schlägt der Block fehl, wird im Fehlerzweig nur `mechanic_notes` angelegt (`storage.py`, Zeilen 155 bis 195). Fehlt anschließend `vector_embeddings`, liefert die Mechaniksuche bereits vor ihrem Text-Fallback keine Ergebnisse.

Die Verbindung zwischen Notiz und Vektor erfolgt über die explizite `mechanic_notes.rowid`-Spalte, nicht über `mechanic_notes.id`. Das gezeigte Schema deklariert dafür keinen Fremdschlüssel. **Der Schreib- beziehungsweise Indexierungspfad für Mechaniknotizen und Dokument-Embeddings ist in den untersuchten Kernstellen nicht belegt.** Daraus lässt sich weder eine befüllte Vektortabelle noch die Verwendung desselben Modells beim Indexaufbau ableiten.

Zusätzlicher Paketbefund: In `/home/nathanael/repos/Deadlock-Brain/pyproject.toml`, Zeilen 10 bis 13, sind nur `faster-whisper` und `yt-dlp` als Projektabhängigkeiten eingetragen. `sentence-transformers` und `sqlite-vec` sind dort nicht deklariert. Ob sie anderweitig installiert werden oder in der Laufzeitumgebung vorhanden sind, bleibt offen.

## 5. Bezug zum geplanten Hybrid-Ausbau von dl-knowledge

Die interne Referenz [dl-knowledge: Wissensdienst für KI-Support und FAQ](dl-knowledge-engine.md), insbesondere Abschnitte 3 bis 5, beschreibt BM25-Retrieval ohne Dense-Kanal und nennt Hybrid-Fusion als Ausbauziel. Das ist hier eine Kontextreferenz, keine erneute Prüfung des Rust-Codes.

**Wiederverwendbar für lokale Query-Embeddings:**

- Das Muster aus `_get_embedding_model()` und `get_embedding()`: Modell erst bei Bedarf laden, innerhalb des Prozesses wiederverwenden und Text lokal in einen Zahlenvektor umwandeln (`retrieval.py`, Zeilen 17 bis 28).
- `all-MiniLM-L6-v2` als bereits im Brain-Code konkret verwendeter Modellkandidat. Seine Eignung für deutsche Supportfragen ist dadurch noch nicht nachgewiesen.
- Das lokale Speicherprinzip mit SQLite und `sqlite-vec` als mögliche Option, sofern es zur Zielarchitektur passt. Die vorhandene Tabelle ist auf Mechaniknotizen und 384 Dimensionen zugeschnitten, nicht auf die Chunks von dl-knowledge (`storage.py`, Zeilen 163 bis 176).

**Noch zu entwerfen und zu prüfen, nicht bereits implementiert:**

- Integration des Python-Encoders in den Rust-Dienst, etwa über einen lokalen Prozess oder Dienst, oder eine kompatible lokale Inferenzimplementierung.
- Aufbau und Aktualisierung eines Dense-Index für die dl-knowledge-Chunks. Query- und Dokument-Embeddings benötigen denselben Modellstand und kompatible Vorverarbeitung, Dimension und Distanzmetrik. Die reine Query-Funktion ersetzt keinen Indexierungsprozess.
- Zusammenführung der BM25- und Dense-Ergebnisse, optionales Reranking sowie Bewertung von Antwortqualität, Laufzeit und Speicherbedarf. Die beiden getrennten Brain-Pfade liefern keine fertige Hybrid-Fusion.
- Zusammenspiel mit der bestehenden lexikalischen Belegprüfung und dem Ablehnungsverhalten von dl-knowledge. Rein semantische Treffer dürfen nicht ungeprüft die Quellenbindung umgehen.
- Wahrung der Korpusgrenzen: Die Wiederverwendung eines lokalen Encoders ist keine Freigabe, interne Brain-Daten oder diese interne Dokumentation in einen öffentlichen Antwortkorpus zu übernehmen.

## 6. Offene Punkte und FAQ-Kurzantwort

Nicht geprüft wurden ein Live-Datenbankbestand, erfolgreiche Vektorsuchen, Modellverfügbarkeit, Paketinstallation, Indexbefüllung, Antwortqualität und die vollständigen internen Aufrufketten von Query-Planer und Review-Kontext. Es wurden keine Modelle geladen und keine Live-Anfragen oder Funktionstests ausgeführt.

**FAQ: Werden Embeddings über eine externe API berechnet?**

Nein, im untersuchten Retrieval-Code berechnet `sentence_transformers.SentenceTransformer('all-MiniLM-L6-v2')` die Embeddings lokal mit `model.encode(text)`. Die entscheidenden Fundstellen sind `retrieval.py`, Zeilen 19 bis 28. Ein möglicher Download des Modells und der separate MiniMax-Chatpfad sind davon zu unterscheiden.
