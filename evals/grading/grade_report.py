#!/usr/bin/env python3
"""
grade_report.py — Score a Triage Report against a fixture's assertions.

Combines parse_report.py output with the fixture's ground_truth and assertions,
emitting a grading.json file in the format the skill-creator viewer expects.

Usage:
    python grade_report.py <fixture-dir> <report.md> [--out grading.json]

Inputs:
    fixture-dir: path to e.g. evals/fixtures/codec-compat
    report.md:   the Triage Report produced for that fixture

Output (default: ./grading.json):
    {
      "expectations": [
        {"text": "...", "passed": true,  "evidence": "..."},
        ...
      ],
      "summary": {"passed": N, "failed": M, "rate": 0.xx}
    }

The grading is a hybrid:
- For ground_truth fields the parser can extract (primary_gap, regen_test_result,
  scope_exposes_deferred, hotfix_needed_first, constitutional_implies,
  recommended_change_layer, cross_spec_contracts), grading is programmatic.
- For ground_truth fields that need semantic checking (e.g. "diagnosis identifies
  X"), this script emits {"passed": null, "evidence": "needs human review"}.
- ID hallucination check is programmatic: cited_ids cross-checked against IDs
  found in the fixture spec/plan/code files.

Run after the skill produces a report, before the eval-viewer step.
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

# Reuse the parser
sys.path.insert(0, str(Path(__file__).parent))
from parse_report import parse as parse_report, collect_requirement_ids


def collect_fixture_ids(fixture_dir: Path) -> set[str]:
    ids: set[str] = set()
    for f in fixture_dir.glob("*.md"):
        ids.update(collect_requirement_ids(f.read_text(encoding="utf-8")))
    constitution = fixture_dir.parent.parent / "shared" / "constitution.md"
    if constitution.exists():
        ids.update(collect_requirement_ids(constitution.read_text(encoding="utf-8")))
    return ids


def check(label: str, predicate: bool, evidence: str) -> dict:
    return {"text": label, "passed": bool(predicate), "evidence": evidence}


def _layer_match(expected, actual: str | None, label_prefix: str) -> tuple[bool, str]:
    """Match a layer-classification field against single- or list-valued ground truth.

    A single string means the canonical answer; the actual must equal it.
    A list of strings means genuine engineering disjunction; the actual must
    be one of them. The label is shaped so failures read clearly in the viewer.
    """
    if isinstance(expected, list):
        match = actual in set(expected)
        label = f"{label_prefix} is one of {sorted(expected)!r}"
    else:
        match = (actual == expected)
        label = f"{label_prefix} is '{expected}'"
    return match, label


def grade(fixture_dir: Path, report_path: Path) -> dict:
    metadata = json.loads((fixture_dir / "eval_metadata.json").read_text(encoding="utf-8"))
    ground_truth = metadata.get("ground_truth", {})
    parsed = parse_report(report_path.read_text(encoding="utf-8"))

    expectations: list[dict] = []

    # 1. Primary gap
    # Ground truth may be a single string (canonical answer) or a list of strings
    # (genuine engineering disjunction — see README "Single value vs list ground
    # truth"). The grader does exact string match against the value, or set
    # membership against the list. No taxonomy-level fallbacks: if a fixture
    # accepts multiple answers, it MUST say so explicitly.
    expected_gap = ground_truth.get("primary_gap")
    if expected_gap and expected_gap != "none-this-is-a-scope-question":
        actual = parsed.get("primary_gap")
        match, label = _layer_match(expected_gap, actual, "Layer Classification → Primary gap")
        expectations.append(check(label, match, f"got: {actual!r}"))

    # 2. Recommended change layer
    expected_rec = ground_truth.get("recommended_change_layer")
    if expected_rec and expected_rec != "n/a":
        actual = parsed.get("recommended_change_layer")
        match, label = _layer_match(expected_rec, actual, "Recommended Change → Layer")
        expectations.append(check(label, match, f"got: {actual!r}"))

    # 3. Regeneration test
    expected_regen = ground_truth.get("regen_test_result")
    if expected_regen and expected_regen != "n/a":
        actual = parsed.get("regen_test_result")
        expectations.append(check(
            f"Regeneration Test → Result is '{expected_regen}'",
            actual == expected_regen,
            f"got: {actual!r}"
        ))

    # 4. Scope check
    expected_scope = ground_truth.get("scope_exposes_deferred")
    if expected_scope:
        actual = (parsed.get("scope_exposes_deferred") or "")
        # 'yes_carefully' means yes-but-don't-promote; we just check it answered yes.
        # Use startswith() so reports that put a yes/no followed by inline prose
        # (e.g. "no. The relevant invariant — P2 — already covers this.") still grade
        # against the boolean answer.
        if expected_scope == "yes_carefully":
            match = actual.startswith("yes")
        else:
            match = actual.startswith(expected_scope)
        expectations.append(check(
            f"Scope Check → Exposes deferred functionality is '{expected_scope}'",
            match,
            f"got: {actual!r}"
        ))

    # 5. Hotfix
    expected_hotfix = ground_truth.get("hotfix_needed")
    if expected_hotfix:
        actual = parsed.get("hotfix_needed_first", "")
        match = actual.startswith(expected_hotfix)
        expectations.append(check(
            f"Tactical vs Structural → Hotfix needed first starts with '{expected_hotfix}'",
            match,
            f"got: {actual!r}"
        ))

    # 6. Constitutional implies
    expected_const = ground_truth.get("constitutional_implies")
    if expected_const and expected_const != "maybe":
        actual = (parsed.get("constitutional_implies") or "")
        # startswith() so an answer like "no. The existing P2 already covers this."
        # grades against the boolean.
        expectations.append(check(
            f"Constitutional Check → Implies project-wide invariant is '{expected_const}'",
            actual.startswith(expected_const),
            f"got: {actual!r}"
        ))

    # 7. Cross-spec contracts non-empty when expected
    expected_cross = ground_truth.get("cross_spec_contracts")
    if expected_cross == "none":
        actual = (parsed.get("cross_spec_contracts") or "").lower()
        # startswith() so reports that follow a `none` answer with explanatory
        # prose (e.g. "none. no shared contract is in dispute") still grade
        # against the boolean — mirrors how scope/hotfix/constitutional fields
        # already grade.
        expectations.append(check(
            "Cross-Spec Impact → Shared contracts touched starts with 'none' (no spurious cross-spec claim)",
            actual.startswith("none") or actual == "",
            f"got: {actual!r}"
        ))
    elif expected_cross is None and ground_truth.get("primary_gap") == "cross-spec":
        actual = (parsed.get("cross_spec_contracts") or "").lower()
        expectations.append(check(
            "Cross-Spec Impact → Shared contracts touched is non-empty",
            actual not in {"none", ""},
            f"got: {actual!r}"
        ))

    # 8. ID hallucination check — only against sections that REFERENCE existing
    # artifacts. Proposed amendments and new principles legitimately introduce
    # new IDs in Constitutional Check / Recommended Change, and those proposed
    # IDs may be cross-referenced in Cascade / Cross-Spec Impact / Open Questions
    # (where the report describes propagation of the proposed change). So:
    #   - Strip Constitutional Check + Recommended Change before extracting IDs
    #     to verify (proposing a new ID there is fine).
    #   - Treat IDs introduced in those proposing sections as "newly proposed"
    #     and accept them as valid wherever else they appear.
    # That way we still catch genuine hallucinations (an ID that appears
    # nowhere in the fixture artifacts AND is not introduced by the report's
    # own proposal) without punishing forward-references to legitimately
    # proposed IDs.
    report_text = report_path.read_text(encoding="utf-8")
    proposed_ids: set[str] = set()
    for proposing_heading in ("Constitutional Check", "Recommended Change"):
        pattern = rf"^##\s+{re.escape(proposing_heading)}\s*$\n(.*?)(?=^##\s+|\Z)"
        m = re.search(pattern, report_text, flags=re.DOTALL | re.MULTILINE)
        if m:
            proposed_ids.update(collect_requirement_ids(m.group(1)))

    referencing_text = report_text
    for excluded_heading in ("Constitutional Check", "Recommended Change"):
        pattern = rf"^##\s+{re.escape(excluded_heading)}\s*$\n.*?(?=^##\s+|\Z)"
        referencing_text = re.sub(pattern, "", referencing_text, flags=re.DOTALL | re.MULTILINE)

    fixture_ids = collect_fixture_ids(fixture_dir)
    referencing_ids = set(collect_requirement_ids(referencing_text))
    hallucinated = referencing_ids - fixture_ids - proposed_ids
    expectations.append(check(
        "Cited requirement IDs (in referencing sections) all exist in fixture artifacts",
        len(hallucinated) == 0,
        f"hallucinated: {sorted(hallucinated)!r}; checked: {sorted(referencing_ids)!r}"
    ))

    # 9. Schema completeness — all required sections present
    required_sections = [
        "Failure", "Context Loaded", "Diagnosis", "Layer Classification",
        "Regeneration Test", "Recommended Change", "Cascade",
        "Cross-Spec Impact", "Constitutional Check", "Scope Check",
        "Tactical vs Structural",
    ]
    present = set(parsed.get("sections_present", []))
    missing = [s for s in required_sections if s not in present]
    expectations.append(check(
        "Triage Report contains all required sections",
        len(missing) == 0,
        f"missing: {missing!r}"
    ))

    # Summary
    passed = sum(1 for e in expectations if e["passed"])
    failed = sum(1 for e in expectations if not e["passed"])
    total = passed + failed
    rate = round(passed / total, 3) if total else 0.0

    return {
        "fixture": fixture_dir.name,
        "expectations": expectations,
        "summary": {"passed": passed, "failed": failed, "total": total, "rate": rate},
    }


def main() -> int:
    if len(sys.argv) < 3:
        print("Usage: grade_report.py <fixture-dir> <report.md> [--out grading.json]",
              file=sys.stderr)
        return 1
    fixture_dir = Path(sys.argv[1])
    report_path = Path(sys.argv[2])
    out_path = Path("grading.json")
    if "--out" in sys.argv:
        out_path = Path(sys.argv[sys.argv.index("--out") + 1])

    result = grade(fixture_dir, report_path)
    out_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if result["summary"]["failed"] == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
