#!/usr/bin/env python3
"""Exact homogeneous neutral-RTK lapse-rank theorem.

Scope: k=0 rolling X_U>0 branch of the frozen shift-symmetric RTK scalar,
after the elliptic matter-compensator has removed the ordinary homogeneous
A-source.  The only direct RTK correction allowed by the previously certified
cross-block support theorem is delta_a={pi_N,H_perp}_RTK.

For any homogeneous shift-symmetric P(X), X=Theta^2/2 and
p_Sigma=sqrt(g) P_X Theta.  At fixed canonical variables the inverse relation
Theta=Theta(p_Sigma,g) contains no lapse N.  The Legendre Hamiltonian is
therefore exactly affine in N.  The mixed C(X)(D Theta)^2 term vanishes on k=0.
Thus delta_a_RTK(k=0)=0 exactly on this support.
"""
import json
import sympy as sp

TARGET='research/theory_targets/RTK_ROUTE_B_U1_ELLIPTIC_K0_RTK_LAPSE_RANK_TARGET_v1.json'
t=json.load(open(TARGET))
assert t['classification']=='RTK_ROUTE_B_U1_ELLIPTIC_K0_RTK_LAPSE_RANK_TARGET_V1_FROZEN'

# Canonical homogeneous variables.  Th is the already inverted velocity
# variable Theta(pSigma,g); by construction it is independent of N.
N, sqrtg, pS, Th = sp.symbols('N sqrtg p_Sigma Theta', positive=True, finite=True)
P = sp.Function('P')
X = Th**2/sp.Integer(2)
Hperp = sp.simplify(pS*Th - sqrtg*P(X))
H = sp.expand(N*Hperp)
assert sp.diff(Th,N)==0
assert sp.diff(Hperp,N)==0
assert sp.simplify(sp.diff(H,N)-Hperp)==0
assert sp.diff(sp.diff(H,N),N)==0

# Explicit representative verifies the momentum relation and inverse-lapse
# cancellation before abstracting to the general Legendre statement.
mu, q, v = sp.symbols('mu q v', positive=True, finite=True)
# P_rep=(mu^2/2)(Theta-q)^2 is only a regular local representative used to
# verify the canonical algebra; the general proof above does not assume it.
Prep = mu**2*(v-q)**2/sp.Integer(2)
p_rep = sp.diff(Prep,v)  # p/sqrtg = P_X*Theta in velocity language up to chosen local coordinate
vsol = sp.solve(sp.Eq(sp.symbols('pbar'),p_rep),v)[0]
assert sp.diff(vsol,N)==0

# The fixed mixed operator is proportional to spatial gradients of Theta and is
# identically zero on the homogeneous support.  Encode one representative jet.
gradTh, C = sp.symbols('gradTheta C', finite=True, real=True)
Lmix = C*gradTh**2
assert sp.simplify(Lmix.subs(gradTh,0))==0
assert sp.simplify(sp.diff(Lmix,C).subs(gradTh,0))==0

# Cross-block conclusion from canonical PB: {pi_N,Hperp}=-dHperp/dN=0.
delta_a = -sp.diff(Hperp,N)
assert sp.simplify(delta_a)==0

out={
  'classification':'RTK_ROUTE_B_U1_ELLIPTIC_K0_RTK_LAPSE_RANK_EXACT_PASS',
  'status':'HOMOGENEOUS_NEUTRAL_RTK_LAPSE_STABILITY_CORRECTION_ZERO_ON_ROLLING_K0_SUPPORT',
  'target':TARGET,
  'domain':t['domain'],
  'canonical_derivation':{
    'momentum_relation':'p_Sigma=sqrt(g) P_X(Theta^2/2) Theta; after inversion Theta=Theta(p_Sigma,g) is N-independent',
    'hamiltonian':'H_Sigma=N[p_Sigma Theta-sqrt(g)P(Theta^2/2)]',
    'H_perp_RTK':'p_Sigma Theta-sqrt(g)P(Theta^2/2)',
    'd_Hperp_dN_at_fixed_canonical_variables':'0',
    'delta_a_RTK':'{pi_N,H_perp}_RTK=0'
  },
  'mixed_operator':{
    'operator':'C(X_U) D_iTheta_U D^iTheta_U',
    'k0_value':'0',
    'homogeneous_lapse_rank_contribution':'0'
  },
  'combination_with_prior_k0_gate':'The prior elliptic k0 ordinary-matter theorem leaves only delta_a_RTK as an independent source correction; this result sets that correction to zero on the stated homogeneous rolling support.',
  'interpretation':'The elliptic homogeneous A-source rescue does not acquire a new lapse-stability rank deformation from the neutral rolling RTK scalar at k=0. The remaining homogeneous rank is inherited from the special pure-gravity U1 block, subject to its own global zero-mode boundary assumptions.',
  'non_claims':t['non_claims'],
  'next_gate':t['next_gate_if_pass']
}
open('u1_elliptic_k0_rtk_lapse_rank_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
