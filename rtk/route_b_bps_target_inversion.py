#!/usr/bin/env python3
"""Constructive inversion from an arbitrary positive RTK target dispersion to BPS parameters.

Input target:
  omega^2 = C p^2/(1+p^2/Mdisp^2), C>0, Mdisp>0.

For any auxiliary tuning parameter 0<h<1, this theorem constructs positive BPS
parameters z, ell=lambda-1, alpha and s such that the exact healthy-BPS rational
pole family reproduces exactly the target C and Mdisp.  It then composes this
inverse family with the exact BPS low-energy cutoffs and the independently
proved C8 accuracy/crossover window to obtain a closed-form optimum in h and a
necessary-and-sufficient hierarchy criterion for a pre-strong-coupling z=3
crossover that preserves a requested finite-range RTK accuracy.

Scope: quadratic pole/dispersion map plus low-energy cutoff/window composition.
It does not solve the off-shell source/residue map, nonlinear constraint problem,
radiative stability, or matter-sector Lorentz-violation bounds.
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

# ---------------------------------------------------------------------------
# Compose the inverse family with the exact BPS low-energy cutoff formulas.
# From BPS Eqs. (5.14)-(5.15), with M_alpha=M_P sqrt(alpha),
# M_lambda=M_P sqrt(ell):
#   ell<=alpha: Lambda_p/M_P = ell^(3/4) alpha^(-1/4)
#   ell>=alpha: Lambda_p/M_P = alpha^(3/4) ell^(-1/4)
# and in either branch (Lambda_omega/Lambda_p)^2 = ell/alpha.
# ---------------------------------------------------------------------------
MP=sp.symbols('M_P', positive=True, finite=True, real=True)
zH,ellH,alphaH,sH,MH,csH,M2H=family(h)
ratio=sp.factor(sp.simplify(ellH/alphaH))
assert sp.simplify(ratio-(3*C+h)/(3*(1-h)))==0

Lp_low=sp.simplify(MP*ellH**sp.Rational(3,4)*alphaH**(-sp.Rational(1,4)))
Lw_low=sp.simplify(MP*ellH**sp.Rational(5,4)*alphaH**(-sp.Rational(3,4)))
Lp_high=sp.simplify(MP*alphaH**sp.Rational(3,4)*ellH**(-sp.Rational(1,4)))
Lw_high=sp.simplify(MP*(alphaH*ellH)**sp.Rational(1,4))
assert sp.simplify((Lw_low/Lp_low)**2-ratio)==0
assert sp.simplify((Lw_high/Lp_high)**2-ratio)==0

# Work with fourth powers to avoid branch-irrelevant radicals.
F_low4=sp.factor(sp.simplify((Lp_low/MP)**4))
F_high4=sp.factor(sp.simplify((Lp_high/MP)**4))
assert sp.simplify(F_low4-4*h**2*(3*C+h)/(27*(1-h)**3))==0
assert sp.simplify(F_high4-12*h**2*(1-h)/(3*C+h)**3)==0

# Branch switch ell=alpha occurs at h_bal=3(1-C)/4 when 0<C<1.
# Low branch is monotone increasing; high branch has one stationary maximum.
h_bal=sp.simplify(3*(1-C)/4)
h_star=sp.simplify(6*C/(9*C+1))
assert sp.simplify(ratio.subs(h,h_bal)-1)==0
assert sp.factor(sp.diff(F_low4,h)-4*h*(C*h+2*C+h)/(9*(1-h)**4))==0
assert sp.factor(sp.diff(F_high4,h)+12*h*((9*C+1)*h-6*C)/(3*C+h)**4)==0
# h_star-h_bal has the sign of 3C-1.
assert sp.simplify(h_star-h_bal-3*(3*C-1)*(3*C+1)/(4*(9*C+1)))==0

# Exact global optimum of Lambda_p over the healthy inverse family 0<h<1:
#   0<C<=1/3 : the branch-balance point h_bal,
#   C>=1/3   : the high-branch stationary point h_star.
Fmax_low=sp.simplify(sp.sqrt(2*(1-C)/(1+3*C)))
Fmax_high=sp.simplify((sp.Rational(16,27)/(C*(3*C+1)**2))**sp.Rational(1,4))
assert sp.simplify(F_low4.subs(h,h_bal)-Fmax_low**4)==0
assert sp.simplify(F_high4.subs(h,h_bal)-Fmax_low**4)==0
assert sp.simplify(F_high4.subs(h,h_star)-Fmax_high**4)==0
# Continuity at C=1/3.
assert sp.simplify(Fmax_low.subs(C,sp.Rational(1,3))-Fmax_high.subs(C,sp.Rational(1,3)))==0

# Optimal inverse parameters and frequency/momentum cutoff ratios.
a_bal=sp.simplify(alphaH.subs(h,h_bal)); e_bal=sp.simplify(ellH.subs(h,h_bal)); z_bal=sp.simplify(zH.subs(h,h_bal))
assert sp.simplify(a_bal-2*(1-C)/(1+3*C))==0
assert sp.simplify(e_bal-a_bal)==0
assert sp.simplify(z_bal-(1-C)/(4*C))==0

a_star=sp.simplify(alphaH.subs(h,h_star)); e_star=sp.simplify(ellH.subs(h,h_star)); z_star=sp.simplify(zH.subs(h,h_star))
assert sp.simplify(a_star-4/(3*(3*C+1)))==0
assert sp.simplify(e_star-4*C/(3*C+1))==0
assert sp.simplify(z_star-2/(9*C+1))==0
assert sp.simplify(ratio.subs(h,h_star)-3*C)==0

# C8 composition. Define p_req=max(Mdisp, p_max/epsilon^(1/6)).
# A strict crossover p_UV can be chosen with
#   p_req < p_UV < Lambda_p
# iff p_req < max_h Lambda_p.  Choosing the h optimum above also guarantees
# the sufficient frequency guard sqrt(2 C) Mdisp < Lambda_omega:
#   for C<=1/3, Lambda_omega=Lambda_p and sqrt(2C)<1;
#   for C>=1/3, Lambda_omega/Lambda_p=sqrt(3C)>sqrt(2C).
# Hence the single exact hierarchy criterion below is sufficient for both
# momentum and frequency cutoffs, and necessary because p_UV>=p_req.

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
    'target_C':'remains exactly fixed',
    'cutoff_warning':'Lambda_p and Lambda_omega scale to zero with h; h->0 cannot be taken blindly at fixed crossover target'
  },
  'cutoff_composition':{
    'branch_ratio':'ell/alpha=(3C+h)/[3(1-h)]',
    'branch_switch':'ell=alpha at h_bal=3(1-C)/4 when 0<C<1',
    'global_momentum_cutoff_optimum':{
      '0<C<=1/3':{
        'h_opt':'3(1-C)/4',
        'alpha_opt=ell_opt':'2(1-C)/(1+3C)',
        'z_opt':'(1-C)/(4C)',
        'Lambda_p,max/M_P':'sqrt[2(1-C)/(1+3C)]',
        'Lambda_omega/Lambda_p':'1'
      },
      'C>=1/3':{
        'h_opt':'6C/(9C+1)',
        'alpha_opt':'4/[3(3C+1)]',
        'ell_opt':'4C/(3C+1)',
        'z_opt':'2/(9C+1)',
        'Lambda_p,max/M_P':'[16/(27 C (3C+1)^2)]^(1/4)',
        'Lambda_omega/Lambda_p':'sqrt(3C)'
      }
    },
    'joint_accuracy_strong_coupling_criterion':{
      'p_req':'max(Mdisp, p_max/epsilon^(1/6)), with 0<epsilon<1',
      'iff':'There exists h and p_UV with gamma=(Mdisp/p_UV)^6 in (0,1], delta(p_max)<epsilon, p_UV<Lambda_p, and the sufficient frequency guard sqrt(2C)Mdisp<Lambda_omega iff p_req < M_P Fmax(C).',
      'Fmax(C)':'sqrt[2(1-C)/(1+3C)] for 0<C<=1/3; [16/(27 C (3C+1)^2)]^(1/4) for C>=1/3',
      'hierarchy_form':'M_P/Mdisp > max(1, (p_max/Mdisp) epsilon^(-1/6))/Fmax(C)',
      'construction':'Choose h=h_opt above and any p_UV strictly between p_req and Lambda_p,max; then gamma=(Mdisp/p_UV)^6.'
    }
  },
  'theorem':'Every positive rational RTK target pole admits a continuous healthy-BPS exact pole/dispersion embedding. After composing with the exact BPS cutoffs and C8 crossover-accuracy condition, the family has a closed-form h that maximizes the available momentum cutoff. The single piecewise hierarchy inequality p_req < M_P Fmax(C) is necessary and sufficient for existence of a strict accuracy-preserving pre-cutoff crossover under the stated sufficient frequency guard.',
  'guards':['quadratic pole/dispersion plus cutoff/window theorem only, not off-shell residue/source equivalence','BPS cutoff formulas are low-energy strong-coupling estimates from the selected nonlinear completion','does not prove radiative stability or matter-sector Lorentz constraints','does not replace full nonlinear constraint/DOF closure'],
  'next_step':'Insert the phenomenological RTK C, Mdisp, p_max and accuracy target epsilon into the exact hierarchy criterion, then audit whether the selected completion also satisfies radiative, matter-sector and nonlinear-constraint requirements.'
}
print('RTK_ROUTE_B_BPS_TARGET_INVERSION_PASS',json.dumps(out,sort_keys=True))
