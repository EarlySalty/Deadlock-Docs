"""Öffentliche Snapshot-Identität und redaktionelle Nachweise, ohne Modellaufruf."""
from __future__ import annotations

import hashlib
import json
from html.parser import HTMLParser
from pathlib import Path


def corpus_digest(public: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(public.rglob("*.html"), key=lambda p: p.relative_to(public).as_posix()):
        if path.is_symlink() or any(parent.is_symlink() for parent in path.parents if parent != public.parent):
            raise ValueError("Symlinks sind im öffentlichen Snapshot nicht zulässig")
        relative = path.relative_to(public).as_posix()
        file_hash = hashlib.sha256(path.read_bytes()).hexdigest()
        digest.update(relative.encode("utf-8") + b"\0" + file_hash.encode("ascii") + b"\n")
    return digest.hexdigest()


class PublicSections(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[str] = []
        self.section: str | None = None
        self.heading: list[str] | None = None
        self.title: list[str] = []
        self.questions: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"meta", "link", "br", "hr", "img", "input"}:
            return
        if tag == "section" and self.stack and self.stack[-1] == "main":
            self.section = dict(attrs).get("id")
        if tag == "h2" and self.section and self.stack and self.stack[-1] == "section":
            self.heading = []
        self.stack.append(tag)

    def handle_data(self, data: str) -> None:
        if "title" in self.stack:
            self.title.append(data)
        if self.heading is not None:
            self.heading.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "h2" and self.heading is not None:
            question = " ".join("".join(self.heading).split())
            if question.endswith("?") and self.section:
                self.questions.append((self.section, question))
            self.heading = None
        if tag == "section":
            self.section = None
        if tag in self.stack:
            self.stack = self.stack[:len(self.stack) - 1 - self.stack[::-1].index(tag)]


def verified_audit(audit: dict, content: bytes) -> bool:
    claims = audit.get("claims", [])
    return bool(
        audit.get("verified_at")
        and audit.get("code")
        and claims
        and all(claim.get("verdict") in {"verified", "removed"} for claim in claims)
        and not audit.get("gaps")
        and audit.get("content_sha256") == hashlib.sha256(content).hexdigest()
    )


def faq_manifest(public: Path, audits: list[dict], *, policy_revision: str) -> dict:
    entries = []
    seen: set[tuple[str, str]] = set()
    for audit in audits:
        relative = audit.get("path", "")
        if not relative.startswith("public/") or ".." in Path(relative).parts:
            continue
        path = public / relative.removeprefix("public/")
        if not path.is_file() or path.is_symlink():
            continue
        content = path.read_bytes()
        if not verified_audit(audit, content):
            continue
        parser = PublicSections()
        parser.feed(content.decode("utf-8"))
        ids = [section for section, _ in parser.questions]
        for section, question in parser.questions:
            key = (relative, section)
            if ids.count(section) != 1 or key in seen:
                continue
            seen.add(key)
            entries.append({"question": question, "path": relative.removeprefix("public/"),
                            "section_id": section, "source_sha256": hashlib.sha256(content).hexdigest()})
    return {"schema_version": 1, "policy_revision": policy_revision,
            "entries": sorted(entries, key=lambda entry: (entry["path"], entry["section_id"]))}


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
