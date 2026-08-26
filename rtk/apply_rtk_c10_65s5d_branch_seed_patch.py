#!/usr/bin/env python3
from pathlib import Path
import json,re,sys
root=Path(sys.argv[1]).resolve();branch=sys.argv[2];repo=Path(__file__).resolve().parents[1];sys.path.insert(0,str(repo/'research/shadow'))
from rtk_c10_65s5d_branch_builder import build
t=json.loads((repo/'research/theory_targets/RTK_C10_65S5D_NEXT_K_MULTIBRANCH_ONE_STEP_PRODUCTION_CANARY_TARGET_v1.json').read_text());d=build(branch);k=json.loads((repo/'research/theory_results/RTK_C10_65S2K_ONE_ACCEPTED_STEP_RETRY_RESULT_v1.json').read_text());assert t['status']=='FROZEN_BEFORE_IMPLEMENTATION';assert float(t['execution']['retry_width_Mpc'])==float(k['retry_width_Mpc'])
def f(x):return format(float(x),'.17g')
def fdt(x):
 s=format(float(x),'.16g');assert float(s)==float(x);return s
c=d['carrier'];U=d['ur_l_ge_3'];vals=[d['k'],c['phi_CLASS_equals_Psi_N'],c['delta_b'],c['theta_b'],c['delta_g'],c['theta_g'],c['delta_ur'],c['theta_ur'],c['shear_ur'],c['delta_cdm_khr'],c['theta_cdm_khr']];row='  {'+','.join(f(x) for x in vals)+',{'+','.join(f(U[l]) for l in range(3,18))+'}}'
p=root/'source'/'rtk_c10_65s2_class_bridge.c';s=p.read_text();pat=r'static const s2seed S\[4\]\s*=\s*\{.*?\n\};\s*\nstatic const double DT\s*=\s*[^;]+;';mm=list(re.finditer(pat,s,re.S));
if len(mm)!=1:raise SystemExit(f'base seed block matches={len(mm)}')
m=mm[0];rep='static const s2seed S[1]={\n'+row+'\n};\nstatic const double DT='+fdt(t['execution']['retry_width_Mpc'])+';';s=s[:m.start()]+rep+s[m.end():]
if s.count('for(i=0;i<4;i++)')!=1:raise SystemExit('seed loop anchor missing');s=s.replace('for(i=0;i<4;i++)','for(i=0;i<1;i++)',1)
if 'static const s2seed S[1]' not in s or 'for(i=0;i<1;i++)' not in s:raise SystemExit('postcondition')
p.write_text(s);print('C10_65S5D_BRANCH_SEED_PATCH',branch,f(d['k']),fdt(t['execution']['retry_width_Mpc']))
