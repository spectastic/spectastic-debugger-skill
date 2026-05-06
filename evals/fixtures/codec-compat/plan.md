---
artifact: plan
feature: capture-engine
feature_id: FEAT-002
spec_version: 1.1.0
phase: mvp
---

# Capture Engine Implementation Plan

## Technical Decisions

### TD-1: Encoding pipeline (FREQ-003)
Use AVFoundation's `AVAssetWriter` with the `AVVideoCodecTypeAppleProRes422HQ` codec type. This is the platform-native ProRes 422 HQ encoder and produces the highest-quality .mov output.

**Rationale:** ProRes 422 HQ is mandated by FREQ-003 for MVP. AVFoundation's built-in encoder is the canonical macOS path; no external dependencies.

### TD-2: Container
.mov via `AVFileTypeQuickTimeMovie`. Required by FREQ-003.

### TD-3: Frame rate handling (NFR-001)
Capture at 60fps using `CGDisplayStreamCreate`. Pull frames into the writer with timestamp adjustment.

### TD-4: File size management (NFR-002)
ProRes 422 HQ averages ~176 Mbps at 1080p60, which exceeds NFR-002's 2GB/10min budget. Mitigation: cap recording length warning at 8 minutes and prompt user. Long-form constraint deferred to v1.1.

## Sequencing

1. Wire CGDisplayStream → CVPixelBuffer pipeline.
2. Configure AVAssetWriter with ProRes 422 HQ codec.
3. Implement start/stop control.
4. Add file-size warning at 8min mark.
5. Validate against AC-1, AC-2, AC-3.

## Risks

- ProRes 422 HQ files are large. Mitigated by 8min warning per TD-4.
- Frame drops under heavy CPU load. Mitigated by hardware encoder use.
