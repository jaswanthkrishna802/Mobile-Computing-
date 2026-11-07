from pathlib import Path
import sys, csv, json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
sys.path.insert(0,str(HERE))
from battery_policy import run as battery_run
from security_audit import audit
from threading_model import compare
from runtime_model import runtime_cases
out=ROOT/"results"; out.mkdir(exist_ok=True)
def write_csv(name, rows):
    with (out/name).open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0].keys()));w.writeheader();w.writerows(rows)
battery=battery_run(); security=audit(); threading=compare(); runtime=runtime_cases()
write_csv("battery_policy_scenarios.csv",battery)
write_csv("security_audit.csv",security)
write_csv("threading_comparison.csv",threading)
write_csv("runtime_model.csv",runtime)
(out/"run_summary.txt").write_text(
"ASSIGNMENT 4 CO4 – SYNTHETIC PROTOTYPE RUN\n"
"All values below are illustrative logic-model outputs, not Android device measurements.\n\n"
+ "BATTERY POLICY\n" + "\\n".join(str(x) for x in battery)
+ "\n\nSECURITY AUDIT\n" + "\\n".join(str(x) for x in security)
+ "\n\nTHREADING MODEL\n" + "\\n".join(str(x) for x in threading)
+ "\n\nRUNTIME MODEL\n" + "\\n".join(str(x) for x in runtime),encoding="utf-8")
print("Generated four CSV result files and run_summary.txt")
print("Evidence boundary: synthetic model only; collect real adb/Profiler/Battery Historian evidence separately.")
