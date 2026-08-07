"""Validate Open Product Format v0.2.0 documents and packs.

Stdlib only. The parser intentionally supports the small YAML subset OPF uses.
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass, field
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

from . import OKF_VERSION, OPF_VERSION

TYPES = {"product", "product-concept"}
KINDS = {
    "user",
    "problem",
    "promise",
    "outcome",
    "journey",
    "moment",
    "surface",
    "state",
    "interaction",
    "content",
    "accessibility",
    "capability",
    "contract",
    "constraint",
    "authority-boundary",
    "slice",
    "acceptance",
    "decision",
    "risk",
}
STATUSES = {"concept", "shaping", "validated", "building", "operating", "retired"}
TIERS = {"human", "job", "agent"}
REF_FIELDS = {
    "intent",
    "research",
    "users",
    "outcomes",
    "first_slice",
    "proof",
    "authority",
    "serves",
    "journeys",
    "moments",
    "surfaces",
    "states",
    "interactions",
    "includes",
    "depends_on",
    "supersedes",
}


@dataclass
class Problem:
    level: str
    rule: str
    detail: str


@dataclass
class Report:
    path: Path
    problems: list[Problem] = field(default_factory=list)

    @property
    def errors(self) -> list[Problem]:
        return [problem for problem in self.problems if problem.level == "error"]


def parse_frontmatter(text: str) -> dict[str, Any]:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    return _parse_yaml_block(text[3:end])


def _parse_yaml_block(block: str) -> dict[str, Any]:
    out: dict[str, Any] = {}
    stack: list[tuple[int, dict[str, Any]]] = [(-1, out)]
    lines = block.splitlines()
    i = 0
    while i < len(lines):
        raw = lines[i]
        if not raw.strip() or raw.lstrip().startswith("#"):
            i += 1
            continue
        indent = len(raw) - len(raw.lstrip())
        line = raw.strip()
        while len(stack) > 1 and indent <= stack[-1][0]:
            stack.pop()
        container = stack[-1][1]
        if line.startswith("- ") or ":" not in line:
            i += 1
            continue
        key, _, value = line.partition(":")
        key, value = key.strip(), value.strip()
        if value == "":
            j = i + 1
            kind = "empty"
            while j < len(lines):
                if not lines[j].strip() or lines[j].lstrip().startswith("#"):
                    j += 1
                    continue
                next_indent = len(lines[j]) - len(lines[j].lstrip())
                if next_indent <= indent:
                    break
                kind = "list" if lines[j].strip().startswith("- ") else "map"
                break
            if kind == "list":
                items: list[str] = []
                j = i + 1
                while j < len(lines):
                    if not lines[j].strip() or lines[j].lstrip().startswith("#"):
                        j += 1
                        continue
                    next_indent = len(lines[j]) - len(lines[j].lstrip())
                    if next_indent <= indent or not lines[j].strip().startswith("- "):
                        break
                    items.append(lines[j].strip()[2:].strip().strip("'\""))
                    j += 1
                container[key] = items
                i = j
                continue
            if kind == "map":
                child: dict[str, Any] = {}
                container[key] = child
                stack.append((indent, child))
                i += 1
                continue
            container[key] = {}
            i += 1
            continue
        if value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            container[key] = [
                part.strip().strip("'\"") for part in inner.split(",") if part.strip()
            ]
        elif value.lower() in {"null", "none", "~"}:
            container[key] = None
        else:
            container[key] = value.strip("'\"")
        i += 1
    return out


def _items(value: Any) -> list[str]:
    if isinstance(value, list):
        return [item for item in value if isinstance(item, str) and item]
    if isinstance(value, str) and value:
        return [value]
    return []


def _missing(fm: dict[str, Any], fields: set[str]) -> list[str]:
    return sorted(field for field in fields if not _items(fm.get(field)))


def validate_document(fm: dict[str, Any], *, face: bool = False) -> list[Problem]:
    problems: list[Problem] = []
    if not fm:
        return [
            Problem("error", "frontmatter", "OPF documents require YAML frontmatter")
        ]

    okf_version = str(fm.get("okf_version") or "")
    if okf_version != OKF_VERSION:
        problems.append(
            Problem("error", "okf_base", f"okf_version must be {OKF_VERSION!r}")
        )

    opf_version = str(fm.get("opf_version") or "")
    if not re.fullmatch(r"\d+\.\d+\.\d+", opf_version):
        problems.append(Problem("error", "opf_version", "opf_version must use X.Y.Z"))
    elif ".".join(opf_version.split(".")[:2]) != okf_version:
        problems.append(
            Problem("error", "version_alignment", "OPF major.minor must match OKF")
        )
    elif opf_version != OPF_VERSION:
        problems.append(
            Problem("warn", "opf_version", f"validator implements {OPF_VERSION}")
        )

    if fm.get("type") not in TYPES:
        problems.append(
            Problem("error", "type", f"type must be one of {sorted(TYPES)}")
        )
    if not str(fm.get("title") or "").strip():
        problems.append(Problem("error", "title", "title is required"))
    if not str(fm.get("opf_id") or "").startswith("opf:"):
        problems.append(
            Problem("error", "opf_id", "stable opf_id must start with 'opf:'")
        )

    verified = fm.get("verified") or {}
    by = str(verified.get("by") or "")
    if by.split(":", 1)[0] not in TIERS:
        problems.append(
            Problem(
                "error", "verified.by", "verified.by must start human:, job:, or agent:"
            )
        )
    if not str(verified.get("method") or "").strip():
        problems.append(
            Problem("error", "verified.method", "verification method is required")
        )

    if face:
        if fm.get("type") != "product":
            problems.append(
                Problem("error", "face_type", "index.md must use type: product")
            )
        status = str(fm.get("status") or "")
        if status not in STATUSES:
            problems.append(
                Problem("error", "status", f"status must be one of {sorted(STATUSES)}")
            )
        if status in {"shaping", "validated", "building", "operating"}:
            required = {
                "intent",
                "users",
                "problem",
                "promise",
                "outcomes",
                "first_slice",
                "non_goals",
                "proof",
                "authority",
            }
            for field in _missing(fm, required):
                problems.append(
                    Problem(
                        "error",
                        "product_admission",
                        f"status {status!r} requires {field}",
                    )
                )
    elif fm.get("type") == "product-concept":
        kind = str(fm.get("kind") or "")
        if kind not in KINDS:
            problems.append(
                Problem("error", "kind", f"kind must be one of {sorted(KINDS)}")
            )
        if kind == "surface":
            for field in _missing(fm, {"serves", "states", "proof"}):
                problems.append(
                    Problem(
                        "error", "surface_traceability", f"surface requires {field}"
                    )
                )
        if kind == "slice":
            for field in _missing(fm, {"serves", "includes", "proof", "non_goals"}):
                problems.append(
                    Problem("error", "slice_traceability", f"slice requires {field}")
                )
    return problems


def references(fm: dict[str, Any]) -> set[str]:
    refs: set[str] = set()
    for ref_field in REF_FIELDS:
        refs.update(
            item for item in _items(fm.get(ref_field)) if item.startswith("opf:")
        )
    return refs


def validate_pack(root: Path, *, strict: bool = False) -> list[Report]:
    root = root.resolve()
    face_path = root / "index.md"
    if not face_path.is_file():
        return [
            Report(
                face_path, [Problem("error", "face_missing", "pack requires index.md")]
            )
        ]

    files = [path for path in sorted(root.rglob("*.md")) if path.name != "log.md"]
    frontmatters = {
        path: parse_frontmatter(path.read_text(encoding="utf-8", errors="replace"))
        for path in files
    }
    reports = [
        Report(path, validate_document(fm, face=path == face_path))
        for path, fm in frontmatters.items()
    ]
    report_by_path = {report.path: report for report in reports}

    by_id: dict[str, Path] = {}
    for path, fm in frontmatters.items():
        opf_id = str(fm.get("opf_id") or "")
        if not opf_id:
            continue
        if opf_id in by_id:
            report_by_path[path].problems.append(
                Problem("error", "duplicate_id", f"also declared by {by_id[opf_id]}")
            )
        else:
            by_id[opf_id] = path

    graph: dict[str, set[str]] = {opf_id: set() for opf_id in by_id}
    for path, fm in frontmatters.items():
        source = str(fm.get("opf_id") or "")
        for target in references(fm):
            if target not in by_id:
                report_by_path[path].problems.append(
                    Problem("error", "unresolved_ref", target)
                )
                continue
            if source in graph:
                graph[source].add(target)
                graph[target].add(source)

    face_id = str(frontmatters.get(face_path, {}).get("opf_id") or "")
    seen: set[str] = set()
    pending = [face_id] if face_id in graph else []
    while pending:
        current = pending.pop()
        if current in seen:
            continue
        seen.add(current)
        pending.extend(graph[current] - seen)
    for opf_id, path in by_id.items():
        if opf_id not in seen:
            report_by_path[path].problems.append(
                Problem("error", "orphan", "concept is disconnected from product face")
            )

    if not (root / "log.md").is_file():
        reports.append(
            Report(
                root / "log.md",
                [
                    Problem(
                        "warn", "log_missing", "packs should keep an append-only log.md"
                    )
                ],
            )
        )
    if strict:
        for report in reports:
            for problem in report.problems:
                if problem.level == "warn":
                    problem.level = "error"
    return reports


def validate_path(path: Path, *, strict: bool = False) -> list[Report]:
    if path.is_dir():
        return validate_pack(path, strict=strict)
    if path.is_file():
        fm = parse_frontmatter(path.read_text(encoding="utf-8", errors="replace"))
        return [Report(path, validate_document(fm, face=path.name == "index.md"))]
    return [Report(path, [Problem("error", "path", "not found")])]


def selftest() -> int:
    base = {
        "okf_version": OKF_VERSION,
        "opf_version": OPF_VERSION,
        "type": "product",
        "opf_id": "opf:test:product",
        "title": "Test",
        "status": "shaping",
        "intent": ["emf:test:intent"],
        "users": ["opf:test:user"],
        "problem": "A problem",
        "promise": "A promise",
        "outcomes": ["opf:test:outcome"],
        "first_slice": "opf:test:slice",
        "non_goals": ["Not everything"],
        "proof": ["opf:test:acceptance"],
        "authority": ["opf:test:authority"],
        "verified": {"by": "human:test", "method": "test"},
    }
    errors = lambda fm, face=False: {
        p.rule for p in validate_document(fm, face=face) if p.level == "error"
    }
    assert not errors(base, face=True)
    assert "product_admission" in errors({**base, "proof": []}, face=True)
    assert "version_alignment" in errors({**base, "opf_version": "0.1.9"}, face=True)
    surface = {
        **base,
        "type": "product-concept",
        "kind": "surface",
        "opf_id": "opf:test:surface",
        "serves": ["opf:test:outcome"],
        "states": [],
    }
    assert "surface_traceability" in errors(surface)
    with TemporaryDirectory() as directory:
        root = Path(directory)
        (root / "index.md").write_text(
            "---\n" + "\n".join(f"{k}: {v}" for k, v in {}) + "\n---\n",
            encoding="utf-8",
        )
        assert any(
            p.rule == "frontmatter" for r in validate_pack(root) for p in r.problems
        )
    print(
        "selftest OK — admission, version alignment, UX traceability, and invalid-pack checks"
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="opf.validate", description=__doc__)
    parser.add_argument("paths", nargs="*", type=Path)
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument(
        "--strict", action="store_true", help="treat warnings as errors"
    )
    args = parser.parse_args(argv)
    if args.selftest:
        return selftest()
    if not args.paths:
        parser.error("give a file or pack directory")
    bad = 0
    count = 0
    for path in args.paths:
        for report in validate_path(path, strict=args.strict):
            count += 1
            bad += bool(report.errors)
            mark = "FAIL" if report.errors else ("warn" if report.problems else "ok  ")
            print(f"{mark}  {report.path}")
            for problem in report.problems:
                print(f"        {problem.level:<5} {problem.rule}: {problem.detail}")
    print(f"\n{count} path(s), {bad} with errors")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
