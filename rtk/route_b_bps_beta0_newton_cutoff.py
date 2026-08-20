#!/usr/bin/env python3
"""Exact Route-B BPS cutoff optimum at fixed measured Newton constant for beta=0.

Primary source: Blas, Pujolas, Sibiryakov, arXiv:1007.3503.
- Eq. (2.10): M_lambda^2=(lambda-1) M_P^2, M_alpha^2=alpha M_P^2.
- Eqs. (5.14)-(5.15): low-energy momentum/frequency cutoffs.
- Eq. (5.30), whose beta=0 form is stated to follow directly from action (2.5):
    G_N = 1/[8 pi M_P^2 (1-alpha/2)]  (beta=0).

Define the measured reduced Newton Planck scale
    Mbar_N^2 = 1/(8 pi G_N).
Then Mbar_N = M_P sqrt(1-alpha/2), so the physical cutoff in measured
Newton units differs from the bare-M_P cutoff used in the quadratic BPS action.

This theorem composes that exact beta=0 normalization with the already checked
RTK-target inverse family and obtains the global momentum-cutoff optimum.
It is deliberately CONDITIONAL on beta=0.  The pure-gravity pole embedding does
not by itself fix the matter metric/beta, so this result must not be promoted to
a generic matter-coupled completion.
"""
import json
import sympy as sp

C,h=sp.symbols('C h', positive=True, finite=True, real=True)
alpha=sp.simplify(2*h/(3*C+h))
ell=sp.simplify(2*h/(3*(1-h)))
ratio=sp.simplify(ell/alpha)

# Exact Newton normalization for beta=0:
# Mbar_N^2/M_P^2 = 1-alpha/2 = 3C/(3C+h).
newton_factor_sq=sp.simplify(1/(1-alpha/2)) # (M_P/Mbar_N)^2
assert sp.simplify(newton_factor_sq-(3*C+h)/(3*C))==0

# Bare-BPS momentum cutoffs in fourth-power form.
F_low4=sp.simplify(ell**3/alpha)       # ell<=alpha
F_high4=sp.simplify(alpha**3/ell)     # ell>=alpha
# Physical fixed-G_N cutoff G=Lambda_p/Mbar_N.
G_low4=sp.factor(sp.simplify(F_low4*newton_factor_sq**2))
G_high4=sp.factor(sp.simplify(F_high4*newton_factor_sq**2))
assert sp.simplify(G_low4-4*h**2*(3*C+h)**3/(243*C**2*(1-h)**3))==0
assert sp.simplify(G_high4-4*h**2*(1-h)/(3*C**2*(3*C+h)))==0

# The ell=alpha branch boundary from the exact inverse family.
h_bal=sp.simplify(3*(1-C)/4)
assert sp.simplify(ratio.subs(h,h_bal)-1)==0

# Low branch: strictly increasing on its physical interval 0<h<1.
dlow=sp.factor(sp.diff(G_low4,h))
# The displayed derivative has positive sign because, for 0<h<1,C>0,
# 2h^2-5h-3Ch-6C < 0.
assert sp.simplify(dlow + 4*h*(3*C+h)**2*(2*h**2-5*h-3*C*h-6*C)/(243*C**2*(1-h)**4))==0

# High branch: unique positive stationary point solves
#   2h^2+(9C-1)h-6C=0.
q=sp.factor(2*h**2+(9*C-1)*h-6*C)
dhigh=sp.factor(sp.diff(G_high4,h))
assert sp.simplify(dhigh + 4*h*q/(3*C**2*(3*C+h)**2))==0
D=sp.sqrt(81*C**2+30*C+1)
hN=sp.simplify((1-9*C+D)/4)
assert sp.simplify(q.subs(h,hN))==0

# Compare the high-branch stationary point with the branch boundary.
# hN-h_bal=[sqrt(81C^2+30C+1)-6C-2]/4.
assert sp.simplify(hN-h_bal-(D-6*C-2)/4)==0
# Squared sign discriminator:
# D^2-(6C+2)^2=3(5C-1)(3C+1), hence the regime switch C=1/5.
assert sp.factor(D**2-(6*C+2)**2-3*(5*C-1)*(3*C+1))==0

# At the balance point, physical cutoff simplifies exactly.  A bare SymPy
# sqrt keeps Abs(1-C); encode the physical balance domain 0<C<1 explicitly
# via C=u/(1+u), u>0, rather than relying on an implicit inequality solver.
G_bal4=sp.factor(sp.simplify(G_low4.subs(h,h_bal)))
assert sp.simplify(G_bal4-(1-C)**2/(4*C**2))==0
u=sp.symbols('u', positive=True, finite=True, real=True)
C01=sp.simplify(u/(1+u))
G_bal2_01=sp.simplify(sp.sqrt(G_bal4.subs(C,C01)))
assert sp.simplify(G_bal2_01-1/(2*u))==0
assert sp.simplify(((1-C)/(2*C)).subs(C,C01)-1/(2*u))==0

# Sufficient C8 frequency guard remains automatically weaker than the
# momentum window at the physical optimum.
# At balance: Lambda_w/Lambda_p=1 and C<=1/5 => sqrt(2C)<1.
# At hN (C>=1/5): r=ell/alpha > 2C.  Prove using the stationary relation by
# parameterizing C through h on the physical root branch h in [3/5,2/3).
hh=sp.symbols('hh', positive=True, finite=True, real=True)
C_h=sp.simplify(hh*(1-2*hh)/(9*hh-6))
r_h=sp.factor(((3*C+h)/(3*(1-h))).subs({C:C_h,h:hh}))
diff_h=sp.factor(r_h-2*C_h)
assert sp.simplify(r_h + hh/(3*(3*hh-2)))==0
assert sp.simplify(diff_h-hh*(4*hh-3)/(3*(3*hh-2)))==0
# For 3/5<=h<2/3, numerator and denominator of the latter are both negative,
# hence diff_h>0. This is recorded as a domain proof rather than delegated to
# an unreliable symbolic inequality solver.

out={
  'classification':'RTK_ROUTE_B_BPS_BETA0_NEWTON_CUTOFF_PASS',
  'scope':'conditional beta=0 universal/minimal matter-metric branch; not generic matter coupling',
  'primary_source':'Blas-Pujolas-Sibiryakov arXiv:1007.3503 Eqs. (2.10), (5.14), (5.15), (5.30) and beta=0 footnote',
  'newton_normalization':{
    'Mbar_N':'(8 pi G_N)^(-1/2)',
    'beta0_relation':'Mbar_N = M_P sqrt(1-alpha/2)',
    'inverse_family_factor':'M_P/Mbar_N = sqrt[(3C+h)/(3C)]'
  },
  'physical_cutoff_fourth_power':{
    'ell_le_alpha':'(Lambda_p/Mbar_N)^4 = 4 h^2 (3C+h)^3/[243 C^2 (1-h)^3]',
    'ell_ge_alpha':'(Lambda_p/Mbar_N)^4 = 4 h^2(1-h)/[3 C^2(3C+h)]'
  },
  'global_optimum':{
    '0<C<=1/5':{
      'h_opt':'3(1-C)/4',
      'alpha_opt=ell_opt':'2(1-C)/(1+3C)',
      'Lambda_p_max_over_Mbar_N':'sqrt[(1-C)/(2C)]'
    },
    'C>=1/5':{
      'h_opt':'[1-9C+sqrt(81C^2+30C+1)]/4',
      'Lambda_p_max_over_Mbar_N':'{4 h_opt^2(1-h_opt)/[3 C^2(3C+h_opt)]}^{1/4}',
      'branch':'ell>=alpha'
    },
    'regime_boundary':'C=1/5 (not C=1/3 as in the bare-M_P optimization)'
  },
  'frequency_guard':'At the beta=0 physical optimum the C8 sufficient frequency condition is weaker than the momentum condition: balance branch has Lambda_w/Lambda_p=1 with C<=1/5; high branch has ell/alpha>2C.',
  'interpretation':'Fixing measured G_N changes the optimization because the bare BPS M_P depends on alpha. The beta=0 physical optimum therefore differs from the bare-M_P optimum.',
  'guards':['beta=0 is an additional matter-coupling choice not fixed by the pure-gravity quadratic embedding','does not establish PPN viability','does not establish off-shell source equivalence, radiative stability or nonlinear DOF closure','generic beta requires a separate matter-metric normalization theorem'],
  'next_step':'Use the state-driven C(a),M_K(a) dictionary to evaluate the beta=0 physical hierarchy, and separately derive/source the generic-beta matter-metric map before making a generic completion claim.'
}
print('RTK_ROUTE_B_BPS_BETA0_NEWTON_CUTOFF_PASS',json.dumps(out,sort_keys=True))
