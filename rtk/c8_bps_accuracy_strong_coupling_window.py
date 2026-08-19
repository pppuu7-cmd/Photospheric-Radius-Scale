#!/usr/bin/env python3
"""C8 constructive window for RTK accuracy and pre-strong-coupling z=3 onset.

Input from the machine-checked BPS two-crossover family:
  omega^2 = c_s^2 p^2 [1+gamma(p^2/M_*^2)^3]/[1+p^2/M_*^2],
  p_UV = M_* gamma^{-1/6}, 0<gamma<=1.

This theorem rewrites the fractional numerator correction exactly as
  delta(p)=(p/p_UV)^6,
then gives a constructive non-empty window in which the RTK rational pole is
accurate through p_max while the actual z=3 crossover occurs below an abstract
low-energy momentum strong-coupling scale Lambda_p.

Lambda_p and Lambda_omega are treated here as the low-energy cutoffs to be
computed from the selected nonlinear BPS completion.  This script does not
claim their numerical values or replace the cubic calculation.
"""
import json
import sympy as sp

M,g,p,cs,Lp,Lw=sp.symbols('M gamma p cs Lambda_p Lambda_omega', positive=True, finite=True, real=True)
puv=sp.simplify(M*g**(-sp.Rational(1,6)))
delta=sp.simplify(g*(p/M)**6)
assert sp.simplify(delta-(p/puv)**6)==0

# At the exact gamma*u^3=1 crossover, u=(p_UV/M)^2=gamma^{-1/3}.
u=sp.simplify(g**(-sp.Rational(1,3)))
omega2_uv=sp.simplify(2*cs**2*M**2*u/(1+u))
# Strict upper bound omega_UV^2 < 2 c_s^2 M^2 for every finite positive u.
margin_freq=sp.simplify(2*cs**2*M**2-omega2_uv)
assert sp.simplify(margin_freq-2*cs**2*M**2/(1+u))==0
assert margin_freq.is_positive is True

# Construct an explicit open compatibility family without relying on symbolic
# inequality solvers.  Let p_UV=M(1+a), Lambda_p=p_UV(1+b),
# epsilon=rho^6 with rho=t/(1+t) in (0,1), and
# p_max=rho*p_UV*c/(1+c), all a,b,t,c>0.  Then:
#   M<p_UV<Lambda_p,
#   delta(p_max)=[rho*c/(1+c)]^6 < epsilon.
a,b,t,c=sp.symbols('a b t c', positive=True, finite=True, real=True)
rho=sp.simplify(t/(1+t)); eps=sp.simplify(rho**6)
puv_c=sp.simplify(M*(1+a)); Lp_c=sp.simplify(puv_c*(1+b))
pmax_c=sp.simplify(rho*puv_c*c/(1+c))
gamma_c=sp.simplify((M/puv_c)**6)
assert sp.simplify(gamma_c-(1+a)**-6)==0
assert sp.simplify(gamma_c*(pmax_c/M)**6-eps*(c/(1+c))**6)==0
# Positive margins prove strict inequalities constructively.
assert sp.simplify(puv_c-M-M*a)==0
assert sp.simplify(Lp_c-puv_c-puv_c*b)==0
assert sp.simplify(rho*puv_c-pmax_c-rho*puv_c/(1+c))==0
assert sp.simplify(eps-gamma_c*(pmax_c/M)**6-eps*(1-(c/(1+c))**6))==0

# General feasibility statement follows from delta=(p/pUV)^6:
# accuracy requires pUV >= pmax/epsilon^(1/6), while gamma<=1 requires
# pUV>=M.  A strict pre-cutoff crossover exists whenever
# max(M,pmax/epsilon^(1/6)) < Lambda_p.
# We record this as the exact logical criterion; the constructive family above
# proves the feasible set is non-empty.

out={
  'classification':'RTK_C8_BPS_ACCURACY_STRONG_COUPLING_WINDOW_PASS',
  'input_family':'BPS z3 two-crossover quadratic scalar family',
  'exact_identity':'delta(p)=gamma(p/M_*)^6=(p/p_UV)^6 with p_UV=M_* gamma^(-1/6)',
  'momentum_feasibility_criterion':'A gamma in (0,1] can satisfy delta(p_max)<=epsilon and p_UV<Lambda_p iff there exists p_UV with max(M_*, p_max/epsilon^(1/6)) <= p_UV < Lambda_p; a strict open choice is guaranteed when max(M_*, p_max/epsilon^(1/6)) < Lambda_p.',
  'constructive_example':{
    'p_UV':'M_*(1+a)','Lambda_p':'p_UV(1+b)','epsilon':'rho^6, rho=t/(1+t)',
    'p_max':'rho p_UV c/(1+c)','gamma':'(1+a)^(-6)',
    'result':'M_*<p_UV<Lambda_p and delta(p_max)=epsilon[c/(1+c)]^6<epsilon for all positive a,b,t,c'
  },
  'frequency_at_uv':'omega_UV^2=2 c_s^2 M_*^2 u/(1+u), u=gamma^(-1/3), hence omega_UV^2<2 c_s^2 M_*^2',
  'sufficient_frequency_guard':'sqrt(2) c_s M_* < Lambda_omega guarantees the crossover frequency itself lies below the low-energy frequency cutoff.',
  'interpretation':'Making gamma arbitrarily tiny is not automatically optimal: it improves finite-range RTK accuracy but raises p_UV. Accuracy and strong-coupling avoidance must be co-designed through the open crossover window.',
  'next_required_step':'Compute Lambda_p and Lambda_omega from the actual selected-family cubic action/canonical normalization and verify the window numerically/parametrically for the phenomenological RTK scale.',
  'non_claims':['does not compute Lambda_p or Lambda_omega','does not prove all selected-family cubic vertices are weakly coupled','does not establish full nonlinear DOF closure','does not prove radiative stability']
}
print('RTK_C8_BPS_ACCURACY_STRONG_COUPLING_WINDOW_PASS',json.dumps(out,sort_keys=True))
