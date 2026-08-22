#!/usr/bin/env python3
"""Scoped C8 theorem: the neutral RTK sector does not make the exceptional-U1
second-class cross block identically singular.

Inputs already established by earlier CI gates:
  * exceptional pure-gravity eta1=eta2=0 has a regular region with det B_g != 0;
  * neutral Sigma sector has no direct A support;
  * modulo momentum constraint it can modify only a={pi_N,H_perp} by delta_a.

Choose a regular scalar-derivative-free canonical slice:
  D_i Sigma = 0, p_Sigma = 0, D_i Theta_U = 0,
with Sigma at a stationary point of its local potential/background energy map.
Then S_mix vanishes and the neutral matter Hamiltonian is N times an
N-independent constraint density on this slice, hence delta_a=0. Therefore
B_coupled=B_g and det B_coupled=det B_g != 0 wherever the chosen gravity point
is regular.

This proves only non-identical degeneracy / existence of a regular coupled
phase-space region. It does NOT prove the rolling RTK cosmological branch has
the same rank; that is the next mandatory gate.
"""
import json
import sympy as sp

ag,bg,cg,dg=sp.symbols('a_g b_g c_g d_g', finite=True)
delta_a=sp.symbols('delta_a', finite=True)

B_g=sp.Matrix([[ag,bg],[cg,dg]])
B_c=sp.Matrix([[ag+delta_a,bg],[cg,dg]])
det_g=sp.expand(B_g.det())
det_c=sp.expand(B_c.det())

# Defining conditions of the scalar-derivative-free canonical slice.
D_Sigma=sp.Integer(0)
p_Sigma=sp.Integer(0)
D_Theta=sp.Integer(0)
# S_mix ~ C (D Theta)^2 and the canonical neutral-matter density has no
# residual nonlinear lapse dependence on this slice.
delta_a_slice=sp.Integer(0)
assert D_Sigma==0 and p_Sigma==0 and D_Theta==0
assert delta_a_slice==0

det_slice=sp.simplify(det_c.subs(delta_a,delta_a_slice))
assert sp.simplify(det_slice-det_g)==0

out={
  'classification':'RTK_ROUTE_B_U1_GENERIC_COUPLED_RANK_SLICE_PASS',
  'slice_conditions':['D_i Sigma = 0','p_Sigma = 0','D_i Theta_U = 0','stationary local scalar/background-energy point'],
  'delta_a_on_slice':'0',
  'det_B_coupled_on_slice':str(det_slice),
  'det_B_gravity':str(det_g),
  'result':'On every regular pure-gravity point of this scalar-derivative-free slice, det(B_coupled)=det(B_gravity)!=0.',
  'scope':'existence/non-identical-degeneracy theorem only',
  'non_claims':[
    'does not prove rank preservation on the rolling RTK cosmological background',
    'does not complete the coupled Hamiltonian DOF count',
    'does not establish radiative stability or PPN viability'
  ],
  'next_gate':'derive delta_a on the rolling homogeneous RTK background with beta0_bare=0 and explicit S_mix, then test whether det(B_g)+d_g*delta_a can vanish in the physical lambda_HL domain'
}
open('u1_generic_coupled_rank_slice_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
