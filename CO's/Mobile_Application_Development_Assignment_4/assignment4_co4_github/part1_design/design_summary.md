# Part I – Structured Design Summary

## Chosen platform for detailed design: Android
Layer order (top to bottom):
1. Applications – Activities, Services, Receivers, Providers; expose user workflows and app components; depend on framework APIs.
2. Application Framework – Activity/Window/Package/Notification/Location/Power managers; exposes stable Java/Kotlin APIs; depends on system services, Binder and native libraries.
3. Android Runtime (ART) + core libraries – loads DEX, verifies and executes code; uses interpretation/JIT/AOT profile-guided compilation and managed heap/GC; depends on Linux process/memory services and native runtime support.
4. Native libraries and system services – Bionic, media, graphics, SQLite, TLS, etc.; expose native APIs and service implementations; depend on HAL and kernel interfaces.
5. Hardware Abstraction Layer (HAL) – standardises vendor hardware modules such as camera, audio, sensors and radio; exposes HAL interfaces; depends on device drivers.
6. Linux kernel – process scheduler, virtual memory, networking, filesystems, power interfaces, IPC primitives, device drivers and security enforcement foundations; exposes system calls and device interfaces.
7. Hardware – CPU/GPU, RAM, flash, display, sensors, modem, battery.

Security location: Android application sandbox/UID separation, SELinux mandatory access control, permission checks in framework/system services and kernel-backed isolation; runtime permissions are granted by the user for applicable dangerous permissions. Package signing is checked during install/update.
Power location: kernel CPU idle/frequency and suspend mechanisms plus framework DeviceIdle/PowerManager/JobScheduler policies; apps should use bounded wakelocks and scheduled work.

## Task 2 problem model
Input: Android/iOS/Windows architecture properties and secure background messaging requirements.
Output: platform decision and delivery path.
Objective: reliable, secure message receipt without unacceptable battery use.
Constraints: OS background limits, notification permissions, network reachability, process termination, encryption, latency.
Decision: use push notification services as wake-up/delivery trigger; persist messages server-side and fetch after notification; do not depend on a permanently running process.

## Task 3 runtime launch model
Android package contains DEX plus native libraries/resources. Package manager installs and verifies; Zygote forks an app process; ART loads/verifies DEX and executes through interpreter/JIT/AOT compiled code depending on profile/compiler state. Framework creates Application and Activity; window is attached and first frame rendered.
iOS apps are delivered as signed native Mach-O binaries; dyld loads images and Objective-C runtime registers classes/selectors; ARC manages object lifetime. Windows app packaging/runtime depends on app model; WinRT is an API/runtime contract, not a universal bytecode VM. Native code is commonly loaded as PE images; managed .NET apps use CLR when applicable.
Cold start performs process creation, library/runtime initialisation and first Activity setup. Warm start may reuse a resident process and already initialised runtime; Activity recreation can still occur.

## Task 4 security repair
- Request only permissions needed at the point of use; explain purpose and handle denial.
- Store tokens in Android Keystore-backed encrypted storage; never world-readable files.
- Verify signed updates and restrict installation/update source.
- Enforce HTTPS/TLS with modern certificate validation; pin only with a rotation/recovery plan.
- Keep components non-exported unless external invocation is required; validate intents and inputs.
- Regression: user-approved contact access still works after runtime permission grant; denial remains a valid state.

## Task 5 power policy
ACTIVE: screen/interaction or urgent foreground task; CPU responsive, sensors at task-specific rate; exit after inactivity.
IDLE: screen off and no immediate work; CPU enters idle states, radios batch; scheduled jobs and push delivery permitted; exit on user interaction, alarm or push.
SUSPENDED/DOZE: device stationary/unplugged for a sustained period; suspend nonessential work, defer network and jobs to maintenance windows; exit on motion, charging, user interaction or permitted high-priority push.
Battery saver at 15% reduces sampling frequency, caps background work and defers nonurgent sync; urgent safety alerts remain allowed subject to OS policy.

## Task 6 RuralCare design
Use native Android and iOS apps for modern smartphones, plus a constrained J2ME/WML-compatible workflow for legacy phones. Legacy mode should capture the minimum necessary structured data and use server-side session controls; if device storage cannot provide adequate confidentiality, avoid storing identifiable records locally and use short-lived encrypted submissions when coverage exists.
Offline record fields: globally unique record UUID, patient pseudonymous ID, device ID (non-secret installation identifier), schema version, created timestamp, updated timestamp, worker ID, payload, encryption/key version, sync state, server acknowledgement/version, retry count and tombstone/delete marker.
Sync is idempotent: upload UUID + version; server enforces unique UUID and returns ACK; client marks synced only after durable ACK. Interrupted uploads retry same UUID. Conflicts are resolved by explicit version/field policy, not blind overwrite.
Lost device: revoke device credential, remote wipe where available, rotate keys; encrypted local database and short lock timeout reduce exposure.

## Part II – prototype scope
The included Python models exercise decision logic and produce repeatable synthetic traces. They are not substitutes for Android instrumentation. Use `evidence_templates/android_evidence_commands.md` to capture real outputs for process/lifecycle, ART, security and power tasks.
