# Part A – Design Summary

See the Word document for the complete task-by-task answers. The design uses:
- Durable queue and state machine for sensor capture and upload.
- Explicit Intent for known internal components; implicit Intent only for resolvable external/system actions.
- WorkManager for deferrable constraint-based work; foreground service only for user-noticeable ongoing work allowed by platform policy.
- Encryption, consent, permission and authentication guards before any sensitive transfer.
- Incremental synchronisation with version checks, idempotency keys, conflict handling and bounded retry.
- Common schedule/check/execute/defer/undo abstraction for sensors, sync and notifications.
- Exact enumeration as a small-instance benchmark and adaptive heuristic for interactive UI/encoding decisions.
