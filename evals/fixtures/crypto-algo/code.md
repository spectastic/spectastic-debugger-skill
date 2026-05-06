# Implementation: SettingsStore.swift (relevant excerpts)

```swift
import SQLite3

class SettingsStore {
    private var db: OpaquePointer?

    func open(at path: String, key: String) throws {
        guard sqlite3_open(path, &db) == SQLITE_OK else { throw StoreError.openFailed }

        // Set encryption key (SQLCipher)
        sqlite3_key(db, key, Int32(key.utf8.count))

        // Use SQLCipher's default cipher (per plan TD-4)
        sqlite3_exec(db, "PRAGMA cipher_compatibility = 4;", nil, nil, nil)
    }
    // ... CRUD methods elided ...
}
```

# Audit finding (Compliance team, 2026-04-22):

```
FINDING: Storage encryption does not meet stated NFR.

Per inspection of the on-disk SQLCipher database header:
  - Cipher: AES-CBC (mode 0)
  - Key size: 256 bits  ✓
  - HMAC: SHA-256
  - cipher_compatibility = 4 corresponds to SQLCipher 4.x defaults: AES-256-CBC

NFR SNFR-001 and Constitution P1 require AES-256-GCM (an authenticated mode
on the FIPS-140-2 validated list). AES-CBC is neither GCM nor authenticated
encryption, and FIPS validation requires GCM mode for this use case.

REMEDIATION REQUIRED: Switch to AES-256-GCM. SQLCipher does not support GCM
in current releases; alternative storage mechanism may be required.
```
