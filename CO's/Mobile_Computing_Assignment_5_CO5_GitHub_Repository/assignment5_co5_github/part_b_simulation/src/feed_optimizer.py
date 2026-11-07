"""Exact and adaptive feed-render configuration model."""
from itertools import product

QUALITIES = [
    {"name":"LOW","frame_cost":2,"energy":1,"visual_penalty":5,"decode_kb":80},
    {"name":"MEDIUM","frame_cost":4,"energy":2,"visual_penalty":2,"decode_kb":160},
    {"name":"HIGH","frame_cost":7,"energy":4,"visual_penalty":0,"decode_kb":300},
]
CACHES = [1,2,3]
PREFETCH = [0,1,2]

def cost(items, q, cache, prefetch, battery_pct=70):
    # Illustrative deterministic objective; lower is better.
    frame_drops = max(0, q["frame_cost"] + prefetch*1.5 - 8) * items
    memory_penalty = max(0, cache* q["decode_kb"] - 500) * 0.015
    energy = items * (q["energy"] + cache*0.25 + prefetch*0.2)
    quality_penalty = items * q["visual_penalty"] * 0.35
    low_battery_penalty = energy * (1.0 if battery_pct < 20 else 0.15)
    return round(frame_drops*3 + memory_penalty + energy + quality_penalty + low_battery_penalty, 3)

def exact(items, battery_pct=70):
    best = None
    evaluated = 0
    for q, cache, prefetch in product(QUALITIES, CACHES, PREFETCH):
        evaluated += 1
        c = cost(items,q,cache,prefetch,battery_pct)
        candidate = {"quality":q["name"],"cache":cache,"prefetch":prefetch,"cost":c}
        if best is None or c < best["cost"]:
            best = candidate
    return best, evaluated

def adaptive(items, battery_pct=70, frame_budget=16):
    # Greedy policy starts at medium quality, cache=2, prefetch=1.
    q = QUALITIES[1]
    cache, prefetch = 2, 1
    changes = 0
    estimated_frame_ms = q["frame_cost"] + prefetch*1.5
    while estimated_frame_ms > frame_budget and (q["name"] != "LOW" or prefetch > 0):
        if prefetch > 0:
            prefetch -= 1
        elif q["name"] == "HIGH":
            q = QUALITIES[1]
        else:
            q = QUALITIES[0]
        changes += 1
        estimated_frame_ms = q["frame_cost"] + prefetch*1.5
    if battery_pct < 20:
        if cache > 1: cache -= 1; changes += 1
        if prefetch > 0: prefetch = 0; changes += 1
        if q["name"] == "HIGH": q = QUALITIES[1]; changes += 1
    return {"quality":q["name"],"cache":cache,"prefetch":prefetch,
            "cost":cost(items,q,cache,prefetch,battery_pct),
            "changes":changes,"estimated_frame_ms":estimated_frame_ms}

def run_cases():
    cases = [
        {"name":"small-balanced","items":5,"battery":70},
        {"name":"medium-low-battery","items":20,"battery":15},
        {"name":"large-feed","items":100,"battery":65},
        {"name":"counterexample-quality","items":12,"battery":70},
    ]
    rows=[]
    for c in cases:
        e,n=exact(c["items"],c["battery"])
        a=adaptive(c["items"],c["battery"])
        rows.append({"case":c["name"],"items":c["items"],"battery":c["battery"],
                     "exact":e,"exact_evaluated":n,"adaptive":a})
    return rows

if __name__ == "__main__":
    import json
    print(json.dumps(run_cases(),indent=2))
