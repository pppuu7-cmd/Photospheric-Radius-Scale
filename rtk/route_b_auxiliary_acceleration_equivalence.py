#!/usr/bin/env python3
"""Route-B theorem: a purely algebraic auxiliary vector is only a rewrite of a_i^2.

Scope
-----
Fixed-metric preferred-foliation quadratic diagnostic plus exact algebraic
elimination.  This asks whether the simplest spatial auxiliary-vector trick can
produce the RTK mixed kinetic term while changing the nonlinear completion
problem.  It cannot: if B_i has no derivatives or extra constraints/couplings,
eliminating it reproduces the direct acceleration-squared operator exactly.

This is not a no-go for nontrivial constrained auxiliary sectors.
"""
import json
import sympy as sp

M,c,q,w,a,B = sp.symbols('M c q w a B', positive=True, nonzero=True, real=True)

# One aligned spatial component is sufficient because the contraction is
# rotationally invariant.  Signature convention: spatial norm is positive.
Laux = -sp.Rational(1,2)*M**2*B**2 + B*a
EOM_B = sp.diff(Laux,B)
Bsol = sp.solve(sp.Eq(EOM_B,0),B)
assert Bsol == [a/M**2]
Leff = sp.factor(Laux.subs(B,Bsol[0]))
assert sp.simplify(Leff-a**2/(2*M**2)) == 0

# Auxiliary Hessian is nonsingular: B is algebraic in this restricted system.
H_B = sp.diff(Laux,B,2)
assert sp.simplify(H_B + M**2) == 0
assert H_B != 0

# Clock decoupling fingerprint a_i ~ partial_i dot(pi).  The direct kinetic
# representative is normalized as 1/2 dot(pi)^2 + Leff - c^2/2 (grad pi)^2.
# Ignoring common |pi|^2/2, its Fourier inverse propagator is
#   (1+q^2/M^2) w^2 - c^2 q^2,
# hence the target rational dispersion.
K = 1 + q**2/M**2
inverse_kernel = sp.expand(K*w**2-c**2*q**2)
w2_solution = sp.solve(sp.Eq(inverse_kernel,0),w**2)
assert w2_solution == [c**2*q**2/(1+q**2/M**2)]
assert sp.simplify(w2_solution[0]-c**2*q**2*M**2/(M**2+q**2)) == 0

# The key equivalence statement is algebraic and exact: any action containing
# only this B sector reduces to the same direct +a_i a^i/(2 M^2) operator.
# Therefore a degeneracy/constraint obstruction of that effective action is not
# evaded merely by keeping B_i unintegrated as a bookkeeping field.

out={
  'classification':'RTK_ROUTE_B_AUXILIARY_ACCELERATION_EQUIVALENCE_PASS',
  'auxiliary_lagrangian':'-M^2 B_i B^i/2 + B_i a^i',
  'auxiliary_equation':'B_i=a_i/M^2',
  'auxiliary_hessian':'-M^2 (nonsingular for M^2>0)',
  'eliminated_operator':'+a_i a^i/(2 M^2)',
  'clock_fingerprint':'a_i~partial_i pi_dot -> q^2 omega^2 |pi|^2',
  'reduced_dispersion':'omega^2=c^2 q^2/(1+q^2/M^2)',
  'theorem':'A derivative-free unconstrained auxiliary spatial vector reproduces the desired mixed kinetic operator but is exactly an algebraic rewrite of acceleration-squared; by itself it cannot evade a degeneracy or constraint obstruction of the corresponding eliminated action.',
  'what_can_still_work':[
    'auxiliary fields with additional primary constraints',
    'nontrivial metric/extrinsic-curvature companion couplings',
    'X-dependent coefficients that alter the effective degeneracy conditions',
    'spatially covariant constructions whose constraint algebra is not equivalent to the direct constant-coefficient acceleration-squared action'
  ],
  'scope_warning':'Fixed-metric derivative fingerprint plus exact algebraic elimination only; not a full ADM Hamiltonian, DHOST degeneracy, hyperbolicity, loop, or strong-coupling theorem.'
}
print('RTK_ROUTE_B_AUXILIARY_ACCELERATION_EQUIVALENCE_PASS',json.dumps(out,sort_keys=True))
