"""Constraint-aware background-work scheduler (educational simulation).

This is a deterministic model, not an Android WorkManager implementation.
It demonstrates feasibility checks, FIFO/priority ordering, cancellation,
instrumentation and a permission-revocation boundary case.
"""
from dataclasses import dataclass, asdict
from typing import List, Dict, Any

@dataclass
class WorkItem:
    work_id: str
    kind: str
    priority: int
    size_kb: int
    sensitive: bool = False
    encrypted: bool = True
    permission_required: bool = False
    critical: bool = False
    status: str = "PENDING"

@dataclass
class Conditions:
    battery_pct: int = 80
    network: str = "GOOD"      # GOOD, METERED, POOR, OFFLINE
    doze: bool = False
    permission_granted: bool = True
    max_workers: int = 2

def feasible(item: WorkItem, c: Conditions):
    if item.sensitive and not item.encrypted:
        return False, "REJECT_UNENCRYPTED"
    if item.permission_required and not c.permission_granted:
        return False, "CANCEL_PERMISSION_REVOKED"
    if c.battery_pct <= 10 and not item.critical:
        return False, "DEFER_LOW_BATTERY"
    if c.doze and not item.critical:
        return False, "DEFER_DOZE"
    if c.network == "OFFLINE":
        return False, "DEFER_OFFLINE"
    if c.network == "POOR" and item.size_kb > 100 and not item.critical:
        return False, "DEFER_POOR_NETWORK"
    if c.network == "METERED" and item.size_kb > 500 and not item.critical:
        return False, "DEFER_METERED_LARGE"
    return True, "ELIGIBLE"

def run_scheduler(items: List[WorkItem], conditions: Conditions, strategy="FIFO"):
    queue = list(items)
    if strategy == "PRIORITY":
        queue.sort(key=lambda x: (-int(x.critical), -x.priority, x.size_kb, x.work_id))
    metrics = {
        "strategy": strategy, "enqueued": len(items), "deferred": 0,
        "cancelled": 0, "rejected": 0, "successful": 0,
        "max_concurrent_workers": 0, "decision_log": []
    }
    active = 0
    for item in queue:
        ok, reason = feasible(item, conditions)
        entry = {"work_id": item.work_id, "decision": reason}
        if not ok:
            if reason.startswith("DEFER"):
                item.status = "DEFERRED"; metrics["deferred"] += 1
            elif reason.startswith("CANCEL"):
                item.status = "CANCELLED"; metrics["cancelled"] += 1
            else:
                item.status = "REJECTED"; metrics["rejected"] += 1
            metrics["decision_log"].append(entry)
            continue
        if active >= conditions.max_workers:
            # The simulation processes workers sequentially after recording the cap.
            active = 0
        active += 1
        metrics["max_concurrent_workers"] = max(metrics["max_concurrent_workers"], active)
        item.status = "SUCCESS"
        metrics["successful"] += 1
        metrics["decision_log"].append({**entry, "decision": "EXECUTE_SUCCESS"})
        active -= 1
    metrics["residual_backlog"] = metrics["deferred"]
    return metrics

def sample_workloads():
    easy = [
        WorkItem("E1","sensor",2,30), WorkItem("E2","upload",3,80),
        WorkItem("E3","alert",5,10,critical=True),
        WorkItem("E4","upload",2,60), WorkItem("E5","sensor",1,25)
    ]
    difficult = [
        WorkItem("D1","upload",1,900,sensitive=True,encrypted=False),
        WorkItem("D2","upload",2,800,sensitive=True,encrypted=True),
        WorkItem("D3","sensor",1,140), WorkItem("D4","upload",2,600),
        WorkItem("D5","alert",5,20,critical=True)
    ]
    return easy, difficult

if __name__ == "__main__":
    easy, hard = sample_workloads()
    for name, items, cond in [
        ("easy", easy, Conditions(battery_pct=75, network="GOOD")),
        ("difficult", hard, Conditions(battery_pct=8, network="POOR", doze=True))
    ]:
        for strategy in ("FIFO","PRIORITY"):
            result = run_scheduler(items, cond, strategy)
            print(name, strategy, json.dumps({k:v for k,v in result.items() if k!="decision_log"}))
