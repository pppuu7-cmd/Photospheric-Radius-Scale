#!/usr/bin/env python3
"""Exact beta=0 BPS cutoff optimum at fixed measured G_N with LV caps.

This theorem composes three previously separate ingredients for the selected
Route-B exact-rational family:

1. alpha(h)=2h/(3C+h), ell(h)=2h/[3(1-h)], C>0, 0<h<1;
2. BPS low-energy momentum cutoffs in bare M_P units;
3. beta=0 Newton normalization Mbar_N=M_P sqrt(1-alpha/2), where
   Mbar_N=(8 pi G_N)^(-1/2).

It then imposes explicit low-energy caps
  0<alpha<=A<2, 0<ell<=E
and proves that no scan is needed: the fixed-G_N cutoff is strictly increasing
up to its unique unconstrained physical optimum, while alpha and ell are both
strictly increasing.  Hence the capped optimum is the minimum of three exact
h bounds.

The caps A,E are abstract inputs.  Numerical phenomenological bounds are to be
sourced and inserted separately so the algebraic theorem remains reusable.
"""
import json
import sympy as sp

C,h,A,E=sp.symbols('C h alpha_cap ell_cap', positive=True, finite=True, real=True)
alpha=sp.simplify(2*h/(3*C+h))
ell=sp.simplify(2*h/(3*(1-h)))
ratio=sp.simplify(ell/alpha)

# Exact cap inversions; monotonicity makes them iff bounds.
hA=sp.simplify(3*A*C/(2-A))
hE=sp.simplify(3*E/(2+3*E))
assert sp.simplify(alpha.subs(h,hA)-A)==0
assert sp.simplify(ell.subs(h,hE)-E)==0
assert sp.simplify(sp.diff(alpha,h)-6*C/(3*C+h)**2)==0
assert sp.simplify(sp.diff(ell,h)-2/(3*(1-h)**2))==0

# Exact cap-dominance crossover hA=hE.
C_cross=sp.simplify(E*(2-A)/(A*(2+3*E)))
assert sp.simplify((hA-hE).subs(C,C_cross))==0

# beta=0 fixed-Newton normalization: M_P/Mbar_N.
newton_factor_sq=sp.simplify(1/(1-alpha/2))
assert sp.simplify(newton_factor_sq-(3*C+h)/(3*C))==0

# Physical fixed-G_N momentum cutoff in fourth-power form.
# Low means ell<=alpha; high means ell>=alpha.
Glo4=sp.factor(sp.simplify((ell**3/alpha)*newton_factor_sq**2))
Ghi4=sp.factor(sp.simplify((alpha**3/ell)*newton_factor_sq**2))
assert sp.simplify(Glo4-4*h**2*(3*C+h)**3/(243*C**2*(1-h)**3))==0
assert sp.simplify(Ghi4-4*h**2*(1-h)/(3*C**2*(3*C+h)))==0

# Derivative structure: low branch always rises; high branch rises until hN.
dlo=sp.factor(sp.diff(Glo4,h))
dhi=sp.factor(sp.diff(Ghi4,h))
assert sp.simplify(dlo + 4*h*(3*C+h)**2*(2*h**2-(5+3*C)*h-6*C)/(243*C**2*(1-h)**4))==0
q=sp.factor(2*h**2+(9*C-1)*h-6*C)
assert sp.simplify(dhi + 4*h*q/(3*C**2*(3*C+h)**2))==0

# Unconstrained fixed-G_N optimizer.
D=sp.sqrt(81*C**2+30*C+1)
hbal=sp.simplify(3*(1-C)/4)
hN=sp.simplify((1-9*C+D)/4)
assert sp.simplify(q.subs(h,hN))==0
assert sp.simplify(hN-hbal-(D-6*C-2)/4)==0
assert sp.factor(D**2-(6*C+2)**2-3*(5*C-1)*(3*C+1))==0

# The physical unconstrained optimum is hbal for C<=1/5, hN for C>=1/5.
# With caps, feasible h<=min(hA,hE), so monotonicity up to h0 proves
# hopt_cap=min(h0,hA,hE).

# Useful exact values at cap saturation, for direct no-scan evaluation.
Glo4_A=sp.factor(sp.simplify(Glo4.subs(h,hA)))
Ghi4_A=sp.factor(sp.simplify(Ghi4.subs(h,hA)))
Glo4_E=sp.factor(sp.simplify(Glo4.subs(h,hE)))
Ghi4_E=sp.factor(sp.simplify(Ghi4.subs(h,hE)))

# Leading small-cap asymptotics at fixed measured G_N.  Newton normalization
# tends to unity as A,E->0, but we prove the coefficients explicitly.
qsmall=sp.symbols('q', positive=True, finite=True, real=True)
ha_q=sp.simplify(hA.subs(A,qsmall))
he_q=sp.simplify(hE.subs(E,qsmall))
assert sp.simplify(sp.limit(Glo4.subs(h,ha_q)/qsmall**2,qsmall,0,dir='+')-C**3)==0
assert sp.simplify(sp.limit(Glo4.subs(h,he_q)/qsmall**2,qsmall,0,dir='+')-C)==0
assert sp.simplify(sp.limit(Ghi4.subs(h,ha_q)/qsmall**2,qsmall,0,dir='+')-1/C)==0
assert sp.simplify(sp.limit(Ghi4.subs(h,he_q)/qsmall**2,qsmall,0,dir='+')-1/C**3)==0

# Exact ell reached when alpha cap is saturated.  This allows a direct check
# whether an ell cap is automatically obeyed on the alpha-limited solution.
ell_at_A=sp.factor(sp.simplify(ell.subs(h,hA)))
assert sp.simplify(ell_at_A-2*A*C/(2-A*(1+3*C)))==0

out={
  'classification':'RTK_ROUTE_B_BPS_BETA0_CAPPED_NEWTON_CUTOFF_PASS',
  'scope':'conditional beta=0 matter branch, fixed measured G_N, abstract positive alpha/ell caps',
  'exact_cap_map':{
    'h_alpha':'3 alpha_cap C/(2-alpha_cap)',
    'h_ell':'3 ell_cap/(2+3 ell_cap)',
    'alpha_vs_ell_cap_crossover_C':'ell_cap(2-alpha_cap)/[alpha_cap(2+3 ell_cap)]',
    'ell_at_alpha_cap':'2 alpha_cap C/[2-alpha_cap(1+3C)]'
  },
  'unconstrained_fixed_GN_optimizer':{
    '0<C<=1/5':'h0=3(1-C)/4',
    'C>=1/5':'h0=[1-9C+sqrt(81C^2+30C+1)]/4'
  },
  'capped_optimizer':'h_opt=min(h0(C), h_alpha, h_ell)',
  'physical_cutoff':{
    'ell_le_alpha':'(Lambda_p/Mbar_N)^4=4 h^2(3C+h)^3/[243 C^2(1-h)^3]',
    'ell_ge_alpha':'(Lambda_p/Mbar_N)^4=4 h^2(1-h)/[3 C^2(3C+h)]',
    'evaluation_rule':'insert h_opt and select the branch from ell(h_opt)<=alpha(h_opt)'
  },
  'small_cap_scaling':{
    'low_branch_alpha_active':'Lambda_p/Mbar_N ~ sqrt(alpha_cap) C^(3/4)',
    'low_branch_ell_active':'Lambda_p/Mbar_N ~ sqrt(ell_cap) C^(1/4)',
    'high_branch_alpha_active':'Lambda_p/Mbar_N ~ sqrt(alpha_cap) C^(-1/4)',
    'high_branch_ell_active':'Lambda_p/Mbar_N ~ sqrt(ell_cap) C^(-3/4)'
  },
  'theorem':'At fixed measured Newton constant on the beta=0 branch, arbitrary alpha/ell upper caps preserve an exact no-scan optimum: the largest allowed cutoff is attained at h=min(h0,h_alpha,h_ell).',
  'interpretation':'This is the appropriate algebraic gate before inserting solar-system/GW bounds. It separates a physical fixed-G_N cutoff from both the bare-M_P theorem and unsourced phenomenological numbers.',
  'guards':['beta=0 is conditional and is not fixed by the pure-gravity quadratic embedding','caps are abstract; no observational values are asserted here','does not establish compact-object regularity, PPN viability, radiative stability, off-shell source equivalence or nonlinear DOF closure'],
  'next_step':'Insert separately sourced alpha/ell bounds and the state-driven C(a),M_K(a) dictionary; report the worst capped hierarchy over the frozen dense-z range.'
}
print('RTK_ROUTE_B_BPS_BETA0_CAPPED_NEWTON_CUTOFF_PASS',json.dumps(out,sort_keys=True))
