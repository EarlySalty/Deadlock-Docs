---
title: "Dashboard & Login"
tags: [discord-server, dashboard, login]
stand: 2026-07-07
quelle: "Deadlock-Bots/docs/support-kb/modules/dashboard-login.html"
---
# Dashboard & Login

Das Master-Dashboard ist der zentrale Login-Dienst und der Verwaltungs-/Auswertungsbereich des Servers; für Mitglieder ist der Großteil unsichtbar. Sichtbar werden nur wenige Dinge: Live-Zahlen und Patchnotes auf der Website, die Austritts-Umfrage, Reaktions-Rollen und eine mögliche Coaching-Sperre.

## Was Mitglieder merken

Die meisten Funktionen sind ein reines Cockpit für Team und Moderation und für Mitglieder nicht zu sehen. Vier Berührungspunkte gibt es aber: Auf der Community-Website erscheinen Live-Zahlen (Mitglieder, Online, Voice) und die Patchnotes aus diesem Dienst. Wer den Server verlässt, kann über einen persönlichen Link eine kurze Austritts-Umfrage ausfüllen und dabei Bilder anhängen. Reaktions-Rollen (per Emoji eine Rolle bekommen, teils mit einer Direktnachricht) werden hier eingerichtet. Und wer einen Coaching-Termin nicht wahrnimmt, kann für eine gewisse Zeit für weitere Buchungen gesperrt sein.

## Mögliche Ausgänge

- Austritts-Umfrage wird gespeichert.
- Eine zweite Einsendung wird abgewiesen.
- Ungültige oder abgelaufene Links werden abgewiesen.
- Bild-Upload wird bei zu vielen, zu großen oder falsch formatierten Bildern abgelehnt.
- Reaktion mit dem passenden Emoji vergibt die zugeordnete Rolle, teils mit Direktnachricht; beim Entfernen der Reaktion kann die Rolle wieder entzogen werden.
- Live-Zahlen und Patchnotes werden auf der Website angezeigt, sofern Live-Daten verfügbar sind.
- Bei aktiver Coaching-Sperre wird die Buchung mit Ablaufzeit und Grund verweigert.

## Sichtbare Zustände

| Zustand | Was du siehst | Was es bedeutet | Sicherer nächster Schritt |
| --- | --- | --- | --- |
| Austritts-Umfrage offen | Der persönliche Umfrage-Link zeigt ein Formular mit Anzeigename, Grund und Feldern zum Ausfüllen. | Der Link ist gültig und die Umfrage wurde noch nicht abgeschickt. | Antworten ausfüllen, optional Bilder anhängen und absenden. |
| Umfrage bereits abgesendet | Meldung, dass die Umfrage schon abgeschickt wurde. | Es ist bereits eine Einsendung gespeichert; eine zweite ist nicht möglich. | Keine Aktion nötig; bei Korrekturbedarf das Team kontaktieren. |
| Umfrage-Link ungültig oder abgelaufen | Fehlermeldung, dass die Umfrage nicht gefunden wurde. | Der Link ist unbekannt, unvollständig oder zu alt. | Prüfen, ob der Link vollständig kopiert wurde; sonst ist er abgelaufen und kann nicht erneuert werden. |
| Bild-Upload abgelehnt | Fehlermeldung zu zu vielen oder zu großen Bildern bzw. falschem Bildtyp. | Die Grenzen für Anzahl, Größe oder Format der Bilder wurden überschritten. | Weniger oder kleinere Bilder in einem gängigen Bildformat (JPG/PNG/WebP/GIF) anhängen. |
| Coaching-Sperre aktiv | Bei einer Coaching-Buchung wird man als gesperrt geführt, mit Ablaufzeit und Grund. | Wegen eines nicht wahrgenommenen Termins besteht eine befristete Sperre. | Bis zum Ablauf der Sperre warten; bei Fragen das Team ansprechen. |
| Kein Dashboard-Zugriff | Nach dem Discord-Login eine Meldung, dass Admin-/Moderator-Rechte fehlen. | Das Konto hat keine der berechtigten Rollen/Rechte für das Verwaltungs-Dashboard. | Das Dashboard ist nur für Team/Moderation gedacht; normale Mitglieder benötigen keinen Zugriff. |

## So läuft es ab

1. Nach dem Verlassen des Servers kommt per Discord-DM ein persönlicher Umfrage-Link.
2. Der Link öffnet ein Formular mit Anzeigename und Austrittsgrund.
3. Antworten ausfüllen und optional einige Bilder anhängen.
4. Absenden speichert die Einsendung einmalig.
5. Bereits abgeschickte oder abgelaufene Umfragen werden abgewiesen.

## Typische Meldungen & Fehler

| Signal | Was es bedeutet | Nächster Schritt |
| --- | --- | --- |
| Umfrage-Link führt zu einer Fehlermeldung, dass nichts gefunden wurde | Der Umfrage-Link ist ungültig, unvollständig oder abgelaufen. | Link vollständig aus der Discord-DM kopieren; abgelaufene Links lassen sich nicht neu ausstellen. |
| Meldung, dass die Umfrage bereits abgeschickt wurde | Die Austritts-Umfrage wurde schon einmal eingereicht. | Keine erneute Einsendung möglich; bei Bedarf das Team kontaktieren. |
| Bilder werden als zu viele oder zu groß abgewiesen | Zu viele Bilder oder ein Bild ist zu groß. | Anzahl und Dateigröße der Bilder reduzieren und erneut absenden. |
| Bild wird wegen des Formats abgelehnt oder das Formular kommt nicht durch | Ein angehängtes Bild hat ein nicht unterstütztes Format bzw. das Formular wurde nicht korrekt gesendet. | Nur JPG/PNG/WebP/GIF anhängen und das Formular normal absenden. |
| Login-Dienst meldet, dass er nicht bereit ist | Der Login-Dienst ist vorübergehend nicht einsatzbereit. | Später erneut versuchen; hält es an, dem Team melden. |
| Meldung über zu viele Anfragen beim Anmelden | In kurzer Zeit wurden zu viele Login-Versuche gemacht. | Kurz warten und erneut versuchen. |
| Live-Serverzahlen werden gerade nicht angezeigt | Die Live-Zahlen sind momentan nicht abrufbar. | Später erneut laden; die Zahlen werden kurz zwischengespeichert. |

### Das darf der Support sagen

- Die Austritts-Umfrage lässt sich nur einmal absenden; ist sie schon eingereicht, kannst du dich fürs Team melden, statt es erneut zu versuchen.
- Wenn der Umfrage-Link nicht mehr funktioniert, prüfe, ob er vollständig kopiert wurde; ein abgelaufener Link lässt sich nicht neu ausstellen.
- Werden deine Bilder abgelehnt, häng weniger oder kleinere Bilder in einem gängigen Format (JPG/PNG/WebP/GIF) an und sende erneut ab.
- Eine Coaching-Sperre nach einem verpassten Termin endet automatisch; die angezeigte Ablaufzeit sagt dir, wann du wieder buchen kannst.

### Nie an Mitglieder weitergeben

- Interne Zahlen jeder Art: Schwellen, Sicherheitswerte, Gewichte, Zeitgrenzen, Limits.
- Die interne Entscheidungs- oder Durchsetzungslogik — welche Signale zu welcher Wirkung führen und in welcher Reihenfolge.
- Interne Technik: IDs, Pfade, Endpunkte, Namespaces, KI-Anbieter oder -Modelle, Zugangsdaten.
- Verdeckte Mechaniken oder Betriebsarten — auch nicht andeutungsweise, welche es geben könnte.
- Im Zweifel abstrahieren und an einen Menschen eskalieren (Details im Agenten-Leitfaden).

## Verwandte Seiten

- [Austritt & Datenlöschung](../workflows/austritt-datenloeschung.md)

**Bewusst nicht dokumentiert:** interne Endpunkte, Zugangsdaten, Schwellenwerte und Zeitgrenzen, verdeckte Mechaniken, Durchsetzungsbedingungen. Diese internen Details bleiben aus Sicherheitsgründen außerhalb dieser Wissensbasis.
