---
artifact: plan
feature: recording-timer-ui
feature_id: FEAT-006
spec_version: 1.0.0
---

# Recording Timer UI Plan

## Technical Decisions

### TD-1: Update mechanism (TREQ-002)
Use a Timer scheduled at 1000ms intervals. On each tick, compute `now - startTime` and update the label.

### TD-2: Formatting (TREQ-001, AC-3)
Format elapsed seconds as HH:MM:SS using integer division and modulo:
- `hours = totalSeconds / 3600`
- `minutes = (totalSeconds % 3600) / 60`
- `seconds = totalSeconds % 60`
- Render with `String(format: "%02d:%02d:%02d", hours, minutes, seconds)`

### TD-3: Accuracy (TREQ-003)
The 1000ms tick interval combined with timestamp-based recompute (not increment-based counter) ensures drift is bounded by tick frequency, well within the 100ms tolerance.
