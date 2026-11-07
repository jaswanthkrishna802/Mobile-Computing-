# Mobile Computing Assignment 3 (CO3) — Simulation Evidence

This repository contains small, reproducible **educational simulations / worked examples** for the practical parts of the Mobile Computing assignment.

## Coverage

| Assignment section | Evidence in this repository |
|---|---|
| Q1 — Wireless network and mobility | `src/q1_wireless_mobility.py` and `results/q1_handoff_trace.csv` |
| Q2 — Mobile IP | `src/q2_mobile_ip.py` and `results/q2_mobile_ip_trace.txt` |
| Q5 — Proactive routing (DSDV-style) | `src/q5_dsdv.py` and `results/q5_dsdv_trace.txt` |
| Q6 — Reactive routing (AODV-style) | `src/q6_aodv.py` and `results/q6_aodv_trace.txt` |
| Q7 — Emergency network | `src/q7_emergency_network.py` and `results/q7_performance.csv` |

## Requirements

- Python 3.9 or later
- No third-party Python packages required

## Run all demonstrations

From the repository root:

```bash
python run_all.py
```

Individual demonstrations can be run with:

```bash
python src/q1_wireless_mobility.py
python src/q2_mobile_ip.py
python src/q5_dsdv.py
python src/q6_aodv.py
python src/q7_emergency_network.py
```

The scripts write their outputs to the `results/` folder.

## Important interpretation note

These are **small logical simulations and worked examples**, not packet-level NS-2/NS-3 experiments and not measurements from physical wireless hardware. Delay, packet delivery, and routing-overhead values in Q7 are generated from a clearly stated simplified model to demonstrate how the metrics are calculated and compared. Do not describe them as real-world measurements.

For a formal packet-level experiment, implement the topology in NS-3 (or NS-2, if required by your faculty), configure mobility and traffic models, run multiple trials, and replace the illustrative values with measured output.

## Suggested submission evidence

Include this repository URL in your assignment after pushing it to GitHub. The `results/` folder contains generated traces and a CSV table that can be inspected by your faculty. The `docs/` folder contains a short evidence summary.
