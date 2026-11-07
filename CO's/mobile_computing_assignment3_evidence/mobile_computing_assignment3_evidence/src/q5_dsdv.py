from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "q5_dsdv_trace.txt"

# Simplified DSDV-style route-table update example.
# Route tuple: (next_hop, hop_count, destination_sequence_number)
route_table = {
    "D": ("B", 2, 16)
}
lines = [
    "DSDV-STYLE ROUTE UPDATE WORKED EXAMPLE",
    "Initial route table at A:",
    "Destination D -> next hop B, hop count 2, sequence 16",
    "Event: link A-B fails.",
    "A receives a fresh route advertisement for D via C:",
    "Advertised hop count = 1; sequence number = 18",
]
received = ("C", 2, 18)  # receiver adds one hop to advertised hop count
current = route_table.get("D")
if current is None or received[2] > current[2] or (
    received[2] == current[2] and received[1] < current[1]
):
    route_table["D"] = received
    lines.append("Decision: accept the fresher sequence number.")
else:
    lines.append("Decision: retain the current route.")

lines.append(
    f"Updated route table: D -> next hop {route_table['D'][0]}, "
    f"hop count {route_table['D'][1]}, sequence {route_table['D'][2]}"
)
lines.append("Note: this is a teaching example of DSDV sequence-number logic, not a full DSDV implementation.")

OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
print("\n".join(lines))
print(f"Trace saved to {OUT.relative_to(ROOT)}")
