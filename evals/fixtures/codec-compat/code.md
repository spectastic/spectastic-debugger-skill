# Implementation: CaptureEngine.swift (relevant excerpts)

```swift
import AVFoundation
import CoreGraphics

class CaptureEngine {
    private var assetWriter: AVAssetWriter?
    private var videoInput: AVAssetWriterInput?

    func startRecording(to url: URL) throws {
        let writer = try AVAssetWriter(outputURL: url, fileType: .mov)

        let videoSettings: [String: Any] = [
            AVVideoCodecKey: AVVideoCodecType.proRes422HQ,
            AVVideoWidthKey: 1920,
            AVVideoHeightKey: 1080,
        ]

        let input = AVAssetWriterInput(mediaType: .video, outputSettings: videoSettings)
        input.expectsMediaDataInRealTime = true
        writer.add(input)

        self.assetWriter = writer
        self.videoInput = input

        writer.startWriting()
        writer.startSession(atSourceTime: .zero)
        // ... CGDisplayStream wiring elided ...
    }

    func stopRecording(completion: @escaping (URL?) -> Void) {
        videoInput?.markAsFinished()
        assetWriter?.finishWriting { [weak self] in
            completion(self?.assetWriter?.outputURL)
        }
    }
}
```

# Test result on dev machine (M1 MacBook Pro, macOS 14.5):

```
✓ Recording starts
✓ Recording stops, file written
✓ File plays in QuickTime Player
✗ File fails to play in team's standard VLC corporate build
✗ File fails to play on Windows team members' machines (no ProRes decoder)
```
