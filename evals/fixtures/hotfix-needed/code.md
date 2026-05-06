# Implementation: AudioCapture.swift (relevant excerpts)

```swift
import AVFoundation

class AudioCapture {
    private var session: AVCaptureSession?

    func setup(for writer: AVAssetWriter) throws {
        let device = AVCaptureDevice.default(for: .audio)!  // <-- BUG: force-unwrap
        let input = try AVCaptureDeviceInput(device: device)

        let session = AVCaptureSession()
        session.addInput(input)
        // ... wire to writer ...
        self.session = session
    }
}
```

# Production incident report (2026-05-04 14:32 UTC)

```
SEVERITY: P1 (production down for affected users)

SYMPTOM: ScreenRecorder crashes on launch for users without an audio
input device. Estimated 12-18% of active users affected (mac mini units
without external audio, virtual machines, headless build agents).

STACK TRACE (from crash report):
  Fatal error: Unexpectedly found nil while unwrapping an Optional value
  at AudioCapture.swift:8
  AudioCapture.setup(for:) -> AVCaptureSession+AudioCapture.swift:8
  CaptureEngine.startRecording(to:) -> CaptureEngine.swift:42
  RecorderViewController.recordPressed(_:) -> RecorderViewController.swift:67

USER IMPACT: Cannot record at all. Force-quit on click of Record button.

ESCALATION: Sales/CS team is fielding inbound from 4 enterprise customers
within the last hour. Need fix shipped today.
```
