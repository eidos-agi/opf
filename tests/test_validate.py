import hashlib
import json
import shutil
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from opf.validate import parse_frontmatter, validate_document, validate_pack

EXAMPLE = Path(__file__).parents[1] / "examples" / "eidos-agent-manager"


def rules(reports):
    return {problem.rule for report in reports for problem in report.problems}


class ValidatorTests(unittest.TestCase):
    def copy_example(self, directory):
        root = Path(directory) / "pack"
        shutil.copytree(EXAMPLE, root)
        return root

    def test_example_is_strict_valid(self):
        self.assertFalse(
            [report for report in validate_pack(EXAMPLE, strict=True) if report.errors]
        )

    def test_parser_rejects_duplicate_keys(self):
        fm = parse_frontmatter('---\ntitle: "A"\ntitle: "B"\n---\n')
        self.assertIn(
            "frontmatter_parse",
            rules([type("R", (), {"problems": validate_document(fm)})()]),
        )

    def test_surface_requires_product_traceability(self):
        fm = {
            "okf_version": "0.2",
            "opf_version": "0.2.2",
            "type": "product-concept",
            "opf_id": "opf:test:surface:x",
            "kind": "surface",
            "title": "X",
            "serves": ["opf:test:outcome:x"],
            "verified": {"by": "agent:test", "method": "test"},
        }
        self.assertIn(
            "surface_traceability",
            rules([type("R", (), {"problems": validate_document(fm)})()]),
        )

    def test_observed_acceptance_requires_evidence(self):
        fm = {
            "okf_version": "0.2",
            "opf_version": "0.2.2",
            "type": "product-concept",
            "opf_id": "opf:test:acceptance:x",
            "kind": "acceptance",
            "title": "X",
            "condition": "X happens",
            "status": "observed",
            "verified": {"by": "agent:test", "method": "test"},
        }
        self.assertIn(
            "acceptance_evidence",
            rules([type("R", (), {"problems": validate_document(fm)})()]),
        )

    def test_local_evidence_closes_validated_lifecycle(self):
        with TemporaryDirectory() as directory:
            root = self.copy_example(directory)
            acceptance = root / "concepts" / "07-acceptance-decision-brief.md"
            evidence_dir = root / "evidence"
            evidence_dir.mkdir()
            receipt = {
                "subject": "opf:eam:acceptance:decision-brief",
                "observed_at": "2026-08-07T23:30:00Z",
                "method": "mechanical fixture proof",
                "source_revision": "test-revision",
                "result": "passed",
                "checks": ["fixture passed"],
            }
            payload = (json.dumps(receipt, indent=2) + "\n").encode()
            evidence_path = evidence_dir / "decision-brief.json"
            evidence_path.write_bytes(payload)
            ref = f"file:evidence/decision-brief.json@sha256-{hashlib.sha256(payload).hexdigest()}"
            acceptance.write_text(
                acceptance.read_text()
                .replace("status: proposed", "status: observed")
                .replace("verified:\n", f"evidence: [{ref}]\nverified:\n")
            )
            face = root / "index.md"
            face.write_text(
                face.read_text()
                .replace("status: shaping", "status: validated")
                .replace("proof: [opf:eam:acceptance:decision-brief]", "proof: [opf:eam:acceptance:decision-brief]\nvalidation: [opf:eam:acceptance:decision-brief]")
            )
            self.assertFalse(
                [report for report in validate_pack(root, strict=True) if report.errors]
            )

    def test_local_evidence_digest_mismatch_is_rejected(self):
        with TemporaryDirectory() as directory:
            root = self.copy_example(directory)
            acceptance = root / "concepts" / "07-acceptance-decision-brief.md"
            acceptance.write_text(
                acceptance.read_text().replace(
                    "status: proposed",
                    f"status: observed\nevidence: [file:evidence/proof.json@sha256-{'0' * 64}]",
                )
            )
            evidence_dir = root / "evidence"
            evidence_dir.mkdir()
            (evidence_dir / "proof.json").write_text("{}\n")
            self.assertIn("evidence_digest", rules(validate_pack(root, strict=True)))

    def test_local_evidence_cannot_escape_evidence_directory(self):
        with TemporaryDirectory() as directory:
            root = self.copy_example(directory)
            acceptance = root / "concepts" / "07-acceptance-decision-brief.md"
            acceptance.write_text(
                acceptance.read_text().replace(
                    "status: proposed",
                    f"status: observed\nevidence: [file:evidence/../proof.json@sha256-{'0' * 64}]",
                )
            )
            self.assertIn("evidence_file_ref", rules(validate_pack(root, strict=True)))

    def test_wrong_first_slice_kind_is_rejected(self):
        with TemporaryDirectory() as directory:
            root = self.copy_example(directory)
            face = root / "index.md"
            face.write_text(
                face.read_text().replace(
                    "first_slice: opf:eam:slice:first-orientation",
                    "first_slice: opf:eam:acceptance:decision-brief",
                )
            )
            self.assertIn("wrong_target_kind", rules(validate_pack(root, strict=True)))

    def test_unpinned_external_intent_is_rejected_in_strict_mode(self):
        with TemporaryDirectory() as directory:
            root = self.copy_example(directory)
            face = root / "index.md"
            face.write_text(
                face.read_text().replace(
                    "intent: [emf:eam:executive-office@2026-08-07]",
                    "intent: [emf:eam:executive-office]",
                )
            )
            self.assertIn(
                "external_ref_unpinned", rules(validate_pack(root, strict=True))
            )

    def test_wrong_external_profile_is_rejected(self):
        with TemporaryDirectory() as directory:
            root = self.copy_example(directory)
            face = root / "index.md"
            text = (
                face.read_text()
                .replace("emf:eam@", "orf:eam@")
                .replace("emf:eam:executive-office@", "orf:eam:executive-office@")
            )
            face.write_text(text)
            self.assertIn(
                "external_ref_profile", rules(validate_pack(root, strict=True))
            )

    def test_incomplete_experience_chain_is_rejected(self):
        with TemporaryDirectory() as directory:
            root = self.copy_example(directory)
            state = root / "concepts" / "05-state-conflicting.md"
            state.write_text(
                state.read_text().replace(
                    "allows: [opf:eam:interaction:inspect-conflict]\n", ""
                )
            )
            found = rules(validate_pack(root, strict=True))
            self.assertIn("state_transition", found)
            self.assertIn("experience_chain", found)

    def test_interaction_cannot_yield_unrelated_outcome(self):
        with TemporaryDirectory() as directory:
            root = self.copy_example(directory)
            face = root / "index.md"
            face.write_text(
                face.read_text().replace(
                    "outcomes: [opf:eam:outcome:protect-attention]",
                    "outcomes: [opf:eam:outcome:protect-attention, opf:eam:outcome:unrelated]",
                )
            )
            outcome = root / "concepts" / "13-outcome-unrelated.md"
            outcome.write_text(
                '---\nokf_version: "0.2"\nopf_version: "0.2.2"\ntype: product-concept\n'
                'opf_id: opf:eam:outcome:unrelated\nkind: outcome\ntitle: "Unrelated"\n'
                'verified:\n  by: agent:test\n  method: "test"\n---\n'
            )
            interaction = root / "concepts" / "12-interaction-inspect-conflict.md"
            interaction.write_text(
                interaction.read_text().replace(
                    "yields: opf:eam:outcome:protect-attention",
                    "yields: opf:eam:outcome:unrelated",
                )
            )
            self.assertIn("experience_outcome", rules(validate_pack(root, strict=True)))

    def test_one_way_supersession_is_rejected(self):
        with TemporaryDirectory() as directory:
            root = self.copy_example(directory)
            current = root / "concepts" / "09-problem-coordination.md"
            current.write_text(
                current.read_text().replace(
                    "serves: [opf:eam:outcome:protect-attention]",
                    "serves: [opf:eam:outcome:protect-attention]\nsupersedes: opf:eam:problem:old",
                )
            )
            old = root / "concepts" / "13-problem-old.md"
            old.write_text(
                '---\nokf_version: "0.2"\nopf_version: "0.2.2"\ntype: product-concept\n'
                'opf_id: opf:eam:problem:old\nkind: problem\ntitle: "Old"\n'
                'verified:\n  by: agent:test\n  method: "test"\n---\n'
            )
            self.assertIn(
                "supersession_inverse", rules(validate_pack(root, strict=True))
            )

    def test_placeholder_non_goal_is_rejected(self):
        with TemporaryDirectory() as directory:
            root = self.copy_example(directory)
            face = root / "index.md"
            face.write_text(
                face.read_text().replace(
                    'non_goals: ["ambient surveillance", "replacing native lifecycle authorities"]',
                    "non_goals: [TBD]",
                )
            )
            self.assertIn("product_admission", rules(validate_pack(root, strict=True)))

    def test_serves_back_reference_does_not_hide_an_orphan(self):
        with TemporaryDirectory() as directory:
            root = self.copy_example(directory)
            orphan = root / "concepts" / "13-risk-orphan.md"
            orphan.write_text(
                '---\nokf_version: "0.2"\nopf_version: "0.2.2"\ntype: product-concept\n'
                'opf_id: opf:eam:risk:orphan\nkind: risk\ntitle: "Orphan"\n'
                "serves: [opf:eam:outcome:protect-attention]\n"
                'verified:\n  by: agent:test\n  method: "test"\n---\n'
            )
            self.assertIn("orphan", rules(validate_pack(root, strict=True)))


if __name__ == "__main__":
    unittest.main()
