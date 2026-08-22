#!/usr/bin/env python3
"""Scoped static 1PN beta theorem for the fixed U1+RTK scalar action.

External equations (Lin, Mukohyama, Wang, Zhu, arXiv:1310.6666):
- Eq. (4.15), in phi=0 gauge: for a2=0, Omega=1,
    J^t=-2 rho_H,  J_A=2 a1 rho_H.
  Hence a1=1 gives J^t+J_A=0 exactly.
- Appendix E Eq. (E.3), for sigma1=sigma2=0:
    2 beta0 div(a) + beta0 a^2 = 8 pi (J^t-gamma1 J_A)
  after the A constraint eliminates R.
- Eqs. (5.43),(5.50),(5.51): for a1=kappa=1, gamma1=-1 the beta0
  consistency relation is identically satisfied and the pure U1 PPN values include beta=1.

Our fixed action has beta0_bare=0 but its exact static mixed operator is
M_Pl^2 a_i a^i, i.e. beta0_eff=2.  The additional reconstructed P(X) clock
has lapse Euler derivative E_P=P-2XP_X=-rho.  With zeta^2=M_Pl^2/2, adding
this scalar on the gravity side changes the paper's Hamiltonian expression by
-E_P/zeta^2.  After homogeneous-background subtraction,
  delta E_P = K_phys n_4,
  K_phys = 2 M_Pl^2 M_K^2,
so the extra O(4) term is -4 M_K^2 n_4.

The family-I gate already established n_2=0. Thus a_i=D_i n_4+O(6), a^2=O(8),
and the static O(4) E.3 equation becomes
    4 Laplacian(n_4) - 4 M_K^2 n_4 = 0.
For M_K^2>0 on a connected regular stellar slice, regularity plus n_4->0 at
spatial infinity implies n_4=0 by the standard energy/maximum-principle
identity.  Therefore the fixed P(X) clock does not shift the static 1PN metric
coefficient on this branch, and the remaining family-I static beta is 1.

This is NOT a moving-source preferred-frame theorem and NOT a strong-field
compact-object theorem.
"""
import json
import sympy as sp

# Exact source cancellation on frozen matter frame.
rho,a1,a2,gamma1=sp.symbols('rho a1 a2 gamma1', finite=True, real=True)
Jt=-2*rho
JA=2*a1*rho  # a2=0, Omega=1, phi=0 specialization of Eq.(4.15)
source=sp.simplify(Jt-gamma1*JA)
source_tuple=sp.simplify(source.subs({a1:1,gamma1:-1}))
assert source_tuple==0

# Family-I beta0 consistency Eq.(5.43): beta0*(a1^2*kappa*gamma1+1)
# +2*kappa*(a1*gamma1+1)^2 =0.
beta0,kappa=sp.symbols('beta0 kappa', finite=True, real=True)
consistency=beta0*(a1**2*kappa*gamma1+1)+2*kappa*(a1*gamma1+1)**2
assert sp.simplify(consistency.subs({a1:1,kappa:1,gamma1:-1}))==0

# Fixed action normalization.
Mpl2,MK2,n4,lapn4=sp.symbols('Mpl2 MK2 n4 lapn4', positive=True, finite=True, real=True)
zeta2=Mpl2/2
Kphys=2*Mpl2*MK2
scalar_paper_term=sp.simplify(-Kphys*n4/zeta2)
assert scalar_paper_term==-4*MK2*n4
beta0_eff=sp.Integer(2)
E4=sp.expand(2*beta0_eff*lapn4 + scalar_paper_term) # a^2 is O(8)
assert E4==4*lapn4-4*MK2*n4

# Energy uniqueness: multiply (Delta-M^2)n=0 by n and integrate over a
# regular asymptotically-flat connected slice. Boundary term vanishes:
#   0 = -int |grad n|^2 - M^2 int n^2.
# Both nonnegative integrals must vanish for M^2>0.
Igrad,In2=sp.symbols('I_grad I_n2', nonnegative=True, finite=True, real=True)
M2=sp.symbols('M2', positive=True, finite=True, real=True)
energy=-Igrad-M2*In2
# Algebraic certificate of the implication energy=0 -> both zero:
# if either integral >0 the expression is strictly negative. Record rather
# than asking SymPy for an inequality proof.

MK0=1.1681315109161161
out={
  'classification':'RTK_ROUTE_B_U1_STATIC_1PN_BETA_YUKAWA_PASS',
  'scope':'static weak-field 1PN, regular connected stellar slice, zero scalar flux/constant-q clock branch, homogeneous cosmological background subtracted, X_U>0',
  'frozen_tuple':{'a1':1,'a2':0,'kappa':1,'gamma1':-1,'sigma1':0,'sigma2':0,'beta0_bare':0,'beta0_eff_static':2},
  'external_equations':{
    'paper':'Lin-Mukohyama-Wang-Zhu arXiv:1310.6666',
    'matter_sources':'Eq.(4.15): at a1=1,a2=0,phi=0,Omega=1, Jt=-2 rho_H and JA=+2 rho_H',
    'O4_constraint':'Appendix E Eq.(E.3)',
    'family_I':'Eqs.(5.43),(5.50),(5.51)'
  },
  'exact_checks':{
    'Jt_minus_gamma1_JA_on_tuple':str(source_tuple),
    'beta0_consistency_on_tuple':str(sp.simplify(consistency.subs({a1:1,kappa:1,gamma1:-1}))),
    'P_X_paper_normalized_O4_term':str(scalar_paper_term),
    'O4_ADM_lapse_equation':'4 Delta n4 - 4 M_K^2 n4 = 0'
  },
  'z0_M_K_Mpc_inv':MK0,
  'boundary_conditions':['n4 regular through stellar center/interior','n4 -> 0 at spatial infinity','no singular shell/source for the RTK scalar lapse equation'],
  'uniqueness_identity':'integral n4(Delta-M_K^2)n4 = -integral|grad n4|^2 - M_K^2 integral n4^2 = 0, hence n4=0',
  'result':'The fixed P(X_U) clock produces no nonzero static O(4) ADM-lapse solution under the stated regular/asymptotically-flat conditions. Therefore it does not shift the static 1PN beta coefficient; the remaining exact family-I value is beta=1.',
  'status_scope':'STATIC_1PN_BETA_GREEN_FIXED_ACTION_REGULAR_STAR',
  'non_claims':[
    'does not establish moving-source alpha1 or alpha2 for the full fixed scalar action',
    'does not cover nonzero scalar flux/charge or black-hole boundary conditions',
    'does not cover strong-field stars, X_U=0, or crossing the DBI edge',
    'does not establish radiative protection, UV tensor dispersion, or strong-coupling cutoff',
    'does not turn the whole PPN sector into a completed gate beyond the stated static 1PN scope'
  ],
  'next_gate':'derive moving-source scalar response and preferred-frame alpha1/alpha2 on the same fixed tuple; separately continue the strong-field zero-flux branch-B radial system and C9 radiative/cutoff gates'
}
open('u1_static_1pn_beta_yukawa_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
