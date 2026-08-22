#!/usr/bin/env python3
"""Symbolic compatibility window for filtered-matter low-k rank and scale rescue.

No value of M_c is selected here.

Previously established inputs:
  * after neutral RTK, the leading low-k baseline is
      B_R=[[A,-b],[b,0]], A=a2+r2, b!=0;
  * projected filtered-matter corrections have to be derived from
      a_eff=1-L^{-1} ~ |k|^2/M_c^2
    and delta a_eff=-(1/M_c^2)L^{-1}delta(D^2)L^{-1};
  * once their leading scaled matrix is written E_m=K/M_c^2, singular-value
    perturbation theory is sufficient if
      ||K||_2/M_c^2 < sigma_min(B_R).

Define C_m >= ||K||_2 and R_rank=C_m/sigma_min(B_R), which has units M_c^2.
Then rank is guaranteed by M_c^2>R_rank.

The already frozen 1% source-separation requirements are
  M_c^2 >= 99 k_cos^2,
  M_c^2 <= k_local^2/99.

Therefore an M_c satisfying all three conditions exists iff
  k_local/k_cos >= 99
and
  R_rank < k_local^2/99.
Equivalently, the admissible symbolic interval is
  max(99 k_cos^2, R_rank) <~ M_c^2 <= k_local^2/99,
where the R_rank lower edge is strict while the cosmological edge is inclusive.

This theorem does not provide C_m; deriving/bounding C_m from the frozen action
is the next physical gate.
"""
import json
import sympy as sp

A,b,Cm,sigma,kcos,klocal,Mc2=sp.symbols(
    'A b C_m sigma_min k_cos k_local M_c_squared', positive=True, finite=True
)

# Baseline determinant and Gram invariants.
BR=sp.Matrix([[A,-b],[b,0]])
Gram=sp.expand(BR.T*BR)
assert sp.simplify(BR.det()-b**2)==0
assert sp.simplify(sp.trace(Gram)-(A**2+2*b**2))==0
assert sp.simplify(Gram.det()-b**4)==0

# Smaller singular value squared for real A,b; A is taken positive as a
# representative magnitude. The output states |A| for the unrestricted case.
smin2=sp.simplify((A**2+2*b**2-A*sp.sqrt(A**2+4*b**2))/2)
# Rationalized form is manifestly positive for b>0.
smin2_rat=sp.simplify(2*b**4/(A**2+2*b**2+A*sp.sqrt(A**2+4*b**2)))
assert sp.simplify(smin2-smin2_rat)==0

Rrank=sp.simplify(Cm/sigma)
Lcos=sp.simplify(99*kcos**2)
Ulocal=sp.simplify(klocal**2/99)
# Exact algebraic equivalence of the pure scale-window condition.
ratio_condition=sp.simplify(Ulocal-Lcos)
assert sp.factor(ratio_condition)==(klocal-99*kcos)*(klocal+99*kcos)/99

# Entrywise optional bound: if |K_ij|<=kappa, ||K||2<=||K||F<=2 kappa.
kappa=sp.symbols('kappa', positive=True, finite=True)
R_entry=sp.simplify(2*kappa/sigma)

out={
  'classification':'RTK_ROUTE_B_U1_FILTERED_MATTER_RANK_WINDOW_PASS',
  'status_scope':'GREEN_SYMBOLIC_COMPATIBILITY_WINDOW_ACTION_DERIVED_C_M_PENDING',
  'baseline_after_neutral_RTK':'B_R=[[A,-b2],[b2,0]], A=a2+r2, b2!=0',
  'baseline_determinant':'det B_R=b2^2',
  'sigma_min_squared':'((A)^2+2 b2^2-|A| sqrt(A^2+4 b2^2))/2',
  'sigma_min_squared_positive_form':'2 b2^4/(A^2+2 b2^2+|A| sqrt(A^2+4 b2^2))',
  'filtered_matter_parameterization':'E_m=K/M_c^2 at leading |k|^2 order, with C_m >= ||K||_2',
  'rank_sufficient_condition':'M_c^2 > R_rank := C_m/sigma_min(B_R)',
  'entrywise_version':'if |K_ij|<=kappa then M_c^2 > 2 kappa/sigma_min(B_R) is sufficient',
  'one_percent_cosmological_rescue':'M_c^2 >= 99 k_cos^2',
  'one_percent_local_recovery':'M_c^2 <= k_local^2/99',
  'combined_window':'M_c^2 must lie above both 99 k_cos^2 (inclusive) and R_rank (strict), and at or below k_local^2/99',
  'existence_iff':[
    'k_local/k_cos >= 99',
    'R_rank < k_local^2/99'
  ],
  'interpretation':'The classical low-k rank requirement can be combined with the previously frozen 1% scale-separation requirements before fitting M_c. Once an action-derived C_m bound is known, the architecture either has a nonempty symbolic M_c window or is rejected without a numerical parameter scan.',
  'non_claims':[
    'does not derive C_m or K from the action',
    'does not choose, fit, or tune M_c',
    'does not certify intermediate/high-k rank',
    'does not replace PPN, GW, cutoff, compact-object, or C9 naturalness gates'
  ],
  'next_gate':'derive the leading filtered-matter K entries or a rigorous C_m bound from Jhat=Jg-a_eff H0 and delta a_eff=-(1/M_c^2)L^{-1}delta(D^2)L^{-1}; then evaluate the symbolic existence conditions without selecting M_c.'
}
with open('u1_filtered_matter_rank_window_result.json','w') as f:
    json.dump(out,f,indent=2,sort_keys=True); f.write('\n')
print(out['classification'],json.dumps(out,sort_keys=True))
