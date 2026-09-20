# Deadlock-Docs

Zentrales Wissens-Repo für die Deutsche Deadlock Community. Es bündelt das geprüfte Wissen zu Community und Discord, Steam-Bot, Twitch-Bot, Patchnotes, Turnieren und Website-Portalen.

## Struktur

- `public/`: öffentliches, redigiertes Supportwissen für Mitglieder.
- `internal/`: Entwicklungs-, Betriebs- und Produktwissen für Menschen mit internem Zugriff.
- `evals/`: sechs geprüfte Fragenpakete mit insgesamt 224 realistischen Supportfragen.
- `quellen.json`: bindet jede interne Seite an die Quell-Repos und Pfade, aus denen sie geschrieben wurde, samt geprüftem Commit.

Alle Wissensseiten unter `public/` und `internal/` sind kanonisches, semantisches HTML. Root-Dateien wie README, Plan und Changelog bleiben Markdown und werden nie indexiert.

## Öffentliche Laufzeit

`public/` und `internal/` bleiben strikt getrennt. Der laufende Wissensdienst erhält ausschließlich den aktuell freigegebenen Teil des committeten `public/`-Baums. Historische Analysen und fachlich entwertete Seiten bleiben im Redaktionsexport erhalten, werden aber außerhalb des aktiven Suchbestands archiviert. `internal/` wird weder exportiert noch vom Support-Agenten indexiert; einen internen Index oder einen Admin-Wissenszugang gibt es in diesem Release nicht.

Der Support-Agent beantwortet belegte Fragen in Direktnachrichten, privaten FAQ-Chats und im Bereich für Serverfragen. Tickets bleiben menschlicher Support: Eine erzeugte Kandidatenantwort erscheint nur in einem internen Prüfbereich und nie direkt im Ticket. Fehlt eine sichere öffentliche Antwort, führt der Weg zum Menschen-Support.

Der Agent fragt keinen aktuellen Dienststatus ab und startet aufgrund einer Nutzerfrage keinen Auto-Debug, keinen Neustart, keinen Befehl und keine andere Aktion.

## Pflege und Prüfung

- Öffentliche Seiten enthalten nur beobachtbares Verhalten, sichtbare Mitgliedswege und sichere nächste Schritte.
- Jede Seite erfüllt den HTML-Vertrag mit Titel, Metadaten, genau einem Hauptbereich und genau einer Hauptüberschrift.
- Der Korpus-Validator prüft Struktur, Links, Trennung und öffentliche Redaction.
- Deployment und Reload verwenden nur committete, validierte Inhalte; der Arbeitsbaum ist kein Produktionskorpus.

### Öffentliche Quellen und fachliche Gültigkeit

`public-sources.json` legt pro Repository die normale Git-Referenz und die positiv belegten öffentlichen Quellen fest. Unbekannte Zielgruppen werden nicht automatisch öffentlich. Explizite interne oder private Kennzeichnungen überstimmen eine ältere Freigabe. Die redigierten HTML-Dateien sind eigenständige, versionierte Redaktion: Ein Refresh überschreibt sie nicht mit Rohtexten aus anderen Repos.

Die Prüfberichte unter `berichte/*-pruefung.json` binden jede freigegebene Seite an ihren Inhalts-Hash, den tatsächlichen Prüfzeitpunkt und relevante Codepfade samt Revision. Quellenentzug, geänderter Inhalt oder geänderter Fachcode entziehen die Freigabe im nächsten Export. Eine weiterhin richtige bedingte Erklärung kann gesonderte offene Produktabweichungen benennen; diese sind nicht mit einer fehlenden Fachprüfung gleichzusetzen.

Der eigene `public-corpus-refresh.timer` prüft alle 15 Minuten und nach jedem Docs-Deployment explizit. Er verwendet `ops/public-corpus-refresh.json`, friert sämtliche Quellrevisionen vor der Prüfung ein und benötigt weder Modellaufrufe noch neue Konfigurationsvariablen. Unveränderte Quellen führen zu keinem neuen Indexaufbau. Der interne Frischebericht hat einen getrennten Zweck und bleibt unabhängig.

```bash
bash tools/deploy_corpus.sh --config ops/public-corpus-refresh.json
python3 tools/refresh_public_corpus.py --config ops/public-corpus-refresh.json --prepare-only
```

Ein vollständiger Redaktionsexport wird zuerst einschließlich seiner Links geprüft. Im daraus gefilterten Suchbestand dürfen Linkziele fehlen, wenn sie selbst nicht mehr als Antwortquelle zugelassen sind; Pfadflucht, aktive Inhalte und interne Referenzen bleiben verboten. Der Leser lädt öffentliche HTML-Dateien und das daraus geprüfte FAQ-Manifest gemeinsam. Erst wenn `/healthz` sowohl `generation` als auch `faq_generation` bestätigt, meldet `status-summary.json` den neuen Snapshot als aktiv. Fehler erhalten den alten bestätigten Stand oder kennzeichnen eine nicht bestätigbare Aktivierung ausdrücklich.

Der Adminstatus unterscheidet geprüfte Quellen, ausstehende Prüfungen, historische Inhalte und ausgeschlossene Repositories. Die Größe des Obsidian-Graphen ist kein Maß für die Antwortabdeckung. Aktuelle Spieldaten kommen zusätzlich aus Deadlock Brain; historische Buildanalysen werden nicht als aktuelle Spielberatung ausgegeben.

### Frische der internen Seiten

Interne Seiten beschreiben Code, der weiterläuft, während die Seite stillsteht. `tools/check_freshness.py` macht diesen Abstand sichtbar: Es liest `quellen.json`, fragt jedes gebundene Quell-Repo, was sich seit dem geprüften Commit in den gebundenen Pfaden geändert hat, und schreibt das Ergebnis nach `berichte/frische.md`.

```bash
python3 tools/check_freshness.py --schreiben   # Bericht erneuern
python3 tools/check_freshness.py --json        # maschinenlesbar
python3 tools/check_freshness.py --strict      # Exit 1, sobald eine Seite veraltet ist
```

Die Quell-Repos werden unter `$DL_REPO_HOME` gesucht, standardmäßig im Elternverzeichnis dieses Repos. Der Lauf ist rein lesend.

Pflege-Vertrag:

- Wer eine interne Seite überarbeitet, setzt `geprueft` des zugehörigen Eintrags auf den dann aktuellen Commit des Quell-Repos und trägt bei der Gelegenheit die genauen Pfade nach.
- Wer eine interne Seite anlegt, legt den Eintrag in `quellen.json` mit an. Ohne Eintrag schlägt der Lauf fehl, auch ohne `--strict`; eine unverfolgte Seite veraltet sonst unbemerkt.
- `veraltet` heißt ungeprüft, nicht falsch. Grob gebundene Seiten liefern Obergrenzen, genau gebundene liefern Befunde.

Website-FAQ und Twitch-In-App sind mögliche spätere Konsumenten desselben öffentlichen Wissensdienstes.
