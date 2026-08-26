#!/usr/bin/env python3
"""C10.65s2l implementation-scale-only finite-short-interval patch."""
from pathlib import Path
import json,re,sys
root=Path(sys.argv[1]).resolve(); repo=Path(__file__).resolve().parents[1]
t=json.loads((repo/'research/theory_targets/RTK_C10_65S2L_FINITE_SHORT_INTERVAL_ENDPOINT_STABILITY_TARGET_v1.json').read_text())
k=json.loads((repo/'research/theory_results/RTK_C10_65S2K_ONE_ACCEPTED_STEP_RETRY_RESULT_v1.json').read_text())
assert t['status']=='FROZEN_BEFORE_EXECUTION'
assert k['classification']=='C10_65S2K_ONE_ACCEPTED_STEP_RETRY_PASS_SCOPED'
w=float(t['execution']['finite_short_interval_Mpc'])
assert w==float(t['execution']['base_retry_width_Mpc'])*int(t['execution']['interval_multiplier'])
p=root/'source'/'rtk_c10_65s2_class_bridge.c'; s=p.read_text()
old=re.findall(r'static const double DT=([^;]+);',s)
if len(old)!=1: raise SystemExit('C10.65s2 bridge DT anchor missing or nonunique')
# implementation-scale-only finite-interval patch: static const double DT=<prospectively frozen s2l interval>;
s=re.sub(r'static const double DT=[^;]+;',f'static const double DT={w:.17g};',s,count=1)
p.write_text(s)
print('C10_65S2L_FINITE_INTERVAL_PATCH_APPLIED',format(w,'.17e'),'old',old[0])
