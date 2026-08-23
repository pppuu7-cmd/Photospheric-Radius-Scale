#!/usr/bin/env python3
"""Exact finite-q zero classification of the filtered off-diagonal pair.

On the flat homogeneous projected support, the exact total off-diagonal
amplitude is
  F(q)=b2 q+c_m(q),
with
  c_m/q = V[M_c^2 H0/(M_c^2+q)^2-tau_H/(M_c^2+q)]
and
  V/b2=-2/[eta0(d-1)M_Pl^2 sqrt(g)].
Writing rho=H0/sqrt(g), tau=tau_H/sqrt(g),
  K=2/[eta0(d-1)M_Pl^2], s=M_c^2+q,
F(q)=0 for q>0 is equivalent to
  s^2+K tau s-K M_c^2 rho=0.
For K>0,rho>0 this quadratic has exactly one positive s root. Since its value
at s=M_c^2 is M_c^2[M_c^2-K(rho-tau)], a physical q>=0 root exists iff
M_c^2<=R=K(rho-tau), assuming rho-tau>0. Equality places the root at q=0;
strict M_c^2<R gives one positive finite-q root; M_c^2>R gives none.

A zero of F is only a candidate full-rank locus because diagonal a*d can still
keep det B nonzero at finite q.
"""
import json
import sympy as sp

m2,K,rho,tau,s,q=sp.symbols('M_c_squared K rho tau s q', positive=True, finite=True)
# tau is not necessarily positive physically; use an unrestricted replacement
tauR=sp.symbols('tau_rho', real=True, finite=True)
P=sp.expand(s**2+K*tauR*s-K*m2*rho)
R=sp.expand(K*(rho-tauR))
Pm=sp.factor(P.subs(s,m2))
assert sp.simplify(Pm-m2*(m2-R))==0
# Formal positive root.
disc=sp.expand(K**2*tauR**2+4*K*m2*rho)
splus=(-K*tauR+sp.sqrt(disc))/2
assert sp.simplify(P.subs(s,splus))==0
# Reconstruct exact normalized amplitude polynomial after multiplying by s^2.
normalized=sp.simplify(1-K*(m2*rho/s**2-tauR/s))
assert sp.simplify(normalized-P/s**2)==0

out={
  'classification':'RTK_ROUTE_B_U1_FILTERED_MATTER_EXACT_OFFDIAGONAL_ROOT_PASS',
  'status_scope':'GREEN_EXACT_OFFDIAGONAL_ZERO_CLASSIFICATION_FULL_DETERMINANT_AT_ROOT_PENDING',
  'domain':'flat homogeneous projected support; eta0>0 so K>0; rho>0; rho-tau_rho>0 for the simple root-location classification',
  'K':'2/[eta0(d-1)M_Pl^2]',
  'R':'K(rho-tau_rho)',
  'root_equation':'s^2+K tau_rho s-K M_c^2 rho=0, s=M_c^2+q',
  'positive_s_root':'[-K tau_rho+sqrt(K^2 tau_rho^2+4 K M_c^2 rho)]/2',
  'classification_by_Mc':{
    'M_c^2>R':'no off-diagonal zero for q>=0',
    'M_c^2=R':'off-diagonal leading coefficient vanishes only at q=0',
    '0<M_c^2<R':'exactly one positive finite-q off-diagonal zero q*=s_+-M_c^2'
  },
  'reinterpretation_of_conservative_bound':'M_c^2>R is not necessary for punctured-low-k rank, but under the stated positive-matter assumptions it is the exact criterion for eliminating all q>=0 zeros of the off-diagonal pair in the rational elliptic-filter symbol.',
  'warning':'F(q*)=0 is not automatically det B(q*)=0 because finite-q diagonal a(q*) d(q*) may be nonzero.',
  'non_claims':[
    'does not classify the full determinant at a finite-q off-diagonal root',
    'does not include time-dependent evolution of rho,tau_rho across different backgrounds in one fixed number',
    'does not choose M_c',
    'does not cover eta0<=0 or exotic rho-tau_rho<=0 with the simplified iff statement'
  ],
  'next_gate':'for any allowed branch with M_c^2<=R, evaluate a(q*)d(q*) using the compressed UV lapse symbol and total d(q) support; for M_c^2>R, combine the nonzero off-diagonal margin with EFT bounds to certify a wider k interval.'
}
open('u1_filtered_matter_exact_offdiagonal_root_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
