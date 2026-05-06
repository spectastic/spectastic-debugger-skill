# Deferred Items — Capture Engine (FEAT-002)

These requirements are part of FEAT-002's design intent but are explicitly out of scope for MVP. Promotion to active scope requires a scope decision per Constitution P2.

## Deferred Requirements

```yaml
- id: FREQ-004
  target_phase: v1.1
  status: deferred
  rationale: "Single-codec MVP reduces complexity in capture pipeline, file-size monitoring, and UI. H.264 brings broader playback compatibility but requires plan-level work on encoder selection abstraction."
  estimated_effort: "2 weeks"

- id: FREQ-005
  target_phase: v1.1
  status: deferred
  rationale: "H.265 follows H.264 once the encoder abstraction is in place."
  estimated_effort: "1 week (after FREQ-004)"

- id: FREQ-006
  target_phase: v2.0
  status: deferred
  rationale: "Per-recording codec selection requires UI work and recording-time API surface."
```

## Promotion Process

To promote a deferred requirement to active scope:
1. Update the requirement's `status` to `active` and `phase` to current phase in spec.md.
2. Re-run `/speckit.plan` to incorporate.
3. Validate against constitution (especially P2: scope discipline).
4. Inform stakeholders of the scope change.

This is not a unilateral decision by the SDD debugger or a single engineer.
