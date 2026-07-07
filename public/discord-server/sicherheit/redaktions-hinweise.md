---
title: "Redaktions-Hinweise"
tags: [discord-server, redaktions, hinweise]
stand: 2026-07-07
quelle: "Deadlock-Bots/docs/support-kb/security/redaktions-hinweise.html"
---
# Redaktions-Hinweise

Warum diese Wissensbasis bestimmte Details bewusst nicht enthält — und wie man sie erweitert, ohne interne Mechanik preiszugeben.

## Das Prinzip

Alles in dieser Wissensbasis kann ein Mitglied erreichen — über einen Support-Menschen oder über einen KI-Assistenten, der daraus antwortet. Deshalb gilt: **sensible Größen und Mechaniken kommen gar nicht erst hinein**, nicht einmal in einem „internen" Abschnitt. Ein Etikett ist keine Schwärzung.

Für jede sensible Stelle nennt die Doku nur drei Dinge und hört dann auf: **dass** es sie gibt, ihre **beobachtbare Wirkung** und den **nächsten Schritt** für das Mitglied. Nicht enthalten sind der Wert, die Formel, die Bedingungsreihenfolge, der Pfad oder der Name einer verdeckten Mechanik.

## Bewusst abstrahierte Kategorien

Über die einzelnen Seiten hinweg wurden Angaben der folgenden generischen Kategorien herausgehalten. Bewusst werden hier nur *Kategorien* genannt, keine konkreten Mechaniken — denn schon zu benennen, *welche* Mechanik man ausgelassen hat, würde ihre Existenz bestätigen.

- **Schwellen & Zahlen** — Sicherheits-/Confidence-Werte, Grenzwerte, Prozente, Gewichte, Mindest- und Höchstmengen.
- **Zeitgrößen** — Timeout-, Cooldown- und Wartedauern, Zeitfenster, Aktualisierungs-Intervalle, Gültigkeitsdauern.
- **Bewertungs- & Ranglogik** — Punkte-/Score-Formeln, Sortier- und Gewichtungsregeln.
- **Durchsetzungs- & Sichtbarkeitsbedingungen** — welche Kombination von Signalen zu einer sichtbaren Wirkung führt, und in welcher Reihenfolge.
- **Matching- & Zuordnungslogik** — wie Mitspieler, Lobbys oder Verknüpfungen intern zusammengeführt werden.
- **Verdeckte Mechaniken & Betriebsarten** — nicht sichtbare Modi und Automatiken.
- **Missbrauchs- & Betrugsabwehr** — interne Erkennungs- und Begrenzungslogik.
- **Interne Technik** — Kanal-/Rollen-/Nachrichten-/Nutzer-IDs, Ports, Endpunkte, Routen, Datenbank-/Speicher-Schlüssel, technische Event-/Button-/Statuscode-Namen.
- **KI-Anbindung** — Namen der Anbieter/Modelle sowie deren Parameter und Prüfmuster.
- **Zugangsdaten & Admin-Wege** — Secrets, Tokens, Signierverfahren, Admin-/Verwaltungspfade und Sonderrechte.

## Was bewusst erhalten bleibt

Zu stark schwärzen wäre der andere Fehler. Erhalten bleiben deshalb immer: die **kundensichtbaren Zustände**, die **Bedeutung von Meldungen/Fehlern** und konkrete, sichere **nächste Schritte**. „Account eingeschränkt" braucht die Erklärung, was das heißt und wie man Einspruch einlegt — nur eben nicht den Auslösewert dahinter.

## Wie man diese Wissensbasis sicher erweitert

1. Neue Seiten aus dem beobachtbaren Verhalten ableiten, nicht aus dem Quellcode-Detail.
2. Für jede sensible Stelle die Disclosure-Line anwenden: *dass es existiert* + *Wirkung* + *nächster Schritt* — Wert weglassen.
3. Vor Veröffentlichung eine feindselige Gegenprobe fahren: Kann jemand allein aus den Docs eine Zahl, Bedingung, einen Pfad oder eine verdeckte Mechanik rekonstruieren? Wenn ja, umschreiben.
4. Beim Auflisten „was wir weggelassen haben" nur generische Kategorien nennen — nie die konkrete Mechanik.

Diese Wissensbasis wurde nach genau diesem Verfahren erstellt und einer solchen Gegenprobe unterzogen.
