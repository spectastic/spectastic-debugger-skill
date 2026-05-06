---
artifact: spec
feature: settings-persistence
feature_id: FEAT-004
version: 1.0.0
phase: mvp
last_amended: 2026-01-15
---

# Settings Persistence Specification

## Summary

User preferences (recording defaults, hotkeys, output paths, account credentials for cloud upload) persist between sessions in a local encrypted store.

## Functional Requirements

```yaml
- id: SREQ-001
  priority: P0
  phase: mvp
  status: active
  text: "When the user changes a preference, the system shall persist it within 1 second."

- id: SREQ-002
  priority: P0
  phase: mvp
  status: active
  text: "On application launch, the system shall restore all persisted preferences."
```

## Non-Functional Requirements

```yaml
- id: SNFR-001
  priority: P0
  phase: mvp
  status: active
  category: security
  text: "All persisted user data, including credentials, shall be encrypted at rest using AES-256-GCM. (See Constitution P1.)"

- id: SNFR-002
  priority: P0
  phase: mvp
  status: active
  category: performance
  text: "Settings load on launch shall complete within 200ms."
```

## Acceptance Criteria

- AC-1: Changes to preferences are persisted and survive restart.
- AC-2: Audit confirms storage uses AES-256-GCM.
- AC-3: Settings load completes within 200ms on supported hardware.
