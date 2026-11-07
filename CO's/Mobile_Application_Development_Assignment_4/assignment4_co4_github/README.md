# Mobile Application Development Environment – Assignment 4 (CO4)

This repository accompanies the individual Assignment 4 submission (Part I + Part II).

## Repository map
- `part1_design/` – structured design notes, platform comparisons, architecture/state models.
- `part2_prototype/src/` – standard-library Python prototype models for policy, audit and runtime/threading experiments.
- `part2_prototype/tests/` – repeatable test runner and test cases.
- `part2_prototype/results/` – generated CSV/text outputs and charts.
- `part2_prototype/docs/` – experiment notes, assumptions and limitations.
- `evidence_templates/` – commands/checklists for collecting genuine Android evidence.

## Important evidence boundary
Part I explicitly prohibits IDE/emulator/SDK use; it is a design-only assignment.
Part II asks for Android/device instrumentation. The Python prototype in this repository is a **logic-level simulation**, not Android runtime evidence. It does not measure real CPU placement, ART compilation, Android process death, Binder traffic, battery current, Doze behaviour, or OS security enforcement. The sample outputs are labelled as simulated. Replace or supplement them with screenshots/logs from your own Android device/emulator before claiming those measurements.

## Run
Requires Python 3.10+; no third-party packages are needed.

```bash
python part2_prototype/src/run_all.py
python -m unittest discover -s part2_prototype/tests -v
```

Charts are generated when `matplotlib` is installed; CSV and text evidence are always generated.

## Suggested GitHub upload
Create a public or private repository named `mobile-application-development-assignment-4-co4`, then upload the contents of this folder. Do not upload personal patient data, API keys, tokens, or real device identifiers.
