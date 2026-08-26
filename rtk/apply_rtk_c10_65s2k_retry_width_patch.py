#!/usr/bin/env python3
"""C10.65s2k implementation-scale-only retry patch; physics and tolerance unchanged."""
from pathlib import Path
import json,re,sys
root=Path(sys.argv[1]).resolve(); repo=Path(__file__).resolve().parents[1]
t=json.loads((repo/'research/theory_targets/RTK_C10_65S2K_ONE_ACCEPTED_STEP_RETRY_TARGET_v1.json').read_text())
j=json.loads((repo/'research/theory_results/RTK_C10_65S2J_PROSPECTIVE_RETRY_WIDTH_RESULT_v1.json').read_text())
assert t['status']=='FROZEN_BEFORE_RETRY_EXECUTION'
assert j['classification']=='C10_65S2J_PROSPECTIVE_RETRY_WIDTH_PASS_SCOPED'
w=float(t['retry_execution']['retry_width_Mpc']); assert w==float(j['retry_width_Mpc'])
p=root/'source'/'rtk_c10_65s2_class_bridge.c'; s=p.read_text()
old=re.findall(r'static const double DT=([^;]+);',s)
if len(old)!=1: raise SystemExit('C10.65s2 bridge DT anchor missing or nonunique')
s=re.sub(r'static const double DT=[^;]+;',f'static const double DT={w:.17g};',s,count=1)
p.write_text(s)
print('C10_65S2K_RETRY_WIDTH_PATCH_APPLIED',format(w,'.17e'),'old',old[0])
