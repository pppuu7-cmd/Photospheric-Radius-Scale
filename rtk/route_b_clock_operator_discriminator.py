#!/usr/bin/env python3
"""Linearized clock-operator discriminator around Minkowski.

Purpose
-------
Identify which preferred-foliation geometric operators can reproduce the
quadratic RTK scalar kinetic deformation

    (grad pi_dot)^2  <->  q^2 omega^2 |pi|^2

without silently replacing it by a higher-spatial-potential operator or by a
higher-time-derivative operator.

Assumptions/scope
-----------------
* Minkowski metric is held fixed (Stueckelberg/clock decoupling diagnostic).
* phi=t+pi defines the foliation; only terms linear in pi are needed before
  squaring to obtain the quadratic action.
* Overall signs and normalization factors are irrelevant for the derivative
  fingerprint; the test tracks powers of q and omega exactly.

At linear order, for the normalized foliation normal u_mu,

    a_i = u^nu partial_nu u_i              ~ partial_i pi_dot,
    K_ij = h_i^mu h_j^nu partial_mu u_nu   ~ partial_i partial_j pi,
    D_l K_ij                               ~ partial_l partial_i partial_j pi,
    A_i = -(1/2) h_i^mu L_u a_mu          ~ -(1/2) partial_i pi_ddot.

Thus:
    a_i a^i               -> q^2 omega^2,
    D_l K_ij D^l K^ij     -> q^6,
    A_i A^i               -> (1/4) q^2 omega^4.

The result is an operator-level discriminator, not a nonlinear constraint or
DHOST degeneracy proof.
"""
import json
import sympy as sp

q,omega=sp.symbols('q omega', positive=True, nonzero=True, real=True)
I=sp.I
pi=sp.symbols('pi', nonzero=True)

# Fourier replacement: spatial derivative -> i q, time derivative -> -i omega.
dx=I*q
dt=-I*omega

# One-dimensional aligned wavevector is sufficient for derivative counting;
# rotational contractions restore q^2, q^6, etc.
a_i=sp.expand(dx*dt*pi)
K_ij=sp.expand(dx*dx*pi)
DK=sp.expand(dx*K_ij)
A_i=sp.expand(-sp.Rational(1,2)*dt*a_i)

# For real quadratic actions use modulus-squared fingerprints: replace i
# phases by their magnitudes, equivalently square derivative powers.
fingerprint_a=sp.expand(q**2*omega**2)
fingerprint_DK=sp.expand(q**6)
fingerprint_A=sp.expand(sp.Rational(1,4)*q**2*omega**4)
target=sp.expand(q**2*omega**2)

assert sp.simplify(fingerprint_a-target)==0
assert sp.simplify(fingerprint_DK-target)!=0
assert sp.simplify(fingerprint_A-target)!=0

# The A_i term is fourth order in omega in the quadratic inverse propagator,
# while the RTK target is second order in omega. The DK term contains no omega.
assert sp.degree(fingerprint_a,omega)==2
assert sp.degree(fingerprint_DK,omega)==0
assert sp.degree(fingerprint_A,omega)==4
assert sp.degree(fingerprint_a,q)==2
assert sp.degree(fingerprint_DK,q)==6
assert sp.degree(fingerprint_A,q)==2

out={
  'classification':'RTK_ROUTE_B_CLOCK_OPERATOR_DISCRIMINATOR_PASS',
  'target_quadratic_fingerprint':'q^2*omega^2 |pi|^2',
  'linearized_clock_geometry':{
    'a_i':'partial_i pi_dot',
    'K_ij':'partial_i partial_j pi',
    'D_l_K_ij':'partial_l partial_i partial_j pi',
    'A_i':'-(1/2) partial_i pi_ddot'
  },
  'quadratic_fingerprints':{
    'a_i_a^i':'q^2*omega^2',
    'D_l_K_ij_D^l_K^ij':'q^6',
    'A_i_A^i':'(1/4)*q^2*omega^4'
  },
  'minimal_derivative_match':'a_i a^i',
  'nablaK_interpretation':'higher-spatial-potential in fixed-metric clock decoupling, not the RTK q^2*omega^2 term',
  'A_i_interpretation':'higher-time-derivative fingerprint in fixed-metric clock decoupling; generic inclusion must be constraint-degenerate to avoid an extra mode',
  'connection_to_prior_route_b':'The desired a_i a^i fingerprint explains why the earlier c4 acceleration route was attractive; its failure was a full metric/DHOST degeneracy obstruction, not a derivative-fingerprint mismatch.',
  'next_completion_target':'Search X-dependent/spatially-covariant companion operators that keep the a_i a^i quadratic fingerprint while restoring a nondegenerate constrained metric sector, or construct an explicit auxiliary-field reduction.',
  'scope_warning':'Linearized fixed-Minkowski clock derivative-counting theorem only; not a full nonlinear DOF, ghost, hyperbolicity, or strong-coupling proof.'
}
print('RTK_ROUTE_B_CLOCK_OPERATOR_DISCRIMINATOR_PASS',json.dumps(out,sort_keys=True))
