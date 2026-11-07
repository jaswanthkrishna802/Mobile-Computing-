# Android evidence collection checklist (run on your own test device/emulator)

These commands are templates. Capture the actual output with device model, Android version, emulator RAM and timestamp. Do not paste real tokens, patient records or device identifiers into a public repository.

## Task 1 – process and lifecycle
```bash
adb shell getprop ro.build.version.release
adb shell getprop ro.product.model
adb shell ps -A
adb shell dumpsys activity processes
adb shell dumpsys meminfo <your.package.name>
adb logcat -d -s ActivityTaskManager ActivityManager
```
Run foreground, background (wait five minutes), and memory-pressure cases. For memory pressure, use a disposable emulator and record the exact command/API used; lifecycle callbacks are app-specific.

## Task 2 – CPU/thread and UI profiling
Use Android Studio Profiler or Perfetto. Record task duration, CPU time, thread count, context switches, heap/PSS and frame timing for the same input and device state. Save trace files/screenshots.

## Task 3 – ART compilation and GC
```bash
adb shell dumpsys package <your.package.name>
adb shell cmd package compile -m verify -f <your.package.name>
adb shell cmd package compile -m speed-profile -f <your.package.name>
adb shell cmd package compile -m speed -f <your.package.name>
adb logcat -d | grep -iE 'art|gc|concurrent copying|outofmemory'
```
Compilation filters and command support vary by Android version. Record unsupported commands as such.

## Task 4 – security
Inspect AndroidManifest.xml, exported components, requested permissions, network security config and storage design. Use a test account and test data only. Capture `adb shell dumpsys package <package>` and a controlled HTTPS/network-capture test. Do not attempt attacks against third-party systems.

## Task 5 – power
```bash
adb shell dumpsys batterystats --reset
# Run a fixed workload for a measured interval
adb shell dumpsys batterystats
adb shell dumpsys deviceidle
adb shell dumpsys power
```
Use Battery Historian/Android Studio Energy Profiler where available. A battery percentage delta alone is insufficient; capture wakelock time, wakeups, radio activity, GPS use and duration.

## Task 6 – prototype validation
Run the Python policy simulation and compare its decisions against a hand-worked three-case reference. If testing Android integration, capture encrypted-storage and authenticated-sync evidence separately.
