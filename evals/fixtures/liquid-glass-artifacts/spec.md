---
artifact: spec
feature: capture-engine
feature_id: FEAT-002
version: 1.2.0
phase: mvp
last_amended: 2026-04-22
---

# Capture Engine Specification

## Summary

The Capture Engine records primary-display screen content via Apple's ScreenCaptureKit and writes the captured frames to a `.mov` file via AVAssetWriter. It is the platform foundation for every recording-producing feature in the product.

## User Stories

- **US-001 [P0]** As a user, I can start and stop a screen recording from the UI and receive a playable video file.
- **US-002 [P0]** As a user, I can record at the native (Retina) pixel density of my display.
- **US-003 [P0]** As a user, the recorded file visually reflects what I saw on the screen during the take.

## Functional Requirements

```yaml
- id: FREQ-001
  priority: P0
  phase: mvp
  status: active
  text: "When the user invokes start-record, the system shall capture the primary display via ScreenCaptureKit (SCStream)."

- id: FREQ-002
  priority: P0
  phase: mvp
  status: active
  text: "Captured frames shall be encoded by AVAssetWriter into an .mov container."

- id: FREQ-003
  priority: P0
  phase: mvp
  status: active
  text: "The system shall capture at native Retina pixel density: SCStreamConfiguration's width/height/scaleFactor honor the display's backingScaleFactor."
  notes: "Sharp-Retina capture; per research R-001 (post bb7b95d) the SCStream config matches Apple's canonical pattern from the 'Capturing screen content' sample code."
```

## Non-Functional Requirements

```yaml
- id: NFR-001
  priority: P0
  phase: mvp
  status: active
  category: fidelity
  text: "Captured frames shall faithfully reflect the bitmap the WindowServer composites for the primary display. The capture pipeline must not transform, re-render, or post-process pixels between SCStream's CMSampleBuffer and the encoder."

- id: NFR-002
  priority: P0
  phase: mvp
  status: active
  category: platform-discipline
  text: "Screen capture MUST use Apple-native frameworks (ScreenCaptureKit + AVFoundation). Third-party capture libraries, custom Metal compositors, or CPU fallbacks for paths reachable by Apple frameworks are forbidden."
  notes: "We consume what the WindowServer hands us. We do not maintain a parallel render path."
```

## Out of Scope (MVP)

- Multi-display capture.
- Live preview of captured frames during recording.
- Re-rendering or compensating for platform-level rendering defects (see NFR-002).

## Acceptance Criteria

- AC-1: A recording can be started, stopped, and played back from the saved .mov.
- AC-2: Captured frames at native Retina resolution match the bitmap produced by `screencapture(1)` of the same surface (spot-comparison).
- AC-3: No pixel-touching code paths exist between SCStream's CMSampleBuffer and AVAssetWriter's input (verified by code inspection).
