"""Exportiert ausschließlich einzeln freigegebene öffentliche Bedienbelege aus Code."""
from __future__ import annotations

import hashlib
import re
from collections.abc import Callable
from pathlib import Path

from import_public_sources import safe_relative
from knowledge_metadata import PublicSections, verified_audit

# Dieser erste Test gibt keine beliebigen Repositories oder Dateien frei.
PUBLIC_CODE_SYMBOLS = frozenset({
    ("rust/crates/dl-community/src/faq.rs", "register:faq"),
    ("rust/crates/dl-voice/src/lfg_panel.rs", "LFG_ERR_SCHON_AKTIVE_SUCHE"),
    ("rust/crates/dl-voice/src/lfg_panel.rs", "LFG_WATCH_ERR_UNVOLLSTAENDIG"),
})


def approved_excerpt(blob: bytes, symbol: str) -> str | None:
    """Erfasst nur die benannte öffentliche Deklaration, keine Nachbarlogik."""
    literal = r'"(?:\\.|[^"\\])*"'
    if symbol == "register:faq":
        pattern = (r'"name": "faq",\s*"description": ' + literal
                   + r',\s*"type": 1,\s*"dm_permission": false,')
    else:
        pattern = r'pub const ' + re.escape(symbol) + r': &str =\s*' + literal + ';'
    matches = re.findall(pattern, blob.decode("utf-8"))
    return matches[0] if len(matches) == 1 else None


def public_code_manifest(
    public: Path,
    audits: list[dict],
    *,
    policy_revision: str,
    policy: dict,
    revisions: dict[str, str],
    read_blob: Callable[[str, str, str], bytes],
) -> dict:
    """Keine Historienausweichsuche: abweichender aktueller Stand entzieht die Quelle."""
    release = policy.get("release_commit", "")
    if (policy.get("schema_version") != 1 or policy.get("repository") != "discord"
            or not isinstance(release, str) or not re.fullmatch(r"[0-9a-f]{40}", release)):
        raise ValueError("Ungültige öffentliche Codequellen-Policy")
    rows = policy.get("entries")
    if not isinstance(rows, list):
        raise TypeError("Codequellen brauchen eine explizite Eintragsliste")
    if len(rows) > 4:
        raise ValueError("Höchstens vier öffentliche Codebelege sind freigegeben")
    result = {"schema_version": 1, "source_policy_version": 1,
              "policy_revision": policy_revision, "release_commit": release, "entries": []}
    if revisions.get("discord") != release:
        return result
    by_path = {audit["path"]: audit for audit in audits}
    seen: set[str] = set()
    for row in rows:
        if not isinstance(row, dict):
            raise TypeError("Ungültiger öffentlicher Codebeleg")
        fields = ("id", "title", "public_help_path", "public_help_section", "source_path",
                  "symbol", "blob_sha256", "excerpt", "explanation")
        if not all(isinstance(row.get(key), str) and row[key].strip() for key in fields):
            raise ValueError("Unvollständiger öffentlicher Codebeleg")
        if not re.fullmatch(r"P[1-4]", row["id"]) or row["id"] in seen:
            raise ValueError("Codebeleg braucht eine eindeutige öffentliche Kennung")
        seen.add(row["id"])
        if ((row["source_path"], row["symbol"]) not in PUBLIC_CODE_SYMBOLS
                or not safe_relative(row["public_help_path"])
                or row["public_help_path"].startswith("internal/")
                or not re.fullmatch(r"[0-9a-f]{64}", row["blob_sha256"])):
            raise ValueError("Nicht freigegebene öffentliche Codequelle")
        if (len((row["excerpt"] + "\n\n" + row["explanation"]).encode("utf-16-le")) // 2 > 2000
                or len(row["title"]) > 160 or len(row["symbol"]) > 160):
            raise ValueError("Öffentlicher Codebeleg überschreitet die Textgrenze")
        if row.get("review_status") != "verified":
            continue
        help_path = public / row["public_help_path"]
        if (not help_path.is_file() or help_path.is_symlink()
                or any(p.is_symlink() for p in help_path.parents if p != public.parent)):
            continue
        content = help_path.read_bytes()
        audit = by_path.get("public/" + row["public_help_path"], {})
        if not verified_audit(audit, content):
            continue
        if not any(check.get("repository") == "discord"
                   and row["source_path"] in check.get("paths", [])
                   for check in audit.get("code", [])):
            continue
        parser = PublicSections()
        parser.feed(content.decode("utf-8"))
        if parser.section_counts.get(row["public_help_section"]) != 1:
            continue
        blob = read_blob("discord", release, row["source_path"])
        if hashlib.sha256(blob).hexdigest() != row["blob_sha256"]:
            continue
        # Der komplette freigegebene Ausschnitt muss exakt einmal vorkommen.
        # Kein Nachladen benachbarter Zeilen oder abweichender alter Revisionen.
        if approved_excerpt(blob, row["symbol"]) != row["excerpt"]:
            continue
        entry = {key: row[key] for key in fields}
        entry.update(repository="discord", public_help_sha256=hashlib.sha256(content).hexdigest())
        result["entries"].append(entry)
    return result
