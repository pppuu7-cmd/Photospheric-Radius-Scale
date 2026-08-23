#!/usr/bin/env python3
"""Exact symbolic compatibility of 1% cosmological compensation and O(3) alpha1.

For the finite-Mc projectable branch
  f(k)=k^2/(M_c^2+k^2),
  alpha1(k)=8 M_c^2/k^2.
The previously frozen exact 1% scale-separation requirement is
  M_c^2 >= 99 k_cos^2.
If an observable at a declared Fourier scale k_loc constrains
  |alpha1(k_loc)| <= eps1,
then
  M_c^2 <= eps1 k_loc^2/8.
Thus a nonempty symbolic interval exists iff
  k_loc/k_cos >= sqrt(792/eps1).

This is a scale-space theorem only.  It does not identify one experimental
baseline r with k_loc=1/r; source-specific real-space mapping is a separate gate.
"""
import json
import sympy as sp
M2,kc,kl,eps=sp.symbols('M_c_squared k_cos k_local epsilon_1', positive=True, finite=True)
lower=99*kc**2
upper=eps*kl**2/8
ratio_req=sp.sqrt(sp.Rational(792,1)/eps)
assert sp.simplify((upper-lower).subs(kl,ratio_req*kc))==0
# Equivalent dimensionless condition.
R=sp.symbols('R', positive=True, finite=True)
expr=sp.factor((upper-lower).subs(kl,R*kc)/kc**2)
assert sp.simplify(expr-(eps*R**2/8-99))==0

illustrative={}
for e in [1e-4,1e-5,6e-6,1e-6]:
    illustrative[f'{e:.0e}']=float((792.0/e)**0.5)

out={
 'classification':'RTK_C9_PROJECTABLE_U1_ALPHA1_COSMOLOGY_SYMBOLIC_WINDOW_PASS',
 'status_scope':'GREEN_EXACT_SYMBOLIC_SCALE_WINDOW_SOURCE_SPECIFIC_EXPERIMENT_MAPPING_PENDING',
 'inputs':['1% cosmological compensation: M_c^2>=99 k_cos^2','finite-Mc moving O3: alpha1(k)=8 M_c^2/k^2','declared local Fourier constraint |alpha1(k_local)|<=epsilon_1'],
 'window':'99 k_cos^2 <= M_c^2 <= epsilon_1 k_local^2/8',
 'existence_iff':'k_local/k_cos >= sqrt(792/epsilon_1)',
 'illustrative_ratio_thresholds_not_adopted_constraints':illustrative,
 'interpretation':'Preferred-frame alpha1 strengthens the required hierarchy beyond the bare 99:1 compensation separation. The theorem is exact once a Fourier-scale alpha1 observable is declared, but real experiments generally have source/baseline form factors and must not be reduced to k=1/r by fiat.',
 'non_claims':['does not choose epsilon_1','does not choose k_local or k_cos','does not identify pulsar strong-field alpha1 with this weak-field kernel','does not replace the real-space Yukawa/source-profile calculation','does not address alpha2 until O4 generalized kernels are solved'],
 'next_gate':'for each concrete weak-field experiment, build its source/measurement transfer function and project the scale-dependent O3 shift response onto that observable; only then intersect the resulting M_c interval with the cosmological lower bound.'
}
open('c9_projectable_u1_alpha1_cosmology_symbolic_window_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
