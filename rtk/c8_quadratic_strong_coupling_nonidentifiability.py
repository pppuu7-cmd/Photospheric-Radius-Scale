#!/usr/bin/env python3
"""C8 no-inference lemma: quadratic RTK data do not fix strong coupling.

Take the proven local mixed-kinetic quadratic representative and add an allowed
cubic interaction with an independent coefficient.  The Hessian at the vacuum,
and hence the complete quadratic dispersion/propagator, is independent of that
coefficient, while the cubic vertex depends on it.  Therefore no unique strong-
coupling scale can be inferred from the quadratic dispersion alone.

This is a structural EFT lemma, not a strong-coupling calculation for the final
nonlinear RTK completion.
"""
import json
import sympy as sp

K,G,M,g,Lam = sp.symbols('K G M g Lambda', positive=True, finite=True, real=True)
x,y,z = sp.symbols('x y z', real=True)  # pi_dot, grad pi, grad pi_dot representatives

L2 = sp.Rational(1,2)*K*x**2 + sp.Rational(1,2)*K*z**2/M**2 - sp.Rational(1,2)*G*y**2
O3 = x*y**2
L = L2 + g*O3/Lam**2
vars_ = (x,y,z)

# Vacuum Hessian: complete quadratic data are independent of g and Lambda.
H = sp.Matrix([[sp.diff(L,a,b).subs({x:0,y:0,z:0}) for b in vars_] for a in vars_])
H2 = sp.Matrix([[sp.diff(L2,a,b) for b in vars_] for a in vars_])
assert sp.simplify(H-H2) == sp.zeros(3,3)
assert not any(entry.has(g) or entry.has(Lam) for entry in H)

# Cubic vertex is nonzero and explicitly controlled by the independent coupling.
vertex = sp.diff(L,x,y,y).subs({x:0,y:0,z:0})
assert sp.simplify(vertex-2*g/Lam**2) == 0

# Two theories with different cubic coefficients have identical quadratic
# Hessian but inequivalent cubic vertices.
g1,g2 = sp.symbols('g1 g2', positive=True, finite=True, real=True)
v1 = sp.simplify(vertex.subs(g,g1)); v2 = sp.simplify(vertex.subs(g,g2))
assert sp.simplify(v1-v2-2*(g1-g2)/Lam**2) == 0

# The quadratic dispersion in Fourier space is the already-proven one.
q,w = sp.symbols('q omega', positive=True, real=True)
inverse_kernel = K*(1+q**2/M**2)*w**2-G*q**2
w2 = sp.solve(sp.Eq(inverse_kernel,0),w**2)[0]
assert sp.simplify(w2-(G/K)*q**2/(1+q**2/M**2)) == 0
assert not w2.has(g) and not w2.has(Lam)

out={
  'classification':'RTK_C8_QUADRATIC_STRONG_COUPLING_NONIDENTIFIABILITY_PASS',
  'quadratic_representative':'L2=K pi_dot^2/2 + K (grad pi_dot)^2/(2M^2) - G (grad pi)^2/2',
  'example_cubic':'L3=(g/Lambda^2) pi_dot (grad pi)^2',
  'vacuum_hessian_independent_of_cubic':True,
  'cubic_vertex':'d^3L/(d pi_dot d(grad pi)^2)=2g/Lambda^2',
  'quadratic_dispersion':'omega^2=(G/K) q^2/(1+q^2/M^2)',
  'theorem':'An infinite family of EFTs with different independent cubic couplings shares exactly the same quadratic Hessian and mixed-kinetic dispersion. Therefore the quadratic dispersive scale M (or M_K/k_*) does not determine a unique interaction strength or strong-coupling cutoff.',
  'required_next_step':'Choose or derive an explicit nonlinear completion; expand to cubic order; impose its constraints; canonically normalize the propagating fields; only then power-count the actual interaction vertices.',
  'non_claims':[
    'does not determine the numerical RTK strong-coupling scale',
    'does not prove any chosen nonlinear completion is weakly coupled',
    'does not establish radiative stability or counterterm closure',
    'does not replace the full C7 constraint/DOF analysis'
  ]
}
print('RTK_C8_QUADRATIC_STRONG_COUPLING_NONIDENTIFIABILITY_PASS',json.dumps(out,sort_keys=True))
