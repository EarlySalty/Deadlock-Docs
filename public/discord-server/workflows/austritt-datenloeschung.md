---
title: "Austritt & Datenlöschung"
tags: [discord-server, austritt, datenloeschung]
stand: 2026-07-07
quelle: "Deadlock-Bots/docs/support-kb/workflows/austritt-datenloeschung.html"
---
# Austritt & Datenlöschung

Rund um einen Austritt gibt es drei Dinge, die ein Mitglied merkt: eine optionale Austritts-Umfrage per persönlichem Link, gelegentliche Reaktivierungs-Erinnerungen an länger inaktive Mitglieder und die Möglichkeit, alle eigenen Daten löschen zu lassen.

## Was Mitglieder merken

Wer länger inaktiv ist, kann automatisch eine persönliche Direktnachricht mit einem Hinweis auf Server und Voice-Kanäle bekommen; solche Erinnerungen lassen sich abbestellen. Wer den Server verlässt, kann eine kurze Austritts-Umfrage per persönlichem Link erhalten und dort einen Grund angeben sowie optional Bilder anhängen; das Ausfüllen ist freiwillig. Auf Wunsch (Löschanfrage bzw. Opt-out) werden alle nutzerbezogenen Daten hart gelöscht; danach bleiben Community-Funktionen gesperrt, bis das Mitglied aktiv wieder zustimmt.

## Ablauf Schritt für Schritt

1. Reaktivierung: Länger inaktive Mitglieder erhalten eine persönliche Erinnerungs-DM mit Server- und Voice-Links; wer das nicht möchte, kann sich per Opt-out abmelden.
2. Austritt: Wer den Server verlässt, kann eine persönliche Umfrage-DM erhalten (gebannte Mitglieder bekommen keine).
3. Umfrage ausfüllen: Über den persönlichen Link öffnet sich ein Formular mit Anzeigename und Austrittsgrund; Antworten ausfüllen und optional einige Bilder anhängen.
4. Absenden: Die Einsendung wird einmalig gespeichert; bereits abgeschickte oder abgelaufene Umfragen werden abgewiesen.
5. Datenlöschung: Auf Löschanfrage bzw. Opt-out werden alle nutzerbezogenen Daten hart gelöscht; ein Opt-out-Vermerk bleibt bestehen.
6. Nach der Löschung bleiben Community-Funktionen gesperrt, bis das Mitglied aktiv wieder zustimmt (Opt-in).

## Mögliche Ausgänge

- Umfrage erfolgreich gespeichert
- Umfrage abgewiesen bei bereits erfolgter Einsendung oder ungültigem/abgelaufenem Link
- Bild-Upload abgelehnt bei zu vielen, zu großen oder falsch formatierten Bildern
- Daten gelöscht und Opt-out aktiv

## Sichtbare Zustände

| Zustand | Was du siehst | Was es bedeutet | Sicherer nächster Schritt |
| --- | --- | --- | --- |
| Reaktivierungs-Erinnerung erhalten | Persönliche Direktnachricht mit Hinweis auf Server und Voice-Kanäle | Das Mitglied wurde als länger inaktiv eingestuft und bekommt eine Rückhol-Nachricht | Ignorieren oder wieder aktiv werden; die Nachricht lässt sich per Opt-out abbestellen |
| Austritts-Umfrage per DM erhalten | Direktnachricht mit kurzer Umfrage bzw. Feedback-Link nach dem Verlassen | Beim Verlassen wurde eine freiwillige Feedback-Anfrage ausgelöst | Optional beantworten; die Nachricht kann auch einfach ignoriert werden |
| Austritts-Umfrage offen | Der persönliche Link zeigt ein Formular mit Anzeigename, Grund und Feldern zum Ausfüllen | Der Link ist gültig und die Umfrage wurde noch nicht abgeschickt | Antworten ausfüllen, optional Bilder anhängen und absenden |
| Umfrage bereits abgesendet | Meldung, dass die Umfrage schon abgeschickt wurde | Es ist bereits eine Einsendung gespeichert; eine zweite ist nicht möglich | Keine Aktion nötig; bei Korrekturbedarf das Team kontaktieren |
| Umfrage-Link ungültig oder abgelaufen | Fehlermeldung, dass der Link nicht gefunden wurde | Der Link ist unbekannt, unvollständig oder zu alt | Prüfen, ob der Link vollständig kopiert wurde; sonst ist er abgelaufen und lässt sich nicht erneuern |
| Bild-Upload abgelehnt | Fehlermeldung zu zu vielen oder zu großen Bildern bzw. falschem Bildtyp | Die Grenzen für Anzahl, Größe oder Format der Bilder wurden überschritten | Weniger oder kleinere Bilder in einem gängigen Bildformat (JPG/PNG/WebP/GIF) anhängen |
| Daten gelöscht | Bestätigung der Löschung; künftig gilt ein Opt-out | Alle nutzerbezogenen Daten wurden hart gelöscht, ein Opt-out-Vermerk bleibt bestehen | Nichts weiter nötig; ein erneutes Mitmachen ist nur durch aktives Opt-in möglich |

## Typische Meldungen & Fehler

| Signal | Was es bedeutet | Nächster Schritt |
| --- | --- | --- |
| Umfrage-Link wird nicht angenommen | Der Link ist ungültig, unvollständig oder abgelaufen | Link vollständig aus der Discord-DM kopieren; abgelaufene Links lassen sich nicht neu ausstellen |
| Umfrage lässt sich nicht erneut abschicken | Die Austritts-Umfrage wurde bereits abgeschickt | Keine erneute Einsendung möglich; bei Bedarf das Team kontaktieren |
| Zu viele oder zu große Bilder | Die Anzahl oder Dateigröße der angehängten Bilder ist zu hoch | Anzahl und Dateigröße der Bilder reduzieren und erneut absenden |
| Bildformat wird abgelehnt | Ein angehängtes Bild hat ein nicht unterstütztes Format bzw. das Formular wurde nicht korrekt gesendet | Nur JPG/PNG/WebP/GIF anhängen und das Formular normal absenden |
| Community-Funktionen sind gesperrt | Es ist ein Datenschutz-Opt-out gesetzt, daher sind Funktionen gesperrt | Ein aktives Opt-in ist nötig, um Community-Funktionen wieder zu nutzen |

### Das darf der Support sagen

- Die Austritts-Umfrage ist freiwillig; du kannst die DM auch einfach ignorieren, ohne Nachteile.
- Reaktivierungs-Erinnerungen kannst du per Opt-out abbestellen, wenn du keine solchen Nachrichten mehr möchtest.
- Wenn dein Umfrage-Link nicht funktioniert, prüfe bitte, ob er vollständig kopiert wurde; abgelaufene Links lassen sich nicht erneuern.
- Auf Wunsch löschen wir alle deine Daten; danach bleiben Community-Funktionen gesperrt, bis du aktiv wieder zustimmst.

### Nie an Mitglieder weitergeben

- Interne Zahlen jeder Art: Schwellen, Sicherheitswerte, Gewichte, Zeitgrenzen, Limits.
- Die interne Entscheidungs- oder Durchsetzungslogik — welche Signale zu welcher Wirkung führen und in welcher Reihenfolge.
- Interne Technik: IDs, Pfade, Endpunkte, Namespaces, KI-Anbieter oder -Modelle, Zugangsdaten.
- Verdeckte Mechaniken oder Betriebsarten — auch nicht andeutungsweise, welche es geben könnte.
- Im Zweifel abstrahieren und an einen Menschen eskalieren (Details im Agenten-Leitfaden).

## Verwandte Seiten

- [Dashboard & Login](../module/dashboard-login.md)

**Bewusst nicht dokumentiert:** Schwellenwerte und Zeitgrenzen, Durchsetzungsbedingungen, verdeckte Mechaniken, interne Endpunkte, Zugangsdaten. Diese internen Details bleiben aus Sicherheitsgründen außerhalb dieser Wissensbasis.
