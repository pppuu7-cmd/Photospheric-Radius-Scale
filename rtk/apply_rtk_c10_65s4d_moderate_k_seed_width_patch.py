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
rows=[]
for kval in ks:
    r=by[kval]; c=r['carrier']; U={int(q['l']):float(q['F_l']) for q in r['ur_l_ge_3']}; assert set(U)==set(range(3,18))
    vals=[kval,c['phi_CLASS_equals_Psi_N'],c['delta_b'],c['theta_b'],c['delta_g'],c['theta_g'],c['delta_ur'],c['theta_ur'],c['shear_ur'],c['delta_cdm_khr'],c['theta_cdm_khr']]
    rows.append('  {'+','.join(f(x) for x in vals)+',{'+','.join(f(U[l]) for l in range(3,18))+'}}')
p=root/'source'/'rtk_c10_65s2_class_bridge.c'; s=p.read_text()
# Match the generated C, not the Python f-string source spelling.  Bound the
# replacement by the immediately following DT declaration so this remains a
# structural, domain-only edit and fails closed if the bridge layout changes.
pat=r'static const s2seed S\[4\]\s*=\s*\{.*?\n\};\s*\nstatic const double DT\s*=\s*[^;]+;'
matches=list(re.finditer(pat,s,re.S))
if len(matches)!=1: raise SystemExit(f's2 bridge low-k seed/DT block not found uniquely: {len(matches)} matches')
m=matches[0]
rep='static const s2seed S[2]={\n'+',\n'.join(rows)+'\n};\nstatic const double DT='+f(t['execution']['retry_width_Mpc'])+';'
s=s[:m.start()]+rep+s[m.end():]
if s.count('for(i=0;i<4;i++)')!=1: raise SystemExit('seed loop anchor missing/nonunique')
s=s.replace('for(i=0;i<4;i++)','for(i=0;i<2;i++)',1)
# Audit: new moderate-k domain is present and old low-k seed literals do not
# survive in the generated bridge.  This is intentionally not a broad textual
# rewrite of any kernel equation.
for kval in ks:
    if f(kval) not in s: raise SystemExit('moderate-k seed literal missing: '+f(kval))
for z in ['1.0000000000000001e-05','3.0000000000000001e-05','0.0001','0.00029999999999999997']:
    if z in s: raise SystemExit('low-k seed literal survived: '+z)
if 'static const s2seed S[2]={' not in s or 'for(i=0;i<2;i++)' not in s:
    raise SystemExit('moderate-k seed table postcondition failed')
p.write_text(s)
print('C10_65S4D_MODERATE_K_SEED_WIDTH_PATCH_APPLIED',','.join(f(x) for x in ks),f(t['execution']['retry_width_Mpc']))
