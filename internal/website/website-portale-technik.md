---
title: "Website-Portale — Technik"
tags: [website, technik]
stand: 2026-07-07
quelle: "public/website/website-portale.md (Technik-Sektion)"
---
## Was passiert technisch?
Die Website kombiniert mehrere Vite-Frontends mit klaren Basispfaden. Einige Portale sind rein statisch, andere sprechen Live-APIs an oder brauchen einen Discord-Login. Das `builds`-Backend läuft in Rust und stellt Router für Auth, Heroes, Builds, Tierlists, Patch-Daten, History, Admin, Coaching, Coach-Plattform und Scrims bereit; die Activity-Daten kommen vom separaten Stats-Service. Für Nutzer zeigt sich das vor allem in zwei Dingen: schnelle, getrennt deploybare Teilseiten und unterschiedliche Funktionslevel je nach Login oder Live-API-Verfügbarkeit.
