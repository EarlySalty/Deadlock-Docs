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
        self.section_depth: int | None = None
        self.heading: list[str] | None = None
        self.title: list[str] = []
        self.questions: list[tuple[str, str]] = []
        self.sections: dict[str, list[str]] = {}
        self.section_counts: dict[str, int] = {}
        self.unsuitable_sections: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"meta", "link", "br", "hr", "img", "input"}:
            return
        if tag == "section" and self.stack and self.stack[-1] == "main":
            self.section = dict(attrs).get("id")
            self.section_depth = len(self.stack)
            if self.section:
                self.section_counts[self.section] = self.section_counts.get(self.section, 0) + 1
                self.sections[self.section] = []
        if self.section and tag in {"a", "table", "nav"}:
            self.unsuitable_sections.add(self.section)
        if (tag == "h2" and self.section
                and len(self.stack) == self.section_depth + 1):
            self.heading = []
        self.stack.append(tag)

    def handle_data(self, data: str) -> None:
        if "title" in self.stack:
            self.title.append(data)
        if self.heading is not None:
            self.heading.append(data)
        elif self.section:
            self.sections[self.section].append(data)

    def handle_endtag(self, tag: str) -> None:
        if self.section and tag in {"p", "li", "ul", "ol", "br", "h2", "h3", "section"}:
            self.sections[self.section].append("\n")
        if tag == "h2" and self.heading is not None:
            question = " ".join("".join(self.heading).split())
            if question.endswith("?") and self.section:
                self.questions.append((self.section, question))
            self.heading = None
        closing_index = (len(self.stack) - 1 - self.stack[::-1].index(tag)
                         if tag in self.stack else None)
        if tag == "section" and closing_index == self.section_depth:
            self.section = None
            self.section_depth = None
        if closing_index is not None:
            self.stack = self.stack[:closing_index]


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
        standards: dict[str, dict] = {}
        for standard in audit.get("standard_answers", []):
            if not isinstance(standard, dict):
                raise ValueError("Ungültiger Standardantwort-Eintrag")
            section = standard.get("section_id")
            question = standard.get("question")
            answer = standard.get("answer")
            scope = standard.get("scope")
            if not all(isinstance(value, str) and value.strip()
                       for value in (section, question, answer, scope)):
                raise ValueError("Standardantwort braucht Abschnitt, Frage, Antwort und Geltungsbereich")
            if (section in standards or parser.section_counts.get(section) != 1
                    or section in parser.unsuitable_sections):
                raise ValueError("Standardantwort braucht einen eindeutigen, selbstständigen Textabschnitt")
            source_text = " ".join("".join(parser.sections[section]).split())
            if " ".join(answer.split()) != source_text:
                raise ValueError("Standardantwort muss den vollständigen geprüften Abschnitt wiedergeben")
            if (len(answer.encode("utf-16-le")) // 2 > 1600
                    or len(scope.encode("utf-16-le")) // 2 > 800
                    or not question.endswith("?")):
                raise ValueError("Ungültige Länge oder Frage der Standardantwort")
            standards[section] = standard
        questions = dict(parser.questions)
        questions.update({section: standard["question"] for section, standard in standards.items()})
        for section, question in questions.items():
            key = (relative, section)
            if parser.section_counts.get(section) != 1 or key in seen:
                continue
            seen.add(key)
            public_path = relative.removeprefix("public/")
            entry = {"id": f"faq:{public_path}#{section}", "question": question,
                     "path": public_path, "section_id": section,
                     "source_sha256": hashlib.sha256(content).hexdigest()}
            if section in standards:
                entry["standard_answer"] = standards[section]["answer"]
                entry["standard_answer_scope"] = standards[section]["scope"]
            entries.append(entry)
    return {"schema_version": 1, "policy_revision": policy_revision,
            "entries": sorted(entries, key=lambda entry: (entry["path"], entry["section_id"]))}


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
