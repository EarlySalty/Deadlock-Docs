#!/usr/bin/env python3
"""Vollständigen öffentlichen Export bauen, aktivieren und am Leser bestätigen."""
from __future__ import annotations

import argparse
import fcntl
import fnmatch
import hashlib
import json
import os
import re
import tempfile
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

from import_public_sources import freeze_revisions, git, import_sources, private_path, safe_relative
from knowledge_metadata import corpus_digest, faq_manifest, verified_audit, write_json
from validate_corpus import validate_root


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def faq_digest(snapshot: Path) -> str | None:
    path = snapshot / "faq-manifest.json"
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None


def atomic_json(path: Path, value: dict) -> None:
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent,
                                     prefix=".status-", delete=False) as output:
        temporary = Path(output.name)
        json.dump(value, output, ensure_ascii=False, indent=2)
        output.write("\n")
        output.flush()
        os.fsync(output.fileno())
    try:
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def switch_current(base: Path, target: Path) -> None:
    with tempfile.TemporaryDirectory(dir=base, prefix=".link-") as temporary:
        link = Path(temporary) / "current"
        link.symlink_to(target)
        os.replace(link, base / "current")


def request(base_url: str, path: str, *, post: bool = False) -> dict:
    parsed = urlparse(base_url)
    if (parsed.scheme != "http" or parsed.hostname not in {"127.0.0.1", "::1"}
            or parsed.username or parsed.password or parsed.query or parsed.fragment
            or parsed.path not in {"", "/"}):
        raise ValueError("Knowledge-Adresse muss eine lokale HTTP-Adresse sein")
    req = urllib.request.Request(base_url.rstrip("/") + path, method="POST" if post else "GET")
    # Kein Proxy und keine Weiterleitung: lokale Verwaltungsroute bleibt lokal.
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            return None
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect())
    deadline = time.monotonic() + 1200
    while True:
        try:
            with opener.open(req, timeout=600 if post else 15) as response:
                return json.load(response)
        except urllib.error.HTTPError as error:
            if not post or error.code != 409 or time.monotonic() >= deadline:
                raise
            # Ein vorheriger HTTP-Abbruch beendet den serverseitigen Aufbau
            # nicht. Auch der Rollback muss warten, bis sein Reload angenommen
            # und vollständig abgeschlossen wurde.
            time.sleep(5)


def export_public(repo: Path, revision: str, destination: Path) -> None:
    rows = git(repo, "ls-tree", "-r", "-z", revision, "--", "public").split(b"\0")
    for row in rows:
        if not row:
            continue
        metadata, encoded = row.split(b"\t", 1)
        relative = encoded.decode("utf-8")
        if (not safe_relative(relative) or private_path(relative)
                or not relative.endswith(".html")
                or metadata.split()[0] not in {b"100644", b"100755"}):
            raise ValueError("Unsicherer öffentlicher Git-Eintrag")
        path = destination / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(git(repo, "show", revision + ":" + relative))


def apply_validity_policy(destination: Path, manifest: dict) -> list[dict]:
    excluded = []
    for rule in manifest.get("export_policy", []):
        if rule.get("status") not in {"historical", "pending"} or not rule.get("reason"):
            raise ValueError("Unvollständige Gültigkeitsregel")
        for path in sorted((destination / "public").rglob("*.html")):
            relative = path.relative_to(destination / "public").as_posix()
            if not fnmatch.fnmatchcase(relative, rule["glob"]):
                continue
            archive = destination / "archive" / "public" / relative
            archive.parent.mkdir(parents=True, exist_ok=True)
            path.rename(archive)
            excluded.append({"path": relative, "status": rule["status"], "reason": rule["reason"]})
    return excluded


def withdraw_invalid_audits(destination: Path, audits: list[dict]) -> list[dict]:
    excluded = []
    by_path = {}
    for audit in audits:
        relative = audit.get("path", "")
        if not safe_relative(relative) or not relative.startswith("public/"):
            raise ValueError("Unsicherer öffentlicher Prüfpfad")
        if relative in by_path:
            raise ValueError("Mehrdeutige Fachprüfung einer öffentlichen Seite")
        by_path[relative] = audit
    for path in sorted((destination / "public").rglob("*.html")):
        relative = path.relative_to(destination).as_posix()
        if verified_audit(by_path.get(relative, {}), path.read_bytes()):
            continue
        archive = destination / "archive" / relative
        archive.parent.mkdir(parents=True, exist_ok=True)
        path.rename(archive)
        excluded.append({"path": relative.removeprefix("public/"), "status": "pending",
                         "reason": "Fachprüfung offen oder durch Inhalts-/Codeänderung entwertet"})
    return excluded


def load_audits(repo: Path, revision: str, manifest: dict, revisions: dict[str, str]) -> list[dict]:
    audits = []
    for path in manifest.get("audit_files", []):
        if not safe_relative(path) or not path.startswith("berichte/"):
            raise ValueError("Ungültige Prüfdatei")
        data = json.loads(git(repo, "show", revision + ":" + path))
        for audit in data["documents"]:
            audit = dict(audit)
            # Geänderte relevante Codepfade entziehen die Fachfreigabe. Der
            # Bericht bleibt erhalten, aber darf kein FAQ-Shortcut autorisieren.
            for check in audit.get("code", []):
                source = next(item for item in manifest["repositories"] if item["id"] == check["repository"])
                if not check.get("paths") or not all(safe_relative(p) for p in check["paths"]):
                    raise ValueError("Ungültiger Codeprüfpfad")
                if git(Path(source["path"]), "diff", "--name-only", check["revision"],
                       revisions[source["id"]], "--", *check["paths"]):
                    audit["gaps"] = [*audit.get("gaps", []), "Relevanter Produktcode seit der Fachprüfung geändert"]
            audits.append(audit)
    return audits


def summary(public: Path, report: dict, audits: list[dict]) -> dict:
    audit_by_path = {audit["path"]: audit for audit in audits}
    target_source = {doc["target"]: source["id"] for source in report["repositories"]
                     for doc in source["documents"]}
    rows = {source["id"]: {"id": source["id"], "label": source.get("label", source["id"]),
            "revision": source["revision"], "public_documents": 0,
            "verified_documents": 0, "pending_review": 0,
            "excluded_documents": source["internal"] + source["unknown"] + source["rejected"],
            "last_verified_at": None} for source in report["repositories"]}
    pending: set[str] = set()
    gaps = []

    def owner(relative: str) -> str:
        audit = audit_by_path.get("public/" + relative, {})
        code = audit.get("code", [])
        candidate = target_source.get(relative) or (code[0]["repository"] if code else "community-docs")
        return candidate if candidate in rows else "community-docs"

    for page in public.rglob("*.html"):
        relative = page.relative_to(public).as_posix()
        audit = audit_by_path.get("public/" + relative, {})
        row = rows[owner(relative)]
        row["public_documents"] += 1
        if verified_audit(audit, page.read_bytes()):
            row["verified_documents"] += 1
            row["last_verified_at"] = max(row["last_verified_at"] or "", audit["verified_at"])
        else:
            pending.add(relative)
        for gap in audit.get("operational_gaps", []):
            gaps.append({"source_id": relative, "title": "Offene Produktabweichung",
                         "reason": str(gap), "status": "pending_review"})
    exclusions = report.get("validity_exclusions", [])
    historical = sum(item["status"] == "historical" for item in exclusions)
    if historical:
        gaps.append({"source_id": "historische-analysen", "title": "Historische Buildanalysen",
                     "reason": f"{historical} historische Buildanalysen sind archiviert. Aktuelle Spieldaten kommen aus Deadlock Brain.",
                     "status": "excluded"})
    for item in exclusions:
        rows[owner(item["path"])]["excluded_documents"] += 1
        if item["status"] == "pending":
            pending.add(item["path"])
    for source in report["repositories"]:
        for doc in source["documents"]:
            if doc.get("status") == "pending_review":
                pending.add(doc["target"])
    for relative in sorted(pending):
        rows[owner(relative)]["pending_review"] += 1
        audit = audit_by_path.get("public/" + relative, {})
        reason = "; ".join(str(gap) for gap in audit.get("gaps", [])) or "Fachprüfung noch nicht vollständig oder nicht mehr gültig"
        gaps.append({"source_id": relative, "title": "Fachprüfung offen", "reason": reason,
                     "status": "pending_review"})
    repositories = list(rows.values())
    totals = {key: sum(row[key] for row in repositories) for key in
              ("public_documents", "verified_documents", "pending_review", "excluded_documents")}
    return {"schema_version": 1, "generated_at": now(), "repositories": repositories,
            "totals": totals, "gaps": gaps}


def refresh(config: dict, *, activate: bool = True) -> dict:
    repo, base = Path(config["repository"]), Path(config["base"])
    if not repo.is_absolute() or not base.is_absolute():
        raise ValueError("Absolute Repository- und Snapshotpfade erforderlich")
    base.mkdir(parents=True, exist_ok=True)
    with (base / ".refresh.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        old = (base / "current").resolve() if (base / "current").exists() else None
        previous = json.loads((base / "status-summary.json").read_text()) if (base / "status-summary.json").exists() else {}
        try:
            reference = config.get("ref", "origin/main")
            if not re.fullmatch(r"origin/[A-Za-z0-9_-]+|[0-9a-f]{40}", reference):
                raise ValueError("Export benötigt einen benannten Hauptzweig oder vollständigen Commit")
            if config.get("fetch", False) and reference.startswith("origin/"):
                git(repo, "fetch", "origin", reference.removeprefix("origin/"))
            revision = git(repo, "rev-parse", "--verify", reference + "^{commit}").decode().strip()
            manifest = json.loads(git(repo, "show", revision + ":public-sources.json"))
            revisions = freeze_revisions(manifest, fetch=config.get("fetch", False))
            fingerprint = hashlib.sha256(json.dumps({"docs": revision, "sources": revisions}, sort_keys=True).encode()).hexdigest()
            if (activate and previous.get("source_fingerprint") == fingerprint
                    and old and old.name == previous.get("active_snapshot")):
                live = request(config["knowledge_url"], "/healthz")
                if (live.get("generation") == previous.get("generation")
                        and live.get("faq_generation") == previous.get("faq_generation")):
                    previous.update(generated_at=now(), refresh_status="ok")
                    atomic_json(base / "status-summary.json", previous)
                    return previous
            with tempfile.TemporaryDirectory(dir=base, prefix=".snapshot-") as temp:
                staging = Path(temp)
                export_public(repo, revision, staging)
                if validate_root(staging):
                    raise ValueError("Vollständiger öffentlicher Redaktionsexport nicht gültig")
                report = import_sources(manifest, staging, revisions=revisions)
                report["validity_exclusions"] = apply_validity_policy(staging, manifest)
                revisions = {source["id"]: source["revision"] for source in report["repositories"]}
                audits = load_audits(repo, revision, manifest, revisions)
                report["validity_exclusions"].extend(withdraw_invalid_audits(staging, audits))
                errors = validate_root(staging, require_existing_targets=False)
                if errors:
                    raise ValueError("Öffentlicher Korpusvertrag nicht erfüllt")
                generation = corpus_digest(staging / "public")
                faq = faq_manifest(staging / "public", audits, policy_revision=revision)
                faq_hash = hashlib.sha256(json.dumps(faq, sort_keys=True).encode()).hexdigest()
                snapshot = f"{revision[:12]}-{report['identity']}-{generation[:12]}-{faq_hash[:12]}"
                write_json(staging / "source-manifest.json", report)
                write_json(staging / "faq-manifest.json", faq)
                faq_generation = faq_digest(staging)
                state = summary(staging / "public", report, audits)
                destination = base / snapshot
                if destination.exists():
                    if (corpus_digest(destination / "public") != generation
                            or json.loads((destination / "faq-manifest.json").read_text()) != faq):
                        raise ValueError("Bestehender Snapshot stimmt nicht mit Export überein")
                else:
                    # TemporaryDirectory räumt anschließend nur das leere
                    # Reservierungsverzeichnis auf; veröffentlichte Daten bleiben.
                    staging.rename(destination)
                    staging.mkdir()
                if not activate:
                    state.update(prepared_snapshot=snapshot, generation=generation)
                    return state
                live = request(config["knowledge_url"], "/healthz")
                switch_current(base, destination)
                confirmed = False
                try:
                    if live.get("generation") != generation or live.get("faq_generation") != faq_generation:
                        request(config["knowledge_url"], "/internal/reload", post=True)
                    live = request(config["knowledge_url"], "/healthz")
                    if live.get("generation") != generation or live.get("faq_generation") != faq_generation:
                        raise ValueError("Aktiver Index bestätigt den Snapshot nicht")
                    confirmed = True
                    state.update(active_snapshot=snapshot, refresh_status="ok", generation=generation,
                                 faq_generation=faq_generation, source_fingerprint=fingerprint)
                    atomic_json(base / "status-summary.json", state)
                except Exception:
                    if old:
                        try:
                            switch_current(base, old)
                            request(config["knowledge_url"], "/internal/reload", post=True)
                            live = request(config["knowledge_url"], "/healthz")
                            if live.get("generation") != corpus_digest(old / "public") or live.get("faq_generation") != faq_digest(old):
                                raise ValueError("Rollback nicht bestätigt")
                        except Exception:
                            previous["last_confirmed_snapshot"] = previous.pop("active_snapshot", None)
                            raise ValueError("Rollback des Wissensindex nicht bestätigt") from None
                    elif confirmed:
                        # Erster bestätigter Index, aber Statuswrite gescheitert:
                        # Es existiert kein alter Snapshot für einen Rollback.
                        # Der Fehlerstatus muss den tatsächlich aktiven nennen.
                        previous = state
                    else:
                        (base / "current").unlink(missing_ok=True)
                        previous.pop("active_snapshot", None)
                    raise
                return state
        except Exception:
            previous.update(schema_version=1, generated_at=now(), refresh_status="failed")
            atomic_json(base / "status-summary.json", previous)
            raise


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--prepare-only", action="store_true")
    args = parser.parse_args()
    state = refresh(json.loads(args.config.read_text()), activate=not args.prepare_only)
    print(json.dumps({key: state[key] for key in ("active_snapshot", "prepared_snapshot", "refresh_status") if key in state}))


if __name__ == "__main__":
    main()
