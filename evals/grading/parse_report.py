#!/usr/bin/env python3
"""
parse_report.py — Extract structured fields from a Triage Report.

The spectastic-debugger skill produces reports in a fixed markdown format
(see skills/spectastic-debugger/references/triage-report-schema.md). This script
parses one and emits a JSON object the eval grader can use to check assertions
programmatically.

Usage:
    python parse_report.py <report.md>

Outputs JSON with the key extracted fields. Missing sections produce null.
"""
from __future__ import annotations
import re
import sys
import json
from pathlib import Path


def extract_section(text: str, heading: str) -> str | None:
    """Return content under a `## <heading>` block, until the next `## ` or EOF."""
    pattern = rf"^##\s+{re.escape(heading)}\s*$\n(.*?)(?=^##\s+|\Z)"
    m = re.search(pattern, text, re.DOTALL | re.MULTILINE)
    return m.group(1).strip() if m else None


def extract_field(section: str | None, field: str) -> str | None:
    """Return the value of a `- Field: value` bullet inside a section.

    Tolerates markdown bolding and code-fenced (backtick) values, so reports
    formatted as `- **Field:** value`, `- Field: value`, `- **Field:** \`value\``,
    or `- Field: \`value\`` all parse the same. The bold and backtick markers
    are stripped before regex matching so the field-name contract stays simple
    and the value comparison stays exact.
    """
    if not section:
        return None
    cleaned = section.replace("**", "")
    pattern = rf"^[-*]\s*{re.escape(field)}\s*:\s*(.+?)$"
    m = re.search(pattern, cleaned, re.MULTILINE)
    if not m:
        return None
    value = m.group(1).strip()
    # Strip wrapping backticks: `spec` -> spec; ``Pass`` -> Pass
    value = value.strip("`").strip()
    return value


def collect_requirement_ids(text: str) -> list[str]:
    """Pull all requirement-shaped IDs cited anywhere in the report."""
    pattern = r"\b(?:[A-Z]{2,5}REQ|FREQ|REQ|NFR|SNFR|MREQ|TREQ|UREQ|AREQ|TD|US|AC|FEAT|P)-?\d+"
    return sorted(set(re.findall(pattern, text)))


def parse(text: str) -> dict:
    layer_section = extract_section(text, "Layer Classification")
    recommended_section = extract_section(text, "Recommended Change")
    regen_section = extract_section(text, "Regeneration Test")
    scope_section = extract_section(text, "Scope Check")
    tactical_section = extract_section(text, "Tactical vs Structural")
    constitutional_section = extract_section(text, "Constitutional Check")
    cross_spec_section = extract_section(text, "Cross-Spec Impact")
    diagnosis_section = extract_section(text, "Diagnosis")
    context_section = extract_section(text, "Context Loaded")

    return {
        "primary_gap": (extract_field(layer_section, "Primary gap") or "").lower() or None,
        "secondary_gaps": extract_field(layer_section, "Secondary gaps"),
        "recommended_change_layer": (extract_field(recommended_section, "Layer") or "").lower() or None,
        "recommended_change_type": extract_field(recommended_section, "Change type"),
        "regen_test_result": extract_field(regen_section, "Result"),
        "scope_exposes_deferred": (extract_field(scope_section, "Exposes deferred functionality") or "").lower() or None,
        "hotfix_needed_first": (extract_field(tactical_section, "Hotfix needed first") or "").lower(),
        "constitutional_implies": (extract_field(constitutional_section, "Implies project-wide invariant") or "").lower() or None,
        "cross_spec_contracts": extract_field(cross_spec_section, "Shared contracts touched"),
        "diagnosis": diagnosis_section,
        "context_loaded": context_section,
        "cited_ids": collect_requirement_ids(text),
        "sections_present": [
            s for s in [
                "Failure", "Context Loaded", "Diagnosis", "Layer Classification",
                "Regeneration Test", "Recommended Change", "Cascade",
                "Cross-Spec Impact", "Constitutional Check", "Scope Check",
                "Tactical vs Structural", "Open Questions",
            ] if extract_section(text, s) is not None
        ],
    }


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: parse_report.py <report.md>", file=sys.stderr)
        return 1
    path = Path(sys.argv[1])
    if not path.exists():
        print(f"File not found: {path}", file=sys.stderr)
        return 1
    parsed = parse(path.read_text(encoding="utf-8"))
    print(json.dumps(parsed, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
