import unittest
from background_scheduler import WorkItem, Conditions, run_scheduler, sample_workloads
from feed_optimizer import exact, adaptive
from video_selector import choose, PROFILES

class Assignment5Tests(unittest.TestCase):
    def test_unencrypted_sensitive_data_rejected(self):
        item=WorkItem("X","upload",3,20,sensitive=True,encrypted=False)
        result=run_scheduler([item],Conditions())
        self.assertEqual(result["rejected"],1)
        self.assertEqual(result["successful"],0)

    def test_low_battery_defers_noncritical(self):
        item=WorkItem("X","upload",3,20)
        result=run_scheduler([item],Conditions(battery_pct=5))
        self.assertEqual(result["deferred"],1)

    def test_critical_alert_can_execute_in_doze(self):
        item=WorkItem("A","alert",5,5,critical=True)
        result=run_scheduler([item],Conditions(battery_pct=5,doze=True,network="GOOD"))
        self.assertEqual(result["successful"],1)

    def test_exact_evaluates_all_small_configurations(self):
        best,n=exact(5)
        self.assertEqual(n,27)
        self.assertIn(best["quality"],["LOW","MEDIUM","HIGH"])

    def test_video_selector_returns_valid_resolution(self):
        result=choose(PROFILES[0])
        self.assertIn(result["resolution"],["480p","720p","1080p"])

if __name__ == "__main__":
    unittest.main()
