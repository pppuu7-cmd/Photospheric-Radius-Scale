#!/usr/bin/env python3
"""Conditional exact leading-rank theorem for antisymmetric filtered matter.

This theorem is purely algebraic and independent of whether the physical k22
suppression gate passes.  It may be applied only when the leading low-k matrix
has already been established to be

    B_RTK = [[A,-b],[b,0]], b!=0,
    Delta B_m = (1/M_c^2) [[0,-x],[x,0]].

Then

    det(B_RTK+Delta B_m) = (b+x/M_c^2)^2.

Thus the RTK e11 coefficient A drops out of the leading determinant exactly.
For M_c^2>0:
  * if b*x >= 0, there is no positive rank-loss root;
  * if b*x < 0, the unique positive root is M_c^2=-x/b=|x|/|b|.
A conservative root-avoiding sufficient condition is

    M_c^2 > |x|/|b|.

Intersecting with the frozen 1% scale window gives

    max(99 k_cos^2, |x|/|b|) <~ M_c^2 <= k_local^2/99,

with the rank lower bound strict and the cosmological lower bound inclusive.
A nonempty conservative window requires k_local/k_cos>=99 and
|x|/|b| < k_local^2/99.
"""
import json
import sympy as sp

A,b,x,M2=sp.symbols('A b x M_c_squared', real=True, finite=True, nonzero=True)
B=sp.Matrix([[A,-b],[b,0]])
K=sp.Matrix([[0,-x],[x,0]])
Bt=sp.simplify(B+K/M2)
detBt=sp.factor(Bt.det())
expected=sp.factor((b+x/M2)**2)
assert sp.simplify(detBt-expected)==0
assert sp.diff(detBt,A)==0

# Solve the unsquared off-diagonal cancellation; M2=-x/b is the only root.
root=sp.simplify(-x/b)
assert sp.simplify((b+x/M2).subs(M2,root))==0

# Conservative scale-window algebra with positive magnitudes.
xb,kcos,klocal=sp.symbols('x_over_b_abs k_cos k_local', positive=True, finite=True)
Lcos=99*kcos**2
Ulocal=klocal**2/99
assert sp.simplify(Ulocal-Lcos-(klocal-99*kcos)*(klocal+99*kcos)/99)==0

out={
  'classification':'RTK_ROUTE_B_U1_FILTERED_MATTER_ANTISYMMETRIC_LEADING_RANK_WINDOW_PASS',
  'status_scope':'GREEN_CONDITIONAL_EXACT_LEADING_ROOT_STRUCTURE_PHYSICAL_K22_GATE_REQUIRED',
  'applicability_condition':'apply only after physical leading K=[[0,-x],[x,0]] is established on the same background/domain',
  'baseline':'B_RTK=[[A,-b],[b,0]], b!=0',
  'filtered_leading':'Delta B_m=(1/M_c^2)[[0,-x],[x,0]]',
  'exact_determinant':'det B_lead=(b+x/M_c^2)^2',
  'A_independence':'the neutral-RTK e11/conditioning coefficient A cancels exactly from the leading determinant',
  'positive_root_classification':['if b*x>=0 there is no positive M_c^2 rank-loss root','if b*x<0 the unique positive rank-loss root is M_c^2=-x/b=|x|/|b|'],
  'conservative_rank_bound':'M_c^2>|x|/|b| is sufficient to exclude the unique cancellation root irrespective of the sign of x/b',
  'combined_conservative_window':'M_c^2 above both 99 k_cos^2 (inclusive) and |x|/|b| (strict), and M_c^2<=k_local^2/99',
  'combined_existence_conditions':['k_local/k_cos>=99','|x|/|b| < k_local^2/99'],
  'interpretation':'Once the physical leading filtered correction is antisymmetric, the low-k determinant problem collapses from a generic matrix-norm bound to one shifted off-diagonal coefficient. The exact leading rank-loss set is empty or a single positive M_c^2 point.',
  'non_claims':['does not establish physical k22=0 by itself','does not bound subleading O(k^4) terms','does not choose M_c','does not certify intermediate/high-k rank or local/GW/C9 viability'],
  'next_gate':'if the flat-FLRW k22 suppression theorem passes, substitute x=V(H0-tau_H), record the explicit conservative M_c window, and then derive a subleading remainder bound that supplies a finite punctured epsilon.'
}
with open('u1_filtered_matter_antisymmetric_leading_rank_window_result.json','w') as f:
    json.dump(out,f,indent=2,sort_keys=True); f.write('\n')
print(out['classification'],json.dumps(out,sort_keys=True))
