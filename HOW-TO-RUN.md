# How to Run This Project

Designed for **Claude Code** (full skill-creator workflow with subagents). Notes for Claude.ai are at the bottom.

## Prerequisites

- skill-creator skill available in your Claude environment.
- Python 3.10+ on the path (for the grading scripts).
- Working directory: this project's root.

## One-shot prompt for Claude Code

Open this folder and tell Claude:

> I want to evaluate the skill at `skills/spectastic-debugger/` using skill-creator. The eval set is in `evals/fixtures/` — there are eight fixtures, each with its own `eval_metadata.json` containing the prompt, ground truth, and assertions. The shared constitution is at `evals/shared/constitution.md`. After each test run produces a Triage Report, score it programmatically with `python3 evals/grading/grade_report.py <fixture-dir> <report.md>`. Run all eight fixtures, both with the skill and as baseline (no skill), aggregate results into a benchmark, and launch the eval viewer so I can review qualitative outputs.

skill-creator will then:
1. Spawn one subagent per fixture with the skill loaded; one without (baseline).
2. Each subagent reads the fixture's spec/plan/code/constitution, follows the skill, produces a Triage Report.
3. Run `grade_report.py` against each report to produce `grading.json`.
4. Aggregate into `benchmark.json` (pass rate, time, tokens, with-skill vs baseline).
5. Open the eval viewer for your qualitative review.

## What to look for in the results

**Programmatic assertions (in `grading.json`):**
- Layer classification matches ground truth.
- Regeneration test result matches ground truth.
- Scope check correctly identifies deferred-functionality cases.
- Hotfix flag set correctly on `hotfix-needed`.
- Cross-spec contracts identified on `ui-capture-format-mismatch`.
- No hallucinated requirement IDs.
- All required Triage Report sections present.

**Qualitative review (in the eval-viewer Outputs tab):**
- **Sharpness of diagnosis.** Is the root cause stated cleanly, or is it hedged?
- **Quality of proposed amendments.** Does the proposed text actually fit the spec's tagging conventions and language?
- **Reasoning depth.** Does the report show the layer-by-layer trace, or jump to a conclusion?
- **Anti-pattern avoidance.** Any over-escalation, under-escalation, or silent scope creep?

## The four diagnostic canaries

When iterating, watch these four fixtures specifically:

1. **`off-by-one`** — if the skill blames the spec or plan, it's reading "fix at the highest layer" too dogmatically. The regeneration test is the discriminator; emphasize it harder.
2. **`deferred-temptation`** — if the skill proposes promoting deferred items, the scope guardrail is too soft. Add explicit positive-list language.
3. **`codec-compat`** — if the skill proposes swapping codec in code without a spec amendment, the principle isn't pushy enough on upstream-fix.
4. **`liquid-glass-artifacts`** — if the skill classifies as `implementation` because the regen test "passes" (or proposes a SCStream knob change as the primary fix), the regeneration heuristic is being applied mechanically without checking whether the bug lives inside the project's stack at all. The discriminator is the screenshot-side reproduction (`screencapture(1)` shows the same artifacts). The right answer is structural — a constitutional protocol for platform-bug handling, paired with a release-notes cascade.

A revision that improves these four without regressing the others is a good revision.

## Iteration loop

1. Run all 8 fixtures. Review benchmark.
2. Read the failure cases in the viewer; leave specific feedback.
3. Modify `skills/spectastic-debugger/SKILL.md` (or the references) based on feedback.
4. Re-run; the `--previous-workspace` flag in skill-creator's viewer lets you compare iterations side-by-side.
5. Stop when:
   - All canaries pass.
   - You're happy with the qualitative outputs.
   - The benchmark shows clear improvement over the no-skill baseline.

## Description optimization (final pass)

After the skill behavior is stable, run skill-creator's `run_loop.py` against the fixture prompts to optimize the frontmatter `description` for triggering accuracy. This tunes WHEN the skill triggers, not WHAT it does.

```bash
python -m scripts.run_loop \
  --eval-set <path-to-trigger-eval.json> \
  --skill-path skills/spectastic-debugger \
  --model <model-id> \
  --max-iterations 5 \
  --verbose
```

Build the trigger-eval JSON with both positive cases (the eight fixture prompts) and negative cases (e.g., "help me write a python loop", "what's the capital of France") to avoid over-triggering.

## Running on Claude.ai (no subagents)

If you're on Claude.ai instead of Claude Code:
- Skip baseline runs and benchmarking.
- Run each fixture serially: read SKILL.md, follow it on the fixture's prompt, save the report.
- Run `grade_report.py` after each report.
- Skip the eval viewer; review reports inline.
- Skip description optimization (requires the `claude` CLI).

## Manual single-fixture run

To debug one fixture without the full harness:

```bash
# 1. Read the skill, then run the fixture prompt manually in Claude
# 2. Save the resulting Triage Report to /tmp/report.md
# 3. Grade it:
python3 evals/grading/grade_report.py evals/fixtures/codec-compat /tmp/report.md
```

The grader will exit non-zero if any assertion failed and print a JSON breakdown.

## Modifying fixtures

Each fixture is self-contained. To add a new test case:
1. Create `evals/fixtures/<new-name>/` with `spec.md`, `plan.md`, `code.md`, and `eval_metadata.json`.
2. Follow the existing `eval_metadata.json` format — `prompt`, `ground_truth`, `assertions`.
3. The grader will pick it up automatically.

To make an existing case harder, edit `eval_metadata.json` to tighten ground truth or add assertions; or edit the spec/plan/code to make the failure more ambiguous.
