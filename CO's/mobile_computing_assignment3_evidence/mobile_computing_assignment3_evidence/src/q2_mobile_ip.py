from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "q2_mobile_ip_trace.txt"

home_address = "10.0.0.25"
care_of_address = "192.0.2.80"
binding = {}

lines = []
lines.append("MOBILE IP WORKED EXAMPLE")
lines.append(f"Mobile Node home address: {home_address}")
lines.append("Mobile Node has moved to a visited network.")
lines.append(f"Obtained Care-of Address: {care_of_address}")
lines.append("MN -> HA: Registration Request")
binding[home_address] = care_of_address
lines.append(f"HA: Binding updated: {home_address} -> {binding[home_address]}")
lines.append("HA -> MN: Registration Reply ACCEPTED")
packet = f"IP packet destined for {home_address}"
lines.append(f"CN -> HA: {packet}")
if home_address in binding:
    lines.append(f"HA: Encapsulate packet and tunnel to {binding[home_address]}")
    lines.append("Tunnel endpoint: Decapsulate original packet")
    lines.append("MN: Original packet DELIVERED")
else:
    lines.append("HA: No binding; packet delivery FAILED")

OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
print("\n".join(lines))
print(f"Trace saved to {OUT.relative_to(ROOT)}")
