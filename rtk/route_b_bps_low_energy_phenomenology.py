#!/usr/bin/env python3
"""Exact Route-B consequences of sourced low-energy khronometric bounds.

Phenomenology source: Enrico Barausse, arXiv:1907.05958, Introduction.
For the beta≈0 branch after GW170817 it summarizes:
  |beta| <=~ 1e-15;
  generic branch (|lambda| >> 1e-7): |alpha| <=~ 1e-7;
  remaining positive lambda is bounded only at roughly 0.01--0.1;
  alternative tuned branch: alpha <=~ 0.25e-4 and
                            lambda ≈ alpha/(1-2 alpha).

For beta=0, comparison of the ADM actions gives the convention dictionary
  ell = lambda_BPS-1 = lambda_modern.

This theorem does NOT turn approximate observational inequalities into exact
physics.  It uses the quoted central cap values as preregistered benchmark
numbers and proves exact algebraic consequences of those benchmark choices for
the selected RTK/BPS inverse family.
"""
import json
import sympy as sp

# Production RTK target speed is C=c_a^2=x/[s^2(s+x)],
# s=sqrt(1+lambda_D x^2), with x,lambda_D>0.
x,L=sp.symbols('x lambda_D', positive=True, finite=True, real=True)
s=sp.sqrt(1+L*x**2)
Cprod=sp.simplify(x/(s**2*(s+x)))
# Exact positive margin proving 0<Cprod<1.
margin=sp.simplify(s**2*(s+x)-x)
assert sp.simplify(margin-(s**3+L*x**3))==0

C,h,A,E=sp.symbols('C h A E', positive=True, finite=True, real=True)
alpha=sp.simplify(2*h/(3*C+h))
ell=sp.simplify(2*h/(3*(1-h)))
hA=sp.simplify(3*A*C/(2-A))
hE=sp.simplify(3*E/(2+3*E))
ellA=sp.factor(sp.simplify(ell.subs(h,hA)))
assert sp.simplify(ellA-2*A*C/(2-A*(1+3*C)))==0

# Sourced benchmark caps, kept exact as rationals.
Agen=sp.Rational(1,10_000_000)  # 1e-7
E01=sp.Rational(1,100)          # 0.01
E10=sp.Rational(1,10)           # 0.1

# Cap crossover C where h_alpha=h_ell.
def Ccross(A0,E0):
    return sp.factor(E0*(2-A0)/(A0*(2+3*E0)))
Cx01=Ccross(Agen,E01)
Cx10=Ccross(Agen,E10)
assert Cx01==sp.Rational(19999999,203)
assert Cx10==sp.Rational(19999999,23)
assert Cx01>1 and Cx10>1

# Therefore for every production RTK target 0<C<1 the alpha=1e-7 benchmark
# binds before either lambda/ell benchmark 0.01 or 0.1.
hA_gen=sp.simplify(hA.subs(A,Agen))
hE01=sp.simplify(hE.subs(E,E01)); hE10=sp.simplify(hE.subs(E,E10))
assert sp.simplify(hA_gen.subs(C,1)-sp.Rational(3,19999999))==0
assert hE01==sp.Rational(3,203)
assert hE10==sp.Rational(3,23)
assert sp.Rational(3,19999999)<hE01<hE10

# The unconstrained fixed-G_N optimum is never below 3/5 on 0<C<1:
# for C<=1/5, h0=3(1-C)/4 >=3/5;
# for C>=1/5 the high-branch stationary quadratic q has q(3/5)<=0,
# placing its positive root at h>=3/5.
q=sp.factor(2*h**2+(9*C-1)*h-6*C)
assert sp.factor(q.subs(h,sp.Rational(3,5)))-sp.factor(3*(1-5*C)/25)==0
assert sp.Rational(3,19999999)<sp.Rational(3,5)
# Hence alpha benchmark, not the unconstrained optimum, controls h for all
# production C in (0,1).

# Exact beta=0 fixed-G_N physical cutoff at alpha saturation.  Production
# C<1 and tiny hA place the solution on ell<=alpha branch.
newton_factor_sq=sp.simplify(1/(1-alpha/2))
Glo4=sp.factor(sp.simplify((ell**3/alpha)*newton_factor_sq**2))
G_A4=sp.factor(sp.simplify(Glo4.subs({h:hA,A:Agen})))
G_A4_expected=sp.factor(32*Agen**2*C**3/((2-Agen)**2*(2-Agen*(1+3*C))**3))
assert sp.simplify(G_A4-G_A4_expected)==0

# Alternative tuned solar-system central curve. At alpha=A, the selected
# inverse family has ell=2AC/[2-A(1+3C)]. Equating this exactly to the quoted
# central tuned relation ell=A/(1-2A) forces C=1.
tuned=sp.simplify(A/(1-2*A))
diff=sp.factor(ellA-tuned)
assert sp.simplify(diff + A*(A-2)*(C-1)/((2*A-1)*(3*A*C+A-2)))==0
# In the physical small-A domain 0<A<1/2 the only zero is C=1; production has
# C<1, so it does not lie exactly on the central tuned curve. The source uses
# an approximate relation, so this is NOT an exclusion of its allowed band.

out={
  'classification':'RTK_ROUTE_B_BPS_LOW_ENERGY_PHENOMENOLOGY_PASS',
  'source':'E. Barausse arXiv:1907.05958, Introduction',
  'convention_dictionary':'for beta=0, ell=lambda_BPS-1=lambda_modern',
  'production_target_speed':{
    'formula':'C=c_a^2=x/[s^2(s+x)], s=sqrt(1+lambda_D x^2)',
    'exact_domain':'0<C<1 for x>0, lambda_D>0'
  },
  'generic_branch_benchmarks':{
    'alpha_cap':'1e-7',
    'ell_cap_bracket':['0.01','0.1'],
    'alpha_vs_ell_crossover_C':{'ell_cap_0.01':str(Cx01),'ell_cap_0.1':str(Cx10)},
    'result':'Because production has 0<C<1, the alpha=1e-7 benchmark always binds before either ell benchmark and before the unconstrained fixed-G_N optimum.',
    'h_opt':'h_alpha=3 alpha_cap C/(2-alpha_cap)',
    'physical_cutoff_exact':'(Lambda_p/Mbar_N)^4=32 alpha_cap^2 C^3/[(2-alpha_cap)^2 (2-alpha_cap(1+3C))^3]'
  },
  'tuned_branch_central_curve':{
    'quoted_relation':'ell approximately alpha/(1-2alpha)',
    'exact_curve_intersection':'If treated as equality, the selected inverse family intersects it only at C=1.',
    'production_relation':'Production has C<1, so no production point lies exactly on that central equality curve.',
    'guard':'The observational relation is approximate; this does not exclude its finite allowed band.'
  },
  'interpretation':'For the sourced generic low-energy benchmark, the phenomenologically relevant Route-B cutoff is alpha-limited everywhere on the production RTK target domain. The loose 0.01--0.1 lambda/ell bound is not the active cutoff constraint.',
  'guards':['benchmark caps summarize a cited low-energy analysis and are not timeless universal bounds','beta=0/minimal matter coupling is conditional','does not establish compact-object regularity for nonzero alpha','does not establish UV radiative stability, matter Lorentz safety, nonlinear DOF closure or off-shell source equivalence'],
  'next_step':'Combine this closed-form alpha-limited cutoff with the current-state C(a),M_K(a) artifact to compute the worst physical hierarchy over all frozen dense redshifts.'
}
print('RTK_ROUTE_B_BPS_LOW_ENERGY_PHENOMENOLOGY_PASS',json.dumps(out,sort_keys=True))
