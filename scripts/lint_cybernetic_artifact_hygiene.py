#!/usr/bin/env python3
"""Hygiene lint for generated cybernetic control artifacts.

The lint checks objective artifact noise only. It does not decide whether PFB,
RSC, setpoint, plan granularity, or review semantics are adequate.
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)
ENUM_STATUS_RE = re.compile(r"(?im)^\s*Status\s*:\s*`?([^`\n]*\s/\s[^`\n]*)`?\s*$")
PLACEHOLDER_RE = re.compile(r"\[[^\]\n]{3,}\](?!\()|YYYY-MM-DD(?:-slug|-<slug>)?")
DUPLICATE_PARAGRAPH_MIN_CHARS = 120

RESPONSE_ONLY_PROMPTS = (
    "$orchestrating-cybernetic-pregoal",
    "$writing-cybernetic-goals",
    "$designing-cybernetic-solutions",
    "/goal Execute",
    "Recommended next step:",
    "Response-only handoff:",
)

DEFENSIVE_CLAUSES = (
    "do not",
    "must not",
    "stop if",
    "unless",
    "if missing",
    "if unavailable",
    "not approved",
    "cannot",
    "forbid",
)

SIZE_BUDGETS = {
    "requirements": (220, 400),
    "design": (260, 500),
    "goal": (220, 380),
    "plan": (350, 700),
    "review": (260, 500),
}


@dataclass
class Finding:
    path: Path
    line: int
    message: str

    def format(self, prefix: str) -> str:
        return f"{prefix}: {self.path}:{self.line}: {self.message}"


def is_template_path(path: Path) -> bool:
    lowered_parts = [part.casefold() for part in path.parts]
    return "assets" in lowered_parts and "template" in path.name.casefold()


def line_number(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def artifact_kind(path: Path) -> str:
    lowered = "/".join(path.parts).casefold()
    name = path.name.casefold()
    if "requirements" in lowered or "requirements" in name:
        return "requirements"
    if "design" in lowered or "design" in name:
        return "design"
    if "goals" in lowered or "goal" in name:
        return "goal"
    if "plans" in lowered or "plan" in name:
        return "plan"
    if "control-reviews" in lowered or "review" in name:
        return "review"
    return "artifact"


def duplicate_headings(path: Path, text: str) -> list[Finding]:
    seen: dict[str, tuple[int, str]] = {}
    findings: list[Finding] = []
    for match in HEADING_RE.finditer(text):
        heading = match.group(2).strip().rstrip("#").strip()
        normalized = f"{len(match.group(1))}:{heading.casefold()}"
        if normalized in seen:
            findings.append(Finding(path, line_number(text, match.start()), f"duplicate heading: {heading}"))
        else:
            seen[normalized] = (line_number(text, match.start()), heading)
    return findings


def normalize_paragraph(paragraph: str) -> str:
    return re.sub(r"\s+", " ", paragraph).strip()


def duplicate_paragraphs(path: Path, text: str) -> list[Finding]:
    paragraphs = re.split(r"\n\s*\n", text)
    seen: dict[str, int] = {}
    findings: list[Finding] = []
    offset = 0
    for paragraph in paragraphs:
        normalized = normalize_paragraph(paragraph)
        paragraph_start = text.find(paragraph, offset)
        offset = paragraph_start + len(paragraph) if paragraph_start >= 0 else offset
        if len(normalized) < DUPLICATE_PARAGRAPH_MIN_CHARS:
            continue
        if normalized.startswith("#") or normalized.startswith("|"):
            continue
        if normalized in seen:
            findings.append(Finding(path, line_number(text, max(paragraph_start, 0)), "duplicate paragraph"))
        else:
            seen[normalized] = line_number(text, max(paragraph_start, 0))
    return findings


def hard_findings(path: Path, text: str) -> list[Finding]:
    findings: list[Finding] = []

    for match in ENUM_STATUS_RE.finditer(text):
        findings.append(Finding(path, line_number(text, match.start()), "unresolved enum status"))

    for match in PLACEHOLDER_RE.finditer(text):
        findings.append(Finding(path, line_number(text, match.start()), "unresolved placeholder"))

    if "runtime-goals" not in "/".join(path.parts).casefold() and path.suffix != ".goal":
        lowered = text.casefold()
        for prompt in RESPONSE_ONLY_PROMPTS:
            index = lowered.find(prompt.casefold())
            if index >= 0:
                findings.append(Finding(path, line_number(text, index), f"response-only prompt leaked into artifact: {prompt}"))

    findings.extend(duplicate_headings(path, text))
    findings.extend(duplicate_paragraphs(path, text))
    findings.extend(size_errors(path, text))
    return findings


def size_errors(path: Path, text: str) -> list[Finding]:
    kind = artifact_kind(path)
    soft, hard = SIZE_BUDGETS.get(kind, (300, 600))
    line_count = len(text.splitlines())
    if line_count <= hard:
        return []
    if "## Artifact Size Justification" in text:
        return []
    return [Finding(path, 1, f"exceeds hard size budget for {kind}: {line_count} lines > {hard}")]


def warnings(path: Path, text: str) -> list[Finding]:
    findings: list[Finding] = []
    kind = artifact_kind(path)
    soft, hard = SIZE_BUDGETS.get(kind, (300, 600))
    line_count = len(text.splitlines())
    if line_count > soft:
        findings.append(Finding(path, 1, f"exceeds soft size budget for {kind}: {line_count} lines > {soft}"))

    nonblank_lines = [line for line in text.splitlines() if line.strip()]
    if nonblank_lines:
        lowered_lines = [line.casefold() for line in nonblank_lines]
        defensive_count = sum(1 for line in lowered_lines if any(clause in line for clause in DEFENSIVE_CLAUSES))
        density = defensive_count / len(nonblank_lines)
        if defensive_count >= 5 and density > 0.20:
            findings.append(Finding(path, 1, f"high defensive clause density: {defensive_count}/{len(nonblank_lines)}"))
    return findings


def lint_paths(paths: list[Path]) -> tuple[list[Finding], list[Finding], list[Finding]]:
    errors: list[Finding] = []
    warns: list[Finding] = []
    skips: list[Finding] = []
    for path in paths:
        if is_template_path(path):
            skips.append(Finding(path, 1, "template file; generated-artifact hygiene lint skipped"))
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except FileNotFoundError:
            errors.append(Finding(path, 1, "missing file"))
            continue
        errors.extend(hard_findings(path, text))
        warns.extend(warnings(path, text))
    return errors, warns, skips


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+")
    args = parser.parse_args()

    errors, warns, skips = lint_paths([Path(path) for path in args.paths])
    print("FAIL" if errors else "PASS")
    for finding in errors:
        print(finding.format("ERROR"))
    for finding in warns:
        print(finding.format("WARN"))
    for finding in skips:
        print(finding.format("SKIP"))
    return 2 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
