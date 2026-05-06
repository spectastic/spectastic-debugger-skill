---
artifact: plan
feature: settings-persistence
feature_id: FEAT-004
spec_version: 1.0.0
---

# Settings Persistence Plan

## Technical Decisions

### TD-1: Storage backend
Use SQLite with SQLCipher for transparent encryption. SQLCipher is widely deployed, has Swift bindings, and handles encryption transparently.

**Rationale:** SQLCipher meets SNFR-001's "encrypted at rest" requirement and is the path of least resistance for a small key-value store.

### TD-2: Schema
Two tables: `preferences (key TEXT PRIMARY KEY, value BLOB)` and `credentials (service TEXT PRIMARY KEY, token BLOB)`.

### TD-3: Key derivation
Derive the SQLCipher passphrase from the OS keychain entry on first launch. Generate a random 32-byte key, store in keychain.

### TD-4: SQLCipher configuration
Use SQLCipher defaults. PRAGMA `cipher_compatibility = 4` for forward compatibility.
