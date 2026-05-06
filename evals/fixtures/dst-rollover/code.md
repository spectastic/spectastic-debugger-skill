# Implementation: Metadata.swift (relevant excerpts)

```swift
import Foundation

struct RecordingMetadata {
    let startTime: Date
    let endTime: Date

    var filename: String {
        let formatter = DateFormatter()
        formatter.dateFormat = "yyyy-MM-dd-HHmmss"
        // Uses default timeZone (local)
        return "recording-\(formatter.string(from: startTime)).mov"
    }

    var duration: TimeInterval {
        return endTime.timeIntervalSince(startTime)
    }
}
```

# Bug report from QA

```
- Recording started: 01:45 local time on Mar 9 2026 (just before US DST spring-forward)
- Recording stopped: 03:15 local time on Mar 9 2026 (after spring-forward)
- Wall clock elapsed: 30 minutes
- duration field reports: 30 minutes  ✓
- Filename includes "01-45-00"  ✓
- BUT: when filtering recordings in gallery for "started after 02:00 Mar 9",
  this recording appears with start time "03:45" — an hour later than reality.
- Subsequent recordings made between 02:00 and 03:00 local time on Mar 9
  conflict on filename (DST gap means the time slot didn't exist locally).
```
