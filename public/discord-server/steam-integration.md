---
title: "Steam-Integration"
tags: [discord-server, steam, integration]
stand: 2026-07-08
quelle: "Deadlock-Bots/docs/steam-integration.md"
---
# Steam-Integration

## Worum geht es?
Die Steam-Integration verbindet dein Discord-Konto mit deinem Steam-Account. Dadurch kann der Server deinen Deadlock-Rang sauber erkennen und dir nach bestätigter Steam-Freundschaft die Steam-Verified-Rolle geben.

Zusätzlich gibt es einen Rank-Lookup für verknüpfte Accounts und einen Hintergrund-Sync, der Freundschaften, Verifizierung und Rangdaten aktuell hält.

## Wie nutze ich das?
Für die normale Verknüpfung nutzt du das Steam-Panel in <#1398021105339334666>:
https://discord.com/channels/1289721245281292288/1398021105339334666

Das Panel hat drei Buttons: `Steam verknüpfen`, `Freundescode eingeben` und `📊 Rang prüfen`. Der Flow läuft in drei Schritten:

1. Du meldest dich kurz über Steam an. Das läuft über Steam OpenID, also ohne Passwort-Eingabe beim Bot. Der persönliche Link aus dem Panel ist 15 Minuten gültig und einmalig verwendbar.
2. Du gibst deinen Steam-Freundescode ein (Button oder Formular-Fallback).
3. Der Bot schickt dir eine Steam-Freundschaftsanfrage — erst wenn du die annimmst, gilt dein Link als vollständig verifiziert.

Falls die Freundschaftsanfrage nicht ankommt, kannst du dem Steam-Bot selbst eine Freundschaftsanfrage schicken. Freundescode des Bots: `820142646`.

`📊 Rang prüfen` zeigt dir deinen erkannten Deadlock-Rang. Die automatische Rang-Rolle kommt aus der Steam-Profilkarte deines verknüpften Accounts und wird im Hintergrund aktuell gehalten.

Wenn du ausdrücklich Account-Verwaltung brauchst, zum Beispiel gespeicherte Accounts ansehen, Hauptaccount ändern oder eine Verknüpfung entfernen, frag gezielt im Server-/Bot-Fragen-Kanal <#1491953161747955853> oder schreib dem Bot direkt.

Für einen Beta-Invite: nett in <#1426220702054355077> fragen und deinen Steam-Freundescode dazu posten — ein Community-Mitglied lädt dich dann persönlich zum Playtest ein. Details dazu stehen in „Onboarding und Invites".

## Kosten / Premium
Die Steam-Verknüpfung, Rank-Erkennung und der Beta-Invite sind kostenlos.

Wenn du den Server unbedingt unterstützen willst, gibt es freiwillig Ko-fi: https://ko-fi.com/deutschedeadlockcommunity — kein Pflichtkauf, schaltet nichts frei und beschleunigt keinen Invite.

## Was passiert technisch (kurz)?
Die Verknüpfung nutzt Steam OpenID und speichert danach die technische Steam-ID zusammen mit deinem Discord-Konto. Eine bestätigte Steam-Freundschaft ist die zweite Freigabe: Erst dann werden Verifizierung und rangbasierte Features aktiv.

Ein Hintergrunddienst synchronisiert regelmäßig die Steam-Freundesliste des Bot-Accounts. Sobald dein Account als Freund bestätigt ist, werden Verifizierung und Rollen nachgezogen. Der Rank-Sync liest die Deadlock-Profilkarte und aktualisiert Rangdaten im Hintergrund.

## Grenzen & häufige Fragen
- Nur ein OpenID-Login reicht nicht. Freundescode + bestätigte Steam-Freundschaft mit dem Bot gehören dazu.
- **„Limited User"**: Steam blockiert Playtest-Invites, wenn auf dem Account noch keine ~5 $ ausgegeben wurden. Das ist eine Valve-Regel, kein Bot-Problem — sie schlägt erst beim Invite-Versuch zu.
- Steam kann außerdem verlangen, dass die Freundschaft mit dem Einladenden mindestens 30 Tage besteht.
- Rank-Lookups und automatische Rangrollen funktionieren nur sauber mit verifiziertem Steam-Freund-Link.
- Wenn du mehrere Steam-Accounts verknüpft hast, zählt für viele Features dein gesetzter Primäraccount.
- Ein Invite erscheint nicht immer sofort — nach Erfolg kann es 1–2 Tage dauern, bis die Einladung bei Steam sichtbar ist. **Siehst du sie nicht?** Schau direkt bei Steam unter https://store.steampowered.com/account/playtestinvites nach — viele übersehen genau diese Seite.
- Vorübergehende Steam- oder Game-Coordinator-Probleme können einzelne Invite-Versuche verzögern. In solchen Fällen hilft meist ein späterer Retry.
