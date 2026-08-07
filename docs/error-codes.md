# Stable OPF error codes

Validator problems expose a stable `code` (e.g. `OPF-E030`) alongside the rule name.
Codes are stable across releases; human-readable messages may change.
Agents and CI should key on the code, not the prose.

| Code | Rule |
|---|---|
| OPF-E001 | frontmatter_parse |
| OPF-E002 | okf_base |
| OPF-E003 | opf_version |
| OPF-E004 | version_alignment |
| OPF-E005 | type |
| OPF-E006 | title |
| OPF-E007 | opf_id |
| OPF-E008 | verified.by |
| OPF-E009 | verified.method |
| OPF-E010 | face_type |
| OPF-E011 | status |
| OPF-E012 | product_admission |
| OPF-E013 | validated_gate |
| OPF-E014 | operating_gate |
| OPF-E015 | retired_gate |
| OPF-E016 | kind |
| OPF-E017 | surface_traceability |
| OPF-E018 | surface_kind |
| OPF-E019 | state_transition |
| OPF-E020 | interaction_proof |
| OPF-E021 | acceptance_status |
| OPF-E022 | acceptance_evidence |
| OPF-E023 | slice_traceability |
| OPF-E024 | journey_traceability |
| OPF-E025 | moment_traceability |
| OPF-E026 | face_missing |
| OPF-E027 | duplicate_id |
| OPF-E028 | unresolved_ref |
| OPF-E029 | wrong_target_kind |
| OPF-E030 | orphan |
| OPF-E031 | log_missing |
| OPF-E032 | invalid_import |
| OPF-E033 | external_ref_unpinned |
| OPF-E034 | external_ref_profile |
| OPF-E035 | external_ref_unimported |
| OPF-E036 | supersession_kind |
| OPF-E037 | supersession_inverse |
| OPF-E038 | supersession_multi_head |
| OPF-E039 | first_slice_count |
| OPF-E040 | experience_chain |
| OPF-E041 | experience_outcome |
| OPF-E042 | validation_not_observed |
| OPF-E043 | operational_proof_not_observed |
| OPF-E044 | path |
| OPF-E045 | open_question_blocking |
| OPF-E046 | failed_acceptance_blocking |
| OPF-E047 | validation_coverage |

New rules receive the next free code. Deprecated rules keep their code permanently reserved.

See also `opf/codes.py` and the `Problem.code` property in the validator.
