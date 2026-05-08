# Triage Report Schema

The Triage Report is the canonical output of the SDD staff-debugger skill. Downstream tooling parses these reports, so the section headings and field names below are required as written.

Output the report as markdown, with `## Section Name` headings exactly as listed.

## Required Sections

```markdown
## Failure
- Reproduction: <steps to reproduce>
- Expected: <expected behavior>
- Actual: <observed behavior>
- Environment: <OS, runtime, version, hardware as relevant>

## Context Loaded
- Constitution: <path>, version: <version or "unspecified">
- Spec: <path>, requirement IDs touched: <REQ-001, REQ-002, ...>
- Plan: <path>, sections touched: <section names>
- Related specs: <paths, or "none">
- Implementation: <files read>
- Skipped (with reason): <files/artifacts you chose not to read and why, or "none">

## Diagnosis
<Root cause in 1–2 sentences. State the cause, not the symptom. No hedging.>

## Layer Classification
- Primary gap: <spec | plan | implementation | cross-spec | constitution>
- Secondary gaps: <list, or "none">
- Reasoning: <why this layer, not the one above or below. Reference specific requirement IDs or plan sections.>

## Regeneration Test
- Result: <Pass | Fail>
- Explanation: <Would current spec and plan reproduce the bug if the implementation were regenerated from scratch? Pass = bug would NOT recur (gap is in code). Fail = bug WOULD recur (gap is upstream).>

## Recommended Change
- Layer: <spec | plan | implementation | constitution>
- Artifact: <path>
- Change type: <amendment | new requirement | new NFR | refactor | regression test | new principle | release-notes entry | external-tracker filing>
- Proposed text / diff: <concrete proposal>
- Rationale: <why this change, at this layer>

## Cascade
- Regenerate: </speckit.plan | /speckit.tasks | /speckit.implement | none>
- Affected downstream artifacts: <list>

## Cross-Spec Impact
- Shared contracts touched: <list, or "none">
- Other specs requiring update: <list, or "none">

## Constitutional Check
- Implies project-wide invariant: <yes | no>
- Proposed amendment: <text, or "N/A">

## Scope Check
- Exposes deferred functionality: <yes | no>
- If yes: <surface as separate scope question; do NOT expand active scope here>

## Tactical vs Structural
- Hotfix needed first: <yes | no, with reasoning>
- Structural fix scheduled for: <next regen | this PR | dedicated amendment | N/A>

## Summary
| Layer | Status | Note |
|---|---|---|
| Constitution | <ok / gap / amendment-proposed / n/a> | <one-line evidence> |
| Spec | <ok / gap / amendment-proposed / n/a> | <one-line evidence> |
| Plan | <ok / gap / amendment-proposed / n/a> | <one-line evidence> |
| Implementation | <ok / gap / hotfix-needed / n/a> | <one-line evidence> |
| Tests | <ok / missing / required-by-P6 / n/a> | <one-line evidence — does a regression test exist or is one mandated by P6?> |

- Primary gap: <copy from Layer Classification above>
- Regeneration test: <copy from Regeneration Test above>
- Hotfix needed: <copy from Tactical vs Structural above>
- Scope expansion risk: <copy from Scope Check above>

## Open Questions
1. <First question that needs human confirmation before editing>
2. <Second question, if any>
3. <…or "none" if everything above is unambiguous>
```

## Field Constraints

- **Primary gap** must be one of: `spec`, `plan`, `implementation`, `cross-spec`, `constitution`. Lowercase.
- **Regeneration Test → Result** must be exactly `Pass` or `Fail`.
- **Scope Check → Exposes deferred functionality** must be exactly `yes` or `no`.
- **Tactical vs Structural → Hotfix needed first** must start with exactly `yes` or `no`.
- **Constitutional Check → Implies project-wide invariant** must be exactly `yes` or `no`.
- **Recommended Change → Layer** must be one of: `spec`, `plan`, `implementation`, `constitution`. Lowercase.

## Formatting Conventions

The headings and field names are non-negotiable (downstream tooling parses them), but the *prose inside* each section should be formatted for human readability. A reviewer will read dozens of these reports a week — make their eyes happy.

- **Bold every field label** in bullets: `- **Reproduction:** ...` rather than `- Reproduction: ...`. The grader tolerates either, but bold labels scan much faster when a reviewer is skimming for "Layer" or "Hotfix needed first".
- **Code-fence everything code-shaped:** file paths, line numbers, function names, requirement IDs, config values, and small inline snippets. Use single backticks for inline (`AudioCapture.swift:8`) and triple-backtick fences with a language tag for multi-line blocks. Plain prose mentions of `FREQ-003` are easier to scan than FREQ-003.
- **Use tables for parallel data.** Action items with priority columns, before/after comparisons of values across DST boundaries, regression-test inputs and expected outputs — anything that's a list of records with the same shape is a table, not a bullet list. The Summary table is the canonical example; mirror that style elsewhere.
- **Number every ordered list.** Sub-steps inside `## Recommended Change`, items under `## Open Questions`, sequenced action plans — if order or count matters, use `1.` `2.` `3.`, not bullets. Numbering also gives a reviewer something to refer back to ("OQ #2 needs product input"), which bullets don't.
- **Use a sign-off / verification checklist** at the bottom of `## Recommended Change` (or in `## Open Questions`) for any change that needs explicit confirmation steps. `- [ ] Item` rendered as a checkbox is a clear hand-off to the implementer.
- **Bold sparingly inside prose** — only on the load-bearing conclusion of a paragraph (e.g., "**This is a plan gap, not a code gap.**"). Bolding everything makes nothing stand out.
- **Indent nested context** with two spaces under its parent bullet. Don't dump multi-paragraph rationale on a single bullet — break it up.

## Layer Ordering Convention

When you list multiple layers in a row (Summary table, Layer Classification's secondary list, Cascade), order them top-down: **Constitution → Spec → Plan → Implementation**. This matches the SDD generation flow and lets a reader see at a glance how high in the stack the gap sits without re-sorting in their head. Cross-spec drift sits beside Spec.

## Code Fix Annotation Style

When the Recommended Change is at the implementation layer, present the fix as an annotated diff that points at the exact offending location. Don't just paste the corrected file — show the reader what changed and why. Use a fenced code block with a comment marker that points to the row, like:

```text
TimerLabel.swift, line 14, in format(_:)
                                      ↓
    let seconds = (totalSeconds % 60) - 1   ← off-by-one: stray "- 1"
                                            should be: totalSeconds % 60
```

Or a unified diff with one-line rationale per hunk. The point is the reader's eye lands on the bug before it lands on the fix.

## Why the strict format

The grader and any propagation pipeline read these fields by exact heading and prefix. Loose formatting breaks downstream automation. The structure is also a discipline — it forces you through the regeneration test and the scope check rather than letting you jump to a fix.

The Summary table near the end is a deliberate redundancy: it lets a reviewer who has just read the full report walk away with a clean recap, and lets someone returning later see the verdict in five seconds. **Populate it after the canonical sections above are finalised** — it should be a copy-down of conclusions you have already justified, never the place where you make up your mind. Putting it after the reasoning is what keeps that discipline honest: if you are filling in the table, your thinking is already done.

Open Questions sits *after* the Summary on purpose: the recap closes the triage, and Open Questions is the action list the reader takes away. The document deliberately ends on what is unresolved, not on the recap, so the reader closes the page with the decisions that are still theirs to make.
