# spectastic-debugger

A Claude Code skill (and eval harness) for debugging defects inside a spec-driven development workflow. Classifies bugs by layer (constitution / spec / plan / implementation / cross-spec) and proposes fixes at the highest layer that needed to change.

## Install

**Recommended — via the spectastic marketplace** (one marketplace, many spec-driven-development plugins):

```
/plugin marketplace add spectastic/marketplace
/plugin install spectastic-debugger
```

After the marketplace is added once, future plugins from spectastic install by name.

**Or direct from this repo:**

```
/plugin install spectastic/spectastic-debugger-skill
```

**Or manual:** clone the repo and copy `skills/spectastic-debugger/` into `~/.claude/skills/`.

## What it triggers on

The skill fires automatically when you describe a bug, defect, regression, or audit failure in a spec-driven project — even without saying "SDD" or "SpecKit". Strong implicit signals:

- Filenames like `spec.md`, `plan.md`, `tasks.md`, `constitution.md` mentioned alongside a failure.
- Requirement-shaped IDs in the prompt (e.g. `FREQ-003`, `NFR-001`, `AC-2`, `P1`, `TD-4`).
- Mentions of `/speckit.plan`, `/speckit.tasks`, `/speckit.implement`, deferred requirements, the regeneration test.
- Questions like "is this a spec issue or a code bug?", "where does the fix belong?", "does this need a new constitutional principle?", "are we silently expanding scope?"

It produces a structured Triage Report classifying the gap (constitution / spec / plan / cross-spec / implementation) and proposing the fix at the highest layer that needed to change. See [`skills/spectastic-debugger/references/triage-report-schema.md`](skills/spectastic-debugger/references/triage-report-schema.md) for the exact format.

## Layout

```
spectastic-debugger-skill/
├── README.md                                  # this file
├── HOW-TO-RUN.md                              # how to run the eval harness
├── .claude-plugin/
│   └── plugin.json                            # plugin manifest
├── skills/
│   └── spectastic-debugger/
│       ├── SKILL.md                           # the skill itself
│       └── references/
│           ├── triage-report-schema.md        # output format
│           └── gap-taxonomy.md                # classification taxonomy
└── evals/
    ├── shared/
    │   └── constitution.md                    # shared project constitution
    ├── grading/
    │   ├── parse_report.py                    # extract structured fields from a report
    │   └── grade_report.py                    # programmatic assertion checking
    └── fixtures/
        ├── codec-compat/                      # constitutional gap (under-escalation canary)
        ├── dst-rollover/                      # spec gap (over-escalation canary)
        ├── crypto-algo/                       # plan gap (NFR violation)
        ├── off-by-one/                        # implementation gap (over-escalation canary)
        ├── ui-capture-format-mismatch/        # cross-spec drift
        ├── deferred-temptation/               # scope-trap (silent scope creep canary)
        └── hotfix-needed/                     # implementation gap requiring tactical+structural fix
```

Each fixture contains:
- `spec.md` (sometimes `spec-capture.md` / `spec-ui.md` for cross-spec cases)
- `plan.md`
- `code.md` (implementation snippet + observed failure)
- `eval_metadata.json` (the prompt to send the agent + ground truth + assertions)

## What the seven fixtures test

| Fixture | Tests | Canary for |
|---|---|---|
| `codec-compat` | Constitutional gap — class-wide portability invariant | **Under-escalation** (skill stops at spec when bug-class recurs across features) |
| `dst-rollover` | Spec gap — missing functional requirement on a feature-local concern | **Over-escalation** (skill reaches for a new constitutional principle when spec is the right home) |
| `crypto-algo` | Plan gap — NFR violation in technical decision | Confusing plan gap with spec gap |
| `off-by-one` | Implementation gap — pure code typo | **Over-escalation** at the bottom edge (escalating a typo to spec) |
| `ui-capture-format-mismatch` | Cross-spec drift on shared contract | Patching one spec when the contract belongs upstream (shared spec section *or* constitutional principle — both legitimate) |
| `deferred-temptation` | Scope question disguised as bug | **Silent scope creep** |
| `hotfix-needed` | Implementation gap with production pressure | Hotfix-only without queueing structural fix |

`codec-compat` and `dst-rollover` together test both edges of the under/over-escalation line — a skill that uniformly answers "spec" gets one wrong; a skill that uniformly proposes new constitutional principles gets the other wrong. The right behavior is taxonomy-driven, asking "does this bug-class recur across features?" before reaching for the constitution. `off-by-one` and `deferred-temptation` are the other diagnostic edges.

## Quick start

See `HOW-TO-RUN.md` for the full skill-creator workflow.

Short version:
1. Open this folder in Claude Code.
2. Invoke skill-creator with: *"Evaluate the skill at `skills/spectastic-debugger/` against the seven fixtures in `evals/fixtures/`. The eval prompts and ground truth are in each fixture's `eval_metadata.json`. Use `evals/grading/grade_report.py` to score each report programmatically."*
3. Review the eval-viewer output, leave qualitative feedback on the failure cases, iterate.

## Related principles in the constitution

The shared constitution (`evals/shared/constitution.md`) defines six principles (P1–P6) the skill must respect. Some fixtures reference these principles directly; one (`codec-compat`) is a candidate for adding a new principle.

## Ground truth: single value vs list

In each fixture's `eval_metadata.json`, layer-classification fields (`primary_gap`, `recommended_change_layer`) are usually a single string — the canonical answer. Occasionally a fixture uses a list (e.g. `["spec", "constitution"]`) to express genuine engineering disjunction.

**Use a single value when the taxonomy points to one answer.** Most defects have one correct layer once you apply the gap-taxonomy rigorously. `codec-compat` is canonically a constitutional gap (the bug-class recurs across every output-producing feature). `dst-rollover` is canonically a spec gap (timestamps are a Recording Metadata concern; constitutional escalation here would be over-engineering). Hedging a single-answer fixture into a list weakens the test — a skill that lands on the wrong canonical answer should fail, and a list lets it pass on the wrong-but-listed alternative.

**Use a list only when both options are genuinely correct.** `ui-capture-format-mismatch` lists `["spec", "constitution"]` for `recommended_change_layer` because the codec contract can legitimately be lifted to either a shared spec section both specs reference, or a more concrete constitutional principle about codec/format vocabularies. Both honor existing P4. A skill picking either one is making a reasonable call; only the third (a code-only patch) is wrong.

**The design rule:** a list is for genuine engineering ambiguity, not for grader hedging. If you find yourself reaching for a list to avoid hard-coding a verdict, ask whether the taxonomy actually points to one answer and you're under-committing. Single values make the eval set sharper.
