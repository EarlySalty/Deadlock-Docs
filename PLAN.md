# Plan: Deadlock-Supportwissen

Stand: 2026-07-11

## Ziel

Ein gemeinsamer Support-Agent beantwortet öffentlich belegte Fragen zu Community und Discord, Steam-Bot, Twitch-Bot, Patchnotes, Turnieren und Website-Portalen. Private Daten, nicht öffentliche Arbeitsbereiche und technische Betriebsdetails bleiben außerhalb seiner Wissensquelle.

## Aktueller Stand

- Alle Wissensseiten unter `public/` und `internal/` sind semantisches HTML; Root-Dokumente und Entwicklungspläne bleiben Markdown und werden nie indexiert.
- Öffentliche und interne Inhalte sind physisch getrennt. Das Laufzeit-Artefakt enthält ausschließlich den committeten `public/`-Baum als validierten Snapshot unter `current`.
- Der Support-Agent verwendet keinen internen Index; ein Admin-Wissenszugang ist nicht Teil dieses Releases.
- Der gebaute Antwortweg deckt Direktnachrichten, private FAQ-Chats und Serverfragen ab. Bei fehlender oder unsicherer Beleglage verweist er an den Menschen-Support.
- Tickets bleiben menschlicher Support. Eine Kandidatenantwort wird nur im internen Prüfbereich gezeigt und nie direkt in das Ticket geschrieben.
- Sechs Eval-Pakete prüfen 224 eindeutige Goldenfragen über alle sechs Produktgruppen, einschließlich dynamischer Fragen, Datenschutzgrenzen und Prompt-Injection.

## Entscheidungen

- Öffentliches Wissen beschreibt nur sichtbares Verhalten, Zugangsgrenzen und sichere nächste Schritte. `internal/` wird nicht durch Antwortregeln verborgen, sondern fehlt vollständig im Laufzeit-Artefakt.
- Aktuelle Preise, Termine, Patches, Empfehlungen und Dienstverfügbarkeit werden nicht erfunden. Die Antwort führt zur jeweils sichtbaren aktuellen Oberfläche oder zum Menschen-Support.
- Eine Nutzerfrage löst keine Live-Status-Abfrage, keinen Auto-Debug, keinen Neustart, keine Befehlsausführung und keine andere Aktion aus.
- Der öffentliche Fragenpfad verwendet ausschließlich das geprüfte Supportwissen; andere Wissenssysteme ersetzen keine fehlende Server- oder Bot-Quelle.
- Der laufende Snapshot stammt immer aus einem Commit. Ein fehlgeschlagener Export oder Reload ersetzt den zuletzt gültigen Stand nicht.

## Abgeschlossen

- Öffentliche und interne Wissensseiten auf den gemeinsamen HTML-Vertrag umgestellt.
- Öffentliche Inhalte redigiert, Produktgrenzen korrigiert und breite Navigation für alle sechs Produktgruppen ergänzt.
- Committeten `public/`-Export mit versionierten Snapshots und atomarem `current`-Wechsel abgesichert.
- Antwortwege und Sicherheitsgrenzen mit 224 realistischen Fragen und ihren erwarteten Quellen geprüft.
- Direkte Ticket-Antworten ausgeschlossen und Unsicherheit auf menschliche Prüfung geroutet.

## Release-Gate

Vor einer Freigabe müssen Korpus-Validator, vollständige Golden-Evaluation, Redaction-Review und die Live-Smokes für Direktnachricht, privaten FAQ-Chat, Serverfragen und Ticket-Trennung grün sein. Der Live-Zustand muss den committeten Snapshot verwenden und darf keine internen oder nicht-HTML-Quellen enthalten.

## Später

- Website-FAQ und Twitch-In-App können denselben öffentlichen Antwortdienst als weitere Konsumenten nutzen.
- Auto-Debug bleibt ein eigenes Folgeprojekt. Falls er später gebaut wird, arbeitet er nur lesend und über eine feste Freigabeliste, warnt deutlich bei möglicher Prompt-Injection und schreibt ausschließlich in einen internen Log- oder Prüfkanal; er erzeugt nie eine direkte Nutzerantwort.
