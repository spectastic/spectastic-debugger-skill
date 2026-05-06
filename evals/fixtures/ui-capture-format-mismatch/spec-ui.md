---
artifact: spec
feature: recorder-ui
feature_id: FEAT-005
version: 1.0.0
phase: mvp
last_amended: 2026-02-18
---

# Recorder UI Specification

## Summary

The Recorder UI is the user-facing surface for starting, stopping, and configuring recordings.

## Functional Requirements

```yaml
- id: UREQ-001
  priority: P0
  phase: mvp
  status: active
  text: "The system shall present a Record button that toggles recording on and off."

- id: UREQ-002
  priority: P0
  phase: mvp
  status: active
  text: "The system shall present a codec selection dropdown with options: MP4 (H.264), MP4 (H.265), MOV (ProRes 422 HQ)."

- id: UREQ-003
  priority: P0
  phase: mvp
  status: active
  text: "When the user changes the codec selection, the system shall persist the choice as the default for subsequent recordings."

- id: UREQ-004
  priority: P0
  phase: mvp
  status: active
  text: "When the user clicks Record, the system shall begin capture using the currently-selected codec."
```

## Acceptance Criteria

- AC-1: Codec dropdown shows three options.
- AC-2: Selection persists across launches.
- AC-3: Recording uses the selected codec.
