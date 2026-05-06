---
artifact: spec
feature: capture-engine
feature_id: FEAT-002
version: 1.1.0
phase: mvp
last_amended: 2026-02-20
---

# Capture Engine Specification (excerpt)

## Functional Requirements

```yaml
- id: FREQ-003
  priority: P0
  phase: mvp
  status: active
  text: "The system shall encode capture output as ProRes 422 HQ in a .mov container."

- id: FREQ-004
  priority: P1
  phase: v1.1
  status: deferred
  text: "The system shall support encoding capture output as MP4 / H.264."
  deferred_rationale: "MP4/H.264 deferred to v1.1 to keep MVP single-codec. See deferred.md for full roadmap."

- id: FREQ-005
  priority: P1
  phase: v1.1
  status: deferred
  text: "The system shall support encoding capture output as MP4 / H.265."
```

## Out of Scope (MVP)

- Multi-codec support (deferred to v1.1; see deferred.md).
- Live streaming or network output.
