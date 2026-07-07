#!/usr/bin/env python3
import argparse
import difflib
import json
import subprocess
import sys
from datetime import date
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

DOC_PATH = Path("public/discord-server/team-und-ansprechpartner.md")
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


def line(member):
    return f"- **{member['display_name']}** (Discord: `{member['username']}`)"


def render_document(stand, moderators, community_moderators, coaches):
    moderator_lines = "\n".join(line(member) for member in moderators)
    community_lines = "\n".join(line(member) for member in community_moderators)
    coach_lines = []
    for member in coaches:
        if member["user_id"] == NANI_ID:
            continue
        suffix = ", organisiert auch die Scrims" if member["user_id"] == LEO_ID else ""
        coach_lines.append(f"{line(member)}{suffix}")
    coach_lines.append("- **Nani** selbst coacht ebenfalls")
    coach_lines = "\n".join(coach_lines)

    return f"""---
title: "Das Team hinter dem Server (Owner, Mods, Coaches)"
tags: [discord-server, team, owner, moderatoren, mods, coaches, ansprechpartner, wer]
stand: {stand}
quelle: "Discord-Rollen der Deutschen Deadlock Community, automatisch aktualisiert"
---
# Das Team hinter dem Server

Wer steckt hinter der Deutschen Deadlock Community? Hier die Leute, die den Server vertreten und am Laufen halten. Diese Liste wird automatisch aus den Discord-Rollen aktualisiert.

## Owner und Gründer
- **Nani** (Discord: `earlysalty`) hat den Server gegründet und betreibt ihn. Er ist auch als **Salty** oder **EarlySalty** bekannt, streamt unter dem Namen EarlySalty auf Twitch und baut die Bots und die Website der Community.

## Moderatoren
Sie kümmern sich um Regeln, Ordnung und Konflikte:
{moderator_lines}

## Community-Moderatoren
Sie unterstützen die Moderation und sind nah an der Community:
{community_lines}

## Coaches
Sie geben kostenloses Coaching für alle Ränge (Anmeldung über <#1494373349944459355> oder die Coaching-Seite der Website):
{coach_lines}

## Paten
Freiwillige aus der Community, die Neulinge persönlich begleiten. Das ist keine feste Liste, wer die Paten-Rolle hat, kann Neulinge übernehmen. Einen Paten bekommst du über den Bot in den DMs.

## Wie erreichst du das Team?
- Bei Problemen oder Fragen: Ticket über den Button in <#1459628609705738539> öffnen.
- Regelverstöße oder Konflikte: an die Moderatoren wenden (Ticket oder direkt ansprechen).
- Fragen an alle: <#1426220702054355077>, da liest auch das Team mit.
"""


def render_from_discord():
    client = McpClient()
    client.initialize()
    roles = {name: fetch_role_members(client, name, role_id) for name, role_id in ROLES}
    return render_document(
        date.today().isoformat(),
        roles["Moderatoren"],
        roles["Community-Moderatoren"],
        roles["Coaches"],
    )


def without_stand_line(text):
    return "\n".join(
        line for line in text.splitlines() if not line.startswith("stand: ")
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
    old = DOC_PATH.read_text(encoding="utf-8") if DOC_PATH.exists() else ""
    # stand:-Zeile ignorieren, sonst committet der Timer täglich nur das Datum
    if without_stand_line(old) == without_stand_line(rendered):
        print("unverändert")
        return 0
    patch = diff(old, rendered)

    if args.dry_run:
        print(patch, end="")
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
    reload_knowledge()
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as e:
        print(f"Fehler: {e}", file=sys.stderr)
        raise SystemExit(1)
