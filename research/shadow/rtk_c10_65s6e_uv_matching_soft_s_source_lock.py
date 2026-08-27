#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
import sympy as sp

ROOT=Path(__file__).resolve().parents[2]
def load(p): return json.loads((ROOT/p).read_text())

def main():
    target=load('research/theory_targets/RTK_C10_65S6E_UV_MATCHING_SOFT_S_SOURCE_LOCK_TARGET_v1.json')
    parent=load('research/theory_results/RTK_C10_65S6D_K003_PRODUCTION_ARCHITECTURE_DECISION_RESULT_v1.json')
    assert target['status']=='FROZEN_BEFORE_IMPLEMENTATION'
    assert target['threshold_changed'] is False

    q1,q2,q3,k=sp.symbols('q1 q2 q3 k', positive=True)
    s=q1+q2+q3
    p2=q1*q2+q1*q3+q2*q3
    kernel=16*(s**3-7*s*p2+12*q1*q2*q3)
    soft=sp.expand(kernel.subs({q1:k**2,q2:k**2,q3:0}))
    soft_ratio=sp.simplify(soft/k**6)

    H,MU,MK,K,ca,x=sp.symbols('H M_U M_K K c_a x', positive=True)
    # Exact fixed-lapse soft-spatial s-channel expression from the archived corrected RTK theorem.
    def soft_amp(kv):
        Z=1+kv**2/MK**2
        N=1+kv**4/MU**4
        D=1+2*kv**4/(MU**4+kv**4)-kv**2/(MK**2+kv**2)
        return -9*H**2*kv**10*sp.sqrt(Z)/(128*sp.pi*K*MU**8*ca*N**sp.Rational(5,2)*D)

    amp=soft_amp(k)
    # Intermediate hierarchy MU << k << MK: first remove MK effects, then k/MU -> infinity.
    amp_MKinf=sp.limit(amp,MK,sp.oo)
    inter=sp.simplify(sp.limit(amp_MKinf.subs(k,x*MU),x,sp.oo))
    inter_expected=-3*H**2*MU**2/(128*sp.pi*K*ca)
    # Deep hierarchy k >> MU,MK: scale k=x with fixed positive scales and divide by k.
    deep_per_k=sp.simplify(sp.limit((amp/k).subs(k,x),x,sp.oo))
    deep_expected=-9*H**2*MU**2/(256*sp.pi*K*ca*MK)

    checks={
      's6d_parent_pass': parent['classification']==target['parents']['C10.65s6d'],
      's6d_production_k003_allowed_false': parent.get('production_k003_allowed') is False,
      'K3_s_exact': sp.simplify(soft_ratio-target['frozen_theorem']['expected_K3_s_over_k6'])==0,
      'intermediate_soft_s_limit_exact': sp.simplify(inter-inter_expected)==0,
      'deep_soft_s_limit_exact': sp.simplify(deep_per_k-deep_expected)==0,
      'no_numeric_M_U_selected': True,
      'no_eta_D_C_S_mapping_claimed': True,
      'threshold_changed': False
    }
    passed=checks['threshold_changed'] is False and all(v for q,v in checks.items() if q!='threshold_changed')
    out={
      'schema':'RTK_C10_65S6E_UV_MATCHING_SOFT_S_SOURCE_LOCK_RESULT_v1',
      'gate':'C10.65s6e',
      'classification':target['pass_classification'] if passed else target['fail_classification'],
      'target':'research/theory_targets/RTK_C10_65S6E_UV_MATCHING_SOFT_S_SOURCE_LOCK_TARGET_v1.json',
      'checks':checks,
      'derived':{
        'K3_s':str(soft),
        'K3_s_over_k6':str(soft_ratio),
        'intermediate_soft_s_limit':str(inter),
        'deep_soft_s_limit_per_k':str(deep_per_k)
      },
      'archived_rtk_source':target['archived_rtk_source'],
      'decision':target['decision_if_pass'] if passed else 'DO_NOT_USE_THIS_GATE_FOR_K003_PRODUCTION',
      'interpretation':'The corrected bare n=2 intrinsic-curvature theorem is independently reproduced at its decisive soft-spatial s-channel. Because the bare q_s=0 cubic vertex is nonzero and becomes marginal/growing rather than automatically UV-soft, this carrier cannot presently be promoted into the missing k=0.03 pre-EFT matching coefficients. Full cubic lapse/shift reduction and the state-dependent coefficient perturbation are required first.' if passed else 'The frozen symbolic source-lock did not reproduce the archived corrected theorem; diagnose before any UV matching or k=0.03 production.',
      'next_gate':target['next_if_pass'] if passed else 'Diagnose C10.65s6e without changing the frozen symbolic theorem.',
      'non_claims':target['non_claims'],
      'threshold_changed':False
    }
    rp=ROOT/'research/theory_results/RTK_C10_65S6E_UV_MATCHING_SOFT_S_SOURCE_LOCK_RESULT_v1.json'
    rp.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    cp=ROOT/'research/checkpoints/RTK_C10_65S6E_UV_MATCHING_SOFT_S_SOURCE_LOCK.md'
    cp.write_text(
      '# RTK C10.65s6e UV matching soft-s source-lock\n\n'
      f"Classification: `{out['classification']}`.\n\n"
      f"Decision: `{out['decision']}`.\n\n"
      f"Recovered exact soft-spatial cubic vertex: `K3_s={soft}`.\n\n"
      f"Intermediate limit: `{inter}`. Deep limit per k: `{deep_per_k}`.\n\n"
      'No numerical M_U is selected and no eta_D/eta_C/eta_S mapping is inferred. k=0.03 production remains blocked pending the full cubic lapse/shift constraint reduction.\n'
    )
    print(out['classification'])
    print(json.dumps(out['derived'],sort_keys=True))
    raise SystemExit(0 if passed else 2)

if __name__=='__main__': main()
