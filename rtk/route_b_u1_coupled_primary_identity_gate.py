#!/usr/bin/env python3
"""C8 coupled primary-identity survival theorem for the selected U(1) route.

Inputs already established separately:
  1) On the exceptional nonprojectable U(1) gravity surface eta1=eta2=0,
     the pure-gravity Dirac chain has the primary combination p_nu+J_A and
     {pi_N,J_A}=0 (Mukohyama et al., arXiv:1504.07357).
  2) The published universal matter frame at a2=0 is canonically affine and
     contributes p_nu^m=-J_A^m with dJ_A^m/dN=0.
  3) The RTK neutral-Sigma DBI/mixed sector built from Theta_U contains N,
     invariant shift and spatial nu derivatives but no A or dot(nu), so its
     direct contributions to J_A and p_nu vanish.

This gate combines the identities exactly. It establishes that coupling these
sectors does not automatically turn {pi_N,J_A} into a nonzero bracket and does
not destroy the U(1) primary combination. Therefore the algebraic prerequisite
for the two extra secondary constraints of the exceptional gravity branch
survives. Independence/rank of the modified secondary constraints is NOT proven.
"""
import json
import sympy as sp

# Generic canonical generators; by definition independent of N,A,nudot here.
a1,H0,Hi,JA_g = sp.symbols('a1 H0 Hi JA_g', real=True, finite=True)
N,A,Ni,nudot,nux = sp.symbols('N A Ni nudot nux', real=True, finite=True)

# a2=0 universal ordinary-matter frame.
Acal=-nudot+Ni*nux+sp.Rational(1,2)*N*nux**2
Nbar=N-a1*(A-Acal)
Nibar=Ni+N*nux
Hm=sp.expand(Nbar*H0+Nibar*Hi)
pnu_m=sp.simplify(-sp.diff(Hm,nudot))
JA_m=sp.simplify(sp.diff(Hm,A))
assert sp.simplify(pnu_m+JA_m)==0
assert sp.simplify(sp.diff(JA_m,N))==0

# Pure exceptional gravity identity represented canonically.
pnu_g=-JA_g
# JA_g is taken independent of N exactly on eta1=eta2=0, the external
# Hamiltonian theorem being tested for survival under the added sectors.
assert sp.diff(JA_g,N)==0

# RTK Sigma sector constructed from Theta_U has no A or nudot direct support.
JA_rtk=sp.Integer(0)
pnu_rtk=sp.Integer(0)

JA_total=sp.simplify(JA_g+JA_m+JA_rtk)
pnu_total=sp.simplify(pnu_g+pnu_m+pnu_rtk)
primary_combo=sp.simplify(pnu_total+JA_total)
piN_JA_total=sp.simplify(sp.diff(JA_total,N))

assert primary_combo==0
assert piN_JA_total==0
assert sp.simplify(JA_rtk)==0 and sp.simplify(pnu_rtk)==0

# Evaluate the frozen family-I a1=1 representative as a consistency check.
assert sp.simplify(primary_combo.subs(a1,1))==0
assert sp.simplify(piN_JA_total.subs(a1,1))==0

out={
  'classification':'RTK_ROUTE_B_U1_COUPLED_PRIMARY_IDENTITY_SURVIVES',
  'surface':'eta1=eta2=0 / sigma1=sigma2=0',
  'matter_frame':{'a1':1,'a2':0},
  'ordinary_matter':{'pnu_m':str(pnu_m),'JA_m':str(JA_m),'pnu_m_plus_JA_m':str(sp.simplify(pnu_m+JA_m)),'dJA_m_dN':str(sp.diff(JA_m,N))},
  'rtk_sigma_direct':{'JA_rtk':'0','pnu_rtk':'0','reason':'Theta_U/DBI+mixed route has no A or dot(nu) direct velocity support'},
  'combined':{'pnu_total_plus_JA_total':str(primary_combo),'dJA_total_dN':str(piN_JA_total)},
  'interpretation':'The selected a2=0 universal matter frame plus the neutral RTK Sigma sector preserve the primary U(1) combination and the vanishing pi_N-J_A bracket condition that is necessary for the exceptional secondary-constraint chain.',
  'non_claims':[
    'does not prove the modified H_perp and phi_A are independent second-class constraints',
    'does not compute their coupled Poisson bracket/rank',
    'does not yet establish 2 tensor + 1 RTK scalar as the final nonlinear DOF count',
    'does not solve PPN/Newton, radiative, GW or cutoff gates'
  ],
  'next_gate':'derive the Sigma-source modifications of H_perp and phi_A and compute the coupled second-class Poisson submatrix/rank with lambda_HL symbolic'
}
open('u1_coupled_primary_identity_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print('RTK_ROUTE_B_U1_COUPLED_PRIMARY_IDENTITY_SURVIVES',json.dumps(out,sort_keys=True))
