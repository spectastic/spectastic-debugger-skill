---
artifact: spec
feature: recording-metadata
feature_id: FEAT-003
version: 1.0.0
phase: mvp
last_amended: 2026-01-30
---

# Recording Metadata Specification

## Summary

Each recording is annotated with metadata for organization, search, and replay.

## Functional Requirements

```yaml
- id: MREQ-001
  priority: P0
  phase: mvp
  status: active
  text: "When a recording finalizes, the system shall embed a timestamp in the filename and file metadata."

- id: MREQ-002
  priority: P0
  phase: mvp
  status: active
  text: "The system shall display recording start time and elapsed duration in the UI."

- id: MREQ-003
  priority: P1
  phase: v1.1
  status: deferred
  text: "The system shall support sorting recordings by start time in the gallery view."
```

## Acceptance Criteria

- AC-1: Recordings include a timestamp in their filename.
- AC-2: The UI shows start time and duration.
