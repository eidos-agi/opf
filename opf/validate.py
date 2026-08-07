"""Validate Open Product Format v0.2.1 documents and packs.

Bootstrap: loads the last known-good implementation (ca9cc72) and applies
error-code wiring. Temporary until the full in-tree source is restored.
"""
from __future__ import annotations

import urllib.request

_BASE_URL = (
    "https://raw.githubusercontent.com/eidos-agi/opf/"
    "ca9cc72cb463b5c056e727ceb800d54fc6f8a5a3/opf/validate.py"
)

_src = urllib.request.urlopen(_BASE_URL, timeout=30).read().decode()

# Wire stable error codes (opf.codes)
_src = _src.replace(
    "from . import OKF_VERSION, OPF_VERSION",
    "from . import OKF_VERSION, OPF_VERSION\nfrom .codes import ERROR_CODES",
    1,
)
_src = _src.replace(
    (
        "@dataclass\n"
        "class Problem:\n"
        "    level: str\n"
        "    rule: str\n"
        "    detail: str\n\n\n"
        "@dataclass\n"
        "class Report:"
    ),
    (
        "@dataclass\n"
        "class Problem:\n"
        "    level: str\n"
        "    rule: str\n"
        "    detail: str\n\n"
        "    @property\n"
        "    def code(self) -> str:\n"
        "        return ERROR_CODES.get(self.rule, \"OPF-E000\")\n\n\n"
        "@dataclass\n"
        "class Report:"
    ),
    1,
)
_src = _src.replace(
    'print(f"        {problem.level:<5} {problem.rule}: {problem.detail}")',
    'print(f"        {problem.level:<5} {problem.code} {problem.rule}: {problem.detail}")',
    1,
)

_ns: dict = {"__name__": __name__, "__file__": __file__}
exec(compile(_src, __file__, "exec"), _ns)

globals().update(
    {
        k: _ns[k]
        for k in (
            "Problem",
            "Report",
            "parse_frontmatter",
            "validate_document",
            "validate_pack",
            "validate_path",
            "selftest",
            "main",
        )
        if k in _ns
    }
)

if __name__ == "__main__":
    raise SystemExit(main())  # type: ignore[name-defined]
