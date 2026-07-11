# Changelog

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
