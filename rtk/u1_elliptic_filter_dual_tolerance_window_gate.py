#!/usr/bin/env python3
"""Exact two-scale tolerance window for the elliptic U(1) matter compensator.

For a_eff(k)=k^2/(M_c^2+k^2), require simultaneously
  a_eff(k_cos) <= eps_cos              (cosmological A-source suppression)
  1-a_eff(k_local) <= eps_local       (local recovery of the parent matter source)
with 0<eps_cos,eps_local<1 and k_local>k_cos>0.

No value of M_c is selected.  The gate derives the exact existence condition.
"""
import json
import sympy as sp

M2,qc,ql,ec,el=sp.symbols('M_c_squared q_cos q_local eps_cos eps_local', positive=True, finite=True)
# Exact lower and upper bounds obtained by rearranging the two inequalities.
lower=sp.factor((1-ec)/ec*qc)
upper=sp.factor(el/(1-el)*ql)
ratio_q=sp.factor((1-ec)*(1-el)/(ec*el))
ratio_k=sp.sqrt(ratio_q)

# Check the familiar symmetric 1% case.
sym_ratio=sp.simplify(ratio_k.subs({ec:sp.Rational(1,100),el:sp.Rational(1,100)}))
assert sym_ratio==99
# 1% cosmological suppression plus 1e-5 local recovery target.
strict_ratio=sp.simplify(ratio_k.subs({ec:sp.Rational(1,100),el:sp.Rational(1,100000)}))
assert strict_ratio==sp.sqrt(sp.Integer(9899901))

out={
  'classification':'RTK_U1_ELLIPTIC_FILTER_DUAL_TOLERANCE_WINDOW_PASS',
  'status_scope':'GREEN_EXACT_SYMBOLIC_SCALE_WINDOW_PHYSICAL_LOCAL_TOLERANCE_MAPPING_PENDING',
  'filter':'a_eff(k)=k^2/(M_c^2+k^2)',
  'requirements':['a_eff(k_cos)<=eps_cos','1-a_eff(k_local)<=eps_local'],
  'Mc2_lower':'M_c^2 >= [(1-eps_cos)/eps_cos] k_cos^2',
  'Mc2_upper':'M_c^2 <= [eps_local/(1-eps_local)] k_local^2',
  'window_exists_iff':'k_local/k_cos >= sqrt[(1-eps_cos)(1-eps_local)/(eps_cos eps_local)]',
  'symmetric_1pct_check':'eps_cos=eps_local=0.01 -> k_local/k_cos>=99',
  'illustrative_strict_local_check':'eps_cos=0.01, eps_local=1e-5 -> k_local/k_cos>=sqrt(9899901) ~= 3146.4',
  'interpretation':'The compensator can suppress the homogeneous/large-scale A source while recovering the parent local matter coupling to an independently chosen tolerance whenever the physical scale hierarchy exceeds the exact bound. This applies to both the current nonprojectable branch and the projectable C9-escape candidate.',
  'non_claims':[
    'does not identify eps_local=1e-5 with a measured PPN bound without a same-action transfer calculation',
    'does not choose M_c',
    'does not specify k_cos or k_local numerically',
    'does not prove the full finite-k cosmological perturbation equations are observationally viable'
  ],
  'next_gate':'for the projectable branch, derive the same-action local PPN source-transfer correction as a function of 1-a_eff and map observational alpha/gamma/beta tolerances onto eps_local; for cosmology define the largest k_cos over which A-source suppression is required.'
}
open('u1_elliptic_filter_dual_tolerance_window_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
