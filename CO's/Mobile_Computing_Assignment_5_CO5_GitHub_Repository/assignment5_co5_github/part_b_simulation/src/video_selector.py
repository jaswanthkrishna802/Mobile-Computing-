"""Heuristic multimedia encoding selector (educational estimate, not codec benchmark)."""
PROFILES = [
    {"name":"Low-end","cpu":2,"battery":18,"uplink_mbps":1.2,"thermal":"WARM"},
    {"name":"Mid-range","cpu":5,"battery":55,"uplink_mbps":5.0,"thermal":"NORMAL"},
    {"name":"Flagship","cpu":9,"battery":85,"uplink_mbps":20.0,"thermal":"NORMAL"},
    {"name":"Weak-network","cpu":6,"battery":35,"uplink_mbps":0.35,"thermal":"HOT"},
]
OPTIONS = [
    {"resolution":"480p","bitrate_mbps":0.8,"encode_cost":1.0,"quality":1},
    {"resolution":"720p","bitrate_mbps":2.0,"encode_cost":2.0,"quality":2},
    {"resolution":"1080p","bitrate_mbps":5.0,"encode_cost":4.0,"quality":3},
]
def choose(profile):
    # Fast heuristic: cap quality by CPU/thermal/battery, then network.
    max_q = 3
    if profile["cpu"] < 4 or profile["thermal"] == "HOT": max_q = 1
    elif profile["cpu"] < 7 or profile["battery"] < 25: max_q = 2
    if profile["battery"] < 15: max_q = 1
    eligible = [o for o in OPTIONS if o["quality"] <= max_q and o["bitrate_mbps"] <= max(0.5,profile["uplink_mbps"]*0.8)]
    option = eligible[-1] if eligible else OPTIONS[0]
    duration_s = 15
    upload_s = option["bitrate_mbps"] * duration_s / max(profile["uplink_mbps"],0.05)
    energy_est = option["encode_cost"]*duration_s*0.08 + upload_s*0.03
    battery_impact = round(energy_est / 100, 3)
    return {"device":profile["name"],"resolution":option["resolution"],
            "bitrate_mbps":option["bitrate_mbps"],"upload_seconds_est":round(upload_s,2),
            "energy_units_est":round(energy_est,2),"battery_fraction_est":battery_impact}
if __name__ == "__main__":
    import json
    print(json.dumps([choose(p) for p in PROFILES],indent=2))
