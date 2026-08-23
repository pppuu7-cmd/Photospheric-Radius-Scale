#!/usr/bin/env python3
"""Flat-background pure-lapse UV Wilson compression for the corrected U(1) action.

External potential input (3 spatial dimensions): Zhu, Wu, Wang, Shu,
arXiv:1108.1237, Eqs. (14),(16), where the lapse scalar operator is
  eth = beta0 + zeta^-2 (beta2+beta4) d^2 - zeta^-4 beta8 d^4.
For Fourier q=|k|^2, d^2 -> -q. Their quadratic pure-lapse action contains
  + zeta^2 q eth(q) phi^2.
Equivalently, using Eq.(55) normalization M_Pl^2=2 zeta^2, the direct
Hamiltonian cross-block entry has symbol
  a_g(q)=M_Pl^2 q eth(q).

On the corrected current IR slice beta0_bare=0. Hence the q term vanishes;
only beta2+beta4 enters q^2 and beta8 enters q^3 in the flat pure-lapse
Hessian. This theorem does not freeze those UV Wilson coefficients.
"""
import json
import sympy as sp

q,zeta,Mpl=sp.symbols('q zeta M_Pl', positive=True, finite=True)
b0,b2,b4,b8=sp.symbols('beta0 beta2 beta4 beta8', real=True, finite=True)
eth=sp.expand(b0-(b2+b4)*q/zeta**2-b8*q**2/zeta**4)
a=sp.expand(Mpl**2*q*eth)
# Current full-action bare-gravity slice: beta0_bare=0 and Mpl^2=2 zeta^2.
a_current=sp.expand(a.subs({b0:0,Mpl**2:2*zeta**2}))
expected=sp.expand(-2*(b2+b4)*q**2-2*b8*q**3/zeta**2)
assert sp.simplify(a_current-expected)==0
assert sp.expand(a_current).coeff(q,1)==0
assert sp.expand(a_current).coeff(q,2)==-2*(b2+b4)
assert sp.expand(a_current).coeff(q,3)==-2*b8/zeta**2

out={
  'classification':'RTK_ROUTE_B_U1_FLAT_LAPSE_UV_WILSON_COMPRESSION_PASS',
  'status_scope':'GREEN_EXACT_FLAT_PURE_LAPSE_UV_COMPRESSION_NUMERICAL_WILSON_BOUNDS_PENDING',
  'external_input':'arXiv:1108.1237 Eqs. (14),(16), d=3 generalized-detailed-balance potential',
  'fourier_operator':'eth(q)=beta0-zeta^-2(beta2+beta4)q-zeta^-4 beta8 q^2',
  'hamiltonian_a_symbol':'a_g(q)=M_Pl^2 q eth(q)',
  'current_slice':'beta0_bare=0 and M_Pl^2=2 zeta^2',
  'current_symbol':'a_g(q)=-2(beta2+beta4)q^2-2 beta8 q^3/zeta^2',
  'q2_wilson_combination':'beta2+beta4 only',
  'q3_wilson_combination':'beta8 only',
  'other_beta_support':'beta1,beta3 are nonlinear in a_i and do not enter the quadratic flat pure-lapse Hessian; beta5,beta6,beta7 require curvature/metric mixing and do not enter the fixed-flat-metric pure-lapse Hessian.',
  'interpretation':'The direct pure-gravity lapse remainder needed for the punctured-low-k bound is controlled by two UV combinations rather than the full potential. The current partial IR tuple does not yet freeze beta2+beta4 or beta8, so a numerical uniform epsilon cannot yet be claimed.',
  'non_claims':[
    'does not set beta2,beta4,beta8 to zero',
    'does not bound metric-lapse mixed perturbations away from the fixed flat background',
    'does not by itself provide a numerical epsilon',
    'does not choose M_c or UV scales'
  ],
  'next_gate':'combine this exact a(q) remainder with the exact d4 coefficient and elliptic-filter remainder to give C(beta2+beta4,beta8,lambda,matter); then impose an EFT-domain bound or freeze UV Wilson coefficients before numerical epsilon certification.'
}
open('u1_flat_lapse_uv_wilson_compression_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
