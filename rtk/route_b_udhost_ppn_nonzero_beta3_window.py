#!/usr/bin/env python3
"""Constructive PPN-safe nonzero-beta3 window for the Route-B U-DHOST rescue.

Primary source:
  Saito, Yao, Kobayashi, arXiv:2402.10459 / JCAP 06 (2024) 040,
  especially Eqs. (82)-(90) and Table 1.

At luminal tensor speed c_GW=1 the source gives
  gamma_PPN = 1 + alpha_H,
  alpha1_PPN = 4[2 gamma_PPN^2 - gamma_PPN - 1 - beta3],
  beta2 = -6 beta1^2/(1+alpha_L),
with alpha2_PPN given by Eq. (86).

This gate proves two distinct facts:
1. The exactly-GR PPN submanifold gamma=1, alpha1=0 requires beta3=0, so
   the exact GR-indistinguishable subclass cannot carry the RTK lapse-gradient
   operator.
2. The experimentally allowed PPN region is larger.  An explicit point with
   beta3=1e-6 != 0, alpha_H=0, alpha_L=1 and an exact algebraic beta1 root has
   gamma=1, beta=1 (for delta1=delta2=0), alpha2=0, and alpha1=-4e-6,
   which lies inside the source Table-1 alpha1 interval and therefore proves
   that nonzero beta3 is not excluded by PPN+luminal-GW constraints alone.

Scope: local PPN/EFT existence gate only. It does not yet prove that the
required cosmological RTK beta3=K/(M^2 M_K^2) lies inside the allowed window,
that one fixed action generates the full C(a),M_K(a) history, or compact-object
and radiative stability.
"""
import json
import sympy as sp

# Symbols and sourced luminal-GW formulas.
aH,b1,b3,aL,d1,d2 = sp.symbols('alpha_H beta1 beta3 alpha_L delta1 delta2', real=True, finite=True)
gamma = 1 + aH
alpha1 = sp.expand(4*(2*gamma**2-gamma-1-b3))
beta2 = sp.simplify(-6*b1**2/(1+aL))

# Exact-GR intersection: gamma=1 -> alpha_H=0; alpha1=0 then forces beta3=0.
assert sp.simplify(alpha1.subs(aH,0) + 4*b3) == 0
assert sp.solve(sp.Eq(alpha1.subs(aH,0),0),b3) == [0]

# Full sourced beta_PPN formula at c_GW=1.
beta_ppn = sp.simplify((4*gamma*(gamma*(1+gamma)+2*d1)-b3*(3+gamma)-2*d2)/(4*(2*gamma**2-b3)))

# Sourced alpha2_PPN Eq. (86), including the U-DHOST degeneracy beta2 relation.
alpha2 = sp.simplify(
    3*(2*(gamma+b1)-2*gamma**2-b3)**2/(2*(2*gamma**2-b3))*(1/aL+1)
    -1 + gamma**2 + 6*b1 - b3/sp.Integer(2)
    +(beta2-6*b1**2-12*b1*gamma)/(2*gamma**2-b3)
)

# Constructive nonzero-beta3 benchmark. beta3=1e-6 is safely nonzero and
# gives alpha1=-4e-6 when alpha_H=0, exactly at the central Table-1 value
# -0.4e-5 and hence inside the quoted uncertainty interval.
bench = {aH:sp.Integer(0), b3:sp.Rational(1,10**6), aL:sp.Integer(1), d1:sp.Integer(0), d2:sp.Integer(0)}
alpha1_bench = sp.simplify(alpha1.subs(bench))
beta_bench = sp.simplify(beta_ppn.subs(bench))
assert alpha1_bench == -sp.Rational(1,250000)  # -4e-6
assert beta_bench == 1
assert sp.simplify(gamma.subs(bench)-1) == 0

# Solve alpha2=0 exactly at the benchmark. There are two real nonzero beta1 roots.
alpha2_bench = sp.factor(alpha2.subs(bench))
roots = sp.solve(sp.Eq(alpha2_bench,0),b1)
assert len(roots)==2
for r in roots:
    assert sp.simplify(alpha2_bench.subs(b1,r)) == 0
    assert r != 0

# Source Table-1 alpha1 interval: -0.4^{+3.7}_{-3.1} x 1e-5.
lo = sp.Rational(-35,10)*sp.Rational(1,10**5)  # -3.5e-5
hi = sp.Rational(33,10)*sp.Rational(1,10**5)   # +3.3e-5
assert lo <= alpha1_bench <= hi

out={
  'classification':'RTK_ROUTE_B_UDHOST_PPN_NONZERO_BETA3_WINDOW_PASS',
  'primary_source':'Saito-Yao-Kobayashi arXiv:2402.10459 / JCAP 06 (2024) 040, Eqs. 82-90 and Table 1',
  'exact_GR_boundary':{
    'conditions':'c_GW=1, gamma_PPN=1, alpha1_PPN=0',
    'result':'beta3=0 exactly',
    'interpretation':'the exactly GR-indistinguishable PPN subclass cannot itself carry the RTK beta3 acceleration operator'
  },
  'constructive_allowed_point':{
    'alpha_H':0.0,'beta3':1e-6,'alpha_L':1.0,'delta1':0.0,'delta2':0.0,
    'beta1_roots':[sp.sstr(r) for r in roots],
    'beta1_roots_numeric':[float(sp.N(r,18)) for r in roots],
    'gamma_PPN':1.0,'beta_PPN':1.0,'alpha1_PPN':float(alpha1_bench),'alpha2_PPN':0.0,
    'unitary_beta2_relation':'beta2=-6 beta1^2/(1+alpha_L)'
  },
  'result':'PPN+luminal-GW+unitary-degeneracy constraints admit at least one explicit nonzero-beta3 point. Therefore PPN does not force the RTK acceleration channel to vanish; it only confines it to a small weak-field window.',
  'guards':[
    'the benchmark beta3=1e-6 is an existence witness, not yet the RTK-required cosmological value',
    'the source PPN derivation assumes alpha_L != 0 and a timelike scalar gradient',
    'scalar radiation/binary constraints are not included in this gate',
    'does not prove fixed-action FLRW matching, compact-object regularity, nonlinear hyperbolicity or radiative stability'
  ],
  'next_step':'Compute the dimensionless beta3 required by the replay-certified RTK C(a),M_K(a) after canonical normalization and compare it to the O(1e-5) PPN window; if too large locally, test X-dependent environmental/background separation in one fixed action.'
}
print('RTK_ROUTE_B_UDHOST_PPN_NONZERO_BETA3_WINDOW_PASS',json.dumps(out,sort_keys=True))
