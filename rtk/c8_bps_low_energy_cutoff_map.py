#!/usr/bin/env python3
"""Exact map of BPS low-energy strong-coupling cutoffs to alpha and ell=lambda-1.

Primary source: Blas, Pujolas, Sibiryakov, arXiv:1007.3503.
Eq. (2.10): M_lambda^2=(lambda-1) M_P^2, M_alpha^2=alpha M_P^2.
Eqs. (5.14)-(5.15):
  Lambda_p=min(M_alpha^-1/2 M_lambda^3/2,
               M_alpha^3/2 M_lambda^-1/2),
  Lambda_omega=min(M_alpha^1/2 M_lambda^1/2,
                   M_alpha^-3/2 M_lambda^5/2).

This script proves the exact branch formulas used for the constructive BPS RTK
completion. It does not itself prove that the higher-spatial sector turns on
before these cutoffs; that is a separate crossover-window condition.
"""
import json
import sympy as sp

alpha,ell,MP=sp.symbols('alpha ell MP', positive=True, finite=True, real=True)
Ma=sp.simplify(MP*sp.sqrt(alpha)); Ml=sp.simplify(MP*sp.sqrt(ell))
Lp1=sp.simplify(Ma**(-sp.Rational(1,2))*Ml**(sp.Rational(3,2)))
Lp2=sp.simplify(Ma**(sp.Rational(3,2))*Ml**(-sp.Rational(1,2)))
Lw1=sp.simplify(Ma**(sp.Rational(1,2))*Ml**(sp.Rational(1,2)))
Lw2=sp.simplify(Ma**(-sp.Rational(3,2))*Ml**(sp.Rational(5,2)))

# The ratio of the two candidates is exactly ell/alpha for both cutoff types.
assert sp.simplify(Lp1/Lp2-ell/alpha)==0
assert sp.simplify(Lw2/Lw1-ell/alpha)==0

# Branch ell<=alpha: Lp1 and Lw2 are the minima.
Lp_low=sp.simplify(MP*ell**sp.Rational(3,4)*alpha**(-sp.Rational(1,4)))
Lw_low=sp.simplify(MP*ell**sp.Rational(5,4)*alpha**(-sp.Rational(3,4)))
assert sp.simplify(Lp1-Lp_low)==0
assert sp.simplify(Lw2-Lw_low)==0

# Branch ell>=alpha: Lp2 and Lw1 are the minima.
Lp_high=sp.simplify(MP*alpha**sp.Rational(3,4)*ell**(-sp.Rational(1,4)))
Lw_high=sp.simplify(MP*(alpha*ell)**sp.Rational(1,4))
assert sp.simplify(Lp2-Lp_high)==0
assert sp.simplify(Lw1-Lw_high)==0

# Balanced point ell=alpha: both cutoffs equal M_alpha=M_lambda=MP sqrt(alpha).
bal={ell:alpha}
for expr in (Lp1,Lp2,Lw1,Lw2):
    assert sp.simplify(expr.subs(bal)-MP*sp.sqrt(alpha))==0

# Connect to the constructive BPS speed parameterization alpha=2z/(1+z).
z,C=sp.symbols('z C', positive=True, finite=True, real=True)
alpha_z=sp.simplify(2*z/(1+z))
cs2=sp.simplify(ell/(z*(2+3*ell)))
# Invert target C=cs2 for ell after eliminating z=alpha/(2-alpha).
ell_target=sp.simplify(2*C*alpha/(2-alpha*(1+3*C)))
z_alpha=sp.simplify(alpha/(2-alpha))
assert sp.simplify(cs2.subs({z:z_alpha,ell:ell_target})-C)==0
# At ell=alpha, the corresponding sound speed is exact.
C_bal=sp.simplify(cs2.subs({z:z_alpha,ell:alpha}))
assert sp.simplify(C_bal-(2-alpha)/(2+3*alpha))==0

out={
  'classification':'RTK_C8_BPS_LOW_ENERGY_CUTOFF_MAP_PASS',
  'primary_source':'Blas-Pujolas-Sibiryakov arXiv:1007.3503 Eqs. (2.10), (5.14), (5.15)',
  'definitions':{'M_alpha':'M_P sqrt(alpha)','M_lambda':'M_P sqrt(ell), ell=lambda-1'},
  'branch_ell_le_alpha':{
    'Lambda_p':'M_P ell^(3/4) alpha^(-1/4)',
    'Lambda_omega':'M_P ell^(5/4) alpha^(-3/4)'
  },
  'branch_ell_ge_alpha':{
    'Lambda_p':'M_P alpha^(3/4) ell^(-1/4)',
    'Lambda_omega':'M_P (alpha ell)^(1/4)'
  },
  'balanced_ell_eq_alpha':'Lambda_p=Lambda_omega=M_P sqrt(alpha)',
  'target_speed_inversion':'For z=alpha/(2-alpha), a desired C=c_s^2 requires ell=2 C alpha/[2-alpha(1+3C)] when the denominator is positive.',
  'balanced_speed':'If ell=alpha then c_s^2=(2-alpha)/(2+3alpha).',
  'use':'Insert these exact cutoffs into the independently machine-checked two-crossover feasibility condition p_UV<Lambda_p and the sufficient frequency guard sqrt(2)c_s M_*<Lambda_omega.',
  'non_claims':['does not itself establish the selected-family z=3 onset occurs below the cutoffs','does not include radiative corrections','does not prove matter-sector Lorentz constraints','does not replace full nonlinear constraint analysis']
}
print('RTK_C8_BPS_LOW_ENERGY_CUTOFF_MAP_PASS',json.dumps(out,sort_keys=True))
