# Golden-Set-Erweiterung

Stand: 2026-09-18.

Der bestehende Golden-Stand mit 224 Fällen wurde um 30 synthetisch aus dem öffentlichen Korpus abgeleitete Fälle erweitert. Die sechs vorhandenen JSON-Dateien bleiben die einzigen Golden-Dateien; jede erhielt fünf neue Fälle.

| Kategorie | Umsetzung |
|---|---|
| Paraphrasen | alternative alltagssprachliche Formulierungen vorhandener Fragen |
| Tippfehler | gezielte Schreibfehler wie „Twtich“, „Deadlok“ oder „geeh“ |
| Englisch | englische Varianten belegter Fragen |
| Fehlercodes | synthetische Codes in Fragen, deren sichere Hilfe weiterhin aus dem Korpus stammt |
| Unbeantwortbar | Fragen nach internen Status- oder Fehlercode-Details ohne Korpusbeleg |

Alle neuen Fälle tragen `"herkunft": "synthetisch"`. Es wurden keine Concierge-Fragen oder sonstige Community-Daten gelesen.

Neuer Umfang: **254 Fälle**, davon **30 synthetisch**. Insgesamt sind **18 Fälle bewusst unbeantwortbar**.

Paket D akzeptiert zukünftige Erweiterungen ab 224 Fällen, verlangt aber weiterhin exakt die sechs bekannten Golden-Dateien, eindeutige Fragen und für jede erwartete Quelle eine vorhandene öffentliche HTML-Datei.
