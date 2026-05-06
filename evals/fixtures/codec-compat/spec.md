---
artifact: spec
feature: capture-engine
feature_id: FEAT-002
version: 1.1.0
phase: mvp
last_amended: 2026-02-20
---

# Capture Engine Specification

## Summary

The Capture Engine records screen content and produces a video file the user can play back, share, or upload.

## User Stories

- **US-001 [P0]** As a user, I can start and stop a screen recording from the UI and receive a playable video file.
- **US-002 [P0]** As a user, I can record at the native resolution of my display.

## Functional Requirements

```yaml
- id: FREQ-001
  priority: P0
  phase: mvp
  status: active
  text: "When the user invokes start-record, the system shall begin capturing the primary display."

- id: FREQ-002
  priority: P0
  phase: mvp
  status: active
  text: "When the user invokes stop-record, the system shall finalize a video file at the configured output path within 5 seconds."

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

## Non-Functional Requirements

```yaml
- id: NFR-001
  priority: P0
  phase: mvp
  status: active
  category: performance
  text: "Recording shall not drop more than 1% of frames at 60fps on supported hardware."

- id: NFR-002
  priority: P0
  phase: mvp
  status: active
  category: storage
  text: "Output files shall be no larger than 2GB per 10 minutes of 1080p capture."
```

## Out of Scope (MVP)

- Multi-codec selection (deferred to v1.1).
- Live streaming or network output.
- Audio mixing across multiple sources.

## Acceptance Criteria

- AC-1: A user can start, stop, and play back a recording on the dev machine.
- AC-2: The output file is a valid ProRes 422 HQ .mov.
- AC-3: Recording at 60fps on supported hardware drops fewer than 1% of frames.
