# Changelog

## #14 — Supportantworten bleiben eigenständig

Problem: Einige richtige Antworten waren nur zusammen mit Überschriften oder Nachbarabsätzen eindeutig und konnten deshalb abgelehnt werden.

Änderung: Die betroffenen öffentlichen Hinweise tragen Frage, Bedingung und nächsten Schritt jetzt jeweils im selben Antwortblock.

Aktuelles Verhalten: Der Support-Agent kann die geprüften Discord-, Steam-, Twitch-, Patchnotes- und Turnierfragen direkt aus vollständigen öffentlichen Passagen beantworten.

## #13 — Steam-Kontoverwaltung als vollständiger Beleg

Problem: Die richtige Antwort zur eigenen Steam-Verwaltung konnte aus der Steam-Bot-Übersicht stammen, deren drei Listenpunkte ohne Satzende aber nicht als vollständige Einzelbelege galten; außerdem war diese Seite im Antworttest nicht zugelassen.

Änderung: Die drei Verwaltungswege enden jetzt als vollständige Aussagen, und der Antworttest akzeptiert die Steam-Bot-Übersicht als passende Quelle.

Aktuelles Verhalten: Belegte Antworten erklären jetzt direkt aus der Steam-Bot-Übersicht, wie du Konten ansiehst, das primäre Konto festlegst und eigene Verknüpfungen entfernst.

## #12 — Rangverlauf-Antwort bleibt einzeln eindeutig

Problem: Die richtige Antwort zur Rang-Sichtbarkeit wurde abgelehnt, wenn nur ihr erster Satz ausgewählt wurde; „privat“ und „sehen“ standen darin nicht gemeinsam. Außerdem fehlte eine passende öffentliche Seite im Antworttest.

Änderung: Die Rang-Passagen nennen jetzt ausdrücklich, dass andere den standardmäßig privaten Rangverlauf nicht sehen können, und der Test akzeptiert auch die öffentliche Statistikübersicht als Quelle.

Aktuelles Verhalten: Andere sehen den Rangverlauf standardmäßig nicht; du selbst siehst ihn weiterhin und kannst die Sichtbarkeit nach Login ändern.

## #11 — Alle belegten Fragewege im Antworttest zugelassen

Problem: Die richtige Antwort zum Stellen einer Serverfrage konnte aus zwei passenden öffentlichen Übersichten kommen, die im Antworttest noch nicht als zulässige Quellen geführt waren.

Änderung: Der Test erkennt nun auch die Concierge- und die allgemeine Bot-Übersicht als passende Quellen für diesen Frageweg an.

Aktuelles Verhalten: Belegte Hinweise auf <em>Frage stellen</em> oder <code>/faq</code> werden aus allen passenden öffentlichen Hilfeseiten akzeptiert.

## #10 — Steam-Modulübersicht als richtige Quelle anerkannt

Problem: Die richtige Live-Antwort zur Steam-Verknüpfung kam aus der öffentlichen Modulübersicht, die im Antworttest noch nicht als zulässige Quelle geführt war.

Änderung: Der Test ordnet nun auch die Modulübersicht der Steam-Verknüpfung als erwartete Quelle zu.

Aktuelles Verhalten: Eine belegte Antwort über Steam-Panel, <code>/account_verknüpfen</code>, Freundescode und Freundschaftsanfrage wird aus allen drei passenden öffentlichen Seiten akzeptiert.

## #9 — Automatische Begrüßungs-DM klar eingegrenzt

Problem: Die richtige Antwort wurde verworfen, weil ihr die eindeutige Zuordnung von Bot, Beitritt und Concierge fehlte; der Test sicherte diese Eingrenzung ebenfalls nicht ab.

Änderung: Die öffentliche Kurzantwort benennt den Concierge-Bot, den Beitritt zum Server und die ausbleibende automatische Begrüßungs-DM gemeinsam; der Antworttest verlangt diese Zuordnung.

Aktuelles Verhalten: Der Concierge-Bot schreibt nach dem Serverbeitritt nicht automatisch eine Begrüßungs-DM; andere dokumentierte, ereignisgebundene Bot-DMs bleiben möglich.

## #8 — Concierge-DM-Antwort nennt ihren Weg vollständig

Problem: Bei Fragen zur Direktnachricht konnte die richtige Kurzantwort ohne die Begriffe „Concierge“ und „per DM“ als zu allgemein verworfen werden.

Änderung: Die erste Kurzpassage nennt jetzt den Concierge und den DM-Weg gemeinsam und behält die bestehende Zustellbedingung bei.

Aktuelles Verhalten: Erreicht eine DM an den Concierge den Bot, antwortet er aus demselben öffentlichen Wissen; `/faq` bleibt der verlässlichere Weg.

## #7 — Team-Support bleibt vollständig und redigiert

Problem: Einzelne Supportantworten konnten den sichtbaren Fundort auslassen; zusätzlich hing die tägliche Team-Aktualisierung von Rollendaten ab und konnte die redigierte Seite wieder durch eine Namensliste ersetzen.

Änderung: Der Supportsatz nennt „Community-Team“ und „Willkommen“ gemeinsam, und die Aktualisierung erzeugt denselben öffentlichen Vertrag, ohne Rollendaten abzufragen oder Namen und Benutzernamen auszugeben.

Aktuelles Verhalten: Der Supportweg bleibt auch als einzeln ausgewählte Antwort verständlich; die generatorfeste Seite bleibt roster-unabhängig und verweist für aktuelle Zuständigkeiten auf den sichtbaren Community-Team-Bereich.

## #6 — Live-Supportantworten nennen den sichtbaren Einstieg vollständig

Problem: Bei allgemeinen Orientierungsfragen fand der Assistent zwar den richtigen Navigationsabschnitt, ließ aber entweder den sichtbaren Einstieg über „Willkommen“ aus oder lehnte die Frage nach dem passenden Kanal beziehungsweise der passenden Rolle als zu unbestimmt ab.

Änderung: Der Navigationsabschnitt nennt den Einstieg und die allgemeine Zuordnung von Kanal, Bereich und selbst wählbarer Rolle jetzt direkt dort, wo die einzelnen Anliegen erklärt werden.

Aktuelles Verhalten: Auf Fragen nach dem richtigen Bereich, Kanal oder der passenden Rolle verweist der Assistent zuerst auf „Willkommen“ und führt anschließend über die aktuelle Navigation sowie „Kanäle &amp; Rollen“ zum passenden sichtbaren Weg.

## #5 — Datenschutz-, Paten- und Antwortgrenzen klargezogen

Problem: Die Dokumentation versprach an mehreren Stellen mehr, als tatsächlich passiert, und erklärte technisch unsichere Discord-Zustände nicht eindeutig.

Änderung: Löschung, Opt-out, Patenwunsch, Fragechat und die Grenzen des Assistenten sind jetzt so beschrieben, wie sie sich beobachten lassen, inklusive sicherer nächster Schritte bei unklarer Zustellung.

Aktuelles Verhalten: Nur „stopp" in einer echten DM an den Concierge stoppt neue Verlaufsspeicherung und ungefragte Kontakte von ihm; im öffentlichen Fragenkanal, FAQ-Chat und privaten Fallback ist das Wort keine Steuerung und löscht nichts; „vergiss mich" löscht nur Concierge-Daten und `/datenschutz` bleibt der umfassendere Weg. Unklare Discord-Zustände werden sichtbar als unsicher behandelt, ein bereits erfolgreicher Patenwunsch wird nicht doppelt weitergegeben, und der aktuelle Support-Agent führt weder Auto-Debug noch andere angeforderte Live-Aktionen aus.

## #4 — Supportwissen für Bots und Server vereinheitlicht

Problem: Fragen zu Discord, Bots und Portalen konnten wegen verstreuter und teils veralteter Inhalte nicht zuverlässig beantwortet werden.

Änderung: Das öffentliche Wissen wurde für Community-Bot, Steam-Bot, Twitch-Bot, Patchnotes, Turniere und Website-Portale vereinheitlicht und mit realistischen Supportfragen geprüft.

Aktuelles Verhalten: Der Assistent antwortet in Direktnachrichten, privaten Fragechats und bei Serverfragen aus dem öffentlichen Wissen; Tickets bleiben menschlicher Support, und unsichere Fälle gehen an Menschen statt eine Diagnose oder Aktion auszulösen.

## #3 — Demo-Ergebnisdownload begrenzt

Problem: Die Betriebsdokumentation erklärte noch nicht, welche Ergebnis-URLs der Demo-Pilot akzeptiert.

Änderung: Der feste HTTPS-Origin und das Ablehnen von Redirects sind im Fehler- und Sicherheitsverhalten ergänzt.

Aktuelles Verhalten: Demo-Ergebnisse werden nur direkt von `demo-extracts.deadlock-api.com` geladen; andere Ziele bleiben als sichtbarer Fehler offen.

## #2 — Demo-Timeout präzisiert

Problem: Die Betriebsdokumentation beschrieb Demo-Polling noch als normalen zentralen Retry-Pfad und ließ die harte Gesamtdeadline offen.

Änderung: Der deadline-bewusste Umgang mit Anfragezeit, 429, Serverfehlern, Transportfehlern, Backoff und Poll-Pause ist konkret dokumentiert.

Aktuelles Verhalten: Betrieb und Review können nachvollziehen, dass kein einzelner Poll-Versuch die konfigurierte Gesamtdauer überschreiten darf.

## #1 — Match-Demo-Lernen dokumentiert

Problem: Der neue Demo-, Report- und Reviewpfad des Deadlock Brain hatte noch keine zentrale interne Betriebsdokumentation.

Änderung: Ablauf, Evidenzvertrag, Kalibrierungstor, Fehlerverhalten und der erste Mo-&-Krill-Live-Tracer sind als interne SSOT festgehalten.

Aktuelles Verhalten: Betrieb und Review können den Pilot reproduzierbar ausführen; die erzeugten Reports bleiben bis zum bestandenen Gate isoliertes Kalibrierungsmaterial.
