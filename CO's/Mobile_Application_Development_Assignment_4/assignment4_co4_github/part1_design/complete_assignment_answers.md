
# MOBILE APPLICATION DEVELOPMENT ENVIRONMENT
## ASSIGNMENT 4 – CO4 (PART I + PART II)
**Individual Assignment | Total: 100 marks across Part I and Part II**

**Student Name:** ____________________  
**Register Number:** ____________________  
**Department / Institution:** SIMATS Engineering  
**Submission Date:** ____________________

# PART I – ARCHITECTURAL ANALYSIS AND DESIGN THROUGH STRUCTURED REASONING

## Task 1 – Architecture Review (6 Marks)

### 1.1 Diagnose the junior engineer's description

| No. | Technical deficiency | Why the description is insufficient |
|---|---|---|
| 1 | Drivers and HAL are omitted | Hardware access paths and vendor-specific interfaces cannot be identified. |
| 2 | Native libraries and system services are omitted | Graphics, media, database, networking and cryptographic services have no defined location. |
| 3 | Kernel responsibility is vague | A kernel does not simply “run applications”; it schedules processes, manages virtual memory, networking, drivers, IPC and low-level security. |
| 4 | Runtime is undefined | The note does not distinguish DEX loading, interpretation, JIT/AOT compilation or native binary loading. |
| 5 | Permission enforcement is vague | It does not identify the grant decision, permission scope, enforcement point or denial behaviour. |
| 6 | Power saving has no trigger or mechanism | No idle state, CPU frequency policy, suspend, Doze, wakelock or scheduled-work mechanism is specified. |
| 7 | App/OS boundary is missing | The path through framework APIs, Binder/system services, native interfaces and system calls is unclear. |

### 1.2 Repaired Android layered architecture

| Layer (top → bottom) | Responsibility | Exposes upward | Depends on below |
|---|---|---|---|
| Applications | Activities, services, receivers, providers and app UI/business logic | App components and user-facing features | Android framework APIs |
| Application framework | Activity/Window/Package/Notification/Location/Power managers and system services | Java/Kotlin APIs and lifecycle contracts | Binder IPC, ART, native libraries and system services |
| Android Runtime (ART) + core libraries | Loads/verifies DEX; interprets and compiles code; manages managed heap and garbage collection | Runtime execution, core language APIs, JNI | Linux process/memory services and native runtime support |
| Native libraries and system services | Bionic, SQLite, TLS, media, graphics and other native services | Native APIs and service endpoints | HAL and kernel interfaces |
| Hardware Abstraction Layer (HAL) | Standardises camera, audio, sensor, radio and other vendor modules | Stable hardware service interfaces | Device drivers |
| Linux kernel | Scheduling, virtual memory, networking, filesystems, device drivers, IPC primitives and security foundations | System calls, device and kernel interfaces | Physical hardware |
| Hardware | CPU/GPU, RAM, flash, display, sensors, modem and battery | Physical compute, storage, radio and sensor capability | — |

**Explicit locations:** Kernel = Linux kernel layer. Runtime = ART. Security enforcement = app UID sandbox and SELinux at OS/kernel boundary, permission checks in framework/system services, package signature verification during install/update. Power management = kernel CPU idle/frequency/suspend controls plus framework PowerManager, DeviceIdle/Doze and JobScheduler policies.

### 1.3 Design defence (under 100 words)

This is an architectural specification because it names every layer, assigns each a bounded responsibility, identifies its upward interface and downward dependency, and locates runtime, security and power-management functions. Another engineer can trace an application request through framework APIs, system services, native interfaces and kernel services. It also identifies enforcement points and observable behaviours instead of relying on vague statements such as “the OS keeps apps secure” or “the OS saves battery.”

## Task 2 – Android vs iOS vs Windows (8 Marks)

### 2.1 Requirement model

| Element | Definition |
|---|---|
| Input | Platform architecture, background execution rules, runtime, security and IPC characteristics |
| Output | Comparison and justified platform strategy for secure background messaging |
| Objective | Deliver messages reliably with acceptable latency, privacy and energy use |
| Constraints | OS background limits, push permissions, process termination, network availability, encryption and battery |
| Decision | Use server-side durable message queues and OS push services; fetch encrypted content when the app is allowed to execute |
| Required information | Kernel family, app process model, runtime, framework, sandbox, permission enforcement, IPC and push mechanism |

### 2.2 Hypothesis

The platform's background execution and process-lifecycle policy will affect message delivery most, because an application process may be suspended or terminated while the OS still permits a system push service to wake or notify the user.

### 2.3 Comparison matrix

| Aspect | Android | iOS | Windows | Messaging consequence |
|---|---|---|---|---|
| Kernel | Linux kernel with Android-specific changes | XNU hybrid kernel (Mach/BSD components) | Windows NT hybrid kernel | Different scheduling, driver and security foundations |
| Kernel interface | Linux system calls, Binder driver and device interfaces | Mach traps, BSD system calls and IOKit interfaces | NT system calls and Windows executive APIs | App code normally uses framework APIs rather than direct kernel calls |
| Runtime | ART executes DEX; interpreter/JIT/AOT depending on profile and build | Native Mach-O plus Objective-C runtime; ARC manages object lifetime | WinRT is an API/runtime contract; native PE and .NET CLR paths depend on app type | Runtime and packaging affect startup, memory and portability |
| Framework | Android SDK/framework services | Cocoa Touch/UIKit and system frameworks | WinUI/UWP/Windows App SDK depending on app model | Background APIs and notification integration differ |
| Isolation | Per-app Linux UID, sandbox, SELinux and permission checks | Per-app sandbox, code signing, entitlements and privacy permissions | AppContainer/capability model for packaged apps; desktop apps have different boundaries | Least privilege must be designed per platform |
| IPC | Binder, intents, services, content providers | XPC, Mach ports, URL schemes and framework APIs | COM/RPC, app services and Windows messaging APIs | IPC endpoints must authenticate and validate data |
| Background messaging | FCM/system services, notification and background execution limits | APNs push notifications; limited background execution | WNS push and background task policies | Push is a wake/notification trigger, not a promise of unlimited app runtime |

### 2.4 Incoming message desk-check (Android vs iOS)

**Android path:** Network packet reaches modem/Wi-Fi hardware → kernel network driver and IP stack → Google Play services/FCM or vendor push service receives push → notification/system service applies permission and channel policy → app may receive a permitted callback or notification tap launches process → ART executes callback → app fetches encrypted message from server and stores it.

**iOS path:** Network event reaches baseband/Wi-Fi and XNU networking → APNs system service receives push → SpringBoard/user notification system applies notification settings → system may display notification while app is suspended → user tap or permitted background notification launches/wakes app → dyld/runtime and app lifecycle execute callback → app fetches encrypted message.

### 2.5 Challenge: app process terminated under memory pressure

| Platform | Prediction | Responsible element | Relevant trace |
|---|---|---|---|
| Android | Process may be killed; push service remains outside the app process. A later notification/tap can recreate the process. | ActivityManager/LMK and FCM/system push service | Push received by system → app process absent → notification displayed → user tap causes Zygote fork/app launch → callback |
| iOS | App process may be jetsam-terminated; APNs can still deliver a user notification. Silent background execution is not guaranteed. | iOS process lifecycle/jetsam and APNs | APNs notification → OS displays alert → app process remains absent until permitted launch/tap |

The prediction is that visible notification delivery can remain possible, but immediate app-code execution is not guaranteed. Therefore the server must retain messages until the client confirms retrieval.

## Task 3 – Runtime Environment Analysis (9 Marks)

### 3.1 Execution models

| Platform | Delivered code | Loader | When executable instructions are produced |
|---|---|---|---|
| Android / ART (historically Dalvik) | DEX bytecode plus native libraries/resources | Package manager, Zygote-created app process and ART class/runtime loader | Interpreter/JIT at runtime and profile-guided AOT compilation; exact mix depends on Android version and compilation state |
| iOS / Objective-C runtime | Signed native Mach-O binary and frameworks | launchd starts process; dyld loads images; Objective-C runtime registers classes/selectors | Native machine code is produced before delivery; loader performs relocation/binding at launch |
| Windows | Native PE binary or managed assembly depending on app technology | Windows loader; CLR for managed .NET applications | Native PE is already machine code; managed code is JIT/AOT according to runtime and deployment mode |

### 3.2 Android launch sequence

1. User taps icon; Launcher resolves the package and launch Activity.
2. ActivityTaskManager requests process start; if no process exists, Zygote forks an app process.
3. Linux kernel allocates process resources, maps memory and schedules the process.
4. ART initialises runtime state, loads DEX and verifies classes/methods.
5. Application class is instantiated; `Application.onCreate` runs.
6. Activity is instantiated and lifecycle callbacks execute (`onCreate`, `onStart`, `onResume`).
7. WindowManager/SurfaceFlinger coordinate the window and display buffers.
8. App performs first layout/draw; first frame appears.

Each step depends on the previous layer: framework callbacks cannot execute before a process and runtime exist; rendering cannot complete before a window/surface and graphics services are available.

### 3.3 Runtime strategy comparison

| Topic | Android ART | iOS Objective-C runtime | Windows runtime paths |
|---|---|---|---|
| Execution | DEX interpretation, JIT and profile-guided AOT | Native compiled code; Objective-C runtime provides dynamic dispatch/metadata | Native PE or CLR-managed code, depending on app |
| Compilation | Install/runtime profile-guided compilation | Ahead-of-time native compilation | Native AOT or CLR JIT depending on framework |
| Memory | Managed heap with tracing GC | ARC reference counting; autorelease pools | Native/manual, COM reference counting or .NET GC depending on technology |
| Native access | JNI and Android NDK | Objective-C/Swift runtime and C APIs | Win32/WinRT APIs, P/Invoke/interop |
| Responsiveness | GC may pause briefly; JIT warms hot paths | ARC releases objects deterministically but retain cycles can leak | Depends on native/managed runtime and GC/interop |
| Startup/storage | DEX and runtime init; AOT profiles trade storage for speed | Native code, dyld loading and framework initialisation | Varies by app model and runtime |
| Portability | DEX runs across compatible Android runtimes | Native binary is built for target Apple architecture/OS | Depends on target framework/runtime and architecture |

**Low-memory conclusion:** No runtime is universally best. For a tightly constrained device, a small native implementation with bounded allocations may minimise runtime overhead. Among the named choices, native compiled code with ARC can avoid a tracing GC heap, but ARC metadata/retain cycles and framework memory still matter. Actual selection must be based on measured peak RSS/PSS, allocation rate and pause behaviour on the target device.

### 3.4 Cold vs warm launch

| Step | Cold start | Warm start |
|---|---|---|
| Process creation | Required if no process exists | Often skipped if process remains resident |
| Runtime initialisation | Required | Usually reused |
| DEX/class loading | Required for classes not yet loaded | Many classes already loaded |
| Application/Activity callbacks | Required for new Activity instance | Activity may resume or be recreated |
| Window/frame rendering | Required | Required for a newly visible frame |

### 3.5 Dependency analysis

Kernel process and memory services must exist before the app process can execute. ART or the platform loader must initialise before application code can run. Framework services must be ready before lifecycle callbacks can request windows, notifications or sensors. This ordering prevents application code from invoking unavailable lower-level resources.

## Task 4 – Security Forensics (7 Marks)

### 4.1 Defect-to-mechanism mapping

| Original decision | Bypassed/unused mechanism | Risk | Repair |
|---|---|---|---|
| Request every permission at install | Least privilege and runtime permission model | Users may deny; excessive access increases attack surface | Request only when feature is used; explain purpose and handle denial |
| Store login token in shared readable file | App sandbox and secure storage | Other apps or a compromised device may read token | Encrypt token using Keystore-backed key; private app storage |
| Accept updates from any source | Code signing/package verification | Malicious or tampered package may replace app | Verify trusted signing identity and secure update channel |
| Use plain HTTP | TLS transport protection | Network attacker can read/modify credentials and data | HTTPS with certificate/hostname validation; protect secrets |

### 4.2 Attack scenario

A user connects to a hostile public Wi-Fi network. The attacker performs a man-in-the-middle attack against the plaintext server connection and captures the login token (confidentiality first lost when the token traverses the unencrypted network). The attacker then uses the token to access the account. Separately, a malicious application reads a shared token file if the file permissions expose it. Integrity is lost when the attacker submits modified notes or account actions.

### 4.3 Minimal repairs on Android

- Request camera/location only when the user starts the related feature; check runtime permission result before access.
- Store token in app-private storage encrypted with an Android Keystore-protected AES key; require appropriate user-authentication policy for high-risk data.
- Accept only signed app updates from the trusted distribution channel; Android package signature continuity is required for updates.
- Enforce HTTPS using platform network security configuration and standard certificate validation.
- Keep internal activities/services non-exported; validate any exported intent entry point.

### 4.4 Regression check

A user taps “Attach photo,” receives a clear camera permission explanation, grants permission, and the camera feature works. If permission is denied, SecureNotes provides a manual attachment alternative and does not crash. This preserves legitimate, consented behaviour while removing blanket permission requests.

## Task 5 – Power Management Reasoning (7 Marks)

### 5.1 State-transition policy

| State | Hardware/kernel behaviour | Entry condition | Exit condition | Permitted work |
|---|---|---|---|---|
| ACTIVE | CPU responsive; display/sensors active as needed; normal scheduling | User interaction, foreground tracking or urgent task | Screen off and no urgent foreground work | Foreground UI, bounded sensor sampling, short jobs |
| IDLE | Display off; CPU enters idle states; radios and jobs may be batched | Screen off and user inactive | User interaction, permitted push, alarm or scheduled window | Push service, short scheduled jobs, batched uploads |
| SUSPENDED/DOZE | Deep idle/suspend; nonessential network and wakelocks restricted | Device stationary, unplugged and idle for platform-defined period | Motion, charging, user interaction or permitted high-priority event | Minimal OS-managed work; app work deferred |

Transitions: ACTIVE → IDLE after inactivity; IDLE → SUSPENDED after sustained stationary idle; SUSPENDED → IDLE on motion/maintenance/push; IDLE → ACTIVE on user interaction.

### 5.2 Urgent push while suspended

A permanent CPU-awake policy is insufficient because it wastes energy and may still conflict with OS background restrictions. Use OS push delivery as the event trigger, keep the device mostly asleep, and perform a short bounded operation after an allowed wake. Use a partial wakelock only for the minimum critical processing window, release it in all success/failure paths, and defer nonurgent work to WorkManager/JobScheduler. The app must stop polling continuously and must not hold a permanent wakelock.

### 5.3 Battery saver at 15%

- Kernel/hardware: lower CPU frequency/performance budget where supported; reduce background wakeups.
- Runtime/framework: defer background jobs, restrict sync cadence and apply platform low-power policies.
- Application: reduce nonessential sensor sampling, batch writes and uploads, pause animations and defer nonurgent refresh.
- Trade-off: location updates may be less frequent, but the ten-hour shift and emergency-critical push path are better protected.

## Task 6 – RuralCare Field-Data Collection Design (13 Marks)

### Stage 1 – Problem model

Input: three device classes, patient data, offline periods, ten-hour battery target and device-loss threat. Output: platform strategy and secure offline-first workflow. Objective: complete field records without loss/duplication while protecting confidentiality and battery. Constraints: J2ME/WML capability, varying storage/security, long offline windows, intermittent connectivity and mixed power controls. Decisions: native smartphone apps plus constrained legacy workflow; local encryption; idempotent synchronisation; device revocation.

### Stage 2 – Platform strategy

Use native Android and iOS applications for Class A/B to access platform security, encrypted storage, background scheduling and current APIs. For Class C, provide a minimal J2ME application where supported or a WML browser workflow. Because legacy devices may lack trustworthy hardware-backed key storage, avoid persistent identifiable patient records on them; use minimum necessary data, short-lived sessions and transmit when connected. If offline retention is mandatory on a legacy device without adequate protection, that device must not store identifiable records and should use a paper/secure offline alternative approved by the organisation.

### Stage 3 – Device constraint table

| Class | Runtime | Security | Power controls | Offline storage | Connectivity |
|---|---|---|---|---|---|
| A Android | ART + Android framework | UID sandbox, runtime permissions, Keystore, file-based encryption | Doze, WorkManager, foreground service, wakelocks | Encrypted Room/SQLite database | Wi-Fi/cellular; intermittent |
| B iPhone | Native Mach-O, Objective-C/Swift runtime | App sandbox, Keychain, Data Protection, entitlements | BackgroundTasks, push, OS-managed suspension | Protected local database/files | Wi-Fi/cellular; intermittent |
| C feature phone | J2ME/JME or WML browser | Device-dependent; often limited secure storage | Basic timer/sleep controls; limited background APIs | Small record queue only if protected; otherwise no identifiable offline storage | Low-bandwidth cellular/SMS/WAP where available |

**Fields retained for safe sync:** UUID (deduplication), patient pseudonymous identifier, schema version, record payload, creation/update timestamps, worker ID, device installation identifier, encryption/key version, sync state, server acknowledgement/version, retry count and tombstone. These fields support idempotency, conflict handling, audit and recovery.

### Stage 4 – Complete solution specification

**Architecture (modern smartphone):** UI layer on main thread → domain/use-case layer on bounded executor → repository/data layer → encrypted local database and sync queue → OS services (Keystore, network, WorkManager/BackgroundTasks, notification). Network requests use authenticated TLS. Keys are not stored alongside ciphertext.

**Capture procedure:**
1. Authenticate worker and verify role.
2. Validate patient identifier and required fields.
3. Generate unique UUID and timestamp.
4. Encrypt record before durable local queueing.
5. Commit record and sync metadata atomically.
6. Display “Saved offline” until server ACK is received.

**Synchronisation procedure:**
1. Confirm connectivity and policy constraints.
2. Select pending records in creation order.
3. Send batch with UUID, version and authenticated worker/device identity over TLS.
4. Server validates identity, schema and access; enforces unique UUID.
5. Server commits record and returns durable ACK plus canonical version.
6. Client marks only acknowledged records as synced.
7. On interruption, retain pending status and retry the same UUID with exponential backoff.
8. Resolve concurrent edits by explicit version/conflict workflow; never silently overwrite.

**Security:** encrypted database and protected keys on Android/iOS; TLS in transit; short lock timeout; minimum local data; device credential revocation and remote wipe where available. Class C stores no identifiable records if its storage cannot be protected.

**Power:** sample only when needed; batch sensor reads; batch network uploads; avoid continuous wakelocks; schedule sync on connectivity/charging; preserve emergency alert path.

**Failure handling:** no network → encrypted queue; permission denied → explain and disable only dependent feature; storage full → stop new sensitive capture and alert; process death → recover from committed queue; key unavailable → do not fall back to plaintext; duplicate upload → server UUID deduplication; lost device → revoke credentials and remote wipe where supported.

### Stage 5 – Desk-check: Class A offline six hours, battery 20%, then device lost

| Step | State/action | Exposure/loss/recovery |
|---|---|---|
| 1 | Records captured and encrypted locally with UUIDs | Plaintext is not written to shared storage |
| 2 | No network for six hours; records remain `PENDING` | Data is retained in encrypted queue |
| 3 | Battery reaches 20%; sampling interval is reduced and sync is deferred unless urgent | Some noncritical location granularity is reduced; committed records remain |
| 4 | Device is lost before sync | Server does not yet have those unsynced records |
| 5 | Administrator revokes device credential and requests remote wipe | Future authenticated sync from lost device is blocked; remote wipe depends on device being reachable |
| 6 | Recovery assessment | Data may remain recoverable only if encrypted backup/managed recovery exists; otherwise unsynced records may be lost. Encryption limits exposure but cannot guarantee recovery |

### Stage 6 – Adversarial tests

| Adverse condition | Prediction | Result against design | Required refinement |
|---|---|---|---|
| Stolen unlocked phone | Local data risk increases | Encryption at rest helps, but an unlocked authorised session may expose app data | Short inactivity lock, re-authentication for sensitive export, rapid credential revocation |
| Sync interrupted after server commit but before ACK | Client retries same UUID | Server unique constraint prevents duplicate record | Keep idempotency key and durable ACK |
| Class C lacks secure storage | Local identifiable data cannot be protected adequately | Design intentionally prohibits identifiable offline persistence on that device | Use minimum non-identifying data, secure alternative or exclude device from offline mode |
| Device clock incorrect | Timestamp ordering may be unreliable | UUID and server receipt time prevent duplicate identity; conflict logic must not trust device time alone | Store client timestamp plus server timestamp and monotonic sequence |

**Conclusion:** The design meets offline reliability and security only when platform capability is respected. The legacy device constraint is a hard boundary: where secure storage is absent, do not persist identifiable data locally.

# PART II – MOBILE SYSTEMS ENGINEERING: ANALYSE, INSTRUMENT, TEST, DEBUG & OPTIMISE

**Important:** The following Python prototype outputs in the repository are synthetic logic-model demonstrations. They are not Android device measurements. Replace them with real adb, profiler, ART, network-capture and Battery Historian evidence before final submission.

## Task 1 – OS model validation (8 Marks)

### 1.1 Architecture and process model

| Area | Android | iOS |
|---|---|---|
| Layers | Linux kernel → HAL → native libraries/ART → framework → apps | Core OS → Core Services → Media → Cocoa Touch |
| Process creation | Zygote fork initiated by ActivityManager/launch services | launchd creates/starts app process |
| IPC | Binder driver and framework Binder interfaces | Mach ports and XPC |
| Lifecycle | Activity/Service/Receiver lifecycle; process importance managed by ActivityManager | UIApplication/scene and UIViewController lifecycle; process may be suspended/jetsam-terminated |

### 1.2 Instrumentation interpretation

Capture `ps -A`, `dumpsys activity processes`, `dumpsys meminfo <package>` and lifecycle logs. PID identifies process; UID identifies app security principal; PSS estimates proportional physical memory; oom adjustment/importance indicates relative kill priority. A foreground visible app is normally more protected than cached background work, but no process is guaranteed permanent survival.

### 1.3 Three conditions and predictions

| Condition | Prediction | Last callback expected | Return behaviour |
|---|---|---|---|
| Foreground | Process remains active | Normal callback sequence | State in memory |
| Background five minutes | May remain cached or be reclaimed | `onStop`/last lifecycle callback depends on navigation | Restore from saved state/database |
| Low-memory pressure | Process may be killed | No guaranteed final callback | Recreate process and restore persisted state |

Actual result depends on Android version, device memory and app implementation. Record mismatches instead of changing the prediction after the fact.

### 1.4 Boundary test

Rotate the device while a form contains unsaved data and a background upload is active. This stresses Activity recreation, state persistence and task ownership. Expected safe behaviour: UI state is restored from saved state/repository and upload is owned by a lifecycle-independent worker rather than the Activity.

## Task 2 – Architecture assumptions vs measured reality (9 Marks)

### 2.1 Normal case

Use identical input data and compare a single-thread main-thread computation with chunked background execution. Keep UI rendering on the main thread; use a bounded executor/coroutine dispatcher for computation. Measure duration, CPU time, thread count, context switches, heap/PSS and frame timing.

### 2.2 Counterexample

A tiny task or lock-contended shared counter can be slower with multiple threads because thread scheduling, synchronisation and contention exceed useful parallel work. The included `threading_model.py` provides an illustrative counterexample; it is not a profiler measurement.

### 2.3 Engineering comparison

| Metric | Single-thread | Multi-thread | Interpretation |
|---|---|---|---|
| CPU work | One worker | Multiple workers | Parallelism only helps independent work |
| Memory | Lower thread-stack/queue overhead | More stacks, queues and task objects | Multi-threading can raise memory |
| UI quality | Risk of jank if work is on main thread | Better if work is off main thread | Main thread must remain responsive |
| Worst case | More predictable for small serial work | Scheduling/lock contention adds variance | Bound concurrency and use backpressure |

### 2.4 Full working day requirement

Prefer efficiency cores for suitable background work, batch parsing and network requests, avoid busy loops, and schedule deferrable work through WorkManager. Retain high-priority foreground processing only for user-visible or urgent functions. Validate with energy profiler and thermal observations; elapsed time alone cannot establish energy efficiency.

## Task 3 – Runtime behaviour (10 Marks)

### Stage A – Workloads and metrics

Use CPU-bound algorithm, allocation-heavy object creation and UI-list rendering. Record cold/warm startup, ART compilation state, GC events/pause durations and heap growth. Include app version, Android version, device/emulator RAM and exact commands.

### Stage B – Compilation-mode predictions

| Mode | Prediction | Workload most affected |
|---|---|---|
| Verify/interpreter-heavy | Lower compilation cost/storage; slower repeated CPU hot path | CPU-bound loop |
| Speed-profile | Hot methods compiled from observed profile; balanced startup/steady state | Repeated CPU and UI code |
| Speed | Larger compiled footprint; faster hot execution; possible install/compile cost | CPU-bound loop |

Use `cmd package compile` only where supported; record command output. Do not assume all Android versions use identical ART behaviour.

### Stage C – Failure detection

Introduce a bounded test leak (e.g. retained Activity reference) and a main-thread sleep in a disposable test build. Detect heap growth/retained Activity with profiler or LeakCanary; detect blocking with StrictMode/ANR traces. Stop the experiment before exhausting the device. GC reports allocation/collection pressure; the system watchdog/ANR machinery reports prolonged main-thread unresponsiveness.

### Stage D – cross-platform runtime comparison

| Runtime | Memory model | UI/thread behaviour | Native access | Trade-off |
|---|---|---|---|---|
| Native Android ART | Managed heap + GC | Main thread must not block; background executors | JNI/NDK and Android APIs | Strong Android integration; separate iOS implementation |
| Swift/Objective-C | ARC | Main actor/UI thread rules | Native Apple frameworks | Strong iOS integration; separate Android implementation |
| Flutter | Dart AOT in release; managed heap/GC | Framework rendering; platform channels | Plugins/platform channels | Shared UI code; engine and memory footprint |
| React Native / WebView hybrid | JavaScript engine GC; bridge/JSI or WebView | JS/UI thread coordination | Native modules/web APIs | Broad code reuse; bridge/runtime and UI performance considerations |

Recommendation: for one codebase, Flutter is a reasonable candidate when consistent custom UI and native plugin access are needed, but benchmark startup, memory and platform integration against the actual workload. If deep platform-specific background services dominate, native apps may be safer. This is a design recommendation, not a measured winner.

## Task 4 – Secure mobile application audit (7 Marks)

### 4.1 Threat model

| Threat (STRIDE category) | Asset/vector | Protection | Residual risk |
|---|---|---|---|
| Spoofing | Stolen session token | Short-lived tokens, secure storage, re-authentication | Token theft on compromised unlocked device |
| Tampering | Modified local appointment DB | Encrypted DB, integrity checks, server validation | Rooted/jailbroken OS |
| Repudiation | User denies update | Audit events with server timestamps and identity | Account compromise |
| Information disclosure | Patient data at rest | Keystore/Keychain-backed encryption and sandbox | Data visible while app is unlocked |
| Denial of service | API flooding or storage exhaustion | Rate limits, quotas, bounded queues | Distributed attacks |
| Elevation of privilege | Exported component misuse | Non-exported components, signature permissions, input validation | Vulnerable trusted component |

### 4.2 Asset decision trace

| Asset | Attack vector | Mechanism | Result |
|---|---|---|---|
| Auth token | Shared file read | Private storage + Keystore encryption | Partially blocked |
| Patient DB | Device theft | Encrypted DB + hardware-backed key | Partially blocked |
| API traffic | MITM | TLS certificate validation | Blocked under correct trust config |
| Exported Activity | Malicious intent | Non-exported + validation | Blocked |
| Package update | Tampered package | Signing verification | Blocked unless signing chain compromised |
| Location | Over-collection | Runtime permission + minimisation | Partially blocked |

### 4.3 Predict before execution

Weakening `android:exported` to true for an internal component is predicted to expose an intent entry point. A malicious app may invoke it with crafted extras. The audit verdict changes from blocked to exposed/partially blocked depending on permission and validation. Run only against your own test package.

### 4.4 Third-party identifier leak

The asset is the device identifier; the affected layers are application/library data handling and transport. Sandbox/permission controls do not stop an app from voluntarily transmitting data it can access. Detect through static dependency review, runtime hooks or network capture. Remediate by removing unnecessary identifier access, minimising/rotating identifiers and enforcing TLS; verify destination and payload.

### 4.5 Biometric and BYOD extension

Add biometric threat cases: spoofing, fallback PIN abuse, replay and compromised biometric prompt integration. Bind cryptographic key use to OS user authentication where supported; do not store biometric templates in the app. BYOD adds profile boundary, work/personal data separation, managed configuration, selective remote wipe and key attestation. Audit must distinguish work-profile assets from personal assets and verify wipe scope.

## Task 5 – Power engineering (7 Marks)

### Technique 1: DVFS / heterogeneous cores
Trigger: CPU utilisation, thermal state and scheduler policy. State: frequency/voltage, runnable load and core capacity. Higher frequency improves latency but increases power/heat; efficiency cores suit sustained modest work. Measure CPU frequency, utilisation, thermal state and energy estimate.

### Technique 2: Doze / App Standby
Trigger: screen off, unplugged, stationary idle and app usage history. State: device idle mode, app standby bucket, pending jobs and maintenance windows. Reduces background wakeups/network activity but delays nonurgent sync. Measure wakeups, job execution and radio-active time.

### Technique 3: App-level batching
Trigger: accumulated sensor samples, network availability or scheduled job. State: queue length, last upload, constraints and active wakelocks. Batching reduces repeated radio wakeups; high-rate sampling still consumes sensor/CPU energy. Measure wakelock duration, sensor rate, radio activity and queued batch size.

**Conflict test:** A permanent partial wakelock can prevent deep idle and nullify Doze benefits. Frequent exact alarms can defeat batching. Prediction: OS-level power savings fall despite enabling Doze because app-level behaviour keeps waking the device. Release wakelocks promptly and use inexact/batched scheduling when precise timing is unnecessary.

**Deployment decision:** Always-on tracking needs carefully bounded foreground service and adaptive sensor sampling; media/gaming needs sustained performance and thermal management; enterprise fleets need version-aware policies, managed configuration and telemetry because OS versions differ.

## Task 6 – Battery-aware secure field-tracking prototype (9 Marks)

### 6.1 Problem model

Input: battery level/charging, network type, motion, device temperature, queue size, last upload and emergency priority. Output: sampling interval and upload decision. Objective: maximise useful tracking data delivered per unit energy while protecting data. Battery alone is insufficient: 20% battery while stationary on Wi-Fi differs from 20% while moving offline or in an emergency.

### 6.2 State-based policy

`Policy[BatteryState][NetworkState][MotionState] → {SamplingRate, UploadAction}`

Default state: NORMAL battery, available network, stationary. Every record is encrypted before queue commit; every upload uses authenticated TLS. Emergency priority overrides routine deferral.

| Condition | Sampling | Upload | Reason |
|---|---:|---|---|
| Charging + Wi-Fi | 10 s | Batch now | Low marginal energy cost |
| 80% + LTE + moving | 15 s | Batch when available | Useful movement detail |
| 20% + LTE + stationary | 120 s | Defer to Wi-Fi/charge | Preserve battery |
| 12% battery saver | 180 s | Queue | Critical reserve |
| Offline + moving | 30 s | Queue offline | Keep useful local samples |
| Device hot | 90 s | Defer until cool/Wi-Fi | Thermal protection |
| Emergency | 5 s | Immediate high priority | Reliability overrides routine saving |

### 6.3 Prototype and estimated energy

Run `python part2_prototype/src/run_all.py`. The output includes sampling interval, upload policy, encryption flag and illustrative energy estimate per policy cycle. These mAh values are model assumptions, not measured device energy.

### 6.4 Independent validation example

For three conditions (20% stationary LTE, offline moving, emergency), independently verify expected choices: 120 s/defer; 30 s/queue; 5 s/immediate high-priority. Compare with CSV output. Agreement verifies branching logic for those cases, not real battery accuracy.

### 6.5 Scalability and radio inquiry

Record policy evaluations, wakeups and queued records at 100, 1,000 and 10,000 records. Batching reduces repeated fixed radio wake-up costs, but continuous high-frequency sensing still consumes sensor, CPU and storage energy and generates more data. The repository contains deterministic test logic; real fleet load and battery tests require device/server instrumentation.

### 6.6 Requirement change: 5,000 devices and emergency updates within seconds

Routine battery policy becomes unsuitable during emergency because deferred uploads violate the new latency/reliability objective. Investigate priority queues, emergency foreground service, high-priority push, edge ingestion and fleet-side scheduling. Trade-offs include battery drain, heat, mobile data cost, privacy exposure and backend load.

### 6.7 Technical reflection (under 150 words)

No single power feature is optimal because energy cost depends on workload, motion, network, temperature, device capability and urgency. Batching is effective when records can wait, but it is unsuitable for emergency alerts that require delivery within seconds. Deep idle saves energy during stationary inactivity, yet continuous tracking may require a foreground service and bounded wake periods. DVFS can reduce energy for sustained low-priority work but may increase completion time. The prototype's policy branches demonstrate that the same battery percentage leads to different actions when connectivity, motion or emergency state changes. Therefore, a practical system needs adaptive policies and explicit priority classes rather than one fixed sampling rate or one OS setting.

## Final evidence and submission checklist

- Part I: submit the design document only; no IDE/emulator/SDK evidence is expected.
- Part II: include actual device/emulator commands, logs, screenshots, profiler traces, compilation outputs, security tests and Battery Historian/energy evidence.
- Keep predictions before each modified run; include actual result and explain every mismatch.
- Identify device model, OS version, RAM, app version and workload.
- Do not describe synthetic Python results as real Android measurements.
