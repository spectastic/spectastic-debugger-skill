---
artifact: plan
feature: recording-metadata
feature_id: FEAT-003
spec_version: 1.0.0
---

# Recording Metadata Plan

## Technical Decisions

### TD-1: Timestamp source
Use `Date()` at recording start and stop. Store both as part of the recording record.

### TD-2: Filename format
`recording-YYYY-MM-DD-HHmmss.mov` using local-system formatter.

### TD-3: Duration calculation
`endTime - startTime` formatted as `HH:MM:SS`.
