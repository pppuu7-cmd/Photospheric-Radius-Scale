#!/usr/bin/env python3
"""Projectable-U(1) compatibility triage for the RTK completion.

Goal: test whether projectability N=N(t) can structurally remove the C9
eta1/eta2 naturalness problem while retaining the intended RTK scalar rational
dispersion and the elliptic ordinary-matter compensator.

Primary literature background:
- Mukohyama et al., arXiv:1504.07357: projectable U(1) has no scalar graviton;
  N is not a local phase-space degree of freedom and the absence is protected
  at full order, unlike the tuned nonprojectable eta1=eta2=0 surface.
- Lin et al., arXiv:1310.6666: the universal A/prepotential matter coupling and
  PPN analysis cover both projectable and nonprojectable U(1) theories.

This gate is an action-compatibility theorem, not yet a full projectable coupled
Dirac/PPN/cosmology certification.
"""
import json
import sympy as sp

k,MK2,Akin,PX,C=sp.symbols('k M_K_squared Akin P_X C', positive=True, finite=True)
w2=sp.factor(PX*k**2/(Akin+2*C*k**2))
ca2=sp.factor(PX/Akin)
# Frozen RTK production identity 2C/Akin=1/MK^2.
w2_reduced=sp.factor(w2.subs(C,Akin/(2*MK2)))
expected=sp.factor(ca2*k**2/(1+k**2/MK2))
assert sp.simplify(w2_reduced-expected)==0

# Projectability: spatial lapse gradient vanishes identically.
dNi=sp.Integer(0)  # D_i N on N=N(t)
ai=dNi                  # proportional to D_i ln N
Da=sp.Integer(0)
eta1,eta2,sigma=sp.symbols('eta1 eta2 sigma', finite=True, real=True)
ct1=sp.simplify(eta1*ai**2*sigma)
ct2=sp.simplify(eta2*Da*sigma)
assert ct1==0 and ct2==0

# Elliptic matter compensator is purely spatial and does not require a local N.
q,Mc2,H0=sp.symbols('q M_c_squared H0', positive=True, finite=True)
ell=1+q/Mc2
Q=sp.factor(H0/ell)
JA=sp.factor(Q-H0)
assert sp.simplify(JA + H0*q/(Mc2+q))==0
assert sp.simplify(JA.subs(q,0))==0
# Isolated auxiliary second-class pair remains invertible for ell>0.
aux_det=sp.factor(ell**2)
assert aux_det>0

out={
  'classification':'RTK_C9_PROJECTABLE_U1_RTK_COMPATIBILITY_PASS',
  'status_scope':'GREEN_STRUCTURAL_C9_ESCAPE_CANDIDATE_FULL_PROJECTABLE_COUPLED_RECERTIFICATION_PENDING',
  'projectability':'N=N(t), hence D_i N=0 and a_i=D_i ln N=0 identically',
  'c9_counterterm_annihilation':{
    'eta1_a2_sigma':'0 identically on projectable configuration space',
    'eta2_Da_sigma':'0 identically on projectable configuration space'
  },
  'rtk_scalar_quadratic_kinetic':'(Akin/2) dot(pi)^2 + C (D_i dot(pi))^2',
  'rtk_dispersion_exact':'omega^2=c_a^2 k^2/(1+k^2/M_K^2)',
  'dispersion_reason':'projectability removes D_i N but does not remove D_i dot(pi), so the frozen mixed spatial-kinetic operator survives',
  'elliptic_compensator':{
    'ell':'1+q/M_c^2',
    'Q':'H0/ell',
    'J_A_matter_plus_aux':'Q-H0=-H0 q/(M_c^2+q)',
    'homogeneous_A_source':'q=0 -> J_A=0 exactly',
    'isolated_aux_pair_det':'ell^2>0'
  },
  'parent_gravity_dof_input':'published projectable U(1) gravity sector has only tensor graviton polarizations at full classical order; the nonprojectable eta1/eta2 radiative detuning mechanism is absent because local lapse gradients do not exist',
  'provisional_total_dof':'2 parent tensor + 1 intended RTK scalar + 0 auxiliary propagating DOF, subject to a fresh coupled projectable Dirac recertification',
  'advantages_over_nonprojectable_branch':[
    'C9 eta1/eta2 tuning problem is structurally bypassed rather than numerically tuned',
    'exact rational RTK scalar dispersion survives',
    'elliptic scale-separated A-source compensator survives',
    'homogeneous evolving ordinary-matter A-source remains cancelled'
  ],
  'non_claims':[
    'does not yet prove the full coupled projectable Dirac algebra with RTK and Q,Lambda sectors',
    'does not yet rederive the same-action projectable PPN equations including the fixed RTK scalar',
    'does not yet reproduce the production Friedmann/background history with the global Hamiltonian constraint',
    'does not yet establish projectable strong-field or black-hole viability',
    'does not choose between the projectable candidate and the current nonprojectable lambda>1 branch'
  ],
  'next_gate':'perform a fresh projectable coupled constraint/DOF count with the RTK scalar and elliptic auxiliary pair; then recertify static/moving PPN on the projectable universal matter frame and derive the homogeneous cosmology/global Hamiltonian constraint.'
}
open('c9_projectable_u1_rtk_compatibility_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
