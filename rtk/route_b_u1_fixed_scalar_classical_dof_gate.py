#!/usr/bin/env python3
"""Scoped classical DOF recertification for the fully fixed RTK scalar action.

Fixed scalar sector:
  P(X_U) reconstructed from production rho,p,c_a^2,
  C(X_U)=M_Pl^2/(2X_U), X_U>0.

Prerequisite executable theorems are run by CI before this script:
  * fixed-C(X) velocity support: no new gravity/gauge time velocity;
  * invariant-shift Noether identity: nu equation remains the divergence of
    the shift equation for arbitrary L(v,Dv,neutral jets), including P(X),C(X);
  * neutral scalar cross-block support: only {pi_N,H_perp} can change;
  * regular timelike X>0 rank slice: det B is not identically zero;
  * fixed-C(X) homogeneous rolling rank: production branch is in the exact
    acceleration-operator class covered by the exceptional-U1 rank theorem.

With the exceptional eta1=eta2=0 gravity branch this leaves 2d+2 first-class
constraints and four second-class constraints. Adding one Sigma canonical pair
to the pure-gravity phase space therefore gives, in d=3, exactly three
physical DOF: two tensors and one intended RTK scalar.
"""
import json
import sympy as sp

d=sp.symbols('d', integer=True, positive=True)
dimP_gravity=d**2+3*d+6
dimP_fixed=sp.expand(dimP_gravity+2)
C1=2*d+2
C2=sp.Integer(4)
Ndof=sp.simplify((dimP_fixed-2*C1-C2)/2)
expected=sp.simplify(d*(d-1)/2)
assert sp.simplify(Ndof-expected)==0
assert Ndof.subs(d,3)==3
assert Ndof.subs(d,3)-2==1

out={
  'classification':'RTK_ROUTE_B_U1_FIXED_SCALAR_CLASSICAL_DOF_PASS',
  'fixed_scalar_action':'research/RTK_C8_U1_FIXED_SCALAR_ACTION_v1.json',
  'gravity_scope':'nonprojectable U1 exceptional sigma1=sigma2=0 branch',
  'domain':'generic regular timelike X_U>0 phase-space region plus the homogeneous rolling production branch',
  'phase_space_dimension':str(dimP_fixed),
  'first_class_constraints':str(C1),
  'second_class_constraints':4,
  'dof_formula':str(Ndof),
  'd3_total_dof':3,
  'd3_content':'2 tensor + 1 intended RTK/DBI scalar',
  'supersession_note':'This recertifies the fixed P(X_U), C(X_U)=M_Pl^2/(2X_U) action. The earlier DOF certificate remains historical for the pre-fixed coefficient treatment and must not be used alone for the fixed action.',
  'status_scope':'CLASSICAL_FIXED_ACTION_DOF_GREEN_X_POSITIVE',
  'non_claims':[
    'does not cover X_U=0 or prove compact-object continuation through that boundary',
    'does not exclude measure-zero inhomogeneous rank-changing hypersurfaces inside X_U>0 without a full functional determinant theorem',
    'does not establish radiative protection of sigma1=sigma2=0',
    'does not establish full moving-source PPN, UV tensor dispersion or strong-coupling cutoff'
  ],
  'next_gate':'complete same-action local static PPN decoupling and beta_PPN in the X_U>0 branch; then attack moving-source alpha1/alpha2 and the C9 radiative/cutoff gates'
}
open('u1_fixed_scalar_classical_dof_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
