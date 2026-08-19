#!/usr/bin/env python3
"""Close the isolated c4=2 loophole for the minimal constant-ci exact RTK mapping.

Scope is deliberately narrow and matches the earlier Route-B scalar-sector
mapping theorem: constant-ci khronometric action, fixed-Minkowski/single-mode
quadratic scalar decoupling target, plus DHOST nondegeneracy of the ordinary
metric kinetic block.

For the RTK target
  omega^2 = c_a^2 q^2/(1+q^2/M^2),
the mixed q^2*omega^2 kinetic term is welcome, but there is no q^4 potential
term in the numerator. With c1 absorbed, the khronometric q^4 scalar Hessian
coefficient is proportional to c2+c3. Thus exact target matching requires
c2+c3=0. Intersecting this with the isolated c4=2 DHOST branch forces the
Class-Ib point c2=1,c3=-1, whose metric kinetic factor f+X*alpha2 vanishes.

This does not exclude X-dependent DHOST, spatially covariant companion
operators, metric/auxiliary constrained reductions, or other nonlinear RTK
completions.
"""
import json
import sympy as sp

X=sp.symbols('X', positive=True, nonzero=True)
c2,c3=sp.symbols('c2 c3', real=True)
c4=sp.Integer(2)
f=sp.Integer(1)

# Exact scalar single-Fourier-mode identity:
# (tr H)^2 = tr(H^2) for H_ij ~ q_i q_j*pi, so c2 and c3 contribute through
# c2+c3 to q^4*pi^2 after c1 absorption.
q2,pi=sp.symbols('q2 pi', nonnegative=True)
trH_sq=q2**2*pi**2
trH2=q2**2*pi**2
assert sp.simplify(trH_sq-trH2)==0
q4_coeff=sp.expand(c2+c3)

# Exact RTK target has V(q) proportional to q^2 only: no q^4 numerator.
exact_target_q4_condition=sp.Eq(q4_coeff,0)
classI_sub={c3:-c2}

# Primary-source special-branch conditions, Ben Achour et al. Eq. (7.11).
D1_c4eq2=8*(1+c3)*(3*c2+c3-2)/X**2
D2_c4eq2=sp.simplify(D1_c4eq2/X)
D1_on_exact_target=sp.factor(D1_c4eq2.subs(classI_sub))
D2_on_exact_target=sp.factor(D2_c4eq2.subs(classI_sub))
assert D1_on_exact_target==-16*(c2-1)**2/X**2
assert D2_on_exact_target==-16*(c2-1)**2/X**3
sol=sp.solve(sp.Eq(D1_on_exact_target,0),c2)
assert sol==[1]
forced={c2:sp.Integer(1),c3:sp.Integer(-1)}

# Khronometric -> DHOST mapping after c1 absorption, Eq. (7.4).
alpha1=-c3/X
alpha2=-c2/X
assert sp.simplify(alpha1.subs(forced))==1/X
assert sp.simplify(alpha2.subs(forced))==-1/X

# At the forced intersection, both common metric-sector discriminants vanish:
# Class-Ib criterion f+X*alpha2=0; also f-X*alpha1=0.
metric_Ib=sp.simplify(f+X*alpha2.subs(forced))
metric_alt=sp.simplify(f-X*alpha1.subs(forced))
assert metric_Ib==0
assert metric_alt==0

# The c4 term remains nonzero and supplies the desired mixed kinetic structure,
# but only at this metric-degenerate exact-target point.
assert c4==2

out={
  'classification':'RTK_ROUTE_B_C4EQ2_MINIMAL_EXACT_TARGET_NOMAPPING_PASS',
  'target':'omega^2=c_a^2*q^2/(1+q^2/M^2)',
  'assumptions':[
    'constant-ci khronometric action with c1 absorbed',
    'fixed-Minkowski single-scalar quadratic decoupling mapping',
    'exact RTK numerator contains q^2 but no q^4 term',
    'ordinary metric kinetic block must remain nondegenerate'
  ],
  'c4_special_branch':2,
  'exact_target_no_q4_condition':'c2+c3=0',
  'D1_after_no_q4':'-16*(c2-1)^2/X^2',
  'D2_after_no_q4':'-16*(c2-1)^2/X^3',
  'unique_degenerate_intersection':{'c2':1,'c3':-1,'c4':2},
  'forced_dhost':{'alpha1':'1/X','alpha2':'-1/X'},
  'metric_f_plus_X_alpha2':0,
  'metric_f_minus_X_alpha1':0,
  'conclusion':'The isolated c4=2 branch does not provide a nondegenerate minimal constant-ci exact mapping to the RTK rational quadratic dispersion.',
  'remaining_open_completions':['X-dependent DHOST companion operators','spatially covariant mixed-derivative operators','constrained auxiliary-field reductions','other nonlinear structures whose reduced quadratic action matches RTK'],
  'scope_warning':'Quadratic exact-mapping no-go under the listed assumptions only; not a no-go theorem for all khronometric/Horava/DHOST-inspired completions or for the RTK model itself.'
}
print('RTK_ROUTE_B_C4EQ2_MINIMAL_EXACT_TARGET_NOMAPPING_PASS',json.dumps(out,sort_keys=True))
