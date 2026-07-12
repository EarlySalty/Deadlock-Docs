#!/usr/bin/env python3
import argparse
import difflib
import html
import json
import subprocess
import sys
from datetime import date
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

DOC_PATH = Path("public/discord-server/team-und-ansprechpartner.html")
DEPLOY_SCRIPT = Path(__file__).resolve().parent / "deploy_corpus.sh"
MCP_URL = "http://127.0.0.1:8890/mcp"
RELOAD_URL = "http://127.0.0.1:8896/internal/reload"
GUILD_ID = "1289721245281292288"
NANI_ID = "662995601738170389"
LEO_ID = "193685907071696896"
ROLES = [
    ("Moderatoren", "1337518124647579661"),
    ("Community-Moderatoren", "1401891955931222110"),
    ("Coaches", "1494372744286965941"),
]


class McpClient:
    def __init__(self, url=MCP_URL):
        self.url = url
        self.next_id = 1

    def call(self, method, params):
        req_id = self.next_id
        self.next_id += 1
        payload = json.dumps(
            {"jsonrpc": "2.0", "id": req_id, "method": method, "params": params}
        ).encode()
        request = Request(
            self.url,
            data=payload,
            method="POST",
            headers={"Content-Type": "application/json", "Accept": "application/json"},
        )
        try:
            with urlopen(request, timeout=70) as response:
                raw = response.read()
        except HTTPError as e:
            raise RuntimeError(f"dl-mcp HTTP {e.code}: {e.reason}") from e
        except URLError as e:
            raise RuntimeError(f"dl-mcp nicht erreichbar: {e.reason}") from e
        except TimeoutError as e:
            raise RuntimeError("dl-mcp Timeout") from e

        try:
            data = json.loads(raw)
        except json.JSONDecodeError as e:
            raise RuntimeError(f"dl-mcp antwortet nicht mit JSON: {e}") from e
        if data.get("error"):
            raise RuntimeError(f"dl-mcp Fehler bei {method}: {data['error']}")
        return data.get("result")

    def initialize(self):
        self.call(
            "initialize",
            {
                "protocolVersion": "2025-06-18",
                "capabilities": {},
                "clientInfo": {"name": "team-doc-updater", "version": "1"},
            },
        )

    def api_call(self, method, path, body):
        result = self.call(
            "tools/call",
            {"name": "api_call", "arguments": {"method": method, "path": path, "body": body}},
        )
        if not isinstance(result, dict) or result.get("isError"):
            raise RuntimeError(f"api_call fehlgeschlagen: {result}")
        content = result.get("content") or []
        text = content[0].get("text") if content and isinstance(content[0], dict) else None
        if not text:
            raise RuntimeError("api_call ohne Text-Ergebnis")
        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            raise RuntimeError(f"api_call Ergebnis ist kein JSON: {e}") from e


def extract_members(response, role_name):
    members = response.get("members") if isinstance(response, dict) else None
    if not members:
        raise ValueError(f"{role_name}: Rollen-Abfrage leer oder fehlerhaft")

    out = []
    for item in members:
        member = item.get("member") if isinstance(item, dict) else None
        user = member.get("user") if isinstance(member, dict) else None
        if not isinstance(user, dict):
            raise ValueError(f"{role_name}: Mitglied ohne User-Daten")
        username = user.get("username")
        user_id = user.get("id")
        display_name = member.get("nick") or user.get("global_name") or username
        if not (display_name and username and user_id):
            raise ValueError(f"{role_name}: Mitglied unvollständig")
        out.append(
            {"display_name": display_name, "username": username, "user_id": user_id}
        )
    # Discord garantiert keine stabile Reihenfolge; ohne Sortierung gäbe es Scheindiffs
    out.sort(key=lambda member: member["display_name"].lower())
    return out


def fetch_role_members(client, role_name, role_id):
    response = client.api_call(
        "POST",
        f"/guilds/{GUILD_ID}/members-search",
        {"and_query": {"role_ids": {"and_query": [role_id]}}, "limit": 50},
    )
    return extract_members(response, role_name)


def member_item(member, suffix=""):
    name = html.escape(member["display_name"])
    username = html.escape(member["username"])
    return f"    <li><strong>{name}</strong> (Discord: <code>{username}</code>){suffix}</li>"


def render_document(stand, moderators, community_moderators, coaches):
    _ = moderators, community_moderators, coaches
    return f"""<!doctype html>
<html lang="de">
<head>
  <meta charset="utf-8">
  <title>Team und Ansprechpartner</title>
  <meta name="tags" content="discord-server, team, support, ansprechpartner, serverproblem, hilfe">
  <meta name="stand" content="{stand}">
  <meta name="quelle" content="Produktdokumentation und geprüftes sichtbares Verhalten">
</head>
<body>
<main>
  <h1>Team und Ansprechpartner</h1>
  <p><strong>Kurz:</strong> Die aktuell zuständigen Personen findest du in <em>Willkommen</em> im Abschnitt <em>Community-Team</em>. Für ein persönliches Anliegen nutzt du den dortigen Support-Schnellzugriff; für reine Wissensfragen zuerst <code>/faq</code>.</p>

  <section id="wen-erreichen">
    <h2>Wen du erreichst</h2>
    <p>Der Abschnitt <em>Community-Team</em> in <em>Willkommen</em> zeigt die aktuell zugeordneten Gruppen wie Owner, Moderation, Community-Moderation und Coach. Unbesetzte Gruppen werden als solche angezeigt. Namen und Besetzung sind dynamisch — deshalb nennt diese Seite keine festen Personen.</p>
    <p>Hast du ein Serverproblem und weißt nicht, wer dir hilft? Nutze beim Abschnitt <em>Community-Team</em> in <em>Willkommen</em> den Support-Schnellzugriff — von dort kümmert sich der Support um dein Serveranliegen.</p>
  </section>

  <section id="richtiger-weg">
    <h2>Der richtige Weg je Anliegen</h2>
    <table>
      <tr><th>Anliegen</th><th>Weg</th></tr>
      <tr><td>Server- oder Bot-Frage</td><td>Privater Fragechat über <code>/faq</code>.</td></tr>
      <tr><td>Persönliches Support- oder Moderationsanliegen</td><td>Support-Schnellzugriff im Abschnitt <em>Willkommen</em>.</td></tr>
      <tr><td>Coaching</td><td>Sichtbarer Coaching-Bereich beziehungsweise <code>/coaching-anfrage</code>.</td></tr>
    </table>
  </section>

  <section id="grenzen">
    <h2>Was hier offen bleibt</h2>
    <ul>
      <li>Keine privaten Kontaktdaten, Dienstpläne oder internen Zuständigkeiten.</li>
      <li>Keine garantierte Antwortzeit oder Verfügbarkeit einer bestimmten Person.</li>
      <li>Direkte DMs an einzelne Teammitglieder sind nicht der vorgesehene Standardweg — nutze den sichtbaren Support-Einstieg.</li>
    </ul>
  </section>
</main>
</body>
</html>
"""


def render_from_discord():
    # Der öffentliche Vertrag ist bewusst roster-unabhängig; der Timer konvergiert ihn nur.
    return render_document(date.today().isoformat(), [], [], [])


def without_stand_line(text):
    # nur die stand-Meta-Zeile ignorieren, sonst committet der Timer täglich nur das Datum
    return "\n".join(
        line for line in text.splitlines() if 'name="stand"' not in line
    )


def diff(old, new):
    return "".join(
        difflib.unified_diff(
            old.splitlines(keepends=True),
            new.splitlines(keepends=True),
            fromfile=str(DOC_PATH),
            tofile=str(DOC_PATH),
        )
    )


def run(cmd):
    subprocess.run(cmd, check=True)


def committed_doc():
    """Inhalt von DOC_PATH so, wie er am HEAD committet ist – sonst leer.

    Maßgeblich ist der committete Stand, nicht die Arbeitskopie: Scheitert ein
    ``git commit`` nach erfolgreichem ``write_text``/``git add``, sieht die
    Arbeitsdatei bereits wie der neue Render aus. Ein Retry, der nur die
    Arbeitskopie vergleicht, hielte das fälschlich für "unverändert" und würde
    den alten HEAD deployen. Der HEAD-Blob deckt genau diesen Fall auf.
    """
    try:
        result = subprocess.run(
            ["git", "show", f"HEAD:{DOC_PATH.as_posix()}"],
            check=True,
            capture_output=True,
            text=True,
        )
    except (subprocess.CalledProcessError, OSError):
        return ""
    return result.stdout


def deploy_corpus(ref):
    run([str(DEPLOY_SCRIPT), ref])


def reload_knowledge():
    request = Request(RELOAD_URL, data=b"", method="POST")
    try:
        with urlopen(request, timeout=20) as response:
            response.read()
    except HTTPError as e:
        raise RuntimeError(f"Reload HTTP {e.code}: {e.reason}") from e
    except URLError as e:
        raise RuntimeError(f"Reload nicht erreichbar: {e.reason}") from e
    except TimeoutError as e:
        raise RuntimeError("Reload Timeout") from e


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    rendered = render_from_discord()
    # Gegen den committeten HEAD-Stand vergleichen, nicht gegen die Arbeitskopie:
    # sonst fiele ein Retry nach fehlgeschlagenem Commit fälschlich in den
    # Unchanged-Zweig und deployte den alten HEAD (uncommitteter Render bliebe
    # dauerhaft liegen).
    committed = committed_doc()
    # stand-Meta-Zeile ignorieren, sonst committet der Timer täglich nur das Datum
    if without_stand_line(committed) == without_stand_line(rendered):
        # Kein neuer Commit, aber den bestehenden HEAD konvergieren lassen:
        # ein früher fehlgeschlagener Push/Deploy/Reload würde sonst dauerhaft
        # einen alten Snapshot oder nicht neu geladenen Dienst hinterlassen.
        print("unverändert – konvergiere bestehenden HEAD")
        if args.dry_run:
            return 0
        run(["git", "push"])
        deploy_corpus("HEAD")
        reload_knowledge()
        return 0

    if args.dry_run:
        old = DOC_PATH.read_text(encoding="utf-8") if DOC_PATH.exists() else ""
        print(diff(old, rendered), end="")
        return 0

    DOC_PATH.write_text(rendered, encoding="utf-8")
    run(["git", "add", str(DOC_PATH)])
    run(
        [
            "git",
            "commit",
            "-m",
            "auto: Team-Doku aus Discord-Rollen aktualisiert",
            "-m",
            "Co-authored-by: Team-Doc-Updater <bot@local>",
        ]
    )
    run(["git", "push"])
    # erst den committeten Korpus deployen, dann den Wissens-Dienst neu laden
    deploy_corpus("HEAD")
    reload_knowledge()
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as e:
        print(f"Fehler: {e}", file=sys.stderr)
        raise SystemExit(1)
