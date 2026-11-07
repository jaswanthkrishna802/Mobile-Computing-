from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "q1_handoff_trace.csv"
OUT.parent.mkdir(exist_ok=True)

# Illustrative signal-strength samples (dBm) as a user moves from AP1 to AP2.
samples = [
    (0, -48, -82),
    (1, -55, -76),
    (2, -63, -68),
    (3, -71, -59),
    (4, -79, -51),
]
threshold = -70
active_ap = "AP1"
rows = []

for time_step, ap1, ap2 in samples:
    best_ap = "AP1" if ap1 > ap2 else "AP2"
    best_signal = max(ap1, ap2)
    event = "CONNECTED"
    if active_ap == "AP1" and ap1 < threshold and ap2 >= threshold:
        active_ap = "AP2"
        event = "HANDOFF_AP1_TO_AP2"
    elif best_signal < threshold:
        event = "WEAK_SIGNAL"
    rows.append({
        "time_step": time_step,
        "AP1_signal_dBm": ap1,
        "AP2_signal_dBm": ap2,
        "active_access_point": active_ap,
        "event": event,
    })

with OUT.open("w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print("Q1 wireless mobility demonstration")
for row in rows:
    print(row)
print(f"Trace saved to {OUT.relative_to(ROOT)}")
