import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from opf.validate import parse_frontmatter, validate_document, validate_pack


class ValidatorTests(unittest.TestCase):
    def test_frontmatter_nested_verified(self):
        fm = parse_frontmatter(
            '---\nokf_version: "0.2"\nopf_version: "0.2.0"\ntype: product-concept\n'
            'opf_id: opf:test:outcome:x\nkind: outcome\ntitle: "X"\n'
            'verified:\n  by: agent:test\n  method: "test"\n---\n'
        )
        self.assertEqual(fm["verified"]["by"], "agent:test")
        self.assertFalse([p for p in validate_document(fm) if p.level == "error"])

    def test_surface_requires_states_and_proof(self):
        fm = {
            "okf_version": "0.2",
            "opf_version": "0.2.0",
            "type": "product-concept",
            "opf_id": "opf:test:surface:x",
            "kind": "surface",
            "title": "X",
            "serves": ["opf:test:outcome:x"],
            "verified": {"by": "agent:test", "method": "test"},
        }
        rules = {p.rule for p in validate_document(fm) if p.level == "error"}
        self.assertIn("surface_traceability", rules)

    def test_pack_rejects_unresolved_and_orphan_concepts(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            root.joinpath("index.md").write_text(
                '---\nokf_version: "0.2"\nopf_version: "0.2.0"\ntype: product\n'
                'opf_id: opf:test:product\ntitle: "Test"\nstatus: concept\n'
                'outcomes: [opf:test:missing]\nverified:\n  by: agent:test\n  method: "test"\n---\n',
                encoding="utf-8",
            )
            root.joinpath("orphan.md").write_text(
                '---\nokf_version: "0.2"\nopf_version: "0.2.0"\ntype: product-concept\n'
                'opf_id: opf:test:orphan\nkind: risk\ntitle: "Orphan"\n'
                'verified:\n  by: agent:test\n  method: "test"\n---\n',
                encoding="utf-8",
            )
            root.joinpath("log.md").write_text("# Log\n", encoding="utf-8")
            rules = {
                problem.rule
                for report in validate_pack(root)
                for problem in report.problems
            }
            self.assertIn("unresolved_ref", rules)
            self.assertIn("orphan", rules)


if __name__ == "__main__":
    unittest.main()
