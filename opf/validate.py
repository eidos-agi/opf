"""Validate Open Product Format v0.2.1 documents and packs.

Stdlib only. The parser accepts the deliberately small YAML subset OPF specifies
and fails closed on syntax it cannot represent faithfully.
"""

from __future__ import annotations

import argparse
import csv
import re
from dataclasses import dataclass, field
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

from . import OKF_VERSION, OPF_VERSION
from .codes import ERROR_CODES

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

    @property
    def code(self) -> str:
        return ERROR_CODES.get(self.rule, "OPF-E000")


@dataclass
class Report:
    path: Path
    problems: list[Problem] = field(default_factory=list)

    @property
    def errors(self) -> list[Problem]:
        return [problem for problem in self.problems if problem.level == "error"]


def parse_frontmatter(text: str) -> dict[str, Any]:
    if not text.startswith("---"):
        return {"__parse_errors__": ["missing opening frontmatter delimiter"]}
    end = text.find("\n---", 3)
    if end == -1:
        return {"__parse_errors__": ["missing closing frontmatter delimiter"]}
    return _parse_yaml_block(text[3:end])
