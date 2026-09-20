#!/usr/bin/env python3
"""Reproduzierbarer Import freigegebener Nutzerdokumente aus Git-Commits.

Nur das Manifest erteilt eine positive Freigabe. Explizite private Audiences
haben Vorrang. Quelldateien, Arbeitsbäume und bestehende Snapshots bleiben
unverändert; jeder Export entsteht vollständig neu.
"""
from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import re
import subprocess
import tempfile
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath

import validate_corpus

PUBLIC = {"public", "streamer", "viewer", "community", "user", "nutzer"}
PRIVATE_PARTS = {"internal", "intern", "private", ".tasks", "node_modules", "vendor", "third_party", ".repos", "_archive"}
MAX_BYTES = 2 * 1024 * 1024


def git(repo: Path, *args: str) -> bytes:
    result = subprocess.run(
        ["git", "--no-replace-objects", "-C", str(repo), *args], capture_output=True, check=False,
        timeout=60,
    )
    if result.returncode:
        raise ValueError("Quell-Repository oder Git-Revision nicht verfügbar")
    return result.stdout


def safe_relative(value: str) -> bool:
    path = PurePosixPath(value)
    return bool(value) and not path.is_absolute() and not any(
        part in {".", "..", ""} for part in value.split("/")
    ) and "\\" not in value and not any(ord(c) < 32 for c in value)


def document_path(path: str) -> bool:
    return Path(path).suffix.lower() in {".md", ".html", ".htm"}


def private_path(path: str) -> bool:
    parts = {part.lower() for part in PurePosixPath(path).parts}
    name = PurePosixPath(path).name.lower()
    return bool(parts & PRIVATE_PARTS) or any(
        term in name for term in ("secret", "credential", ".env", "private-key")
    )


def frontmatter(raw: str) -> tuple[dict[str, str], str]:
    raw = raw.replace("\r\n", "\n")
    if not raw.startswith("---\n"):
        return {}, raw
    end = raw.find("\n---\n", 4)
    if end < 0:
        raise ValueError("Unvollständige Metadaten")
    meta = {}
    for line in raw[4:end].splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            if key.strip() in meta:
                raise ValueError("Mehrdeutige Metadaten")
            meta[key.strip()] = value.strip().strip("\"'")
    return meta, raw[end + 5:]


class TextPage(HTMLParser):
    """Passiver HTML-Inhalt; keine Assets, Kommentare, Skripte oder Includes."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.blocks: list[tuple[int, str]] = []
        self.parts: list[str] = []
        self.heading = 0
        self.hidden = 0
        self.in_body = False
        self.audiences: list[str] = []

    def flush(self) -> None:
        text = re.sub(r"\s+", " ", "".join(self.parts)).strip()
        if text:
            self.blocks.append((self.heading, text))
        self.parts = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs = dict(attrs)
        if tag == "meta" and attrs.get("name", "").lower() in {"audience", "visibility"}:
            self.audiences.append((attrs.get("content") or "").lower())
        if tag == "body":
            self.in_body = True
        if tag in {"script", "style", "nav", "footer", "noscript", "svg"}:
            self.flush()
            self.hidden += 1
        if self.hidden or not self.in_body:
            return
        if tag in {"p", "div", "section", "article", "li", "tr", "br", "h1", "h2", "h3", "h4", "h5", "h6"}:
            self.flush()
            self.heading = int(tag[1]) if re.fullmatch(r"h[1-6]", tag) else 0
        if tag in {"td", "th"}:
            self.parts.append(" | ")

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "nav", "footer", "noscript", "svg"}:
            self.hidden = max(0, self.hidden - 1)
            return
        if self.hidden:
            return
        if tag in {"p", "div", "section", "article", "li", "tr", "body", "h1", "h2", "h3", "h4", "h5", "h6"}:
            self.flush()
            self.heading = 0
        if tag == "body":
            self.in_body = False

    def handle_data(self, data: str) -> None:
        if self.in_body and not self.hidden:
            self.parts.append(data)


def freeze_revisions(config: dict, *, fetch: bool = False) -> dict[str, str]:
    # Erst alle Aktualisierungen abschließen, danach den gesamten Lauf an
    # unveränderliche Commits binden – auch repoübergreifende Codeprüfungen.
    for source in config["repositories"]:
        if not Path(source["path"]).is_absolute():
            raise ValueError("Repo-Pfad muss absolut sein")
        ref = source.get("ref", "origin/main")
        if not re.fullmatch(r"origin/[A-Za-z0-9_-]+|HEAD", ref):
            raise ValueError("Nur benannte Hauptzweige sind zulässig")
        if source.get("inventory_only") and source.get("public"):
            raise ValueError("Ausgeschlossene Repository-Quelle darf keine öffentlichen Importregeln haben")
        if fetch and ref.startswith("origin/") and not source.get("inventory_only"):
            git(Path(source["path"]), "fetch", "origin", ref.removeprefix("origin/"))
    return {source["id"]: git(Path(source["path"]), "rev-parse", "--verify",
                                   source.get("ref", "origin/main") + "^{commit}").decode().strip()
                 for source in config["repositories"]}


def import_sources(config: dict, destination: Path, *, fetch: bool = False,
                   revisions: dict[str, str] | None = None) -> dict:
    report = {"version": 1, "repositories": [], "imported": 0}
    selected_targets: set[str] = set()
    identity = hashlib.sha256(json.dumps(config, sort_keys=True).encode())
    revisions = revisions if revisions is not None else freeze_revisions(config, fetch=fetch)
    curated = {}
    for target in config.get("managed_targets", []):
        if not safe_relative(target) or not target.endswith(".html"):
            raise ValueError("Ungültiges verwaltetes Ziel")
        existing = destination / "public" / target
        if existing.exists():
            curated[target] = existing.read_text(encoding="utf-8")
            # Im Suchsnapshot gibt es weder alte SSOT-Kopien noch synthetische
            # Ersatzantworten. Die tracked Redaktion wird nicht verändert.
            existing.unlink()
    for source in config["repositories"]:
        repo = Path(source["path"])
        if not repo.is_absolute():
            raise ValueError("Repo-Pfad muss absolut sein")
        ref = source.get("ref", "origin/main")
        if not re.fullmatch(r"origin/[A-Za-z0-9_-]+|HEAD", ref):
            raise ValueError("Nur benannte Hauptzweige sind zulässig")
        revision = revisions[source["id"]]
        identity.update((source["id"] + revision).encode())
        rows = git(repo, "ls-tree", "-r", "-z", revision).split(b"\0")
        summary = {"id": source["id"], "label": source.get("label", source["id"]),
                   "revision": revision, "public": 0,
                   "internal": 0, "unknown": 0, "represented": 0,
                   "imported": 0, "rejected": 0, "pending_review": 0, "documents": []}
        for row in rows:
            if not row:
                continue
            metadata, path_bytes = row.split(b"\t", 1)
            path = path_bytes.decode("utf-8")
            if not document_path(path):
                continue
            if private_path(path):
                summary["internal"] += 1
                continue
            rule = next((rule for rule in source.get("public", [])
                         if fnmatch.fnmatchcase(path, rule["glob"])), None)
            if rule is None:
                summary["unknown"] += 1
                continue
            if not rule.get("evidence"):
                raise ValueError("Positive Audience-Begründung fehlt")
            if metadata.split()[0] != b"100644" and metadata.split()[0] != b"100755":
                summary["rejected"] += 1
                continue
            if rule.get("represented"):
                size = int(git(repo, "cat-file", "-s", revision + ":" + path))
                if size > MAX_BYTES:
                    summary["rejected"] += 1
                    continue
                represented_raw = git(repo, "show", revision + ":" + path).decode("utf-8")
                represented_meta = frontmatter(represented_raw)[0]
                represented_html = TextPage()
                represented_html.feed(represented_raw)
                if (any(represented_meta[key].lower() not in PUBLIC for key in ("audience", "visibility") if key in represented_meta)
                        or any(value not in PUBLIC for value in represented_html.audiences)):
                    summary["rejected"] += 1
                    if source["id"] == "community-docs" and path.startswith("public/"):
                        (destination / path).unlink(missing_ok=True)
                    continue
                summary["public"] += 1
                summary["represented"] += 1
                if rule.get("represented_by"):
                    summary.setdefault("represented_documents", []).append({
                        "path": path, "target": rule["represented_by"],
                        "committed_revision": revision,
                        "source_sha256": hashlib.sha256(represented_raw.encode()).hexdigest(),
                    })
                continue
            target = rule.get("target") or f"{rule.get('target_prefix', 'quellen/' + source['id'])}/{PurePosixPath(path).stem.lower()}.html"
            if not safe_relative(target) or private_path(target) or not target.endswith(".html"):
                raise ValueError("Ungültiger Zielpfad")
            if target in selected_targets:
                raise ValueError("Doppelte öffentliche Zieladresse")
            selected_targets.add(target)
            record = {"path": path, "target": target}
            summary["documents"].append(record)
            size = int(git(repo, "cat-file", "-s", revision + ":" + path))
            if size > MAX_BYTES:
                record["status"] = "rejected_size"
                summary["rejected"] += 1
                continue
            raw = git(repo, "show", revision + ":" + path).decode("utf-8")
            try:
                if rule.get("use_curated"):
                    # Das geprüfte öffentliche HTML liegt bereits im
                    # committeten Docs-Export. Keine freien Repo-Rohtexte.
                    if target not in curated:
                        raise ValueError("Redigierte öffentliche Anleitung fehlt")
                    metadata = frontmatter(raw)[0]
                    audience = metadata.get("audience")
                    if any(metadata[key].lower() not in PUBLIC for key in ("audience", "visibility") if key in metadata):
                        raise ValueError("Nicht öffentliche Audience")
                    if rule.get("require_audience") and (audience or "").lower() not in PUBLIC:
                        raise ValueError("Öffentliche Audience fehlt")
                    check_html = TextPage()
                    check_html.feed(raw)
                    if any(value not in PUBLIC for value in check_html.audiences):
                        raise ValueError("Nicht öffentliche Audience")
                    page = curated[target]
                else:
                    raise ValueError("Redaktionelle HTML-Fassung und Prüfung erforderlich")
                with tempfile.TemporaryDirectory() as tmp:
                    check = Path(tmp) / "public" / target
                    check.parent.mkdir(parents=True)
                    check.write_text(page, encoding="utf-8")
                    # Einzelseitenprüfung erhält den logischen Pfad. Verlinkte
                    # Seiten werden im vollständigen Redaktionsexport geprüft;
                    # sie müssen nicht selbst zum aktiven Suchbestand gehören.
                    errors = validate_corpus.validate_root(Path(tmp), require_existing_targets=False)
                    if errors:
                        raise ValueError("Öffentlicher HTML-/Redactionvertrag nicht erfüllt")
            except ValueError as error:
                record["status"] = "rejected"
                record["reason"] = str(error)
                summary["rejected"] += 1
                continue
            summary["public"] += 1
            record["source_sha256"] = hashlib.sha256(raw.encode()).hexdigest()
            record["content_sha256"] = hashlib.sha256(page.encode()).hexdigest()
            record["committed_revision"] = revision
            review = source.get("reviews", {}).get(path)
            if (not review
                    or review.get("source_sha256") != hashlib.sha256(raw.encode()).hexdigest()
                    or review.get("content_sha256") != hashlib.sha256(page.encode()).hexdigest()):
                record["status"] = "pending_review"
                record["reason"] = "Inhalt noch nicht gegen den aktuellen Produktstand geprüft"
                summary["pending_review"] += 1
                continue
            checks = review.get("code", [])
            if not checks or not review.get("verified_at"):
                raise ValueError("Prüfnachweis ohne Codebezug oder Prüfdatum")
            stale = False
            for check in checks:
                code_source = next(item for item in config["repositories"] if item["id"] == check["repository"])
                code_repo = Path(code_source["path"])
                code_head = revisions[code_source["id"]]
                if not check.get("paths") or not all(safe_relative(p) for p in check["paths"]):
                    raise ValueError("Prüfnachweis ohne sichere Codepfade")
                if git(code_repo, "diff", "--name-only", check["revision"], code_head, "--", *check["paths"]):
                    stale = True
            if stale:
                record["status"] = "pending_review"
                record["reason"] = "Verknüpfter Produktcode seit der Prüfung geändert"
                summary["pending_review"] += 1
                continue
            output = destination / "public" / target
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(page, encoding="utf-8")
            record["status"] = "imported"
            record["verified_at"] = review["verified_at"]
            summary["imported"] += 1
            report["imported"] += 1
        report["repositories"].append(summary)
    report["identity"] = identity.hexdigest()[:20]
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--destination", required=True, type=Path)
    parser.add_argument("--report", required=True, type=Path)
    parser.add_argument("--fetch", action="store_true")
    args = parser.parse_args()
    config = json.loads(args.config.read_text(encoding="utf-8"))
    report = import_sources(config, args.destination, fetch=args.fetch)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(report["identity"])


if __name__ == "__main__":
    main()
