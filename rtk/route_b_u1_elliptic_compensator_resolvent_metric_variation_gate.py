#!/usr/bin/env python3
"""Resolvent/metric-variation theorem for the elliptic compensator filter.

Let L=1-D^2/M_c^2 on a spatial slice with boundary conditions for which
K=-D^2 is nonnegative self-adjoint.  Then L=1+K/M_c^2 >= 1 is strictly
positive, L^{-1} exists, and the projected coupling operator is

    a_eff = I-L^{-1}.

The exact inverse-variation identity is

    delta L^{-1} = -L^{-1}(delta L)L^{-1},
    delta a_eff  =  L^{-1}(delta L)L^{-1}
                 = -(1/M_c^2)L^{-1}[delta(D^2)]L^{-1}.

Consequently ||L^{-1}||<=1 and
||delta a_eff|| <= ||delta(D^2)||/M_c^2 in operator norm.  This localizes all
metric dependence of the filtered source that is invisible in the c-number
Fourier-symbol support gate.
"""
import json
import sympy as sp

# Spectral theorem check on an arbitrary nonnegative eigenvalue kappa.
kappa,Mc=sp.symbols('kappa M_c', nonnegative=True, positive=False)
# Re-declare Mc strictly positive separately to avoid ambiguous assumptions.
Mc=sp.symbols('M_c', positive=True, finite=True)
kappa=sp.symbols('kappa', nonnegative=True, finite=True)
Linveig=sp.factor(1/(1+kappa/Mc**2))
aeffeig=sp.factor(1-Linveig)
assert sp.simplify(aeffeig-kappa/(Mc**2+kappa))==0
assert sp.simplify(Linveig.subs(kappa,0)-1)==0
assert sp.simplify(aeffeig.subs(kappa,0))==0
assert sp.simplify(sp.limit(Linveig,kappa,sp.oo))==0
assert sp.simplify(sp.limit(aeffeig,kappa,sp.oo)-1)==0
assert sp.simplify(sp.diff(Linveig,kappa)+Mc**2/(Mc**2+kappa)**2)==0
assert sp.simplify(sp.diff(aeffeig,kappa)-Mc**2/(Mc**2+kappa)**2)==0

# Exact finite-dimensional representative of the universal inverse derivative
# identity.  The identity follows generally from delta(LL^{-1})=0; this symbolic
# 2x2 check protects signs/order in the implementation.
t=sp.symbols('t', real=True)
a,b,c,d,e,f=sp.symbols('a b c d e f', finite=True)
L0=sp.Matrix([[a,b],[b,c]])
dL=sp.Matrix([[d,e],[e,f]])
L=L0+t*dL
Linv=L.inv()
deriv=sp.simplify(Linv.diff(t).subs(t,0))
expected=sp.simplify(-L0.inv()*dL*L0.inv())
assert all(sp.simplify(x)==0 for x in (deriv-expected))

daeff=sp.simplify(-deriv)
expected_aeff=sp.simplify(L0.inv()*dL*L0.inv())
assert all(sp.simplify(x)==0 for x in (daeff-expected_aeff))

out={
  'classification':'RTK_ROUTE_B_U1_ELLIPTIC_COMPENSATOR_RESOLVENT_METRIC_VARIATION_PASS',
  'status_scope':'GREEN_EXACT_OPERATOR_VARIATION_BOUND_PHYSICAL_PFAFFIAN_PENDING',
  'operator':'L=1-D^2/M_c^2 = 1+(-D^2)/M_c^2',
  'assumption':'spatial boundary conditions make -D^2 nonnegative self-adjoint; M_c>0',
  'spectral_results':{
    'L_inverse_eigenvalue':'1/(1+kappa/M_c^2) in (0,1] for kappa>=0',
    'a_eff_eigenvalue':'kappa/(M_c^2+kappa) in [0,1)',
    'no_filter_pole':'L has no zero eigenvalue on the assumed physical domain'
  },
  'exact_variation':{
    'delta_L_inverse':'-L^{-1}(delta L)L^{-1}',
    'delta_a_eff':'L^{-1}(delta L)L^{-1}=-(1/M_c^2)L^{-1}[delta(D^2)]L^{-1}'
  },
  'operator_norm_bound':'||delta a_eff|| <= ||delta(D^2)||/M_c^2 because ||L^{-1}||<=1',
  'interpretation':'Metric dependence of the reduced filtered matter source is completely controlled by a resolvent sandwich. There are no hidden poles from the auxiliary filter on the positive elliptic branch; finite-k rank corrections can be organized explicitly as insertions of delta(D^2) between bounded L^{-1} factors.',
  'non_claims':[
    'does not bound delta(D^2) on an arbitrary nonlinear geometry',
    'does not prove the reduced U1 Pfaffian remains nonzero',
    'does not choose M_c',
    'does not address radiative stability of the exceptional gravity surface'
  ],
  'next_gate':'use the resolvent sandwich in the functional metric Poisson brackets of Jhat with H_perp_hat/phi_hat and derive a quantitative sufficient bound excluding Pfaffian zeros in a specified perturbative geometry domain.'
}
with open('u1_elliptic_compensator_resolvent_metric_variation_result.json','w') as fp:
    json.dump(out,fp,indent=2,sort_keys=True); fp.write('\n')
print(out['classification'],json.dumps(out,sort_keys=True))
