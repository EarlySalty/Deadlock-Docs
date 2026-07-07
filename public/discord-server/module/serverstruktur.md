---
title: "Serverstruktur"
tags: [discord-server, serverstruktur, discord]
stand: 2026-07-07
quelle: "Deadlock-Bots/docs/support-kb/modules/serverstruktur.html"
---
# Serverstruktur

Kategorien, Kanäle und Rollen samt ihrer Sichtbarkeits-, Schreib- und Voice-Rechte werden zentral als feste Struktur verwaltet und vom Team kontrolliert ausgerollt. Was ein Mitglied sieht, wo es schreiben und welche Voice-Kanäle es betreten darf, kommt aus dieser Struktur.

## Was Mitglieder merken

Für Mitglieder wirkt das System still im Hintergrund: Öffentliche Bereiche sind für alle offen, Info- und Ankündigungskanäle nur lesbar, und geschützte Bereiche (z.B. Moderation, VIP, Streamer, Support, Archiv) tauchen nur mit passender Rolle überhaupt auf. Manchmal erscheinen Kanäle neu, verschwinden, werden umbenannt oder verschoben, oder ein Voice-Beitritt ist gesperrt. Das sind gewollte Struktur-Änderungen des Teams, keine Fehler und nichts, was ein einzelnes Mitglied selbst auslöst.

## Mögliche Ausgänge

- Kanäle, Kategorien und Rollen werden angelegt, umbenannt oder verschoben
- Sichtbarkeits- und Schreibrechte werden auf den Soll-Zustand gebracht
- Ausgemusterte Kanäle werden in ein unsichtbares Archiv geschoben
- Löschungen von Kanälen oder Rollen passieren nie automatisch; nur überflüssige Rechte-Einträge werden bereinigt
- Die Serverstruktur wird zentral konsistent gehalten

## Sichtbare Zustände

| Zustand | Was du siehst | Was es bedeutet | Sicherer nächster Schritt |
| --- | --- | --- | --- |
| Öffentlich: lesen & schreiben | Kanal ist sichtbar, man kann lesen und schreiben | Der Kanal liegt in einem öffentlichen Bereich ohne Sonderrechte; es gelten nur die Server-Grundrechte | Normal nutzen; keine Aktion nötig |
| Nur lesen | Kanal sichtbar, aber Schreiben/Threads gesperrt (z.B. Regelwerk, Willkommen, Patchnotes, Ankündigungen) | Info-/Ankündigungskanal: bewusst nur zum Lesen, Schreiben ist nur für berechtigte Rollen oder Bots offen | Ist so gewollt; bei Bedarf im vorgesehenen Community-Kanal schreiben |
| Unsichtbar ohne passende Rolle | Ein Bereich oder Kanal ist gar nicht sichtbar | Der Bereich ist rollenbeschränkt (z.B. Moderation, VIP, Streamer, Support) oder archiviert; ohne passende Rolle wird er ausgeblendet | Beim Team nach der passenden Rolle bzw. dem Zugang fragen |
| Voice gesperrt bis verifiziert | Beitritt zu bestimmten Voice-Kanälen (z.B. Ranked-Lanes) nicht möglich | Der Beitritt ist gesperrt, bis eine Verifizierung vorliegt bzw. eine bestimmte Rolle vergeben ist | Den vorgesehenen Verifizierungs-Ablauf abschließen und erneut versuchen |
| AFK: stummgeschaltet | Im AFK-Voice kein Reden, Streamen oder Schreiben | Der AFK-Bereich ist absichtlich stummgeschaltet | Kein Fehler; einen aktiven Voice-Kanal betreten |
| Individuelle Sperre oder Freigabe | Einzelnes Mitglied sieht oder nutzt einen Kanal anders als andere (gesperrt oder zusätzlich freigegeben), unabhängig von Rollen | Einzelne Sonderfälle werden vom Team gepflegt | Betroffene können beim Mod-Team nach Anlass und Überprüfung fragen |

## So läuft es ab

1. Team oder Verwaltung stößt einen Abgleich der Serverstruktur an (nicht durch einzelne Mitglieder auslösbar)
2. Aktuellen Ist-Zustand des Servers einlesen
3. Soll-Zustand aus den hinterlegten Regeln ableiten
4. Unterschiede als Vorschau berechnen und speichern
5. Nach Bestätigung der Vorschau die Änderungen an Kanälen, Rollen und Rechten ausführen

## Typische Meldungen & Fehler

| Signal | Was es bedeutet | Nächster Schritt |
| --- | --- | --- |
| Eine Struktur-Änderung wurde abgebrochen, weil die bestätigte Vorschau nicht mehr zum Server passte | Kein Effekt für Mitglieder; der Abgleich stoppt sicherheitshalber | Team-intern: Zustand neu einlesen und Vorschau erneut erzeugen |
| Die Änderungs-Vorschau war zu alt und wurde verworfen | Kein Effekt für Mitglieder; die Vorschau wird aus Sicherheit nicht angewendet | Team-intern: Vorschau frisch erzeugen und bestätigen |
| Zwei Kanäle würden auf denselben Zielnamen umbenannt | Kein direkter Effekt; der Lauf stoppt zur Klärung der Namenskollision | Team-intern: kollidierende Kanäle manuell klären |
| Ein Kanal oder Objekt existierte nicht mehr | Die einzelne Änderung wird übersprungen, der Rest läuft weiter | Kein Handlungsbedarf für Mitglieder |
| Ein im Server-Onboarding verlinkter Kanal lässt sich nicht verstecken | Die Änderung wird übersprungen und der Kanal bleibt sichtbar | Team-intern: Kanal ggf. aus dem Onboarding entfernen, falls er verborgen werden soll |

### Das darf der Support sagen

- Wenn ein Kanal für dich plötzlich weg ist oder neu auftaucht, war das meist eine geplante Struktur-Anpassung des Teams, kein Fehler bei dir.
- Geschützte Bereiche wie Moderation, VIP, Streamer oder Support sind ohne passende Rolle komplett ausgeblendet; wenn du dort Zugang brauchst, frag beim Team nach der Rolle.
- Manche Voice-Kanäle kann man erst nach abgeschlossener Verifizierung betreten; schließ den vorgesehenen Ablauf ab und versuch es dann erneut.
- Wenn du einen Kanal anders siehst als andere Mitglieder, kann das eine dokumentierte Einzel-Ausnahme sein; das Mod-Team kann Anlass und Überprüfung klären.

### Nie an Mitglieder weitergeben

- Interne Zahlen jeder Art: Schwellen, Sicherheitswerte, Gewichte, Zeitgrenzen, Limits.
- Die interne Entscheidungs- oder Durchsetzungslogik — welche Signale zu welcher Wirkung führen und in welcher Reihenfolge.
- Interne Technik: IDs, Pfade, Endpunkte, Namespaces, KI-Anbieter oder -Modelle, Zugangsdaten.
- Verdeckte Mechaniken oder Betriebsarten — auch nicht andeutungsweise, welche es geben könnte.
- Im Zweifel abstrahieren und an einen Menschen eskalieren (Details im Agenten-Leitfaden).

**Bewusst nicht dokumentiert:** Durchsetzungsbedingungen, verdeckte Mechaniken, Schwellenwerte und Zeitgrenzen, Bewertungslogik, interne Endpunkte. Diese internen Details bleiben aus Sicherheitsgründen außerhalb dieser Wissensbasis.
