---
artifact: plan
feature: capture-engine
feature_id: FEAT-002
spec_version: 1.2.0
phase: mvp
last_amended: 2026-04-22
---

# Capture Engine Implementation Plan

## Technical Decisions

### TD-1: Capture API (FREQ-001, NFR-002)
Use `SCStream` from ScreenCaptureKit. SCStream is the Apple-recommended path for screen capture from macOS 12.3+; CGDisplayStream is deprecated.

**Rationale:** Apple-native, FREQ-001 mandate, NFR-002 binds us to first-party frameworks.

### TD-2: Encoder (FREQ-002)
AVAssetWriter with H.264 in `.mov` container. Apple-native, FREQ-002 mandate.

### TD-3: Sharp Retina sourceRect (FREQ-003)
Per research R-001 (post bb7b95d):

- `SCStreamConfiguration.width` = `display.width × display.backingScaleFactor`
- `SCStreamConfiguration.height` = `display.height × display.backingScaleFactor`
- `SCStreamConfiguration.scaleFactor` = `display.backingScaleFactor`
- `SCStreamConfiguration.sourceRect` = full display rect at points
- `SCStreamConfiguration.pixelFormat` = `kCVPixelFormatType_32BGRA`
- `SCStreamConfiguration.colorSpaceName` = display's default

This config matches Apple's "Capturing screen content" sample code line-for-line.

### TD-4: NFR-001 fidelity guarantee — passthrough
SCStream delivers `CMSampleBuffer`s already composed by the WindowServer. We pass these straight to AVAssetWriter without intermediate transforms — no custom shaders, no color reinterpretation, no Metal re-composition. NFR-001 is satisfied by construction: we do not touch the pixels between WindowServer and the file.

## Sequencing

1. Configure `SCStream` + `SCStreamConfiguration` per TD-1, TD-3.
2. Wire SCStream output → AVAssetWriter input (passthrough per TD-4).
3. Implement start/stop control.
4. Validate against AC-1, AC-2, AC-3.

## Risks

- **R-1 (acknowledged):** WindowServer compositing is opaque to us. NFR-001 commits us to consuming whatever WindowServer hands us; if WindowServer's bitmap is wrong, our captured frame is wrong. NFR-002 forbids a parallel-render workaround. Risk accepted; no in-stack mitigation possible within the spec's constraints.
