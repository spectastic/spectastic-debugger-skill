---
artifact: plan
features: [FEAT-002, FEAT-005]
phase: mvp
---

# Combined Plan: Capture + UI

## Capture Engine (FEAT-002)

### TD-C1: Encoder
AVAssetWriter with `AVVideoCodecType.proRes422HQ`. (Per FREQ-003.)

## Recorder UI (FEAT-005)

### TD-U1: Codec dropdown (UREQ-002)
Render NSPopUpButton with three menu items: MP4 (H.264), MP4 (H.265), MOV (ProRes 422 HQ).

### TD-U2: Selection persistence (UREQ-003)
Store user's codec choice in SettingsStore under key `recording.codec`.

### TD-U3: Selection wiring (UREQ-004)
Pass selected codec to CaptureEngine on record start.

---

# Implementation: combined excerpts

## RecorderViewController.swift

```swift
@IBOutlet weak var codecPopup: NSPopUpButton!

override func viewDidLoad() {
    codecPopup.addItem(withTitle: "MP4 (H.264)")
    codecPopup.addItem(withTitle: "MP4 (H.265)")
    codecPopup.addItem(withTitle: "MOV (ProRes 422 HQ)")
    let saved = settings.string(forKey: "recording.codec") ?? "MOV (ProRes 422 HQ)"
    codecPopup.selectItem(withTitle: saved)
}

@IBAction func recordPressed(_ sender: Any) {
    let _ = codecPopup.titleOfSelectedItem  // ignored
    captureEngine.startRecording(to: outputURL)
}
```

## CaptureEngine.swift

```swift
func startRecording(to url: URL) throws {
    let writer = try AVAssetWriter(outputURL: url, fileType: .mov)
    let videoSettings: [String: Any] = [
        AVVideoCodecKey: AVVideoCodecType.proRes422HQ,  // hard-coded
        // ...
    ]
    // ... rest elided ...
}
```

# Bug report from QA

```
- Selected "MP4 (H.264)" from dropdown
- Pressed Record
- Output file is recording.mov, ProRes-encoded
- Same result for "MP4 (H.265)" selection
- Selection IS persisted across restarts (UREQ-003 satisfied)
- But the actual output ignores the selection (UREQ-004 violated)
```
