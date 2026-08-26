#!/usr/bin/env python3
from __future__ import annotations
import json, math, pathlib, sys
P=pathlib.Path

def L(path):
    return json.load(open(path))

def rel(a,b):
    a=float(a); b=float(b)
    return abs(a-b)/max(abs(a),abs(b),1e-300)

def main():
    t=L('research/theory_targets/RTK_C10_65S2F_IMPLICIT_CONDITIONING_AUDIT_TARGET_v1.json')
    e=L('research/theory_results/RTK_C10_65S2E_CURRENT_STATE_DERIVATIVE_SLIP_CLOSURE_RESULT_v1.json')
    n=L('research/theory_results/RTK_C10_65N_CONDITIONAL_COMPLETED_U1_ONSET_SEED_PREFLIGHT_RESULT_v1.json')
    assert t['status']=='FROZEN_BEFORE_IMPLEMENTATION'
    assert e['classification']=='C10_65S2E_CURRENT_STATE_DERIVATIVE_SLIP_CLOSURE_FAIL_SCOPED'
    assert t['failed_parent_is_not_reclassified'] is True

    bg=n['background']
    a=float(bg['a']); H=float(bg['H'])
    rb=float(bg['rhob']); rg=float(bg['rhog']); ru=float(bg['rhour'])
    rk=float(bg['rho_khr']); pk=float(bg['p_khr'])
    Wg=(4.0/3.0)*rg; Wu=(4.0/3.0)*ru
    W0=rb+Wg+Wu; Wk=rk+pk; W=W0+Wk
    W0_over_W=W0/W; Wk_over_W=Wk/W

    rows=[]
    max_c_rel=0.0; max_den_rel=0.0; max_amp=0.0
    min_den=float('inf'); max_den=0.0; finite_all=True
    smallest_k_rel=0.0
    for r in e['records']:
        lam=float(r['lambda_HL']); k=float(r['k']); k2=k*k
        D=3.0*lam-1.0; rr=lam-1.0; Lk=-k2; Xt=3.0*a*a*W
        A11=rr*2.0*Lk-2.0*D*H*H
        A12=-D*H*Xt
        A21=D*H
        A22=rr*Lk+Xt
        det=A11*A22-A12*A21
        c_analytic=((A11+D*D*H*H)/det)*(3.0*a*a*Wk)
        den_analytic=1.0-c_analytic
        c_dual=float(r['dynamic']['Bprime_affine_coefficient'])
        den_dual=float(r['dynamic']['Bprime_implicit_denominator'])
        amp=1.0/abs(den_analytic)
        ec=rel(c_dual,c_analytic); ed=rel(den_dual,den_analytic)
        max_c_rel=max(max_c_rel,ec); max_den_rel=max(max_den_rel,ed)
        max_amp=max(max_amp,amp); min_den=min(min_den,abs(den_analytic)); max_den=max(max_den,abs(den_analytic))
        if abs(k-1e-5) <= 1e-16:
            smallest_k_rel=max(smallest_k_rel,rel(den_analytic,W0_over_W))
        vals=[A11,A12,A21,A22,det,c_analytic,den_analytic,c_dual,den_dual,amp]
        finite_all &= all(math.isfinite(x) for x in vals)
        rows.append({
            'lambda_HL':lam,'M_c_Mpc_inv':float(r['M_c_Mpc_inv']),'k':k,
            'cB_dual':c_dual,'cB_analytic':c_analytic,
            'dual_vs_analytic_cB_relative':ec,
            'denominator_dual':den_dual,'denominator_analytic':den_analytic,
            'dual_vs_analytic_denominator_relative':ed,
            'amplification':amp,'detA':det
        })

    den_spread=(max_den-min_den)/max(max_den,min_den,1e-300)
    fc=t['frozen_checks']
    noncond=all(v for k,v in e['checks'].items() if k!='Bprime_implicit_denominator')
    checks={
        'record_count':len(rows)==int(fc['record_count']),
        'dual_vs_analytic_cB':max_c_rel<=float(fc['max_dual_vs_analytic_cB_relative']),
        'dual_vs_analytic_denominator':max_den_rel<=float(fc['max_dual_vs_analytic_denominator_relative']),
        'smallest_k_enthalpy_limit':smallest_k_rel<=float(fc['max_smallest_k_denominator_vs_W0_over_W_relative']),
        'scalar_implicit_amplification':max_amp<=float(fc['max_scalar_implicit_amplification']),
        'implicit_denominator':min_den>=float(fc['min_abs_implicit_denominator']),
        'denominator_grid_spread':den_spread<=float(fc['max_denominator_relative_spread_over_grid']),
        's2e_nonconditioning_checks':bool(noncond)==bool(fc['s2e_all_nonconditioning_checks_must_have_passed']),
        's2e_threshold_unchanged':(e.get('provenance',{}).get('threshold_changed') is False)==bool(fc['s2e_threshold_changed_must_be_false']),
        'finite':finite_all==bool(fc['all_values_finite'])
    }
    passed=all(checks.values())
    out={
        'schema':'RTK_C10_65S2F_IMPLICIT_CONDITIONING_AUDIT_RESULT_v1',
        'gate':'C10.65s2f',
        'classification':t['pass_classification'] if passed else t['fail_classification'],
        'target':'research/theory_targets/RTK_C10_65S2F_IMPLICIT_CONDITIONING_AUDIT_TARGET_v1.json',
        'failed_parent_classification_preserved':e['classification'],
        'checks':checks,
        'background_enthalpy_fractions':{'W0_over_W':W0_over_W,'Wk_over_W':Wk_over_W,'sum':W0_over_W+Wk_over_W},
        'global':{
            'max_dual_vs_analytic_cB_relative':max_c_rel,
            'max_dual_vs_analytic_denominator_relative':max_den_rel,
            'max_smallest_k_denominator_vs_W0_over_W_relative':smallest_k_rel,
            'min_abs_implicit_denominator':min_den,
            'max_abs_implicit_denominator':max_den,
            'max_scalar_implicit_amplification':max_amp,
            'denominator_relative_spread_over_grid':den_spread
        },
        'interpretation':'C10.65s2e remains FAIL because its >0.9 guard was frozen and violated. This audit only asks whether the observed feedback is the exact DAE enthalpy-fraction coupling and is separately well-conditioned under the new pre-frozen criterion.',
        'records':rows,
        'threshold_changed':False,
        'next':t['next_if_pass'] if passed else 'Do not proceed to production; resolve implicit-conditioning mismatch.',
        'non_claims':t['non_claims']
    }
    P('research/theory_results/RTK_C10_65S2F_IMPLICIT_CONDITIONING_AUDIT_RESULT_v1.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(out['classification'])
    print(json.dumps(out['global'],sort_keys=True))
    return 0 if passed else 2

if __name__=='__main__':
    sys.exit(main())
