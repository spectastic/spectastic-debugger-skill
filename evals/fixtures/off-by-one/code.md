# Implementation: TimerLabel.swift (relevant excerpts)

```swift
import Foundation
import AppKit

class TimerLabel: NSTextField {
    private var startTime: Date?
    private var timer: Timer?

    func start() {
        startTime = Date()
        timer = Timer.scheduledTimer(withTimeInterval: 1.0, repeats: true) { [weak self] _ in
            self?.tick()
        }
    }

    private func tick() {
        guard let start = startTime else { return }
        let elapsed = Int(Date().timeIntervalSince(start))
        self.stringValue = format(elapsed)
    }

    private func format(_ totalSeconds: Int) -> String {
        let hours = totalSeconds / 3600
        let minutes = (totalSeconds % 3600) / 60
        let seconds = (totalSeconds % 60) - 1   // <-- BUG
        return String(format: "%02d:%02d:%02d", hours, minutes, seconds)
    }
}
```

# Bug report from QA

```
- Started recording, immediately observed timer
- Stopwatch on phone shows 60 seconds elapsed
- Timer label shows "00:00:59"
- At 2 minutes wall clock: label shows "00:01:59"
- Timer is consistently 1 second behind throughout the recording
- AC-2 (accuracy within 100ms) is violated
```
