# Implementation: CaptureStream.swift (relevant excerpts)

```swift
import ScreenCaptureKit
import AVFoundation

final class CaptureStream: NSObject, SCStreamOutput {
    private var stream: SCStream?
    private var assetWriter: AVAssetWriter?
    private var videoInput: AVAssetWriterInput?

    func start(display: SCDisplay, output: URL) async throws {
        // TD-3: sharp Retina, canonical Apple pattern
        let config = SCStreamConfiguration()
        config.width  = Int(display.width)  * Int(display.backingScaleFactor)
        config.height = Int(display.height) * Int(display.backingScaleFactor)
        config.scaleFactor = CGFloat(display.backingScaleFactor)
        config.sourceRect = CGRect(x: 0, y: 0, width: display.width, height: display.height)
        config.pixelFormat = kCVPixelFormatType_32BGRA
        config.minimumFrameInterval = CMTime(value: 1, timescale: 60)

        let filter = SCContentFilter(display: display, excludingWindows: [])
        let stream = SCStream(filter: filter, configuration: config, delegate: nil)
        try stream.addStreamOutput(self, type: .screen, sampleHandlerQueue: .main)

        let writer = try AVAssetWriter(outputURL: output, fileType: .mov)
        let videoSettings: [String: Any] = [
            AVVideoCodecKey:  AVVideoCodecType.h264,
            AVVideoWidthKey:  config.width,
            AVVideoHeightKey: config.height,
        ]
        let input = AVAssetWriterInput(mediaType: .video, outputSettings: videoSettings)
        input.expectsMediaDataInRealTime = true
        writer.add(input)

        writer.startWriting()
        writer.startSession(atSourceTime: .zero)
        try await stream.startCapture()

        self.stream = stream
        self.assetWriter = writer
        self.videoInput = input
    }

    // TD-4: passthrough — no pixel transforms between WindowServer and encoder
    func stream(_ stream: SCStream,
                didOutputSampleBuffer sampleBuffer: CMSampleBuffer,
                of type: SCStreamOutputType) {
        guard type == .screen,
              let input = videoInput,
              input.isReadyForMoreMediaData else { return }
        input.append(sampleBuffer)
    }
}
```

# Test results on dev machine (M1 MacBook Pro, macOS Tahoe 26.x)

```
✓ Recording starts via SCStream.startCapture
✓ Recording stops, file written
✓ File plays in QuickTime Player
✓ Pixel-density spot-check matches `screencapture(1)` of same surface     (AC-2)
✓ No pixel-touching code path between SCStream and AVAssetWriter          (AC-3)

✗ Frames containing macOS Liquid Glass UI surfaces (Control Center,
  recent system menus, Sequoia+ system UI) show visual artifacts in the
  .mov: banding, blur smearing, color-tint shifts, transparency-blending
  oddities.

  Reproduction OUTSIDE our app, on the same UI surfaces:
  - Cmd-Shift-3 / Cmd-Shift-4 system shortcut → screenshot .png shows
    the SAME artifacts.
  - `screencapture -i out.png` from the terminal → SAME artifacts.
  - Apple's "Capturing screen content" sample code (bare, unmodified
    SCStream consumer) → SAME artifacts.

  AC-2 paradoxically PASSES — our captured frames match `screencapture(1)`'s
  bitmap exactly. Both contain the artifacts.
```
