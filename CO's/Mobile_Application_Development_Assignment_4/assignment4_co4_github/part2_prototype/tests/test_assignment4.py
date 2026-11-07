import sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from battery_policy import Condition, decide
from security_audit import audit
from threading_model import compare
class TestAssignment4(unittest.TestCase):
    def test_emergency_overrides_low_battery(self):
        d=decide(Condition("urgent",8,"LTE","MOVING",emergency=True))
        self.assertEqual(d.upload,"IMMEDIATE_HIGH_PRIORITY")
    def test_offline_data_is_queued_and_encrypted(self):
        d=decide(Condition("offline",55,"NONE","MOVING"))
        self.assertEqual(d.upload,"QUEUE_OFFLINE"); self.assertTrue(d.encrypted)
    def test_low_battery_stationary_sampling_slows(self):
        d=decide(Condition("low",20,"LTE","STATIONARY"))
        self.assertEqual(d.sample_seconds,120)
    def test_security_audit_has_six_assets(self):
        self.assertGreaterEqual(len(audit()),6)
    def test_more_threads_not_always_better(self):
        rows={r["workload"]:r for r in compare()}
        self.assertGreater(rows["tiny_task"]["multi_ms"],rows["tiny_task"]["single_ms"])
        self.assertGreater(rows["large_parse"]["single_ms"],rows["large_parse"]["multi_ms"])
if __name__=="__main__": unittest.main()
