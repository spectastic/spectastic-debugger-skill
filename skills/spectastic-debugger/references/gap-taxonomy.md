# Gap Taxonomy

How to classify a defect to the right layer. The taxonomy is exclusive at the **primary** level — pick the highest-level gap that is genuinely the source. Secondary gaps can be listed if multiple layers need touching.

## Spec Gap

The user-visible behavior, NFR, scope, or contract is missing or wrong.

**Markers:**
- The behavior the user expected was never specified.
- The bug arises from an environmental constraint (platform, codec, locale, network, hardware) that wasn't captured as an NFR.
- A different LLM session, given only the current spec, would make the same wrong choice.
- The failure would survive a full regeneration of plan and code.

**Examples:**
- Output codec works on dev machine, fails on production target — missing portability NFR.
- Time handling breaks on DST — timezone behavior never specified.
- Error message UX undefined; implementer made one up that confuses users.

**Fix:** amend the spec. Add a requirement, NFR, or acceptance criterion. Cite the existing requirement IDs around it.

## Plan Gap

The spec is correct, but a technical decision in the plan violates a constraint, NFR, or shared invariant.

**Markers:**
- The spec already says the right thing.
- The plan picked a library, algorithm, configuration, or pattern that contradicts a spec NFR or constitutional principle.
- Code is faithfully implementing the plan; the plan itself is the leak.

**Examples:**
- Spec says "AES-256-GCM at rest"; plan picked SQLCipher with default AES-128-CBC.
- Spec says "responsive on mobile"; plan picked a CSS framework with poor mobile defaults.
- Spec says "must work offline"; plan picked an architecture with no offline mode.

**Fix:** amend the plan. Update the technical decision with a one-line justification linking back to the spec requirement it now honors.

## Implementation Gap

The spec and plan are both correct; the generated code drifted.

**Markers:**
- Off-by-one, typo, unhandled nil, missing guard, wrong variable name.
- Spec and plan would NOT reproduce the bug if regenerated.
- The fix is local and obvious once the bug is found.

**Examples:**
- Timer formatter has `Math.floor(seconds % 60) - 1`.
- Retry loop uses linear backoff when plan called for exponential.
- Function called with arguments in the wrong order.

**Fix:** code change + regression test. Do NOT escalate to spec or plan amendments — that's spec inflation.

## Cross-Spec Drift

Two specs disagree on a shared contract. The bug surfaces at the integration point.

**Markers:**
- Two features were specced separately and silently picked different formats, schemas, or vocabularies.
- The bug only appears when the two features interact.
- Neither spec is wrong in isolation; together they conflict.

**Examples:**
- UI spec lists codec options that capture spec doesn't support.
- Service A emits events with field name `userId`; Service B reads `user_id`.
- Recorder spec says "ProRes only"; UI spec offers MP4/H.264/H.265/ProRes dropdown.

**Fix:** lift the shared contract upstream — into a constitutional principle, a shared spec section, or a contract document — and update both specs to reference it. Do NOT patch one spec to match the other; that just shifts the leak.

## Constitutional Gap

A project-wide invariant is missing, or an existing principle is being violated.

**Markers:**
- The same class of bug could plausibly recur across multiple features.
- Multiple features have or could have the same gap.
- The fix should propagate to all current and future specs, not just this one.

**Examples:**
- Codec portability: every output-producing feature in the system has the same risk.
- Defensive hardware probing: every hardware-dependent feature has the same risk.
- Encryption baseline: every persistent-data feature has the same risk.

**Fix:** propose a constitutional amendment. The current feature's spec and plan are then re-validated against the new principle, and the principle propagates to all future specs.

## Disambiguation Rules

When two layers seem to apply, use these tiebreakers:

1. **Apply the regeneration test.** If the bug would NOT recur after a clean regen from current spec+plan, the gap is in implementation. Stop.
2. **Check the spec for the relevant constraint.** If absent, it's a spec gap. If present but the plan didn't honor it, it's a plan gap.
3. **Count affected features.** If the gap could recur across multiple features, escalate to constitutional.
4. **Check for shared contracts.** If the bug crosses a boundary between two specs, it's cross-spec drift, not a single-spec gap.

## Scope-Trap Detection

Sometimes a "bug" is actually a feature request for deferred functionality. Markers:

- Customer wants behavior that is explicitly tagged `phase: <future-phase>` or `status: deferred` in the spec.
- The fix would require promoting deferred requirements to active scope.
- The current spec, as written, is being honored correctly — the user just wants different requirements.

This is **not** a bug. Surface it via the Scope Check section as a scope question. Do NOT silently promote deferred items.

## Platform Defect (Upstream of Project)

A defect that reproduces *outside* the project's code — via the platform vendor's own first-party tools, an unmodified vendor sample-code consumer of the same API, or a sibling consumer API on the same platform. The bug is upstream of every API surface the project touches; no in-stack configuration knob can route around it.

This case does not introduce a sixth `primary_gap` enum value. It is a recognition pattern that routes to one of the existing layers — typically `constitution` (for the structural protocol) or `spec` (for the immediate cascade).

**Markers:**

- The regeneration test paradoxically *passes* — regenerating spec → plan → code from current artifacts would NOT reproduce the bug, because the bug is not in the project's code.
- The same defect is reproducible via the platform vendor's first-party tooling, the OS-level system shortcut for the operation, an unmodified vendor sample-code consumer, OR a sibling consumer API on the same platform.
- The project is bound (by spec NFR or constitutional principle) to the platform — a non-platform fallback is forbidden.

**Examples:**

- macOS WindowServer's compositor renders a system material with visual artifacts; the same artifacts appear via `screencapture(1)`, `Cmd-Shift-3`, and an unmodified Apple SCStream sample.
- An iOS audio framework drops a left channel on multichannel sources; the same drop reproduces in QuickTime, Safari, and a bare `AVAudioEngine` sample.
- A browser engine miscomputes a CSS subpixel offset; the same defect reproduces in a bare HTML page outside the app, in two other apps using the same engine.

**Disambiguation against Implementation Gap.** If the bug is observable with no project code in the loop, it is *not* an implementation gap regardless of the regen-test result. The regen test is necessary but not sufficient — also ask: "could this bug have originated outside any layer the project owns?" If yes, this section applies, not Implementation.

**Canonical disposition (paired tracks):**

1. **Spec-level cascade (immediate).** Document the limitation in release notes for the affected version. `Recommended Change → Layer: spec`, `Change type: release-notes entry`. Cite the affected feature and the user-trust expectation that is silently broken.
2. **External-tracker filing (this cycle).** File the platform vendor's bug tracker (Apple Feedback Assistant, Chromium Issues, etc.) before the version ships. `Change type: external-tracker filing`. Capture the tracker ID back into the release notes when filed.
3. **Structural fix (separate amendment cycle).** Propose a constitutional principle establishing the protocol for platform defects — file the tracker, document as known limitation, refuse to mask with synthetic output, refuse a non-platform fallback (already forbidden by the project's platform-binding). `Constitutional Check → Implies project-wide invariant: yes`. The principle exists because platform-binding makes platform-bug encounters inevitable; without a documented protocol the response is improvised per incident.

**Primary gap classification.** Genuine engineering disjunction between `constitution` (structural framing — propose the missing protocol) and `spec` (immediate-cascade framing — release-notes entry). Either is defensible; both are common. What is NOT defensible: classifying as `implementation` (the regen-pass-is-not-implementation trap), `plan` (the plan correctly chose the canonical platform path), or `cross-spec` (no shared contract is in dispute). Likewise: do NOT propose a code-level patch — if the platform vendor's own tooling reproduces the defect, no in-stack knob will mitigate it.
