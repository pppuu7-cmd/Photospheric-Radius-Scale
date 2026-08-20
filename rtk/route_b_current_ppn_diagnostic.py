#!/usr/bin/env python3
"""Current-state pointwise PPN diagnostic for the Route-B BPS inverse family.

Primary sources:
- Blas, Pujolas, Sibiryakov, arXiv:1007.3503 Eq. (5.34), small-coupling PPN.
- Gumrukcuoglu, Saravani, Sotiriou, arXiv:1711.08845 / PRD 97 024032,
  whose low-energy Horava ppN constraint is Eq. (12) and whose tensor-speed
  constraint after GW170817 drives |beta| to O(1e-15).
- Barausse, arXiv:1907.05958, Introduction, summarizes |beta|<~1e-15 and the
  two solar-system branches.

Scope: this is a TODAY / asymptotic-low-energy pointwise diagnostic of the
Minkowski inverse at the replay-certified z=0 target C. It is not a PPN theorem
for the still-unconstructed single fixed-action FLRW completion.
"""
import json
import sympy as sp

A,C=sp.symbols('A C', positive=True, finite=True, real=True)
# Exact inverse family evaluated at alpha=A.
hA=sp.simplify(3*A*C/(2-A))
ellA=sp.factor(2*A*C/(2-A*(1+3*C)))
alpha=A

# 2018 low-energy Horava ppN translated constraint, Eq. (12), on beta=0:
# | alpha/(2-alpha) * [1-alpha(1+2 gamma)/gamma] | <=~ 1e-7,
# with gamma=ell for beta=0 in the BPS/modern convention dictionary.
ppn_signed=sp.factor(alpha/(2-alpha)*(1-alpha*(1+2*ellA)/ellA))
assert sp.simplify(ppn_signed-A*(C-1)/(2*C))==0
# Production has 0<C<1, so magnitude is A(1-C)/(2C).
ppn_mag=sp.simplify(A*(1-C)/(2*C))
P=sp.Rational(1,10_000_000) # sourced translated ~1e-7 benchmark
Amax_beta0=sp.factor(2*C*P/(1-C))
assert sp.simplify(ppn_mag.subs(A,Amax_beta0)-P)==0

# Replay-certified current z=0 target.
C0=sp.Float('1.4738358401883835e-8',50)
Abench=sp.Float('1e-7',50)
ppn_bench=sp.N(ppn_mag.subs({C:C0,A:Abench}),30)
Amax0=sp.N(Amax_beta0.subs(C,C0),30)
assert float(ppn_bench)>1.0
assert float(Amax0)<1e-14

# The exact 2018 ppN expression contains alpha-2 beta as an overall factor;
# hence the tuned plane alpha=2 beta makes the preferred-frame ppN expression
# vanish. Combining with the post-GW170817 |beta|~<=1e-15 benchmark yields
# alpha~<=2e-15 on that tuned plane.
beta=sp.symbols('beta', real=True, finite=True)
gamma=sp.symbols('gamma', positive=True, finite=True, real=True)
ppn_general=sp.factor((A-2*beta)/(2-A)*(1-(A-2*beta)*(1+beta+2*gamma)/((1-beta)*(beta+gamma))))
assert sp.simplify(ppn_general.subs(beta,A/2))==0
beta_gw=sp.Rational(1,10**15)
A_tuned_gw=2*beta_gw

out={
  'classification':'RTK_ROUTE_B_CURRENT_PPN_DIAGNOSTIC_PASS',
  'scope':'pointwise z=0 low-energy/Minkowski diagnostic; not global FLRW completion',
  'provenance':{
    'scale_dictionary_run_id':32320390501,
    'capped_hierarchy_run_id':32322717923,
    'objective_fingerprint':'754edb2ff5380eff314867b0ecb1a23a8b861a69f7e46070c4b8251c98573666',
    'C_z0':float(C0),
  },
  'beta0_exact_reduction':{
    'inverse_ell_at_alpha_A':'2 A C/[2-A(1+3C)]',
    'ppn_constraint_expression_magnitude':'A(1-C)/(2C) for 0<C<1',
    'translated_bound_benchmark':'1e-7',
    'alpha_max_formula':'2 C*1e-7/(1-C)',
    'alpha_max_current_z0':float(Amax0),
  },
  'correction_to_previous_benchmark':{
    'alpha_1e-7_ppn_expression_at_z0':float(ppn_bench),
    'ratio_to_1e-7_bound':float(ppn_bench/1e-7),
    'status':'alpha=1e-7 beta=0 capped hierarchy was a conservative scale-separation benchmark, NOT a PPN-viable current beta=0 point.'
  },
  'tuned_ppn_plane':{
    'condition':'alpha=2 beta',
    'ppn_expression':'vanishes identically in the cited low-energy formula',
    'GW_beta_benchmark_abs_max':1e-15,
    'implied_alpha_abs_max_on_exact_tuned_plane':float(A_tuned_gw),
  },
  'interpretation':'The beta=0 pointwise inverse can satisfy current ppN only at alpha of order 1e-15 for the replay z=0 C, much smaller than the earlier 1e-7 hierarchy benchmark. A distinct alpha=2 beta tuned matter branch cancels the ppN expression but GW propagation then caps alpha at O(1e-15). Neither statement supplies the missing single fixed-action FLRW completion.',
  'guards':['Eq. (12) is a low-energy Horava/ppN constraint, not a higher-spatial-derivative compact-object theorem','the z=0 inverse is pointwise; do not apply its action coefficients as time-dependent Wilson coefficients','the tuned alpha=2 beta branch requires redoing the physical matter-frame rational-pole map rather than assuming the beta=0 exact map unchanged','compact-object UV regularity and radiative/matter-sector Lorentz safety remain open'],
  'next_step':'Re-evaluate the scale-separation margin at alpha~3e-15 (beta=0 diagnostic) and alpha~2e-15 (PPN-tuned/GW benchmark), then derive the fixed-action FLRW quadratic map.'
}
print('RTK_ROUTE_B_CURRENT_PPN_DIAGNOSTIC_PASS',json.dumps(out,sort_keys=True))
