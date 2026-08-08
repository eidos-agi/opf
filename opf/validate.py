"""Validate Open Product Format v0.2.5 documents and packs.

Stdlib only. The parser accepts the deliberately small YAML subset OPF specifies
and fails closed on syntax it cannot represent faithfully.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
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
SURFACE_KINDS = {
    "screen",
    "api",
    "physical-control",
    "device-output",
    "voice",
    "notification",
    "document",
    "service",
}
ACCEPTANCE_STATUSES = {"proposed", "observed", "failed"}
PLACEHOLDERS = {"tbd", "todo", "later", "unknown", "none", "n/a", "placeholder"}
ID_RE = re.compile(r"^opf:[a-z0-9][a-z0-9._-]*(?::[a-z0-9][a-z0-9._-]*){1,5}$")
EXTERNAL_RE = re.compile(
    r"^(?P<profile>emf|orf|okf):(?P<pack>[a-z0-9][a-z0-9._-]*):"
    r"(?P<object>[a-z0-9][a-z0-9:._/-]*)@(?P<revision>[A-Za-z0-9._-]+)$"
)
IMPORT_RE = re.compile(
    r"^(?P<profile>emf|orf|okf):(?P<pack>[a-z0-9][a-z0-9._-]*)@"
    r"(?P<revision>[A-Za-z0-9._-]+)$"
)
LOCAL_EVIDENCE_RE = re.compile(
    r"^file:(?P<path>evidence/[A-Za-z0-9._/-]+\.json)@sha256-(?P<digest>[a-f0-9]{64})$"
)
LOCAL_REFERENCE_RE = re.compile(
    r"^file:(?P<path>references/[A-Za-z0-9._/-]+)@sha256-(?P<digest>[a-f0-9]{64})$"
)
REVIEW_REVISION_RE = re.compile(r"^sha256:[a-f0-9]{64}$")
REALIZATION_FIDELITIES = {
    "intent-equivalent",
    "behaviorally-equivalent",
    "experience-equivalent",
    "reference-faithful",
}
FIDELITY_DIMENSIONS = {
    "visual-composition",
    "content",
    "interaction",
    "interaction-timing",
    "explanation-semantics",
    "deterministic-output",
    "accessibility",
    "performance",
    "physical-form",
}
EXPERIENCE_QUALITIES = {
    "operability",
    "usability",
    "clarity",
    "readability",
    "visual-cleanliness",
    "consistency",
    "experiential-character",
}
QUALITY_ASSURANCE = {"mechanical", "human", "hybrid"}
MIN_SUPPORTED_OPF_VERSION = (0, 2, 1)

# Field names are edge types. Target kinds are checked mechanically.
EDGE_TARGET_KINDS: dict[str, set[str]] = {
    "users": {"user"},
    "problem": {"problem"},
    "promise": {"promise"},
    "outcomes": {"outcome"},
    "first_slice": {"slice"},
    "proof": {"acceptance"},
    "validation": {"acceptance"},
    "operational_proof": {"acceptance"},
    "authority": {"authority-boundary"},
    "realization": {"contract"},
    "experience_quality": {"contract"},
    "reviewed_surfaces": {"surface"},
    "actor": {"user"},
    "outcome": {"outcome"},
    "journeys": {"journey"},
    "moments": {"moment"},
    "in_journey": {"journey"},
    "on_surface": {"surface"},
    "surfaces": {"surface"},
    "states": {"state"},
    "of_surface": {"surface"},
    "allows": {"interaction"},
    "interactions": {"interaction"},
    "on": {"surface", "state"},
    "yields": {"state", "outcome"},
    "covered_by": {"acceptance"},
    "appears_on": {"surface", "state"},
    "applies_to": {"surface", "state", "interaction"},
    "serves": {"outcome", "moment", "surface", "slice"},
    "includes": {
        "journey",
        "moment",
        "surface",
        "state",
        "interaction",
        "content",
        "accessibility",
        "capability",
        "contract",
    },
    "depends_on": KINDS,
    "supersedes": KINDS,
    "superseded_by": KINDS,
}
REF_FIELDS = set(EDGE_TARGET_KINDS)
EXTERNAL_FIELDS = {"intent": {"emf"}, "research": {"orf"}, "evidence": {"okf", "orf"}}

# Only composition edges make a document a member of the product definition.
# Grounding/back-reference fields such as serves, actor, and of_surface do not.
COMPOSITION_FIELDS = {
    "users",
    "problem",
    "promise",
    "outcomes",
    "first_slice",
    "proof",
    "validation",
    "operational_proof",
    "authority",
    "realization",
    "experience_quality",
    "journeys",
    "moments",
    "on_surface",
    "surfaces",
    "states",
    "allows",
    "interactions",
    "includes",
    "covered_by",
    "appears_on",
    "applies_to",
    "depends_on",
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
    """Parse the small YAML-compatible frontmatter subset used by OPF documents."""
    if not text.startswith("---"):
        return {"__parse_errors__": ["missing opening frontmatter delimiter"]}
    end = text.find("\n---", 3)
    if end == -1:
        return {"__parse_errors__": ["missing closing frontmatter delimiter"]}
    return _parse_yaml_block(text[3:end])


def _parse_yaml_block(block: str) -> dict[str, Any]:
    out: dict[str, Any] = {}
    errors: list[str] = []
    stack: list[tuple[int, dict[str, Any]]] = [(-1, out)]
    lines = block.splitlines()
    i = 0
    while i < len(lines):
        raw = lines[i]
        if not raw.strip() or raw.lstrip().startswith("#"):
            i += 1
            continue
        if "\t" in raw:
            errors.append(f"line {i + 1}: tabs are unsupported")
            i += 1
            continue
        indent = len(raw) - len(raw.lstrip())
        line = raw.strip()
        while len(stack) > 1 and indent <= stack[-1][0]:
            stack.pop()
        container = stack[-1][1]
        if line.startswith("- "):
            errors.append(f"line {i + 1}: unexpected list item")
            i += 1
            continue
        if ":" not in line:
            errors.append(f"line {i + 1}: expected key: value")
            i += 1
            continue
        key, _, value = line.partition(":")
        key, value = key.strip(), value.strip()
        if key in container:
            errors.append(f"line {i + 1}: duplicate key {key!r}")
            i += 1
            continue
        if value in {"|", ">"} or value.startswith(("{", "&")):
            errors.append(f"line {i + 1}: unsupported YAML construct")
            i += 1
            continue
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
                    item = lines[j].strip()
                    if next_indent <= indent or not item.startswith("- "):
                        break
                    item = item[2:].strip()
                    if re.match(r"^[A-Za-z_][A-Za-z0-9_-]*:\s", item):
                        errors.append(f"line {j + 1}: lists of maps are unsupported")
                    else:
                        items.append(item.strip("'\""))
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
            try:
                row = next(csv.reader([inner], skipinitialspace=True)) if inner else []
                container[key] = [
                    part.strip().strip("'\"") for part in row if part.strip()
                ]
            except csv.Error as error:
                errors.append(f"line {i + 1}: invalid inline list: {error}")
        elif value.lower() in {"null", "none", "~"}:
            container[key] = None
        else:
            container[key] = value.strip("'\"")
        i += 1
    if errors:
        out["__parse_errors__"] = errors
    return out


def _items(value: Any) -> list[str]:
    if isinstance(value, list):
        return [item for item in value if isinstance(item, str) and item.strip()]
    if isinstance(value, str) and value.strip():
        return [value]
    return []


def _is_placeholder(value: str) -> bool:
    return value.strip().lower() in PLACEHOLDERS


def _missing(fm: dict[str, Any], fields: set[str]) -> list[str]:
    return sorted(
        ref_field
        for ref_field in fields
        if not _items(fm.get(ref_field))
        or all(_is_placeholder(item) for item in _items(fm.get(ref_field)))
    )


def _version_tuple(value: str) -> tuple[int, int, int] | None:
    if not re.fullmatch(r"\d+\.\d+\.\d+", value):
        return None
    return tuple(int(part) for part in value.split("."))


def validate_document(fm: dict[str, Any], *, face: bool = False) -> list[Problem]:
    """Validate one parsed OPF document and return all discovered problems."""
    problems = [
        Problem("error", "frontmatter_parse", detail)
        for detail in fm.get("__parse_errors__", [])
    ]
    if len(fm) == 1 and "__parse_errors__" in fm:
        return problems

    okf_version = str(fm.get("okf_version") or "")
    if okf_version != OKF_VERSION:
        problems.append(
            Problem("error", "okf_base", f"okf_version must be {OKF_VERSION!r}")
        )
    opf_version = str(fm.get("opf_version") or "")
    declared_version = _version_tuple(opf_version)
    if declared_version is None:
        problems.append(Problem("error", "opf_version", "opf_version must use X.Y.Z"))
    elif ".".join(opf_version.split(".")[:2]) != okf_version:
        problems.append(
            Problem("error", "version_alignment", "OPF major.minor must match OKF")
        )
    elif declared_version < MIN_SUPPORTED_OPF_VERSION:
        problems.append(
            Problem(
                "warn",
                "opf_version",
                f"document uses unsupported legacy {opf_version}; migrate to 0.2.1 or newer",
            )
        )
    elif declared_version > _version_tuple(OPF_VERSION):
        problems.append(
            Problem(
                "warn",
                "opf_version",
                f"document requires {opf_version}; validator implements {OPF_VERSION}",
            )
        )

    if fm.get("type") not in TYPES:
        problems.append(
            Problem("error", "type", f"type must be one of {sorted(TYPES)}")
        )
    if not str(fm.get("title") or "").strip():
        problems.append(Problem("error", "title", "title is required"))
    opf_id = str(fm.get("opf_id") or "")
    if not ID_RE.fullmatch(opf_id):
        problems.append(
            Problem(
                "error", "opf_id", "opf_id does not match the stable OPF ID grammar"
            )
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
        _validate_face(fm, problems)
    elif fm.get("type") == "product-concept":
        _validate_concept(fm, problems)
    return problems


def _validate_face(fm: dict[str, Any], problems: list[Problem]) -> None:
    if fm.get("type") != "product":
        problems.append(
            Problem("error", "face_type", "index.md must use type: product")
        )
    status = str(fm.get("status") or "")
    if status not in STATUSES:
        problems.append(
            Problem("error", "status", f"status must be one of {sorted(STATUSES)}")
        )
    active = {"shaping", "validated", "building", "operating"}
    if status in active:
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
        face_version = _version_tuple(str(fm.get("opf_version") or "")) or (0, 0, 0)
        if face_version >= (0, 2, 3):
            required.add("realization")
        if face_version >= (
            0,
            2,
            4,
        ):
            required.add("experience_quality")
        for missing in _missing(fm, required):
            problems.append(
                Problem(
                    "error",
                    "product_admission",
                    f"status {status!r} requires {missing}",
                )
            )
    if status == "validated" and _missing(fm, {"validation"}):
        problems.append(
            Problem("error", "validated_gate", "validated requires observed validation")
        )
    if status == "operating" and _missing(fm, {"operational_proof"}):
        problems.append(
            Problem(
                "error",
                "operating_gate",
                "operating requires observed operational_proof",
            )
        )
    if status == "retired" and _missing(fm, {"retirement_reason"}):
        problems.append(
            Problem("error", "retired_gate", "retired requires retirement_reason")
        )


def _validate_concept(fm: dict[str, Any], problems: list[Problem]) -> None:
    kind = str(fm.get("kind") or "")
    if kind not in KINDS:
        problems.append(
            Problem("error", "kind", f"kind must be one of {sorted(KINDS)}")
        )
        return
    requirements: dict[str, set[str]] = {
        "journey": {"actor", "outcome", "moments"},
        "moment": {"in_journey", "on_surface"},
        "surface": {"serves", "states", "proof", "surface_kind"},
        "state": {"of_surface"},
        "interaction": {"on", "yields"},
        "content": {"appears_on"},
        "accessibility": {"applies_to", "requirement"},
        "slice": {"serves", "includes", "proof", "non_goals"},
        "acceptance": {"condition", "status"},
    }
    for missing in _missing(fm, requirements.get(kind, set())):
        problems.append(
            Problem("error", f"{kind}_traceability", f"{kind} requires {missing}")
        )
    if kind == "surface" and str(fm.get("surface_kind") or "") not in SURFACE_KINDS:
        problems.append(
            Problem(
                "error",
                "surface_kind",
                f"surface_kind must be one of {sorted(SURFACE_KINDS)}",
            )
        )
    if (
        kind == "state"
        and not _items(fm.get("allows"))
        and str(fm.get("terminal") or "").lower() != "true"
    ):
        problems.append(
            Problem(
                "error", "state_transition", "state requires allows or terminal: true"
            )
        )
    if kind == "interaction" and not (
        _items(fm.get("proof")) or _items(fm.get("covered_by"))
    ):
        problems.append(
            Problem(
                "error", "interaction_proof", "interaction requires proof or covered_by"
            )
        )
    if kind == "acceptance":
        status = str(fm.get("status") or "")
        if status not in ACCEPTANCE_STATUSES:
            problems.append(
                Problem(
                    "error",
                    "acceptance_status",
                    f"status must be one of {sorted(ACCEPTANCE_STATUSES)}",
                )
            )
        if status in {"observed", "failed"} and _missing(fm, {"evidence"}):
            problems.append(
                Problem(
                    "error",
                    "acceptance_evidence",
                    f"status {status!r} requires evidence",
                )
            )
    if kind == "contract" and str(fm.get("contract_type") or "") == "realization":
        for missing in _missing(fm, {"applies_to", "dimensions", "fidelity", "proof"}):
            problems.append(
                Problem(
                    "error",
                    "realization_contract",
                    f"realization contract requires {missing}",
                )
            )
        fidelity = str(fm.get("fidelity") or "")
        if fidelity not in REALIZATION_FIDELITIES:
            problems.append(
                Problem(
                    "error",
                    "realization_fidelity",
                    f"fidelity must be one of {sorted(REALIZATION_FIDELITIES)}",
                )
            )
        dimensions = _items(fm.get("dimensions"))
        invalid_dimensions = sorted(set(dimensions) - FIDELITY_DIMENSIONS)
        if invalid_dimensions:
            problems.append(
                Problem(
                    "error",
                    "realization_dimensions",
                    f"unsupported dimensions {invalid_dimensions}",
                )
            )
        if fidelity == "reference-faithful":
            for missing in _missing(fm, {"references", "tolerances"}):
                problems.append(
                    Problem(
                        "error",
                        "reference_fidelity",
                        f"reference-faithful contract requires {missing}",
                    )
                )
    if (
        kind == "contract"
        and str(fm.get("contract_type") or "") == "experience-quality"
    ):
        required = {"scope", "qualities", "requirements", "assurance", "proof"}
        for missing in _missing(fm, required):
            problems.append(
                Problem(
                    "error",
                    "experience_quality_contract",
                    f"experience-quality contract requires {missing}",
                )
            )
        if str(fm.get("scope") or "") != "product":
            problems.append(
                Problem("error", "experience_quality_scope", "scope must be product")
            )
        qualities = _items(fm.get("qualities"))
        if set(qualities) != EXPERIENCE_QUALITIES or len(qualities) != len(
            EXPERIENCE_QUALITIES
        ):
            missing = sorted(EXPERIENCE_QUALITIES - set(qualities))
            unsupported = sorted(set(qualities) - EXPERIENCE_QUALITIES)
            problems.append(
                Problem(
                    "error",
                    "experience_quality_dimensions",
                    f"missing {missing}; unsupported {unsupported}",
                )
            )
        requirements: dict[str, str] = {}
        malformed: list[str] = []
        for item in _items(fm.get("requirements")):
            dimension, separator, criterion = item.partition("=")
            dimension = dimension.strip()
            if (
                not separator
                or not dimension
                or not criterion.strip()
                or dimension in requirements
            ):
                malformed.append(item)
                continue
            requirements[dimension] = criterion.strip()
        if set(requirements) != EXPERIENCE_QUALITIES or malformed:
            problems.append(
                Problem(
                    "error",
                    "experience_quality_requirements",
                    f"requirements must define each quality once; malformed {malformed}",
                )
            )
        assurance = str(fm.get("assurance") or "")
        if assurance not in QUALITY_ASSURANCE:
            problems.append(
                Problem(
                    "error",
                    "experience_quality_assurance",
                    f"assurance must be one of {sorted(QUALITY_ASSURANCE)}",
                )
            )
        elif assurance == "mechanical":
            problems.append(
                Problem(
                    "error",
                    "experience_quality_human_review",
                    "experiential-character requires human or hybrid assurance",
                )
            )


def internal_references(fm: dict[str, Any]) -> list[tuple[str, str]]:
    """Return internal OPF references paired with their source field."""
    return [
        (ref_field, item)
        for ref_field in REF_FIELDS
        for item in _items(fm.get(ref_field))
        if item.startswith("opf:")
    ]


def external_references(fm: dict[str, Any]) -> list[tuple[str, str, set[str]]]:
    """Return external references with their source field and allowed profiles."""
    return [
        (ref_field, item, profiles)
        for ref_field, profiles in EXTERNAL_FIELDS.items()
        for item in _items(fm.get(ref_field))
        if not item.startswith("file:")
    ]


def validate_pack(root: Path, *, strict: bool = False) -> list[Report]:
    """Validate one OPF pack rooted at a directory containing index.md."""
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
    kind_by_id: dict[str, str] = {}
    fm_by_id: dict[str, dict[str, Any]] = {}
    for path, fm in frontmatters.items():
        opf_id = str(fm.get("opf_id") or "")
        if not opf_id:
            continue
        if opf_id in by_id:
            report_by_path[path].problems.append(
                Problem("error", "duplicate_id", f"also declared by {by_id[opf_id]}")
            )
            continue
        by_id[opf_id] = path
        kind_by_id[opf_id] = (
            "product" if path == face_path else str(fm.get("kind") or "")
        )
        fm_by_id[opf_id] = fm

    directed: dict[str, set[str]] = {opf_id: set() for opf_id in by_id}
    for path, fm in frontmatters.items():
        source = str(fm.get("opf_id") or "")
        for ref_field, target in internal_references(fm):
            if target not in by_id:
                report_by_path[path].problems.append(
                    Problem("error", "unresolved_ref", f"{ref_field} -> {target}")
                )
                continue
            allowed = EDGE_TARGET_KINDS[ref_field]
            if kind_by_id[target] not in allowed:
                report_by_path[path].problems.append(
                    Problem(
                        "error",
                        "wrong_target_kind",
                        f"{ref_field} -> {target} ({kind_by_id[target]!r}); expected {sorted(allowed)}",
                    )
                )
            if ref_field in COMPOSITION_FIELDS and source in directed:
                directed[source].add(target)

    face_fm = frontmatters.get(face_path, {})
    _validate_local_evidence(root, frontmatters, report_by_path)
    _validate_local_references(root, frontmatters, report_by_path)
    _validate_external_refs(
        frontmatters, report_by_path, face_fm, face_path, strict=strict
    )
    _validate_supersession(fm_by_id, kind_by_id, by_id, report_by_path)
    _validate_lifecycle(face_fm, fm_by_id, kind_by_id, face_path, report_by_path)

    face_id = str(face_fm.get("opf_id") or "")
    seen: set[str] = set()
    pending = [face_id] if face_id in directed else []
    while pending:
        current = pending.pop()
        if current in seen:
            continue
        seen.add(current)
        pending.extend(directed[current] - seen)
    for opf_id, path in by_id.items():
        if opf_id not in seen:
            report_by_path[path].problems.append(
                Problem(
                    "error",
                    "orphan",
                    "concept is not reachable from the product face through composition edges",
                )
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


def _validate_local_evidence(
    root: Path,
    frontmatters: dict[Path, dict[str, Any]],
    report_by_path: dict[Path, Report],
) -> None:
    for document_path, fm in frontmatters.items():
        for ref in _items(fm.get("evidence")):
            if not ref.startswith("file:"):
                continue
            match = LOCAL_EVIDENCE_RE.fullmatch(ref)
            if not match:
                report_by_path[document_path].problems.append(
                    Problem(
                        "error",
                        "evidence_file_ref",
                        f"invalid local evidence reference {ref}",
                    )
                )
                continue
            evidence_path = (root / match.group("path")).resolve()
            try:
                evidence_path.relative_to((root / "evidence").resolve())
            except ValueError:
                report_by_path[document_path].problems.append(
                    Problem(
                        "error", "evidence_file_ref", f"evidence escapes pack: {ref}"
                    )
                )
                continue
            if not evidence_path.is_file():
                report_by_path[document_path].problems.append(
                    Problem("error", "evidence_file_missing", match.group("path"))
                )
                continue
            payload = evidence_path.read_bytes()
            if hashlib.sha256(payload).hexdigest() != match.group("digest"):
                report_by_path[document_path].problems.append(
                    Problem(
                        "error",
                        "evidence_digest",
                        f"digest mismatch for {match.group('path')}",
                    )
                )
                continue
            try:
                receipt = json.loads(payload)
            except (UnicodeDecodeError, json.JSONDecodeError):
                receipt = None
            required = {"subject", "observed_at", "method", "source_revision", "result"}
            checks = receipt.get("checks") if isinstance(receipt, dict) else None
            if (
                not isinstance(receipt, dict)
                or any(
                    not isinstance(receipt.get(key), str) or not receipt[key].strip()
                    for key in required
                )
                or not isinstance(checks, list)
                or not checks
                or any(
                    not isinstance(check, str) or not check.strip() for check in checks
                )
            ):
                report_by_path[document_path].problems.append(
                    Problem(
                        "error",
                        "evidence_receipt",
                        f"incomplete receipt {match.group('path')}",
                    )
                )
                continue
            if receipt["subject"] != fm.get("opf_id"):
                report_by_path[document_path].problems.append(
                    Problem(
                        "error",
                        "evidence_subject",
                        f"receipt subject must be {fm.get('opf_id')}",
                    )
                )
            reviewed_revision = str(fm.get("reviewed_revision") or "")
            if reviewed_revision and receipt["source_revision"] != reviewed_revision:
                report_by_path[document_path].problems.append(
                    Problem(
                        "error",
                        "experience_quality_revision_mismatch",
                        "reviewed_revision must match the pinned receipt source_revision",
                    )
                )
            expected = {"observed": "passed", "failed": "failed"}.get(
                str(fm.get("status") or "")
            )
            if expected and receipt["result"] != expected:
                report_by_path[document_path].problems.append(
                    Problem(
                        "error",
                        "evidence_result",
                        f"status requires receipt result {expected!r}",
                    )
                )


def _validate_local_references(
    root: Path,
    frontmatters: dict[Path, dict[str, Any]],
    report_by_path: dict[Path, Report],
) -> None:
    reference_root = (root / "references").resolve()
    for document_path, fm in frontmatters.items():
        for ref in _items(fm.get("references")):
            match = LOCAL_REFERENCE_RE.fullmatch(ref)
            if not match:
                report_by_path[document_path].problems.append(
                    Problem("error", "reference_file_ref", f"invalid reference {ref}")
                )
                continue
            reference_path = (root / match.group("path")).resolve()
            try:
                reference_path.relative_to(reference_root)
            except ValueError:
                report_by_path[document_path].problems.append(
                    Problem(
                        "error", "reference_file_ref", f"reference escapes pack: {ref}"
                    )
                )
                continue
            if not reference_path.is_file():
                report_by_path[document_path].problems.append(
                    Problem("error", "reference_file_missing", match.group("path"))
                )
                continue
            if hashlib.sha256(reference_path.read_bytes()).hexdigest() != match.group(
                "digest"
            ):
                report_by_path[document_path].problems.append(
                    Problem(
                        "error",
                        "reference_digest",
                        f"digest mismatch for {match.group('path')}",
                    )
                )


def _validate_external_refs(
    frontmatters: dict[Path, dict[str, Any]],
    report_by_path: dict[Path, Report],
    face_fm: dict[str, Any],
    face_path: Path,
    *,
    strict: bool,
) -> None:
    imports = set(_items(face_fm.get("imports")))
    valid_imports = {item for item in imports if IMPORT_RE.fullmatch(item)}
    for item in imports - valid_imports:
        report_by_path[face_path].problems.append(
            Problem("error" if strict else "warn", "invalid_import", item)
        )
    for path, fm in frontmatters.items():
        for ref_field, ref, expected_profiles in external_references(fm):
            match = EXTERNAL_RE.fullmatch(ref)
            level = "error" if strict else "warn"
            if not match:
                report_by_path[path].problems.append(
                    Problem(level, "external_ref_unpinned", f"{ref_field} -> {ref}")
                )
                continue
            if match.group("profile") not in expected_profiles:
                report_by_path[path].problems.append(
                    Problem(
                        "error",
                        "external_ref_profile",
                        f"{ref_field} cannot reference {match.group('profile')}",
                    )
                )
                continue
            import_id = f"{match.group('profile')}:{match.group('pack')}@{match.group('revision')}"
            if import_id not in valid_imports:
                report_by_path[path].problems.append(
                    Problem(
                        level,
                        "external_ref_unimported",
                        f"{ref} needs import {import_id}",
                    )
                )


def _validate_supersession(
    fm_by_id: dict[str, dict[str, Any]],
    kind_by_id: dict[str, str],
    by_id: dict[str, Path],
    report_by_path: dict[Path, Report],
) -> None:
    incoming: dict[str, list[str]] = {}
    for source, fm in fm_by_id.items():
        for target in _items(fm.get("supersedes")):
            if target not in fm_by_id:
                continue
            incoming.setdefault(target, []).append(source)
            if kind_by_id[source] != kind_by_id[target]:
                report_by_path[by_id[source]].problems.append(
                    Problem(
                        "error", "supersession_kind", f"{source} and {target} differ"
                    )
                )
            if source not in _items(fm_by_id[target].get("superseded_by")):
                report_by_path[by_id[source]].problems.append(
                    Problem(
                        "error",
                        "supersession_inverse",
                        f"{target} must declare superseded_by: {source}",
                    )
                )
        for target in _items(fm.get("superseded_by")):
            if target in fm_by_id and source not in _items(
                fm_by_id[target].get("supersedes")
            ):
                report_by_path[by_id[source]].problems.append(
                    Problem(
                        "error",
                        "supersession_inverse",
                        f"{target} must declare supersedes: {source}",
                    )
                )
    for target, sources in incoming.items():
        if len(sources) > 1:
            report_by_path[by_id[target]].problems.append(
                Problem("error", "supersession_multi_head", f"superseded by {sources}")
            )


def _validate_lifecycle(
    face_fm: dict[str, Any],
    fm_by_id: dict[str, dict[str, Any]],
    kind_by_id: dict[str, str],
    face_path: Path,
    report_by_path: dict[Path, Report],
) -> None:
    status = str(face_fm.get("status") or "")
    face_version = _version_tuple(str(face_fm.get("opf_version") or "")) or (0, 0, 0)
    if status in {"shaping", "building", "validated", "operating"}:
        for contract_id in _items(face_fm.get("realization")):
            contract = fm_by_id.get(contract_id, {})
            if contract and str(contract.get("contract_type") or "") != "realization":
                report_by_path[face_path].problems.append(
                    Problem(
                        "error",
                        "realization_contract_type",
                        f"{contract_id} must declare contract_type: realization",
                    )
                )
        for contract_id in _items(face_fm.get("experience_quality")):
            contract = fm_by_id.get(contract_id, {})
            if (
                contract
                and str(contract.get("contract_type") or "") != "experience-quality"
            ):
                report_by_path[face_path].problems.append(
                    Problem(
                        "error",
                        "experience_quality_contract_type",
                        f"{contract_id} must declare contract_type: experience-quality",
                    )
                )
            if status in {"validated", "operating"} and contract:
                proofs = _items(contract.get("proof"))
                observed_proofs = [
                    fm_by_id[proof]
                    for proof in proofs
                    if proof in fm_by_id
                    and str(fm_by_id[proof].get("status") or "") == "observed"
                ]
                if not observed_proofs:
                    report_by_path[face_path].problems.append(
                        Problem(
                            "error",
                            "experience_quality_not_observed",
                            f"{contract_id} needs observed acceptance proof",
                        )
                    )
                elif face_version >= (0, 2, 5) and not any(
                    set(_items(proof.get("quality_coverage"))) == EXPERIENCE_QUALITIES
                    and len(_items(proof.get("quality_coverage")))
                    == len(EXPERIENCE_QUALITIES)
                    and any(
                        reviewer.startswith("human:") and len(reviewer) > 6
                        for reviewer in _items(proof.get("reviewed_by"))
                    )
                    and any(
                        kind_by_id.get(surface) == "surface"
                        for surface in _items(proof.get("reviewed_surfaces"))
                    )
                    and REVIEW_REVISION_RE.fullmatch(
                        str(proof.get("reviewed_revision") or "")
                    )
                    for proof in observed_proofs
                ):
                    report_by_path[face_path].problems.append(
                        Problem(
                            "error",
                            "experience_quality_review_missing",
                            f"{contract_id} needs observed proof covering all qualities with a human reviewer, surface, and pinned revision",
                        )
                    )
        _validate_first_slice(face_fm, fm_by_id, kind_by_id, face_path, report_by_path)
    if status == "validated":
        _require_observed(face_fm, "validation", fm_by_id, face_path, report_by_path)
    if status == "operating":
        _require_observed(
            face_fm, "operational_proof", fm_by_id, face_path, report_by_path
        )


def _require_observed(
    face_fm: dict[str, Any],
    ref_field: str,
    fm_by_id: dict[str, dict[str, Any]],
    face_path: Path,
    report_by_path: dict[Path, Report],
) -> None:
    for target in _items(face_fm.get(ref_field)):
        if (
            target in fm_by_id
            and str(fm_by_id[target].get("status") or "") == "observed"
        ):
            return
    report_by_path[face_path].problems.append(
        Problem(
            "error",
            f"{ref_field}_not_observed",
            f"{ref_field} requires at least one observed acceptance",
        )
    )


def _validate_first_slice(
    face_fm: dict[str, Any],
    fm_by_id: dict[str, dict[str, Any]],
    kind_by_id: dict[str, str],
    face_path: Path,
    report_by_path: dict[Path, Report],
) -> None:
    requires_realization = (
        _version_tuple(str(face_fm.get("opf_version") or "")) or (0, 0, 0)
    ) >= (0, 2, 3)
    realized_surfaces = {
        surface_id
        for contract_id in _items(face_fm.get("realization"))
        if str(fm_by_id.get(contract_id, {}).get("contract_type") or "")
        == "realization"
        for surface_id in _items(fm_by_id.get(contract_id, {}).get("applies_to"))
    }
    slice_ids = _items(face_fm.get("first_slice"))
    if len(slice_ids) != 1:
        report_by_path[face_path].problems.append(
            Problem(
                "error", "first_slice_count", "first_slice must name exactly one slice"
            )
        )
        return
    slice_id = slice_ids[0]
    if kind_by_id.get(slice_id) != "slice":
        return
    slice_fm = fm_by_id[slice_id]
    journeys = [
        target
        for target in _items(slice_fm.get("includes"))
        if kind_by_id.get(target) == "journey"
    ]
    if not journeys:
        report_by_path[face_path].problems.append(
            Problem("error", "experience_chain", "first slice must include a journey")
        )
        return
    for journey_id in journeys:
        journey = fm_by_id[journey_id]
        outcome = _items(journey.get("outcome"))
        moments = _items(journey.get("moments"))
        if not outcome or not moments:
            report_by_path[face_path].problems.append(
                Problem(
                    "error",
                    "experience_chain",
                    f"{journey_id} lacks outcome or moments",
                )
            )
            continue
        complete = False
        for moment_id in moments:
            moment = fm_by_id.get(moment_id, {})
            if journey_id not in _items(moment.get("in_journey")):
                continue
            for surface_id in _items(moment.get("on_surface")):
                surface = fm_by_id.get(surface_id, {})
                if (
                    requires_realization
                    and str(surface.get("surface_kind") or "") == "screen"
                    and surface_id not in realized_surfaces
                ):
                    report_by_path[face_path].problems.append(
                        Problem(
                            "error",
                            "realization_coverage",
                            f"screen surface {surface_id} needs a face-level realization contract",
                        )
                    )
                surface_proof = _items(surface.get("proof"))
                for state_id in _items(surface.get("states")):
                    state = fm_by_id.get(state_id, {})
                    if surface_id not in _items(state.get("of_surface")):
                        continue
                    for interaction_id in _items(state.get("allows")):
                        interaction = fm_by_id.get(interaction_id, {})
                        if not (
                            {state_id, surface_id} & set(_items(interaction.get("on")))
                        ):
                            continue
                        yields = set(_items(interaction.get("yields")))
                        if not (yields & (set(outcome) | {state_id})):
                            report_by_path[face_path].problems.append(
                                Problem(
                                    "error",
                                    "experience_outcome",
                                    f"{interaction_id} does not yield the journey outcome or a declared state",
                                )
                            )
                            continue
                        proof = (
                            surface_proof
                            + _items(interaction.get("proof"))
                            + _items(interaction.get("covered_by"))
                        )
                        if any(kind_by_id.get(item) == "acceptance" for item in proof):
                            complete = True
        if not complete:
            report_by_path[face_path].problems.append(
                Problem(
                    "error",
                    "experience_chain",
                    f"{journey_id} lacks journey -> moment -> surface -> state -> interaction -> proof",
                )
            )


def validate_path(path: Path, *, strict: bool = False) -> list[Report]:
    """Validate an OPF document or complete pack path."""
    if path.is_dir():
        return validate_pack(path, strict=strict)
    if path.is_file():
        fm = parse_frontmatter(path.read_text(encoding="utf-8", errors="replace"))
        return [Report(path, validate_document(fm, face=path.name == "index.md"))]
    return [Report(path, [Problem("error", "path", "not found")])]


def selftest() -> int:
    """Run dependency-free smoke checks for the validator's critical gates."""
    base = {
        "okf_version": OKF_VERSION,
        "opf_version": OPF_VERSION,
        "type": "product",
        "opf_id": "opf:test:product",
        "title": "Test",
        "status": "shaping",
        "intent": ["emf:test:intent@r1"],
        "users": ["opf:test:user"],
        "problem": "opf:test:problem",
        "promise": "opf:test:promise",
        "outcomes": ["opf:test:outcome"],
        "first_slice": "opf:test:slice",
        "non_goals": ["Not everything"],
        "proof": ["opf:test:acceptance"],
        "authority": ["opf:test:authority"],
        "realization": ["opf:test:contract"],
        "experience_quality": ["opf:test:quality-contract"],
        "verified": {"by": "human:test", "method": "test"},
    }

    def errors(fm: dict[str, Any], face: bool = False) -> set[str]:
        return {
            problem.rule
            for problem in validate_document(fm, face=face)
            if problem.level == "error"
        }

    assert not errors(base, face=True)
    assert "product_admission" in errors({**base, "proof": ["TBD"]}, face=True)
    assert "version_alignment" in errors({**base, "opf_version": "0.1.9"}, face=True)
    assert "frontmatter_parse" in errors(
        parse_frontmatter("---\ntitle: A\ntitle: B\n---\n")
    )
    with TemporaryDirectory() as directory:
        root = Path(directory)
        (root / "index.md").write_text("---\n---\n", encoding="utf-8")
        assert any(
            problem.rule == "okf_base"
            for report in validate_pack(root)
            for problem in report.problems
        )
    print(
        "selftest OK — admission, version alignment, placeholder, parser, and invalid-pack gates"
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    """Run the OPF validator command-line interface."""
    parser = argparse.ArgumentParser(prog="opf.validate", description=__doc__)
    parser.add_argument("paths", nargs="*", type=Path)
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="require pinned imports and treat warnings as errors",
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
