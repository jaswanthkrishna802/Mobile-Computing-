from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
SCRIPTS = [
    "q1_wireless_mobility.py",
    "q2_mobile_ip.py",
    "q5_dsdv.py",
    "q6_aodv.py",
    "q7_emergency_network.py",
]

for script in SCRIPTS:
    print(f"\n===== Running {script} =====")
    subprocess.run([sys.executable, str(ROOT / "src" / script)], check=True, cwd=ROOT)

print("\nAll demonstrations completed. See the results/ directory.")
