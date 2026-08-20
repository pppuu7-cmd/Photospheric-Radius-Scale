#!/usr/bin/env python3
"""Exact BPS cutoff optimum under explicit low-energy LV parameter caps.

This theorem starts from the already machine-checked inverse family

  alpha(h)=2h/(3C+h),
  ell(h)=lambda-1=2h/[3(1-h)],
  0<h<1, C>0,

which reproduces an arbitrary positive RTK rational target pole exactly.
It asks a stricter question than the unconstrained cutoff theorem: what is the
largest BPS low-energy momentum cutoff if phenomenology imposes

  0 < alpha <= alpha_cap < 2,
  0 < ell   <= ell_cap,

with arbitrary positive caps?

The result is analytic: both alpha(h) and ell(h) are strictly increasing, so
the caps become exact upper bounds on h.  Since the unconstrained cutoff is
strictly increasing up to its unique global maximizer h0(C), the constrained
maximizer is simply min(h0,h_alpha,h_ell).  No parameter scan is required.

Scope: quadratic inverse family and BPS low-energy cutoff formulas only.  The
caps are abstract inputs; this script does not assert observational values for
them or prove matter-sector/radiative consistency.
"""
import json
import sympy as sp

C,h,A,E=sp.symbols('C h alpha_cap ell_cap', positive=True, finite=True, real=True)
alpha=sp.simplify(2*h/(3*C+h))
ell=sp.simplify(2*h/(3*(1-h)))

# Strict monotonicity on the physical domain 0<h<1.
dalpha=sp.factor(sp.diff(alpha,h))
dell=sp.factor(sp.diff(ell,h))
assert sp.simplify(dalpha-6*C/(3*C+h)**2)==0
assert sp.simplify(dell-2/(3*(1-h)**2))==0

# Exact cap inversions.  For 0<A<2 and E>0:
# alpha<=A iff h<=h_alpha; ell<=E iff h<=h_ell.
h_alpha=sp.simplify(3*A*C/(2-A))
h_ell=sp.simplify(3*E/(2+3*E))
assert sp.simplify(alpha.subs(h,h_alpha)-A)==0
assert sp.simplify(ell.subs(h,h_ell)-E)==0

# Exact BPS cutoff branches, F=Lambda_p/M_P.
# ell<=alpha -> F^4=ell^3/alpha; ell>=alpha -> F^4=alpha^3/ell.
F_low4=sp.factor(sp.simplify(ell**3/alpha))
F_high4=sp.factor(sp.simplify(alpha**3/ell))
assert sp.simplify(F_low4-4*h**2*(3*C+h)/(27*(1-h)**3))==0
assert sp.simplify(F_high4-12*h**2*(1-h)/(3*C+h)**3)==0

# Branch selector ell/alpha <= 1 iff 4h <= 3(1-C).
ratio=sp.factor(sp.simplify(ell/alpha))
assert sp.simplify(ratio-(3*C+h)/(3*(1-h)))==0
assert sp.simplify((3*(1-h))*(ratio-1)-(3*C+4*h-3))==0

# Derivative signs behind the no-scan constrained optimum.
dF_low4=sp.factor(sp.diff(F_low4,h))
dF_high4=sp.factor(sp.diff(F_high4,h))
assert sp.simplify(dF_low4-4*h*(C*h+2*C+h)/(9*(1-h)**4))==0
assert sp.simplify(dF_high4+12*h*((9*C+1)*h-6*C)/(3*C+h)**4)==0

# Unconstrained global optimizer from the prior theorem.
h_bal=sp.simplify(3*(1-C)/4)
h_star=sp.simplify(6*C/(9*C+1))
# C<=1/3 -> h0=h_bal. C>=1/3 -> h0=h_star.
assert sp.simplify(h_star-h_bal-3*(3*C-1)*(3*C+1)/(4*(9*C+1)))==0

# Small-cap asymptotics quantify how the cutoff collapses when LV parameters
# are forced toward zero.  These are useful for later insertion of actual PPN
# or matter-sector bounds without hard-coding any such bound here.
# C<1, alpha-cap active in the h->0/low branch:
#   F ~ sqrt(A) C^(3/4).
# C<1, ell-cap active:
#   F ~ sqrt(E) C^(1/4).
# C>1, alpha-cap active in the h->0/high branch:
#   F ~ sqrt(A) C^(-1/4).
# C>1, ell-cap active:
#   F ~ sqrt(E) C^(-3/4).
q=sp.symbols('q', positive=True, finite=True, real=True)
# Use q->0 to make cap scaling explicit and avoid ambiguous multivariate limits.
ha_q=sp.simplify(h_alpha.subs(A,q))
he_q=sp.simplify(h_ell.subs(E,q))
assert sp.simplify(sp.limit(F_low4.subs(h,ha_q)/q**2,q,0,dir='+')-C**3)==0
assert sp.simplify(sp.limit(F_low4.subs(h,he_q)/q**2,q,0,dir='+')-C)==0
assert sp.simplify(sp.limit(F_high4.subs(h,ha_q)/q**2,q,0,dir='+')-1/C)==0
assert sp.simplify(sp.limit(F_high4.subs(h,he_q)/q**2,q,0,dir='+')-1/C**3)==0

out={
  'classification':'RTK_ROUTE_B_BPS_CONSTRAINED_CUTOFF_PASS',
  'input':'C>0, 0<alpha_cap<2, ell_cap>0',
  'inverse_family':{
    'alpha(h)':'2h/(3C+h)',
    'ell(h)':'2h/[3(1-h)]',
    'monotonicity':'both strictly increase for 0<h<1'
  },
  'exact_cap_map':{
    'h_alpha':'3 alpha_cap C/(2-alpha_cap)',
    'h_ell':'3 ell_cap/(2+3 ell_cap)',
    'feasible_h':'0<h<=min(h_alpha,h_ell)'
  },
  'unconstrained_optimizer':{
    '0<C<=1/3':'h0=3(1-C)/4',
    'C>=1/3':'h0=6C/(9C+1)'
  },
  'constrained_optimizer':'h_opt,cap=min(h0(C), h_alpha, h_ell)',
  'cutoff_evaluation':{
    'low_branch_condition':'4 h_opt,cap <= 3(1-C)',
    'low_branch':'(Lambda_p,max,cap/M_P)^4 = 4 h^2(3C+h)/[27(1-h)^3]',
    'high_branch':'(Lambda_p,max,cap/M_P)^4 = 12 h^2(1-h)/(3C+h)^3'
  },
  'small_cap_scaling':{
    'C<1_alpha_cap_active':'Lambda_p/M_P ~ sqrt(alpha_cap) C^(3/4)',
    'C<1_ell_cap_active':'Lambda_p/M_P ~ sqrt(ell_cap) C^(1/4)',
    'C>1_alpha_cap_active':'Lambda_p/M_P ~ sqrt(alpha_cap) C^(-1/4)',
    'C>1_ell_cap_active':'Lambda_p/M_P ~ sqrt(ell_cap) C^(-3/4)'
  },
  'interpretation':'Arbitrarily small alpha and ell remain compatible with the exact target pole, but the available low-energy cutoff then decreases as the square root of the active small cap. The correct phenomenological test is therefore the capped hierarchy p_req < M_P F_cap(C,alpha_cap,ell_cap), not the unconstrained Fmax(C).',
  'guards':['abstract caps only; no observational numerical bound is asserted','quadratic pole/cutoff theorem only','does not establish matter-sector coupling, radiative stability, nonlinear DOF closure or off-shell source equivalence'],
  'next_step':'Combine the exact capped cutoff with the state-driven RTK dictionary C=c_a^2(a), Mdisp=M_K(a), then insert separately sourced phenomenological alpha/ell caps.'
}
print('RTK_ROUTE_B_BPS_CONSTRAINED_CUTOFF_PASS',json.dumps(out,sort_keys=True))
