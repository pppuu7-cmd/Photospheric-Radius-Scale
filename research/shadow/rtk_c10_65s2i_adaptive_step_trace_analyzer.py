#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def L(p): return json.loads((ROOT/p).read_text())
def rel(a,b): return abs(a-b)/max(1.0,abs(a),abs(b))

def observer(path):
    out={}
    for line in Path(path).read_text().splitlines():
        p=line.split(',')
        if len(p)!=63: raise RuntimeError('bad observer shape')
        if p[0]=='AFTER': out[float(p[3])]=int(p[8])
    return out

def trace(path):
    groups={}; begins=[]; ends=[]
    for line in Path(path).read_text().splitlines():
        p=line.split(','); kind=p[0]; k=float(p[1])
        if kind=='BEGIN': begins.append(k); groups.setdefault(k,[])
        elif kind=='END': ends.append(k)
        elif kind=='ACCEPT':
            vals=[float(x) for x in p[2:7]]
            groups.setdefault(k,[]).append({'x0':vals[0],'x1':vals[1],'htry':vals[2],'hdid':vals[3],'hnext':vals[4],'rejected':int(p[7]),'errmax':float(p[8])})
        else: raise RuntimeError(kind)
    return groups,begins,ends

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--trace',required=True); ap.add_argument('--observer',required=True); ap.add_argument('--patch',required=True); ap.add_argument('--output',required=True); a=ap.parse_args()
    t=L('research/theory_targets/RTK_C10_65S2I_ADAPTIVE_STEP_TRACE_TARGET_v1.json')
    h=L('research/theory_results/RTK_C10_65S2H_PRODUCTION_CANARY_FAILURE_DIAGNOSIS_RESULT_v1.json')
    s2=L('research/theory_results/RTK_C10_65S2_DIRECT_ONSET_ONE_STEP_PRODUCTION_CANARY_RESULT_v1.json')
    assert t['status']=='FROZEN_BEFORE_TRACE_EXECUTION'; assert h['classification']=='C10_65S2H_FAILURE_DIAGNOSIS_PASS_SCOPED'; assert s2['classification']=='C10_65S2_DIRECT_ONSET_ONE_STEP_PRODUCTION_CANARY_FAIL_SCOPED'
    G,beg,end=trace(a.trace); O=observer(a.observer); ks=[float(x) for x in t['frozen_execution']['k_Mpc_inv']]; dt=float(t['frozen_execution']['short_step_delta_tau_Mpc'])
    checks={}
    checks['four_begin_and_four_end_markers']=sorted(beg)==ks and sorted(end)==ks
    records=[]; allfinite=True; positive=True; multi=True; widths=True; accounting=True; rejects=True
    for k in ks:
        q=G.get(k,[]); A=len(q); R=sum(x['rejected'] for x in q); T=A+R
        finite=all(math.isfinite(v) for x in q for v in (x['x0'],x['x1'],x['htry'],x['hdid'],x['hnext'],x['errmax']))
        allfinite &= finite; positive &= A>0 and all(x['hdid']>0 for x in q); multi &= A>1; rejects &= all(x['rejected']>=0 for x in q)
        total=sum(x['hdid'] for x in q); widths &= rel(total,dt)<=float(t['frozen_checks']['sum_hdid_matches_1e-4_relative_tolerance'])
        expected=A+5*T+1; accounting &= O.get(k)==expected
        records.append({'k':k,'accepted_substeps':A,'rejected_trials':R,'rkck_trials':T,'observer_rhs_calls':O.get(k),'accounting_rhs_calls':expected,'sum_hdid':total,'first_accepted_hdid':q[0]['hdid'] if q else None,'minimum_hdid':min((x['hdid'] for x in q),default=None),'maximum_hdid':max((x['hdid'] for x in q),default=None),'accepted_steps':q})
    checks.update({'all_trace_values_finite':allfinite,'accepted_hdid_positive':positive,'accepted_steps_per_anchor_greater_than_one':multi,'sum_hdid_matches_1e-4':widths,'trace_rhs_accounting_matches_observer_exactly':accounting,'all_rejection_counts_nonnegative':rejects})
    txt=Path(a.patch).read_text(); checks['no_physics_or_tolerance_mutation_static_guard']=all(x in txt for x in ['diagnostics only','no integration mutation','rtk_c10_65s2i_trace_begin','rtk_c10_65s2i_trace_end']) and not any(x in txt for x in ['tol_perturb_integration =','ppr->tol_perturb_integration =','dy[','y['])
    checks['first_production_rhs_bound_inherited']=s2['max_first_production_rhs_relative'] < 5e-9
    checks['retry_width_selected']=False
    checks['threshold_changed']=False
    passed=all(v is True for k,v in checks.items() if k not in ('retry_width_selected','threshold_changed')) and checks['retry_width_selected'] is False and checks['threshold_changed'] is False
    first=[r['first_accepted_hdid'] for r in records if r['first_accepted_hdid'] is not None]
    out={'schema':'RTK_C10_65S2I_ADAPTIVE_STEP_TRACE_RESULT_v1','gate':'C10.65s2i','classification':t['pass_classification'] if passed else t['fail_classification'],'checks':checks,'records':records,'global':{'minimum_first_accepted_hdid':min(first) if first else None,'maximum_first_accepted_hdid':max(first) if first else None,'total_accepted_substeps':sum(r['accepted_substeps'] for r in records),'total_rejected_trials':sum(r['rejected_trials'] for r in records)},'original_s2_classification_preserved':s2['classification'],'retry_width_selected':False,'threshold_changed':False,'next_gate':t['next_if_pass'] if passed else 'Repair trace instrumentation only; do not alter production physics, tolerance, or C10.65s2 classification.','non_claims':t['non_claims']}
    Path(a.output).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n'); print(out['classification']); print(json.dumps(out['global'],sort_keys=True)); return 0 if passed else 2
if __name__=='__main__': raise SystemExit(main())
