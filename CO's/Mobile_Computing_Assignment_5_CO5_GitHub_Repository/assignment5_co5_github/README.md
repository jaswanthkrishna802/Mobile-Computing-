# Mobile Computing – Assignment 5 (CO5)

This repository contains the Assignment 5 design answers and reproducible Python simulations.

## Structure
- `part_a_design/` – language-independent pseudocode, task answers and diagrams.
- `part_b_simulation/src/` – background scheduler, exact/adaptive feed optimiser and multimedia selector.
- `part_b_simulation/tests/` – unit tests.
- `part_b_simulation/results/` – deterministic model outputs and graph.
- `evidence_templates/` – Android evidence checklist and test log template.

## Run
Python 3.10+ recommended.

```bash
python part_b_simulation/src/run_all.py
python -m unittest discover -s part_b_simulation/tests -v
```

## Important limitation
The Python implementation is a deterministic educational simulation. It is not an Android application, does not call WorkManager, does not measure real battery drain, and does not produce Android Profiler traces. Use the evidence template to add genuine Android Studio/emulator/physical-device evidence if required.
