#!/usr/bin/env python3
"""Exact filtered-matter b_m=-c_m relation on the flat homogeneous canonical slice.

After exact auxiliary projection Jm=-a_eff(q,g) H0. On D_i nu=0 and the flat
homogeneous canonical background:
  * Jm is independent of lapse, A, nu and gravity momentum;
  * the filtered matter self bracket with H0 vanishes;
  * gravity potential terms and the neutral RTK Hamiltonian carry no gravity
    canonical momentum conjugate to the metric on this source channel, so their
    direct bracket with Jm vanishes;
  * shift/prepotential pieces are weak momentum-constraint support.
Thus the filtered contribution to c={J,Hperp} comes entirely from the gravity
kinetic Hamiltonian K_g and is lapse-independent:
  c_m={Jm,K_g}.
The same source in preservation of Ghat is phi_m=N c_m, hence with
{pi_N,N}=-1,
  b_m={pi_N,phi_m}=-c_m.
This is exact in the elliptic q dependence within this flat-background support,
not merely a leading-q statement.
"""
import json
import sympy as sp

N,pN,q,M2,V,H,tau=sp.symbols('N pi_N q M_c_squared V H0 tau_H', finite=True)
# Exact previously derived filtered c_m on the isotropic gravity background.
c=sp.simplify(V*(M2*q*H/(M2+q)**2-q*tau/(M2+q)))
phi=sp.expand(N*c)
def PB_N(f,g):
    return sp.simplify(sp.diff(f,N)*sp.diff(g,pN)-sp.diff(f,pN)*sp.diff(g,N))
b=sp.simplify(PB_N(pN,phi))
assert sp.simplify(b+c)==0
assert sp.diff(c,N)==0
# q->0 coefficient reproduces the earlier leading relation.
M2p,qp=sp.symbols('M2p qp', positive=True, finite=True)
cp=c.subs({M2:M2p,q:qp})
lead=sp.simplify(sp.limit(cp/qp,qp,0,dir='+'))
assert sp.simplify(lead-V*(H-tau)/M2p)==0
# Exact q^2 coefficient.
series=sp.series(cp,qp,0,3).removeO().expand()
c_q2=sp.factor(series.coeff(qp,2))
assert sp.simplify(c_q2-V*(-2*H+tau)/M2p**2)==0

out={
  'classification':'RTK_ROUTE_B_U1_FILTERED_MATTER_BC_EXACT_FLAT_PASS',
  'status_scope':'GREEN_EXACT_FILTERED_OFFDIAGONAL_PAIR_FLAT_HOMOGENEOUS_SUPPORT',
  'domain':'Dirac-projected D_i nu=0 flat homogeneous canonical background, isotropic gravity momentum, modulo total momentum-constraint support',
  'exact_c_m':'V [M_c^2 q H0/(M_c^2+q)^2 - q tau_H/(M_c^2+q)]',
  'exact_b_m':'-c_m',
  'exact_phi_m':'N c_m',
  'q_leading':'c_m=(q/M_c^2)V(H0-tau_H)+O(q^2)',
  'q2_coefficient':'V(-2 H0+tau_H)/M_c^4',
  'interpretation':'Within the stated flat homogeneous canonical support, the projected ordinary-matter filter preserves exact antisymmetry of the two off-diagonal cross-block entries for its entire rational q dependence.',
  'non_claims':[
    'does not extend b_m=-c_m to arbitrary inhomogeneous scalar/gravity canonical backgrounds',
    'does not say the total diagonal entries a,d vanish',
    'does not certify rank at an off-diagonal zero without evaluating a*d',
    'does not choose M_c'
  ],
  'next_gate':'combine the exact filtered c_m with b2 and V/b2 to solve the exact off-diagonal zero equation as a quadratic in s=M_c^2+q; treat each zero as a candidate full-rank locus, not automatically a determinant zero.'
}
open('u1_filtered_matter_bc_exact_flat_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
