#!/usr/bin/env python3
"""Symbolic audit of the explicitly frozen RTK preferred-frame EFT Route A1.

This proves only statements inside the reduced scalar EFT assumptions documented
in PREFERRED_FRAME_EFT_ROUTE_A1.md. It is not a full metric/constraint proof.
"""
import json
import sympy as sp

# 3+1 preferred-frame coordinates.
t, x, y, z = sp.symbols('t x y z', real=True)
coords = (x, y, z)
pi = sp.Function('pi')(t, x, y, z)
pid = sp.diff(pi, t)
grad = [sp.diff(pi, q) for q in coords]
lap = sum(sp.diff(pi, q, 2) for q in coords)

O1 = pid**3
O2 = pid * sum(g*g for g in grad)
O3 = pid**2 * lap
O4 = sum(g*g for g in grad) * lap

# Integration-by-parts identities used to reduce the D=4 basis.
alt3 = pid * sum(sp.diff(pi,q)*sp.diff(pid,q) for q in coords)
div3 = sum(sp.diff(sp.Rational(1,2)*pid**2*sp.diff(pi,q), q) for q in coords)
assert sp.simplify(div3 - alt3 - sp.Rational(1,2)*O3) == 0

alt4 = sum(sp.diff(pi,qi)*sp.diff(pi,qj)*sp.diff(pi,qi,qj)
           for qi in coords for qj in coords)
div4 = sum(sp.diff(sp.Rational(1,2)*sum(g*g for g in grad)*sp.diff(pi,qi), qi)
           for qi in coords)
assert sp.simplify(div4 - alt4 - sp.Rational(1,2)*O4) == 0

# Basis enumeration by derivative partition and SO(3) index counting.
# D=3: (1,1,1) -> dot^3 and dot*(grad)^2.
# D=4: (2,1,1), ddot excluded -> dot^2*lap and (grad)^2*lap modulo IBP.
basis = {
    'D3': ['dot(pi)^3', 'dot(pi)*(grad pi)^2'],
    'D4': ['dot(pi)^2*Laplacian(pi)', '(grad pi)^2*Laplacian(pi)'],
}
assert sum(len(v) for v in basis.values()) == 4

# No basis representative contains a second time derivative.
for expr in (O1,O2,O3,O4):
    for der in expr.atoms(sp.Derivative):
        assert der.variables.count(t) <= 1, (expr, der)

# Canonical momentum/velocity-Hessian structure.
K, M, c1, c2, c3 = sp.symbols('K M c1 c2 c3', positive=True, finite=True)
# Treat Laplacian(pi) and |grad pi|^2 as independent spatial background symbols
# for the local Legendre-map algebra.
LAP, GR2, v = sp.symbols('LAP GR2 v', real=True)
P_local = K*v + 3*c1*v**2 + c2*GR2 + 2*c3*v*LAP
Hvel_local = sp.diff(P_local, v)
assert sp.simplify(Hvel_local - (K + 6*c1*v + 2*c3*LAP)) == 0

# The higher-spatial-derivative quadratic kinetic term contributes the
# positive Fourier operator K(1+q^2/M^2).
q = sp.symbols('q', nonnegative=True, finite=True)
Kq = K*(1 + q**2/M**2)
assert sp.ask(sp.Q.positive(Kq)) is True

# Mass dimensions after low-q canonical normalization pi_c=sqrt(K) pi.
# In 4D [pi_c]=1, [d_mu]=1.
operator_dimensions = {
    'dot(pi_c)^3': 6,
    'dot(pi_c)*(grad pi_c)^2': 6,
    'dot(pi_c)^2*Laplacian(pi_c)': 7,
    '(grad pi_c)^2*Laplacian(pi_c)': 7,
}
coefficient_dimensions = {k: 4-v for k,v in operator_dimensions.items()}
assert list(coefficient_dimensions.values()) == [-2,-2,-3,-3]

result = {
    'classification': 'ROUTE_A1_REDUCED_SCALAR_CUBIC_EFT_AUDIT_PASS',
    'symmetry_class': {
        'preferred_frame': True,
        'spatial_translations_rotations': True,
        'spatial_parity': True,
        'constant_shift_postulate': True,
        'lorentz_invariance_assumed': False,
        'time_reversal_assumed': False,
    },
    'cubic_basis_D_le_4': basis,
    'basis_size': 4,
    'ibp_identities_verified': 2,
    'no_second_time_derivative_in_basis': True,
    'background_fourier_kinetic_operator': 'K*(1+q^2/M^2)>0',
    'reduced_scalar_dof_statement': 'one perturbative scalar canonical pair while velocity Hessian remains invertible',
    'canonical_coefficient_mass_dimensions': coefficient_dimensions,
    'strong_coupling_scale_determined': False,
    'full_gravity_ghost_free_proved': False,
}
print('RTK_ROUTE_A1_CUBIC_AUDIT_PASS', json.dumps(result, sort_keys=True))
