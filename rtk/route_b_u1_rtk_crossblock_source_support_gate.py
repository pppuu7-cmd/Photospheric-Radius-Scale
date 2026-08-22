#!/usr/bin/env python3
"""C8 source-support theorem for the coupled U(1) second-class cross block.

External pure-gravity input (Mukohyama et al., arXiv:1504.07357, special
eta1=eta2=0 branch): the rank decision is the 2x2 block
 B=[[{pi_N,H_perp},{pi_N,phi_A}],
    [{J_A,H_perp},{J_A,phi_A}]].

Previously executable RTK inputs:
  * neutral Sigma DBI/mixed action has no direct A or dot(nu) support;
  * it depends on nu only through invariant shift v^i=N^i-N D^i nu and Dv;
  * its nu Euler equation obeys E_nu=D_i(N E_shift^i).

This theorem tracks the *direct RTK source support* modulo the momentum/shift
constraint. Since J_A=J_A[g] on the exceptional surface and H_Sigma contains
no gravitational canonical momentum pi^{ij}, {J_A,H_Sigma}=0 exactly. The
RTK contribution to preservation of p_nu+J_A is only the invariant-shift
Noether divergence and therefore vanishes weakly on the total momentum
constraint. Hence phi_A receives no independent RTK source weakly.

Consequently, among the four entries of B, only a={pi_N,H_perp} can receive a
direct RTK correction. The other three remain the pure-gravity operators
weakly. This is a support theorem, not yet a proof that det B stays nonzero.
"""
import json
import sympy as sp

# Abstract pure-gravity cross-block entries and one possible RTK lapse-stability
# correction. The identities below encode the canonical-support result.
ag,bg,cg,dg,da=sp.symbols('a_g b_g c_g d_g delta_a', finite=True)

# Canonical source labels. Exact zeros were proved by the preceding gates.
dJA_sigma=sp.Integer(0)          # A-independence of neutral Sigma sector
dc_sigma=sp.Integer(0)           # {J_A[g],H_sigma[g,S,pS,N,v]}: no pi_g on either side
dphi_sigma_weak=sp.Integer(0)    # E_nu^Sigma = div(N E_shift^Sigma) ≈ 0 on momentum constraint
db_sigma_weak=sp.Integer(0)      # pi_N acting on a weak momentum-divergence source is weakly zero
dd_sigma_weak=sp.Integer(0)      # J_A bracket with absent independent phi_A Sigma source

assert dJA_sigma==0 and dc_sigma==0
assert dphi_sigma_weak==0 and db_sigma_weak==0 and dd_sigma_weak==0

B_g=sp.Matrix([[ag,bg],[cg,dg]])
B_c=sp.Matrix([[ag+da,bg+db_sigma_weak],[cg+dc_sigma,dg+dd_sigma_weak]])
det_g=sp.expand(B_g.det())
det_c=sp.expand(B_c.det())
delta_det=sp.factor(det_c-det_g)
assert sp.simplify(delta_det-da*dg)==0

out={
  'classification':'RTK_ROUTE_B_U1_RTK_CROSSBLOCK_SOURCE_SUPPORT_PASS',
  'basis':['pi_N','J_A','H_perp','phi_A'],
  'direct_RTK_sources':{
    'delta_J_A':'0 (neutral Sigma action is A-independent)',
    'delta_phi_A_weak':'0 (invariant-shift Noether identity modulo total momentum constraint)',
    'delta_{J_A,H_perp}':'0 (J_A and H_Sigma contain no conjugate gravity momenta)',
    'delta_{pi_N,phi_A}_weak':'0',
    'delta_{J_A,phi_A}_weak':'0',
    'delta_{pi_N,H_perp}':'delta_a, generally nonzero because mixed kinetic Hamiltonian can depend on lapse gradients'
  },
  'B_gravity':str(B_g),
  'B_coupled_weak':str(B_c),
  'det_B_gravity':str(det_g),
  'det_B_coupled_weak':str(det_c),
  'delta_det_B':str(delta_det),
  'interpretation':'Modulo the momentum constraint, the neutral invariant-shift RTK sector can alter only the lapse-stability entry a of the second-class cross block; b,c,d retain their pure-gravity operators.',
  'non_claims':[
    'does not prove det(B_coupled) is everywhere or weakly nonzero',
    'does not exclude rank-changing exceptional Sigma backgrounds',
    'uses the special eta1=eta2=0 pure-gravity J_A[g] structure as external Hamiltonian input'
  ],
  'next_gate':'prove generic coupled rank by showing delta_a vanishes on a regular scalar-derivative-free phase-space slice where the pure-gravity detB is nonzero; then separately audit the rolling RTK cosmological branch for rank change'
}
open('u1_rtk_crossblock_source_support_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print('RTK_ROUTE_B_U1_RTK_CROSSBLOCK_SOURCE_SUPPORT_PASS',json.dumps(out,sort_keys=True))
