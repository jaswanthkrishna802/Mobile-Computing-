# Android evidence checklist

Record device model, Android version/build, app version/commit, battery level, thermal state, network state and exact test steps.

Capture:
1. Good-network / high-battery successful WorkManager run.
2. Doze or low-battery routine work deferral.
3. Permission revocation during or before work and cancellation.
4. Encrypted outbox state and server acknowledgement.
5. FIFO and priority scheduler counts for the same workload.
6. Profiler/logcat evidence and server-side idempotency evidence.

Suggested commands:
```bash
adb shell getprop ro.build.version.release
adb shell getprop ro.build.fingerprint
adb shell dumpsys battery
adb shell dumpsys deviceidle
adb shell dumpsys jobscheduler
adb shell dumpsys meminfo <package.name>
adb logcat -v time
```

Do not claim Python model outputs are real Android measurements.
