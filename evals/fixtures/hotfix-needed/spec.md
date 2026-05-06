---
artifact: spec
feature: audio-capture
feature_id: FEAT-007
version: 1.0.0
phase: mvp
last_amended: 2026-02-12
---

# Audio Capture Specification

## Summary

Optional audio capture during screen recording. Audio is mixed into the output file.

## Functional Requirements

```yaml
- id: AREQ-001
  priority: P0
  phase: mvp
  status: active
  text: "When the user starts a recording and an audio input device is available, the system shall capture audio from the default device."

- id: AREQ-002
  priority: P0
  phase: mvp
  status: active
  text: "When no audio input device is available, the system shall record video-only and notify the user."

- id: AREQ-003
  priority: P0
  phase: mvp
  status: active
  text: "The system shall not crash, hang, or fail to start recording due to absence of an audio device."
```

## Acceptance Criteria

- AC-1: Recording succeeds with audio when a microphone is connected.
- AC-2: Recording succeeds video-only when no microphone is connected.
- AC-3: Application does not crash on machines without audio input.
