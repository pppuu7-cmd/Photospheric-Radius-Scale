#!/usr/bin/env python3
"""C10.65s4f endpoint selector only; no physics/tolerance mutation."""
from pathlib import Path
import argparse,json,re
ap=argparse.ArgumentParser();ap.add_argument('class_root');ap.add_argument('--width',required=True,type=float);a=ap.parse_args();repo=Path(__file__).resolve().parents[1]
t=json.loads((repo/'research/theory_targets/RTK_C10_65S4F_MODERATE_K_TIME_WIDENED_TRAJECTORY_TARGET_v1.json').read_text());assert t['status']=='FROZEN_BEFORE_EXECUTION';allowed=[float(x) for x in t['sample_elapsed_tau_Mpc']]
if not any(a.width==x for x in allowed):raise SystemExit('width not in frozen C10.65s4f list')
p=Path(a.class_root).resolve()/'source'/'rtk_c10_65s2_class_bridge.c';s=p.read_text();old=re.findall(r'static const double DT=([^;]+);',s)
if len(old)!=1:raise SystemExit('DT anchor missing/nonunique')
s=re.sub(r'static const double DT=[^;]+;',f'static const double DT={a.width:.17g};',s,count=1);p.write_text(s);print('C10_65S4F_FROZEN_INTERVAL',format(a.width,'.17e'))
