"""Battery-aware field tracking policy simulation (illustrative, not device power measurement)."""
from dataclasses import dataclass, asdict
from typing import List
@dataclass
class Condition:
    name: str; battery: int; network: str; motion: str; charging: bool=False; hot: bool=False; emergency: bool=False
@dataclass
class Decision:
    name: str; sample_seconds: int; upload: str; encrypted: bool; estimated_mAh: float; reason: str
def decide(c: Condition) -> Decision:
    if c.emergency:
        return Decision(c.name, 5, "IMMEDIATE_HIGH_PRIORITY", True, 0.42, "Emergency priority overrides routine battery deferral.")
    if c.hot:
        return Decision(c.name, 90, "DEFER_UNTIL_COOL_OR_WIFI", True, 0.11, "Thermal protection reduces workload.")
    if c.charging and c.network == "WIFI":
        return Decision(c.name, 10, "BATCH_UPLOAD_NOW", True, 0.16, "Charging and Wi-Fi provide a suitable sync window.")
    if c.battery <= 15:
        return Decision(c.name, 180, "QUEUE_UNTIL_WIFI_OR_CHARGING", True, 0.06, "Critical battery saver policy.")
    if c.battery <= 25 and c.motion == "STATIONARY":
        return Decision(c.name, 120, "QUEUE_UNTIL_WIFI_OR_CHARGING", True, 0.07, "Low battery and stationary motion.")
    if c.network == "NONE":
        return Decision(c.name, 30 if c.motion=="MOVING" else 120, "QUEUE_OFFLINE", True, 0.08, "No connectivity; retain encrypted records.")
    if c.motion == "MOVING":
        return Decision(c.name, 15, "BATCH_UPLOAD_WHEN_AVAILABLE", True, 0.18, "Moving vehicle needs higher sampling frequency.")
    return Decision(c.name, 60, "COALESCE_UPLOAD", True, 0.10, "Default balanced mode.")
def scenarios():
    return [
      Condition("charging_wifi",92,"WIFI","MOVING",True),
      Condition("high_battery_lte_moving",80,"LTE","MOVING"),
      Condition("low_battery_stationary",20,"LTE","STATIONARY"),
      Condition("battery_saver",12,"LTE","MOVING"),
      Condition("offline_six_hours",55,"NONE","MOVING"),
      Condition("device_hot",48,"WIFI","MOVING",hot=True),
      Condition("emergency_alert",18,"LTE","MOVING",emergency=True),
    ]
def run():
    return [asdict(decide(c)) for c in scenarios()]
if __name__=="__main__":
    for row in run(): print(row)
