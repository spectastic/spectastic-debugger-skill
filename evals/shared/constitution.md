---
artifact: constitution
project: ScreenRecorder
version: 1.3.0
last_amended: 2026-02-14
---

# ScreenRecorder Constitution

Project-wide invariants. All specs, plans, and implementations must honor these. Amendments require team review and propagate to all features.

## Principles

- **P1 — Encryption baseline.** All persistent data containing user content or preferences MUST use FIPS-140-2 compliant encryption at rest. Minimum: AES-256-GCM. Algorithms not on the FIPS-validated list are forbidden regardless of library defaults.

- **P2 — Scope discipline.** Plans MUST only address requirements with `status: active` and `phase` matching the current release. Deferred or future-phase requirements are excluded from planning and implementation by default. Promotion requires explicit scope decision, not implicit drift.

- **P3 — Source-layer fix.** Code defects classified as spec or plan gaps MUST be fixed at the source layer, not patched in implementation. Code-only patches for upstream gaps are technical debt and require an upstream amendment to be queued in the same change.

- **P4 — Cross-spec contracts.** When two or more specs touch the same data shape, format, or vocabulary, the contract MUST be defined upstream — either in this constitution or in a shared spec section both reference. Inline duplication across specs is forbidden.

- **P5 — Tagging conventions.** All requirements use `[priority]` (P0/P1/P2) and `[phase-tag]` markers, plus per-requirement YAML frontmatter with `id`, `priority`, `phase`, and `status` fields. New requirements MUST follow this convention.

- **P6 — Regression tests for implementation gaps.** Every implementation-gap fix MUST land with a regression test that would have caught the bug. No exceptions.

## Versioning

This constitution is versioned. Amendments increment the minor version (1.3 → 1.4) for additions, major version (1.x → 2.0) for breaking changes to existing principles. The `last_amended` field reflects the most recent change.

## Notes for the SDD staff-debugger

When analyzing defects:
- A bug that violates an existing principle (P1–P6) is at minimum a plan or implementation gap, depending on which layer dropped the ball.
- A bug that exposes a class of risk not covered by P1–P6 is a candidate for a new principle (constitutional gap).
- The Constitutional Check section of the Triage Report should answer "does this imply a project-wide invariant" with a yes/no and propose the amendment text if yes.
