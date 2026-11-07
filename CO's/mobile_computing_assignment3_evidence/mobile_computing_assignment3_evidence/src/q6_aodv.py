from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "q6_aodv_trace.txt"

# Small AODV-style route-discovery trace on S-A-B-D.
topology = {
    "S": ["A"],
    "A": ["S", "B"],
    "B": ["A", "D"],
    "D": ["B"],
}
source, destination = "S", "D"
queue = [(source, [source])]
visited = {source}
route = None
events = ["AODV-STYLE ROUTE DISCOVERY", f"Source {source} needs a route to {destination}.", "S broadcasts RREQ."]
while queue:
    node, path = queue.pop(0)
    if node == destination:
        route = path
        break
    for neighbor in topology[node]:
        if neighbor not in visited:
            visited.add(neighbor)
            events.append(f"{node} forwards RREQ to {neighbor}.")
            queue.append((neighbor, path + [neighbor]))

if route:
    events.append(f"{destination} generates RREP.")
    events.append("RREP follows reverse path: " + " <- ".join(reversed(route[:-1])))
    events.append("Installed forward route: " + " -> ".join(route))
    events.append("Data packet forwarded successfully.")
else:
    events.append("No route found; ROUTE_NOT_FOUND.")

events.append("Link failure example: A-B goes DOWN.")
events.append("Affected route is marked INVALID; source may initiate a new RREQ.")
events.append("Note: this is a simplified AODV-style discovery demonstration, not a complete RFC implementation.")

OUT.write_text("\n".join(events) + "\n", encoding="utf-8")
print("\n".join(events))
print(f"Trace saved to {OUT.relative_to(ROOT)}")
