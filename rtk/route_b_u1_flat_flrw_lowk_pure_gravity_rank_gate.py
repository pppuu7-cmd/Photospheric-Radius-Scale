#!/usr/bin/env python3
"""Low-k pure-gravity rank theorem from the published special-U(1) brackets.

External Hamiltonian input: Mukohyama-Namba-Saitou-Watanabe, arXiv:1504.07357,
Eqs. (55)-(63), on eta1=eta2=0.  Eta0 is redundant and may be normalized to
eta0=1 (their Eq. 21); we retain eta0 symbolically and require eta0 != 0.

On a spatially flat homogeneous background with isotropic canonical momentum

    pi^{ij}=P g^{ij},  pi=d P,

and a Fourier smearing mode with |k|^2=k2, the common differential operator in
Eqs. (56),(57) has leading symbol

    O(k)= P (d-1)/(d lambda-1) k2.

Thus

    b={pi_N,phi_A} = -2 eta0 O = -B2 k2,
    c={J_A,Hperp}  = +2 eta0 O = +B2 k2,

where B2=2 eta0 P(d-1)/(d lambda-1).
Eq. (58) begins at O(k^4) on flat space.  Eq. (55) can depend on N only through
spatial lapse-gradient operators a_i and their derivatives on the homogeneous
background, so its symbol begins at O(k^2).  Therefore

    det B = a d - b c = B2^2 k^4 + O(k^6).

For B2 != 0 there is an open punctured low-k interval 0<k<epsilon in which the
pure-gravity cross block is nonsingular.  Exactly k=0 is a separate global mode:
all four local symbols may vanish there and must not be used as the propagating
rank test.
"""
import json
import sympy as sp

d=sp.symbols('d', integer=True, positive=True)
lam,P,eta0,k2=sp.symbols('lambda P eta0 k2', real=True, finite=True)
# Algebraic derivation of Eq.56/57 operator coefficient for isotropic pi^{ij}.
# D^2 -> -k2, pi=dP, pi^{ij}D_iD_j -> -P k2.
O=sp.factor(((lam-1)/(d*lam-1))*(d*P)*(-k2) - (-P*k2))
O_expected=sp.factor(P*(d-1)/(d*lam-1)*k2)
assert sp.simplify(O-O_expected)==0
B2=sp.factor(2*eta0*P*(d-1)/(d*lam-1))
b=sp.factor(-B2*k2)
c=sp.factor(B2*k2)
assert sp.simplify(-b*c-B2**2*k2**2)==0  # k2=|k|^2, so this is |k|^4.

# Analytic low-k bookkeeping: a=a2*k2+O(k2^2), dB=d4*k2^2+O(k2^3).
a2,d4,a4,d6=sp.symbols('a2 d4 a4 d6', finite=True)
a=sp.expand(a2*k2+a4*k2**2)
dentry=sp.expand(d4*k2**2+d6*k2**3)
det_trunc=sp.expand(a*dentry-b*c)
leading=sp.expand(det_trunc).coeff(k2,2)
assert sp.simplify(leading-B2**2)==0
assert sp.simplify(det_trunc-B2**2*k2**2).subs(k2,0)==0

# Exact global constant-mode caveat in the flat local-symbol limit.
assert b.subs(k2,0)==0 and c.subs(k2,0)==0
assert a.subs(k2,0)==0 and dentry.subs(k2,0)==0

out={
  'classification':'RTK_ROUTE_B_U1_FLAT_FLRW_LOWK_PURE_GRAVITY_RANK_PASS',
  'status_scope':'GREEN_PURE_GRAVITY_PUNCTURED_LOWK_RANK_BASELINE_COUPLED_FILTER_CORRECTIONS_PENDING',
  'external_input':'arXiv:1504.07357 Eqs. (55)-(63), special eta1=eta2=0 branch; eta0 may be normalized to 1 by Eq. (21)',
  'background':'spatially flat homogeneous metric with isotropic pi^{ij}=P g^{ij}',
  'fourier_symbol':{
    'k2':'|k|^2',
    'O_56_57':'P(d-1)/(d lambda-1) k2',
    'b':'-2 eta0 P(d-1)/(d lambda-1) k2',
    'c':'+2 eta0 P(d-1)/(d lambda-1) k2',
    'a':'O(k2) from lapse-gradient potential support on homogeneous flat background',
    'd_entry':'O(k2^2)=O(|k|^4) from Eq. (58) on R_ij=0'
  },
  'leading_determinant':'det B = [2 eta0 P(d-1)/(d lambda-1)]^2 |k|^4 + O(|k|^6)',
  'sufficient_nonzero_conditions':['eta0 != 0','P != 0 (rolling/expanding canonical gravity background)','d>1','d lambda != 1'],
  'punctured_interval_result':'By continuity/analyticity, if the leading coefficient is nonzero there exists epsilon>0 such that det B != 0 for every 0<|k|<epsilon.',
  'exact_k0_caveat':'For the exactly constant smearing mode on flat FLRW, the local symbols b,c and the displayed homogeneous-support a,d vanish. The global k=0 mode is therefore not a valid stand-alone local second-class rank certificate; physical scalar rank must be tested at k>0 and then approached as k->0+.',
  'interpretation':'The published special-U1 gravity sector has a robust nonzero leading low-k determinant on an expanding flat background even though the exact global zero mode is degenerate as a local Fourier symbol. This supplies the baseline against which filtered-matter and RTK finite-k corrections must be bounded.',
  'non_claims':[
    'does not yet include the projected filtered-matter metric-resolvent corrections at finite k',
    'does not include inhomogeneous RTK mixed-operator corrections at finite k',
    'does not provide a numerical epsilon without a bound on higher-order coefficients',
    'does not promote the exact k=0 global mode to a propagating-DOF rank test'
  ],
  'next_gate':'derive the O(|k|^2) corrections to b and c from Jhat=Jg-a_eff H0 using delta L^{-1}=-L^{-1}(delta L)L^{-1}; require the corrected leading coefficient of det B to stay nonzero before choosing M_c.'
}
with open('u1_flat_flrw_lowk_pure_gravity_rank_result.json','w') as f:
    json.dump(out,f,indent=2,sort_keys=True); f.write('\n')
print(out['classification'],json.dumps(out,sort_keys=True))
