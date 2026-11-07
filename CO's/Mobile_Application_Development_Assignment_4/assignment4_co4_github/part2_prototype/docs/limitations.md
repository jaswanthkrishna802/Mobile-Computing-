# Measurement and validity note

The Python prototype produces deterministic synthetic examples to make policy decisions, threat-to-control mappings, runtime comparison assumptions and threading-overhead counterexamples reproducible.

It does **not** emulate Android's kernel, ART, Binder, Zygote, Doze, JobScheduler, Keystore, SELinux, CPU governors, radio hardware or actual battery discharge. The numbers in `runtime_model.csv` and `threading_comparison.csv` are teaching placeholders. They must not be reported as measured device results.

For full credit under Part II, run the requested Android experiments on a real device/emulator and replace the illustrative records with captured logs, profiler traces, screenshots and environment details. If a particular experiment cannot be run, document the limitation rather than fabricating evidence.
