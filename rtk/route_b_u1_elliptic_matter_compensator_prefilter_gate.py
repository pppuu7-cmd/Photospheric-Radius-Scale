#!/usr/bin/env python3
"""Prefilter for a scale-separated, nonpropagating U1 matter compensator.

Motivation
----------
A coordinate-only clock source F_Sigma(Sigma) can cancel the homogeneous
ordinary-matter A source but cannot track arbitrary independent delta rho_H.
A compensator that directly sees the canonical matter state is needed, while
we also want to avoid changing the local/solar-system family-I coupling.

Hamiltonian-level auxiliary ansatz (neutral Q, Lambda):

  H_aux contains  sigma Q + Lambda [ L Q - rho_H ],
  L = 1 - D^2/M_c^2.

Signs are chosen so that, on the sigma=0 branch, variation of Lambda gives
L Q=rho_H and the sigma Q term contributes an A source opposite to ordinary
family-I matter.  In Fourier space on a regular spatial slice,

  L(y)=1+y/M_c^2 > 0,  y=k_phys^2 >= 0,
  Q/rho_H = 1/L(y).

Thus Q=rho_H exactly at k=0, whereas Q/rho_H -> 0 as k->infinity.  Q and Lambda
have no time derivatives. Their primary momenta and two elliptic secondary
constraints form an invertible four-second-class auxiliary block whenever
L(y)>0, so the auxiliary pair carries no propagating DOF in this scoped sector.

This is a prefilter, not a full U1 completion: the complete gravity+matter+
RTK+auxiliary Dirac matrix, cosmological perturbations, PPN and radiative
stability must still be recomputed on one frozen action.
"""
import json
import sympy as sp

y, Mc = sp.symbols('y M_c', positive=True, finite=True, real=True)
L = 1 + y/Mc**2
f = sp.simplify(1/L)
assert sp.simplify(f.subs(y,0)-1)==0
assert sp.limit(f,y,sp.oo)==0
assert sp.simplify(sp.diff(f,y)) < 0

# Auxiliary canonical rank. Constraints ordered as p_Q,p_Lambda,C_Q,C_Lambda,
# with the nonzero canonical cross brackets represented by L. Overall signs do
# not affect rank. The antisymmetric 4x4 matrix has det=L^4.
ell = sp.symbols('ell', positive=True, finite=True, real=True)
M = sp.Matrix([
    [0,0,0,-ell],
    [0,0,-ell,0],
    [0,ell,0,0],
    [ell,0,0,0],
])
detM = sp.factor(M.det())
assert detM == ell**4
assert sp.simplify(detM.subs(ell,L)) > 0

# Preregistered 1% scale-separation window. Demand compensation fraction
# f(k_cos)>=0.99 and f(k_local)<=0.01. This gives
# Mc >= sqrt(99) k_cos and Mc <= k_local/sqrt(99), hence a nonempty interval
# iff k_local/k_cos >= 99.  Use exact rationals so no branch assumptions on a
# generic epsilon are hidden inside symbolic square-root simplification.
kcos, klocal = sp.symbols('k_cos k_local', positive=True, finite=True, real=True)
eps1 = sp.Rational(1,100)
Mc_min_1pct = sp.sqrt(99)*kcos
Mc_max_1pct = klocal/sp.sqrt(99)
ratio_1pct = sp.simplify((Mc_min_1pct/kcos)/(Mc_max_1pct/klocal))
assert ratio_1pct == 99
fcos_boundary = sp.simplify(1/(1+(kcos/Mc_min_1pct)**2))
flocal_boundary = sp.simplify(1/(1+(klocal/Mc_max_1pct)**2))
assert fcos_boundary == 1-eps1
assert flocal_boundary == eps1

out={
  'classification':'RTK_ROUTE_B_U1_ELLIPTIC_MATTER_COMPENSATOR_PREFILTER_PASS',
  'status_scope':'YELLOW_CONSTRUCTIVE_SCALE_SEPARATED_A_SOURCE_RESCUE_FULL_DIRAC_AND_OBSERVABLES_PENDING',
  'candidate':{
    'representation':'Hamiltonian-level neutral auxiliary pair Q,Lambda',
    'constraint':'(1-D^2/M_c^2) Q = rho_H',
    'A_source_term':'sigma Q with sign opposite to ordinary family-I A source',
    'fourier_filter':'Q/rho_H = 1/(1+k_phys^2/M_c^2)'
  },
  'exact_results':{
    'FLRW_k0':'Q=rho_H exactly, so homogeneous A-source cancellation is possible',
    'high_k':'Q/rho_H -> 0, so the compensator decouples from sufficiently short-wavelength/local sources',
    'elliptic_operator':'L(y)=1+y/M_c^2 > 0 for M_c^2>0 and y>=0',
    'auxiliary_constraint_matrix_det':'L(y)^4 > 0',
    'auxiliary_physical_dof':'0 in the isolated Q,Lambda sector because four auxiliary phase-space dimensions are removed by four second-class constraints'
  },
  'one_percent_window':{
    'cosmological_requirement':'M_c >= k_cos*sqrt(99) gives Q/rho >= 0.99 at k_cos',
    'local_requirement':'M_c <= k_local/sqrt(99) gives Q/rho <= 0.01 at k_local',
    'existence_condition':'k_local/k_cos >= 99'
  },
  'why_it_evades_coordinate_only_obstruction':'Q is constrained by the independent matter state rho_H rather than by Sigma alone, so delta Q can track an independent delta rho_H. The spatial filter allows this tracking to switch off continuously toward local/high-k physics.',
  'why_it_is_not_equivalent_to_a1_zero_everywhere':'The cancellation fraction is scale dependent: exactly one at k=0 but tends to zero at high k. Integrating out Q produces spatially nonlocal filtering, while the local auxiliary representation remains elliptic and contains no time kinetic term.',
  'non_claims':[
    'does not yet prove the full gravity+matter+RTK+Q+Lambda Dirac matrix has exactly 3 physical DOF',
    'does not prove the desired cosmological perturbation transfer functions across finite k',
    'does not establish PPN/equivalence-principle bounds for finite M_c',
    'does not establish radiative protection or a UV completion',
    'rho_H must be implemented in a precise canonical matter representation; this gate assumes the existing a2=0 Hamiltonian matter generator rather than an ad hoc velocity-dependent Lagrangian density'
  ],
  'next_gate':'freeze a canonical action for the Q,Lambda auxiliary pair using the a2=0 matter Hamiltonian generator; derive the full primary/secondary constraint matrix and prove the auxiliary four-second-class block remains independent after coupling. Then derive the finite-k A-constraint transfer function and identify an M_c window that preserves production cosmological modes while suppressing local PPN contamination.'
}
with open('u1_elliptic_matter_compensator_prefilter_result.json','w') as f:
    json.dump(out,f,indent=2,sort_keys=True); f.write('\n')
print(out['classification'],json.dumps(out,sort_keys=True))
