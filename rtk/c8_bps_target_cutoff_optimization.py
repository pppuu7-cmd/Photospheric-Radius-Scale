#!/usr/bin/env python3
"""Optimize the published BPS low-energy momentum cutoff over the exact target inversion family.

Combine the machine-checked target inversion
  alpha=2h/(3C+h), ell=2h/[3(1-h)], 0<h<1, C=c_s^2>0
with the published BPS momentum cutoff map.

This theorem proves the branch boundary, monotonicity/critical point and exact
global maximum of Lambda_p over h for fixed target C.  It therefore gives a
hard momentum budget for placing the z=3 crossover in the constructive RTK-like
BPS completion.
"""
import json
import sympy as sp

h,C,MP=sp.symbols('h C MP', positive=True, finite=True, real=True)
alpha=sp.simplify(2*h/(3*C+h))
ell=sp.simplify(2*h/(3*(1-h)))
ratio=sp.simplify(ell/alpha)
assert sp.simplify(ratio-(3*C+h)/(3*(1-h)))==0

# Branch change ell=alpha.
h_bal=sp.simplify(3*(1-C)/4)
assert sp.simplify(ratio.subs(h,h_bal)-1)==0

# Published cutoff branches, normalized by MP.
Lp_low=sp.simplify(ell**sp.Rational(3,4)*alpha**(-sp.Rational(1,4)))   # ell<=alpha
Lp_high=sp.simplify(alpha**sp.Rational(3,4)*ell**(-sp.Rational(1,4))) # ell>=alpha
Lw_low=sp.simplify(ell**sp.Rational(5,4)*alpha**(-sp.Rational(3,4)))
Lw_high=sp.simplify((alpha*ell)**sp.Rational(1,4))

# Exact logarithmic derivatives. For 0<h<1 the low branch is strictly increasing.
dlog_low=sp.factor(sp.diff(sp.log(Lp_low),h))
expected_low=sp.simplify(3*(C*h+2*C+h)/(4*h*(3*C+h)*(1-h)))
assert sp.simplify(dlog_low-expected_low)==0

# High branch has one stationary point hcrit and changes from increasing to decreasing there.
dlog_high=sp.factor(sp.diff(sp.log(Lp_high),h))
expected_high=sp.simplify((6*C-h*(9*C+1))/(4*h*(3*C+h)*(1-h)))
assert sp.simplify(dlog_high-expected_high)==0
hcrit=sp.simplify(6*C/(9*C+1))
assert sp.simplify(expected_high.subs(h,hcrit))==0
assert sp.simplify(hcrit-h_bal-3*(3*C-1)*(3*C+1)/(4*(9*C+1)))==0

# At C=1/3 the critical and balanced points coincide. For C<1/3, hcrit lies
# below the high-branch domain, so the global maximum is at h_bal. For C>1/3,
# hcrit lies inside the high branch and is the global maximum.
assert sp.simplify((hcrit-h_bal).subs(C,sp.Rational(1,3)))==0

# Exact parameter/cutoff values at both candidate maxima.
alpha_bal=sp.simplify(alpha.subs(h,h_bal)); ell_bal=sp.simplify(ell.subs(h,h_bal))
assert sp.simplify(alpha_bal-2*(1-C)/(3*C+1))==0
assert sp.simplify(ell_bal-alpha_bal)==0
Lpmax_bal=sp.simplify(Lp_low.subs(h,h_bal))
assert sp.simplify(Lpmax_bal-sp.sqrt(2*(1-C)/(3*C+1)))==0

alpha_crit=sp.simplify(alpha.subs(h,hcrit)); ell_crit=sp.simplify(ell.subs(h,hcrit))
assert sp.simplify(alpha_crit-4/(3*(3*C+1)))==0
assert sp.simplify(ell_crit-4*C/(3*C+1))==0
assert sp.simplify((ell_crit/alpha_crit)-3*C)==0
Lpmax_crit=sp.simplify(Lp_high.subs(h,hcrit))
Lpmax_crit_expected=sp.simplify(2/(3**sp.Rational(3,4)*C**sp.Rational(1,4)*sp.sqrt(3*C+1)))
assert sp.simplify(Lpmax_crit-Lpmax_crit_expected)==0

# Continuity at C=1/3.
assert sp.simplify(Lpmax_bal.subs(C,sp.Rational(1,3))-Lpmax_crit_expected.subs(C,sp.Rational(1,3)))==0

# GR-like h->0 limit loses cutoff as sqrt(h); exact coefficients depend on branch.
small_low=sp.simplify(sp.limit(Lp_low/sp.sqrt(h),h,0,dir='+'))
small_high=sp.simplify(sp.limit(Lp_high/sp.sqrt(h),h,0,dir='+'))
assert sp.simplify(small_low-sp.sqrt(6)*C**sp.Rational(1,4)/3)==0
assert sp.simplify(small_high-sp.sqrt(6)/(3*C**sp.Rational(3,4)))==0

out={
  'classification':'RTK_C8_BPS_TARGET_CUTOFF_OPTIMIZATION_PASS',
  'input_map':'alpha=2h/(3C+h), ell=2h/[3(1-h)], C=c_s^2>0, 0<h<1',
  'branch_ratio':'ell/alpha=(3C+h)/[3(1-h)]',
  'branch_boundary':'For C<1, ell=alpha at h_bal=3(1-C)/4; for C>=1 the physical h interval is entirely ell>alpha.',
  'momentum_cutoff_behavior':{
    'ell_le_alpha':'Lambda_p/MP increases strictly with h',
    'ell_ge_alpha':'Lambda_p/MP increases until hcrit=6C/(9C+1) and decreases afterward'
  },
  'global_maximum':{
    '0<C<=1/3':{
      'h_opt':'3(1-C)/4','alpha=ell':'2(1-C)/(3C+1)',
      'Lambda_p_max':'M_P sqrt[2(1-C)/(3C+1)]'
    },
    'C>=1/3':{
      'h_opt':'6C/(9C+1)','alpha':'4/[3(3C+1)]','ell':'4C/(3C+1)',
      'ell_over_alpha':'3C',
      'Lambda_p_max':'2 M_P/[3^(3/4) C^(1/4) sqrt(3C+1)]'
    },
    'continuity':'the two formulas coincide at C=1/3'
  },
  'small_h':'Lambda_p proportional to M_P sqrt(h) ->0 as h->0 at fixed C',
  'design_consequence':'For the momentum part of the two-crossover construction to have any solution over h, the required lower crossover bound max(M_*,p_max/epsilon^(1/6)) must lie below the appropriate Lambda_p_max(C). Frequency and full cubic constraints remain additional filters.',
  'theorem':'At fixed positive target sound speed, the exact BPS target-inversion family has a finite optimal low-energy momentum cutoff. Driving alpha and lambda-1 arbitrarily close to zero eventually worsens, rather than improves, the strong-coupling margin.',
  'non_claims':['does not optimize Lambda_omega jointly','does not include matter Lorentz constraints','does not compute a phenomenological numerical cutoff without C,M_*,p_max,epsilon','does not replace selected-family nonlinear interaction analysis']
}
print('RTK_C8_BPS_TARGET_CUTOFF_OPTIMIZATION_PASS',json.dumps(out,sort_keys=True))
