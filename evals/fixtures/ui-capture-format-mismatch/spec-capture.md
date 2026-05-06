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
  notes: "MVP single-codec. Multi-codec parity deferred to v1.1 (see FREQ-004..FREQ-006)."

- id: FREQ-004
  priority: P1
  phase: v1.1
  status: deferred
  text: "The system shall support encoding capture output as MP4 / H.264."

- id: FREQ-005
  priority: P1
  phase: v1.1
  status: deferred
  text: "The system shall support encoding capture output as MP4 / H.265."

- id: FREQ-006
  priority: P2
  phase: v2.0
  status: deferred
  text: "The system shall support codec selection at recording start time."
```
