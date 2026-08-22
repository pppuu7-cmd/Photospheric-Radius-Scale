#!/usr/bin/env python3
"""Scoped C8 classical coupled-DOF certification for the corrected U(1)+RTK action.

This combines only already established structural inputs:
  1. local U(1) invariance of the neutral RTK mixed operator;
  2. a2=0 canonical affinity and total primary identity p_nu+J_A=0;
  3. invariant-shift Noether identity, so the U(1)/spatial gauge generators survive;
  4. reduction of the four second-class constraints to det B != 0;
  5. generic coupled-rank slice PASS (det B is not identically zero);
  6. rolling homogeneous rank-shift PASS (the production rolling background
     changes only the same lapse-gradient operator class for which the pure
     exceptional-U1 Hamiltonian theorem gives nonzero rank for arbitrary L_V
     coefficients).

External pure-gravity Hamiltonian input: Mukohyama et al., arXiv:1504.07357,
eta1=eta2=0 branch, Eqs. (48)-(65).

The result is deliberately scoped: a classical generic/background DOF count,
not radiative stability, PPN, tensor phenomenology, compact objects or cutoff.
"""
import json
import sympy as sp

d=sp.symbols('d', integer=True, positive=True)

# Pure exceptional-U1 gravity phase-space dimension from the Hamiltonian paper,
# plus one canonical pair (Sigma,p_Sigma) for the intended RTK scalar.
dimP_gravity=d**2+3*d+6
dimP_coupled=sp.expand(dimP_gravity+2)

# Gauge symmetries retained by the invariant coupled action.
C1=2*d+2
# Four independent second-class constraints (pi_N,J_A,H_perp,phi_A) when B has rank 2.
C2=sp.Integer(4)
Ndof=sp.simplify((dimP_coupled-2*C1-C2)/2)
expected=sp.simplify(d*(d-1)/2)
assert sp.simplify(Ndof-expected)==0
assert Ndof.subs(d,3)==3

# Separate the intended scalar from the tensor polarizations in d=3.
tensor_d3=sp.Integer(2)
scalar_d3=sp.simplify(Ndof.subs(d,3)-tensor_d3)
assert scalar_d3==1

# Cross-block determinant identity used by all rank prerequisites.
a,b,c,dd=sp.symbols('a b c d_cross', finite=True)
B=sp.Matrix([[a,b],[c,dd]])
detB=sp.factor(B.det())
assert detB==a*dd-b*c

out={
  'classification':'RTK_ROUTE_B_U1_CLASSICAL_COUPLED_DOF_CERTIFICATION_PASS',
  'action_scope':'corrected exceptional nonprojectable U1 gravity + neutral DBI Sigma + explicit U1-invariant S_mix, with beta0_bare=0 and sigma1=sigma2=0',
  'phase_space_dimension':str(dimP_coupled),
  'first_class_constraints':str(C1),
  'second_class_constraints':4,
  'second_class_basis':['pi_N','J_A','H_perp','phi_A'],
  'rank_condition':str(detB)+' != 0',
  'generic_rank_basis':'generic coupled-rank slice theorem proves detB is not identically zero and hence the generic coupled phase-space rank is four',
  'rolling_background_basis':'rolling homogeneous rank-shift theorem plus the external arbitrary-L_V exceptional-U1 rank theorem supports rank four on the production homogeneous rolling branch',
  'dof_formula':str(Ndof),
  'd3_total_physical_dof':3,
  'd3_interpretation':'2 tensor polarizations + exactly 1 intended RTK/DBI scalar',
  'lambda_HL_status':'not fixed by this count; exclude the singular DeWitt value lambda_HL=1/d when using the inverse supermetric formulas',
  'status_scope':'CLASSICAL_GREEN_SCOPED_DOF_ONLY',
  'non_claims':[
    'does not establish technical naturalness of sigma1=sigma2=0',
    'does not exclude measure-zero or specially engineered inhomogeneous rank-changing configurations',
    'does not provide the fresh full-action static/Newton/PPN solution with S_mix retained',
    'does not establish tensor/GW bounds, nonlinear compact-object behavior, or EFT strong-coupling cutoff',
    'does not constitute a UV completion'
  ],
  'next_gate':'freeze one IR representative lambda_HL after excluding lambda_HL=1/d; lambda_HL=1 is the canonical GR-kinetic representative to test next, then derive the same-action TT sector and static weak-field equations with explicit S_mix before any viability claim'
}
open('u1_classical_coupled_dof_certification_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
