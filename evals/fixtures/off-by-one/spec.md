---
artifact: spec
feature: recording-timer-ui
feature_id: FEAT-006
version: 1.0.0
phase: mvp
last_amended: 2026-02-05
---

# Recording Timer UI Specification

## Summary

While a recording is active, the UI displays a live elapsed-time counter so the user knows how long they've been recording.

## Functional Requirements

```yaml
- id: TREQ-001
  priority: P0
  phase: mvp
  status: active
  text: "While recording is active, the system shall display elapsed recording time formatted as HH:MM:SS."

- id: TREQ-002
  priority: P0
  phase: mvp
  status: active
  text: "The displayed time shall update at least once per second."

- id: TREQ-003
  priority: P0
  phase: mvp
  status: active
  text: "The displayed time shall be accurate to within 100ms of true elapsed time."
```

## Acceptance Criteria

- AC-1: Timer increments every second.
- AC-2: At any sample point, displayed time is within 100ms of (now - startTime).
- AC-3: Format follows HH:MM:SS, including leading zeros (e.g., "00:01:30" not "1:30").
