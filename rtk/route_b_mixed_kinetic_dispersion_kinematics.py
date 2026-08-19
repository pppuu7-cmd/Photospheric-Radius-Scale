#!/usr/bin/env python3
"""Exact kinematics of the RTK target mixed-kinetic scalar branch.

For the reduced quadratic inverse kernel
    (1 + q^2/M^2) omega^2 - c_s^2 q^2 = 0,
this script proves the exact positive-frequency dispersion, phase/group
velocities, stability sign conditions, and asymptotic limits.

Scope: one reduced scalar branch only. This is not the characteristic analysis
of the full metric+Khronon+RT system and is not a proof of nonlinear causality,
strong hyperbolicity, or strong-coupling scale.
"""
import json
import sympy as sp

q,M,c=sp.symbols('q M c', positive=True, finite=True, real=True)
x=sp.symbols('x', positive=True, real=True)

omega=sp.simplify(c*q/sp.sqrt(1+q**2/M**2))
v_phase=sp.simplify(omega/q)
v_group=sp.simplify(sp.diff(omega,q))
assert sp.simplify(v_phase-c/sp.sqrt(1+q**2/M**2))==0
assert sp.simplify(v_group-c/(1+q**2/M**2)**sp.Rational(3,2))==0

omega2=sp.simplify(omega**2)
assert sp.simplify(omega2-c**2*q**2/(1+q**2/M**2))==0

# Monotonic positive-frequency branch: d omega/dq > 0 for q,M,c>0.
assert v_group.is_positive is True
# v_phase<c follows from an exact positive difference of squares.
assert sp.simplify(c**2-v_phase**2)==sp.simplify(c**2*q**2/(M**2+q**2))
assert sp.ask(sp.Q.positive(sp.simplify(c**2-v_phase**2))) is True

# Dimensionless x=q/M makes the velocity ordering and asymptotics explicit.
omega_x=sp.simplify(omega.subs(q,M*x))
vp_x=sp.simplify(v_phase.subs(q,M*x))
vg_x=sp.simplify(v_group.subs(q,M*x))
assert sp.simplify(vp_x-vg_x-c*x**2/(1+x**2)**sp.Rational(3,2))==0
assert sp.ask(sp.Q.positive(sp.simplify(vp_x-vg_x))) is True
# vg<c is equivalent (for positive quantities) to (1+x^2)^3>1.
vg_bound_poly=sp.expand((1+x**2)**3-1)
assert sp.factor(vg_bound_poly)==x**2*(x**4+3*x**2+3)
assert sp.ask(sp.Q.positive(vg_bound_poly)) is True

assert sp.limit(omega_x,x,0,dir='+')==0
assert sp.limit(omega_x/(c*M*x),x,0,dir='+')==1
assert sp.limit(omega_x,x,sp.oo)==c*M
assert sp.limit(vp_x,x,0,dir='+')==c
assert sp.limit(vp_x,x,sp.oo)==0
assert sp.limit(vg_x,x,0,dir='+')==c
assert sp.limit(vg_x,x,sp.oo)==0
assert sp.limit(vg_x*x**3/c,x,sp.oo)==1

# Low-q series: omega^2 = c^2 q^2 [1-q^2/M^2+O(q^4/M^4)].
series_omega2=sp.series(c**2*M**2*x**2/(1+x**2),x,0,7).removeO()
expected_series=c**2*M**2*(x**2-x**4+x**6)
assert sp.simplify(series_omega2-expected_series)==0

result={
  'classification':'RTK_ROUTE_B_MIXED_KINETIC_DISPERSION_KINEMATICS_PASS',
  'inverse_kernel':'(1+q^2/M^2) omega^2 - c_s^2 q^2',
  'positive_frequency':'omega=c_s q/sqrt(1+q^2/M^2)',
  'phase_velocity':'v_phase=c_s/sqrt(1+q^2/M^2)',
  'group_velocity':'v_group=c_s/(1+q^2/M^2)^(3/2)',
  'sign_conditions':'M^2>0 and c_s^2>0 give real omega^2 for q^2>=0 on this reduced branch',
  'velocity_bounds':'0 < v_group <= v_phase <= c_s for q>=0; if c_s<=1 in units with metric light speed 1, both reduced-branch phase and group velocities are <=1',
  'low_q':'omega^2=c_s^2 q^2 [1-q^2/M^2+q^4/M^4+...]',
  'high_q':'omega -> c_s M, v_phase ~ c_s M/q, v_group ~ c_s M^3/q^3',
  'interpretation':'The mixed kinetic factor suppresses phase/group propagation at q>>M while keeping the reduced mode real for positive M^2,c_s^2.',
  'non_claims':[
    'not the front-velocity/causal-cone theorem of the full coupled PDE system',
    'not full strong hyperbolicity',
    'not a ghost theorem for all coupled modes',
    'not a strong-coupling cutoff',
    'not a nonlinear or radiative-stability result'
  ]
}
print('RTK_ROUTE_B_MIXED_KINETIC_DISPERSION_KINEMATICS_PASS',json.dumps(result,sort_keys=True))
