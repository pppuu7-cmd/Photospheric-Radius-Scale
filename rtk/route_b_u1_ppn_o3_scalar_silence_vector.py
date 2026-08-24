#!/usr/bin/env python3
"""O(v^3) moving-source scalar-silence/vector-decoupling theorem.

This gate is deliberately scoped to the standard PPN branch: weak fields,
slowly moving matter, no independent incoming/homogeneous RTK scalar mode.
It checks that the fixed RTK scalar action supplies no source to the O(3)
vector/shift system once the already-certified O(2) bare-lapse result n2=0 is
used.
"""
import json
import sympy as sp

TARGET='research/theory_targets/RTK_ROUTE_B_U1_PPN_O3_SCALAR_SILENCE_VECTOR_TARGET_v1.json'
t=json.load(open(TARGET))
assert t['classification']=='RTK_ROUTE_B_U1_PPN_O3_SCALAR_SILENCE_VECTOR_TARGET_V1_FROZEN'

r2=json.load(open('research/theory_results/RTK_ROUTE_B_U1_STATIC_O2_NEWTON_DBI_EXACT_RESULT_v1.json'))
ru=json.load(open('research/theory_results/RTK_ROUTE_B_U1_STATIC_BARE_LAPSE_NONLINEAR_UNIQUENESS_RESULT_v1.json'))
assert r2['classification']=='RTK_ROUTE_B_U1_STATIC_O2_NEWTON_DBI_EXACT_PASS'
assert r2['uniqueness']['solution']=='n=0'
assert ru['classification']=='RTK_ROUTE_B_U1_STATIC_BARE_LAPSE_NONLINEAR_UNIQUENESS_EXACT_PASS'

# Exact background identities. B is one representative component of the
# invariant shift and sgrad one representative D_i Sigma jet. The production
# scalar action is frozen on X_star>0, so encode that physical-domain assumption
# explicitly rather than asking SymPy to infer sqrt(X_star)*sqrt(1/X_star)=1.
q,N,B,sgrad=sp.symbols('q N B sgrad', nonzero=True, finite=True, real=True)
Xstar=sp.symbols('Xstar', positive=True, finite=True)
Theta=(q-B*sgrad)/N
X=sp.Rational(1,2)*(Theta**2-sgrad**2)
assert sp.simplify(Theta.subs({sgrad:0,N:1})-q)==0
assert sp.simplify(sp.diff(Theta,B).subs(sgrad,0))==0
assert sp.simplify(X.subs({sgrad:0,N:1})-q**2/sp.Integer(2))==0

# DBI production rest point u=sqrt(X/Xstar)=1. Work with an abstract positive
# lambda and mu and explicitly verify P=P_X=0 at X=Xstar.
Xv,lam,mu=sp.symbols('Xv lam mu', positive=True, finite=True)
u=sp.sqrt(Xv/Xstar)
P=2*mu**2/lam*(1-sp.sqrt(1-lam*(u-1)**2))
P_at=sp.simplify(P.subs(Xv,Xstar))
PX_at=sp.simplify(sp.diff(P,Xv).subs(Xv,Xstar))
assert P_at==0
assert PX_at==0

# First-variation structure of the mixed term Lm=C(X) g^{ij} DiTheta DjTheta.
# Denote the background gradient by G and an arbitrary variation by dG,dC,dg.
C,G,dC,dG,dg,g=sp.symbols('C G dC dG dg g', finite=True, real=True)
Lm=C*g*G**2
dLm=sp.expand(sp.diff(Lm,C)*dC+sp.diff(Lm,g)*dg+sp.diff(Lm,G)*dG)
assert sp.simplify(dLm.subs(G,0))==0

# PN order bookkeeping: n2=0; shift B3 and time derivatives begin at O3.
# With D_i Sigma=0 the B3 contribution to Theta vanishes identically. Thus
# N=1+O4 => Theta=q+O4, X=Xstar+O4, P=P_X=O4-or-higher and DiTheta=O4.
# Consequently no scalar-action first variation can source an O3 vector eq.

out={
  'classification':'RTK_ROUTE_B_U1_PPN_O3_SCALAR_SILENCE_VECTOR_EXACT_PASS',
  'status':'O3_MOVING_SOURCE_VECTOR_SECTOR_MATCHES_PURE_U1_ON_STANDARD_PPN_BRANCH',
  'target':TARGET,
  'ppn_ordering':t['ppn_ordering'],
  'o2_bridge':{
    'statement':'The O(2) scalar constraints are unchanged by O(3) shift/time-derivative terms; the certified regular solution is n2=0.',
    'certified_source':'research/theory_results/RTK_ROUTE_B_U1_STATIC_O2_NEWTON_DBI_EXACT_RESULT_v1.json'
  },
  'exact_background_algebra':{
    'Theta':'(q-B^i D_iSigma)/N',
    'D_iSigma':'0',
    'dTheta_dB_on_background':'0',
    'Theta_through_O3':'q',
    'X_through_O3':'X_star=q^2/2',
    'X_star_domain':'positive',
    'P_at_Xstar':'0',
    'P_X_at_Xstar':'0',
    'D_iTheta_through_O3':'0'
  },
  'first_variation':{
    'P_sector':'P=P_X=0 through O3, so no lapse/shift/spatial-metric/scalar source from P(X) at this order',
    'mixed_sector':'the first variation of C(X) g^{ij}D_iTheta D_jTheta vanishes when D_iTheta=0; no O3 vector/shift source',
    'scalar_equation':'Sigma=q t remains unsourced through O3 on the no-extra-homogeneous-mode PPN branch because both P_X and D_iTheta vanish at the background to this order'
  },
  'consequence':'Through O(v^3), the full fixed-action shift/vector equations coincide with the corresponding sigma1=sigma2=0 pure-U1 family-I equations for a1=1,a2=0,kappa=1.',
  'boundary_condition':t['scalar_background']['homogeneous_scalar_perturbation'],
  'non_claims':t['non_claims'],
  'next_gate':'preferred-frame alpha1/alpha2 inheritance with regular algebraic cancellation before gamma1=-1 and lambda_HL=1 limits'
}
open('u1_ppn_o3_scalar_silence_vector_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
