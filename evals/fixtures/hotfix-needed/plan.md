---
artifact: plan
feature: audio-capture
feature_id: FEAT-007
spec_version: 1.0.0
---

# Audio Capture Plan

## Technical Decisions

### TD-1: Device probing (AREQ-001, AREQ-002, AREQ-003)
On recording start, query AVCaptureDevice for the default audio device. If `nil` is returned, log the absence and proceed with video-only recording. The presence/absence of an audio device must never block or crash recording.

### TD-2: User notification (AREQ-002)
When falling back to video-only, post a non-blocking notification banner: "Recording without audio (no microphone detected)."

### TD-3: Audio writer wiring (AREQ-001)
When an audio device IS available, add an AVAssetWriterInput for audio and pull samples through the writer.

## Sequencing

1. Probe for audio device.
2. Branch: device present → wire audio writer; absent → log + notify, skip audio writer.
3. Start recording.
