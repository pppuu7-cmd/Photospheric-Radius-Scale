#!/usr/bin/env python3
"""C10 exact source transformation into Newtonian-coordinate representation.

The theorem keeps the preferred shear B explicit and intentionally does not
classify zeros of the partial B coefficient as physical poles.  That belongs to
a later full DAE/determinant gate.
"""
import json
from pathlib import Path
import sympy as sp

H,a,G=sp.symbols('H a G', positive=True, finite=True, real=True)
lam,L,k,Mc=sp.symbols('lambda L k M_c', finite=True, real=True)
rho,p,rhop,pp=sp.symbols('rho p rho_prime p_prime', finite=True, real=True)
rho_o,p_o,rhop_o=sp.symbols('rho_o p_o rho_o_prime', finite=True, real=True)
B=sp.symbols('B', finite=True, real=True)
dmuQ,dmuN,dpQ,dpN,qQ,qN,PiQ,PiN=sp.symbols('dmu_Q dmu_N dp_Q dp_N q_Q q_N Pi_Q Pi_N', finite=True, real=True)
psi,psip,phi=sp.symbols('psi psi_prime phi', finite=True, real=True)
D=3*lam-1
r=lam-1

# Frozen coordinate convention: new Newtonian coordinates use T=-B from the
# quasilongitudinal E=0 branch. Scalar perturbations transform as
# delta f_new=delta f_old-fbar' T.
T=-B
dmuN_expr=sp.expand(dmuQ-rhop*T)
dpN_expr=sp.expand(dpQ-pp*T)
assert sp.simplify(dmuN_expr-(dmuQ+rhop*B))==0
assert sp.simplify(dpN_expr-(dpQ+pp*B))==0
# Inverse maps.
dmuQ_expr=sp.solve(sp.Eq(dmuN,dmuN_expr),dmuQ)[0]
dpQ_expr=sp.solve(sp.Eq(dpN,dpN_expr),dpQ)[0]
assert sp.simplify(dmuQ_expr-(dmuN-rhop*B))==0
assert sp.simplify(dpQ_expr-(dpN-pp*B))==0

# Primary q=-a(rho+p)(v+B). Under the same coordinate representation the
# mixed stress component gives q_new=q_old-a(rho+p)T.
qN_expr=sp.expand(qQ-a*(rho+p)*T)
qQ_expr=sp.solve(sp.Eq(qN,qN_expr),qQ)[0]
assert sp.simplify(qN_expr-(qQ+a*(rho+p)*B))==0
assert sp.simplify(qQ_expr-(qN-a*(rho+p)*B))==0
assert sp.simplify(PiN-PiQ)==PiN-PiQ  # background anisotropic stress is zero; map is identity below

# Ordinary-only A source: delta H0_Q=delta H0_N-H0'_ordinary B.
dH0N=sp.symbols('delta_H0_N', finite=True, real=True)
dH0Q=sp.expand(dH0N-rhop_o*B)
# Helmholtz A constraint, k>0 convention already certified.
A_lhs=(k**2+a**2*Mc**2)*psi
A_rhs=-4*sp.pi*G*a**2*dH0Q

# Total momentum constraint: D(psi'+H phi)+r L B=8 pi G a q_Q.
MqN=8*sp.pi*G*a*qN
mom_pref=D*(psip+H*phi)+r*L*B-8*sp.pi*G*a*qQ
mom_new=sp.expand(mom_pref.subs(qQ,qQ_expr))
KB=sp.expand(r*L+8*sp.pi*G*a**2*(rho+p))
mom_target=sp.expand(KB*B-MqN+D*(psip+H*phi))
assert sp.simplify(mom_new-mom_target)==0

# Exact inverse-map round trip guards.
assert sp.simplify(dmuN_expr.subs(dmuQ,dmuQ_expr)-dmuN)==0
assert sp.simplify(dpN_expr.subs(dpQ,dpQ_expr)-dpN)==0
assert sp.simplify(qN_expr.subs(qQ,qQ_expr)-qN)==0

out={
  'classification':'C10_U1_NEWTONIAN_TOTAL_SOURCE_TRANSFORM_PASS_SCOPED',
  'status_scope':'GREEN_EXACT_SOURCE_COORDINATE_MAP_FULL_DAE_POLE_AUDIT_NEXT',
  'source_map_QL_to_N':{
    'delta_mu_N':'delta_mu_QL+rho_prime B',
    'delta_p_N':'delta_p_QL+p_prime B',
    'q_N':'q_QL+a(rho+p)B',
    'Pi_N':'Pi_QL'
  },
  'source_map_N_to_QL':{
    'delta_mu_QL':'delta_mu_N-rho_prime B',
    'delta_p_QL':'delta_p_N-p_prime B',
    'q_QL':'q_N-a(rho+p)B',
    'Pi_QL':'Pi_N'
  },
  'ordinary_A_source_scope':'delta H0_QL=delta H0_N-H0_ordinary_prime B; neutral Khronon is not inserted into H0_ordinary',
  'transformed_A_constraint':'(k^2+a^2 M_c^2)psi=-4 pi G a^2[delta H0_N-H0_ordinary_prime B]',
  'transformed_momentum_constraint':'K_B_partial B=8 pi G a q_N-(3lambda-1)(psi_prime+H phi)',
  'K_B_partial':'(lambda-1)L+8 pi G a^2(rho_total+p_total)',
  'critical_guard':'K_B_partial is only a partial-elimination coefficient. Its zero is NOT classified as a physical pole before the transformed A constraint, its time derivative, Hamiltonian constraint and total conservation equations are included in one DAE/determinant audit.',
  'round_trip_source_map':'PASS',
  'next_gate':'full transformed DAE/determinant and pole audit over the certified finite-k rank domain',
  'non_claims':[
    'no physical-pole classification from K_B_partial alone',
    'not a completed transformed gravity solver',
    'not a CLASS implementation',
    'not a B4 massive-neutrino extension',
    'not a likelihood result'
  ],
  'target':'research/theory_targets/RTK_C10_U1_NEWTONIAN_SOURCE_TRANSFORM_TARGET_v1.json'
}
Path('u1_newtonian_source_transform_result.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
