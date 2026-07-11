# Deadlock-Docs

Zentrales Wissens-Repo für die Deutsche Deadlock Community. Es bündelt das geprüfte Wissen zu Community und Discord, Steam-Bot, Twitch-Bot, Patchnotes, Turnieren und Website-Portalen.

## Struktur

- `public/`: öffentliches, redigiertes Supportwissen für Mitglieder.
- `internal/`: Entwicklungs-, Betriebs- und Produktwissen für Menschen mit internem Zugriff.
- `evals/`: sechs geprüfte Fragenpakete mit insgesamt 224 realistischen Supportfragen.

Alle Wissensseiten unter `public/` und `internal/` sind kanonisches, semantisches HTML. Root-Dateien wie README, Plan und Changelog bleiben Markdown und werden nie indexiert.

## Öffentliche Laufzeit

`public/` und `internal/` bleiben strikt getrennt. Der laufende Wissensdienst erhält ausschließlich ein validiertes Abbild des committeten `public/`-Baums: Der Export legt einen versionierten Snapshot ab und schaltet `current` erst nach erfolgreicher Prüfung um. `internal/` wird weder exportiert noch vom Support-Agenten indexiert; einen internen Index oder einen Admin-Wissenszugang gibt es in diesem Release nicht.

Der Support-Agent beantwortet belegte Fragen in Direktnachrichten, privaten FAQ-Chats und im Bereich für Serverfragen. Tickets bleiben menschlicher Support: Eine erzeugte Kandidatenantwort erscheint nur in einem internen Prüfbereich und nie direkt im Ticket. Fehlt eine sichere öffentliche Antwort, führt der Weg zum Menschen-Support.

Der Agent fragt keinen aktuellen Dienststatus ab und startet aufgrund einer Nutzerfrage keinen Auto-Debug, keinen Neustart, keinen Befehl und keine andere Aktion.

## Pflege und Prüfung

- Öffentliche Seiten enthalten nur beobachtbares Verhalten, sichtbare Mitgliedswege und sichere nächste Schritte.
- Jede Seite erfüllt den HTML-Vertrag mit Titel, Metadaten, genau einem Hauptbereich und genau einer Hauptüberschrift.
- Der Korpus-Validator prüft Struktur, Links, Trennung und öffentliche Redaction.
- Deployment und Reload verwenden nur committete, validierte Inhalte; der Arbeitsbaum ist kein Produktionskorpus.

Website-FAQ und Twitch-In-App sind mögliche spätere Konsumenten desselben öffentlichen Wissensdienstes.
