from background_scheduler import *
from feed_optimizer import run_cases
from video_selector import choose, PROFILES
import json, csv
from pathlib import Path

out = Path(__file__).resolve().parents[1] / "results"
out.mkdir(exist_ok=True)
easy, hard = sample_workloads()
summary = {}
for name, items, cond in [
    ("Workload A",easy,Conditions(battery_pct=75,network="GOOD")),
    ("Workload B",hard,Conditions(battery_pct=8,network="POOR",doze=True))
]:
    summary[name]={}
    for strategy in ("FIFO","PRIORITY"):
        summary[name][strategy]=run_scheduler(items,cond,strategy)
(out/"background_results.json").write_text(json.dumps(summary,indent=2))
cases=run_cases()
(out/"feed_optimizer_results.json").write_text(json.dumps(cases,indent=2))
video=[choose(p) for p in PROFILES]
(out/"video_selector_results.json").write_text(json.dumps(video,indent=2))
with (out/"video_selector_results.csv").open("w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=video[0].keys()); w.writeheader(); w.writerows(video)
print("Background workload summary:")
for name, strategies in summary.items():
    for strategy, r in strategies.items():
        print(name, strategy, "enqueued",r["enqueued"],"success",r["successful"],
              "deferred",r["deferred"],"cancelled",r["cancelled"],"rejected",r["rejected"])
print("\\nFeed optimizer:")
for c in cases:
    print(c["case"],"exact",c["exact"],"adaptive",c["adaptive"],"evaluations",c["exact_evaluated"])
print("\\nVideo selector:")
for v in video: print(v)
