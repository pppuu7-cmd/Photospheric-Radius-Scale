#!/usr/bin/env python3
"""C10.65s3b/s3c endpoint selector only; no physics/tolerance mutation.

The selector is intentionally incapable of inventing an endpoint: a requested
width must occur in one of the already-frozen trajectory targets.  C10.65s3b
runs still source only the s3b list; C10.65s3c runs source only the s3c list.
The only CLASS mutation remains replacement of the pre-existing constant DT.
"""
from pathlib import Path
import argparse,json,re
ap=argparse.ArgumentParser();ap.add_argument('class_root');ap.add_argument('--width',required=True,type=float);a=ap.parse_args()
repo=Path(__file__).resolve().parents[1]
targets=[
  repo/'research/theory_targets/RTK_C10_65S3B_TRAJECTORY_SAMPLED_CONSTRAINT_TARGET_v1.json',
  repo/'research/theory_targets/RTK_C10_65S3C_TIME_WIDENED_TRAJECTORY_TARGET_v1.json',
]
allowed=[]
for q in targets:
    if q.exists():
        t=json.loads(q.read_text());assert t['status']=='FROZEN_BEFORE_EXECUTION';allowed.extend(float(x) for x in t['sample_elapsed_tau_Mpc'])
if not any(a.width==x for x in allowed): raise SystemExit('width not in any frozen s3b/s3c sample list')
p=Path(a.class_root).resolve()/'source'/'rtk_c10_65s2_class_bridge.c';s=p.read_text();old=re.findall(r'static const double DT=([^;]+);',s)
if len(old)!=1: raise SystemExit('DT anchor missing/nonunique')
s=re.sub(r'static const double DT=[^;]+;',f'static const double DT={a.width:.17g};',s,count=1);p.write_text(s)
print('C10_65_FROZEN_SAMPLE_INTERVAL_PATCH_APPLIED',format(a.width,'.17e'),'old',old[0])
