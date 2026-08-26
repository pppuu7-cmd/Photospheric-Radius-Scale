#!/usr/bin/env python3
"""C10.65s4d domain-only production patch: replace low-k seed table by s4b moderate-k carrier and keep s2k width.

This adapter deliberately changes only the frozen seed-domain table and retry width.
The generated C bridge from the s2 patch contains a normal C initializer `S[4]={...}`;
the earlier adapter incorrectly searched for the Python f-string source spelling `{{`.
No scientific criterion, equation, or threshold is changed here.
"""
from pathlib import Path
import json,re,sys
root=Path(sys.argv[1]).resolve(); repo=Path(__file__).resolve().parents[1]
t=json.loads((repo/'research/theory_targets/RTK_C10_65S4D_MODERATE_K_ONE_ACCEPTED_STEP_PRODUCTION_CANARY_TARGET_v1.json').read_text())
b=json.loads((repo/'research/theory_results/RTK_C10_65S4B_MODERATE_K_COMPLETED_ONSET_SEED_RESULT_v1.json').read_text())
k=json.loads((repo/'research/theory_results/RTK_C10_65S2K_ONE_ACCEPTED_STEP_RETRY_RESULT_v1.json').read_text())
assert t['status']=='FROZEN_BEFORE_IMPLEMENTATION'
assert b['classification']=='C10_65S4B_MODERATE_K_COMPLETED_ONSET_SEED_PASS_SCOPED'
assert k['classification']=='C10_65S2K_ONE_ACCEPTED_STEP_RETRY_PASS_SCOPED'
assert float(t['execution']['retry_width_Mpc'])==float(k['retry_width_Mpc'])
ks=[float(x) for x in t['domain']['k_Mpc_inv']]; by={float(r['k']):r for r in b['records']}; assert set(by)==set(ks)
def f(x): return format(float(x),'.17g')
def fdt(x):
    # Canonical shortest-enough decimal used only for the frozen step width.
    # It round-trips to exactly the same binary64 value as the target while
    # remaining compatible with the original frozen workflow's textual guard.
    s=format(float(x),'.16g')
    assert float(s)==float(x)
    return s
rows=[]
for kval in ks:
    r=by[kval]; c=r['carrier']; U={int(q['l']):float(q['F_l']) for q in r['ur_l_ge_3']}; assert set(U)==set(range(3,18))
    vals=[kval,c['phi_CLASS_equals_Psi_N'],c['delta_b'],c['theta_b'],c['delta_g'],c['theta_g'],c['delta_ur'],c['theta_ur'],c['shear_ur'],c['delta_cdm_khr'],c['theta_cdm_khr']]
    rows.append('  {'+','.join(f(x) for x in vals)+',{'+','.join(f(U[l]) for l in range(3,18))+'}}')
p=root/'source'/'rtk_c10_65s2_class_bridge.c'; s=p.read_text()
pat=r'static const s2seed S\[4\]\s*=\s*\{.*?\n\};\s*\nstatic const double DT\s*=\s*[^;]+;'
matches=list(re.finditer(pat,s,re.S))
if len(matches)!=1: raise SystemExit(f's2 bridge low-k seed/DT block not found uniquely: {len(matches)} matches')
m=matches[0]
rep='static const s2seed S[2]={\n'+',\n'.join(rows)+'\n};\nstatic const double DT='+fdt(t['execution']['retry_width_Mpc'])+';'
s=s[:m.start()]+rep+s[m.end():]
if s.count('for(i=0;i<4;i++)')!=1: raise SystemExit('seed loop anchor missing/nonunique')
s=s.replace('for(i=0;i<4;i++)','for(i=0;i<2;i++)',1)
tab=re.search(r'static const s2seed S\[2\]\s*=\s*\{(.*?)\n\};',s,re.S)
if tab is None: raise SystemExit('moderate-k S[2] initializer missing after replacement')
row_matches=re.findall(r'^\s*\{\s*([^,]+),',tab.group(1),re.M)
if len(row_matches)!=2: raise SystemExit(f'moderate-k seed row count mismatch: {len(row_matches)}')
parsed=[float(x.strip()) for x in row_matches]
if parsed!=ks: raise SystemExit(f'moderate-k seed-domain mismatch: {parsed} != {ks}')
if 'static const s2seed S[2]={' not in s or 'for(i=0;i<2;i++)' not in s:
    raise SystemExit('moderate-k seed table postcondition failed')
p.write_text(s)
print('C10_65S4D_MODERATE_K_SEED_WIDTH_PATCH_APPLIED',','.join(f(x) for x in ks),fdt(t['execution']['retry_width_Mpc']))
