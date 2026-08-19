#!/usr/bin/env python3
"""Constructive inversion from an arbitrary positive RTK target dispersion to BPS parameters.

Input target:
  omega^2 = C p^2/(1+p^2/Mdisp^2), C>0, Mdisp>0.

For any auxiliary tuning parameter 0<h<1, this theorem constructs positive BPS
parameters z, ell=lambda-1, alpha and s such that the exact healthy-BPS rational
pole family reproduces exactly the target C and Mdisp.  As h->0, both low-energy
Lorentz-violating parameters alpha and ell tend to zero while the target sound
speed C remains fixed.

Scope: inverse pole/dispersion map only.  It does not solve the off-shell
source/residue map, nonlinear constraint problem, strong coupling or radiative
stability.
"""
import json
import sympy as sp

C,Mdisp,h=sp.symbols('C Mdisp h', positive=True, finite=True, real=True)
# We explicitly parameterize h=k/(1+k), so 0<h<1 is machine-manifest.
k=sp.symbols('k', positive=True, finite=True, real=True)
hk=sp.simplify(k/(1+k))

# Constructive inverse family.
def family(H):
    z=sp.simplify(H/(3*C))
    ell=sp.simplify(2*H/(3*(1-H)))
    alpha=sp.simplify(2*H/(3*C+H))
    s=alpha
    Muv=Mdisp
    cs2=sp.simplify(ell/(z*(2+3*ell)))
    Mdisp2_from_bps=sp.simplify(alpha*Muv**2/s)
    return z,ell,alpha,s,Muv,cs2,Mdisp2_from_bps

z,ell,alpha,s,Muv,cs2,M2=family(hk)
assert sp.simplify(cs2-C)==0
assert sp.simplify(M2-Mdisp**2)==0

# Positivity and healthy parameter intervals are manifest under C,k>0.
assert z.is_positive is True
assert ell.is_positive is True
assert alpha.is_positive is True
# alpha<2: exact positive margin.
alpha_margin=sp.simplify(2-alpha)
assert sp.ask(sp.Q.positive(alpha_margin)) is True
# lambda=1+ell>1, f3=-s<0 and source-paper ghost ratio positive.
lam=sp.simplify(1+ell)
ghost_ratio=sp.simplify((3*lam-1)/(lam-1))
assert sp.ask(sp.Q.positive(ghost_ratio)) is True

# As h->0 (equivalently k->0), alpha and ell approach GR-like zero while C is fixed.
assert sp.limit(alpha,k,0,dir='+')==0
assert sp.limit(ell,k,0,dir='+')==0
assert sp.limit(z,k,0,dir='+')==0
assert sp.simplify(cs2-C)==0

# Exact first-order small-h scaling for interpretation.
alpha_over_h=sp.simplify(alpha/hk)
ell_over_h=sp.simplify(ell/hk)
assert sp.limit(alpha_over_h,k,0,dir='+')==sp.simplify(2/(3*C))
assert sp.limit(ell_over_h,k,0,dir='+')==sp.Rational(2,3)

out={
  'classification':'RTK_ROUTE_B_BPS_TARGET_INVERSION_PASS',
  'target':'omega^2=C p^2/(1+p^2/Mdisp^2), C>0, Mdisp>0',
  'free_tuning':'h in (0,1), parameterized as h=k/(1+k) with k>0',
  'inverse_map':{
    'z':'h/(3C)',
    'ell=lambda-1':'2h/[3(1-h)]',
    'alpha':'2h/(3C+h)',
    's':'alpha',
    'M_*':'Mdisp'
  },
  'exact_checks':{
    'c_s^2':'ell/[z(2+3ell)] = C exactly',
    'Mdisp^2':'alpha M_*^2/s = Mdisp^2 exactly',
    'healthy_interval':'0<alpha<2 and lambda>1 for all C>0, 0<h<1'
  },
  'small_h_limit':{
    'alpha':'~2h/(3C) ->0',
    'ell':'~2h/3 ->0',
    'z':'~h/(3C) ->0',
    'target_C':'remains exactly fixed'
  },
  'theorem':'Every positive rational target pole of the RTK form admits a continuous healthy-BPS exact pole/dispersion embedding. The low-energy alpha and lambda-1 parameters can simultaneously be made arbitrarily small at fixed target C and Mdisp by taking h->0.',
  'guards':['pole/dispersion only, not off-shell residue/source equivalence','small alpha,ell do not automatically guarantee a usable strong-coupling window because the BPS cutoffs also decrease','matter Lorentz-violation and cosmological stability constraints remain separate'],
  'next_step':'Combine this inverse map with the exact C8 BPS cutoff/window formulas to identify which h values preserve both phenomenological target accuracy and a pre-strong-coupling z=3 crossover.'
}
print('RTK_ROUTE_B_BPS_TARGET_INVERSION_PASS',json.dumps(out,sort_keys=True))
